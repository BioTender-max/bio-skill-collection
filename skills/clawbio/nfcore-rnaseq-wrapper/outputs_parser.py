from __future__ import annotations

import sys
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


def parse_outputs(
    output_dir: Path,
    *,
    aligner: str = "star_salmon",
    pseudo_aligner: str | None = None,
    skip_alignment: bool = False,
    skip_quantification_merge: bool = False,
) -> dict[str, object]:
    upstream_dir = _require_upstream_results_dir(output_dir)
    aligner_effective = aligner or "star_salmon"
    aligner_dir = upstream_dir / aligner_effective
    pseudo_aligner_effective = pseudo_aligner or ""
    quant_dir = _select_quant_dir(upstream_dir, aligner_dir, aligner_effective, pseudo_aligner_effective, skip_alignment)
    quant_prefix = _select_quant_prefix(aligner_effective, pseudo_aligner_effective, quant_dir)

    per_sample_quant_dirs: list[str] = []
    rsem_genes_results: list[str] = []
    preferred_counts_tsv = ""
    raw_counts_tsv = ""
    tpm_tsv = ""
    rds_file = ""
    tx2gene_augmented = ""
    kallisto_counts_tsv = ""
    salmon_pseudo_counts_tsv = ""
    rsem_gene_counts_scaled_tsv = ""
    rsem_gene_lengths_tsv = ""
    rsem_tx2gene_tsv = ""
    rsem_tx2gene_augmented_tsv = ""
    rsem_transcript_counts_tsv = ""
    rsem_transcript_tpm_tsv = ""
    rsem_transcript_lengths_tsv = ""
    rsem_transcript_rds = ""
    rsem_merge_counts_dir = ""
    salmon_gene_counts_scaled_tsv = ""
    salmon_gene_lengths_tsv = ""
    salmon_tx2gene_tsv = ""
    transcript_counts_tsv = ""
    transcript_tpm_tsv = ""
    transcript_rds = ""
    transcript_lengths_tsv = ""

    if skip_quantification_merge:
        per_sample_quant_dirs = _find_per_sample_quant_dirs(quant_dir, quant_prefix)
    elif aligner_effective == "star_rsem":
        rsem_genes_results = _find_rsem_genes_results(aligner_dir)
        raw_counts_tsv = _existing(aligner_dir / "rsem.merged.gene_counts.tsv")
        preferred_counts_tsv = _existing(aligner_dir / "rsem.merged.gene_counts_length_scaled.tsv") or raw_counts_tsv
        tpm_tsv = _existing(aligner_dir / "rsem.merged.gene_tpm.tsv")
        rds_file = _existing(aligner_dir / "rsem.merged.gene.SummarizedExperiment.rds")
        rsem_gene_counts_scaled_tsv = _existing(aligner_dir / "rsem.merged.gene_counts_scaled.tsv")
        rsem_gene_lengths_tsv = _existing(aligner_dir / "rsem.merged.gene_lengths.tsv")
        rsem_tx2gene_tsv = _existing(aligner_dir / "rsem.merged.tx2gene.tsv")
        rsem_tx2gene_augmented_tsv = _existing(aligner_dir / "rsem.merged.tx2gene_augmented.tsv")
        rsem_transcript_counts_tsv = _existing(aligner_dir / "rsem.merged.transcript_counts.tsv")
        rsem_transcript_tpm_tsv = _existing(aligner_dir / "rsem.merged.transcript_tpm.tsv")
        rsem_transcript_lengths_tsv = _existing(aligner_dir / "rsem.merged.transcript_lengths.tsv")
        rsem_transcript_rds = _existing(aligner_dir / "rsem.merged.transcript.SummarizedExperiment.rds")
        # Legacy RSEM merge script outputs — documented in nf-core/rnaseq 3.26.0 output docs.
        # Contains *.gene_counts.tsv, *.gene_tpm.tsv, *.transcript_counts.tsv, etc.
        rsem_merge_counts_dir = _existing(aligner_dir / "rsem_merge_counts")
    elif quant_prefix:
        raw_counts_tsv = _existing(quant_dir / f"{quant_prefix}.merged.gene_counts.tsv")
        preferred_counts_tsv = _existing(quant_dir / f"{quant_prefix}.merged.gene_counts_length_scaled.tsv") or raw_counts_tsv
        tpm_tsv = _existing(quant_dir / f"{quant_prefix}.merged.gene_tpm.tsv") or _existing(quant_dir / f"{quant_prefix}.gene_tpm.tsv")
        rds_file = _existing(quant_dir / f"{quant_prefix}.merged.gene.SummarizedExperiment.rds")
        tx2gene_augmented = _existing(quant_dir / f"{quant_prefix}.merged.tx2gene_augmented.tsv")
        salmon_gene_counts_scaled_tsv = _existing(quant_dir / f"{quant_prefix}.merged.gene_counts_scaled.tsv")
        salmon_gene_lengths_tsv = _existing(quant_dir / f"{quant_prefix}.merged.gene_lengths.tsv")
        salmon_tx2gene_tsv = _existing(quant_dir / f"{quant_prefix}.merged.tx2gene.tsv")
        transcript_counts_tsv = _existing(quant_dir / f"{quant_prefix}.merged.transcript_counts.tsv")
        transcript_tpm_tsv = _existing(quant_dir / f"{quant_prefix}.merged.transcript_tpm.tsv")
        transcript_rds = _existing(quant_dir / f"{quant_prefix}.merged.transcript.SummarizedExperiment.rds")
        transcript_lengths_tsv = _existing(quant_dir / f"{quant_prefix}.merged.transcript_lengths.tsv")

    # Kallisto co-quant: when pseudo_aligner=kallisto runs alongside a primary aligner
    # (skip_alignment=False), the pipeline produces independent kallisto output at
    # upstream/results/kallisto/ in addition to the primary aligner's salmon counts.
    if pseudo_aligner_effective == "kallisto" and not skip_alignment and not skip_quantification_merge:
        kallisto_dir = upstream_dir / "kallisto"
        kallisto_counts_tsv = (
            _existing(kallisto_dir / "kallisto.merged.gene_counts_length_scaled.tsv")
            or _existing(kallisto_dir / "kallisto.merged.gene_counts.tsv")
        )

    # Salmon co-quant: when pseudo_aligner=salmon runs alongside a primary aligner
    # (skip_alignment=False), the pipeline produces an independent standalone salmon/
    # directory at upstream/results/salmon/ separate from the STAR-aligned outputs in
    # star_salmon/.  This mirrors the kallisto_counts_tsv pattern above.
    if pseudo_aligner_effective == "salmon" and not skip_alignment and not skip_quantification_merge:
        salmon_pseudo_dir = upstream_dir / "salmon"
        salmon_pseudo_counts_tsv = (
            _existing(salmon_pseudo_dir / "salmon.merged.gene_counts_length_scaled.tsv")
            or _existing(salmon_pseudo_dir / "salmon.merged.gene_counts.tsv")
        )

    hisat2_no_quant = aligner_effective == "hisat2" and not preferred_counts_tsv

    samples_detected = _detect_samples(
        preferred_counts_tsv or raw_counts_tsv,
        per_sample_quant_dirs=per_sample_quant_dirs,
        rsem_genes_results=rsem_genes_results,
    )

    return {
        "aligner_effective": aligner_effective,
        "pseudo_aligner_effective": pseudo_aligner_effective,
        "quant_dir": str(quant_dir) if quant_prefix else "",
        "quant_prefix": quant_prefix,
        "preferred_counts_tsv": preferred_counts_tsv,
        "raw_counts_tsv": raw_counts_tsv,
        "tpm_tsv": tpm_tsv,
        "rds_file": rds_file,
        "tx2gene_augmented": tx2gene_augmented,
        "kallisto_counts_tsv": kallisto_counts_tsv,
        "salmon_pseudo_counts_tsv": salmon_pseudo_counts_tsv,
        "per_sample_quant_dirs": per_sample_quant_dirs,
        "rsem_genes_results": rsem_genes_results,
        "rsem_gene_counts_scaled_tsv": rsem_gene_counts_scaled_tsv,
        "rsem_gene_lengths_tsv": rsem_gene_lengths_tsv,
        "rsem_tx2gene_tsv": rsem_tx2gene_tsv,
        "rsem_tx2gene_augmented_tsv": rsem_tx2gene_augmented_tsv,
        "salmon_gene_counts_scaled_tsv": salmon_gene_counts_scaled_tsv,
        "salmon_gene_lengths_tsv": salmon_gene_lengths_tsv,
        "salmon_tx2gene_tsv": salmon_tx2gene_tsv,
        "transcript_counts_tsv": transcript_counts_tsv,
        "transcript_tpm_tsv": transcript_tpm_tsv,
        "transcript_rds": transcript_rds,
        "transcript_lengths_tsv": transcript_lengths_tsv,
        "rsem_transcript_counts_tsv": rsem_transcript_counts_tsv,
        "rsem_transcript_tpm_tsv": rsem_transcript_tpm_tsv,
        "rsem_transcript_lengths_tsv": rsem_transcript_lengths_tsv,
        "rsem_transcript_rds": rsem_transcript_rds,
        "rsem_merge_counts_dir": rsem_merge_counts_dir,
        "bam_reprocessing_samplesheet": _existing(upstream_dir / "samplesheets" / "samplesheet_with_bams.csv"),
        "multiqc_report": find_multiqc_report(upstream_dir, aligner_effective),
        "multiqc_reports": find_multiqc_reports(upstream_dir, aligner_effective),
        "pipeline_info_dir": find_pipeline_info_dir(upstream_dir),
        "samples_detected": samples_detected,
        "handoff_available": bool(preferred_counts_tsv) and not skip_quantification_merge,
        "hisat2_no_quant": hisat2_no_quant,
        "skip_quantification_merge": bool(skip_quantification_merge),
    }


