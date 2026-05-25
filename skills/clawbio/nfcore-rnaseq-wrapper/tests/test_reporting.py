from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import pytest

_SKILL_DIR = Path(__file__).resolve().parent.parent
if str(_SKILL_DIR) in sys.path:
    sys.path.remove(str(_SKILL_DIR))
sys.path.insert(0, str(_SKILL_DIR))


def _purge_foreign_bare_modules(*names: str) -> None:
    for name in names:
        module = sys.modules.get(name)
        module_file = Path(getattr(module, "__file__", "") or "")
        if module is not None and _SKILL_DIR not in module_file.parents and module_file != _SKILL_DIR / f"{name}.py":
            sys.modules.pop(name, None)


def _purge_local_modules(*names: str) -> None:
    for name in names:
        module = sys.modules.get(name)
        module_file = Path(getattr(module, "__file__", "") or "")
        if module is not None and (module_file == _SKILL_DIR / f"{name}.py" or _SKILL_DIR in module_file.parents):
            sys.modules.pop(name, None)


_purge_foreign_bare_modules("reporting", "schemas")

from reporting import build_repro_command_args, write_check_result, write_report, write_repro_commands, write_result

_purge_local_modules("reporting", "schemas")
if str(_SKILL_DIR) in sys.path:
    sys.path.remove(str(_SKILL_DIR))


def _args(tmp_path: Path, **kwargs) -> argparse.Namespace:
    defaults = dict(
        input=str(tmp_path / "samplesheet.csv"),
        output=str(tmp_path / "out"),
        aligner="star_salmon",
        pseudo_aligner=None,
        trimmer="trimgalore",
        profile="docker",
        pipeline_version="3.26.0",
        pipeline_local=None,
        resume=False,
        demo=False,
        check=False,
        run_downstream=False,
        metadata=None,
        formula=None,
        contrast=None,
        downstream_output=None,
        skip_quantification_merge=False,
        skip_trimming=False,
        skip_alignment=False,
        skip_pseudo_alignment=False,
        skip_markduplicates=False,
        skip_bigwig=False,
        skip_stringtie=False,
        skip_fastqc=False,
        skip_dupradar=False,
        skip_qualimap=False,
        skip_rseqc=False,
        skip_biotype_qc=False,
        skip_deseq2_qc=False,
        skip_multiqc=False,
        skip_qc=False,
        save_reference=False,
        save_trimmed=False,
        save_align_intermeds=False,
        save_unaligned=False,
        save_merged_fastq=False,
        save_non_ribo_reads=False,
        save_umi_intermeds=False,
        gencode=False,
        deseq2_vst=None,
        fasta=None,
        gtf=None,
        gff=None,
        transcript_fasta=None,
        additional_fasta=None,
        gene_bed=None,
        splicesites=None,
        star_index=None,
        rsem_index=None,
        hisat2_index=None,
        bowtie2_index=None,
        salmon_index=None,
        kallisto_index=None,
        genome=None,
        remove_ribo_rna=False,
        ribo_removal_tool=None,
        with_umi=False,
        skip_umi_extract=False,
        umi_dedup_tool=None,
        umitools_bc_pattern=None,
        umitools_bc_pattern2=None,
        umitools_umi_separator=None,
        umitools_extract_method=None,
        umi_discard_read=None,
        umitools_grouping_method=None,
        stranded_threshold=None,
        unstranded_threshold=None,
        min_mapped_reads=None,
        pseudo_aligner_kmer_size=None,
        extra_trimgalore_args=None,
        extra_fastp_args=None,
        extra_salmon_quant_args=None,
        extra_kallisto_quant_args=None,
        min_trimmed_reads=None,
        seq_center=None,
        seq_platform=None,
        salmon_quant_libtype=None,
        kallisto_quant_fraglen=None,
        kallisto_quant_fraglen_sd=None,
        featurecounts_feature_type=None,
        featurecounts_group_type=None,
        gtf_extra_attributes=None,
        gtf_group_features=None,
        rseqc_modules=None,
        extra_star_align_args=None,
        extra_bowtie2_align_args=None,
        star_ignore_sjdbgtf=False,
        bam_csi_index=False,
        stringtie_ignore_gtf=False,
        email=None,
        multiqc_title=None,
        multiqc_config=None,
        multiqc_logo=None,
        enable_preseq=False,
        prokaryotic=False,
        contaminant_screening=None,
        contaminant_screening_input=None,
        kraken_db=None,
        bracken_precision=None,
        sylph_db=None,
        sylph_taxonomy=None,
        bbsplit_fasta_list=None,
        bbsplit_index=None,
        save_kraken_assignments=False,
        save_kraken_unassigned=False,
        rsem_extra_args=None,
        skip_downstream=False,
        nextflow_config=None,
        skip_bbsplit=False,
        igenomes_base=None,
        publish_dir_mode=None,
        email_on_fail=None,
    )
    defaults.update(kwargs)
    return argparse.Namespace(**defaults)


