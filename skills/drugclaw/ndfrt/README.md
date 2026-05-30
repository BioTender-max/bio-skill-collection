# NDF-RT

> **Subcategory**: `drug_ontology` &nbsp;|&nbsp; **Access mode**: `REST API`

**Purpose**: National drug file taxonomy  

**Coverage**: VA National Drug File ontology of drug classes and roles  

## Usage

```python
from drugclaw.skills.drug_ontology.ndfrt import NDFRTSkill

skill = NDFRTSkill(config={
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

- Homepage: <https://evsexplore.semantics.cancer.gov/evsexplore/welcome?terminology=ndfrt>
