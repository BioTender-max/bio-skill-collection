---
name: druglib-reviews
description: >
  Query the DrugLib.com Drug Review Dataset (UCI #461). Use whenever the user
  asks about patient drug reviews, drug effectiveness ratings, side-effect
  profiles, or condition-specific treatment experiences from DrugLib.com.
---

# DrugLib Reviews Query Skill

Search patient drug reviews by drug name or medical condition. Auto-detects
entity type and routes to the appropriate field.

| Input Pattern | Detected As | Match Logic |
|---|---|---|
| single/two-word term (e.g. `lamictal`) | drug name | substring on `urlDrugName` |
| multi-word or medical keyword (e.g. `bipolar disorder`) | condition | substring on `condition` |

Condition keywords that trigger condition routing: disease, disorder, syndrome,
infection, pain, cancer, diabetes, hypertension, depression, anxiety, asthma,
arthritis, migraine, allergy, insomnia, nausea, obesity, acne, gerd, copd.

## API

| Function | Input | Returns |
|---|---|---|
| `load_reviews()` | — | list[dict] (cached) |
| `search(entity)` | single entity string | list[dict] |
| `search_batch(entities)` | list of entity strings | dict[str, list[dict]] |
| `summarize(hits, entity)` | list[dict] + label | compact LLM-readable text |
| `to_json(hits)` | list[dict] | list[dict] (JSON-serialisable) |

## Usage

See `if __name__ == "__main__"` block in `16_DRUGLIB_REVIEWS.py` for runnable
examples covering: drug name search, condition search, batch search, and JSON
output.

## Data

- **Source**: Drug Review Dataset (Druglib.com), UCI ML Repository #461
- **Citation**: Kallumadi, S. & Gräßer, F. (2018). *Drug Reviews (Druglib.com)* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C55G6J
- **License**: CC BY 4.0
- **Files**: `drugLibTrain_raw.tsv`, `drugLibTest_raw.tsv` (TSV, merged at load)
- **Path**: `DATA_DIR` variable in `16_DRUGLIB_REVIEWS.py`
- **Columns**:

| Column | Type | Description |
|---|---|---|
| `urlDrugName` | str | Drug name (lowercase, URL-style) |
| `rating` | int 0–9 | Overall patient satisfaction |
| `effectiveness` | str | Highly / Considerably / Moderately / Marginally Effective, Ineffective |
| `sideEffects` | str | No / Mild / Moderate / Severe / Extremely Severe Side Effects |
| `condition` | str | Medical condition being treated |
| `benefitsReview` | str | Free-text review of benefits |
| `sideEffectsReview` | str | Free-text review of side effects |
| `commentsReview` | str | Free-text general comments |
