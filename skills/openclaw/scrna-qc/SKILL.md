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

---
name: scrna-qc
description: Execute the MAD-based single-cell RNA-seq QC workflow (scripts + Python API) to filter low-quality cells and emit reports plus filtered AnnData files.
measurable_outcome: Produce filtered .h5ad files, before/after plots, and qc_summary.json within 20 minutes per dataset.
allowed-tools:
  - read_file
  - run_shell_command
---

## At-a-Glance
- **description (10-20 chars):** QC autopilot
- **keywords:** scRNAseq, MAD, h5ad, QC, plots

## Workflow
1. Accept `.h5ad`, 10x `.h5`, or 10x directory inputs; set mitochondrial/ribosomal patterns as needed.
2. Run `qc_analysis.py` (CLI) or call `qc_core` helpers to compute metrics, apply MAD thresholds, and filter cells/genes.
3. Generate standard plots (metrics before/after, threshold overlays) plus filtered data artifacts.
4. Document parameters (mad_counts/genes/mt, mt_threshold, min_cells, log1p flag) inside the summary JSON.
5. Provide guidance on next steps (doublet detection, downstream analysis).

## Guardrails
- Adjust MT% expectations for tissue context; avoid over-filtering rare populations.
- This workflow is QC only—doublet handling and batch correction stay separate.
- Keep reproducibility by storing command invocations and environment info.

## References
- See `README.md`, `qc_core.py`, `qc_analysis.py`, and `qc_plotting.py` for API usage and schema details.


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->