def _require_upstream_results_dir(output_dir: Path) -> Path:
    upstream_dir = Path(output_dir) / "upstream" / "results"
    if upstream_dir.exists():
        return upstream_dir
    raise SkillError(
        stage="parsing",
        error_code=ErrorCode.EXPECTED_OUTPUTS_NOT_FOUND,
        message="Pipeline output directory was not created.",
        fix="Re-run the wrapper after checking the Nextflow logs.",
        details={"expected_dir": str(upstream_dir)},
    )


def find_multiqc_report(upstream_dir: Path, aligner: str) -> str:
    """Return the primary (aligner-level) MultiQC report path, or the most recently modified."""
    aligner_report = upstream_dir / "multiqc" / aligner / "multiqc_report.html"
    if aligner_report.exists():
        return str(aligner_report)
    matches = list(upstream_dir.glob("multiqc/**/multiqc_report.html"))
    if not matches:
        matches = list(upstream_dir.glob("**/multiqc_report.html"))
    if not matches:
        matches = list(upstream_dir.glob("**/*multiqc_report.html"))
    # Pick the most recently modified file so a fallback glob never silently
    # returns the wrong report due to alphabetical ordering.
    # Break mtime ties with the path string so the result is always deterministic
    # on filesystems with coarse timestamp resolution (FAT32, some HPC mounts).
    return str(max(matches, key=lambda p: (p.stat().st_mtime, str(p)))) if matches else ""


