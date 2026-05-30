# KEGG Drug

> **Subcategory**: `ddi` &nbsp;|&nbsp; **Access mode**: `CLI (package-first)`

**Purpose**: KEGG drug interactions  

**Coverage**: Drug-drug interactions from KEGG with pathway context  

## Setup

Install the preferred CLI package:
```bash
pip install bioservices
```
Falls back to REST API if the package is unavailable.

## Usage

```python
from drugclaw.skills.ddi.kegg_drug import KEGGDrugSkill

skill = KEGGDrugSkill(config={
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
