# Drug Reviews (Drugs.com)

> **Subcategory**: `drug_review` &nbsp;|&nbsp; **Access mode**: `Dataset`

**Purpose**: Drug reviews dataset  

**Coverage**: UCI/Drugs.com drug reviews with patient ratings  

## Setup

## Configuration

| Key | Type / Description |
|-----|--------------------|
| `csv_path` | path to drugsComTrain_raw.tsv or drugsComTest_raw.tsv |
| `delimiter` | column delimiter (default: "   ") |

## Usage

```python
from drugclaw.skills.drug_review.drugs_com_reviews import DrugsComReviewsSkill

skill = DrugsComReviewsSkill(config={
    "csv_path": "...",  # path to drugsComTrain_raw.tsv or drugsComTest_raw.tsv
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
