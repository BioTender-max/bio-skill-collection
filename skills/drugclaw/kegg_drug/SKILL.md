# 68 · KEGG Drug

> Approved drugs — structures, targets, pathways & drug-drug interactions  
> **Category:** Drug-centric | **Type:** DB | **Subcategory:** DDI  
> **API:** `https://rest.kegg.jp` (free, no key required for academic use)

| Resource | URL |
|----------|-----|
| Homepage | https://www.genome.jp/kegg/ |
| API docs | https://www.kegg.jp/kegg/docs/keggapi.html |
| Paper    | https://academic.oup.com/nar/article/38/suppl_1/D355/3112250 |

---

## What it provides

- **Drug metadata**: name, formula, molecular weight, efficacy, class
- **Targets**: gene/protein targets for each approved drug
- **Interactions (DDI)**: drug-drug interaction annotations
- **Pathways**: linked KEGG pathway IDs

---

## Quick start

```python
from 68_KEGG_Drug import query

# Single entity
results = query("aspirin")

# Multiple entities
results = query(["aspirin", "metformin", "imatinib"])

# By KEGG Drug ID
results = query("D00109")

# Specific fields only
results = query("warfarin", fields="targets")
results = query("warfarin", fields="interactions")
```

---

## `query()` interface

```
query(entities, fields="all") -> list[dict]
```

| Parameter  | Type               | Description |
|------------|--------------------|-------------|
| `entities` | `str \| list[str]` | Drug name(s) or KEGG Drug ID(s) (e.g. `"D00109"`) |
| `fields`   | `str`              | `"all"` — full entry; `"targets"` — targets only; `"interactions"` — DDI only |

### Return structure (`fields="all"`)

```json
[
  {
    "drug_id": "dr:D00109",
    "query": "aspirin",
    "name": "Aspirin (JP18/USP/INN); ...",
    "formula": "C9H8O4",
    "mol_weight": "180.0423",
    "targets": ["PTGS1 ...", "PTGS2 ..."],
    "interactions": ["Warfarin [precaution] ...", ...],
    "pathways": ["map07112 ...", ...],
    "classes": ["Analgesic ...", ...]
  }
]
```

If a name cannot be resolved, the entry contains `{"query": "xxx", "error": "No match found"}`.

---

## Lower-level functions

| Function | Input | Output | Description |
|----------|-------|--------|-------------|
| `search(query, limit=10)` | drug name/keyword | `list[{id, name}]` | Keyword search |
| `get_entry(drug_id)` | KEGG Drug ID | `dict` | Full parsed entry |
| `get_targets(drug_id)` | KEGG Drug ID | `list[str]` | Target lines |
| `get_interactions(drug_id)` | KEGG Drug ID | `list[str]` | DDI lines |

---

## Notes

- KEGG REST API is free for academic use; commercial use requires a license.
- Rate limit: no official cap, but keep requests reasonable (~1 req/sec).
- Drug IDs look like `D00109` or `dr:D00109`; both formats accepted.
- Not all drugs have interaction or target annotations — empty list means no data.
