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
name: spatial-transcriptomics-analysis
description: Automated analysis pipeline for Spatial Transcriptomics (Visium, Xenium) integrating histology and gene expression.
keywords:
  - spatial-transcriptomics
  - visium
  - xenium
  - scanpy
  - squidpy
measurable_outcome: Process a Visium dataset, identify spatially variable genes, and generate spatial feature plots within 30 minutes.
license: MIT
metadata:
  author: MD BABU MIA, PhD
  version: "1.0.0"
compatibility:
  - system: python 3.9+
allowed-tools:
  - run_shell_command
  - read_file
  - write_file
---

# Spatial Transcriptomics Skill

**Version:** 1.0.0
**Author:** MD BABU MIA, PhD
**Date:** February 2026

## Overview
This skill provides automated analysis capabilities for Spatial Transcriptomics data, specifically designed for 10x Visium and Xenium platforms. It enables the integration of histological data with gene expression profiles to uncover spatial organization of cell types.

## Capabilities
1.  **Data Loading:** Supports Spaceranger output (h5, images).
2.  **QC & Preprocessing:** Spatial QC metrics, normalization.
3.  **Spatial Variable Features:** Identification of spatially variable genes (SVGs) using Moran's I and Geary's C.
4.  **Deconvolution:** Interface for cell type deconvolution (mapping scRNA-seq to spatial).
5.  **Visualization:** Interactive spatial plots overlaying gene expression on tissue images.

## Usage
```python
from Skills.Genomics.Spatial_Transcriptomics.spatial_analyzer import SpatialAnalyzer

# Initialize
sa = SpatialAnalyzer(data_path="./data/visium_sample1")

# Run Pipeline
sa.load_data()
sa.preprocess()
sa.find_spatial_features()
sa.plot_spatial("INS", save_path="./output/insulin_spatial.png")
```

## Requirements
*   scanpy
*   squidpy
*   anndata
*   matplotlib

<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->