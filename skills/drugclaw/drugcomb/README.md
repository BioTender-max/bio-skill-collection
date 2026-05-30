# DrugComb

> **Subcategory**: `drug_combination` &nbsp;|&nbsp; **Access mode**: `Local File`

**Purpose**: Drug combination screening  

**Coverage**: Drug combination screening data across cancer cell lines  

## Setup

1. Canonical packaged file: `resources_metadata/drug_combination/DrugComb/drugcomb.csv`
2. Set `csv_path` in config (or use resolver defaults).

## Configuration

| Key | Type / Description |
|-----|--------------------|
| `csv_path` | path to DrugComb summary CSV |
| `delimiter` | column delimiter (default: auto-detect) |

## Usage

```python
from drugclaw.skills.drug_combination.drugcomb import DrugCombSkill

skill = DrugCombSkill(config={
    "csv_path": "/data/boom/Agent/DrugClaw/resources_metadata/drug_combination/DrugComb/drugcomb.csv",
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

- Homepage: <https://drugcomb.fimm.fi/>
