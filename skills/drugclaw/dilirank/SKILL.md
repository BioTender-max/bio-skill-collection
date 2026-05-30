---
name: 48_LTKB
description: >
  Query the DILIrank/FDA Liver Toxicity Knowledge Base (LTKB). Use whenever the user asks
  about drug-induced liver injury (DILI) risk, hepatotoxicity classification,
  or wants to look up any drug (by name, LTKB ID, or DILIst ID) in the
  DILIrank or DILIst datasets.
---

# LTKB Query Skill

Search FDA LTKB records (DILIrank 2.0 + DILIst) by any entity. Auto-detects type by pattern:

| Input Pattern | Detected As | Searched In |
|---|---|---|
| `LT00040` | LTKB ID | DILIrank only |
| `2` (digits) | DILIst ID | DILIst only |
| anything else | drug name | both datasets (substring) |

## Datasets

**DILIrank 2.0** — 1,036 FDA-approved drugs ranked by DILI concern:

| vDILI-Concern | Meaning |
|---|---|
| vMOST-DILI-concern | Strong evidence of causing DILI |
| vLess-DILI-concern | Some evidence of causing DILI |
| vNo-DILI-concern | No credible evidence |
| vAmbiguous-DILI-concern | Conflicting/insufficient evidence |

Columns: `LTKBID`, `CompoundName`, `SeverityClass`, `LabelSection`, `vDILI-Concern`, `Comment`

**DILIst** — 1,279 drugs classified by DILI severity:

| Classification | Meaning |
|---|---|
| 1 | DILI-positive |
| 0 | DILI-negative |

Columns: `DILIST_ID`, `CompoundName`, `DILIst Classification`, `Routs of Administration`

## API

| Function | Input | Returns |
|---|---|---|
| `load_all(rank_path, list_path)` | Excel paths | `{"dilirank": [...], "dilist": [...]}` |
| `search(data, entity)` | data dict + entity string | `{"entity", "type", "dilirank": [], "dilist": []}` |
| `search_batch(data, entities)` | data dict + list of strings | `{entity: search_result}` |
| `summarize(result, entity)` | search result + label | compact text |
| `to_json(result)` | search result | JSON string |

## Usage

See `if __name__ == "__main__"` block in `48_LTKB.py` for runnable examples covering: drug name, LTKB ID, DILIst ID, batch search, and JSON output.

## Data

- **Source**: FDA LTKB — <https://www.fda.gov/science-research/bioinformatics-tools/liver-toxicity-knowledge-base-ltkb>
- **Files**: `Drug Induced Liver Injury Rank (DILIrank 2.0) Dataset  FDA.xlsx`, `DILIst Supplementary Table.xlsx`
- **Path**: `DATA_DIR` variable in `48_LTKB.py`
