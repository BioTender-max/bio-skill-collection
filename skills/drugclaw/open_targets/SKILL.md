---
name: open-targets-platform
description: >
  Query the Open Targets Platform for drug-target-disease associations.
  Use whenever the user asks about drug targets, gene-disease associations,
  drug indications, clinical trial phases, or wants to look up any entity
  (Ensembl gene ID, ChEMBL drug ID, or free-text gene/drug name) in Open
  Targets. Also trigger when the user mentions Open Targets, ENSG IDs,
  CHEMBL IDs, or asks about target prioritization for diseases.
---

# Open Targets Platform Query Skill

Query the Open Targets GraphQL API for drug, target, and disease association data. No API key required.

## Entity Auto-Detection

| Input Pattern | Detected As | Example |
|---|---|---|
| `ENSG00000...` | Target (Ensembl gene ID) | `ENSG00000146648` (EGFR) |
| `CHEMBL...` | Drug (ChEMBL ID) | `CHEMBL941` (Imatinib) |
| anything else | Free-text search | `BRCA1`, `aspirin` |

## API

| Function | Input | Returns |
|---|---|---|
| `query(entity)` | single entity string | dict with type, name, associations |
| `query_batch(entities)` | list of entity strings | list[dict] |
| `summarize(result)` | query result dict | compact one-line text |
| `get_target_info(ensembl_id)` | Ensembl ID string | raw GraphQL response |
| `get_drug_info(chembl_id)` | ChEMBL ID string | raw GraphQL response |
| `search_entities(term)` | free-text string | raw GraphQL response |

## Return Format

**Target result:**
```json
{"entity": "ENSG00000146648", "type": "target", "found": true,
 "symbol": "EGFR", "name": "epidermal growth factor receptor",
 "biotype": "protein_coding",
 "top_diseases": [{"disease": "lung carcinoma", "score": 0.78}]}
```

**Drug result:**
```json
{"entity": "CHEMBL941", "type": "drug", "found": true,
 "name": "IMATINIB", "drug_type": "Small molecule",
 "max_phase": 4,
 "indications": [{"disease": "chronic myeloid leukemia", "phase": 4}]}
```

**Search result:**
```json
{"entity": "BRCA1", "type": "search", "found": true,
 "hits": [{"id": "ENSG00000012048", "name": "BRCA1", "entity_type": "target"}]}
```

## Usage

See `if __name__ == "__main__"` block in `12_Open_Targets_Platform.py` for runnable examples covering: single target/drug/search query, batch query, and JSON output.

## Source

- **Endpoint**: `https://api.platform.opentargets.org/api/v4/graphql`
- **Docs**: https://platform.opentargets.org/
- **Paper**: https://doi.org/10.1093/nar/gkac1046
