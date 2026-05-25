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
name: 'variant-interpretation-acmg'
description: 'Classifies genetic variants according to ACMG (American College of Medical Genetics) guidelines.'
measurable_outcome: Execute skill workflow successfully with valid output within 15 minutes.
allowed-tools:
  - read_file
  - run_shell_command
---


# Variant Interpretation (ACMG)

The **Variant Interpretation Skill** automates the classification of genetic variants (Pathogenic, Benign, VUS) using a rules-based engine derived from ACMG guidelines.

## When to Use This Skill

*   When analyzing a VCF file for clinical reporting.
*   To determine the clinical significance of a specific mutation (e.g., BRCA1 c.123A>G).
*   To aggregate evidence (population freq, computational predictions) into a final verdict.

## Core Capabilities

1.  **Rule Scoring**: Applies codes like PVS1 (Null variant), PM2 (Rare), PP3 (In silico).
2.  **Classification**: Combines scores to reach a verdict (Pathogenic, Likely Pathogenic, VUS, etc.).
3.  **Explanation**: Provides the logic/evidence used for the classification.

## Workflow

1.  **Input**: Variant details (Gene, HGVS, Consequence) or Evidence codes directly.
2.  **Process**: Sums weights of applied ACMG criteria.
3.  **Output**: Final classification and score breakdown.

## Example Usage

**User**: "Classify a variant with evidence PVS1 and PM2."

**Agent Action**:
```bash
python3 Skills/Genomics/Variant_Interpretation/acmg_classifier.py \
    --evidence "PVS1,PM2"
```



<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->