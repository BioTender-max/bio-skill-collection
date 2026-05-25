from __future__ import annotations

import csv
import importlib
from pathlib import Path
import sys
import types

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


_purge_foreign_modules("errors", "schemas", "samplesheet_builder")

from errors import ErrorCode, SkillError
from samplesheet_builder import _looks_like_fastq_path, validate_and_normalize_samplesheet

_purge_local_modules("errors", "schemas", "samplesheet_builder")
_remove_skill_dir_from_sys_path()


def _touch(path: Path, text: str = "x") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _write_sheet(path: Path, rows: list[dict[str, str]], fieldnames: list[str] | None = None) -> Path:
    if fieldnames is None:
        seen: list[str] = []
        for row in rows:
            for key in row:
                if key not in seen:
                    seen.append(key)
        fieldnames = seen
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    return path


def _valid_row(tmp_path: Path, **overrides: str) -> dict[str, str]:
    r1 = _touch(tmp_path / "reads" / "sample_R1.fastq.gz")
    row = {"sample": "sampleA", "fastq_1": str(r1), "strandedness": "auto"}
    row.update(overrides)
    return row


@pytest.mark.parametrize("missing", ["sample", "fastq_1", "strandedness"])
def test_rejects_missing_required_columns(tmp_path, missing):
    row = _valid_row(tmp_path)
    fieldnames = [name for name in ("sample", "fastq_1", "strandedness") if name != missing]
    _write_sheet(tmp_path / "samplesheet.csv", [row], fieldnames=fieldnames)

    with pytest.raises(SkillError) as exc:
        validate_and_normalize_samplesheet(tmp_path / "samplesheet.csv", tmp_path / "normalized.csv")

    assert exc.value.error_code == ErrorCode.INVALID_SAMPLESHEET
    assert missing in exc.value.details["missing_columns"]


def test_accepts_single_end_fastq_and_writes_optional_fastq_2_blank(tmp_path):
    src = _write_sheet(tmp_path / "samplesheet.csv", [_valid_row(tmp_path)])
    out = tmp_path / "normalized.csv"

    result = validate_and_normalize_samplesheet(src, out)

    row = next(csv.DictReader(out.open(encoding="utf-8")))
    assert result["sample_count"] == 1
    assert row["fastq_2"] == ""
    assert Path(row["fastq_1"]).is_absolute()


@pytest.mark.parametrize("filename", ["sample_R1.txt"])
def test_rejects_non_upstream_fastq_suffixes(tmp_path, filename):
    r1 = _touch(tmp_path / filename)
    src = _write_sheet(tmp_path / "samplesheet.csv", [{"sample": "sampleA", "fastq_1": str(r1), "strandedness": "auto"}])

    with pytest.raises(SkillError) as exc:
        validate_and_normalize_samplesheet(src, tmp_path / "normalized.csv")

    assert exc.value.error_code == ErrorCode.INVALID_FASTQ


def test_rejects_fastq_basename_with_space_but_allows_parent_space(tmp_path):
    reads_dir = tmp_path / "reads with spaces"
    bad = _touch(reads_dir / "sample R1.fastq.gz")
    src = _write_sheet(tmp_path / "samplesheet.csv", [{"sample": "sampleA", "fastq_1": str(bad), "strandedness": "auto"}])

    with pytest.raises(SkillError) as exc:
        validate_and_normalize_samplesheet(src, tmp_path / "normalized.csv")

    assert exc.value.error_code == ErrorCode.INVALID_FASTQ
    assert exc.value.details["filename"] == "sample R1.fastq.gz"


def test_resolves_relative_fastq_against_samplesheet_directory(tmp_path):
    sheet_dir = tmp_path / "inputs"
    r1 = _touch(sheet_dir / "reads" / "sample_R1.fastq.gz")
    src = _write_sheet(sheet_dir / "samplesheet.csv", [{"sample": "sampleA", "fastq_1": "reads/sample_R1.fastq.gz", "strandedness": "auto"}])
    out = tmp_path / "normalized.csv"

    validate_and_normalize_samplesheet(src, out)

    row = next(csv.DictReader(out.open(encoding="utf-8")))
    assert row["fastq_1"] == r1.resolve().as_posix()


def test_rejects_missing_fastq_path(tmp_path):
    src = _write_sheet(
        tmp_path / "samplesheet.csv",
        [{"sample": "sampleA", "fastq_1": "missing.fastq.gz", "strandedness": "auto"}],
    )

    with pytest.raises(SkillError) as exc:
        validate_and_normalize_samplesheet(src, tmp_path / "normalized.csv")

    assert exc.value.error_code == ErrorCode.MISSING_FASTQ


