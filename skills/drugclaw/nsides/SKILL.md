---
name: nsides-query
description: >
  Query the nSIDES drug side effect databases (OnSIDES, OffSIDES, KidSIDES).
  Use whenever the user asks about drug adverse reactions, side effects,
  off-label safety signals, or pediatric drug safety for a given drug name.
---

# nSIDES Query Skill

Search drug adverse reactions across three complementary nSIDES sources by drug name.

| Source | Content | Method | Scale |
|---|---|---|---|
| **OnSIDES** v3.1.0 | Label-extracted ADEs (US/EU/UK/JP) | PubMedBERT NLP on product labels | 1,955 ingredients, 5.5M drug-ADE pairs |
| **OffSIDES** | Off-label side effects | Propensity-score matching on FAERS | 3,300+ drugs |
| **KidSIDES** | Pediatric safety signals by developmental phase | Disproportionality analysis on FAERS | Age-stratified ADE signals |

## Entity Detection

| Input | Routing |
|---|---|
| any free text | substring match on drug / ingredient name across all three sources |

No ID-based routing — all queries are natural-language drug names.

## API

| Function | Input | Returns |
|---|---|---|
| `search(entity, limit)` | drug name string | `dict` with keys: `entity`, `onsides`, `offsides`, `kidsides` |
| `search_batch(entities, limit)` | list of drug names | `list[dict]` |
| `search_onsides(drug_name, limit)` | drug name | `list[dict]` — ingredient, effect, meddra_id, source, label_count |
| `search_offsides(drug_name, limit)` | drug name | `list[dict]` — drug, condition, PRR, A/B/C/D |
| `search_kidsides(drug_name, limit)` | drug name | `list[dict]` — drug, event, nichd_phase, gam_score, ror |
| `summarize(result)` | single `search()` output | compact text |
| `to_json(result)` | single `search()` output | JSON string |

## Output Fields

### OnSIDES row
- `ingredient` — RxNorm ingredient name
- `effect` — MedDRA adverse effect term
- `meddra_id` — MedDRA concept ID
- `source` — label origin country (US / EU / UK / JP)
- `label_count` — number of labels reporting this ADE

### OffSIDES row
- `drug` — RxNorm drug name
- `condition` — MedDRA side effect name
- `PRR` — proportional reporting ratio (>1 = signal)
- `A/B/C/D` — 2×2 contingency counts
- `mean_reporting_frequency` — proportion of drug reports with this effect

### KidSIDES row
- `drug` — drug concept name
- `event` — adverse event name
- `nichd_phase` — NICHD developmental phase (e.g. "Neonatal", "Infancy", "Adolescence")
- `gam_score` — GAM model score
- `ror` / `ror_lower` / `ror_upper` — reporting odds ratio with 95% CI

## Usage

See `if __name__ == "__main__"` block in `15_nSIDES.py` for runnable examples:
single-drug query, batch query, text summary, and JSON output.

## Data

| File | Location | Size |
|---|---|---|
| `onsides.db` | `DATA_DIR/onsides.db` | SQLite, from OnSIDES v3.1.0 release |
| `OFFSIDES.csv.gz` | `DATA_DIR/OFFSIDES.csv.gz` | gzipped CSV |
| `ade_nichd.csv.gz` | `DATA_DIR/ade_nichd.csv.gz` | gzipped CSV (172 MB) |
| `drug.csv.gz` | `DATA_DIR/drug.csv.gz` | KidSIDES drug dictionary |
| `event.csv.gz` | `DATA_DIR/event.csv.gz` | KidSIDES event dictionary |
| `dictionary.csv.gz` | `DATA_DIR/dictionary.csv.gz` | NICHD phase dictionary |

`DATA_DIR` default: `resources_metadata/adr/nSIDES`

## Citations

- **OnSIDES**: Tanaka Y et al. OnSIDES database: Extracting adverse drug events from drug labels using NLP models. *Med*. 2025;100642. doi:10.1016/j.medj.2025.100642
- **OffSIDES / TwoSIDES**: Tatonetti NP et al. Data-driven prediction of drug effects and interactions. *Sci Transl Med*. 2012;4(125):125ra31. doi:10.1126/scitranslmed.3003377
- **KidSIDES**: Giangreco NP, Tatonetti NP. A database of pediatric drug effects to evaluate ontogenic mechanisms. *Med*. 2022.
