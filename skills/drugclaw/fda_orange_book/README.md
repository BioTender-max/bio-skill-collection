# FDA Orange Book

> **Subcategory**: `drug_knowledgebase` &nbsp;|&nbsp; **Access mode**: `REST API`

**Purpose**: Approved drug products  

**Coverage**: FDA-approved drugs with bioequivalence and patent info  

## Usage

```python
from drugclaw.skills.drug_knowledgebase.fda_orange_book import FDAOrangeBookSkill

skill = FDAOrangeBookSkill(config={
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

- Homepage: <https://www.accessdata.fda.gov/scripts/cder/ob/>
