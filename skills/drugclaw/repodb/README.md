# RepoDB

> **Subcategory**: `drug_repurposing` &nbsp;|&nbsp; **Access mode**: `Dataset`

**Purpose**: Drug repositioning outcomes  

**Coverage**: Labelled drug-disease repositioning pairs from clinical trials  

## Setup

1. Download the dataset from: <https://unmtid-shinyapps.net/shiny/repodb/>
2. Set `csv_path` (or `tsv_path` / `json_path`) in config (see below).

## Usage

```python
from drugclaw.skills.drug_repurposing.repodb import RepoDBSkill

skill = RepoDBSkill(config={
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

- Homepage: <https://unmtid-shinyapps.net/shiny/repodb/>
