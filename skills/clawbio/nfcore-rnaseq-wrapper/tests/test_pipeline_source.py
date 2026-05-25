from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys

import pytest

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


_purge_foreign_modules("errors", "schemas", "pipeline_source")

from errors import SkillError
from pipeline_source import resolve_pipeline_source

_purge_local_modules("errors", "schemas", "pipeline_source")
_remove_skill_dir_from_sys_path()

_requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not on PATH")


def _make_valid_local_checkout(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    (path / "main.nf").write_text("// main", encoding="utf-8")
    (path / "nextflow.config").write_text("// config", encoding="utf-8")
    assets = path / "assets"
    assets.mkdir()
    (assets / "schema_input.json").write_text("{}", encoding="utf-8")


def test_resolves_to_remote_when_no_local_dir(tmp_path):
    absent = tmp_path / "nonexistent_rnaseq"
    result = resolve_pipeline_source(
        requested_version="3.26.0",
        local_pipeline_dir=absent,
    )
    assert result["source_kind"] == "remote_repo"
    assert result["source_ref"] == "nf-core/rnaseq"
    assert result["resolved_version"] == "3.26.0"
    assert result["dirty"] is False
    assert result["branch"] == ""


def test_resolves_to_local_when_valid_checkout(tmp_path):
    local = tmp_path / "rnaseq"
    _make_valid_local_checkout(local)
    result = resolve_pipeline_source(
        requested_version="3.26.0",
        local_pipeline_dir=local,
    )
    assert result["source_kind"] == "local_checkout"
    assert result["source_ref"] == str(local.resolve())
    assert result["resolved_version"] == "3.26.0"
    assert result["branch"] == ""
    assert result["dirty"] is False


def test_raises_when_local_dir_missing_required_files(tmp_path):
    local = tmp_path / "rnaseq"
    local.mkdir()
    (local / "main.nf").write_text("// main", encoding="utf-8")
    with pytest.raises(SkillError) as exc:
        resolve_pipeline_source(
            requested_version="3.26.0",
            local_pipeline_dir=local,
        )
    assert exc.value.error_code == "PIPELINE_SOURCE_INVALID"
    assert exc.value.details["missing_files"] == ["nextflow.config", "assets/schema_input.json"]
    assert exc.value.details["path"] == str(local.resolve())


def test_local_checkout_result_contains_expected_keys(tmp_path):
    local = tmp_path / "rnaseq"
    _make_valid_local_checkout(local)
    result = resolve_pipeline_source(
        requested_version="3.26.0",
        local_pipeline_dir=local,
    )
    assert set(result) == {"source_kind", "source_ref", "resolved_version", "branch", "dirty"}


def test_remote_result_contains_expected_keys(tmp_path):
    result = resolve_pipeline_source(
        requested_version="3.26.0",
        local_pipeline_dir=tmp_path / "missing",
    )
    assert set(result) == {"source_kind", "source_ref", "resolved_version", "branch", "dirty"}


@_requires_git
def test_local_checkout_uses_git_commit_when_available(tmp_path):
    local = tmp_path / "rnaseq"
    _make_valid_local_checkout(local)
    subprocess.run(["git", "init"], cwd=local, check=True, capture_output=True, text=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=local, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=local, check=True)
    subprocess.run(["git", "add", "."], cwd=local, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=local, check=True, capture_output=True, text=True)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=local, check=True, capture_output=True, text=True).stdout.strip()
    result = resolve_pipeline_source(
        requested_version="3.26.0",
        local_pipeline_dir=local,
    )
    assert result["resolved_version"] == commit
    assert result["dirty"] is False
