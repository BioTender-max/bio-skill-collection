# FAERS

> **Subcategory**: `adr` &nbsp;|&nbsp; **Access mode**: `Dataset`

**Purpose**: Post-market drug safety surveillance  

**Coverage**: FDA spontaneous adverse event reports (all marketed drugs)  

## Setup

## Configuration

| Key | Type / Description |
|-----|--------------------|
| `csv_path` | path to processed CSV with columns: |
| `min_reports` | minimum report count to include (default 5) |

## Usage

```python
from drugclaw.skills.adr.faers import FAERSSkill

skill = FAERSSkill(config={
    "csv_path": "...",  # path to processed CSV with columns:
    "min_reports": "...",  # minimum report count to include (default 5)
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
