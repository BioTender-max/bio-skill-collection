---
name: DrugComb
description: >
  Query the DrugComb drug combination database for cancer cell-line synergy
  and sensitivity data. Use whenever the user asks about drug combinations,
  synergy scores (ZIP/Bliss/Loewe/HSA), combination sensitivity (CSS),
  or wants to look up how two drugs interact in a specific cancer cell line.
---

# DrugComb Query Skill

Search DrugComb summary records by any entity. Auto-detects type by pattern:

| Input Pattern | Detected As | Match Logic |
|---|---|---|
| `5-FU` / `imatinib` | drug name | case-insensitive substring on `drug_row` OR `drug_col` |
| `A549` / `MCF-7` | cell line | case-insensitive substring on `cell_line_name` |
| `12345` (pure digits) | block_id | exact on `block_id` |
| `CID:2244` | PubChem CID | exact on `drug_row_cid` OR `drug_col_cid` |

## API

| Function | Input | Returns |
|---|---|---|
| `load_drugcomb(path)` | CSV path | `list[dict]` |
| `columns(data)` | loaded data | column name list |
| `search(data, entity)` | single entity string | `list[dict]` |
| `search_batch(data, entities)` | list of entity strings | `dict[str, list[dict]]` |
| `summarize(hits, entity)` | hit list + label | compact LLM-readable text |
| `to_json(hits)` | hit list | `list[dict]` |

## Usage

See `if __name__ == "__main__"` block in `example.py` for runnable examples covering: drug name search, cell-line search, batch search, and JSON output.

## Data

- **Source**: DrugComb normalized full-package output
- **Key columns**: `drug_row`, `drug_col`, `cell_line_name`, `synergy_zip`, `synergy_bliss`
- **Path**: `resources_metadata/drug_combination/DrugComb/drugcomb.csv`

## Citation

Zagidullin B, Aldahdooh J, Zheng S, et al. DrugComb: an integrative cancer drug combination data portal. *Nucleic Acids Res.* 2019;47(W1):W43–W51. doi:10.1093/nar/gkz337
