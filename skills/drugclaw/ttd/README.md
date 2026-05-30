# TTD

> **Subcategory**: `dti` &nbsp;|&nbsp; **Access mode**: `Local File`

**Purpose**: Therapeutic target database  

**Coverage**: Approved/clinical/experimental targets with drug linkages  

## Setup

1. Download the dataset from: <https://ttd.idrblab.cn/downloads/>
2. Set `csv_path` (or `tsv_path` / `json_path`) in config (see below).

## Configuration

| Key | Type / Description |
|-----|--------------------|
| `drug_target_tsv` | to TTD_drug_target.txt or P1-01-TTD_target_download.txt |

## Usage

```python
from drugclaw.skills.dti.ttd import TTDSkill

skill = TTDSkill(config={
    "drug_target_tsv": "...",  # to TTD_drug_target.txt or P1-01-TTD_target_download.txt
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

- Homepage: <https://ttd.idrblab.cn/downloads/>
