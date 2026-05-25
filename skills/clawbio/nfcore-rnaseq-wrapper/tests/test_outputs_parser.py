from __future__ import annotations

from pathlib import Path
import sys

import pytest

_SKILL_DIR = Path(__file__).resolve().parent.parent
if str(_SKILL_DIR) in sys.path:
    sys.path.remove(str(_SKILL_DIR))
sys.path.insert(0, str(_SKILL_DIR))


def _purge_foreign_bare_modules(*names: str) -> None:
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


_purge_foreign_bare_modules("errors", "outputs_parser", "schemas")

from errors import SkillError
from outputs_parser import parse_outputs

_purge_local_modules("errors", "outputs_parser", "schemas")
if str(_SKILL_DIR) in sys.path:
    sys.path.remove(str(_SKILL_DIR))


def _upstream(root: Path) -> Path:
    path = root / "upstream" / "results"
    path.mkdir(parents=True)
    return path


def _write(path: Path, text: str = "x") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _merged_tsv(path: Path, samples: tuple[str, ...] = ("S1", "S2")) -> Path:
    # Real nf-core/rnaseq format: gene_id + gene_name + sample columns.
    return _write(path, "gene_id\tgene_name\t" + "\t".join(samples) + "\nENSG1\tMyGene\t1\t2\n")


def test_samples_detected_two_id_cols(tmp_path):
    # nf-core TSVs have gene_id + gene_name before sample columns; samples_detected
    # must not count gene_name as a sample (regression: was off-by-one before fix).
    upstream = _upstream(tmp_path)
    _merged_tsv(upstream / "star_salmon" / "salmon.merged.gene_counts_length_scaled.tsv", samples=("A", "B", "C"))
    result = parse_outputs(tmp_path, aligner="star_salmon")
    assert result["samples_detected"] == 3


def test_samples_detected_single_id_col(tmp_path):
    # Fallback: TSVs with only gene_id (no gene_name) still count correctly.
    upstream = _upstream(tmp_path)
    p = upstream / "star_salmon" / "salmon.merged.gene_counts_length_scaled.tsv"
    _write(p, "gene_id\tX\tY\nENSG1\t1\t2\n")
    result = parse_outputs(tmp_path, aligner="star_salmon")
    assert result["samples_detected"] == 2


def test_star_salmon_prefers_length_scaled_counts(tmp_path):
    upstream = _upstream(tmp_path)
    preferred = _merged_tsv(upstream / "star_salmon" / "salmon.merged.gene_counts_length_scaled.tsv")
    raw = _merged_tsv(upstream / "star_salmon" / "salmon.merged.gene_counts.tsv")
    result = parse_outputs(tmp_path, aligner="star_salmon")
    assert result["preferred_counts_tsv"] == str(preferred)
    assert result["raw_counts_tsv"] == str(raw)
    assert result["handoff_available"] is True


def test_star_salmon_falls_back_to_raw_counts(tmp_path):
    upstream = _upstream(tmp_path)
    raw = _merged_tsv(upstream / "star_salmon" / "salmon.merged.gene_counts.tsv")
    result = parse_outputs(tmp_path, aligner="star_salmon")
    assert result["preferred_counts_tsv"] == str(raw)
    assert result["raw_counts_tsv"] == str(raw)


def test_bowtie2_salmon_uses_its_own_aligner_dir(tmp_path):
    upstream = _upstream(tmp_path)
    preferred = _merged_tsv(upstream / "bowtie2_salmon" / "salmon.merged.gene_counts_length_scaled.tsv")
    _merged_tsv(upstream / "star_salmon" / "salmon.merged.gene_counts_length_scaled.tsv")
    result = parse_outputs(tmp_path, aligner="bowtie2_salmon")
    assert result["preferred_counts_tsv"] == str(preferred)
    assert result["aligner_effective"] == "bowtie2_salmon"


def test_star_rsem_prefers_length_scaled_counts_for_de_handoff(tmp_path):
    # length-scaled counts are the recommended DESeq2 input for RSEM (tximport
    # lengthScaledTPM), mirroring the star_salmon route's preference.
    upstream = _upstream(tmp_path)
    raw = _merged_tsv(upstream / "star_rsem" / "rsem.merged.gene_counts.tsv", ("S1", "S2"))
    length_scaled = _merged_tsv(upstream / "star_rsem" / "rsem.merged.gene_counts_length_scaled.tsv", ("S1", "S2"))
    result = parse_outputs(tmp_path, aligner="star_rsem")
    assert result["preferred_counts_tsv"] == str(length_scaled)
    assert result["raw_counts_tsv"] == str(raw)
    assert result["handoff_available"] is True


