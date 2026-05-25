"""Smoke tests for turingdb-graph.

These tests do NOT require a running TuringDB server. They verify:

- SKILL.md parses as valid YAML frontmatter + body
- All three demo files exist and are readable
- The CLI parses --help and each subcommand without errors
- The COHORT_QUERIES dict contains the expected analyses
- The HTTP wrapper importable

Live integration tests (actually spinning up TuringDB and running the three demos)
are out of scope for CI; run them locally with:

    python turingdb_graph.py --demo cohort --out /tmp/tg-cohort
    python turingdb_graph.py --demo pathway --out /tmp/tg-pathway
    python turingdb_graph.py --demo antibody --out /tmp/tg-antibody
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent


def test_skill_md_parses() -> None:
    import yaml

    skill_md = (SKILL_ROOT / "SKILL.md").read_text()
    assert skill_md.startswith("---\n"), "SKILL.md must start with YAML frontmatter"
    _, front, body = skill_md.split("---", 2)
    meta = yaml.safe_load(front)

    assert meta["name"] == "turingdb-graph"
    assert meta["license"] == "MIT"
    assert "metadata" in meta
    md = meta["metadata"]
    assert md["domain"] == "graph-analytics"
    assert md["version"] == "0.1.0"
    assert "inputs" in md and "outputs" in md
    assert "openclaw" in md
    assert md["openclaw"]["emoji"] == "\U0001f578"

    for section in ("## Domain Decisions", "## Safety", "## Agent Boundary",
                    "## Core Capabilities", "## CLI Reference", "## Gotchas"):
        assert section in body, f"SKILL.md body missing {section!r}"


def test_demo_datasets_exist() -> None:
    for name in ("cohort.csv", "pathway.gml", "antibody.csv"):
        p = SKILL_ROOT / "demo" / name
        assert p.exists(), f"Missing demo dataset: {p}"
        assert p.stat().st_size > 0, f"Empty demo dataset: {p}"


def test_demo_csv_is_anonymous() -> None:
    """Safety Rule 2: no real names / identifiers in the demo cohort."""
    cohort = (SKILL_ROOT / "demo" / "cohort.csv").read_text()
    # Generic placeholder names only — all names should match 'Patient NNN'
    import csv
    from io import StringIO
    rows = list(csv.DictReader(StringIO(cohort)))
    for row in rows:
        assert row["name"].startswith("Patient "), \
            f"Demo cohort must use 'Patient NNN' placeholders, got: {row['name']!r}"


def test_cli_help() -> None:
    result = subprocess.run(
        [sys.executable, str(SKILL_ROOT / "turingdb_graph.py"), "--help"],
        capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stderr
    out = result.stdout
    for token in ("--build", "--query", "--analyse-cohort", "--demo",
                  "--stop-server", "--host", "--data-dir"):
        assert token in out, f"--help missing flag: {token}"


def test_cohort_queries_present() -> None:
    spec = importlib.util.spec_from_file_location(
        "turingdb_graph", SKILL_ROOT / "turingdb_graph.py",
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules["turingdb_graph"] = mod  # required so dataclass annotations resolve
    spec.loader.exec_module(mod)

    expected = {
        "patient_count", "age_stats", "junior_count", "senior_count",
        "top_conditions", "top_medications",
        "top_comorbidities", "top_comedications",
    }
    assert set(mod.COHORT_QUERIES) == expected


def test_http_server_importable() -> None:
    # Importing http_server pulls in fastapi — skip if not installed
    try:
        import fastapi  # noqa: F401
    except ImportError:
        import pytest
        pytest.skip("fastapi not installed")

    # Register turingdb_graph first so http_server's "from turingdb_graph import ..." resolves
    tg_spec = importlib.util.spec_from_file_location(
        "turingdb_graph", SKILL_ROOT / "turingdb_graph.py",
    )
    tg_mod = importlib.util.module_from_spec(tg_spec)
    sys.modules["turingdb_graph"] = tg_mod
    tg_spec.loader.exec_module(tg_mod)

    spec = importlib.util.spec_from_file_location(
        "http_server", SKILL_ROOT / "http_server.py",
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules["http_server"] = mod
    spec.loader.exec_module(mod)

    routes = {r.path for r in mod.app.routes if hasattr(r, "path")}
    assert "/health" in routes
    assert "/build" in routes
    assert "/query" in routes
    assert "/analyse-cohort" in routes
    assert "/demo" in routes


def test_reference_docs_shipped() -> None:
    ref = SKILL_ROOT / "reference"
    for name in ("startup.md", "querying.md", "writing.md",
                 "algorithms.md", "introspection.md", "biomedical.md"):
        assert (ref / name).exists(), f"Missing reference doc: {name}"
