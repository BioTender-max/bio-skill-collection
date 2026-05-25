<!--
# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

-->

# Single-Cell RNA-seq Quality Control

**ID:** `biomedical.genomics.single_cell_qc`
**Version:** 1.1.0
**Status:** Production
**Category:** Genomics / Single-Cell Analysis

---

## Overview

The **Single-Cell RNA-seq Quality Control Skill** runs a production-grade QC workflow for single-cell transcriptomics. It computes standard scverse metrics and applies **MAD-based outlier detection** with **log1p transforms for counts/genes** plus **high-tail filtering for mitochondrial percentage**. The result is a reproducible, dataset-adaptive filter that removes low-quality cells and likely doublets while preserving biological heterogeneity.

---

## Key Capabilities

1. **Adaptive QC thresholds** using Median Absolute Deviation (MAD) instead of fixed cutoffs.
2. **Multi-metric filtering** for library size, gene detection, and mitochondrial content.
3. **Publication-ready plots** (before/after distributions and threshold overlays).
4. **Machine-readable summary** (`qc_summary.json`) for pipelines and audits.

---

## Supported Inputs

- `.h5ad` (AnnData)
- `.h5` (10x Genomics HDF5)
- 10x Genomics **directory** (matrix.mtx + barcodes + features/genes)

**Gene patterns**
- `mt_pattern` and `ribo_pattern` are **comma-separated prefixes** (e.g., `mt-,MT-`).
- `hb_pattern` is a **regex** (default: `^Hb[^(p)]|^HB[^(P)]`).

---

## Outputs

All outputs are written to `<input_basename>_qc_results/` unless overridden.

- `qc_metrics_before_filtering.png`
- `qc_filtering_thresholds.png`
- `qc_metrics_after_filtering.png`
- `<input_basename>_filtered.h5ad`
- `<input_basename>_with_qc.h5ad`
- `qc_summary.json`

---

## Usage

### Command Line

```bash
# H5AD input
python qc_analysis.py /path/to/data.h5ad --output-dir ./qc_results

# 10x H5 input
python qc_analysis.py /path/to/raw_feature_bc_matrix.h5

# 10x directory input
python qc_analysis.py /path/to/10x_directory/

# Customize thresholds
python qc_analysis.py data.h5ad --mad-counts 4 --mad-genes 4 --mad-mt 2.5 --mt-threshold 10

# Disable log1p transform for MAD calculations (advanced)
python qc_analysis.py data.h5ad --no-log1p
```

### Python API

```python
import anndata as ad
from qc_core import calculate_qc_metrics, build_qc_masks, filter_cells, filter_genes

adata = ad.read_h5ad("sample.h5ad")
calculate_qc_metrics(adata, inplace=True)

masks = build_qc_masks(
    adata,
    mad_counts=5,
    mad_genes=5,
    mad_mt=3,
    mt_threshold=8,
    counts_transform="log1p",
    genes_transform="log1p"
)

adata_filtered = filter_cells(adata, masks["pass_qc"], inplace=False)
filter_genes(adata_filtered, min_cells=20, inplace=True)
adata_filtered.write("sample_filtered.h5ad")
```

### LLM Agent Integration (Tool Skeleton)

```python
@tool
def run_scrna_qc(file_path: str) -> dict:
    """Run scRNA-seq QC and return a summary dict."""
    # Call qc_analysis.py or use qc_core helpers directly
    return {
        "status": "ok",
        "output_dir": "...",
        "summary_json": "qc_summary.json"
    }
```

---

## Parameters

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `file_path` | str | required | `.h5ad`, `.h5`, or 10x directory |
| `mad_counts` | float | 5.0 | MAD multiplier for total counts |
| `mad_genes` | float | 5.0 | MAD multiplier for genes per cell |
| `mad_mt` | float | 3.0 | MAD multiplier for mitochondrial % (high tail only) |
| `mt_threshold` | float | 8.0 | Hard MT% cutoff |
| `min_cells` | int | 20 | Gene filtering threshold |
| `mt_pattern` | str | `mt-,MT-` | Comma-separated prefixes |
| `ribo_pattern` | str | `Rpl,Rps,RPL,RPS` | Comma-separated prefixes |
| `hb_pattern` | str | `^Hb[^(p)]|^HB[^(P)]` | Regex |
| `no_log1p` | flag | false | Disable log1p for MAD on counts/genes |

---

## Methodology

- **Counts and genes** use MAD thresholds on log1p-transformed values.
- **Mitochondrial percentage** uses **high-tail MAD** plus a hard cutoff.
- **Ribosomal and hemoglobin metrics** are calculated for reporting and QC context.

This workflow aligns with scverse best practices and avoids over-filtering rare but valid cell types.

---

## qc_summary.json Schema (Key Fields)

```json
{
  "input": {"path": "...", "type": "h5ad"},
  "parameters": {"mad_counts": 5, "mad_genes": 5, "mad_mt": 3, "mt_threshold": 8},
  "counts": {"cells_before": 10000, "cells_after": 9200, "genes_before": 20000, "genes_after": 18000},
  "filtering": {"cells_removed": 800, "retention_rate": 92.0},
  "outputs": {"filtered_h5ad": "sample_filtered.h5ad"}
}
```

---

## Validation and Expected Ranges

- Healthy PBMC datasets typically retain 85-95% of cells.
- Tumor or stressed samples may retain 70-85% depending on MT% distribution.
- Always review pre/post plots before committing filtering decisions.

---

## Guardrails and Limitations

- QC is **not** doublet detection; use scDblFinder or scrublet afterward.
- Tissue-specific MT% baselines vary; adjust thresholds for neurons and cardiomyocytes.
- This workflow assumes droplet-based scRNA-seq; adjust for Smart-seq if needed.

---

## Related Skills

- **CRISPR Design Agent:** For follow-up knockout experiments.
- **Spatial Transcriptomics:** For spatial context after QC and annotation.
- **CellAgent:** For cell type labeling after QC.

---

## Author

**MD BABU MIA**
*Artificial Intelligence Group*
*Icahn School of Medicine at Mount Sinai*
md.babu.mia@mssm.edu


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->