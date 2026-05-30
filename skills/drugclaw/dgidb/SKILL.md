---
name: 16_DGIdb
description: >
  Query the DGIdb (Drug-Gene Interaction Database) for drug-gene interactions,
  gene druggability categories, and drug target information. Use whenever the
  user asks about drug targets, druggable genes, gene-drug interactions, or
  wants to look up any entity (gene name, drug name, druggability category)
  in DGIdb.
---

# DGIdb Query Skill

Search DGIdb records by any entity. Auto-detects type by naming convention:

| Input Pattern | Detected As | Example |
|---|---|---|
| ALL-CAPS ≤15 chars | Gene | `EGFR`, `BRAF`, `TP53` |
| Known category keyword | Druggability category | `clinically actionable`, `kinase` |
| Anything else | Drug | `imatinib`, `erlotinib` |

Supported category keywords: `clinically actionable`, `drug resistance`, `druggable genome`, `tumor suppressor`, `transcription factor`, `kinase`, `g protein coupled receptor`, `hormone activity`, `ion channel`, `protease`, `dna repair`.

## API

| Function | Input | Returns |
|---|---|---|
| `search(entity)` | single entity string | `list[dict]` |
| `search_batch(entities)` | list of entity strings | `dict[str, list[dict]]` |
| `summarize(results, entity)` | result list + label | compact text for LLM |
| `to_json(results)` | result list | `list[dict]` (passthrough) |

## Key Fields

**Gene result**: `name`, `long_name`, `categories`, `interaction_count`, `interactions[]` (each with `drug`, `drug_concept_id`, `score`, `types`, `directionality`, `attributes`, `pmids`, `sources`).

**Drug result**: `name`, `concept_id`, `approval_ratings`, `interaction_count`, `interactions[]` (each with `gene`, `gene_long_name`, `score`, `types`, `directionality`, `attributes`, `pmids`, `sources`).

**Category result**: `category`, `gene_count`, `genes[]` (each with `name`, `long_name`).

## Usage

See `if __name__ == "__main__"` block in `16_DGIdb.py` for runnable examples covering: single gene, single drug, category, batch (mixed types), and JSON output.

## Data Source

- **Database**: DGIdb v5.0 — Drug-Gene Interaction Database
- **Endpoint**: `https://dgidb.org/api/graphql` (GraphQL, no API key)
- **Coverage**: 40+ source databases, ~100 k drug-gene interactions
- **Paper**: Freshour et al., *Nucleic Acids Res.* 2024; 52(D1):D1227-D1235. DOI: [10.1093/nar/gkac1046](https://doi.org/10.1093/nar/gkac1046)
