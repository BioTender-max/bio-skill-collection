# SIDER - Side Effect Resource

**Category:** Drug-centric | **Type:** DB | **Subcategory:** Adverse Drug Reaction (ADR)  
**Link:** http://sideeffects.embl.de/ | **Paper:** https://doi.org/10.1093/nar/gkv1075

SIDER contains marketed medicines and their recorded adverse drug reactions, mined from public documents and package inserts.

## Entity Type Auto-Detection

| Input Pattern | Detected As | Example |
|---|---|---|
| `CIDxxxxxxxxx` | STITCH ID | `CID100000085` |
| `Cxxxxxxx` (8-char, digits after C) | UMLS CUI | `C0011849` |
| `X##XX##` (7-char ATC pattern) | ATC code | `N05BA01` |
| anything else | free text | `aspirin`, `headache` |

Free text first attempts exact/substring match on drug names; if no drug is matched, it searches side-effect and indication names.

## API

| Function | Input | Returns |
|---|---|---|
| `search(entity)` | single entity string | `dict` with drug_name, stitch_ids, atc_codes, side_effects, indications, freq |
| `search_batch(entities)` | list of entity strings | `dict[str, dict]` |
| `summarize(result)` | one result dict | compact text string |
| `to_json(result)` | one result dict | same dict (pipeline passthrough) |

## Usage

```python
from 14_SIDER import search, search_batch, summarize

# Single query — drug name
result = search("aspirin")
print(summarize(result))

# Single query — STITCH ID
result = search("CID100000085")
print(summarize(result))

# Single query — side-effect text
result = search("headache")
print(summarize(result))

# Batch query — mixed entity types
results = search_batch(["metformin", "ibuprofen", "C0011849"])
for entity, r in results.items():
    print(summarize(r))
```

## Data Files

All pre-downloaded and extracted under:  
`resources_metadata/adr/SIDER`

| File | Content |
|---|---|
| `drug_names.tsv` | STITCH flat ID → drug name |
| `drug_atc.tsv` | STITCH flat ID → ATC code |
| `meddra_all_se.tsv` | All side effects (STITCH, UMLS, MedDRA type, SE name) |
| `meddra_all_indications.tsv` | All indications (STITCH, UMLS, method, MedDRA name) |
| `meddra_freq.tsv` | Side effects with frequency info |

The loader auto-detects `.tsv` / `.tsv.gz` variants. Results are capped at 50 records per category for readability.
