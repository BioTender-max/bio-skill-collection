# MedlinePlus Drug Info

> **Subcategory**: `drug_labeling` &nbsp;|&nbsp; **Access mode**: `REST API`

**Purpose**: Patient drug information  

**Coverage**: NIH MedlinePlus drug information for patients and clinicians  

## Usage

```python
from drugclaw.skills.drug_labeling.medlineplus import MedlinePlusSkill

skill = MedlinePlusSkill(config={
})

if skill.is_available():
    results = skill.retrieve(
        entities={"drug": ["aspirin", "ibuprofen"]},
        query="patient drug information",
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
