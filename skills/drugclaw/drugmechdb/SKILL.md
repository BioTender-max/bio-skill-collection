---
name: drugmechdb-query
description: >
  Query the DrugMechDB drug mechanism-of-action database. Use whenever the user
  asks about drug mechanisms, drug-to-disease paths, biological targets of a drug,
  or wants to look up any biomedical entity (drug name, protein, disease, DrugBank ID,
  MESH ID, UniProt ID, GO term, etc.) in DrugMechDB.
---

# DrugMechDB Query Skill

Search drug mechanism-of-action paths by entity name or ID. Each path is a directed graph: Drug → (intermediates) → Disease, with typed nodes and labeled edges.

## Data

- **Source**: `indication_paths.json`
- **Path**: `resources_metadata/drug_mechanism/DRUGMECHDB/indication_paths.json`
- **Records**: ~4846 mechanism paths, ~32k relationships

## Entity auto-detection

| Input pattern | Detected as | Example |
|---|---|---|
| `DB:DB00619` | DrugBank ID | exact on node/graph IDs |
| `MESH:D015464` | MESH ID | exact on node/graph IDs |
| `UniProt:P00519` | UniProt protein | exact on node IDs |
| `GO:0006915` | GO term | exact on node IDs |
| `CHEBI:*`, `HP:*`, `UBERON:*`, `CL:*`, `reactome:*`, `InterPro:*`, `PR:*`, `taxonomy:*` | respective types | exact on node IDs |
| anything else | free text | substring match on drug/disease/node names |

## API

| Function | Signature | Returns |
|---|---|---|
| `load(path)` | path to JSON | `list[dict]` — full database |
| `build_index(db)` | loaded db | `(by_id, by_name, by_drug, by_disease)` dicts for O(1) lookup |
| `search(db, entity, index=None)` | single query string | `list[dict]` — matching paths |
| `search_batch(db, entities, index=None)` | list of query strings | `dict[str, list[dict]]` |
| `summarize(paths, entity)` | search results | compact multi-line text |
| `to_json(paths)` | search results | list of flat dicts (id, drug, disease, nodes, links) |

## Node types (14)

BiologicalProcess, Cell, CellularComponent, ChemicalSubstance, Disease, Drug, GeneFamily, GrossAnatomicalStructure, MacromolecularComplex, MolecularActivity, OrganismTaxon, Pathway, PhenotypicFeature, Protein

## Quick usage

```python
import drugmechdb_query as dq

db = dq.load()  # uses default DATA_PATH
idx = dq.build_index(db)  # optional, recommended for repeated queries

# Single query — by name or ID
paths = dq.search(db, "imatinib", idx)
paths = dq.search(db, "UniProt:P00519", idx)
paths = dq.search(db, "MESH:D003920", idx)
print(dq.summarize(paths, "imatinib"))

# Batch query
results = dq.search_batch(db, ["metformin", "MESH:D003920", "asthma"], idx)
for entity, paths in results.items():
    print(dq.summarize(paths, entity))

# JSON export
print(dq.to_json(paths))
```

## Output structure per path

```
graph:  { _id, drug, disease, drugbank, drug_mesh, disease_mesh }
nodes:  [{ id, label, name }, ...]
links:  [{ source, target, key }, ...]
```

`key` examples: `decreases activity of`, `causes`, `positively regulates`, `treats`, `increases expression of`, etc. (66 relation types total).
