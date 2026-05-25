import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import seq_wrangler as sw
from pathlib import Path
import json
import types
import pytest

import seq_wrangler as sw


def test_load_samplesheet_mixed_se_pe(tmp_path: Path):
    p = tmp_path / "samples.csv"
    p.write_text(
        "sample,fastq_1,fastq_2\n"
        "CTRL,a_R1.fastq.gz,a_R2.fastq.gz\n"
        "TREAT,b.fastq.gz,\n",
        encoding="utf-8"
    )
    rows = sw.load_samplesheet(p)
    assert len(rows) == 2
    assert rows[0]["sample"] == "CTRL"
    assert rows[0]["fastq_2"] == "a_R2.fastq.gz"
    assert rows[1]["sample"] == "TREAT"
    assert rows[1]["fastq_2"] == ""


def test_load_samplesheet_missing_required_columns(tmp_path: Path):
    p = tmp_path / "bad.csv"
    p.write_text("sample,foo\nS1,x.fastq.gz\n", encoding="utf-8")
    with pytest.raises(ValueError):
        sw.load_samplesheet(p)


def test_detect_threads_positive():
    assert sw.detect_threads() >= 1


def test_check_tool_false_for_nonexistent():
    assert sw.check_tool("definitely_not_a_real_binary_123") is False


def test_sha256_file(tmp_path: Path):
    p = tmp_path / "x.txt"
    p.write_text("abc", encoding="utf-8")
    h = sw.sha256_file(p)
    assert len(h) == 64
    assert h == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_run_command_non_critical_failure():
    result = sw.run_command(
        [sys.executable, "-c", "import sys; sys.exit(3)"],
        "fail-non-critical",
        critical=False,
    )
    assert result.returncode == 3


def test_validate_args_demo_ok():
    args = types.SimpleNamespace(
        demo=True, index=None, samplesheet=None, r1=None, r2=None
    )
    sw.validate_args(args)  # no exception


def test_validate_args_requires_index_when_not_demo():
    args = types.SimpleNamespace(
        demo=False, index=None, samplesheet=None, r1="a.fastq.gz", r2=None
    )
    with pytest.raises(ValueError):
        sw.validate_args(args)


def test_validate_args_samplesheet_xor_single():
    args = types.SimpleNamespace(
        demo=False, index="/ref/hg38", samplesheet="samples.csv", r1="a.fastq.gz", r2=None
    )
    with pytest.raises(ValueError):
        sw.validate_args(args)


def test_generate_report_and_demo_outputs(tmp_path: Path):
    args = types.SimpleNamespace(
        output=str(tmp_path),
        aligner="bwa",
        mapq=20,
        remove_duplicates=False,
        samplesheet=None,
        r1=None,
        r2=None,
        index=None,
        threads=2,
        trim=False,
        run_fastqc=False,
        run_multiqc=False,
        demo=True,
        genome_build="GRCh38",
    )

    sw.run_demo(args)

    report = tmp_path / "report.md"
    summary = tmp_path / "summary.json"
    repro_cmd = tmp_path / "reproducibility" / "commands.sh"
    repro_env = tmp_path / "reproducibility" / "environment.yml"

    assert report.exists()
    assert summary.exists()
    assert repro_cmd.exists()
    assert repro_env.exists()

    data = json.loads(summary.read_text(encoding="utf-8"))
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["sample"] in {"CTRL_REP1", "TREAT_REP1"}