def _source() -> dict:
    return {"source_kind": "remote_tag", "source_ref": "3.26.0", "resolved_version": "3.26.0"}


def _preflight() -> dict:
    return {
        "java": {"version": "21.0.1"},
        "nextflow": {"version": "25.04.3"},
        "warnings": [],
    }


def _parsed(**kwargs) -> dict:
    defaults = dict(
        aligner_effective="star_salmon",
        preferred_counts_tsv="/out/star_salmon/salmon.merged.gene_counts_length_scaled.tsv",
        raw_counts_tsv="/out/star_salmon/salmon.merged.gene_counts.tsv",
        tpm_tsv="/out/star_salmon/salmon.merged.gene_tpm.tsv",
        rds_file="/out/star_salmon/salmon.merged.gene.SummarizedExperiment.rds",
        tx2gene_augmented="/out/star_salmon/salmon.merged.tx2gene_augmented.tsv",
        per_sample_quant_dirs=[],
        rsem_genes_results=[],
        multiqc_report="/out/multiqc/star_salmon/multiqc_report.html",
        pipeline_info_dir="/out/pipeline_info",
        samples_detected=2,
        handoff_available=True,
        hisat2_no_quant=False,
        skip_quantification_merge=False,
    )
    defaults.update(kwargs)
    return defaults


def test_write_report_creates_rnaseq_report(tmp_path):
    path = write_report(tmp_path, args=_args(tmp_path), pipeline_source=_source(), preflight_result=_preflight(), parsed_outputs=_parsed(), command_str="nextflow run nf-core/rnaseq")
    assert path == tmp_path / "report.md"
    assert "# nf-core/rnaseq Wrapper Report" in path.read_text(encoding="utf-8")


def test_report_summary_contains_bulk_rnaseq_fields(tmp_path):
    write_report(tmp_path, args=_args(tmp_path, pseudo_aligner="salmon", trimmer="fastp"), pipeline_source=_source(), preflight_result=_preflight(), parsed_outputs=_parsed(samples_detected=3), command_str="cmd")
    content = (tmp_path / "report.md").read_text(encoding="utf-8")
    assert "Pseudo-aligner: `salmon`" in content
    assert "Trimmer: `fastp`" in content
    assert "Samples: `3`" in content


def test_report_next_steps_emit_rnaseq_de_template(tmp_path):
    write_report(tmp_path, args=_args(tmp_path), pipeline_source=_source(), preflight_result=_preflight(), parsed_outputs=_parsed(), command_str="cmd")
    content = (tmp_path / "report.md").read_text(encoding="utf-8")
    # Must use CLAWBIO_REPO anchor so the command works from any directory.
    assert '"${CLAWBIO_REPO}/clawbio.py" run rnaseq' in content
    assert "python clawbio.py run rnaseq" not in content
    assert "--counts /out/star_salmon/salmon.merged.gene_counts_length_scaled.tsv" in content
    assert "<your_metadata.csv>" in content
    assert "--formula" in content
    assert "--contrast" in content


