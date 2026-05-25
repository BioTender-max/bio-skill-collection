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

# MAGE: Monoclonal Antibody Generator

**ID:** `biomedical.drug_discovery.antibody_design`
**Version:** 1.1.0
**Status:** Integrated & Downloaded
**Category:** Drug Discovery / Antibody Design

---

## Overview

MAGE is a protein language model for generating monoclonal antibody sequences conditioned on an antigen. It accelerates early antibody discovery by proposing candidate variable regions for downstream validation.

---

## Inputs

| Field | Type | Notes |
|------|------|------|
| `antigen_sequence` | str | Amino acid sequence (FASTA or raw) |
| `num_candidates` | int | Number of sequences to generate |
| `output_dir` | str | Path to save FASTA outputs |

---

## Outputs

- FASTA files containing candidate antibody sequences
- Optional metadata (model checkpoint, seed, generation parameters)

---

## Quick Start

```bash
cd repo
python generate_antibodies.py --antigen_sequence "YOUR_ANTIGEN_SEQ" --output_dir ./results
```

---

## Guardrails

- Generated sequences require structural validation (AlphaFold, Rosetta).
- Do not claim binding or efficacy without wet-lab confirmation.
- Track model version and generation parameters for reproducibility.

---

## References

- https://github.com/IGlab-VUMC/MAGE_ab_generation



<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->