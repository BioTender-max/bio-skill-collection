# CADEC

> **Subcategory**: `drug_nlp` &nbsp;|&nbsp; **Access mode**: `Dataset`

**Purpose**: Clinical ADE corpus  

**Coverage**: CSIRO annotated drug side-effect corpus from social media  

## Setup

1. Download the dataset from: <https://data.csiro.au/collection/csiro:10948v3>
2. Set `csv_path` (or `tsv_path` / `json_path`) in config (see below).

## Configuration

| Key | Type / Description |
|-----|--------------------|
| `csv_path` | path to CADEC pre-parsed CSV |
| `tsv_path` | alternative TSV path |
| `delimiter` | column delimiter (default: auto-detect) |

## Usage

```python
from drugclaw.skills.drug_nlp.cadec import CADECSkill

skill = CADECSkill(config={
    "csv_path": "...",  # path to CADEC pre-parsed CSV
    "tsv_path": "...",  # alternative TSV path
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

- Homepage: <https://data.csiro.au/collection/csiro:10948v3>
