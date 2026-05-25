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
name: 'antibody-design-agent'
description: 'An advanced agent for de novo antibody design and optimization using state-of-the-art protein language models (MAGE, RFdiffusion).'
measurable_outcome: Execute skill workflow successfully with valid output within 15 minutes.
allowed-tools:
  - read_file
  - run_shell_command
---


# Antibody Design Agent

This skill brings together cutting-edge tools for antibody engineering, including MAGE (Monoclonal Antibody Generator) and RFdiffusion for Antibodies. It enables the de novo design of antibodies against specific viral or tumoral targets.

## When to Use This Skill

*   **De Novo Design**: Generating antibody sequences/structures that bind to a specific antigen.
*   **Epitope Targeting**: Designing VHH or binders for a specific epitope on a target protein.
*   **Optimization**: Improving the affinity or stability of an existing antibody candidate.
*   **Viral Defense**: Rapidly generating antibodies against novel viral strains.

## Core Capabilities

1.  **MAGE (Monoclonal Antibody Generator)**: Uses a protein language model to generate diverse antibody sequences against unseen viral strains.
2.  **RFdiffusion for Antibodies**: Generates 3D antibody structures that bind to a target structure with high precision.
3.  **ProteinMPNN**: Optimizes the sequence of the generated structures for solubility and expression.

## Workflow

1.  **Target Definition**: Input the PDB structure or sequence of the antigen (target).
2.  **Design Phase**:
    *   Use **RFdiffusion** to generate the backbone of the binder (CDR loops).
    *   Use **ProteinMPNN** to design the sequence for the backbone.
    *   *Alternatively*, use **MAGE** to generate sequences directly from viral strain data.
3.  **Validation (In Silico)**: Use AlphaFold3 or ESMFold to predict the complex structure and assess binding confidence (pLDDT, PAE).
4.  **Selection**: Rank candidates for synthesis.

## Example Usage

**User**: "Design a VHH nanobody that binds to the RBD of the SARS-CoV-2 KP.2 variant."

**Agent Action**:
1.  Retrieves RBD structure for KP.2.
2.  Runs `RFdiffusion` with "binder" constraints on the RBD surface.
3.  Generates 100 backbone candidates.
4.  Sequences them with `ProteinMPNN`.
5.  Folds the complexes with `AlphaFold3` to verify binding interface.
6.  Returns top 5 sequences.


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->