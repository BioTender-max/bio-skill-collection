from __future__ import annotations

import csv
import os
import re
import sys
from collections import Counter
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent
if str(_SKILL_DIR) in sys.path:
    sys.path.remove(str(_SKILL_DIR))
sys.path.insert(0, str(_SKILL_DIR))


def _purge_foreign_bare_modules(*names: str) -> None:
    for name in names:
        module = sys.modules.get(name)
        module_file = Path(getattr(module, "__file__", "") or "")
        if module is not None and _SKILL_DIR not in module_file.parents and module_file != _SKILL_DIR / f"{name}.py":
            sys.modules.pop(name, None)


_purge_foreign_bare_modules("errors", "schemas")

from errors import ErrorCode, SkillError
from schemas import REQUIRED_SAMPLE_COLUMNS, SUPPORTED_SAMPLE_COLUMNS, SUPPORTED_STRANDEDNESS


_SAMPLE_NAME_RE = re.compile(r"^\S+$")
_SAMPLE_WHITESPACE_RE = re.compile(r"\s+")
_NO_WHITESPACE_RE = re.compile(r"^\S+$")
_NO_WHITESPACE_COLUMNS = ("seq_platform", "seq_center")
_FASTQ_BASENAME_RE = re.compile(r"^[^\s/]+\.f(?:ast)?q(?:\.gz)?$")
_BAM_BASENAME_RE = re.compile(r"^[^\s/]+\.bam$", re.IGNORECASE)
_BASE_OUTPUT_COLUMNS = ("sample", "fastq_1", "fastq_2", "strandedness", "genome_bam", "transcriptome_bam")
_UPSTREAM_OPTIONAL_SAMPLE_COLUMNS = {"seq_platform", "seq_center", "percent_mapped"}
_SUPPORTED_SAMPLE_COLUMNS = set(SUPPORTED_SAMPLE_COLUMNS) | _UPSTREAM_OPTIONAL_SAMPLE_COLUMNS
_FASTQ_COLUMNS = ("fastq_1", "fastq_2")
_BAM_COLUMNS = ("genome_bam", "transcriptome_bam")


def validate_and_normalize_samplesheet(
    input_path: Path, output_path: Path, *, skip_alignment: bool = False
) -> dict[str, object]:
    # nf-core/rnaseq 3.26.0 schema: input pattern ^\S+\.csv$ — reject non-.csv files early.
    if input_path.suffix.lower() != ".csv":
        raise SkillError(
            stage="validation",
            error_code=ErrorCode.INVALID_SAMPLESHEET,
            message=f"The samplesheet must be a CSV file (nf-core schema: --input pattern ^\\.csv$); "
                    f"got '{input_path.name}'.",
            fix="Rename the file to end in .csv and ensure it uses comma-separated format.",
            details={"path": str(input_path), "suffix": input_path.suffix},
        )
    fieldnames, rows = _read_samplesheet(input_path)
    unknown_columns = _unknown_columns(fieldnames)
    output_columns = _build_output_columns(fieldnames)
    normalized_rows, sample_names, fastq_paths, bam_paths, strandedness_counts = _normalize_rows(
        rows,
        input_path=input_path,
        output_columns=output_columns,
        skip_alignment=skip_alignment,
    )
    _write_normalized_samplesheet(output_path, output_columns, normalized_rows)

    return {
        "normalized_path": output_path,
        "sample_count": len(sample_names),
        "sample_names": sample_names,
        "fastq_paths": fastq_paths,
        "bam_paths": bam_paths,
        "strandedness_counts": dict(strandedness_counts),
        "unknown_columns": unknown_columns,
    }


