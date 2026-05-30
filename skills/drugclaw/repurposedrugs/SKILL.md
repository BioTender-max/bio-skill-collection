---
name: RepurposeDrugs-query
description: >
  Query the RepurposeDrugs single-agent drug repurposing database. Use whenever
  the user asks about drug-disease repurposing associations, clinical trial phases
  for repurposed drugs, or wants to look up any entity (drug name, disease name,
  NCT ID) in RepurposeDrugs.
---

# RepurposeDrugs Query Skill

Search canonical drug-disease repurposing rows. Auto-detects query type by pattern:

| Input Pattern | Detected As | Match Logic |
|---|---|---|
| `34567890` | PMID | exact on `pmid` |
| anything else | free text | substring on `drug` OR `disease` |

## API

| Function | Input | Returns |
|---|---|---|
| `load_data(path)` | CSV path | `list[dict]` |
| `search(rows, entity)` | single entity string | `list[dict]` |
| `search_batch(rows, entities)` | list of entity strings | `dict[str, list[dict]]` |
| `summarize(hits, entity)` | rows + label | compact text |
| `to_json(hits)` | rows | `list[dict]` |

## Usage

See `if __name__ == "__main__"` block in `example.py` for runnable examples.

## Data

- **Source**: RepurposeDrugs normalized full-package output
- **URL**: <https://repurposedrugs.org/>
- **Local file**: `repurposedrugs.csv`
- **Columns**: `drug`, `disease`, `score`, `status`, `pmid`
- **Path**: `resources_metadata/drug_repurposing/RepurposeDrugs/repurposedrugs.csv`
