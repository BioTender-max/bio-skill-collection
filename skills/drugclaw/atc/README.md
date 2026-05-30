# ATC/DDD

> **Subcategory**: `drug_ontology` &nbsp;|&nbsp; **Access mode**: `REST API`

**Purpose**: WHO drug classification  

**Coverage**: ATC classification + daily doses  

## Usage

```python
from drugclaw.skills.drug_ontology.atc import ATCSkill

skill = ATCSkill(config={
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

## Data Source

- Homepage: <https://atcddd.fhi.no/atc_ddd_index/>