def _read_samplesheet(input_path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not input_path.exists():
        raise SkillError(
            stage="validation",
            error_code=ErrorCode.MISSING_INPUT,
            message="Samplesheet was not found.",
            fix="Provide a valid --input path to a samplesheet.csv file.",
            details={"path": str(input_path)},
        )

    with input_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        _validate_required_columns(fieldnames)
        rows = list(reader)

    if not rows:
        raise SkillError(
            stage="validation",
            error_code=ErrorCode.INVALID_SAMPLESHEET,
            message="Samplesheet is empty.",
            fix="Add at least one sample row to the input CSV.",
            details={"path": str(input_path)},
        )
    return fieldnames, rows


def _validate_required_columns(fieldnames: list[str]) -> None:
    # BAM-reprocessing samplesheets have genome_bam/transcriptome_bam instead of fastq_1.
    # In that mode, fastq_1 is optional at the header level; row-level validation guards
    # the actual values. Only sample and strandedness are universally required.
    bam_mode = any(col in fieldnames for col in _BAM_COLUMNS)
    if bam_mode:
        always_required = ("sample", "strandedness")
    else:
        always_required = REQUIRED_SAMPLE_COLUMNS
    missing_columns = [name for name in always_required if name not in fieldnames]
    if missing_columns:
        raise SkillError(
            stage="validation",
            error_code=ErrorCode.INVALID_SAMPLESHEET,
            message="Samplesheet is missing required columns.",
            fix=(
                "FASTQ samplesheets must contain sample, fastq_1, and strandedness. "
                "BAM reprocessing samplesheets must contain sample, strandedness, and "
                "at least one of genome_bam or transcriptome_bam."
            ),
            details={"missing_columns": missing_columns},
        )


def _unknown_columns(fieldnames: list[str]) -> list[str]:
    return [name for name in fieldnames if name not in _SUPPORTED_SAMPLE_COLUMNS]


def _build_output_columns(fieldnames: list[str]) -> list[str]:
    extras = [name for name in fieldnames if name not in _BASE_OUTPUT_COLUMNS]
    return list(dict.fromkeys([*_BASE_OUTPUT_COLUMNS, *extras]))


def _normalize_rows(
    rows: list[dict[str, str]],
    *,
    input_path: Path,
    output_columns: list[str],
    skip_alignment: bool = False,
) -> tuple[list[dict[str, str]], list[str], list[Path], list[Path], Counter[str]]:
    normalized_rows: list[dict[str, str]] = []
    sample_names: list[str] = []
    fastq_paths: list[Path] = []
    bam_paths: list[Path] = []
    strandedness_counts: Counter[str] = Counter()
    raw_samples_by_normalized: dict[str, str] = {}
    strandedness_by_sample: dict[str, str] = {}
    seen_fastq_rows: set[tuple[str, str, str]] = set()

    for line_number, row in enumerate(rows, start=2):
        normalized, sample, row_fastqs, row_bams = _normalize_row(
            row,
            input_path=input_path,
            output_columns=output_columns,
            line_number=line_number,
            skip_alignment=skip_alignment,
        )
        _reject_sample_name_collision(raw_samples_by_normalized, row, line_number, sample)
        _reject_inconsistent_strandedness(strandedness_by_sample, sample, normalized["strandedness"], line_number)
        _reject_duplicate_fastq_row(seen_fastq_rows, sample, row_fastqs, line_number)
        normalized_rows.append(normalized)
        if sample not in sample_names:
            sample_names.append(sample)
        fastq_paths.extend(row_fastqs)
        bam_paths.extend(row_bams)
        strandedness_counts[normalized["strandedness"]] += 1

    return normalized_rows, sample_names, fastq_paths, bam_paths, strandedness_counts


def _normalize_row(
    row: dict[str, str],
    *,
    input_path: Path,
    output_columns: list[str],
    line_number: int,
    skip_alignment: bool = False,
) -> tuple[dict[str, str], str, list[Path], list[Path]]:
    sample = _validate_sample_name(row, line_number)
    strandedness = _validate_strandedness(row, line_number)
    _validate_no_whitespace_fields(row, line_number)
    bam_provided = _row_has_bam(row)
    fastq_provided = _row_has_fastq(row)
    if bam_provided and fastq_provided and not skip_alignment:
        raise SkillError(
            stage="validation",
            error_code=ErrorCode.INVALID_SAMPLESHEET,
            message="A samplesheet row cannot mix FASTQ and BAM columns.",
            fix=(
                "Use either FASTQ columns (fastq_1[, fastq_2]) for fresh runs, OR BAM columns "
                "(genome_bam, transcriptome_bam) with --skip-alignment for reprocessing — never both."
            ),
            details={
                "line": line_number,
                "sample": sample,
                "fastq_columns": [c for c in _FASTQ_COLUMNS if str(row.get(c, "")).strip()],
                "bam_columns": [c for c in _BAM_COLUMNS if str(row.get(c, "")).strip()],
            },
        )
    if bam_provided:
        resolved_fastqs: dict[str, Path] = {}
        resolved_bams = _resolve_bam_columns(row, input_path=input_path, line_number=line_number)
    else:
        resolved_fastqs = _resolve_fastq_columns(row, input_path=input_path, line_number=line_number)
        resolved_bams = {}
    normalized = {column: str(row.get(column, "")).strip() for column in output_columns}
    normalized.update(
        {
            "sample": sample,
            "fastq_1": resolved_fastqs["fastq_1"].as_posix() if "fastq_1" in resolved_fastqs else "",
            "fastq_2": resolved_fastqs["fastq_2"].as_posix() if "fastq_2" in resolved_fastqs else "",
            "strandedness": strandedness,
            "genome_bam": resolved_bams.get("genome_bam", Path("")).as_posix() if "genome_bam" in resolved_bams else "",
            "transcriptome_bam": (
                resolved_bams.get("transcriptome_bam", Path("")).as_posix()
                if "transcriptome_bam" in resolved_bams
                else ""
            ),
        }
    )
    return normalized, sample, list(resolved_fastqs.values()), list(resolved_bams.values())


def _row_has_fastq(row: dict[str, str]) -> bool:
    return any(str(row.get(column, "")).strip() for column in _FASTQ_COLUMNS)


def _row_has_bam(row: dict[str, str]) -> bool:
    return any(str(row.get(column, "")).strip() for column in _BAM_COLUMNS)


def _validate_no_whitespace_fields(row: dict[str, str], line_number: int) -> None:
    for column in _NO_WHITESPACE_COLUMNS:
        value = str(row.get(column, "")).strip()
        if value and not _NO_WHITESPACE_RE.match(value):
            raise SkillError(
                stage="validation",
                error_code=ErrorCode.INVALID_SAMPLESHEET,
                message=f"{column} must not contain whitespace (nf-core schema pattern: ^\\S+$).",
                fix=f"Remove spaces from the {column} value, e.g. 'MyCenter' not 'My Center'.",
                details={"line": line_number, "column": column, "value": value},
            )


def _validate_sample_name(row: dict[str, str], line_number: int) -> str:
    raw_sample = str(row.get("sample", "")).strip()
    sample = _normalize_sample_name(raw_sample)
    if not sample or not _SAMPLE_NAME_RE.match(sample):
        raise SkillError(
            stage="validation",
            error_code=ErrorCode.INVALID_SAMPLESHEET,
            message="Sample names must be non-empty and cannot contain whitespace after normalization.",
            fix="Provide a non-empty sample value; whitespace is normalized to underscores before validation.",
            details={"line": line_number, "sample": raw_sample, "normalized_sample": sample},
        )
    return sample


def _normalize_sample_name(raw_sample: str) -> str:
    return _SAMPLE_WHITESPACE_RE.sub("_", raw_sample.strip())


def _validate_strandedness(row: dict[str, str], line_number: int) -> str:
    strandedness = str(row.get("strandedness", "")).strip()
    if strandedness not in SUPPORTED_STRANDEDNESS:
        raise SkillError(
            stage="validation",
            error_code=ErrorCode.INVALID_STRANDEDNESS,
            message="Invalid strandedness value in samplesheet.",
            fix="Use one of: auto, forward, reverse, unstranded.",
            details={"line": line_number, "strandedness": strandedness},
        )
    return strandedness


def _resolve_fastq_columns(row: dict[str, str], *, input_path: Path, line_number: int) -> dict[str, Path]:
    resolved: dict[str, Path] = {}
    for column in _FASTQ_COLUMNS:
        raw_value = str(row.get(column, "")).strip()
        if column == "fastq_2" and not raw_value:
            continue
        if column == "fastq_1" and not raw_value:
            raise SkillError(
                stage="validation",
                error_code=ErrorCode.INVALID_SAMPLESHEET,
                message="fastq_1 is required for every row.",
                fix="Provide a FASTQ path in the fastq_1 column.",
                details={"line": line_number, "column": column},
            )
        path = _resolve_path(raw_value, base_dir=input_path.parent)
        _validate_fastq_path(path, column=column, line_number=line_number)
        resolved[column] = path
    return resolved


def _resolve_bam_columns(row: dict[str, str], *, input_path: Path, line_number: int) -> dict[str, Path]:
    resolved: dict[str, Path] = {}
    for column in _BAM_COLUMNS:
        raw_value = str(row.get(column, "")).strip()
        if not raw_value:
            continue
        path = _resolve_path(raw_value, base_dir=input_path.parent)
        _validate_bam_path(path, column=column, line_number=line_number)
        resolved[column] = path
    _validate_percent_mapped(row, line_number=line_number)
    return resolved


def _validate_bam_path(path: Path, *, column: str, line_number: int) -> None:
    if not _BAM_BASENAME_RE.match(path.name):
        raise SkillError(
            stage="validation",
            error_code=ErrorCode.INVALID_BAM,
            message="BAM path does not have a .bam extension.",
            fix="Ensure the genome_bam or transcriptome_bam column points to a file ending in .bam or .BAM.",
            details={"line": line_number, "column": column, "filename": path.name},
        )
    if not path.exists():
        raise SkillError(
            stage="validation",
            error_code=ErrorCode.MISSING_INPUT,
            message="BAM path in samplesheet was not found.",
            fix=f"Correct the {column} path or remove it from the samplesheet.",
            details={"line": line_number, "column": column, "path": str(path)},
        )


def _validate_percent_mapped(row: dict[str, str], *, line_number: int) -> None:
    raw = str(row.get("percent_mapped", "")).strip()
    if not raw:
        return
    try:
        value = float(raw)
    except ValueError:
        raise SkillError(
            stage="validation",
            error_code=ErrorCode.INVALID_SAMPLESHEET,
            message="percent_mapped must be a numeric value between 0 and 100.",
            fix="Provide a number between 0 and 100 for percent_mapped, or leave the field empty.",
            details={"line": line_number, "percent_mapped": raw},
        )
    if not (0.0 <= value <= 100.0):
        raise SkillError(
            stage="validation",
            error_code=ErrorCode.INVALID_SAMPLESHEET,
            message="percent_mapped is out of range — must be between 0 and 100.",
            fix="Provide a number between 0 and 100 for percent_mapped.",
            details={"line": line_number, "percent_mapped": value},
        )


def _resolve_path(value: str, *, base_dir: Path) -> Path:
    path = Path(os.path.expanduser(value))
    if not path.is_absolute():
        path = base_dir / path
    return path.resolve()


def _validate_fastq_path(path: Path, *, column: str, line_number: int) -> None:
    if not _looks_like_fastq_path(path):
        raise SkillError(
            stage="validation",
            error_code=ErrorCode.INVALID_FASTQ,
            message="FASTQ basename is not compatible with nf-core/rnaseq.",
            fix="Use .fq, .fastq, .fq.gz, or .fastq.gz and remove whitespace from the basename.",
            details={"line": line_number, "column": column, "filename": path.name},
        )
    if not path.exists():
        raise SkillError(
            stage="validation",
            error_code=ErrorCode.MISSING_FASTQ,
            message="FASTQ file was not found.",
            fix="Correct the FASTQ path in the samplesheet.",
            details={"line": line_number, "column": column, "path": str(path)},
        )


def _looks_like_fastq_path(path: Path) -> bool:
    return bool(_FASTQ_BASENAME_RE.match(path.name))


def _reject_sample_name_collision(
    raw_samples_by_normalized: dict[str, str],
    row: dict[str, str],
    line_number: int,
    sample: str,
) -> None:
    raw_sample = str(row.get("sample", "")).strip()
    previous_raw = raw_samples_by_normalized.setdefault(sample, raw_sample)
    if previous_raw != raw_sample:
        raise SkillError(
            stage="validation",
            error_code=ErrorCode.INVALID_SAMPLESHEET,
            message="Two sample names collide after whitespace normalization.",
            fix="Rename samples so whitespace-normalized names are unique.",
            details={
                "line": line_number,
                "sample": raw_sample,
                "previous_sample": previous_raw,
                "normalized_sample": sample,
            },
        )


def _reject_inconsistent_strandedness(
    strandedness_by_sample: dict[str, str],
    sample: str,
    strandedness: str,
    line_number: int,
) -> None:
    previous = strandedness_by_sample.setdefault(sample, strandedness)
    if previous != strandedness:
        raise SkillError(
            stage="validation",
            error_code=ErrorCode.INVALID_STRANDEDNESS,
            message="Repeated sample rows must use the same strandedness.",
            fix="Use one strandedness value for all technical replicate rows of a sample.",
            details={"line": line_number, "sample": sample, "previous": previous, "observed": strandedness},
        )


def _reject_duplicate_fastq_row(
    seen_fastq_rows: set[tuple[str, str, str]],
    sample: str,
    fastqs: list[Path],
    line_number: int,
) -> None:
    key = (sample, fastqs[0].as_posix() if fastqs else "", fastqs[1].as_posix() if len(fastqs) > 1 else "")
    if key in seen_fastq_rows:
        raise SkillError(
            stage="validation",
            error_code=ErrorCode.INVALID_SAMPLESHEET,
            message="Duplicate sample/FASTQ row found.",
            fix="Remove duplicate technical replicate rows from the samplesheet.",
            details={"line": line_number, "sample": sample},
        )
    seen_fastq_rows.add(key)


def _write_normalized_samplesheet(output_path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
