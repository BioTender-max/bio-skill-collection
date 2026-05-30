# DDI Corpus 2013

> **Subcategory**: `drug_nlp` &nbsp;|&nbsp; **Access mode**: `Dataset`

**Purpose**: DDI extraction corpus  

**Coverage**: Annotated DDI extraction corpus from drug labels/MEDLINE  

## Setup

1. Download the dataset from: <https://github.com/isegura/DDICorpus>
2. Set `csv_path` (or `tsv_path` / `json_path`) in config (see below).

## Configuration

| Key | Type / Description |
|-----|--------------------|
| `tsv_path` | path to pre-parsed TSV (columns: drug1, drug2, ddi_type, sentence) |
| `csv_path` | alternative CSV path |
| `delimiter` | column delimiter (default: "   " for TSV, "," for CSV) |

## Usage

```python
from drugclaw.skills.drug_nlp.ddi_corpus import DDICorpusSkill

skill = DDICorpusSkill(config={
    "tsv_path": "...",  # path to pre-parsed TSV (columns: drug1, drug2, ddi_type, sentence)
    "csv_path": "...",  # alternative CSV path
    "delimiter": "...",  # column delimiter (default: "   " for TSV, "," for CSV)
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

- Homepage: <https://github.com/isegura/DDICorpus>
