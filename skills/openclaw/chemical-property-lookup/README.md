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

# Chemical Property Lookup

**ID:** `biomedical.drug_discovery.chemical_properties`
**Version:** 1.1.0
**Status:** Production
**Category:** Drug Discovery / Cheminformatics

---

## Overview

The **Chemical Property Lookup Skill** provides RDKit-based property calculations for SMILES inputs. It is a foundational utility for drug discovery workflows and validation steps.

---

## Inputs

| Field | Type | Notes |
|------|------|------|
| `smiles` | str | Canonical or valid SMILES string |

---

## Outputs

- Molecular weight, cLogP, TPSA
- HBD/HBA counts
- QED score
- Lipinski summary

### Example Summary Output

```json
{
  "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
  "molecular_weight": 180.16,
  "logp": 1.19,
  "tpsa": 63.6,
  "hbd": 1,
  "hba": 4,
  "qed": 0.62,
  "lipinski": {"pass": true, "violations": []}
}
```

---

## Core Functions

| Function | Output | Use |
|----------|--------|-----|
| `calculate_molecular_weight` | float | Lipinski, dosing heuristics |
| `calculate_logp` | float | Solubility / permeability |
| `calculate_tpsa` | float | Oral absorption / BBB |
| `count_hbd_hba` | dict | Hydrogen bonding checks |
| `calculate_qed` | float | Drug-likeness score |
| `check_lipinski` | dict | Pass/fail + violations |
| `summarize_properties` | dict | All properties in one call |

---

## Usage (Python)

```python
from molecular_tools import summarize_properties

aspirin = "CC(=O)OC1=CC=CC=C1C(=O)O"
summary = summarize_properties(aspirin)
print(summary)
```

---

## Guardrails

- Reject invalid SMILES with clear error messages.
- Do not infer stereochemistry if not provided.
- Log invalid inputs for manual review.

---

## Dependencies

```
rdkit>=2023.03
```

---

## Integration Notes

This skill is commonly used by:
- **AgentD Drug Discovery** for property filtering
- **ADMET pipelines** for input validation



<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->