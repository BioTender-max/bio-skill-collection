# WHO Essential Medicines List

> **Subcategory**: `drug_knowledgebase` &nbsp;|&nbsp; **Access mode**: `Local File`

**Purpose**: Essential medicines  

**Coverage**: WHO list of essential medicines with therapeutic category  

## Setup

1. Prepare a structured CSV export of the WHO Essential Medicines List.
2. Prefer a locally mirrored file under `resources_metadata/drug_knowledgebase/WHO_EML/`.
3. Set `csv_path` in config (see below).

## Usage

```python
from drugclaw.skills.drug_knowledgebase.who_eml import WHOEssentialMedicinesSkill

skill = WHOEssentialMedicinesSkill(config={
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

## Data Source

- Homepage: <https://www.who.int/publications/i/item/WHO-MHP-HPS-EML-2023.02>
- Verified runtime note: the publication landing page is reachable, but the old community CSV URL and the old PDF URL used by earlier examples are stale. This runtime skill should be treated as local-file-only unless a maintained CSV mirror is provided.
