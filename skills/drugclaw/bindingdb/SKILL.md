---
name: bindingdb-query
description: >
  Query the BindingDB drug-target binding affinity database. Use whenever the
  user asks about protein-ligand binding data, affinity measurements (Ki, IC50,
  Kd, EC50), or wants to look up binding partners for a UniProt ID, PDB ID,
  or compound SMILES string.
---

# BindingDB Query Skill

Search BindingDB binding affinity records by any entity. Auto-detects type by pattern:

| Input Pattern | Detected As | Example | API Endpoint |
|---|---|---|---|
| `P35355`, `Q9Y233` | UniProt ID | `P00533` (EGFR) | `getLigandsByUniprots` |
| `1Q0L`, `3ANM` | PDB ID (4-char, digit-leading) | `1Q0L` | `getLigandsByPDBs` |
| contains `=()#[]@/\` | SMILES string | `CC(=O)Oc1ccccc1C(O)=O` | `getTargetByCompound` |
| fallback | treated as UniProt | — | `getLigandsByUniprots` |

## API

| Function | Input | Returns |
|---|---|---|
| `search(entity, cutoff)` | single entity string | dict with `entity`, `type`, `hits`, `affinities` |
| `search_batch(entities, cutoff)` | list of entity strings | dict[str, search_result] |
| `summarize(result)` | search() output | compact multi-line text |
| `to_json(result)` | search() output | list[dict] of affinity records |
| `query_by_uniprot(ids, cutoff)` | UniProt ID(s), nM cutoff | list[dict] |
| `query_by_pdb(ids, cutoff, identity)` | PDB ID(s), nM cutoff, % identity | list[dict] |
| `query_by_smiles(smiles, cutoff)` | SMILES, similarity 0–1 | list[dict] |

**Parameters**

- `cutoff` (int): affinity threshold in nM (default 10 000). Entries with IC50/Ki/Kd ≤ cutoff are returned.
- `identity` (int, PDB only): sequence-identity cutoff in percent (default 92).
- Results are capped at 50 per query for LLM readability.

## Usage

See `if __name__ == "__main__"` block in `26_BindingDB.py` for runnable examples covering: UniProt single query, PDB query, SMILES compound query, batch query, and JSON output.

## Key Fields in Each Affinity Record

| Field | Description |
|---|---|
| `query` | Target protein name |
| `monomerid` | BindingDB compound ID |
| `smile` | SMILES structure of ligand |
| `affinity_type` | Ki, IC50, Kd, or EC50 |
| `affinity` | Value in nM |
| `pmid` | PubMed ID of source |
| `doi` | DOI of source publication |

## Data Source

- **Database**: BindingDB (https://www.bindingdb.org/)
- **Size**: 3.2M data points, 1.4M compounds, 11.4K targets
- **Access**: Public REST API (JSON), no authentication required
- **Citation**: BindingDB in 2024: a FAIR knowledgebase of protein-small molecule binding data. *Nucleic Acids Research*, 53(D1), D1633 (2025). DOI: 10.1093/nar/gkae1199
