---
name: chembl-query
description: >
  Query the ChEMBL database for drug molecules, bioactivity data, and drug targets
  via the ChEMBL REST API. Use whenever the user asks about drug properties
  (molecular weight, logP, Lipinski violations), drug-target interactions,
  bioactivity assay results, or wants to look up any entity by ChEMBL ID or
  drug/gene name in ChEMBL. Supports single entity or batch queries. No API key required.
---

# ChEMBL Query Skill

Query ChEMBL bioactivity database for molecules, targets, and activity data. Auto-detects input type by prefix:

| Input Pattern | Detected As | Action |
|---|---|---|
| `CHEMBL25` | ChEMBL ID (molecule) | direct fetch by ID |
| `aspirin` | drug name | substring search on `pref_name` |
| `CHEMBL203` | ChEMBL ID (target) | direct fetch by ID |
| `EGFR` | gene/protein name | substring search on `target_synonym` |

## API

| Function | Input | Returns |
|---|---|---|
| `query_molecules(entities, limit)` | `str` or `list[str]` — ChEMBL IDs or drug names | `dict[str, list[dict]]` |
| `query_targets(entities, limit)` | `str` or `list[str]` — ChEMBL IDs or gene names | `dict[str, list[dict]]` |
| `query_bioactivities(chembl_ids, limit)` | `str` or `list[str]` — molecule ChEMBL IDs | `dict[str, list[dict]]` |
| `summarize_molecule(mol)` | single molecule dict | compact one-line string |
| `summarize_activity(act)` | single activity dict | compact one-line string |
| `summarize_target(tgt)` | single target dict | compact one-line string |

## Usage

See `if __name__ == "__main__"` block in `chembl_query.py` for runnable examples covering:

1. **Single molecule by ID** — `query_molecules("CHEMBL25")`
2. **Batch molecule search by name** — `query_molecules(["ibuprofen", "metformin"], limit=3)`
3. **Bioactivities for multiple molecules** — `query_bioactivities(["CHEMBL25", "CHEMBL1642"], limit=3)`
4. **Single target by gene name** — `query_targets("EGFR", limit=3)`
5. **Batch target lookup by ID** — `query_targets(["CHEMBL203", "CHEMBL204"])`

## Key Fields

**Molecule**: `molecule_chembl_id`, `pref_name`, `molecule_properties.full_mwt`, `molecule_properties.alogp`, `molecule_properties.num_ro5_violations`

**Activity**: `molecule_chembl_id`, `target_chembl_id`, `target_pref_name`, `standard_type`, `standard_value`, `standard_units`

**Target**: `target_chembl_id`, `pref_name`, `target_type`, `organism`

## Data Source

- **API**: `https://www.ebi.ac.uk/chembl/api/data` (no key required)
- **Paper**: https://doi.org/10.1093/nar/gkad1004
