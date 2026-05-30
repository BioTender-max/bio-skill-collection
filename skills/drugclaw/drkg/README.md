# DRKG

> **Subcategory**: `drug_repurposing` &nbsp;|&nbsp; **Access mode**: `Local File`

**Purpose**: Drug repurposing KG  

**Coverage**: Multi-relational KG integrating DrugBank, Hetionet, STRING, etc.  

## Setup

1. Download the dataset from: <https://github.com/gnn4dr/DRKG>
2. Set `csv_path` (or `tsv_path` / `json_path`) in config (see below).

## Configuration

| Key | Type / Description |
|-----|--------------------|
| `drkg_tsv` | absolute path to drkg.tsv |

## Usage

```python
from drugclaw.skills.drug_repurposing.drkg import DRKGSkill

skill = DRKGSkill(config={
    "drkg_tsv": "...",  # absolute path to drkg.tsv
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

- Homepage: <https://github.com/gnn4dr/DRKG>
