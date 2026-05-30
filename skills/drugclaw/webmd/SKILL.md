---
name: webmd-drug-reviews
description: >
  Query the WebMD Drug Reviews dataset (~362 k patient reviews, 2007–2020).
  Use whenever the user asks about patient-reported drug effectiveness,
  ease of use, satisfaction ratings, side effects, or reviews for a
  specific drug or medical condition.
---

# WebMD Drug Reviews Query Skill

Search patient reviews by drug name or medical condition. Auto-fallback: if no drug matches, searches conditions.

| Input Example | Match Logic |
|---|---|
| `Lipitor` | substring on `Drug` column |
| `High Blood Pressure` | substring on `Condition` column |
| any text | try `Drug` first → fall back to `Condition` |

## API

| Function | Input | Returns |
|---|---|---|
| `load_reviews(path)` | CSV path (default `DATA_PATH`) | list[dict] |
| `search(rows, entity)` | single entity string | list[dict] |
| `search_by_drug(rows, drug)` | drug name string | list[dict] |
| `search_by_condition(rows, cond)` | condition string | list[dict] |
| `search_batch(rows, entities)` | list of entity strings | dict[str, list[dict]] |
| `summarize(hits, entity)` | matched rows + label | compact text (counts, avg ratings, top conditions/drugs) |
| `to_json(hits)` | matched rows | list[dict] |

## Usage

See `if __name__ == "__main__"` block in `10_WebMD_Drug_Reviews.py` for runnable examples covering: single drug lookup, single condition lookup, batch search, and JSON output.

## Data

- **Source**: `webmd.csv` (Kaggle – rohanharode07/webmd-drug-reviews-dataset)
- **Columns**: `Drug`, `Condition`, `Reviews`, `Side`, `Age`, `Sex`, `Effectiveness`, `EaseofUse`, `Satisfaction`
- **Ratings**: 1-5 star scale for Effectiveness, EaseofUse, Satisfaction
- **Path**: `DATA_PATH` variable in `10_WebMD_Drug_Reviews.py`
  (`resources_metadata/drug_review/WebMDDrugReviews/webmd.csv`)
