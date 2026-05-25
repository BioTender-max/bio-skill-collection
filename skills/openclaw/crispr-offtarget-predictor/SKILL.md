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
name: 'crispr-offtarget-predictor'
description: 'Predicts potential off-target sites for a given sgRNA sequence using mismatch analysis.'
measurable_outcome: Execute skill workflow successfully with valid output within 15 minutes.
allowed-tools:
  - read_file
  - run_shell_command
---


# CRISPR Off-Target Predictor

This skill identifies potential off-target binding sites for a specific sgRNA sequence. It helps researchers assess the specificity of their CRISPR design.

## When to Use This Skill

*   Designing new CRISPR experiments.
*   Validating sgRNA specificity before synthesis.
*   Analyzing potential safety risks in gene editing protocols.

## Core Capabilities

1.  **Mismatch Scoring**: Calculates mismatch penalties for potential sites.
2.  **PAM Validation**: Filters targets based on PAM (Protospacer Adjacent Motif) compatibility.
3.  **Risk Assessment**: Categorizes off-targets as Low, Medium, or High risk.

## Workflow

1.  **Input**: sgRNA sequence (20nt) and PAM (e.g., NGG).
2.  **Analysis**: Scans a reference library (mocked for this version) for similar sequences.
3.  **Output**: List of potential off-targets with locations and risk scores.

## Example Usage

**User**: "Check sgRNA 'GAGTCCGAGCAGAAGAAGAA' for off-targets."

**Agent Action**:
```bash
python3 Skills/Genomics/CRISPR_Prediction/impl.py --sequence GAGTCCGAGCAGAAGAAGAA --pam NGG
```


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->