def find_multiqc_reports(upstream_dir: Path, aligner: str) -> list[str]:
    """Return all MultiQC report paths found under upstream_dir.

    rapid_quant.config generates per-sample MultiQC reports alongside (or
    instead of) a merged aligner-level report.  This function enumerates
    every multiqc_report.html so provenance audits can see all of them.
    The list is sorted for deterministic ordering.
    """
    matches = sorted(upstream_dir.glob("multiqc/**/multiqc_report.html"))
    if not matches:
        matches = sorted(upstream_dir.glob("**/multiqc_report.html"))
    if not matches:
        matches = sorted(upstream_dir.glob("**/*multiqc_report.html"))
    return [str(m) for m in matches]


def find_pipeline_info_dir(upstream_dir: Path) -> str:
    pipeline_info_dir = upstream_dir / "pipeline_info"
    return str(pipeline_info_dir) if pipeline_info_dir.exists() else ""


def _existing(path: Path) -> str:
    return str(path) if path.exists() else ""


def _select_quant_dir(
    upstream_dir: Path,
    aligner_dir: Path,
    aligner: str,
    pseudo_aligner: str,
    skip_alignment: bool,
) -> Path:
    if pseudo_aligner and (skip_alignment or aligner == "hisat2"):
        return upstream_dir / pseudo_aligner
    return aligner_dir


