# GDSC

> **Subcategory**: `drug_molecular_property` &nbsp;|&nbsp; **Access mode**: `Local File`

**Purpose**: Genomics of drug sensitivity in cancer  

**Coverage**: GDSC compound metadata plus drug sensitivity resources  

## Setup

1. Download the current release from:
   <https://ftp.sanger.ac.uk/pub/project/cancerrxgene/releases/current_release/>
2. Set `csv_path` (or `tsv_path` / `json_path`) in config (see below).

## Configuration

| Key | Type / Description |
|-----|--------------------|
| `csv_path` | path to a real GDSC CSV, e.g. `screened_compounds_rel_8.4.csv` |
| `delimiter` | column delimiter (default: auto-detect from extension) |

## Usage

```python
from drugclaw.skills.drug_molecular_property.gdsc import GDSCSkill

skill = GDSCSkill(config={
    "csv_path": "...",  # path to GDSC CSV file (e.g. GDSC2_fitted_dose_response.csv)
    "delimiter": "...",  # column delimiter (default: auto-detect from extension)
})

if skill.is_available():
    results = skill.retrieve(
        entities={"drug": ["Erlotinib"]},
        query="target",
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

- Current release: <https://ftp.sanger.ac.uk/pub/project/cancerrxgene/releases/current_release/>
