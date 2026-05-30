# RepurposeDrugs

> **Subcategory**: `drug_repurposing` &nbsp;|&nbsp; **Access mode**: `Local File`

**Purpose**: Repurposing portal  

**Coverage**: Open drug repurposing portal with disease-drug associations  

## Setup

1. Canonical packaged file: `resources_metadata/drug_repurposing/RepurposeDrugs/repurposedrugs.csv`
2. Set `csv_path` in config (or use resolver defaults).

## Configuration

| Key | Type / Description |
|-----|--------------------|
| `csv_path` | path to RepurposeDrugs CSV/TSV export |
| `delimiter` | column delimiter (default: auto-detect from extension) |

## Usage

```python
from drugclaw.skills.drug_repurposing.repurposedrugs import RepurposeDrugsSkill

skill = RepurposeDrugsSkill(config={
    "csv_path": "/data/boom/Agent/DrugClaw/resources_metadata/drug_repurposing/RepurposeDrugs/repurposedrugs.csv",
    "delimiter": "...",  # column delimiter (default: auto-detect from extension)
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

- Homepage: <https://repurposedrugs.org/>
