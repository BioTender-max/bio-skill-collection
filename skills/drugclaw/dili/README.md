# DILI

> **Subcategory**: `drug_toxicity` &nbsp;|&nbsp; **Access mode**: `REST API`

**Purpose**: Drug-induced liver injury evidence  

**Coverage**: Live hepatotoxicity assay and safety-warning evidence from ChEMBL  

## Setup

Optional local example fixture file: `resources_metadata/drug_toxicity/DILI/dili.csv`

## Usage

```python
from drugclaw.skills.drug_toxicity.dili import DILISkill

skill = DILISkill(config={
    "timeout": 20,
})

if skill.is_available():
    results = skill.retrieve(
        entities={"drug": ["imatinib"]},
        query="hepatotoxicity",
        max_results=20,
    )
    for r in results:
        print(r.source_entity, r.relationship, r.target_entity)
```

## Output (`RetrievalResult`)

| Field | Description |
|-------|-------------|
| `source_entity` | Drug name |
| `target_entity` | Target / disease / ADE / partner |
| `relationship` | Relation type |
| `weight` | Confidence / score (0–1 or raw) |
| `evidence_text` | Human-readable summary |
| `sources` | Source IDs (PMID, DOI, etc.) |
| `metadata` | Extra fields specific to this skill |

## Data Source

- ChEMBL API: <https://www.ebi.ac.uk/chembl/api/data>
- Related paper: <https://doi.org/10.1021/acs.chemrestox.0c00296>
- Canonical packaged offline fixture (for `example.py`): `resources_metadata/drug_toxicity/DILI/dili.csv`
