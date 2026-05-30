# DDInter

> **Subcategory**: `ddi` &nbsp;|&nbsp; **Access mode**: `REST API`

**Purpose**: DDI interaction database  

**Coverage**: Comprehensive DDI database with clinical evidence  

## Usage

```python
from drugclaw.skills.ddi.ddinter import DDInterSkill

skill = DDInterSkill(config={
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

- Homepage: <https://ddinter2.scbdd.com/>
