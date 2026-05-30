---
name: drugbank-query
description: >
  Query a locally downloaded DrugBank database. Use whenever the user asks about
  drug information, drug targets, drug-drug interactions, drug categories, or wants
  to look up any entity (DrugBank ID, drug name, CAS number, synonym) in DrugBank.
---

# DrugBank Local Query Skill

Search local DrugBank data by any entity. Auto-detects query type:

| Input Pattern | Detected As | Match Logic |
|---|---|---|
| `DB00945` | DrugBank ID | exact on `drugbank_id` |
| anything else | free text | substring on `name`, `synonyms`, `cas_number` |

## Data

- **Base dir**: `resources_metadata/drug_knowledgebase/DrugBank/`
- **Files**:
  - `full database.xml` — rich fields: description, targets, interactions, categories, synonyms, groups
  - `drugbank vocabulary.csv` — lightweight: DrugBank ID, name, CAS, synonyms
- **Auto-select**: prefers XML if present, falls back to vocabulary CSV

## API

| Function | Input | Returns |
|---|---|---|
| `load(path)` | file path (XML or TSV/CSV, auto-detected) | `list[dict]` |
| `search(data, entity)` | single entity string | `list[dict]` |
| `search_batch(data, entities)` | list or comma-separated string | `dict[str, list[dict]]` |
| `summarize(hits, entity)` | hit list + label | compact text |
| `to_json(hits)` | hit list | JSON string |

## Usage

```python
from 07_DrugBank import load, search, search_batch, summarize, to_json

data = load()                              # auto-selects XML or CSV

# single query
hits = search(data, "aspirin")
print(summarize(hits, "aspirin"))

# batch query
results = search_batch(data, ["metformin", "DB00316", "ibuprofen"])
for entity, hits in results.items():
    print(summarize(hits, entity))

# JSON output
print(to_json(hits[:1]))
```

See `if __name__ == "__main__"` block in `07_DrugBank.py` for runnable examples.
