# TAC 2017 ADR

> **Subcategory**: `drug_nlp` &nbsp;|&nbsp; **Access mode**: `Dataset`

**Purpose**: TAC ADR extraction corpus  

**Coverage**: TAC 2017 adverse drug reaction extraction from FDA drug labels  

## Setup

1. Download the dataset from: <https://bionlp.nlm.nih.gov/tac2017adversereactions/>
2. Set `csv_path` (or `tsv_path` / `json_path`) in config (see below).

## Configuration

| Key | Type / Description |
|-----|--------------------|
| `tsv_path` | path to pre-processed TSV/CSV (drug, ade, section, label_id) |
| `json_path` | path to JSON-lines file with {drug, ade, section, pmid} dicts |
| `delimiter` | column delimiter for TSV (default: tab) |
| `max_rows` | max rows to load (default: unlimited) |

## Usage

```python
from drugclaw.skills.drug_nlp.tac2017 import TAC2017ADRSkill

skill = TAC2017ADRSkill(config={
    "tsv_path": "...",  # path to pre-processed TSV/CSV (drug, ade, section, label_id)
    "json_path": "...",  # path to JSON-lines file with {drug, ade, section, pmid} dicts
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

- Homepage: <https://bionlp.nlm.nih.gov/tac2017adversereactions/>
