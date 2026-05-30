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

# Image Analysis - Usage Guide

## Overview

This skill covers processing and analyzing tissue images from spatial transcriptomics data using Squidpy, including feature extraction, segmentation, and morphological analysis.

## Prerequisites

```bash
pip install squidpy scanpy scikit-image
# Optional for better segmentation:
pip install cellpose
```

## Quick Start

Tell your AI agent what you want to do:
- "Extract image features from my tissue image"
- "Segment cells in my Visium image"

## Example Prompts

### Feature Extraction
> "Calculate image features for each spot"

> "Extract texture features from the H&E image"

### Segmentation
> "Segment nuclei in my tissue image"

> "Run cell segmentation with Cellpose"

### Color Deconvolution
> "Separate hematoxylin and eosin stains"

## What the Agent Will Do

1. Load tissue image from spatial data
2. Process image (segmentation, feature extraction)
3. Store features in adata.obsm or adata.obs
4. Return summary of extracted features

## Tips

- **ImageContainer** - Use Squidpy's ImageContainer for organized handling
- **Scale factors** - Remember to account for image scaling
- **Spot size** - spot_scale parameter controls feature extraction area
- **Cellpose** - Provides better cell segmentation than watershed


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->