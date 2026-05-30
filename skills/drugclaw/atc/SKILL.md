---
name: 27_ATC_DDD
description: >
  Query the WHO ATC/DDD Classification System. Use whenever the user asks about
  ATC codes, drug classification hierarchy, Defined Daily Doses (DDD), or wants
  to look up drugs by ATC class or find the ATC code for a drug name.
---

# ATC/DDD Query Skill

Look up ATC classification and DDD data for drugs. Auto-detects entity type:

| Input Pattern | Detected As | Query Path |
|---|---|---|
| `N02BA` `A10BA02` `C09XX01` | ATC code | local DDD lookup + RxNav member drugs |
| `aspirin` `metformin` | drug name | RxNav ATC classification + local DDD match |

ATC code regex: `^[A-Z]\d{2}([A-Z]{1,2}\d{0,2})?$`

## API

| Function | Input | Returns |
|---|---|---|
| `load_local(path)` | Excel path | `list[dict]` — cached ATC/DDD records |
| `search(entity)` | single string | `dict` with `entity`, `entity_type`, `local_hits`, `api_hits` |
| `search_batch(entities)` | list of strings | `dict[str, dict]` — keyed by entity |
| `summarize(result)` | search result dict | compact LLM-readable text |
| `to_json(result)` | search result dict | JSON string |

All functions accept `use_api=True|False` to toggle RxNav queries (default: on).

## Usage

See `if __name__ == "__main__"` block in `27_ATC_DDD.py` for runnable examples:

```python
from importlib import import_module
atc = import_module("27_ATC_DDD")

# Drug name → ATC classes
r = atc.search("aspirin")
print(atc.summarize(r))

# ATC code → member drugs + DDD
r = atc.search("N02BA")
print(atc.summarize(r))

# Batch
results = atc.search_batch(["metformin", "A10BA02", "C09XX01"])

# JSON for pipeline
print(atc.to_json(atc.search("sparsentan")))
```

## Data

- **Local file**: `ATC_DDD_new and alterations 2026_final.xlsx`
- **Columns**: `atc_code`, `atc_level_name`, `new_ddd`, `unit`, `adm_route`, `note`
- **Path**: `DATA_DIR` / `XLSX_PATH` in `27_ATC_DDD.py`
- **Remote API**: RxNav RxClass (`rxnav.nlm.nih.gov/REST/rxclass/`)
- **Citation**: WHOCC — WHO Collaborating Centre for Drug Statistics Methodology, ATC/DDD Index 2026. https://atcddd.fhi.no/atc_ddd_index/
