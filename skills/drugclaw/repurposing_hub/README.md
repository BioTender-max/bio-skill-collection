# Drug Repurposing Hub

> **Subcategory**: `drug_repurposing` &nbsp;|&nbsp; **Access mode**: `Local File`

**Coverage**: Broad-spectrum repurposing library with mechanism annotations  

## Setup

## Usage

```python
from drugclaw.skills.drug_repurposing.repurposing_hub import RepurposingHubSkill

skill = RepurposingHubSkill(config={
    "csv_path": "/path/to/data.csv",
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
