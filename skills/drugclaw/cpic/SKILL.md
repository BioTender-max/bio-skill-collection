# 67 · CPIC

> Clinical Pharmacogenomics Implementation Consortium — gene-based prescribing guidelines  
> **Category:** Drug-centric | **Type:** DB | **Subcategory:** Drug Knowledgebase  
> **API:** `https://api.cpicpgx.org/v1` (PostgREST, free, no key required)

| Resource | URL |
|----------|-----|
| Homepage | https://cpicpgx.org/ |
| API / Data | https://cpicpgx.org/cpic-data/ |
| Paper | https://pubmed.ncbi.nlm.nih.gov/33479744/ |

---

## What it provides

- **Drug metadata**: drugid (RxNorm), DrugBank ID, ATC codes, flowchart links
- **Guidelines**: peer-reviewed pharmacogenomics prescribing guidelines (drug + gene → dosing advice)
- **Gene-drug pairs**: curated pairs with CPIC level, PharmGKB level, PGx testing status
- **Dosing recommendations**: phenotype-specific dosing adjustments per drug-gene combination

---

## API schema note

The `pair` and `recommendation` tables use **`drugid`** (e.g. `RxNorm:32968`), not drug name.  
This script resolves drug names automatically via the `/v1/drug` table before querying.

Guideline lookup uses two strategies: (1) name substring match, (2) `guidelineid` from the drug table.  
This is necessary because some guidelines use class names (e.g. simvastatin → `"SLCO1B1, ABCG2, CYP2C9, and Statins"`, codeine → `"CYP2D6, OPRM1, COMT, and Opioids"`).

---

## Quick start

```python
from 67_CPIC import query

# Single drug
results = query("clopidogrel")

# Multiple drugs
results = query(["warfarin", "codeine"])

# Query by gene symbol
results = query("CYP2D6", fields="pairs")

# Specific fields only
results = query("codeine", fields="guidelines")
results = query("codeine", fields="recommendations")
```

---

## `query()` interface

```
query(entities, fields="all") -> list[dict]
```

| Parameter  | Type               | Description |
|------------|--------------------|-------------|
| `entities` | `str \| list[str]` | Drug name(s) or gene symbol(s) |
| `fields`   | `str`              | `"all"` — everything; `"guidelines"` / `"pairs"` / `"recommendations"` |

### Return structure (`fields="all"`)

```json
[
  {
    "query": "clopidogrel",
    "drug_info": [
      {"drugid": "RxNorm:32968", "name": "clopidogrel",
       "drugbankid": "DB00758", "atcid": ["B01AC04"], "flowchart": "..."}
    ],
    "guidelines": [
      {"name": "CYP2C19 and Clopidogrel", "url": "...", "version": 66}
    ],
    "gene_drug_pairs": [
      {"genesymbol": "CYP2C19", "drugid": "RxNorm:32968",
       "cpiclevel": "A", "clinpgxlevel": "1A",
       "pgxtesting": "Actionable PGx", "citations": ["21716271", ...]}
    ],
    "recommendations": [
      {"drugid": "RxNorm:32968",
       "phenotypes": {"CYP2C19": "Ultrarapid Metabolizer"},
       "implications": {"CYP2C19": "Increased active metabolite ..."},
       "recommendation": "Use at standard dose (75 mg/day)",
       "classification": "Strong",
       "population": "CVI ACS PCI"}
    ]
  }
]
```

On error: `{"query": "xxx", "error": "..."}`.

---

## Lower-level functions

| Function | Input | Output | Description |
|----------|-------|--------|-------------|
| `get_drug_info(drug_name)` | drug name | `list[dict]` | Drug table lookup (fuzzy) |
| `get_guidelines(drug_name=None)` | optional drug name | `list[dict]` | All or filtered guidelines |
| `get_gene_drug_pairs(drug_name=None, gene=None)` | optional filters | `list[dict]` | Gene-drug pairs (name auto-resolved to drugid) |
| `get_recommendations(drug_name)` | drug name | `list[dict]` | Dosing recommendations (name auto-resolved) |

---

## Notes

- CPIC levels: **A** = guideline published, **B** = in progress, **C/D** = lower evidence.
- Gene symbols are auto-detected (uppercase, ≤12 chars) and routed to `genesymbol` filter.
- Drug names are fuzzy-matched via `ilike` on the `/v1/drug` table.
- No rate limit documented, but keep requests reasonable.
