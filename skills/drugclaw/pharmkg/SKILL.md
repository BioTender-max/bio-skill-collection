---
name: pharmkg-query
description: >
  Query the PharmKG knowledge graph (180k entities, 39 relation types, >1M triples).
  Use whenever the user asks about biomedical relationships among genes, drugs/chemicals,
  and diseases — e.g. drug–gene interactions, drug–disease associations, gene–disease
  links, or drug–drug relationships derived from literature and curated databases.
---

# PharmKG Query Skill

Search PharmKG triples by entity name. Matching is case-insensitive; exact match
is tried first via a prebuilt index, with substring fallback.

| Input Example | Matches On |
|---|---|
| `aspirin` | exact on Entity1\_name or Entity2\_name |
| `BRCA1` | exact / substring on entity names |
| `Alzheimer Disease` | substring on entity names |

## Entity & Relation Types

**Entities** (~188 k): Drug/Chemical (DrugBank, ChEMBL), Gene/Protein (Entrez, UniProt), Disease (DO, MeSH).

**Relations** (39 types): chemical–gene (inhibition, activation, binding …), chemical–disease (treatment, marker, risk factor), gene–disease (association, marker), chemical–chemical (similarity, interaction), and others.

## API

| Function | Input | Returns |
|---|---|---|
| `load_pharmkg(path)` | CSV path | `list[dict]` of triples |
| `_build_index(triples)` | triple list | `dict[str, list]` (entity→triples) |
| `search(triples, entity, index=)` | entity string | `list[dict]` |
| `search_batch(triples, entities, index=)` | list of strings | `dict[str, list]` |
| `summarize(hits, entity)` | hits + label | compact text |
| `to_json(hits)` | hits | JSON string |

## Usage

See `if __name__ == "__main__"` block in `55_PharmKG.py` for runnable examples
covering: single entity search, batch search, summarize, and JSON output.

## Data

- **Source**: `raw_PharmKG-180k.csv` (comma-separated)
- **Columns**: `Entity1_name`, `relationship_type`, `Entity2_name`
- **Scale**: ~188 k entities, 39 relation types, >1 M triples
- **Path**: `DATA_PATH` variable in `55_PharmKG.py`
- **Paper**: Zheng et al., *Briefings in Bioinformatics* 22(4), 2021. DOI: 10.1093/bib/bbaa344
