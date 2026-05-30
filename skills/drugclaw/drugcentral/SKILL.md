---
name: drugcentral-query
description: >
  Query the DrugCentral drug pharmacology database. Use whenever the user asks about
  approved drug structures, drug targets, pharmacological actions, or wants to look up
  any entity (drug name, DrugCentral ID, CAS number, InChIKey) in DrugCentral.
---

# DrugCentral Query Skill

Search local DrugCentral flat files by any entity. Auto-detects query type:

| Input Pattern | Detected As | Match Logic |
|---|---|---|
| `860` (numeric) | DrugCentral ID | exact on `ID` |
| `50-78-2` (NNN-NN-N) | CAS Number | exact on `CAS_RN` |
| `BSYNRYMUTXBXSQ` or full key | InChIKey (prefix or full) | prefix match on `InChIKey` |
| anything else | free text | substring on `INN` (drug name) |

## Data

Download from <https://drugcentral.org/download>:

| File | Description | Required |
|---|---|---|
| `structures.smiles.tsv` | SMILES, InChI, InChIKey, ID, INN, CAS_RN | **Yes** |
| `drug.target.interaction.tsv` | Drug-target interaction profiles (gene, action, potency) | Recommended |
| `FDA+EMA+PMDA_Approved.csv` | Approval status (ID, drug_name) | Optional |

Place files in `DATA_DIR` (default: `resources_metadata/drug_knowledgebase/DrugCentral`, or set env `DRUGCENTRAL_DIR`).

## API

| Function | Input | Returns |
|---|---|---|
| `search(entity)` | single entity string | `dict` with `structures`, `targets`, `approved` |
| `search_batch(entities)` | list or comma-separated string | `dict[str, dict]` |
| `summarize(result, entity)` | search result dict + label | compact text |
| `to_json(result)` | search result dict | JSON string |

## Key Fields

**structures**: `ID`, `INN` (drug name), `CAS_RN`, `SMILES`, `InChI`, `InChIKey`

**targets** (from DTI file): `GENE`, `TARGET_NAME`, `TARGET_CLASS`, `ACTION_TYPE`, `ACT_VALUE`, `ACT_TYPE`, `ACT_UNIT`, `ACCESSION` (UniProt), `TDL`, `ORGANISM`

**approved**: `id`, `name`, `approved` (bool)

## Usage

```python
from 18_DrugCentral import search, search_batch, summarize, to_json

# Single query — drug name
result = search("aspirin")
print(summarize(result))

# Single query — DrugCentral ID
result = search("860")
print(summarize(result))

# Single query — CAS number
result = search("50-78-2")
print(summarize(result))

# Batch query
results = search_batch(["metformin", "ibuprofen", "50-78-2"])
for entity, res in results.items():
    print(summarize(res, entity))

# JSON export
print(to_json(result))
```

See `if __name__ == "__main__"` block in `18_DrugCentral.py` for runnable examples covering: drug name, DrugCentral ID, CAS number, InChIKey prefix, batch search, and JSON output.

## Source

- **DrugCentral**: <https://drugcentral.org/>
- **Paper**: Avram et al., *Nucleic Acids Research* 2023, 51(D1):D1276–D1287. DOI: [10.1093/nar/gkac1085](https://doi.org/10.1093/nar/gkac1085)
- **License**: CC BY-NC 4.0 (non-commercial)
