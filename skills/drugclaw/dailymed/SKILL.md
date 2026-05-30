---
name: dailymed-query
description: >
  Query DailyMed for FDA drug label / package insert information. Use whenever
  the user asks about drug labeling, SPL documents, prescribing information,
  NDC codes, or needs to look up current FDA-approved drug details by name or
  NDC. Supports single entity or batch queries.
---

# DailyMed Query Skill

Search DailyMed SPL labels by drug name or NDC code. No API key required.

| Input Type | Function | Returns |
|---|---|---|
| drug name (str) | `search_drug_labels(name, limit)` | list of label summaries |
| SPL set ID | `get_label_detail(set_id)` | dict (parsed from XML) |
| NDC code | `get_ndc_info(ndc, limit)` | list of label summaries (JSON) |
| str or list[str] | `query(entities, limit)` | concise text summary |
| list[str] | `search_batch(entities, limit)` | dict[entity → results] |

## API

| Function | Input | Returns |
|---|---|---|
| `search_drug_labels(drug_name, limit=5)` | drug name string | `list[dict]` with `title`, `setid` |
| `get_label_detail(set_id)` | SPL set ID | `dict` (XML→dict, keys vary by label) |
| `get_ndc_info(ndc, limit=5)` | NDC string | `list[dict]` with `title`, `setid` |
| `search_batch(entities, limit=3)` | list of drug names | `dict[str, list[dict]]` |
| `summarize(results, entity)` | results list + label | compact text |
| `query(entities, limit=3)` | single str or list[str] | LLM-readable text block |

## Usage

See `if __name__ == "__main__"` block in `06_DailyMed.py` for runnable examples covering: single drug search, batch multi-drug search, label detail retrieval, and NDC lookup.

## Quick Examples

```python
from importlib.machinery import SourceFileLoader
dm = SourceFileLoader("dm", "06_DailyMed.py").load_module()

# Single entity
print(dm.query("metformin"))

# Multiple entities
print(dm.query(["aspirin", "lisinopril", "atorvastatin"]))

# Full label detail
hits = dm.search_drug_labels("metformin", limit=1)
detail = dm.get_label_detail(hits[0]["setid"])
```

## Data Source

- **Provider**: U.S. National Library of Medicine / DailyMed
- **Base URL**: `https://dailymed.nlm.nih.gov/dailymed/services/v2`
- **Auth**: None (public API)
- **Note**: Search (`/spls.json`) and NDC lookup (`/spls.json?ndc=...`) return JSON. Detail endpoint (`/spls/{setid}.xml`) is XML-only; parsed to dict automatically.
