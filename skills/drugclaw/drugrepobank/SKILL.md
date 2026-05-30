---
name: DrugRepoBank-query
description: >
  Query the DrugRepoBank drug repurposing evidence database. Use whenever the
  user asks about repurposing candidates, drug–disease–target repurposing
  evidence, or wants to look up any entity (drug name, DrugBank ID, ChEMBL ID,
  PubChem CID, TTD target ID, UniProt ID, disease name) in DrugRepoBank.
---

# DrugRepoBank Query Skill

Search four linked tables (Drug, Target, DrugTargetInteraction, Literature)
for repurposing evidence. Auto-detects entity type by prefix:

| Input Pattern | Detected As | Example |
|---|---|---|
| `DB00945` | DrugBank ID | exact on `DrugBank_ID` / `DrugID` |
| `T47101` | TTD Target ID | exact on `TargetID` |
| `FGFR1_HUMAN` | UniProt ID | exact on `UniprotID` |
| `CHEMBL2103749` | ChEMBL ID | exact on `ChEMBL ID` in Drug table |
| `16129704` (digits) | PubChem CID | exact on `PubChem_Compound_ID` / `PubChemID` |
| anything else | free text | substring on drug Name, TargetName, Disease, NewDisease |

## API

| Function | Input | Returns |
|---|---|---|
| `load_all()` | — | `dict` with keys `drug`, `dti`, `lit`, `target` (lists of row-dicts) |
| `search(tables, entity)` | tables dict + single entity string | `dict` with keys `entity`, `entity_type`, `drug`, `target`, `dti`, `literature` |
| `search_batch(tables, entities)` | tables dict + list of entity strings | `dict[str, search_result]` |
| `summarize(result)` | single `search()` result | compact one-line LLM-readable text |
| `to_json(result)` | single `search()` result | JSON string (trimmed heavy fields) |

## Usage

See `if __name__ == "__main__"` block in `42_DrugRepoBank.py` for runnable
examples covering: drug name, DrugBank ID, TTD target ID, UniProt ID, ChEMBL
ID, disease free-text, batch search, and JSON output.

## Data

Four CSV tables in `DATA_DIR`:

| File | Key Columns | Description |
|---|---|---|
| `Drug.csv` | DrugBank_ID, Name, Drug Groups, PubChem_Compound_ID, ChEMBL ID, SMILES | Drug identifiers & structures |
| `DrugTargetInteraction.csv` | UniprotID, PubchemID, TargetID, DrugID, Highest_status, MOA | Drug–target links with mechanism of action |
| `Literature.csv` | DrugName, DrugID, Target, Disease, NewDisease, Evidence, Insilico, Invitro, Invivo, Clinicaltrial, PMID | Repurposing evidence & literature references |
| `Targets.csv` | TargetID, UniprotID, TargetName, TargetGeneName, TargetType, Function | Target annotations & pathway memberships |

- **Path**: `DATA_DIR` variable in `42_DrugRepoBank.py`  
  (`resources_metadata/drug_repurposing/DrugRepoBank`)
- **Source**: https://awi.cuhk.edu.cn/DrugRepoBank/php/index.php
- **Paper**: Huang et al., *Database* 2024, baae051. DOI:10.1093/database/baae051
