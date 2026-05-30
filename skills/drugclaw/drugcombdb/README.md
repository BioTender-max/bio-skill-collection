# DrugCombDB

> **Subcategory**: `drug_combination` &nbsp;|&nbsp; **Access mode**: `Local File`

**Purpose**: Drug combination database  

**Coverage**: Human/animal drug combination synergy/antagonism records  

## Setup

1. Canonical packaged file: `resources_metadata/drug_combination/DrugCombDB/drugcombdb.csv`
2. Set `csv_path` in config (or use resolver defaults).

## Configuration

| Key | Type / Description |
|-----|--------------------|
| `csv_path` | path to DrugCombDB CSV file |
| `delimiter` | column delimiter (default: auto-detect) |

## Usage

```python
from drugclaw.skills.drug_combination.drugcombdb import DrugCombDBSkill

skill = DrugCombDBSkill(config={
    "csv_path": "/data/boom/Agent/DrugClaw/resources_metadata/drug_combination/DrugCombDB/drugcombdb.csv",
    "delimiter": "...",  # column delimiter (default: auto-detect)
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

- Homepage: <http://drugcombdb.idrblab.net/main/>
