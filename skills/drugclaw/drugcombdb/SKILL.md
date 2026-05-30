---
name: drugcombdb-query
description: >
  Query canonical DrugCombDB combination records. Use when the user asks about
  drug pairs, synergy values, or cell-line-specific combination evidence.
---

# DrugCombDB Query Skill

Query canonical packaged DrugCombDB CSV rows.

## Data

- Path: `resources_metadata/drug_combination/DrugCombDB/drugcombdb.csv`
- Columns: `Drug1`, `Drug2`, `Cell`, `Synergy`, `SynergyType`, `PMID`

## API

| Function | Input | Returns |
|---|---|---|
| `load_data(path)` | CSV path | `list[dict]` |
| `search_drug(drug_name, limit)` | drug name | `list[dict]` |
| `search_cell_line(cell, limit)` | cell line | `list[dict]` |
| `search_drug_pair(drug1, drug2, limit)` | drug pair | `list[dict]` |
| `search(entity, limit)` | free text | `list[dict]` |
| `search_batch(entities, limit)` | list of strings | `dict[str, list[dict]]` |
| `summarize(results, entity)` | rows + label | compact text |

## Usage

Run `example.py` directly for canonical-path demos.