def _select_quant_prefix(aligner: str, pseudo_aligner: str, quant_dir: Path) -> str:
    if aligner == "hisat2" and not pseudo_aligner:
        return ""
    if pseudo_aligner and quant_dir.name == pseudo_aligner:
        return pseudo_aligner
    if aligner in {"star_salmon", "bowtie2_salmon"}:
        return "salmon"
    return ""


def _find_per_sample_quant_dirs(quant_dir: Path, quant_prefix: str) -> list[str]:
    if not quant_prefix:
        return []
    # For aligner+Salmon routes (star_salmon, bowtie2_salmon) nf-core/rnaseq 3.26.0
    # places per-sample quant dirs directly under the aligner dir:
    #   star_salmon/<SAMPLE>/quant.sf
    # The nested probe (quant_dir/<prefix>/) is kept as a legacy fallback for older
    # pipeline versions that wrote star_salmon/salmon/<SAMPLE>/quant.sf.
    # For standalone pseudo-aligner runs quant_dir.name == quant_prefix (e.g.
    # upstream/results/salmon with prefix "salmon"), so quant_dir itself is the root.
    if quant_dir.name != quant_prefix:
        quant_files = sorted((quant_dir / quant_prefix).glob("*/quant.sf"))
        if quant_files:
            return [str(path.parent) for path in quant_files]
    quant_files = sorted(quant_dir.glob("*/quant.sf"))
    if not quant_files and quant_prefix == "kallisto":
        quant_files = sorted(quant_dir.glob("*/abundance.tsv"))
    return [str(path.parent) for path in quant_files]


def _find_rsem_genes_results(aligner_dir: Path) -> list[str]:
    return sorted(str(path) for path in aligner_dir.glob("*.genes.results"))


def _detect_samples(
    counts_tsv: str,
    *,
    per_sample_quant_dirs: list[str],
    rsem_genes_results: list[str],
) -> int:
    if per_sample_quant_dirs:
        return len(per_sample_quant_dirs)
    if counts_tsv:
        return _sample_count_from_tsv_header(Path(counts_tsv))
    if rsem_genes_results:
        return len(rsem_genes_results)
    return 0


_NONSAMPLE_HEADER_COLS = frozenset(
    {"gene_id", "gene_name", "tx_id", "transcript_id", "feature_id"}
)


def _sample_count_from_tsv_header(path: Path) -> int:
    # Stream just the first line: count matrices can have millions of rows and
    # read_text() pulls the whole file into memory only to discard everything
    # past the header.
    try:
        with path.open(encoding="utf-8") as handle:
            first_line = handle.readline()
    except OSError:
        return 0
    if not first_line:
        return 0
    columns = first_line.rstrip("\n").split("\t")
    # nf-core merged TSVs have gene_id + gene_name (2 cols) before sample cols.
    # Count all known identifier columns; fall back to 1 for unknown formats.
    n_id = sum(1 for c in columns if c in _NONSAMPLE_HEADER_COLS)
    return max(0, len(columns) - (n_id if n_id > 0 else 1))
