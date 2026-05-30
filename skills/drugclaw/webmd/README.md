# WebMD Drug Reviews

> **Subcategory**: `drug_review` &nbsp;|&nbsp; **Access mode**: `Dataset`

**Purpose**: Patient drug reviews (WebMD)  

**Coverage**: 362 000+ patient drug reviews from WebMD  

## Setup

1. Download the dataset from: <https://www.kaggle.com/datasets/rohanharode07/webmd-drug-reviews-dataset>
2. Set `csv_path` (or `tsv_path` / `json_path`) in config (see below).

## Configuration

| Key | Type / Description |
|-----|--------------------|
| `csv_path` | path to webmd_drug_reviews.csv |
| `delimiter` | column delimiter (default: ",") |

## Usage

```python
from drugclaw.skills.drug_review.webmd import WebMDReviewsSkill

skill = WebMDReviewsSkill(config={
    "csv_path": "...",  # path to webmd_drug_reviews.csv
    "delimiter": "...",  # column delimiter (default: ",")
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

- Homepage: <https://www.kaggle.com/datasets/rohanharode07/webmd-drug-reviews-dataset>