@pytest.mark.parametrize("strandedness", ["", "AUTO"])
def test_rejects_invalid_strandedness_values(tmp_path, strandedness):
    src = _write_sheet(tmp_path / "samplesheet.csv", [_valid_row(tmp_path, strandedness=strandedness)])

    with pytest.raises(SkillError) as exc:
        validate_and_normalize_samplesheet(src, tmp_path / "normalized.csv")

    assert exc.value.error_code == ErrorCode.INVALID_STRANDEDNESS


def test_normalizes_sample_whitespace_to_underscores(tmp_path):
    src = _write_sheet(tmp_path / "samplesheet.csv", [_valid_row(tmp_path, sample="sample  A")])

    result = validate_and_normalize_samplesheet(src, tmp_path / "normalized.csv")

    assert result["sample_names"] == ["sample_A"]


def test_rejects_sample_collision_after_whitespace_normalization(tmp_path):
    r1a = _touch(tmp_path / "a_R1.fastq.gz")
    r1b = _touch(tmp_path / "b_R1.fastq.gz")
    src = _write_sheet(
        tmp_path / "samplesheet.csv",
        [
            {"sample": "sample A", "fastq_1": str(r1a), "strandedness": "auto"},
            {"sample": "sample_A", "fastq_1": str(r1b), "strandedness": "auto"},
        ],
    )

    with pytest.raises(SkillError) as exc:
        validate_and_normalize_samplesheet(src, tmp_path / "normalized.csv")

    assert exc.value.error_code == ErrorCode.INVALID_SAMPLESHEET


def test_rejects_inconsistent_repeated_sample_strandedness(tmp_path):
    r1a = _touch(tmp_path / "sample_L001_R1.fastq.gz")
    r1b = _touch(tmp_path / "sample_L002_R1.fastq.gz")
    src = _write_sheet(
        tmp_path / "samplesheet.csv",
        [
            {"sample": "sampleA", "fastq_1": str(r1a), "strandedness": "forward"},
            {"sample": "sampleA", "fastq_1": str(r1b), "strandedness": "reverse"},
        ],
    )

    with pytest.raises(SkillError) as exc:
        validate_and_normalize_samplesheet(src, tmp_path / "normalized.csv")

    assert exc.value.error_code == ErrorCode.INVALID_STRANDEDNESS


def test_rejects_duplicate_fastq_rows(tmp_path):
    r1 = _touch(tmp_path / "sample_R1.fastq.gz")
    src = _write_sheet(
        tmp_path / "samplesheet.csv",
        [
            {"sample": "sampleA", "fastq_1": str(r1), "strandedness": "auto"},
            {"sample": "sampleA", "fastq_1": str(r1), "strandedness": "auto"},
        ],
    )

    with pytest.raises(SkillError) as exc:
        validate_and_normalize_samplesheet(src, tmp_path / "normalized.csv")

    assert exc.value.error_code == ErrorCode.INVALID_SAMPLESHEET


def test_supports_genome_and_transcriptome_bam_columns(tmp_path):
    gbam = _touch(tmp_path / "sample.genome.bam")
    tbam = _touch(tmp_path / "sample.transcriptome.bam")
    # BAM-only row: fastq_1 must be empty (mixing FASTQ + BAM is rejected).
    src = _write_sheet(
        tmp_path / "samplesheet.csv",
        [_valid_row(tmp_path, fastq_1="", genome_bam=str(gbam), transcriptome_bam=str(tbam))],
    )

    result = validate_and_normalize_samplesheet(src, tmp_path / "normalized.csv")

    assert result["bam_paths"] == [gbam.resolve(), tbam.resolve()]
    assert result["fastq_paths"] == []


def test_rejects_row_mixing_fastq_and_bam_columns(tmp_path):
    gbam = _touch(tmp_path / "sample.genome.bam")
    src = _write_sheet(
        tmp_path / "samplesheet.csv",
        [_valid_row(tmp_path, genome_bam=str(gbam))],  # fastq_1 set by default
    )

    with pytest.raises(SkillError) as exc:
        validate_and_normalize_samplesheet(src, tmp_path / "normalized.csv")

    assert exc.value.error_code == ErrorCode.INVALID_SAMPLESHEET
    assert "FASTQ and BAM" in exc.value.message


def test_rejects_missing_bam_path(tmp_path):
    src = _write_sheet(
        tmp_path / "samplesheet.csv",
        [_valid_row(tmp_path, fastq_1="", genome_bam="missing.bam")],
    )

    with pytest.raises(SkillError) as exc:
        validate_and_normalize_samplesheet(src, tmp_path / "normalized.csv")

    assert exc.value.error_code == ErrorCode.MISSING_INPUT