def test_report_replay_line_includes_clawbio_repo(tmp_path):
    """The Replay line in report.md must include the CLAWBIO_REPO prefix so users
    can copy-paste it directly — commands.sh requires the env var to be set."""
    write_report(tmp_path, args=_args(tmp_path), pipeline_source=_source(), preflight_result=_preflight(), parsed_outputs=_parsed(), command_str="cmd")
    content = (tmp_path / "report.md").read_text(encoding="utf-8")
    assert "CLAWBIO_REPO=" in content
    assert "bash" in content
    assert "commands.sh" in content


def test_report_handoff_quotes_counts_path_with_spaces(tmp_path):
    write_report(
        tmp_path,
        args=_args(tmp_path),
        pipeline_source=_source(),
        preflight_result=_preflight(),
        parsed_outputs=_parsed(preferred_counts_tsv="/tmp/run with spaces/counts.tsv"),
        command_str="nextflow run nf-core/rnaseq",
    )
    content = (tmp_path / "report.md").read_text(encoding="utf-8")
    assert "--counts '/tmp/run with spaces/counts.tsv' \\" in content


def test_report_next_steps_explain_hisat2_no_handoff(tmp_path):
    parsed = _parsed(preferred_counts_tsv="", handoff_available=False, hisat2_no_quant=True)
    write_report(tmp_path, args=_args(tmp_path, aligner="hisat2"), pipeline_source=_source(), preflight_result=_preflight(), parsed_outputs=parsed, command_str="cmd")
    content = (tmp_path / "report.md").read_text(encoding="utf-8")
    assert "HISAT2" in content
    assert "rnaseq" in content


def test_write_result_summary_contains_handoff_keys(tmp_path):
    result_path = write_result(tmp_path, args=_args(tmp_path), pipeline_source=_source(), parsed_outputs=_parsed(), command_str="cmd")
    payload = json.loads(result_path.read_text(encoding="utf-8"))
    summary = payload["summary"]
    assert summary["preferred_counts_tsv"] == _parsed()["preferred_counts_tsv"]
    assert summary["handoff_available"] is True
    assert summary["hisat2_no_quant"] is False
    assert summary["skip_quantification_merge"] is False


def test_write_result_data_contains_full_outputs(tmp_path):
    parsed = _parsed(samples_detected=7)
    result_path = write_result(tmp_path, args=_args(tmp_path), pipeline_source=_source(), parsed_outputs=parsed, command_str="cmd")
    payload = json.loads(result_path.read_text(encoding="utf-8"))
    assert payload["data"]["canonical_skill_name"] == "nfcore-rnaseq-wrapper"
    assert payload["data"]["cli_alias"] == "rnaseq-pipeline"
    assert payload["data"]["outputs"] == parsed
    assert payload["data"]["output_artifacts"] == parsed


def test_write_repro_commands_uses_rnaseq_script_name(tmp_path):
    write_repro_commands(tmp_path, args=_args(tmp_path))
    content = (tmp_path / "reproducibility" / "commands.sh").read_text(encoding="utf-8")
    assert "nfcore_rnaseq_wrapper.py" in content
    assert "nfcore_scrnaseq_wrapper.py" not in content


def test_write_repro_commands_appends_portability_notice_for_real_run(tmp_path):
    write_repro_commands(tmp_path, args=_args(tmp_path, demo=False))
    content = (tmp_path / "reproducibility" / "commands.sh").read_text(encoding="utf-8")
    assert "Portability notice" in content
    assert "remap_paths.py" in content


def test_write_repro_commands_skips_portability_notice_for_demo(tmp_path):
    write_repro_commands(tmp_path, args=_args(tmp_path, demo=True))
    content = (tmp_path / "reproducibility" / "commands.sh").read_text(encoding="utf-8")
    assert "Portability notice" not in content


