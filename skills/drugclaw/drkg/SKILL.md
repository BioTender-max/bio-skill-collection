---
name: drkg-query
description: >
  Query the DRKG (Drug Repurposing Knowledge Graph). Use whenever the user asks
  about drug–gene, drug–disease, gene–disease, or other biomedical entity
  relationships in a knowledge-graph context, drug repurposing candidates,
  COVID-19 drug repurposing, or wants to explore neighbours of any biomedical
  entity (compound, gene, disease, pathway, side effect, etc.) in DRKG.
---

# DRKG Query Skill

Search the Drug Repurposing Knowledge Graph (97 238 entities, 5 874 261
triplets, 107 relation types) by any entity. Auto-detects entity type by
input pattern and returns all KG neighbours.

## Entity Format

Entities in DRKG are typed strings: `Type::ID`.

| Entity Type | Example | Count |
|---|---|---|
| Compound | `Compound::DB00945` | 24 313 |
| Gene | `Gene::1956` | 39 220 |
| Disease | `Disease::DOID:162` | 5 103 |
| Anatomy | `Anatomy::UBERON:0001474` | 400 |
| Biological Process | `Biological Process::GO:0006915` | 11 381 |
| Cellular Component | `Cellular Component::GO:0005634` | 1 391 |
| Molecular Function | `Molecular Function::GO:0005515` | 2 884 |
| Pathway | `Pathway::PC7_8078` | 1 822 |
| Pharmacologic Class | `Pharmacologic Class::N0000175605` | 345 |
| Side Effect | `Side Effect::C0000737` | 5 701 |
| Symptom | `Symptom::D009325` | 415 |
| Atc | `Atc::N02BE01` | 4 048 |
| Tax | `Tax::9606` | 215 |

Relations are typed strings: `Source::RelType::HeadType:TailType`, e.g.
`DRUGBANK::target::Compound:Gene`, `Hetionet::CtD::Compound:Disease`.

## Input Auto-Detection

| Input Pattern | Detected As | Match Logic |
|---|---|---|
| `Compound::DB00945` | full DRKG entity | exact match |
| `DB\d{5,}` | DrugBank ID | prepend `Compound::` |
| `DOID:\d+` / `MESH:D\d+` | Disease ID | prepend `Disease::` |
| `GO:\d+` | GO term | try BP / MF / CC |
| pure digits (`1956`) | Entrez Gene ID | prepend `Gene::` |
| anything else | free text | case-insensitive substring across all entities |

## API

| Function | Input | Returns |
|---|---|---|
| `search(query, limit=200)` | single entity string | dict with `resolved`, `as_head`, `as_tail` |
| `search_batch(queries, limit=200)` | list of entity strings | dict[query → result] |
| `get_sources(entity)` | resolved DRKG entity | source attribution string |
| `get_relation_info(relation)` | relation string | glossary dict |
| `entity_types()` | — | list of 13 entity type names |
| `summarize(result)` | search result dict | compact LLM-readable text |
| `to_json(result)` | search result dict | JSON-serialisable dict |

## Usage

See `if __name__ == "__main__"` block in `25_DRKG.py` for runnable examples:
single-entity search (full ID, bare ID, free text), batch search, relation
glossary lookup, and JSON output.

## Data Sources

DRKG integrates six databases plus COVID-19 literature:

| Source | Triplets | Coverage |
|---|---|---|
| DrugBank | 1 424 790 | drug–drug, drug–gene, drug–disease, ATC |
| Hetionet | 2 250 197 | gene–gene, anatomy, pathways, side effects |
| GNBR | 335 369 | gene–gene, compound–gene, disease–gene |
| STRING | 1 496 708 | protein–protein interactions |
| IntAct | 256 151 | protein–protein interactions |
| DGIdb | 26 290 | drug–gene interactions |
| Bibliography | 84 756 | COVID-19 related |

## Data Files

Located at `DATA_DIR` in `25_DRKG.py`:

| File | Description |
|---|---|
| `drkg.tsv` | 5 874 261 triplets (head, relation, tail) |
| `relation_glossary.tsv` | relation type glossary with source info |
| `entity2src.tsv` | entity → original data-source mapping |

## Citation

```
Ioannidis et al. "DRKG - Drug Repurposing Knowledge Graph for Covid-19", 2020.
https://github.com/gnn4dr/DRKG
```