def test_hisat2_sets_no_quant_flags(tmp_path):
    _upstream(tmp_path)
    result = parse_outputs(tmp_path, aligner="hisat2")
    assert result["hisat2_no_quant"] is True
    assert result["handoff_available"] is False
    assert result["preferred_counts_tsv"] == ""


def test_hisat2_with_salmon_pseudo_aligner_exposes_merged_counts(tmp_path):
    upstream = _upstream(tmp_path)
    preferred = _merged_tsv(upstream / "salmon" / "salmon.merged.gene_counts_length_scaled.tsv")
    raw = _merged_tsv(upstream / "salmon" / "salmon.merged.gene_counts.tsv")
    result = parse_outputs(tmp_path, aligner="hisat2", pseudo_aligner="salmon")
    assert result["preferred_counts_tsv"] == str(preferred)
    assert result["raw_counts_tsv"] == str(raw)
    assert result["hisat2_no_quant"] is False
    assert result["handoff_available"] is True
    assert result["quant_dir"] == str(upstream / "salmon")


def test_skip_quantification_merge_collects_per_sample_quant_dirs(tmp_path):
    upstream = _upstream(tmp_path)
    q1 = _write(upstream / "star_salmon" / "salmon" / "S1" / "quant.sf")
    q2 = _write(upstream / "star_salmon" / "salmon" / "S2" / "quant.sf")
    result = parse_outputs(tmp_path, aligner="star_salmon", skip_quantification_merge=True)
    assert result["per_sample_quant_dirs"] == [str(q1.parent), str(q2.parent)]
    assert result["preferred_counts_tsv"] == ""
    assert result["handoff_available"] is False


def test_skip_quantification_merge_does_not_use_merged_counts(tmp_path):
    upstream = _upstream(tmp_path)
    _merged_tsv(upstream / "star_salmon" / "salmon.merged.gene_counts_length_scaled.tsv")
    result = parse_outputs(tmp_path, aligner="star_salmon", skip_quantification_merge=True)
    assert result["preferred_counts_tsv"] == ""
    assert result["skip_quantification_merge"] is True


def test_multiqc_prefers_aligner_specific_report(tmp_path):
    upstream = _upstream(tmp_path)
    _write(upstream / "multiqc" / "other" / "multiqc_report.html")
    wanted = _write(upstream / "multiqc" / "star_salmon" / "multiqc_report.html")
    result = parse_outputs(tmp_path, aligner="star_salmon")
    assert result["multiqc_report"] == str(wanted)


def test_parse_outputs_raises_when_upstream_results_missing(tmp_path):
    with pytest.raises(SkillError) as exc:
        parse_outputs(tmp_path, aligner="star_salmon")
    assert exc.value.error_code == "EXPECTED_OUTPUTS_NOT_FOUND"


def test_contract_contains_expected_keys(tmp_path):
    _upstream(tmp_path)
    result = parse_outputs(tmp_path, aligner="star_salmon")
    assert set(result) == {
            "aligner_effective",
            "pseudo_aligner_effective",
            "quant_dir",
            "quant_prefix",
            "preferred_counts_tsv",
        "raw_counts_tsv",
        "tpm_tsv",
        "rds_file",
        "tx2gene_augmented",
        "kallisto_counts_tsv",
        "salmon_pseudo_counts_tsv",
        "per_sample_quant_dirs",
        "rsem_genes_results",
        "rsem_gene_counts_scaled_tsv",
        "rsem_gene_lengths_tsv",
        "rsem_tx2gene_tsv",
        "rsem_tx2gene_augmented_tsv",
        "multiqc_report",
        "multiqc_reports",
        "pipeline_info_dir",
        "samples_detected",
        "handoff_available",
        "hisat2_no_quant",
        "skip_quantification_merge",
        "bam_reprocessing_samplesheet",
        # Salmon gene-level extras (M1/M2/L2)
        "salmon_gene_counts_scaled_tsv",
        "salmon_gene_lengths_tsv",
        "salmon_tx2gene_tsv",
        # Transcript-level (M3)
        "transcript_counts_tsv",
        "transcript_tpm_tsv",
        "transcript_rds",
        "transcript_lengths_tsv",
        "rsem_transcript_counts_tsv",
        "rsem_transcript_tpm_tsv",
        "rsem_transcript_lengths_tsv",
        "rsem_transcript_rds",
        # Legacy RSEM merge script output directory (nf-core/rnaseq 3.26.0 docs)
        "rsem_merge_counts_dir",
    }