def test_build_repro_command_args_includes_rnaseq_core_flags(tmp_path):
    command_args = build_repro_command_args(tmp_path, args=_args(tmp_path, aligner="star_rsem", profile="singularity"))
    assert command_args["--output"] == tmp_path.as_posix()
    assert command_args["--aligner"] == "star_rsem"
    assert command_args["--profile"] == "singularity"
    assert command_args["--pipeline-version"] == "3.26.0"


def test_build_repro_command_args_includes_reference_paths(tmp_path):
    fasta = tmp_path / "ref.fa"
    gtf = tmp_path / "genes.gtf"
    command_args = build_repro_command_args(tmp_path, args=_args(tmp_path, fasta=str(fasta), gtf=str(gtf)))
    assert command_args["--fasta"] == fasta.resolve().as_posix()
    assert command_args["--gtf"] == gtf.resolve().as_posix()


def test_build_repro_command_args_demo_omits_input(tmp_path):
    command_args = build_repro_command_args(tmp_path, args=_args(tmp_path, demo=True))
    assert "--demo" in command_args
    assert "--input" not in command_args


def test_build_repro_command_args_real_run_uses_bundle_samplesheet(tmp_path):
    command_args = build_repro_command_args(tmp_path, args=_args(tmp_path, input=str(tmp_path / "ss.csv")))
    assert command_args["--input"] == "${SCRIPT_DIR}/samplesheet.valid.csv"


# ── P1: reporting fixes for _noinput, remote refs, --nextflow-config ──────────


def test_build_repro_command_args_noinput_includes_profile(tmp_path):
    """commands.sh for self-contained profiles must preserve --profile so replay is correct."""
    args = _args(tmp_path, input=None, demo=False, profile="docker,test_full")
    args._noinput = True
    result = build_repro_command_args(tmp_path, args=args)
    assert result.get("--profile") == "docker,test_full"


@pytest.mark.parametrize("scheme,field", [
    ("https", "fasta"),
])
def test_build_repro_command_args_remote_refs_not_mangled(tmp_path, scheme, field):
    """Remote URI refs in commands.sh must be written unchanged, not resolved through Path.

    Path(value).resolve() turns 'https://example.org/genome.fa' into
    '/.../https:/example.org/genome.fa', breaking replay.  _REPRO_PATH_FLAGS
    fields must use URI-aware serialization.
    """
    uri = f"{scheme}://bucket.example.org/refs/file.fa"
    args = _args(tmp_path, **{field: uri})
    result = build_repro_command_args(tmp_path, args=args)
    flag = f"--{field.replace('_', '-')}"
    assert result.get(flag) == uri, (
        f"commands.sh must write remote URI {uri!r} unchanged; got {result.get(flag)!r}"
    )


def test_build_repro_command_args_nextflow_config_included(tmp_path):
    """--nextflow-config paths must appear in build_repro_command_args output.

    If a user ran with --nextflow-config hpc.config --nextflow-config rsem.config,
    commands.sh must include those flags so the replay is reproducible.
    """
    cfg1 = tmp_path / "hpc.config"
    cfg2 = tmp_path / "rsem.config"
    cfg1.write_text("", encoding="utf-8")
    cfg2.write_text("", encoding="utf-8")
    args = _args(tmp_path, nextflow_config=[str(cfg1), str(cfg2)])
    result = build_repro_command_args(tmp_path, args=args)
    assert "--nextflow-config" in result, "--nextflow-config must appear in repro command args"
    configs = result["--nextflow-config"]
    assert str(cfg1.resolve()) in configs or str(cfg1) in configs
    assert str(cfg2.resolve()) in configs or str(cfg2) in configs


# ── P1: four flags missing from build_repro_command_args ──────────────────────


def test_build_repro_command_args_includes_igenomes_base(tmp_path):
    base = tmp_path / "igenomes"
    result = build_repro_command_args(tmp_path, args=_args(tmp_path, igenomes_base=str(base)))
    assert "--igenomes-base" in result
    assert str(base.resolve()) in result["--igenomes-base"]


