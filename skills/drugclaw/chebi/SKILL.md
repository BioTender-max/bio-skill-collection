---
name: chebi-query
description: >
  Query the ChEBI (Chemical Entities of Biological Interest) database.
  Use whenever the user asks about small molecule identifiers, chemical
  ontology roles, molecular formulae, SMILES, InChI, synonyms, or
  cross-references for biologically relevant chemical compounds via ChEBI.
---

# ChEBI Query Skill

Search the ChEBI 2.0 REST API by any entity. Auto-detects input type:

| Input Pattern | Detected As | Action |
|---|---|---|
| `CHEBI:15422` / `chebi:15422` | ChEBI ID (prefixed) | full entity lookup via `/compound/{id}/` |
| `27732` (pure digits ≤7) | ChEBI ID (numeric) | full entity lookup via `/compound/{id}/` |
| anything else | free text | Elasticsearch search via `/es_search/?term=...` |

## API

| Function | Input | Returns |
|---|---|---|
| `search(query, max_results=25)` | single entity string | `list[dict]` |
| `search_batch(queries, max_results=25)` | list of entity strings | `dict[str, list[dict]]` |
| `summarize(results, label)` | result list + label | compact one-line-per-hit text |
| `to_json(results)` | result list | `list[dict]` (JSON-serialisable) |

Lower-level helpers (called internally):

| Function | Purpose |
|---|---|
| `search_chebi(query, max_results)` | keyword search via `GET /es_search/?term=...&size=N` |
| `get_entity(chebi_id)` | full entity via `GET /compound/CHEBI:{id}/` |
| `get_entities_batch(chebi_ids)` | batch lookup via `GET /compounds/?chebi_ids=id1,id2,...` |

`search_batch()` automatically uses the efficient batch endpoint when all
queries are ChEBI IDs; otherwise it iterates with a 0.3 s delay.

## Usage

See `if __name__ == "__main__"` block in `64_ChEBI.py` for runnable examples
covering: single ID lookup, name search, formula search, batch ID search,
mixed batch search, and JSON output.

## Key Fields Returned

**Top-level**: `chebi_accession`, `name`, `ascii_name`, `definition`, `stars`
(curation quality; 3 = fully curated), `secondary_ids`, `is_released`.

**chemical_data** (nested dict): `formula`, `charge`, `mass`,
`monoisotopic_mass`.

**default_structure** (nested dict): `smiles`, `standard_inchi`,
`standard_inchi_key`, `wurcs`.

**names** (nested dict by type): keys like `IUPAC NAME`, `SYNONYM`,
`BRAND NAME`, `UNIPROT NAME`; each value is a list of name objects.

**ontology_relations**: `incoming_relations` and `outgoing_relations`, each a
list of `{init_id, init_name, relation_type, final_id, final_name}`.

**database_accessions** (nested dict by type): `CAS`, `MANUAL_X_REF`,
`REGISTRY_NUMBER`, `CITATION`; cross-refs to DrugBank, KEGG, HMDB, PubChem,
PDBeChem, Wikipedia, etc.

**roles_classification**: list of role dicts with `chebi_accession`, `name`,
`definition`, `biological_role` (bool), `application` (bool),
`chemical_role` (bool).

## Data Source

- **Database**: ChEBI 2.0 (EMBL-EBI), >195,000 molecular entities
- **API base**: `https://www.ebi.ac.uk/chebi/backend/api/public/`
- **Docs**: <https://www.ebi.ac.uk/chebi/backend/api/docs/>
- **License**: CC BY 4.0
- **Citation**: Bento et al. *Nucleic Acids Res.* 2025, 54(D1), D1768–D1774.
