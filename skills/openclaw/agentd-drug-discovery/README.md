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

# AgentD: Drug Discovery Agent

**ID:** `biomedical.drug_discovery.agentd`
**Version:** 1.1.0
**Status:** Production
**Category:** Drug Discovery / Cheminformatics

---

## Overview

**AgentD** accelerates early-stage drug discovery by combining literature mining, molecule generation, and property prediction. It is designed to produce **testable hypotheses** and **ranked candidate lists**, not final clinical decisions.

---

## Inputs

| Field | Type | Notes |
|------|------|------|
| `target_protein` | str | Gene symbol or UniProt ID |
| `reference_compound` | str | Optional SMILES scaffold |
| `indication` | str | Disease context for constraints |
| `constraints` | dict | Property limits (LogP, MW, TPSA, etc.) |
| `num_candidates` | int | Number of molecules to return |

---

## Outputs

- Ranked candidate table with SMILES and predicted properties
- SAR rationale for each candidate
- ADMET and toxicity flags
- Reproducibility manifest (data source versions, model checkpoints)

### Output Schema (Recommended)

```json
{
  "candidate_id": "EGFR_01",
  "smiles": "COc1cc...",
  "scores": {"logp": 2.8, "mw": 432, "qed": 0.71, "dock": -9.2},
  "novelty": 0.78,
  "alerts": ["PAINS risk"],
  "rationale": "Retained quinazoline core, reduced LogP"
}
```

---

## Workflow

1. **Evidence retrieval** - extract known ligands, SAR trends, and liabilities.
2. **Candidate generation** - scaffold hopping or fragment growth.
3. **Property filtering** - apply Lipinski, QED, and ADMET heuristics.
4. **Docking setup** - optional preparation for Vina/Glide workflows.
5. **Ranking** - combine efficacy, developability, and novelty.
6. **Reporting** - produce a ranked, annotated candidate list.

---

## Guardrails

- Always label outputs as **in silico** hypotheses.
- Never claim clinical efficacy or safety.
- Flag PAINS motifs and reactive groups when detected.
- Track data source versions for auditability.

---

## Dependencies

```
rdkit>=2023.03
requests>=2.28
pandas>=1.5
numpy>=1.24
torch>=2.0
```

---

## References

- AgentD: https://github.com/hoon-ock/AgentD
- ChemCrow, DrugAgent, REINVENT
- Bickerton et al. (2012) QED

---

## Author

**MD BABU MIA**
*Artificial Intelligence Group*
*Icahn School of Medicine at Mount Sinai*
md.babu.mia@mssm.edu


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->