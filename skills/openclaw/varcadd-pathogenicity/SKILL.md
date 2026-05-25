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
name: varcadd-pathogenicity
description: Variant Scorer
keywords:
  - variant-interpretation
  - CADD
  - pathogenicity
  - genomics
  - prediction
measurable_outcome: Return pathogenicity scores for a VCF of 1000 variants within 2 minutes, flagging top 1% deleterious hits.
license: Non-Commercial
metadata:
  author: Genome Medicine 2025
  version: "1.0.0"
compatibility:
  - system: Python 3.9+
allowed-tools:
  - run_shell_command
  - read_file
---

# varCADD (Variant Pathogenicity Predictor)

Genome-wide pathogenicity prediction leveraging standing variation data to improve accuracy over traditional CADD scores.

## When to Use

*   **Variant Prioritization**: Ranking candidate variants in rare disease cases.
*   **VUS Interpretation**: Assessing variants of uncertain significance.
*   **Research**: Annotating novel variants in population studies.

## Core Capabilities

1.  **Score Generation**: Calculate C-scores for SNVs and indels.
2.  **Annotation**: Add functional context (conservation, protein domains).
3.  **Filtering**: Identify likely pathogenic variants based on thresholds.

## Workflow

1.  **Input**: VCF file.
2.  **Annotate**: Run varCADD model.
3.  **Filter**: Keep variants with Score > X.
4.  **Output**: Annotated VCF or ranked table.

## Example Usage

**User**: "Score these variants from patient X."

**Agent Action**:
```bash
varcadd score --input patient.vcf --output scored.vcf
```


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->