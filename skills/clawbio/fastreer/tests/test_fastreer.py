"""
Tests for fastreer.py
"""

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "fastreer.py"


def run(args, **kwargs):
    return subprocess.run(
        [sys.executable, str(SCRIPT)] + args,
        capture_output=True,
        text=True,
        **kwargs,
    )


class TestDemoMode:
    def test_demo_exits_zero(self, tmp_path):
        result = run(["--demo", "--output", str(tmp_path)])
        assert result.returncode == 0, result.stderr

    def test_demo_creates_report_md(self, tmp_path):
        run(["--demo", "--output", str(tmp_path)])
        assert (tmp_path / "report.md").exists()

    def test_demo_creates_result_json(self, tmp_path):
        run(["--demo", "--output", str(tmp_path)])
        rj = tmp_path / "result.json"
        assert rj.exists()
        data = json.loads(rj.read_text())
        assert "command" in data
        assert "samples" in data

    def test_demo_creates_reproducibility_bundle(self, tmp_path):
        run(["--demo", "--output", str(tmp_path)])
        assert (tmp_path / "reproducibility" / "commands.sh").exists()

    def test_demo_default_command_is_vcf2tree(self, tmp_path):
        run(["--demo", "--output", str(tmp_path)])
        data = json.loads((tmp_path / "result.json").read_text())
        assert data["command"] == "VCF2TREE"

    def test_demo_vcf2dist_command(self, tmp_path):
        result = run(["--demo", "--command", "VCF2DIST", "--output", str(tmp_path)])
        assert result.returncode == 0, result.stderr
        data = json.loads((tmp_path / "result.json").read_text())
        assert data["command"] == "VCF2DIST"

    def test_demo_fasta2dist_command(self, tmp_path):
        result = run(["--demo", "--command", "FASTA2DIST", "--output", str(tmp_path)])
        assert result.returncode == 0, result.stderr
        data = json.loads((tmp_path / "result.json").read_text())
        assert data["command"] == "FASTA2DIST"


class TestOutputContents:
    def test_report_md_contains_sample_count(self, tmp_path):
        run(["--demo", "--output", str(tmp_path)])
        report = (tmp_path / "report.md").read_text()
        assert "sample" in report.lower()

    def test_report_md_contains_disclaimer(self, tmp_path):
        run(["--demo", "--output", str(tmp_path)])
        report = (tmp_path / "report.md").read_text()
        assert "ClawBio" in report

    def test_result_json_has_required_keys(self, tmp_path):
        run(["--demo", "--output", str(tmp_path)])
        data = json.loads((tmp_path / "result.json").read_text())
        for key in ("command", "samples", "input_file", "output_dir"):
            assert key in data, f"Missing key: {key}"

    def test_vcf2tree_creates_nwk_file(self, tmp_path):
        run(["--demo", "--command", "VCF2TREE", "--output", str(tmp_path)])
        assert (tmp_path / "tree.nwk").exists()

    def test_vcf2dist_creates_dist_file(self, tmp_path):
        run(["--demo", "--command", "VCF2DIST", "--output", str(tmp_path)])
        assert (tmp_path / "distances.dist").exists()

    def test_fasta2dist_creates_dist_file(self, tmp_path):
        run(["--demo", "--command", "FASTA2DIST", "--output", str(tmp_path)])
        assert (tmp_path / "distances.dist").exists()


class TestValidation:
    def test_invalid_command_exits_nonzero(self, tmp_path):
        result = run(["--command", "INVALID", "--input", "x.vcf", "--output", str(tmp_path)])
        assert result.returncode != 0

    def test_missing_input_without_demo_exits_nonzero(self, tmp_path):
        result = run(["--command", "VCF2TREE", "--output", str(tmp_path)])
        assert result.returncode != 0

    def test_missing_output_exits_nonzero(self):
        result = run(["--demo"])
        assert result.returncode != 0
