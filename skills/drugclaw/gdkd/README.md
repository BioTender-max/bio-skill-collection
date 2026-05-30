# GDKD

> **Subcategory**: `dti` &nbsp;|&nbsp; **Access mode**: `Local File`

**Purpose**: Genomics-drug knowledge  

**Coverage**: Genomics-Drug Knowledge Database from Synapse  

## Setup

1. Canonical packaged file: `resources_metadata/dti/GDKD/gdkd.csv`
2. Optional override: set `csv_path` in config.

## Usage

```python
from drugclaw.skills.dti.gdkd import GDKDSkill

skill = GDKDSkill(config={
    "csv_path": "/data/boom/Agent/DrugClaw/resources_metadata/dti/GDKD/gdkd.csv",
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

- Homepage: <https://www.synapse.org/#!Synapse:syn2370773>
