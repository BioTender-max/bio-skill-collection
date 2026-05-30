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

# Spatial Multi-omics Analysis - Usage Guide

## Overview

Analyze high-resolution spatial transcriptomics from Slide-seq, Stereo-seq, Visium HD, and similar platforms.

## Prerequisites

```bash
pip install squidpy spatialdata scanpy
```

## Quick Start

- "Analyze my Slide-seq data"
- "Process Stereo-seq at bin level"
- "Work with Visium HD subcellular data"

## Example Prompts

### Data Loading

> "Load my Stereo-seq data into SpatialData"

> "Convert Slide-seq puck to AnnData"

### Spatial Analysis

> "Find spatially variable genes in my Visium HD data"

> "Bin my high-resolution spots for neighborhood analysis"

### Multi-modal

> "Integrate spatial transcriptomics with H&E morphology"

> "Combine transcript locations with cell segmentation"

## What the Agent Will Do

1. Load high-resolution spatial data
2. Bin or aggregate spots if needed
3. Compute spatial neighbors
4. Run spatial statistics
5. Integrate with morphology if available

## Tips

- **Binning** - Aggregate for computational efficiency on dense data
- **SpatialData** - Modern framework for multi-modal spatial
- **Squidpy** - Best for spatial statistics and visualization
- **Memory** - High-res data can be large; use chunked processing
- **Coordinate systems** - Check units (pixels vs microns)


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->