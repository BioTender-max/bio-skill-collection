# DGIdb

> **Subcategory**: `dti` &nbsp;|&nbsp; **Access mode**: `REST API`

**Purpose**: Drug–gene interactions  

**Coverage**: Curated drug–gene interaction database (NCI, ClinVar, etc.)  

## Usage

```python
from drugclaw.skills.dti.dgidb import DGIdbSkill

skill = DGIdbSkill(config={
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
