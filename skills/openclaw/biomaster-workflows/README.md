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

# BioMaster: Automated Bioinformatics Workflows

**ID:** `biomedical.genomics.biomaster`
**Version:** 1.1.0
**Status:** Integrated & Downloaded
**Category:** Genomics / Workflow Orchestration

---

## Overview

BioMaster is a multi-agent system for end-to-end bioinformatics pipelines across multiple omics modalities. It decomposes high-level tasks into reproducible steps with tool-specific parameters and error recovery.

---

## Supported Workflows

- RNA-seq: QC -> alignment -> quantification -> DEG -> enrichment
- ChIP-seq: QC -> alignment -> peak calling -> motif analysis
- Single-cell: QC -> normalization -> clustering -> annotation
- Hi-C: QC -> alignment -> contact map -> compartment analysis

---

## Inputs

| Field | Type | Notes |
|------|------|------|
| `config_path` | str | YAML config with tool paths and parameters |
| `input_data` | str | FASTQ, BAM, or h5ad depending on workflow |
| `workflow` | str | `rnaseq`, `chipseq`, `singlecell`, `hic` |

---

## Outputs

- Standard pipeline outputs (BAM, counts, peak files)
- QC reports and logs
- Summary report with parameters and runtime metadata

---

## Quick Start

```bash
cd repo
pip install -r requirements.txt
python repo/run.py --config repo/config.yaml
```

---

## Guardrails

- Always log tool versions and parameters for reproducibility.
- Fail fast on missing reference genomes or index files.
- Require explicit confirmation before deleting intermediate files.

---

## References

- https://github.com/ai4nucleome/BioMaster



<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->