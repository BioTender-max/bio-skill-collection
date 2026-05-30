---
name: NCI-DTP-MolTarget
description: >
  Query the NCI-60 Molecular Target (Protein) database from the Developmental
  Therapeutics Program. Use when the user asks about protein expression of drug
  targets across the NCI-60 cancer cell line panel, or wants to look up a gene,
  cell line, or cancer panel in the NCI DTP molecular target dataset.
---

# NCI DTP Molecular Target Query Skill

Search NCI-60 protein-level molecular target data by any entity. Auto-detects type:

| Input Pattern | Detected As | Match Logic |
|---|---|---|
| `EGFR`, `TP53` | gene / protein | exact on `GENE` or substring on `ENTITY_MEASURED`, `TITLE` |
| `MCF7`, `NCI-H460` | cell line | substring on `cellname` |
| `Breast`, `Leukemia` | cancer panel | substring on `pname` |
| `12345` (pure digits) | MOLTID | exact on `MOLTID` (NCI pattern #) |

## Drug-Relevance Guide

Only **protein expression data** is downloaded — proteins are the direct molecular
targets of drugs (kinase inhibitors → kinase expression, antibodies → receptor levels).

| Dataset | Download? | Reason |
|---|---|---|
| **WEB_DATA_PROTEIN.ZIP** | **YES** | Drug targets: protein expression across NCI-60 |
| WEB_DATA_ALL_MT.ZIP | Optional | Superset incl. enzyme activity (also drug-relevant) |
| WEB_DATA_DNA.ZIP | No | Genomic characterisation, not drug targets |
| WEB_DATA_SEQUENOM_METHYLATION.ZIP | No | Epigenetic; indirect |
| WEB_DATA_*_MIR.ZIP | No | microRNA regulation; indirect |
| WEB_DATA_METABOLON*.ZIP | No | Metabolomics; downstream, indirect |
| Microarray / SNP / CopyNum / Karyotype | No | Cell-line genomic profiling; indirect |

## API

| Function | Input | Returns |
|---|---|---|
| `load_data(path)` | file or directory path | `list[dict]` |
| `search(data, entity)` | data + single entity string | `list[dict]` |
| `search_batch(data, entities)` | data + list of entity strings | `dict[str, list[dict]]` |
| `summarize(hits, entity)` | hit list + label | compact LLM-readable text |
| `to_json(hits)` | hit list | `list[dict]` (JSON-serialisable) |
| `query(data, entities, top_n)` | data + str or list | text block |

## Record Fields

Each record contains:

| Field | Description |
|---|---|
| `MOLTID` | NCI pattern number (molecular target ID) |
| `GENE` | Gene symbol |
| `TITLE` | Gene / protein full name |
| `MOLTNBR` | NCI experiment ID |
| `PANELNBR` / `CELLNBR` | Internal panel / cell identifiers |
| `pname` | Cancer panel name (e.g., Breast, Leukemia) |
| `cellname` | Cell line name (e.g., MCF7, A549/ATCC) |
| `ENTITY_MEASURED` | What was measured (e.g., protein name) |
| `GeneID` | NCBI Gene ID |
| `UNITS` | Measurement units |
| `METHOD` | Assay method |
| `VALUE` | Numeric measurement value |
| `TEXT` | Additional notes |

## Usage

See `if __name__ == "__main__"` block in `16_NCI_DTP_MolTarget.py` for runnable
examples covering: single gene query, cell line profile, batch multi-target
search, cancer panel query, and JSON output.

## Quick Examples

```python
from importlib.machinery import SourceFileLoader
mt = SourceFileLoader("mt", "16_NCI_DTP_MolTarget.py").load_module()

data = mt.load_data()

# Single drug target
print(mt.query(data, "EGFR"))

# Multiple targets
print(mt.query(data, ["TP53", "BRAF", "HER2"]))

# Cell line molecular profile
print(mt.query(data, "MCF7"))

# JSON for downstream pipeline
import json
hits = mt.search(data, "EGFR")
print(json.dumps(mt.to_json(hits[:5]), indent=2))
```

## Data Source & Download

- **Provider**: NCI Developmental Therapeutics Program (DTP)
- **URL**: https://wiki.nci.nih.gov/spaces/NCIDTPdata/pages/155845004/Molecular+Target+Data
- **File**: `WEB_DATA_PROTEIN.TXT` (headerless CSV, comma-delimited)
- **Local Path**: `resources_metadata/dti/Molecular Target Data/WEB_DATA_PROTEIN.TXT`
- **Format**: comma-delimited, 14 columns (see Record Fields above)
- **Auth**: None (public domain, U.S. government)

### Download Commands

```bash
# File already at:
# resources_metadata/dti/Molecular Target Data/WEB_DATA_PROTEIN.TXT
```
