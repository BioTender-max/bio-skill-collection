---
name: oregano-query
description: >
  Query the OREGANO knowledge graph for computational drug repurposing.
  Use whenever the user asks about drug–target–disease–gene–pathway
  relationships, compound cross-references, drug repurposing hypotheses,
  or wants to explore neighbors of any biomedical entity in a knowledge
  graph that includes natural compounds.
---

# OREGANO Query Skill

Search the OREGANO knowledge graph (88,937 nodes, 824,231 links) by any entity. Auto-resolves input to OREGANO node IDs via cross-reference tables.

| Input Pattern | Detected As | Match Logic |
|---|---|---|
| OREGANO internal ID (e.g. `1234`) | OREGANO node ID | exact in triplet index |
| `DB00331` / DrugBank ID | external xref | exact in COMPOUND.tsv |
| UniProt / KEGG / MeSH / UMLS ID | external xref | exact across all metadata TSVs |
| `metformin`, `BRCA1`, free text | entity name | substring on name columns |

## API

| Function | Input | Returns |
|---|---|---|
| `search(query)` | single entity string | dict: `{query, resolved_ids, metadata, triplets}` |
| `search_batch(queries)` | list of entity strings | `dict[str, search_result]` |
| `summarize(result)` | search result dict | compact LLM-readable text |
| `to_json(result)` | search result dict | JSON-serializable dict |
| `get_stats()` | — | graph-level counts (triplets, nodes, predicates, entity types) |

## Graph Schema

**11 node types**: Compound (90,868), Gene (35,794), Target (22,096), Disease (18,333), Phenotype (11,605), Side Effect (6,060), Indication (2,714), Pathway (2,129), Effect (171), Activity (78).

**19 relation types** (predicates): e.g. `has_target`, `has_indication`, `has_side_effect`, `interacts_with`, `involved_in_pathway`, `associated_with`, `has_phenotype`, etc. Run `get_stats()` to list all predicates with counts.

## Usage

See `if __name__ == "__main__"` block in `21_OREGANO.py` for runnable examples covering: free-text drug name search, DrugBank ID lookup, batch search, JSON pipeline output, and graph statistics.

## Data

- **Source**: Zenodo DOI 10.5281/zenodo.10103842 (CC-BY 4.0)
- **Version**: v2.1 (published 2023-11-10)
- **Core file**: `OREGANO_V2.1.tsv` — tab-delimited triplets (Subject, Predicate, Object)
- **Metadata files**: `COMPOUND.tsv`, `TARGET.tsv`, `GENES.tsv`, `DISEASES.tsv`, `PHENOTYPES.tsv`, `PATHWAYS.tsv`, `INDICATION.tsv`, `SIDE_EFFECT.tsv`, `ACTIVITY.tsv`, `EFFECT.tsv`
- **Path**: `DATA_DIR` variable in `21_OREGANO.py`

## Citation

Boudin, M., Diallo, G., Drancé, M. & Mougin, F. The OREGANO knowledge graph for computational drug repurposing. *Sci Data* 10, 871 (2023). https://doi.org/10.1038/s41597-023-02757-0