def test_strandedness_summary_reads_from_strandedness_counts(tmp_path):
    preflight = _preflight()
    preflight["samplesheet"] = {"strandedness_counts": {"forward": 2, "reverse": 1}}
    write_report(tmp_path, args=_args(tmp_path), pipeline_source=_source(), preflight_result=preflight, parsed_outputs=_parsed(), command_str="cmd")
    content = (tmp_path / "report.md").read_text(encoding="utf-8")
    assert "forward: 2" in content
    assert "reverse: 1" in content


# ── Task 3: Verify _noinput guard ensures test-profile runs omit --input ──────


def test_repro_command_omits_input_for_noinput_runs(tmp_path):
    """build_repro_command_args must omit --input when args._noinput is True.

    Test-profile runs (test_full, test_prokaryotic, etc.) set _noinput=True.
    The replay command must not include --input so re-running the profile
    uses the bundled test data, not an external samplesheet.
    """
    args = _args(tmp_path, demo=False)
    args._noinput = True  # simulates test-profile run

    command_args = build_repro_command_args(tmp_path, args=args)

    assert "--input" not in command_args, (
        "--input must be absent from replay command for _noinput runs; "
        f"got keys: {list(command_args.keys())}"
    )
    assert "--demo" not in command_args, "--demo must not be set for _noinput runs"


# ── Step 3: post_run_warnings surfaced in report.md and result.json ──────────

def test_write_report_renders_post_run_warnings_section(tmp_path):
    """When post_run_warnings is non-empty, report.md must contain a
    '## Post-run Warnings' section listing each warning."""
    warnings = ["Provenance bundle could not be written (OSError: no space left)."]
    write_report(
        tmp_path,
        args=_args(tmp_path),
        pipeline_source=_source(),
        preflight_result=_preflight(),
        parsed_outputs=_parsed(),
        command_str="cmd",
        post_run_warnings=warnings,
    )
    content = (tmp_path / "report.md").read_text(encoding="utf-8")
    assert "## Post-run Warnings" in content, "report.md must include a Post-run Warnings section"
    assert "Provenance bundle" in content or "no space left" in content, (
        "report.md must include the warning text"
    )


def test_write_result_includes_post_run_warnings_in_json(tmp_path):
    """When post_run_warnings is non-empty, result.json summary must include
    a 'post_run_warnings' key listing the warnings."""
    warnings = ["Provenance bundle could not be written (RuntimeError: disk full)."]
    write_result(
        tmp_path,
        args=_args(tmp_path),
        pipeline_source=_source(),
        parsed_outputs=_parsed(),
        command_str="cmd",
        post_run_warnings=warnings,
    )
    result = json.loads((tmp_path / "result.json").read_text(encoding="utf-8"))
    stored = result.get("summary", {}).get("post_run_warnings", None)
    assert stored is not None, "result.json summary must have 'post_run_warnings' key"
    assert len(stored) == 1
    assert "disk full" in stored[0] or "Provenance" in stored[0]


def test_replay_line_is_shell_safe_for_apostrophe_path(tmp_path):
    """report.md replay line must survive output dirs containing single quotes."""
    tricky_out = tmp_path / "it's" / "out"
    tricky_out.mkdir(parents=True)
    write_report(
        tricky_out,
        args=_args(tmp_path, output=str(tricky_out)),
        pipeline_source=_source(),
        preflight_result=_preflight(),
        parsed_outputs=_parsed(),
        command_str="nextflow run nf-core/rnaseq",
    )
    content = (tricky_out / "report.md").read_text(encoding="utf-8")
    commands_sh_path = str(tricky_out / "reproducibility" / "commands.sh")
    # The old broken form must not appear verbatim.
    assert f"bash '{commands_sh_path}'" not in content
    # The replay line must still reference commands.sh somehow.
    assert "commands.sh" in content
