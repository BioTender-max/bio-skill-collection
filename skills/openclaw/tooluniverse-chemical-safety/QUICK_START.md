# Chemical Safety & Toxicology - Quick Start

## Overview

This skill performs comprehensive chemical safety assessment using 25+ tools across 6 databases (ADMET-AI, CTD, FDA, DrugBank, STITCH, ChEMBL). It generates structured reports with evidence grading and risk classification.

---

## Quick Start Examples

### Example 1: Assess Safety of a Known Drug

**Query**: "Assess the toxicity profile of Acetaminophen"

**What happens**:
1. Resolves "Acetaminophen" to SMILES via PubChem (CID: 1983)
2. Runs 9 ADMET-AI predictions (toxicity, BBB, bioavailability, CYP, etc.)
3. Queries CTD for chemical-gene and chemical-disease associations
4. Extracts FDA label safety data (boxed warnings, contraindications, adverse reactions)
5. Retrieves DrugBank safety profile
6. Maps STITCH chemical-protein interactions
7. Checks ChEMBL structural alerts
8. Generates integrated risk assessment

**Output**: `Acetaminophen_safety_report.md` with risk classification and recommendations

---

### Example 2: Screen Novel Compound by SMILES

**Query**: "Predict toxicity for this compound: CC(=O)Oc1ccccc1C(=O)O"

**What happens**:
1. Detects SMILES input, resolves to PubChem CID (Aspirin, CID: 2244)
2. Runs full ADMET-AI toxicity + ADMET property prediction
3. Queries CTD, FDA, DrugBank for known safety data
4. Generates comparative predictive vs. known safety profile

---

### Example 3: Environmental Chemical Risk Assessment

**Query**: "What are the health risks of Bisphenol A?"

**What happens**:
1. Resolves "Bisphenol A" via PubChem
2. Runs ADMET-AI predictions
3. Queries CTD extensively (BPA has rich toxicogenomics data)
4. FDA/DrugBank phases skipped (not an approved drug)
5. Maps STITCH interactions (endocrine disruption targets)
6. Generates environmental health risk report

---

### Example 4: Batch Toxicity Screening

**Query**: "Compare the toxicity profiles of ibuprofen, naproxen, and celecoxib"

**What happens**:
1. Resolves all three names to SMILES
2. Runs ADMET-AI batch predictions
3. Creates comparative toxicity table
4. Queries safety data for each compound
5. Generates comparative risk assessment

---

## Python SDK Usage

```python
from tooluniverse import ToolUniverse

tu = ToolUniverse()
tu.load_tools()

# Phase 0: Resolve compound
cid_result = tu.tools.PubChem_get_CID_by_compound_name(name="Acetaminophen")
cid = cid_result['data']['IdentifierList']['CID'][0]  # 1983

props = tu.tools.PubChem_get_compound_properties_by_CID(cid=cid)
smiles = props['data']['PropertyTable']['Properties'][0]['CanonicalSMILES']

# Phase 1: Toxicity predictions
tox = tu.tools.ADMETAI_predict_toxicity(smiles=[smiles])
print("Toxicity:", tox)

# Phase 2: ADMET
bbb = tu.tools.ADMETAI_predict_BBB_penetrance(smiles=[smiles])
cyp = tu.tools.ADMETAI_predict_CYP_interactions(smiles=[smiles])
print("BBB:", bbb)
print("CYP:", cyp)

# Phase 3: Toxicogenomics
gene_interactions = tu.tools.CTD_get_chemical_gene_interactions(input_terms="Acetaminophen")
disease_assoc = tu.tools.CTD_get_chemical_diseases(input_terms="Acetaminophen")

# Phase 4: FDA Safety
boxed = tu.tools.FDA_get_boxed_warning_info_by_drug_name(drug_name="Acetaminophen")
adverse = tu.tools.FDA_get_adverse_reactions_by_drug_name(drug_name="Acetaminophen")

# Phase 5: DrugBank Safety
safety = tu.tools.drugbank_get_safety_by_drug_name_or_drugbank_id(
    query="Acetaminophen", case_sensitive=False, exact_match=False, limit=5
)
```

---

## MCP Integration

When used via MCP (Claude Desktop, Cursor, etc.), simply ask:

- "Assess the toxicity of metformin"
- "Is caffeine safe? Generate a comprehensive safety report"
- "Predict ADMET properties for SMILES: c1ccc(cc1)O"
- "What genes does arsenic interact with?"
- "Compare safety profiles of aspirin and ibuprofen"

The skill will automatically invoke the appropriate tools and generate a report.

---

## Key Tool Reference

| Tool | Input | What It Returns |
|------|-------|-----------------|
| `ADMETAI_predict_toxicity` | SMILES list | AMES, DILI, LD50, hERG, carcinogenicity predictions |
| `ADMETAI_predict_BBB_penetrance` | SMILES list | BBB crossing probability |
| `ADMETAI_predict_CYP_interactions` | SMILES list | CYP1A2/2C9/2C19/2D6/3A4 inhibition/substrate |
| `CTD_get_chemical_gene_interactions` | Chemical name | Gene interaction list with types |
| `CTD_get_chemical_diseases` | Chemical name | Disease association list |
| `FDA_get_boxed_warning_info_by_drug_name` | Drug name | Black box warnings |
| `FDA_get_adverse_reactions_by_drug_name` | Drug name | Known adverse reactions |
| `drugbank_get_safety_by_drug_name_or_drugbank_id` | Query + flags | Toxicity, contraindications |
| `STITCH_get_chemical_protein_interactions` | STITCH IDs | Chemical-protein interaction network |
| `ChEMBL_search_compound_structural_alerts` | ChEMBL ID | Structural toxicity flags |

---

## Evidence Tiers

| Tier | Meaning | Source Examples |
|------|---------|----------------|
| [T1] | Direct human/regulatory evidence | FDA labels, clinical trial data |
| [T2] | Animal studies, curated databases | CTD curated, DrugBank, nonclinical toxicology |
| [T3] | Computational prediction, association | ADMET-AI, CTD inferred, STITCH scores |
| [T4] | Database annotation, text-mined | Literature mentions, unvalidated predictions |
