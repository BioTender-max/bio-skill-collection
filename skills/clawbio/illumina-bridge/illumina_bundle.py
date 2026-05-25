"""Helpers for discovering and parsing Illumina/DRAGEN export bundles."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SAMPLE_SHEET_PATTERNS = (
    "SampleSheet.csv",
    "samplesheet.csv",
    "*SampleSheet*.csv",
    "*sample_sheet*.csv",
)
VCF_PATTERNS = ("*.vcf.gz", "*.vcf")
QC_PATTERNS = (
    "qc_metrics.json",
    "*qc*.json",
    "*metrics*.json",
    "qc_metrics.csv",
    "*qc*.csv",
    "*metrics*.csv",
    "MetricsOutput.tsv",
    "*Metrics*.tsv",
    "*metrics*.tsv",
    "*qc*.tsv",
)
MOCK_ICA_FILENAME = "mock_ica_metadata.json"
SAMPLE_SHEET_SECTION_PRIORITY = (
    "cloud_tso500s_data",
    "data",
    "bclconvert_data",
    "cloud_data",
)


@dataclass(frozen=True)
class BundleArtifacts:
    """Discovered paths that define a DRAGEN export bundle."""

    bundle_dir: Path
    vcf_path: Path
    qc_path: Path
    sample_sheet_path: Path
    mock_ica_metadata_path: Path | None = None


def _sorted_matches(bundle_dir: Path, patterns: tuple[str, ...]) -> list[Path]:
    matches: list[Path] = []
    seen: set[Path] = set()
    for pattern in patterns:
        for path in sorted(bundle_dir.rglob(pattern), key=lambda p: str(p).lower()):
            if path.is_file() and path not in seen:
                matches.append(path)
                seen.add(path)
    return matches


def _resolve_artifact(
    bundle_dir: Path,
    override: str | Path | None,
    patterns: tuple[str, ...],
    label: str,
) -> Path:
    if override:
        path = Path(override).expanduser().resolve()
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"{label} override not found: {path}")
        return path

    matches = _sorted_matches(bundle_dir, patterns)
    if not matches:
        raise FileNotFoundError(
            f"No {label} found in bundle '{bundle_dir}'. Expected one of: {', '.join(patterns)}"
        )
    if label == "VCF":
        return _select_preferred_vcf(matches)
    return matches[0]


def _select_preferred_vcf(matches: list[Path]) -> Path:
    """Prefer primary result VCFs over intermediate or auxiliary outputs."""

    def score(path: Path) -> tuple[int, int, int, int, int, str]:
        text = str(path).lower()
        name = path.name.lower()
        return (
            0 if "/results/" in text else 1,
            0 if "hard-filtered" in name else 1,
            1 if ".raw." in name else 0,
            1 if "_rna" in text or "splice" in name else 0,
            1 if "cnv" in name or "annotated" in name or "abcn" in name else 0,
            text,
        )

    return sorted(matches, key=score)[0]


def discover_bundle_artifacts(
    bundle_dir: str | Path,
    *,
    vcf_override: str | Path | None = None,
    qc_override: str | Path | None = None,
    sample_sheet_override: str | Path | None = None,
) -> BundleArtifacts:
    """Discover the canonical artifact set for an Illumina export bundle."""

    bundle_dir = Path(bundle_dir).expanduser().resolve()
    if not bundle_dir.exists():
        raise FileNotFoundError(f"Bundle directory not found: {bundle_dir}")
    if not bundle_dir.is_dir():
        raise NotADirectoryError(f"Expected a bundle directory, got: {bundle_dir}")

    sample_sheet_path = _resolve_artifact(
        bundle_dir,
        sample_sheet_override,
        SAMPLE_SHEET_PATTERNS,
        "SampleSheet",
    )
    vcf_path = _resolve_artifact(bundle_dir, vcf_override, VCF_PATTERNS, "VCF")
    qc_path = _resolve_artifact(bundle_dir, qc_override, QC_PATTERNS, "QC metrics")

    mock_ica = bundle_dir / MOCK_ICA_FILENAME
    return BundleArtifacts(
        bundle_dir=bundle_dir,
        vcf_path=vcf_path,
        qc_path=qc_path,
        sample_sheet_path=sample_sheet_path,
        mock_ica_metadata_path=mock_ica if mock_ica.exists() else None,
    )


def is_recognizable_illumina_bundle(bundle_dir: str | Path) -> bool:
    """Heuristic used by the orchestrator to detect DRAGEN-like export folders."""

    try:
        bundle_dir = Path(bundle_dir).expanduser().resolve()
    except OSError:
        return False
    if not bundle_dir.exists() or not bundle_dir.is_dir():
        return False

    has_sample_sheet = bool(_sorted_matches(bundle_dir, SAMPLE_SHEET_PATTERNS))
    has_vcf = bool(_sorted_matches(bundle_dir, VCF_PATTERNS))
    return has_sample_sheet and has_vcf


def _extract_named_sections(lines: list[str]) -> list[tuple[str, list[str]]]:
    sections: list[tuple[str, list[str]]] = []
    current_name: str | None = None
    current_lines: list[str] = []

    for raw_line in lines:
        line = raw_line.strip()
        if line.startswith("[") and line.endswith("]"):
            if current_name is not None:
                sections.append((current_name, current_lines))
            current_name = line[1:-1].strip()
            current_lines = []
            continue
        if current_name is not None:
            current_lines.append(raw_line)

    if current_name is not None:
        sections.append((current_name, current_lines))
    return sections


def _candidate_section_score(section_name: str) -> tuple[int, str]:
    lowered = section_name.lower()
    try:
        return SAMPLE_SHEET_SECTION_PRIORITY.index(lowered), lowered
    except ValueError:
        return len(SAMPLE_SHEET_SECTION_PRIORITY), lowered


def _extract_data_section(lines: list[str]) -> list[str]:
    for section_name, section_lines in sorted(
        _extract_named_sections(lines),
        key=lambda item: _candidate_section_score(item[0]),
    ):
        meaningful_lines = [line for line in section_lines if line.strip()]
        if not meaningful_lines:
            continue
        headers = [cell.strip().lower() for cell in meaningful_lines[0].split(",")]
        if "sample_id" in headers:
            return meaningful_lines
    return []


def _normalize_sample_row(row: dict[str, str]) -> dict[str, str]:
    get = lambda *keys: next((row.get(key, "").strip() for key in keys if row.get(key, "").strip()), "")
    return {
        "sample_id": get("Sample_ID", "SampleID", "sample_id"),
        "sample_name": get("Sample_Name", "SampleName", "sample_name", "Pair_ID"),
        "sample_project": get("Sample_Project", "SampleProject", "sample_project", "ProjectName"),
        "sample_type": get("Sample_Type", "sample_type"),
        "pair_id": get("Pair_ID", "pair_id"),
        "sample_feature": get("Sample_Feature", "sample_feature"),
        "lane": get("Lane", "lane"),
        "index": get("index", "Index"),
        "index2": get("index2", "Index2"),
        "index_id": get("Index_ID", "index_id"),
        "project_name": get("ProjectName", "project_name"),
        "library_name": get("LibraryName", "library_name"),
        "library_prep_kit_name": get("LibraryPrepKitName", "library_prep_kit_name"),
        "index_adapter_kit_name": get("IndexAdapterKitName", "index_adapter_kit_name"),
        "description": get("Description", "description", "Sample_Feature"),
    }


def _merge_sample_row(existing: dict[str, str], incoming: dict[str, str]) -> dict[str, str]:
    merged = dict(existing)
    for key, value in incoming.items():
        if value and not merged.get(key):
            merged[key] = value
    return merged


def parse_sample_sheet(sample_sheet_path: str | Path) -> list[dict[str, str]]:
    """Parse a standard Illumina SampleSheet and return normalized sample rows."""

    sample_sheet_path = Path(sample_sheet_path)
    lines = sample_sheet_path.read_text(encoding="utf-8").splitlines(keepends=True)
    sections = _extract_named_sections(lines)
    merged_rows: dict[str, dict[str, str]] = {}
    sample_order: list[str] = []

    for section_name, section_lines in sorted(sections, key=lambda item: _candidate_section_score(item[0])):
        meaningful_lines = [line for line in section_lines if line.strip()]
        if not meaningful_lines:
            continue
        headers = [cell.strip().lower() for cell in meaningful_lines[0].split(",")]
        if "sample_id" not in headers:
            continue

        reader = csv.DictReader(meaningful_lines)
        for row in reader:
            cleaned = {
                (key or "").strip(): (value or "").strip()
                for key, value in row.items()
            }
            if not any(cleaned.values()):
                continue
            normalized = _normalize_sample_row(cleaned)
            if not normalized["sample_id"]:
                raise ValueError(
                    f"SampleSheet row missing Sample_ID in '{sample_sheet_path.name}': {cleaned}"
                )
            sample_id = normalized["sample_id"]
            if sample_id not in merged_rows:
                merged_rows[sample_id] = normalized
                sample_order.append(sample_id)
            else:
                merged_rows[sample_id] = _merge_sample_row(merged_rows[sample_id], normalized)

    if merged_rows:
        return [merged_rows[sample_id] for sample_id in sample_order]

    data_lines = _extract_data_section(lines)
    reader = csv.DictReader(data_lines or lines)
    normalized_rows: list[dict[str, str]] = []
    for row in reader:
        cleaned = {
            (key or "").strip(): (value or "").strip()
            for key, value in row.items()
        }
        if not any(cleaned.values()):
            continue
        normalized = _normalize_sample_row(cleaned)
        if not normalized["sample_id"]:
            raise ValueError(
                f"SampleSheet row missing Sample_ID in '{sample_sheet_path.name}': {cleaned}"
            )
        normalized_rows.append(normalized)

    if not normalized_rows:
        raise ValueError(f"No sample rows found in SampleSheet: {sample_sheet_path}")
    return normalized_rows


def _coerce_metric_value(value: str) -> Any:
    text = value.strip()
    if text in {"", "NA"}:
        return None
    if text.upper() == "TRUE":
        return True
    if text.upper() == "FALSE":
        return False
    try:
        if "." in text:
            return float(text)
        return int(text)
    except ValueError:
        return text


def _normalize_qc_keys(raw: dict[str, Any]) -> dict[str, Any]:
    aliases = {
        "run_id": ("run_id", "runId", "analysis_id", "analysisId"),
        "instrument": ("instrument", "instrument_name", "instrumentName", "sequencer"),
        "analysis_software": ("analysis_software", "analysisSoftware"),
        "workflow_version": ("workflow_version", "workflowVersion"),
        "yield_gb": ("yield_gb", "yieldGb", "yield_gbases", "yield"),
        "percent_q30": ("percent_q30", "percentQ30", "q30_percentage", "q30Percent"),
        "percent_q30_read1": ("percent_q30_read1", "percentQ30Read1", "PCT_Q30_R1"),
        "percent_q30_read2": ("percent_q30_read2", "percentQ30Read2", "PCT_Q30_R2"),
        "pf_reads": ("pf_reads", "pfReads", "pass_filter_reads", "passFilterReads"),
        "percent_pf_reads": ("percent_pf_reads", "percentPfReads", "PCT_PF_READS"),
        "cluster_density_k_mm2": (
            "cluster_density_k_mm2",
            "clusterDensityKmm2",
            "cluster_density",
        ),
        "completed_samples": ("completed_samples",),
        "reported_sample_count": ("reported_sample_count",),
    }
    normalized: dict[str, Any] = {}
    for target, keys in aliases.items():
        for key in keys:
            if key in raw:
                normalized[target] = raw[key]
                break
    normalized["raw_metrics"] = raw
    return normalized


def _parse_header_rows(rows: list[list[str]]) -> dict[str, Any]:
    header: dict[str, Any] = {}
    for row in rows:
        if len(row) >= 2 and row[0]:
            header[row[0]] = _coerce_metric_value(row[1])
    return header


def _parse_value_column_metrics(rows: list[list[str]]) -> dict[str, Any]:
    if len(rows) < 2:
        return {}
    header = rows[0]
    try:
        value_index = next(
            index for index, cell in enumerate(header) if cell.strip().lower() == "value"
        )
    except StopIteration:
        return {}

    metrics: dict[str, Any] = {}
    for row in rows[1:]:
        if row and row[0]:
            metric_name = row[0].split("(", 1)[0].strip()
            if value_index < len(row):
                metrics[metric_name] = _coerce_metric_value(row[value_index])
    return metrics


def _parse_analysis_status(rows: list[list[str]]) -> dict[str, Any]:
    if len(rows) < 2:
        return {}
    samples = [cell for cell in rows[0][1:] if cell]
    metrics: dict[str, list[Any]] = {}
    for row in rows[1:]:
        if row and row[0]:
            metrics[row[0]] = [_coerce_metric_value(value) for value in row[1 : 1 + len(samples)]]

    completed_values = metrics.get("COMPLETED_ALL_STEPS", [])
    failed_values = metrics.get("FAILED_STEPS", [])
    skipped_values = metrics.get("STEPS_NOT_EXECUTED", [])
    return {
        "reported_sample_count": len(samples),
        "completed_samples": sum(value is True for value in completed_values),
        "samples_with_failed_steps": sum(value not in {None, "", "NA"} for value in failed_values),
        "samples_with_skipped_steps": sum(value not in {None, "", "NA"} for value in skipped_values),
        "sample_ids": samples,
    }


def _parse_metrics_output_tsv(qc_path: Path) -> dict[str, Any]:
    title = ""
    sections: dict[str, list[list[str]]] = {}
    current_section: str | None = None

    for raw_line in qc_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if not title and not line.startswith("["):
            title = line
            continue
        if line.startswith("[") and line.endswith("]"):
            current_section = line[1:-1].strip()
            sections[current_section] = []
            continue
        if current_section is None:
            continue
        cells = [cell.strip() for cell in raw_line.split("\t")]
        while cells and not cells[-1]:
            cells.pop()
        if any(cells):
            sections[current_section].append(cells)

    header = _parse_header_rows(sections.get("Header", []))
    run_qc = _parse_value_column_metrics(sections.get("Run QC Metrics", []))
    analysis_status = _parse_analysis_status(sections.get("Analysis Status", []))

    percent_q30_r1 = run_qc.get("PCT_Q30_R1")
    percent_q30_r2 = run_qc.get("PCT_Q30_R2")
    percent_q30: float | None = None
    if isinstance(percent_q30_r1, (int, float)) and isinstance(percent_q30_r2, (int, float)):
        percent_q30 = round((float(percent_q30_r1) + float(percent_q30_r2)) / 2, 2)
    elif isinstance(percent_q30_r1, (int, float)):
        percent_q30 = float(percent_q30_r1)
    elif isinstance(percent_q30_r2, (int, float)):
        percent_q30 = float(percent_q30_r2)

    raw = {
        "analysis_software": title,
        "workflow_version": header.get("Workflow Version"),
        "output_date": header.get("Output Date"),
        "output_time": header.get("Output Time"),
        "PCT_PF_READS": run_qc.get("PCT_PF_READS"),
        "PCT_Q30_R1": percent_q30_r1,
        "PCT_Q30_R2": percent_q30_r2,
        "reported_sample_count": analysis_status.get("reported_sample_count"),
        "completed_samples": analysis_status.get("completed_samples"),
        "analysis_status": analysis_status,
        "sections_present": sorted(sections.keys()),
    }
    if percent_q30 is not None:
        raw["percent_q30"] = percent_q30
    return _normalize_qc_keys(raw)


def parse_qc_metrics(qc_path: str | Path) -> dict[str, Any]:
    """Parse QC metrics from JSON or CSV into a stable summary shape."""

    qc_path = Path(qc_path)
    suffix = qc_path.suffix.lower()

    if suffix == ".json":
        try:
            raw = json.loads(qc_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Malformed QC metrics JSON: {qc_path}") from exc

        if isinstance(raw, dict):
            if "summary" in raw and isinstance(raw["summary"], dict):
                return _normalize_qc_keys(raw["summary"])
            return _normalize_qc_keys(raw)
        raise ValueError(f"Unsupported QC metrics JSON structure in {qc_path}")

    if suffix == ".csv":
        rows = list(csv.DictReader(qc_path.read_text(encoding="utf-8").splitlines()))
        if not rows:
            raise ValueError(f"QC metrics CSV is empty: {qc_path}")

        if {"metric", "value"}.issubset(rows[0].keys()):
            raw = {row["metric"].strip(): row["value"].strip() for row in rows if row.get("metric")}
            return _normalize_qc_keys(raw)

        first_row = rows[0]
        if len(first_row) == 1:
            raise ValueError(f"QC metrics CSV is malformed: {qc_path}")
        return _normalize_qc_keys({k.strip(): v.strip() for k, v in first_row.items() if k})

    if suffix == ".tsv":
        return _parse_metrics_output_tsv(qc_path)

    raise ValueError(f"Unsupported QC metrics format: {qc_path.suffix}")


def summarize_sample_sheet(sample_rows: list[dict[str, str]]) -> dict[str, Any]:
    """Compute a stable summary used in reports and manifests."""

    sample_ids = [row["sample_id"] for row in sample_rows]
    projects = sorted({row["sample_project"] for row in sample_rows if row["sample_project"]})
    sample_types = sorted({row["sample_type"] for row in sample_rows if row.get("sample_type")})
    return {
        "sample_count": len(sample_rows),
        "sample_ids": sample_ids,
        "sample_projects": projects,
        "sample_types": sample_types,
    }
