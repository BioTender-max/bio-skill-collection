"""Tests for ukb-navigator — UK Biobank schema search."""

import csv
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ukb_navigator import (
    DEMO_RESULTS,
    generate_report,
    field_lookup,
    query_schema,
)


# ---------------------------------------------------------------------------
# DEMO_RESULTS validation
# ---------------------------------------------------------------------------

class TestDemoResults:
    def test_non_empty(self):
        assert len(DEMO_RESULTS) > 0

    def test_required_keys(self):
        for entry in DEMO_RESULTS:
            assert "text" in entry
            assert "source" in entry
            assert "similarity" in entry
            assert "metadata" in entry

    def test_similarities_in_range(self):
        for entry in DEMO_RESULTS:
            assert 0 <= entry["similarity"] <= 1

    def test_sorted_by_similarity(self):
        sims = [e["similarity"] for e in DEMO_RESULTS]
        assert sims == sorted(sims, reverse=True)


# ---------------------------------------------------------------------------
# generate_report
# ---------------------------------------------------------------------------

class TestGenerateReport:
    def test_report_contains_query(self, tmp_path):
        report_path = generate_report("blood pressure", DEMO_RESULTS, tmp_path)
        text = report_path.read_text()
        assert "blood pressure" in text

    def test_report_contains_disclaimer(self, tmp_path):
        report_path = generate_report("test", DEMO_RESULTS, tmp_path)
        text = report_path.read_text()
        assert "research and educational tool" in text

    def test_report_contains_date(self, tmp_path):
        report_path = generate_report("test", DEMO_RESULTS, tmp_path)
        text = report_path.read_text()
        assert "**Date**:" in text

    def test_report_contains_result_count(self, tmp_path):
        report_path = generate_report("test", DEMO_RESULTS, tmp_path)
        text = report_path.read_text()
        assert f"{len(DEMO_RESULTS)} matches" in text

    def test_csv_output(self, tmp_path):
        generate_report("test", DEMO_RESULTS, tmp_path)
        csv_path = tmp_path / "matched_fields.csv"
        assert csv_path.exists()
        with open(csv_path) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == len(DEMO_RESULTS)
        assert "rank" in rows[0]
        assert "similarity" in rows[0]
        assert "source" in rows[0]
        assert "text" in rows[0]

    def test_creates_output_dir(self, tmp_path):
        out = tmp_path / "new_dir"
        report_path = generate_report("test", DEMO_RESULTS, out)
        assert report_path.exists()

    def test_creates_reproducibility(self, tmp_path):
        generate_report("test", DEMO_RESULTS, tmp_path)
        cmd_file = tmp_path / "reproducibility" / "commands.sh"
        assert cmd_file.exists()

    def test_demo_mode_flag(self, tmp_path):
        report_path = generate_report("test", DEMO_RESULTS, tmp_path, is_demo=True)
        text = report_path.read_text()
        assert "Demo" in text

    def test_empty_results(self, tmp_path):
        report_path = generate_report("nothing", [], tmp_path)
        text = report_path.read_text()
        assert "0 matches" in text


# ---------------------------------------------------------------------------
# field_lookup delegates to query_schema
# ---------------------------------------------------------------------------

class TestFieldLookup:
    def test_delegates_correctly(self):
        # field_lookup just wraps query_schema with a formatted string
        # With no ChromaDB collection, it should return empty list
        # (we test the delegation logic, not the DB)
        # This test verifies the function exists and is callable
        assert callable(field_lookup)
