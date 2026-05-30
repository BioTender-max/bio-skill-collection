---
name: molecular-targets-query
description: >
  Query the NCI CCDI Molecular Targets Platform (pediatric oncology) for
  targets (genes), diseases, drugs, and target-disease associations via
  its public GraphQL API.  Auto-detects entity type from input string.
---

# Molecular Targets Platform Query Skill

Search the CCDI Molecular Targets Platform — an NCI-supported Open Targets
instance focused on **preclinical pediatric oncology** data.  Includes FDA
Pediatric Molecular Target Lists and additional pediatric cancer datasets.

## Entity Auto-Detection

| Input Pattern | Detected As | Query Used |
|---|---|---|
| `ENSG00000141510` | Target (Ensembl gene) | `target(ensemblId)` |
| `EFO_\d+`, `MONDO_\d+`, `Orphanet_\d+`, `HP_\d+`, `DOID_\d+` | Disease / Phenotype | `disease(efoId)` |
| `CHEMBL\d+` | Drug / molecule | `drug(chemblId)` |
| anything else | Free text | `search(queryString)` |

## API

| Function | Input | Returns |
|---|---|---|
| `search(entity, size=10)` | single entity string | `dict` (GraphQL data) or `None` |
| `search_batch(entities)` | list of strings | `dict[str, dict\|None]` — uses batch GraphQL where possible |
| `get_associations(entity, size=10)` | Ensembl ID or EFO/MONDO ID | associated diseases (for target) or targets (for disease) |
| `summarize(data, entity)` | result dict + label | compact LLM-readable text |
| `to_json(data)` | result dict | `list[dict]` for pipeline output |

### Helper

| Function | Purpose |
|---|---|
| `detect_entity_type(entity)` | returns `'target'`, `'disease'`, `'drug'`, or `'search'` |

## Usage

See `if __name__ == "__main__"` block in `16_MolecularTargets.py` for runnable
examples covering:

1. Free-text search (`"neuroblastoma"`)
2. Target lookup by Ensembl ID (`"ENSG00000141510"` → TP53)
3. Disease lookup by ontology ID (`"MONDO_0005072"`)
4. Drug lookup by ChEMBL ID (`"CHEMBL941"` → imatinib)
5. Target → disease associations
6. Disease → target associations
7. Batch search (mixed entity types)
8. JSON pipeline output

## Data Source

- **Platform**: NCI CCDI Molecular Targets Platform
- **URL**: <https://moleculartargets.ccdi.cancer.gov>
- **API endpoint**: `https://moleculartargets.ccdi.cancer.gov/api/v4/graphql`
- **Method**: HTTP POST, `Content-Type: application/json`, no auth required
- **Upstream schema**: Open Targets Platform GraphQL v4
- **Focus**: Pediatric oncology — FDA Pediatric Molecular Target Lists, preclinical data

## Notes

- The API is optimised for single-entity queries.  For bulk analyses consider
  Open Targets data downloads.
- Batch functions (`search_batch`) use the plural GraphQL fields
  (`targets`, `diseases`, `drugs`) to reduce round-trips where possible;
  free-text queries fall back to one-at-a-time.
- `get_associations()` returns scored target↔disease links ranked by overall
  evidence score (0–1). Use `size` to control how many rows are returned.
- Returns `None` / `[]` on HTTP errors — callers handle no-results gracefully.
