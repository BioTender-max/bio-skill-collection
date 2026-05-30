---
name: DDInter
description: >
  Query the DDInter drug-drug interaction database. Use whenever the user asks
  about drug-drug interactions, DDI severity levels, or wants to look up
  interactions for a drug name or DDInter ID.
---

# DDInter Query Skill

Search DDInter interaction records by drug name or DDInter ID. Auto-detects input type:

| Input Pattern | Detected As | Match Logic |
|---|---|---|
| `DDInter582` | DDInter ID | exact on `DDInterID_A` or `DDInterID_B` |
| anything else | drug name | exact then substring on `Drug_A` / `Drug_B` |

## API

| Function | Input | Returns |
|---|---|---|
| `search(entity)` | drug name or DDInter ID | `list[dict]` |
| `search_batch(entities)` | list of entity strings | `dict[str, list[dict]]` |
| `get_interactions_between(drug_a, drug_b)` | two drug names | `list[dict]` |
| `summarize(hits, entity)` | hit list + label | compact text |
| `to_json(hits)` | hit list | `list[dict]` |
| `list_drugs()` | — | sorted unique drug names |

## Usage

See `if __name__ == "__main__"` block in `20_DDInter.py` for runnable examples covering: single drug search, DDInter ID lookup, pairwise interaction check, batch search, and JSON output.

## Key Fields

Each interaction row contains: `DDInterID_A`, `Drug_A`, `DDInterID_B`, `Drug_B`, `Level` (Major / Moderate / Minor).

## Data

- **Source**: 8 CSV files partitioned by ATC code (`ddinter_downloads_code_{A,B,D,H,L,P,R,V}.csv`)
- **Path**: `resources_metadata/ddi/DDInter/`
- **Citation**: Xiong G, et al. *Nucleic Acids Res.* 2025;53(D1):D1356. DDInter 2.0.
