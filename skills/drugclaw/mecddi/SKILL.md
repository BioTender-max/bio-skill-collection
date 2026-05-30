---
name: mecddi-query
description: >
  Query the MecDDI mechanism-based drug-drug interaction database. Use whenever
  the user asks about drug-drug interactions, DDI mechanisms (PK/PD), enzyme or
  transporter-mediated interactions, or wants to look up interacting drug pairs
  by drug name or MecDDI drug ID. Trigger on keywords like DDI, drug interaction,
  MecDDI, mechanism-based interaction, pharmacokinetic interaction, pharmacodynamic
  interaction, or any query involving two drugs that may interact.
---

# MecDDI Query Skill

Search MecDDI drug-drug interaction records by drug name or drug ID. Auto-detects input type:

| Input Pattern | Detected As | Match Logic |
|---|---|---|
| `D0123` | MecDDI Drug ID | exact on `A_Drug_ID` / `B_Drug_ID` |
| anything else | free text | substring on `A_Drug_Name` / `B_Drug_Name` |

## Mechanism Categories (7 files)

| Category | Type |
|---|---|
| Affected Gastrointestinal Absorption | PK |
| Affected Cellular Transport | PK |
| Affected Organization Distribution | PK |
| Affected Intra/Extra-Hepatic Metabolism | PK |
| Affected Excretion Pathways | PK |
| Pharmacodynamic Additive Effects | PD |
| Pharmacodynamic Antagonistic Effects | PD |

## API

| Function | Input | Returns |
|---|---|---|
| `load_mecddi(data_dir)` | directory path | list[dict] (all records) |
| `search(records, entity)` | single entity string | list[dict] |
| `search_batch(records, entities)` | list of strings | dict[str, list[dict]] |
| `summarize(hits, entity)` | hits + label | compact text for LLM |
| `to_json(hits)` | list[dict] | JSON string |

## Data

- **Source**: 7 TSV files downloaded from <https://mecddi.idrblab.net/download>
- **Path**: `DATA_DIR` variable in `19_MecDDI.py` (default: `resources_metadata/ddi/MecDDI`)
- **Columns**: `A_Drug_ID`, `A_Drug_Name`, `B_Drug_ID`, `B_Drug_Name`, `Mechanism_Category`

## Usage

See `if __name__ == "__main__"` block in `19_MecDDI.py` for runnable examples covering:

1. **Single drug name** → `search(data, "Atropine")`
2. **Single drug ID** → `search(data, "D0123")`
3. **Batch query** → `search_batch(data, ["Meclizine", "Isocarboxazid", "D0853"])`
4. **JSON output** → `to_json(hits)`
5. **LLM-friendly summary** → `summarize(hits, entity)`
