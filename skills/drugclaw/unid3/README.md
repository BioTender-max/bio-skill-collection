# UniD3

> **Subcategory**: `drug_knowledgebase` &nbsp;|&nbsp; **Access mode**: `Local File`

**Purpose**: Drug discovery knowledge graph  

**Coverage**: Multi-KG + drug-disease datasets from 150 000+ PubMed articles  

## Setup

1. Download the dataset from: <https://github.com/QSong-github/UniD3>
2. Set `csv_path` (or `tsv_path` / `json_path`) in config (see below).

## Configuration

| Key | Type / Description |
|-----|--------------------|
| `graphml_paths` | {graph_name: path_to_graphml_file} |

## Usage

```python
from drugclaw.skills.drug_knowledgebase.unid3 import UniD3Skill

skill = UniD3Skill(config={
    "graphml_paths": "...",  # {graph_name: path_to_graphml_file}
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

- Homepage: <https://github.com/QSong-github/UniD3>
