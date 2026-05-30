# PsyTAR

> **Subcategory**: `drug_nlp` &nbsp;|&nbsp; **Access mode**: `Dataset`

**Purpose**: Psychiatric drug ADE corpus  

**Coverage**: Annotated psychiatric drug adverse events from patient forums  

## Setup

1. Download the dataset from: <https://www.askapatient.com (derived) / Zenodo>
2. Set `csv_path` (or `tsv_path` / `json_path`) in config (see below).

## Configuration

| Key | Type / Description |
|-----|--------------------|
| `csv_path` | path to PsyTAR CSV file |
| `delimiter` | column delimiter (default: ",") |

## Usage

```python
from drugclaw.skills.drug_nlp.psytar import PsyTARSkill

skill = PsyTARSkill(config={
    "csv_path": "...",  # path to PsyTAR CSV file
    "delimiter": "...",  # column delimiter (default: ",")
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

- Homepage: <https://www.askapatient.com (derived) / Zenodo>
