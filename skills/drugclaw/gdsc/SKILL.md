# 60_GDSC_GDSC2 — Genomics of Drug Sensitivity in Cancer

## Overview

| Field | Value |
|---|---|
| Category | Drug-centric |
| Subcategory | Drug Molecular Property |
| Source | Sanger / Wellcome Trust |
| Datasets | **screened_compounds** (drug list), **GDSC1/GDSC2** (dose-response), **Cell Model Passports** (cell-line annotations) |
| URL | <https://www.cancerrxgene.org/> |
| Cell Models | <https://cellmodelpassports.sanger.ac.uk/downloads> |

GDSC contains pharmacological profiles for ~500 drugs tested in ~1,000 cancer cell lines. Queryable entities include drug names, gene targets, pathways, and cell-line identifiers.

## File Layout

```
DATA_DIR/
  ├── screened_compounds_rel_8.4.csv           # drug list (~100 KB)
  ├── GDSC1_fitted_dose_response_27Oct23.xlsx  # GDSC1 IC50/AUC (~80 MB, optional)
  └── GDSC2_fitted_dose_response_27Oct23.xlsx  # GDSC2 IC50/AUC (~50 MB, optional)
```

Default `DATA_DIR`:
```
resources_metadata/drug_molecular_property/GDSC
```

Override via environment variable: `export GDSC_DATA_DIR=/your/path`

## Dependencies

```bash
conda install openpyxl   # or: pip install openpyxl
```

## Download & Query

The script auto-downloads all data files (drug list CSV + GDSC1/GDSC2 dose-response XLSX) on first run if the data directory is empty.

### CLI

```bash
# First run: auto-downloads all files, then queries default examples (Erlotinib, Nutlin, A549)
python 60_GDSC_GDSC2.py
```

If auto-download fails (e.g. no internet on HPC compute node), download manually from the repository root:

```bash
cd resources_metadata/drug_molecular_property/GDSC
wget 'https://ftp.sanger.ac.uk/pub/project/cancerrxgene/releases/current_release/screened_compounds_rel_8.4.csv'
wget 'https://cog.sanger.ac.uk/cancerrxgene/GDSC_data_8.5/GDSC1_fitted_dose_response_27Oct23.xlsx'
wget 'https://cog.sanger.ac.uk/cancerrxgene/GDSC_data_8.5/GDSC2_fitted_dose_response_27Oct23.xlsx'
```

### Python API

```python
from importlib.machinery import SourceFileLoader
mod = SourceFileLoader("gdsc", "60_GDSC_GDSC2.py").load_module()

# Single entity
results = mod.query_gdsc("Erlotinib")

# Multiple entities
results = mod.query_gdsc(["Nutlin", "A549", "EGFR"])

# Optional: manually trigger download
mod.download_gdsc_data()
```

### Return Format

```json
[
  {
    "source": "screened_compounds_rel_8.4.csv",
    "match_count": 1,
    "matches": [
      {
        "DRUG_NAME": "Erlotinib",
        "TARGET": "EGFR",
        "TARGET_PATHWAY": "EGFR signaling",
        "PUBCHEM_ID": "176870",
        "...": "..."
      }
    ]
  }
]
```

- Returns an empty list when no matches are found.
- Returns `{"error": "..."}` if the data directory is missing or empty.

### LLM Integration Example

```text
User:  "What is the target of Erlotinib in GDSC?"
Agent: calls query_gdsc("Erlotinib")
       → source: screened_compounds_rel_8.4.csv, TARGET: EGFR, PATHWAY: EGFR signaling
       → "Erlotinib targets EGFR (EGFR signaling pathway) according to GDSC."
```
