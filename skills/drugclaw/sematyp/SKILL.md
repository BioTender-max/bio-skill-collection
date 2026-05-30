# 66 · SemaTyP

> Drug-Disease Association Knowledge Graph from literature mining + TTD  
> **Category:** Drug-centric | **Type:** KG | **Subcategory:** Drug-Disease Associations  
> **Access:** Local files (downloaded from GitHub)

| Resource | URL |
|----------|-----|
| GitHub | https://github.com/ShengtianSang/SemaTyP |
| Paper | https://link.springer.com/article/10.1186/s12859-018-2167-5 |

---

## What it provides

SemaTyP combines two data sources into a knowledge graph for drug discovery / repositioning:

- **SemMedDB predications** (`data/SemmedDB/predications.txt`): subject–predicate–object triples with UMLS semantic types, extracted from PubMed abstracts (full version: ~39M triples).
- **TTD curated associations** (`data/TTD/`): drug-disease and target-disease links from Therapeutic Target Database (2016), with ICD-9/ICD-10 codes.
- **Processed associations** (`data/processed/`): pre-computed drug→disease, disease→drug, disease→target mappings.

### Data schema

| File | Format | Columns |
|------|--------|---------|
| `data/SemmedDB/predications.txt` | TSV | subject, object, context, predicate, subj_semtype, obj_semtype |
| `data/TTD/drug-disease_TTD2016.txt` | TSV | TTDDRUGID, drug_name, indication, ICD9, ICD10 |
| `data/TTD/target-disease_TTD2016.txt` | TSV | target_id, target_name, disease, ICD9, ICD10 |
| `data/processed/drug_disease` | TSV | drug, disease, ... |
| `data/processed/disease_drug` | TSV | disease, drug, ... |
| `data/processed/disease_targets` | TSV | disease, target, ... |

---

## Setup

Data must be downloaded locally first:

```bash
git clone https://github.com/ShengtianSang/SemaTyP.git
```

Then set the data path (default points to your HiPerGator location):

```python
# Option 1: environment variable
export SEMATYP_DATA_DIR="/path/to/SemaTyP-main"

# Option 2: edit DATA_DIR in 66_SemaTyP.py directly
```

**Note:** The GitHub repo only contains a 100-line sample of `predications.txt`. The full 39M-triple file must be downloaded separately per the repo README.

---

## Quick start

```python
from 66_SemaTyP import query

# Single entity (drug, disease, target, or any biomedical concept)
results = query("aspirin")

# Multiple entities
results = query(["metformin", "diabetes", "CYP2D6"])

# Specific data source only
results = query("imatinib", fields="predications", pred_limit=10)
results = query("Schizophrenia", fields="ttd")
results = query("cancer", fields="processed")
```

---

## `query()` interface

```
query(entities, fields="all", pred_limit=50) -> list[dict]
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `entities` | `str \| list[str]` | Entity name(s), case-insensitive |
| `fields` | `str` | `"all"` — everything; `"predications"` / `"ttd"` / `"processed"` |
| `pred_limit` | `int` | Max predication triples per entity (default 50) |

### Return structure (`fields="all"`)

```json
[
  {
    "query": "aspirin",
    "predications": [
      {"subject": "aspirin", "object": "pain", "predicate": "TREATS",
       "context": "...", "subj_type": "phsu", "obj_type": "sosy"}
    ],
    "predication_count": 42,
    "ttd_drug_disease": [
      {"ttdid": "DAP000XXX", "drug": "Aspirin", "disease": "Pain",
       "icd9": "...", "icd10": "..."}
    ],
    "ttd_target_disease": [],
    "processed_drug_disease": [...],
    "processed_disease_drug": [...],
    "processed_disease_targets": [...]
  }
]
```

---

## Lower-level functions

| Function | Input | Output | Description |
|----------|-------|--------|-------------|
| `get_predications(entity, limit=50)` | entity name | `list[dict]` | SemMedDB KG triples |
| `get_ttd_drug_disease(entity)` | drug or disease | `list[dict]` | TTD drug-disease associations |
| `get_ttd_target_disease(entity)` | target or disease | `list[dict]` | TTD target-disease associations |
| `get_processed_drug_disease(entity)` | entity name | `list[dict]` | Processed drug→disease |
| `get_processed_disease_drug(entity)` | entity name | `list[dict]` | Processed disease→drug |
| `get_processed_disease_targets(entity)` | entity name | `list[dict]` | Processed disease→target |

---

## Notes

- All lookups are **case-insensitive** (indexed by lowercased entity names).
- Data is **lazy-loaded**: first `query()` call triggers a one-time index build (may take seconds for large predications file).
- UMLS semantic type codes in predications: `phsu` = pharmaceutical substance, `dsyn` = disease/syndrome, `gngm` = gene/genome, `sosy` = sign/symptom, `podg` = patient/group, etc.
- The GitHub sample `predications.txt` has only 100 lines; for full coverage, download the complete file per the repo README instructions.
