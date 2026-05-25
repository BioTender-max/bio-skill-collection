from __future__ import annotations

import importlib.util
import inspect
import json
import stat
import subprocess
import sys
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch

import pytest


SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPT_PATH = SKILL_DIR / "nfcore_rnaseq_wrapper.py"
PROJECT_ROOT = SKILL_DIR.parent.parent


def _load_clawbio_module():
    spec = importlib.util.spec_from_file_location("clawbio_main_module", PROJECT_ROOT / "clawbio.py")
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_clawbio_and_capture(monkeypatch, argv: list[str]) -> dict[str, object]:
    clawbio = _load_clawbio_module()
    captured = {}

    def fake_run_skill(**kwargs):
        captured.update(kwargs)
        return {"success": True, "exit_code": 0, "output_dir": "out", "files": [], "stdout": "", "stderr": "", "duration_seconds": 0}

    monkeypatch.setattr(clawbio, "run_skill", fake_run_skill)
    monkeypatch.setattr(sys, "argv", argv)

    with pytest.raises(SystemExit) as exc:
        clawbio.main()

    assert exc.value.code == 0
    return captured


def _load_skill_module():
    spec = importlib.util.spec_from_file_location("nfcore_rnaseq_wrapper_module", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for name in (
        "command_builder",
        "errors",
        "executor",
        "outputs_parser",
        "params_builder",
        "pipeline_source",
        "preflight",
        "provenance",
        "reporting",
        "samplesheet_builder",
        "schemas",
    ):
        loaded = sys.modules.get(name)
        loaded_file = Path(getattr(loaded, "__file__", "") or "")
        if loaded is not None and (loaded_file == SKILL_DIR / f"{name}.py" or SKILL_DIR in loaded_file.parents):
            sys.modules.pop(name, None)
    if str(SKILL_DIR) in sys.path:
        sys.path.remove(str(SKILL_DIR))
    return module


def _fake_pipeline_source(version: str = "3.26.0") -> dict[str, object]:
    return {
        "source_kind": "remote_repo",
        "source_ref": "nf-core/rnaseq",
        "resolved_version": version,
        "branch": "",
        "dirty": False,
    }


def _fake_preflight() -> dict[str, object]:
    return {
        "ok": True,
        "java": {"version": "21.0.0", "path": "/usr/bin/java"},
        "nextflow": {"version": "25.04.3", "path": "/usr/local/bin/nextflow"},
        "profile": {"profile": "docker", "backend_ready": True},
        "pipeline_source": _fake_pipeline_source(),
        "references": {},
        "aligner_effective": "star_salmon",
        "handoff_available": True,
        "warnings": [],
        "samplesheet": {"sample_count": 1, "sample_names": ["sampleA"], "unknown_columns": []},
    }


def _write_samplesheet(tmp_path: Path) -> Path:
    r1 = tmp_path / "sampleA_R1.fastq.gz"
    r2 = tmp_path / "sampleA_R2.fastq.gz"
    r1.write_text("x", encoding="utf-8")
    r2.write_text("x", encoding="utf-8")
    samplesheet = tmp_path / "samplesheet.csv"
    samplesheet.write_text(
        f"sample,fastq_1,fastq_2,strandedness\nsampleA,{r1},{r2},auto\n",
        encoding="utf-8",
    )
    return samplesheet


def test_entrypoint_file_exists():
    assert SCRIPT_PATH.exists()


def test_parser_accepts_core_flags():
    module = _load_skill_module()
    args = module.build_parser().parse_args(
        [
            "--input",
            "samplesheet.csv",
            "--output",
            "out",
            "--demo",
            "--check",
            "--profile",
            "docker",
            "--pipeline-version",
            "3.26.0",
            "--pipeline-local",
            "/tmp/rnaseq",
            "--resume",
        ]
    )
    assert args.input == "samplesheet.csv"
    assert args.output == "out"
    assert args.demo is True
    assert args.check is True
    assert args.profile == "docker"
    assert args.pipeline_version == "3.26.0"
    assert args.pipeline_local == "/tmp/rnaseq"
    assert args.resume is True


@pytest.mark.parametrize(
    ("flag", "dest"),
    [
        ("--fasta", "fasta"),
        ("--genome", "genome"),
    ],
)
def test_parser_exposes_reference_flags(flag, dest):
    module = _load_skill_module()
    args = module.build_parser().parse_args(["--output", "out", flag, "/ref/file"])
    assert getattr(args, dest) == "/ref/file"


@pytest.mark.parametrize(
    ("flag", "value"),
    [
        ("--aligner", "bad_aligner"),
    ],
)
def test_parser_rejects_invalid_choices(flag, value):
    module = _load_skill_module()
    with pytest.raises(SystemExit):
        module.build_parser().parse_args(["--output", "out", flag, value])


def test_parser_defaults_match_plan():
    module = _load_skill_module()
    args = module.build_parser().parse_args(["--output", "out"])
    assert args.profile == "docker"
    assert args.pipeline_version == "3.26.0"
    # --aligner defaults to None (sentinel); star_salmon is applied after all
    # override functions run via _apply_aligner_default in _run_wrapper.
    assert args.aligner is None
    assert args.trimmer == "trimgalore"
    assert args.pseudo_aligner is None
    assert args.pseudo_aligner_kmer_size is None
    assert args.ribo_removal_tool is None
    assert args.stranded_threshold is None
    assert args.unstranded_threshold is None
    assert args.deseq2_vst is None


def test_parser_accepts_nextflow_config_flag():
    """--nextflow-config must be accepted by the argument parser and stored as a list."""
    module = _load_skill_module()
    args = module.build_parser().parse_args([
        "--output", "out",
        "--nextflow-config", "/path/to/hpc.config",
    ])
    assert hasattr(args, "nextflow_config"), "Parser must expose --nextflow-config as args.nextflow_config"
    assert "/path/to/hpc.config" in (args.nextflow_config or [])


def test_prokaryotic_coerces_default_aligner_to_bowtie2_salmon():
    """--prokaryotic with no explicit aligner must coerce to bowtie2_salmon."""
    module = _load_skill_module()
    args = module.build_parser().parse_args(["--output", "out", "--prokaryotic"])
    assert args.aligner is None  # sentinel default — no explicit aligner given
    module._apply_prokaryotic_overrides(args)
    assert args.aligner == "bowtie2_salmon"


def test_prokaryotic_does_not_coerce_explicit_aligner():
    """--prokaryotic with an explicit non-default aligner leaves the aligner unchanged."""
    module = _load_skill_module()
    args = module.build_parser().parse_args(["--output", "out", "--prokaryotic", "--aligner", "hisat2"])
    module._apply_prokaryotic_overrides(args)
    assert args.aligner == "hisat2"


def test_sync_profile_flags_sets_prokaryotic_from_profile_string():
    """_sync_profile_flags must set args.prokaryotic=True when 'prokaryotic' is in --profile."""
    module = _load_skill_module()
    args = module.build_parser().parse_args(["--output", "out", "--profile", "prokaryotic"])
    assert args.prokaryotic is False  # before sync
    module._sync_profile_flags(args)
    assert args.prokaryotic is True


@pytest.mark.parametrize("profile", [
    "docker,test",
])
def test_sync_profile_flags_sets_noinput_for_self_contained_profiles(profile):
    """_sync_profile_flags must set args._noinput=True for self-contained nf-core profiles.

    Official nf-core/rnaseq profiles (test, test_full, test_prokaryotic, etc.) ship
    with params.input in their profile config.  Running them without --input is valid
    upstream; the wrapper must not block them with MISSING_INPUT.
    _sync_profile_flags detects these profiles and sets a _noinput sentinel so
    _prepare_samplesheet and params_builder skip the input requirement.
    """
    module = _load_skill_module()
    args = module.build_parser().parse_args(["--output", "out", "--profile", profile])
    module._sync_profile_flags(args)
    assert getattr(args, "_noinput", False) is True, (
        f"_sync_profile_flags did not set _noinput=True for --profile {profile!r}"
    )


def test_sync_profile_flags_test_prokaryotic_sets_both_prokaryotic_and_noinput():
    """test_prokaryotic must trigger both _noinput (no input required) and prokaryotic (aligner coercion)."""
    module = _load_skill_module()
    args = module.build_parser().parse_args(["--output", "out", "--profile", "test_prokaryotic"])
    module._sync_profile_flags(args)
    assert getattr(args, "_noinput", False) is True, "test_prokaryotic must set _noinput"
    assert getattr(args, "prokaryotic", False) is True, "test_prokaryotic must set prokaryotic"


def test_sync_profile_flags_sets_rapid_quant_from_profile_string():
    """_sync_profile_flags must set args.rapid_quant=True when 'rapid_quant' is in --profile."""
    module = _load_skill_module()
    args = module.build_parser().parse_args(["--output", "out", "--profile", "rapid_quant"])
    assert args.rapid_quant is False  # before sync
    module._sync_profile_flags(args)
    assert args.rapid_quant is True


def test_sync_profile_flags_sets_arm_from_arm64_token():
    """--profile arm64 must set args.arm=True so params.yaml gets arm: true."""
    module = _load_skill_module()
    args = module.build_parser().parse_args(["--output", "out", "--profile", "arm64"])
    assert args.arm is False  # before sync
    module._sync_profile_flags(args)
    assert args.arm is True


def test_apply_demo_overrides_clears_all_reference_flags(capsys):
    """--demo must clear every reference/index arg before they reach params.yaml.

    The upstream `test` profile bundles sample FASTQs paired with its own
    reference data. Leaving even one reference flag (e.g. --fasta) would let
    params-file override the profile's matched ref and silently desynchronise
    samples from references — producing garbage counts with no error. This
    test pins the contract: every flag in _DEMO_CLEARED_REFERENCE_FIELDS that
    the user set must be None after _apply_demo_overrides, and the user must
    receive a single structured warning naming the cleared flags.
    """
    module = _load_skill_module()
    args = module.build_parser().parse_args([
        "--output", "out",
        "--demo",
        "--fasta", "/tmp/custom.fa",
        "--gtf", "/tmp/custom.gtf",
        "--genome", "GRCh38",
        "--star-index", "/tmp/star",
        "--salmon-index", "/tmp/salmon",
        "--transcript-fasta", "/tmp/tx.fa",
    ])
    module._apply_demo_overrides(args)
    for field in module._DEMO_CLEARED_REFERENCE_FIELDS:
        assert getattr(args, field, None) is None, (
            f"--demo did not clear {field!r}; partial overrides desync samples from refs"
        )
    captured = capsys.readouterr()
    assert "--demo ignores reference flags" in captured.err
    # The warning should name the specific flags the user actually set.
    for cleared in ("--fasta", "--gtf", "--genome", "--star-index", "--salmon-index", "--transcript-fasta"):
        assert cleared in captured.err, f"warning should list {cleared}"


def test_apply_demo_overrides_silent_when_no_refs_set(capsys):
    """--demo without any reference flags must not print the ref-clearing warning."""
    module = _load_skill_module()
    args = module.build_parser().parse_args(["--output", "out", "--demo"])
    module._apply_demo_overrides(args)
    captured = capsys.readouterr()
    assert "--demo ignores reference flags" not in captured.err


def test_debug_profile_does_not_set_noinput():
    """--profile debug must NOT set _noinput=True.

    The debug profile only enables debug logging (dumpHashes, cleanup=false).
    It does not include params.input and still requires --input from the user.
    """
    module = _load_skill_module()
    args = module.build_parser().parse_args(["--output", "out", "--profile", "debug"])
    module._sync_profile_flags(args)
    assert getattr(args, "_noinput", False) is False, (
        "--profile debug must not set _noinput — it carries no params.input"
    )


def test_prepare_samplesheet_skips_input_requirement_when_noinput(tmp_path):
    """_prepare_samplesheet must not raise MISSING_INPUT when args._noinput is True.

    This is the core of the P2 fix: when a self-contained test profile is used
    without --input, _prepare_samplesheet should behave like demo mode (no user
    samplesheet) instead of raising SkillError(MISSING_INPUT).
    """
    module = _load_skill_module()
    args = module.build_parser().parse_args(["--output", str(tmp_path), "--profile", "test_full"])
    args._noinput = True
    args.demo = False
    staging_dir = tmp_path / "staging"
    staging_dir.mkdir()
    # Must not raise SkillError
    normalized, staged, summary = module._prepare_samplesheet(args, tmp_path, staging_dir=staging_dir)
    assert normalized is not None
    assert summary["sample_count"] == 0  # no user rows, same as demo mode


def test_noinput_samplesheet_uses_noinput_filename(tmp_path):
    """_prepare_samplesheet with _noinput=True must NOT produce samplesheet.demo.csv.

    The stub written for self-contained test profiles should be named
    samplesheet.noinput.csv so that provenance audits can distinguish it
    from a real --demo run.
    """
    module = _load_skill_module()
    args = module.build_parser().parse_args(["--output", str(tmp_path), "--profile", "test_full"])
    args._noinput = True
    args.demo = False
    staging_dir = tmp_path / "staging"
    staging_dir.mkdir()

    normalized, staged, summary = module._prepare_samplesheet(args, tmp_path, staging_dir=staging_dir)
    assert "demo" not in normalized.name, (
        f"samplesheet for _noinput must not be named samplesheet.demo.csv; got {normalized.name}"
    )
    assert "noinput" in normalized.name, (
        f"samplesheet for _noinput should contain 'noinput' in the name; got {normalized.name}"
    )


def test_demo_samplesheet_still_uses_demo_filename(tmp_path):
    """--demo must still produce samplesheet.demo.csv (no regression)."""
    module = _load_skill_module()
    args = module.build_parser().parse_args(["--output", str(tmp_path), "--demo"])
    staging_dir = tmp_path / "staging"
    staging_dir.mkdir()

    normalized, staged, summary = module._prepare_samplesheet(args, tmp_path, staging_dir=staging_dir)
    assert "demo" in normalized.name, (
        f"--demo samplesheet should be named samplesheet.demo.csv; got {normalized.name}"
    )


def test_noinput_does_not_force_igenomes_ignore_in_params_builder(tmp_path):
    """params_builder must NOT write igenomes_ignore=True solely because _noinput is set.

    test_full* profiles use params.genome='GRCh37' (iGenomes); setting
    igenomes_ignore=True would prevent nf-core from resolving that genome.
    The profile itself controls igenomes_ignore — the wrapper must stay silent.
    """
    import importlib.util as _ilu
    pb_spec = _ilu.spec_from_file_location("params_builder_mod", SKILL_DIR / "params_builder.py")
    pb = _ilu.module_from_spec(pb_spec)
    pb_spec.loader.exec_module(pb)

    module = _load_skill_module()
    fake_samplesheet = tmp_path / "reproducibility" / "samplesheet.noinput.csv"
    fake_samplesheet.parent.mkdir(parents=True, exist_ok=True)
    fake_samplesheet.write_text("", encoding="utf-8")

    args = module.build_parser().parse_args(["--output", str(tmp_path), "--profile", "test_full"])
    args._noinput = True
    args.aligner = "star_salmon"  # _apply_aligner_default has not run yet

    params = pb._build_base_params(args, normalized_samplesheet=fake_samplesheet, output_dir=tmp_path)
    assert "igenomes_ignore" not in params, (
        f"_build_base_params must not set igenomes_ignore for _noinput (non-demo) runs; got {params}"
    )
    assert "input" not in params, (
        "_build_base_params must not set params.input for _noinput runs"
    )


def test_check_mode_writes_check_result_and_does_not_execute(tmp_path, monkeypatch):
    module = _load_skill_module()
    executed = []
    monkeypatch.setattr(module, "resolve_pipeline_source", lambda **kw: _fake_pipeline_source(kw["requested_version"]))
    monkeypatch.setattr(module, "run_preflight", lambda *a, **kw: _fake_preflight())
    monkeypatch.setattr(module, "execute_nextflow", lambda *a, **kw: executed.append(True))
    rc = module.main(["--output", str(tmp_path), "--demo", "--check"])
    assert rc == 0
    assert not executed
    payload = json.loads((tmp_path / "check_result.json").read_text(encoding="utf-8"))
    assert payload["ok"] is True
    assert payload["skill"] == "nfcore-rnaseq-wrapper"


def test_check_demo_passes_with_mocked_environment(tmp_path, monkeypatch):
    module = _load_skill_module()
    monkeypatch.setattr(module, "resolve_pipeline_source", lambda **kw: _fake_pipeline_source())
    monkeypatch.setattr(module, "run_preflight", lambda *a, **kw: _fake_preflight())
    rc = module.main(["--output", str(tmp_path), "--demo", "--check", "--profile", "docker"])
    assert rc == 0
    assert (tmp_path / "reproducibility" / "samplesheet.demo.csv").exists()



def test_run_execution_mode_builds_params_before_command(tmp_path, monkeypatch):
    module = _load_skill_module()
    order = []
    captured_success = {}
    params_path = tmp_path / "reproducibility" / "params.yaml"
    params_path.parent.mkdir()

    monkeypatch.setattr(module, "build_effective_params", lambda *a, **kw: order.append("params") or {"outdir": "x", "aligner": "star_salmon"})
    monkeypatch.setattr(module, "check_resume_params_checksum", lambda *a, **kw: order.append("params_checksum"))
    monkeypatch.setattr(module, "check_resume_samplesheet_checksum", lambda *a, **kw: order.append("samplesheet_checksum"))
    monkeypatch.setattr(module, "write_params_yaml", lambda *a, **kw: order.append("write_params") or params_path)
    monkeypatch.setattr(module, "execute_nextflow", lambda *a, **kw: order.append("execute") or {"returncode": 0})
    monkeypatch.setattr(module, "parse_outputs", lambda *a, **kw: {"preferred_counts_tsv": "counts.tsv", "handoff_available": True})
    monkeypatch.setattr(
        module,
        "_write_success_outputs",
        lambda *a, **kw: order.append("success_outputs") or captured_success.update(parsed_outputs=kw["parsed_outputs"]),
    )

    args = Namespace(
        aligner="star_salmon",
        demo=False,
        profile="docker",
        prokaryotic=False,
        resume=True,
        run_downstream=True,
        skip_downstream=False,
    )
    staged = tmp_path / "stage.csv"
    staged.write_text("ok", encoding="utf-8")
    normalized = tmp_path / "reproducibility" / "samplesheet.valid.csv"
    rc = module._run_execution_mode(
        args,
        output_dir=tmp_path,
        pipeline_source=_fake_pipeline_source(),
        preflight_result=_fake_preflight(),
        normalized_samplesheet=normalized,
        staged_samplesheet=staged,
        samplesheet_summary={"sample_count": 1},
    )
    assert rc == 0
    assert order[:5] == ["params", "params_checksum", "samplesheet_checksum", "write_params", "execute"]
    assert (tmp_path / "reproducibility" / "rnaseq_de_handoff.sh").exists()
    assert captured_success["parsed_outputs"]["rnaseq_de_handoff"].endswith("rnaseq_de_handoff.sh")
    assert "rnaseq_de_output_dir" not in captured_success["parsed_outputs"]
    assert captured_success["parsed_outputs"]["rnaseq_de_status"] == "template_only"


# ── Task 9: Mocked Nextflow end-to-end integration test ───────────────────


def _write_fake_star_salmon_artifacts(output_dir: Path) -> Path:
    counts = output_dir / "upstream" / "results" / "star_salmon" / "salmon.merged.gene_counts.tsv"
    counts.parent.mkdir(parents=True, exist_ok=True)
    counts.write_text("gene_id\tsampleA\nGENE1\t100\n", encoding="utf-8")
    multiqc = output_dir / "upstream" / "results" / "multiqc" / "star_salmon" / "multiqc_report.html"
    multiqc.parent.mkdir(parents=True, exist_ok=True)
    multiqc.write_text("<html>multiqc</html>", encoding="utf-8")
    pipeline_info = output_dir / "upstream" / "results" / "pipeline_info"
    pipeline_info.mkdir(parents=True, exist_ok=True)
    (pipeline_info / "execution_report.html").write_text("<html>exec</html>", encoding="utf-8")
    return counts


def test_mocked_nextflow_end_to_end_writes_all_expected_outputs(tmp_path, monkeypatch):
    module = _load_skill_module()
    counts_path = _write_fake_star_salmon_artifacts(tmp_path)

    def fake_execute_nextflow(command, cwd, output_dir, timeout_seconds):
        logs = Path(output_dir) / "logs"
        logs.mkdir(parents=True, exist_ok=True)
        stdout_log = logs / "nextflow.stdout.log"
        stderr_log = logs / "nextflow.stderr.log"
        stdout_log.write_text("Completed successfully", encoding="utf-8")
        stderr_log.write_text("", encoding="utf-8")
        return {"returncode": 0, "stdout_log": str(stdout_log), "stderr_log": str(stderr_log)}

    monkeypatch.setattr(module, "execute_nextflow", fake_execute_nextflow)
    monkeypatch.setattr(module, "time", Namespace(monotonic=iter([0.0, 5.123]).__next__), raising=False)

    samplesheet = tmp_path / "reproducibility" / "samplesheet.valid.csv"
    samplesheet.parent.mkdir(parents=True, exist_ok=True)
    samplesheet.write_text("sample,fastq_1,strandedness\nsampleA,/data/R1.fastq.gz,auto\n", encoding="utf-8")

    args = Namespace(
        aligner="star_salmon",
        demo=True,
        profile="docker",
        prokaryotic=False,
        resume=False,
        run_downstream=False,
        skip_downstream=False,
        pseudo_aligner=None,
        pipeline_version="3.26.0",
        pipeline_local=None,
    )

    rc = module._run_execution_mode(
        args,
        output_dir=tmp_path,
        pipeline_source=_fake_pipeline_source(),
        preflight_result=_fake_preflight(),
        normalized_samplesheet=samplesheet,
        staged_samplesheet=samplesheet,
        samplesheet_summary={"sample_count": 1, "sample_names": ["sampleA"], "unknown_columns": []},
    )

    assert rc == 0
    assert (tmp_path / "report.md").exists()
    assert (tmp_path / "result.json").exists()
    result = json.loads((tmp_path / "result.json").read_text(encoding="utf-8"))
    assert result["summary"]["preferred_counts_tsv"] == str(counts_path)
    assert (tmp_path / "provenance" / "runtime.json").exists()
    runtime = json.loads((tmp_path / "provenance" / "runtime.json").read_text(encoding="utf-8"))
    assert runtime["duration_seconds"] == 5.123
    assert (tmp_path / "reproducibility" / "commands.sh").exists()


def test_run_downstream_handoff_template_only_without_required_flags(tmp_path):
    module = _load_skill_module()
    args = Namespace(run_downstream=True, skip_downstream=False, metadata=None, formula=None, contrast=None, downstream_output=None)
    with patch("subprocess.run") as run:
        result = module._run_downstream_handoff(
            args,
            parsed_outputs={"preferred_counts_tsv": "counts.tsv", "handoff_available": True},
            output_dir=tmp_path,
        )
    run.assert_not_called()
    assert result == {
        "template_path": str(tmp_path / "reproducibility" / "rnaseq_de_handoff.sh"),
        "downstream_output_dir": None,
        "downstream_status": "template_only",
        "downstream_returncode": None,
    }
    assert (tmp_path / "reproducibility" / "rnaseq_de_handoff.sh").exists()


def test_run_downstream_handoff_launches_rnaseq_de_when_required_flags_present(tmp_path, monkeypatch):
    module = _load_skill_module()
    launched = {}
    args = Namespace(
        run_downstream=True,
        skip_downstream=False,
        metadata=str(tmp_path / "meta with spaces.csv"),
        formula="~ batch + condition",
        contrast="condition,treated,control",
        downstream_output=None,
    )

    def fake_run(cmd, capture_output, text, timeout, cwd):
        launched["cmd"] = cmd
        launched["capture_output"] = capture_output
        launched["text"] = text
        launched["timeout"] = timeout
        launched["cwd"] = cwd
        return subprocess.CompletedProcess(cmd, 0, stdout="ok", stderr="")

    monkeypatch.setattr(module.subprocess, "run", fake_run)
    result = module._run_downstream_handoff(
        args,
        parsed_outputs={"preferred_counts_tsv": str(tmp_path / "counts with spaces.tsv"), "handoff_available": True},
        output_dir=tmp_path,
    )
    assert result == {
        "template_path": str(tmp_path / "reproducibility" / "rnaseq_de_handoff.sh"),
        "downstream_output_dir": str(tmp_path / "rnaseq_de"),
        "downstream_status": "completed",
        "downstream_returncode": 0,
    }
    assert launched["cmd"][:4] == [sys.executable, str(PROJECT_ROOT / "clawbio.py"), "run", "rnaseq"]
    assert launched["cmd"] == [
        sys.executable,
        str(PROJECT_ROOT / "clawbio.py"),
        "run",
        "rnaseq",
        "--counts",
        str(tmp_path / "counts with spaces.tsv"),
        "--metadata",
        str(tmp_path / "meta with spaces.csv"),
        "--formula",
        "~ batch + condition",
        "--contrast",
        "condition,treated,control",
        "--output",
        str(tmp_path / "rnaseq_de"),
    ]
    assert launched["capture_output"] is True
    assert launched["text"] is True
    assert launched["timeout"] == 60 * 60 * 2
    assert launched["cwd"] == str(PROJECT_ROOT)


def test_downstream_handoff_uses_absolute_clawbio_path(tmp_path, monkeypatch):
    """_run_downstream_handoff must invoke clawbio.py via its absolute path."""
    module = _load_skill_module()
    import pathlib

    captured_commands = []

    def fake_run(cmd, **kwargs):
        captured_commands.append(list(cmd))
        return subprocess.CompletedProcess(cmd, returncode=0, stdout="", stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)

    # Write a stub clawbio.py so the existence check passes
    fake_clawbio = module._PROJECT_ROOT / "clawbio.py"
    already_exists = fake_clawbio.exists()
    if not already_exists:
        fake_clawbio.write_text("# stub\n", encoding="utf-8")

    try:
        counts = str(tmp_path / "counts.tsv")
        pathlib.Path(counts).write_text("gene\ts1\n", encoding="utf-8")
        meta = str(tmp_path / "meta.csv")
        pathlib.Path(meta).write_text("sample,condition\n", encoding="utf-8")

        args = Namespace(
            run_downstream=True,
            skip_downstream=False,
            metadata=meta,
            formula="~ condition",
            contrast="condition,treated,control",
            downstream_output=None,
        )
        parsed_outputs = {"preferred_counts_tsv": counts, "handoff_available": True}

        module._run_downstream_handoff(args, parsed_outputs=parsed_outputs, output_dir=tmp_path)
    finally:
        if not already_exists:
            fake_clawbio.unlink(missing_ok=True)

    assert captured_commands, "subprocess.run was never called"
    invoked = pathlib.Path(captured_commands[0][1])
    assert invoked.is_absolute(), (
        f"clawbio.py was invoked via a relative path: {captured_commands[0][1]!r}"
    )


def test_downstream_handoff_warns_when_clawbio_missing(tmp_path, monkeypatch, capsys):
    """_run_downstream_handoff must warn and return error status if clawbio.py is absent."""
    module = _load_skill_module()
    import pathlib

    fake_root = tmp_path / "fake_project"
    fake_root.mkdir()
    monkeypatch.setattr(module, "_PROJECT_ROOT", fake_root)
    # clawbio.py does NOT exist in fake_root

    counts = str(tmp_path / "counts.tsv")
    pathlib.Path(counts).write_text("gene\ts1\n", encoding="utf-8")
    meta = str(tmp_path / "meta.csv")
    pathlib.Path(meta).write_text("sample,condition\n", encoding="utf-8")

    args = Namespace(
        run_downstream=True,
        skip_downstream=False,
        metadata=meta,
        formula="~ condition",
        contrast="condition,treated,control",
        downstream_output=None,
    )
    parsed_outputs = {"preferred_counts_tsv": counts, "handoff_available": True}

    result = module._run_downstream_handoff(args, parsed_outputs=parsed_outputs, output_dir=tmp_path)

    captured = capsys.readouterr()
    assert "WARNING" in captured.err, f"Expected WARNING in stderr, got: {captured.err!r}"
    assert result["downstream_status"] == "error"


def test_resume_uses_staging_to_preserve_previous_artifacts(tmp_path, monkeypatch):
    module = _load_skill_module()
    previous = tmp_path / "reproducibility" / "samplesheet.valid.csv"
    previous.parent.mkdir(parents=True)
    previous.write_text("previous\n", encoding="utf-8")
    samplesheet = _write_samplesheet(tmp_path)

    def fake_preflight(*a, **kw):
        raise module.SkillError("preflight", "INVALID_RESUME_STATE", "bad resume", "fix", {})

    monkeypatch.setattr(module, "resolve_pipeline_source", lambda **kw: _fake_pipeline_source())
    monkeypatch.setattr(module, "run_preflight", fake_preflight)
    rc = module.main(["--input", str(samplesheet), "--output", str(tmp_path), "--genome", "GRCh38", "--resume"])
    assert rc == 1
    assert previous.read_text(encoding="utf-8") == "previous\n"


def test_main_writes_json_skill_error_to_stderr(tmp_path, capsys, monkeypatch):
    module = _load_skill_module()
    monkeypatch.setattr(
        module,
        "resolve_pipeline_source",
        lambda **kw: (_ for _ in ()).throw(module.SkillError("preflight", "PIPELINE_SOURCE_INVALID", "bad", "fix", {})),
    )
    rc = module.main(["--output", str(tmp_path), "--demo"])
    assert rc == 1
    payload = json.loads(capsys.readouterr().err)
    assert payload["ok"] is False
    assert payload["error_code"] == "PIPELINE_SOURCE_INVALID"


def test_main_writes_json_unexpected_error_to_stderr(tmp_path, capsys, monkeypatch):
    module = _load_skill_module()
    monkeypatch.setattr(module, "resolve_pipeline_source", lambda **kw: (_ for _ in ()).throw(RuntimeError("boom")))
    rc = module.main(["--output", str(tmp_path), "--demo"])
    assert rc == 1
    payload = json.loads(capsys.readouterr().err)
    assert payload["error_code"] == "UNEXPECTED_ERROR"
    assert payload["details"]["exception_type"] == "RuntimeError"


def test_macos_docker_config_has_audited_rnaseq_content(tmp_path):
    module = _load_skill_module()
    config_path = module._write_macos_docker_config(tmp_path)
    assert config_path == tmp_path / ".nextflow_macos_docker.config"
    content = config_path.read_text(encoding="utf-8")
    assert "stageInMode = 'copy'" in content
    assert "--platform linux/amd64" in content
    assert "containerOptions" in content
    assert "resourceLimits" in content
    assert "STARsolo" not in content
    assert "ext.args" not in content
    assert not (tmp_path / "reproducibility" / "macos_docker.config").exists()


def test_rapid_quant_override_sets_profile_implied_args():
    """--rapid-quant must sync skip_alignment, pseudo_aligner, skip_quantification_merge."""
    module = _load_skill_module()
    args = module.build_parser().parse_args(["--output", "out", "--rapid-quant"])
    assert args.pseudo_aligner is None
    assert args.skip_alignment is False
    assert args.skip_quantification_merge is False
    module._apply_rapid_quant_overrides(args)
    assert args.pseudo_aligner == "salmon"
    assert args.skip_alignment is True
    assert args.skip_quantification_merge is True


def test_rapid_quant_override_respects_explicit_pseudo_aligner():
    """--rapid-quant must not override an explicit --pseudo-aligner."""
    module = _load_skill_module()
    args = module.build_parser().parse_args(["--output", "out", "--rapid-quant", "--pseudo-aligner", "kallisto"])
    module._apply_rapid_quant_overrides(args)
    assert args.pseudo_aligner == "kallisto"


def test_rapid_quant_override_no_op_when_not_set():
    """_apply_rapid_quant_overrides must not touch args when --rapid-quant is not passed."""
    module = _load_skill_module()
    args = module.build_parser().parse_args(["--output", "out"])
    module._apply_rapid_quant_overrides(args)
    assert args.pseudo_aligner is None
    assert args.skip_alignment is False
    assert args.skip_quantification_merge is False


# ── Step 2: _write_success_outputs provenance isolation ──────────────────────


def test_write_success_outputs_calls_write_report_even_if_provenance_raises(tmp_path, monkeypatch):
    """If write_provenance_bundle raises, write_report and write_result must still be called."""
    module = _load_skill_module()
    calls = []
    monkeypatch.setattr(module, "write_repro_commands", lambda *a, **kw: None)
    monkeypatch.setattr(module, "write_provenance_bundle", lambda *a, **kw: (_ for _ in ()).throw(RuntimeError("disk full")))
    monkeypatch.setattr(module, "write_report", lambda *a, **kw: calls.append("write_report"))
    monkeypatch.setattr(module, "write_result", lambda *a, **kw: calls.append("write_result"))

    params = tmp_path / "reproducibility" / "params.yaml"
    samplesheet = tmp_path / "reproducibility" / "samplesheet.valid.csv"
    params.parent.mkdir(parents=True)
    params.write_text("{}", encoding="utf-8")
    samplesheet.write_text("x", encoding="utf-8")

    module._write_success_outputs(
        tmp_path,
        args=Namespace(aligner="star_salmon", profile="docker", demo=False,
                       resume=False, pseudo_aligner=None, prokaryotic=False),
        pipeline_source=_fake_pipeline_source(),
        preflight_result=_fake_preflight(),
        params_path=params,
        params_payload={"aligner": "star_salmon"},
        normalized_samplesheet=samplesheet,
        samplesheet_summary={"sample_count": 1, "fastq_paths": []},
        parsed_outputs={"preferred_counts_tsv": "/counts.tsv"},
        execution_result={},
        command_str="nextflow run nf-core/rnaseq",
    )
    assert "write_report" in calls, "write_report must be called even when provenance fails"
    assert "write_result" in calls, "write_result must be called even when provenance fails"


def test_write_success_outputs_passes_provenance_warnings_to_write_report(tmp_path, monkeypatch):
    """A provenance failure must produce a post_run_warnings entry passed to write_report."""
    module = _load_skill_module()
    captured_warnings = {}
    monkeypatch.setattr(module, "write_repro_commands", lambda *a, **kw: None)
    monkeypatch.setattr(module, "write_provenance_bundle", lambda *a, **kw: (_ for _ in ()).throw(OSError("no space left")))
    monkeypatch.setattr(module, "write_report", lambda *a, **kw: captured_warnings.update(post_run_warnings=kw.get("post_run_warnings", [])))
    monkeypatch.setattr(module, "write_result", lambda *a, **kw: None)

    params = tmp_path / "reproducibility" / "params.yaml"
    samplesheet = tmp_path / "reproducibility" / "samplesheet.valid.csv"
    params.parent.mkdir(parents=True)
    params.write_text("{}", encoding="utf-8")
    samplesheet.write_text("x", encoding="utf-8")

    module._write_success_outputs(
        tmp_path,
        args=Namespace(aligner="star_salmon", profile="docker", demo=False,
                       resume=False, pseudo_aligner=None, prokaryotic=False),
        pipeline_source=_fake_pipeline_source(),
        preflight_result=_fake_preflight(),
        params_path=params,
        params_payload={"aligner": "star_salmon"},
        normalized_samplesheet=samplesheet,
        samplesheet_summary={"sample_count": 1, "fastq_paths": []},
        parsed_outputs={"preferred_counts_tsv": "/counts.tsv"},
        execution_result={},
        command_str="nextflow run nf-core/rnaseq",
    )
    warnings = captured_warnings.get("post_run_warnings", [])
    assert len(warnings) >= 1, "Expected at least one post_run_warning from the provenance failure"
    assert any("provenance" in w.lower() or "OSError" in w or "no space" in w.lower() for w in warnings)


def test_clawbio_nextflow_config_in_rnaseq_pipeline_allowlist():
    """--nextflow-config must be in the rnaseq-pipeline allowed_extra_flags so it
    survives the SEC INT-001 filter inside run_skill.  Regression test for the P1 bug
    where the flag was absent from the allowlist and silently dropped."""
    clawbio = _load_clawbio_module()
    rnaseq_info = clawbio.SKILLS.get("rnaseq-pipeline", {})
    allowed = rnaseq_info.get("allowed_extra_flags", set())
    assert "--nextflow-config" in allowed, (
        "--nextflow-config must be in SKILLS['rnaseq-pipeline']['allowed_extra_flags']; "
        f"got allowed={sorted(allowed)!r}"
    )


def test_clawbio_nextflow_config_forwarded_to_rnaseq_pipeline(monkeypatch):
    """--nextflow-config values passed to clawbio.py run rnaseq-pipeline must reach
    run_skill's extra_args with both occurrences preserved (action='append' in wrapper).
    The allowlist check above guarantees they also survive SEC INT-001."""
    captured = _run_clawbio_and_capture(
        monkeypatch,
        [
            "clawbio.py", "run", "rnaseq-pipeline",
            "--nextflow-config", "/tmp/hpc.config",
            "--nextflow-config", "/tmp/rsem.config",
            "--output", "/tmp/out",
        ],
    )
    extra = captured.get("extra_args") or []
    assert "--nextflow-config" in extra, (
        "--nextflow-config must reach run_skill via extra_args; "
        f"got extra_args={extra!r}"
    )
    config_values = [extra[i + 1] for i, v in enumerate(extra) if v == "--nextflow-config"]
    assert "/tmp/hpc.config" in config_values, f"hpc.config missing from extra_args: {extra!r}"
    assert "/tmp/rsem.config" in config_values, f"rsem.config missing from extra_args: {extra!r}"


def test_clawbio_star_index_forwarded_to_rnaseq_pipeline(monkeypatch):
    """--star-index passed to 'clawbio run rnaseq-pipeline' must reach run_skill via
    extra_args.  Regression test: the flag was declared in run_parser (→ args) but was
    absent from the rnaseq-pipeline value_flag forwarding loop, so it was silently dropped."""
    captured = _run_clawbio_and_capture(
        monkeypatch,
        [
            "clawbio.py", "run", "rnaseq-pipeline",
            "--star-index", "/refs/star_index",
            "--output", "/tmp/out",
        ],
    )
    extra = captured.get("extra_args") or []
    idx = next((i for i, v in enumerate(extra) if v == "--star-index"), None)
    assert idx is not None, f"--star-index not found in extra_args: {extra!r}"
    assert extra[idx + 1] == "/refs/star_index", f"wrong value after --star-index: {extra!r}"


def test_clawbio_kallisto_index_forwarded_to_rnaseq_pipeline(monkeypatch):
    """--kallisto-index passed to 'clawbio run rnaseq-pipeline' must reach run_skill
    via extra_args.  Regression test: absent from the rnaseq-pipeline value_flag loop."""
    captured = _run_clawbio_and_capture(
        monkeypatch,
        [
            "clawbio.py", "run", "rnaseq-pipeline",
            "--kallisto-index", "/refs/kallisto_index",
            "--output", "/tmp/out",
        ],
    )
    extra = captured.get("extra_args") or []
    idx = next((i for i, v in enumerate(extra) if v == "--kallisto-index"), None)
    assert idx is not None, f"--kallisto-index not found in extra_args: {extra!r}"
    assert extra[idx + 1] == "/refs/kallisto_index", f"wrong value after --kallisto-index: {extra!r}"