def test_handoff_false_without_counts(tmp_path):
    _upstream(tmp_path)
    result = parse_outputs(tmp_path, aligner="star_salmon")
    assert result["handoff_available"] is False


def test_bam_reprocessing_samplesheet_detected_when_present(tmp_path):
    upstream = _upstream(tmp_path)
    ss = _write(upstream / "samplesheets" / "samplesheet_with_bams.csv")
    result = parse_outputs(tmp_path, aligner="star_salmon")
    assert result["bam_reprocessing_samplesheet"] == str(ss)


def test_salmon_gene_counts_scaled_detected(tmp_path):
    upstream = _upstream(tmp_path)
    f = _write(upstream / "star_salmon" / "salmon.merged.gene_counts_scaled.tsv")
    result = parse_outputs(tmp_path, aligner="star_salmon")
    assert result["salmon_gene_counts_scaled_tsv"] == str(f)


def test_find_multiqc_reports_returns_list(tmp_path):
    """find_multiqc_reports must return a list of all MultiQC HTML paths.

    rapid_quant.config generates per-sample MultiQC reports at
    multiqc/<sample>/multiqc_report.html in addition to (or instead of) a
    merged report.  The result payload should expose a multiqc_reports list
    so provenance audits can enumerate all reports.
    """
    import importlib
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "outputs_parser_mod2",
        Path(__file__).parent.parent / "outputs_parser.py",
    )
    op = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(op)
    find_multiqc_reports = op.find_multiqc_reports
    upstream = _upstream(tmp_path)
    r1 = _write(upstream / "multiqc" / "star_salmon" / "multiqc_report.html")
    r2 = _write(upstream / "multiqc" / "sampleA" / "multiqc_report.html")
    r3 = _write(upstream / "multiqc" / "sampleB" / "multiqc_report.html")
    reports = find_multiqc_reports(upstream, aligner="star_salmon")
    assert isinstance(reports, list), "find_multiqc_reports must return a list"
    assert len(reports) >= 1
    paths = {str(r) for r in reports}
    assert str(r1) in paths or str(r2) in paths  # at least one found


def test_skip_quantification_merge_collects_per_sample_quant_dirs_direct_layout(tmp_path):
    # nf-core/rnaseq 3.26.0 places quant dirs directly under the aligner dir:
    #   star_salmon/<SAMPLE>/quant.sf  (no nested salmon/ subdirectory)
    upstream = _upstream(tmp_path)
    q1 = _write(upstream / "star_salmon" / "S1" / "quant.sf")
    q2 = _write(upstream / "star_salmon" / "S2" / "quant.sf")
    result = parse_outputs(tmp_path, aligner="star_salmon", skip_quantification_merge=True)
    assert result["per_sample_quant_dirs"] == [str(q1.parent), str(q2.parent)]
    assert result["preferred_counts_tsv"] == ""
    assert result["handoff_available"] is False


def test_kallisto_coquant_counts_surfaced(tmp_path):
    upstream = _upstream(tmp_path)
    _merged_tsv(upstream / "star_salmon" / "salmon.merged.gene_counts_length_scaled.tsv")
    kal = _merged_tsv(upstream / "kallisto" / "kallisto.merged.gene_counts_length_scaled.tsv")
    result = parse_outputs(tmp_path, aligner="star_salmon", pseudo_aligner="kallisto")
    assert result["kallisto_counts_tsv"] == str(kal)
    assert result["preferred_counts_tsv"] != ""


def test_kallisto_coquant_empty_when_skip_alignment(tmp_path):
    upstream = _upstream(tmp_path)
    _merged_tsv(upstream / "kallisto" / "kallisto.merged.gene_counts_length_scaled.tsv")
    result = parse_outputs(tmp_path, aligner="star_salmon", pseudo_aligner="kallisto", skip_alignment=True)
    assert result["kallisto_counts_tsv"] == ""
    assert result["preferred_counts_tsv"] != ""