def test_reports_unknown_columns_and_preserves_them(tmp_path):
    src = _write_sheet(tmp_path / "samplesheet.csv", [_valid_row(tmp_path, condition="treated")])
    out = tmp_path / "normalized.csv"

    result = validate_and_normalize_samplesheet(src, out)

    row = next(csv.DictReader(out.open(encoding="utf-8")))
    assert result["unknown_columns"] == ["condition"]
    assert row["condition"] == "treated"


def test_rejects_empty_samplesheet(tmp_path):
    (tmp_path / "samplesheet.csv").write_text("sample,fastq_1,strandedness\n", encoding="utf-8")

    with pytest.raises(SkillError) as exc:
        validate_and_normalize_samplesheet(tmp_path / "samplesheet.csv", tmp_path / "normalized.csv")

    assert exc.value.error_code == ErrorCode.INVALID_SAMPLESHEET


def test_rejects_missing_samplesheet_file(tmp_path):
    with pytest.raises(SkillError) as exc:
        validate_and_normalize_samplesheet(tmp_path / "missing.csv", tmp_path / "normalized.csv")

    assert exc.value.error_code == ErrorCode.MISSING_INPUT


def test_normalized_output_has_stable_rnaseq_columns(tmp_path):
    src = _write_sheet(tmp_path / "samplesheet.csv", [_valid_row(tmp_path, condition="treated")])
    out = tmp_path / "normalized.csv"

    validate_and_normalize_samplesheet(src, out)

    reader = csv.DictReader(out.open(encoding="utf-8"))
    assert reader.fieldnames[:6] == [
        "sample",
        "fastq_1",
        "fastq_2",
        "strandedness",
        "genome_bam",
        "transcriptome_bam",
    ]


# ── mixed PE/SE / BAM coverage / metadata pass-through ──────────────────────


def test_accepts_mixed_paired_and_single_end_rows_in_same_sheet(tmp_path):
    pe_r1 = _touch(tmp_path / "reads" / "pe_R1.fastq.gz")
    pe_r2 = _touch(tmp_path / "reads" / "pe_R2.fastq.gz")
    se_r1 = _touch(tmp_path / "reads" / "se_R1.fastq.gz")
    rows = [
        {"sample": "PE", "fastq_1": str(pe_r1), "fastq_2": str(pe_r2), "strandedness": "auto"},
        {"sample": "SE", "fastq_1": str(se_r1), "fastq_2": "", "strandedness": "forward"},
    ]
    src = _write_sheet(tmp_path / "samplesheet.csv", rows)
    out = tmp_path / "normalized.csv"

    result = validate_and_normalize_samplesheet(src, out)

    assert result["sample_count"] == 2
    assert result["sample_names"] == ["PE", "SE"]
    rows_out = list(csv.DictReader(out.open(encoding="utf-8")))
    assert rows_out[0]["fastq_2"] == str(pe_r2.resolve())
    assert rows_out[1]["fastq_2"] == ""


def test_rejects_whitespace_only_fastq_1(tmp_path):
    src = _write_sheet(
        tmp_path / "samplesheet.csv",
        [_valid_row(tmp_path, fastq_1="   ")],
    )

    with pytest.raises(SkillError) as exc:
        validate_and_normalize_samplesheet(src, tmp_path / "normalized.csv")

    assert exc.value.error_code == ErrorCode.INVALID_SAMPLESHEET


def test_bam_normalized_fastq1_is_empty_string_not_dot(tmp_path):
    """Normalized BAM samplesheet must write fastq_1='' not '.' (nf-core schema forbids '.')."""
    gbam = _touch(tmp_path / "sample.genome.bam")
    src = _write_sheet(
        tmp_path / "samplesheet.csv",
        [{"sample": "sampleA", "fastq_1": "", "strandedness": "auto", "genome_bam": str(gbam)}],
    )
    out = tmp_path / "normalized.csv"
    validate_and_normalize_samplesheet(src, out)
    import csv as _csv
    row = next(_csv.DictReader(out.open(encoding="utf-8")))
    assert row["fastq_1"] == "", f"Expected empty string, got {row['fastq_1']!r}"


def test_non_csv_extension_rejected(tmp_path):
    """Samplesheet with .tsv extension must be rejected — schema: input must be a .csv file."""
    tsv = tmp_path / "samplesheet.tsv"
    tsv.write_text("sample,fastq_1,strandedness\nsampleA,/reads/A_R1.fastq.gz,auto\n", encoding="utf-8")
    out = tmp_path / "normalized.csv"
    with pytest.raises(SkillError) as exc:
        validate_and_normalize_samplesheet(tsv, out)
    assert exc.value.error_code == ErrorCode.INVALID_SAMPLESHEET
