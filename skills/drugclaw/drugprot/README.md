# DrugProt

> **Subcategory**: `drug_nlp` &nbsp;|&nbsp; **Access mode**: `Dataset`

**Purpose**: Drug-protein relation corpus  

**Coverage**: BioCreative VII drug-protein relation extraction corpus  

## Setup

1. Download the dataset from: <https://zenodo.org/record/5119892>
2. Set `csv_path` (or `tsv_path` / `json_path`) in config (see below).

## Configuration

| Key | Type / Description |
|-----|--------------------|
| `tsv_path` | path to DrugProt entities+relations TSV or combined file |
| `delimiter` | column delimiter (default: "   ") |

## Usage

```python
from drugclaw.skills.drug_nlp.drugprot import DrugProtSkill

skill = DrugProtSkill(config={
    "tsv_path": "...",  # path to DrugProt entities+relations TSV or combined file
    "delimiter": "...",  # column delimiter (default: "   ")
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

- Homepage: <https://zenodo.org/record/5119892>