def test_kallisto_coquant_empty_when_skip_quantification_merge(tmp_path):
    upstream = _upstream(tmp_path)
    _write(upstream / "star_salmon" / "S1" / "quant.sf")
    result = parse_outputs(tmp_path, aligner="star_salmon", pseudo_aligner="kallisto", skip_quantification_merge=True)
    assert result["kallisto_counts_tsv"] == ""


def test_transcript_lengths_tsv_detected_for_star_salmon(tmp_path):
    """salmon.merged.transcript_lengths.tsv is produced by nf-core/rnaseq 3.26.0
    for star_salmon runs (confirmed in AWS megatest results) and must be surfaced."""
    upstream = _upstream(tmp_path)
    f = _write(upstream / "star_salmon" / "salmon.merged.transcript_lengths.tsv")
    result = parse_outputs(tmp_path, aligner="star_salmon")
    assert result["transcript_lengths_tsv"] == str(f)


# ---------------------------------------------------------------------------
# transcript_tpm_tsv and transcript_rds for star_salmon
# ---------------------------------------------------------------------------

def test_star_salmon_transcript_tpm_tsv_detected(tmp_path):
    """salmon.merged.transcript_tpm.tsv produced by star_salmon must be surfaced."""
    upstream = _upstream(tmp_path)
    f = _write(upstream / "star_salmon" / "salmon.merged.transcript_tpm.tsv")
    result = parse_outputs(tmp_path, aligner="star_salmon")
    assert result["transcript_tpm_tsv"] == str(f)


def test_star_salmon_transcript_rds_detected(tmp_path):
    """salmon.merged.transcript.SummarizedExperiment.rds must be surfaced for star_salmon."""
    upstream = _upstream(tmp_path)
    f = _write(upstream / "star_salmon" / "salmon.merged.transcript.SummarizedExperiment.rds")
    result = parse_outputs(tmp_path, aligner="star_salmon")
    assert result["transcript_rds"] == str(f)


# ---------------------------------------------------------------------------
# RSEM transcript-level outputs for star_rsem
# ---------------------------------------------------------------------------

def test_rsem_transcript_counts_tsv_detected(tmp_path):
    """rsem.merged.transcript_counts.tsv must be surfaced for star_rsem runs."""
    upstream = _upstream(tmp_path)
    f = _write(upstream / "star_rsem" / "rsem.merged.transcript_counts.tsv")
    result = parse_outputs(tmp_path, aligner="star_rsem")
    assert result["rsem_transcript_counts_tsv"] == str(f)


def test_rsem_transcript_tpm_tsv_detected(tmp_path):
    upstream = _upstream(tmp_path)
    f = _write(upstream / "star_rsem" / "rsem.merged.transcript_tpm.tsv")
    result = parse_outputs(tmp_path, aligner="star_rsem")
    assert result["rsem_transcript_tpm_tsv"] == str(f)


def test_rsem_transcript_lengths_tsv_detected(tmp_path):
    upstream = _upstream(tmp_path)
    f = _write(upstream / "star_rsem" / "rsem.merged.transcript_lengths.tsv")
    result = parse_outputs(tmp_path, aligner="star_rsem")
    assert result["rsem_transcript_lengths_tsv"] == str(f)


def test_rsem_transcript_rds_detected(tmp_path):
    upstream = _upstream(tmp_path)
    f = _write(upstream / "star_rsem" / "rsem.merged.transcript.SummarizedExperiment.rds")
    result = parse_outputs(tmp_path, aligner="star_rsem")
    assert result["rsem_transcript_rds"] == str(f)


# ---------------------------------------------------------------------------
# rsem_merge_counts_dir — legacy RSEM merge script output directory
# documented in nf-core/rnaseq 3.26.0 output docs under star_rsem/
# ---------------------------------------------------------------------------

def test_rsem_merge_counts_dir_detected_when_present(tmp_path):
    """star_rsem/rsem_merge_counts/ is a documented legacy output directory and
    must be surfaced so callers can enumerate the legacy TSV files inside it."""
    upstream = _upstream(tmp_path)
    merge_dir = upstream / "star_rsem" / "rsem_merge_counts"
    merge_dir.mkdir(parents=True)
    result = parse_outputs(tmp_path, aligner="star_rsem")
    assert result["rsem_merge_counts_dir"] == str(merge_dir)
