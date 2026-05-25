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

# STAgent (Spatial Transcriptomics Agent)

**ID:** `biomedical.genomics.st_agent`
**Version:** 1.0.0
**Status:** Candidate
**Category:** Genomics / Spatial Transcriptomics

---

## Overview

**STAgent** is a multimodal LLM-based autonomous agent designed for spatial transcriptomics (ST) data analysis. Unlike standard single-cell analysis, ST requires understanding both gene expression and histological (visual) context. STAgent integrates visual reasoning (H&E images) with code generation to perform tasks like identifying spatially variable genes (SVGs) and cell-cell communication analysis.

## Key Capabilities

- **Visual Reasoning:** Analyzes H&E images to identify tissue regions (tumor vs. stroma).
- **Tool Use:** Automates `Scanpy`, `Squidpy`, and `Giotto` workflows.
- **Reporting:** Generates publication-style reports with embedded plots.

## Reference
- *LiuLab-Bioelectronics-Harvard* (GitHub)


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->