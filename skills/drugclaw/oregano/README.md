# OREGANO

> **Subcategory**: `drug_repurposing` &nbsp;|&nbsp; **Access mode**: `Local File`

**Purpose**: Drug repurposing candidates  

**Coverage**: Drug repurposing predictions with clinical evidence  

## Setup

1. Download the dataset from: <https://github.com/fusion-jena/OREGANO>
2. Set `csv_path` (or `tsv_path` / `json_path`) in config (see below).

## Configuration

| Key | Type / Description |
|-----|--------------------|
| `csv_path` | path to oregano_drug_disease.csv or equivalent TSV/CSV file |

## Usage

```python
from drugclaw.skills.drug_repurposing.oregano import OREGANOSkill

skill = OREGANOSkill(config={
    "csv_path": "...",  # path to oregano_drug_disease.csv or equivalent TSV/CSV file
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

- Homepage: <https://github.com/fusion-jena/OREGANO>
