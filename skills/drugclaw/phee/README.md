# PHEE

> **Subcategory**: `drug_nlp` &nbsp;|&nbsp; **Access mode**: `Dataset`

**Purpose**: Pharmacovigilance event corpus  

**Coverage**: Pharmacovigilance event extraction corpus (EMNLP 2022)  

## Setup

1. Download the dataset from: <https://github.com/ZhaoyueSun/PHEE>
2. Set `csv_path` (or `tsv_path` / `json_path`) in config (see below).

## Configuration

| Key | Type / Description |
|-----|--------------------|
| `json_path` | path to PHEE JSON or JSON-lines file |
| `tsv_path` | path to pre-processed TSV (drug, effect, event_type, sentence) |
| `delimiter` | column delimiter for TSV (default: tab) |
| `max_rows` | max rows to load (default: unlimited) |

## Usage

```python
from drugclaw.skills.drug_nlp.phee import PHEESkill

skill = PHEESkill(config={
    "json_path": "...",  # path to PHEE JSON or JSON-lines file
    "tsv_path": "...",  # path to pre-processed TSV (drug, effect, event_type, sentence)
    "delimiter": "...",  # column delimiter for TSV (default: tab)
    "max_rows": "...",  # max rows to load (default: unlimited)
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

- Homepage: <https://github.com/ZhaoyueSun/PHEE>
