# CPIC

> **Subcategory**: `drug_knowledgebase` &nbsp;|&nbsp; **Access mode**: `REST API`

**Purpose**: Clinical pharmacogenomics  

**Coverage**: CPIC guidelines linking genes/variants to drug dosing  

## Usage

```python
from drugclaw.skills.drug_knowledgebase.cpic import CPICSkill

skill = CPICSkill(config={
})

if skill.is_available():
    results = skill.retrieve(
        entities={"drug": ["imatinib"]},
        query="mechanism",
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
