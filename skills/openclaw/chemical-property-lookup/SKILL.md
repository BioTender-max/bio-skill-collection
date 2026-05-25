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
name: chemical-property-lookup
description: Compute RDKit-driven molecular properties (MW, logP, TPSA, QED, Lipinski) for a SMILES string to support downstream drug discovery tools.
allowed-tools:
  - read_file
  - run_shell_command
---

## At-a-Glance
- **description (10-20 chars):** RDKit stats
- **keywords:** SMILES, RDKit, Lipinski, QED, ADMET
- **measurable_outcome:** Return a validated property summary (JSON + Lipinski verdict) for each SMILES within 60 seconds of request.

## Workflow
1. Validate SMILES input; raise explicit errors for invalid syntax.
2. Call helpers from `molecular_tools.py` (`summarize_properties`, `check_lipinski`, etc.).
3. Report MW, logP, TPSA, HBD/HBA, QED, and Lipinski pass/fail with violations.
4. Surface any calculation warnings (e.g., aromaticity perception issues).

## Guardrails
- Never infer stereochemistry; report as "not provided".
- Log invalid SMILES for manual follow-up.
- Communicate that results are screening heuristics, not definitive ADMET outcomes.

## References
- `README.md` plus `molecular_tools.py` for function signatures and dependencies.


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->