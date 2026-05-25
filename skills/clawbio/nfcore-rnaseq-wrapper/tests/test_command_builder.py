from __future__ import annotations

from pathlib import Path
import sys

_SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_DIR))


def _purge_foreign_modules(*names: str) -> None:
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


def _remove_skill_dir_from_sys_path() -> None:
    while str(_SKILL_DIR) in sys.path:
        sys.path.remove(str(_SKILL_DIR))


_purge_foreign_modules("command_builder")

from command_builder import build_nextflow_command, compose_profile

_purge_local_modules("command_builder")
_remove_skill_dir_from_sys_path()


def test_local_checkout_command_uses_params_file_and_profile(tmp_path):
    params_path = tmp_path / "params.yaml"
    params_path.write_text("aligner: star_salmon\n", encoding="utf-8")
    source = {
        "source_kind": "local_checkout",
        "source_ref": str(tmp_path / "rnaseq"),
        "resolved_version": "abc1234",
    }
    cmd, _cmd_str = build_nextflow_command(
        pipeline_source=source,
        profile="docker",
        params_path=params_path,
        resume=False,
    )
    assert cmd[:3] == ["nextflow", "run", (tmp_path / "rnaseq").as_posix()]
    assert ["-profile", "docker"] == cmd[3:5]
    assert ["-params-file", params_path.as_posix()] == cmd[5:7]
    assert "-r" not in cmd
    assert "-resume" not in cmd


def test_remote_repo_command_includes_requested_version(tmp_path):
    params_path = tmp_path / "params.yaml"
    params_path.write_text("aligner: star_salmon\n", encoding="utf-8")
    source = {
        "source_kind": "remote_repo",
        "source_ref": "nf-core/rnaseq",
        "resolved_version": "3.26.0",
    }
    cmd, _cmd_str = build_nextflow_command(
        pipeline_source=source,
        profile="singularity",
        params_path=params_path,
        resume=False,
    )
    assert cmd[:5] == ["nextflow", "run", "nf-core/rnaseq", "-r", "3.26.0"]
    assert ["-profile", "singularity"] == cmd[5:7]


def test_compose_profile_adds_test_before_backend_for_demo():
    assert compose_profile("docker", demo=True) == "test,docker"


def test_compose_profile_adds_prokaryotic_after_backend():
    assert compose_profile("docker", prokaryotic=True) == "docker,prokaryotic"


def test_compose_profile_deduplicates_existing_parts():
    assert compose_profile("test,docker,prokaryotic", demo=True, prokaryotic=True) == "test,docker,prokaryotic"


def test_work_dir_extra_configs_and_resume_are_ordered_after_params(tmp_path):
    params_path = tmp_path / "params.yaml"
    params_path.write_text("aligner: star_salmon\n", encoding="utf-8")
    work_dir = tmp_path / "upstream" / "work"
    cfg1 = tmp_path / "custom.config"
    cfg2 = tmp_path / "extra.config"
    cfg1.write_text("process { }\n", encoding="utf-8")
    cfg2.write_text("docker { enabled = true }\n", encoding="utf-8")
    source = {
        "source_kind": "local_checkout",
        "source_ref": str(tmp_path / "rnaseq"),
        "resolved_version": "abc1234",
    }
    cmd, _cmd_str = build_nextflow_command(
        pipeline_source=source,
        profile="docker",
        params_path=params_path,
        work_dir=work_dir,
        extra_configs=[cfg1, cfg2],
        resume=True,
    )
    assert ["-work-dir", work_dir.as_posix()] == cmd[cmd.index("-work-dir"):cmd.index("-work-dir") + 2]
    assert cmd.count("-c") == 2
    assert cfg1.as_posix() in cmd
    assert cfg2.as_posix() in cmd
    assert cmd.index("-resume") > cmd.index("-c")


def test_command_str_quotes_paths_with_spaces(tmp_path):
    params_path = tmp_path / "params with spaces.yaml"
    params_path.write_text("aligner: star_salmon\n", encoding="utf-8")
    source = {
        "source_kind": "local_checkout",
        "source_ref": str(tmp_path / "rnaseq checkout"),
        "resolved_version": "abc1234",
    }
    _cmd, cmd_str = build_nextflow_command(
        pipeline_source=source,
        profile="docker",
        params_path=params_path,
        resume=False,
    )
    assert "'" in cmd_str or '"' in cmd_str or "\\ " in cmd_str


def test_command_uses_composed_profile_for_arm(tmp_path):
    params_path = tmp_path / "params.yaml"
    params_path.write_text("aligner: star_salmon\n", encoding="utf-8")
    source = {
        "source_kind": "remote_repo",
        "source_ref": "nf-core/rnaseq",
        "resolved_version": "3.26.0",
    }
    cmd, _cmd_str = build_nextflow_command(
        pipeline_source=source,
        profile="docker",
        params_path=params_path,
        resume=False,
        arm=True,
    )
    assert cmd[cmd.index("-profile") + 1] == "docker,arm64"


def test_compose_profile_test_prokaryotic_with_prokaryotic_flag_no_duplicate():
    """compose_profile("test_prokaryotic", prokaryotic=True) must not produce test_prokaryotic,prokaryotic.

    test_prokaryotic already includes prokaryotic semantics (it inherits
    conf/prokaryotic.config upstream).  When _sync_profile_flags sets
    args.prokaryotic=True from the test_prokaryotic token, compose_profile
    must recognise the overlap and not append a redundant 'prokaryotic' suffix.
    """
    result = compose_profile("test_prokaryotic", prokaryotic=True)
    assert result == "test_prokaryotic", (
        f"compose_profile must not append prokaryotic when test_prokaryotic is present; got {result!r}"
    )


def test_build_nextflow_command_includes_user_config_files(tmp_path):
    """build_nextflow_command must include user-supplied -c configs alongside system ones.

    Users need to pass custom Nextflow config files for institution-specific
    settings, RSEM extra args (removed from nf-core schema), or HPC profiles
    not covered by built-in params.  These must appear as -c flags in the
    Nextflow command before -params-file.
    """
    params_path = tmp_path / "params.yaml"
    params_path.write_text("aligner: star_salmon\n", encoding="utf-8")
    user_cfg = tmp_path / "my_hpc.config"
    user_cfg.write_text("process.executor = 'slurm'\n", encoding="utf-8")
    source = {
        "source_kind": "remote",
        "source_ref": "nf-core/rnaseq",
        "resolved_version": "3.26.0",
    }
    cmd, cmd_str = build_nextflow_command(
        pipeline_source=source,
        profile="docker",
        params_path=params_path,
        resume=False,
        extra_configs=[user_cfg],
    )
    assert "-c" in cmd
    cfg_idx = cmd.index("-c")
    assert cmd[cfg_idx + 1] == user_cfg.as_posix(), (
        f"Expected user config path after -c; got {cmd[cfg_idx + 1]!r}"
    )
