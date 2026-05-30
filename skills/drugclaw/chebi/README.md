# ChEBI

> **Subcategory**: `drug_ontology` &nbsp;|&nbsp; **Access mode**: `CLI (package-first)`

**Purpose**: Chemical entity ontology  

**Coverage**: Ontology of chemical entities with biological roles  

## Setup

Install the preferred CLI package:
```bash
pip install libchebipy
```
Falls back to REST API if the package is unavailable.

## Usage

```python
from drugclaw.skills.drug_ontology.chebi import ChEBISkill

skill = ChEBISkill(config={
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
