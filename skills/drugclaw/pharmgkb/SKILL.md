---
name: pharmgkb-clinpgx
description: >
  Query ClinPGx (PharmGKB) and CPIC for pharmacogenomics data. Use whenever
  the user asks about gene-drug interactions, pharmacogenomics clinical
  annotations, drug-metabolizing enzymes, CPIC guidelines, or variant-level
  PGx evidence for any gene symbol, drug name, rsID, or ClinPGx accession.
---

# PharmGKB / ClinPGx Query Skill

Queries two complementary APIs:

- **ClinPGx API** (`api.clinpgx.org/v1`) — gene, chemical, variant detail
- **CPIC API** (`api.cpicpgx.org/v1`) — gene-drug pairs, CPIC guideline levels (PostgREST)

Auto-detects input entity type by pattern:

| Input Pattern | Detected As | Data Sources |
|---|---|---|
| `PA128` | ClinPGx accession | gene or chemical detail + CPIC pairs |
| `rs4244285` | dbSNP rsID | variant lookup |
| `CYP2D6` | gene symbol (uppercase, 2-15 chars) | gene detail + CPIC pairs |
| anything else | drug / free text | chemical detail + CPIC pairs |

## API

| Function | Input | Returns |
|---|---|---|
| `search(entity)` | single entity string | dict with `genes`, `chemicals`, `variants`, `cpic_pairs`, `related` |
| `search_batch(entities)` | list of entity strings | dict[str → search result] |
| `summarize(result, entity)` | search result + label | compact text (one line per hit) |
| `to_json(result)` | search result | indented JSON string |
| `search_gene(symbol)` | gene symbol | list of gene dicts (ClinPGx) |
| `search_drug(name)` | drug name | list of chemical dicts (ClinPGx) |
| `search_variant(rsid)` | rsID string | list of variant dicts (ClinPGx) |
| `get_cpic_pairs_by_gene(symbol)` | gene symbol | list of pair dicts (CPIC `pair_view`) |
| `get_cpic_pairs_by_drug(name)` | drug name | list of pair dicts (CPIC `pair_view`) |

## Usage

See `if __name__ == "__main__"` block in `49_PHARMGKB_CLINPGX.py` for runnable
examples covering: gene symbol, drug name, rsID, ClinPGx accession, batch
search, and JSON output.

## Key Fields

**Gene** (ClinPGx): `id`, `symbol`, `name`, `hasCpicGuideline`

**Chemical** (ClinPGx): `id`, `name`, `types`

**Variant** (ClinPGx): `id`, `symbol`, `genes`, `location`

**CPIC Pair** (`pair_view`): `genesymbol`, `drugname`, `cpiclevel` (A/B/C/D),
`clinpgxlevel` (evidence), `pgxtesting`, `guidelinename`

## Data Sources

- **ClinPGx** (Stanford / NIH) — https://www.clinpgx.org/ — REST JSON, no key, ≤2 req/s, CC BY-SA 4.0
- **CPIC API** — https://api.cpicpgx.org/ — PostgREST, no key — gene-drug guideline pairs
- **Note**: PharmGKB was subsumed by ClinPGx (July 2025). CPIC API remains at `api.cpicpgx.org`.
