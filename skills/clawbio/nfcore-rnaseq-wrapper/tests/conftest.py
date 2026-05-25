"""
conftest.py — pre-stub clawbio package to avoid loading runner.py
(runner.py loads clawbio.py which uses `str | None` syntax, Python 3.10+ only)
"""
from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent


def _ensure_clawbio_stubs() -> None:
    if "clawbio" not in sys.modules:
        pkg = types.ModuleType("clawbio")
        pkg.__path__ = [str(_REPO_ROOT / "clawbio")]  # type: ignore[attr-defined]
        pkg.__package__ = "clawbio"
        sys.modules["clawbio"] = pkg
    if "clawbio.common" not in sys.modules:
        common = types.ModuleType("clawbio.common")
        common.__path__ = [str(_REPO_ROOT / "clawbio" / "common")]  # type: ignore[attr-defined]
        common.__package__ = "clawbio.common"
        sys.modules["clawbio.common"] = common

    def _load(name: str) -> None:
        if name in sys.modules:
            return
        path = _REPO_ROOT / (name.replace(".", "/") + ".py")
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
        mod.__package__ = name.rsplit(".", 1)[0]
        sys.modules[name] = mod
        spec.loader.exec_module(mod)  # type: ignore[union-attr]

    _load("clawbio.common.checksums")
    _load("clawbio.common.portable_commands")
    _load("clawbio.common.report")
    _load("clawbio.common.reproducibility")


_ensure_clawbio_stubs()
