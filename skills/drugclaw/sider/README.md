# SIDER

> **Subcategory**: `adr` &nbsp;|&nbsp; **Access mode**: `Local File`

**Purpose**: Side effect resource  

**Coverage**: Drug–side-effect associations from package inserts  

## Setup

1. Download the dataset from: <http://sideeffects.embl.de/>
2. Set `csv_path` (or `tsv_path` / `json_path`) in config (see below).

## Configuration

| Key | Type / Description |
|-----|--------------------|
| `se_tsv` | path to meddra_all_se.tsv |
| `name_to_stitch` | {drug_name_lower: stitch_id} mapping (optional) |

## Usage

```python
from drugclaw.skills.adr.sider import SIDERSkill

skill = SIDERSkill(config={
    "se_tsv": "...",  # path to meddra_all_se.tsv
    "name_to_stitch": "...",  # {drug_name_lower: stitch_id} mapping (optional)
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

- Homepage: <http://sideeffects.embl.de/>
