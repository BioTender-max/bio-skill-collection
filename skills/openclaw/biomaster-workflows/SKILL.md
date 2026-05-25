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
name: biomaster-workflows
description: Pipeline maestro
keywords:
  - workflows
  - RNAseq
  - ChIPseq
  - automation
  - YAML
measurable_outcome: Execute a configured pipeline end-to-end (including QC report + summary) within 24 hours of receiving inputs, logging every tool/parameter.
license: MIT
metadata:
  author: BioMaster Team
  version: "1.0.0"
compatibility:
  - system: Python 3.9+
allowed-tools:
  - run_shell_command
  - read_file
---

# BioMaster Workflows

Orchestrate BioMaster’s multi-agent pipelines (RNA-seq, ChIP-seq, single-cell, Hi-C) using the provided configs and repos to deliver reproducible outputs.

## Workflow
1. **Config prep:** Populate YAML with tool paths, reference genomes, and workflow selection (`rnaseq`, `chipseq`, `singlecell`, `hic`).
2. **Environment:** `cd repo && pip install -r requirements.txt` (or container) prior to running.
3. **Launch:** `python repo/run.py --config repo/config.yaml` (or chosen config) and monitor progress.
4. **Error recovery:** Let BioMaster agents retry failing stages; review logs for missing reference/index files.
5. **Output packaging:** Collect BAMs/counts/peaks + QC + narrative summary of parameters and runtimes.

## Guardrails
- Fail fast when reference files or indices are absent to avoid wasted compute.
- Record tool versions for every stage (alignment, quantification, etc.).
- Require confirmation before deleting intermediates or rerunning destructive steps.

## References
- Full workflow descriptions, supported modalities, and repo links reside in `README.md`.


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->