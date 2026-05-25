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
name: compbioagent-explorer
description: scRNA-seq Explorer
keywords:
  - single-cell
  - visualization
  - web-app
  - cellxgene
  - exploration
measurable_outcome: Launch a local web instance for interactive scRNA-seq exploration and generate 3+ custom visualizations per session.
license: MIT
metadata:
  author: CompBioAgent Team
  version: "1.0.0"
compatibility:
  - system: Python 3.9+
allowed-tools:
  - run_shell_command
  - web_fetch
---

# CompBioAgent (Single-Cell Explorer)

An LLM-powered web application for single-cell RNA-seq data exploration, integrating with CellDepot and Cellxgene VIP.

## When to Use

*   **Interactive Exploration**: When you need to visually explore a dataset without writing code.
*   **Hypothesis Generation**: Quickly checking expression of specific markers across clusters.
*   **Sharing**: Presenting data to non-computational collaborators.

## Core Capabilities

1.  **Natural Language Querying**: "Show me the expression of TP53 in the B-cell cluster."
2.  **Cellxgene Integration**: Leverages robust visualization tools.
3.  **Data Integration**: Connects with CellDepot for dataset retrieval.

## Workflow

1.  **Setup**: `pip install compbioagent`.
2.  **Launch**: `compbioagent start --data ./data.h5ad`.
3.  **Interact**: Open the local URL (e.g., http://localhost:8050) and chat with the agent to generate plots.

## Example Usage

**User**: "Launch the explorer for my kidney dataset."

**Agent Action**:
```bash
compbioagent launch --port 8080 --data ./kidney_atlas.h5ad
```


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->