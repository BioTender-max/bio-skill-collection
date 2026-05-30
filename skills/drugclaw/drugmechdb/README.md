# DRUGMECHDB

> **Subcategory**: `drug_mechanism` &nbsp;|&nbsp; **Access mode**: `REST API`

**Purpose**: Drug mechanism-of-action paths  

**Coverage**: Curated MoA paths linking drugs to diseases via biological graphs  

## Configuration

| Key | Type / Description |
|-----|--------------------|
| `local_path` | optional path to indication_paths.json |
| `fetch_remote` | download from GitHub if local_path missing (default True) |

## Usage

```python
from drugclaw.skills.drug_mechanism.drugmechdb import DrugMechDBSkill

skill = DrugMechDBSkill(config={
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

- Homepage: <https://github.com/SuLab/DrugMechDB>
