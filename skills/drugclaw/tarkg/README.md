# TarKG

> **Subcategory**: `dti` &nbsp;|&nbsp; **Access mode**: `Local File`

**Purpose**: Target knowledge graph  

**Coverage**: Drug-target KG linking targets to diseases via pathways  

## Setup

1. Canonical packaged file: `resources_metadata/dti/TarKG/tarkg.tsv`
2. Set `tsv_path` in config (or use resolver defaults).

## Usage

```python
from drugclaw.skills.dti.tarkg import TarKGSkill

skill = TarKGSkill(config={
    "tsv_path": "/data/boom/Agent/DrugClaw/resources_metadata/dti/TarKG/tarkg.tsv",
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

- Homepage: <https://tarkg.ddtmlab.org/>
