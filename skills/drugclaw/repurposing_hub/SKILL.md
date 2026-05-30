---
name: Drug-Repurposing-Hub
description: >
  Query the Broad Institute Drug Repurposing Hub (~6,800 compounds).
  Look up drugs by name, gene target, MOA, disease area, Broad ID,
  or InChIKey.  Returns clinical phase, mechanism of action, targets,
  disease area, indication, and chemical identifiers.
---

# Drug Repurposing Hub Query Skill

Search the Broad Institute Drug Repurposing Hub by any entity.
Auto-detects input type by pattern:

| Input Pattern | Detected As | Match Logic |
|---|---|---|
| `BRD-A12345678` | Broad compound ID | prefix on `broad_id` |
| `ABCDEFGHIJKLMN-OPQRSTUVWX-Y` | InChIKey | exact on `InChIKey` |
| `EGFR`, `BRAF`, `TOP1` | Gene / target | exact token in `target` (pipe-separated) |
| anything else | free text | substring on `pert_iname`, `moa`, `indication`, `disease_area` |

## API

| Function | Input | Returns |
|---|---|---|
| `load_drugs(path)` | drug TSV path | list[dict] |
| `load_samples(path)` | sample TSV path | list[dict] |
| `load_merged()` | — | list[dict] (drugs + chemical IDs from samples) |
| `search(entity)` | single entity string | list[dict] |
| `search_batch(entities)` | list of entity strings | dict[str, list[dict]] |
| `summarize(hits, entity)` | hits + label | compact LLM-readable text |
| `to_json(hits)` | list[dict] | list[dict] (JSON-serialisable) |

## Usage

See `if __name__ == "__main__"` block in `29_Drug_Repurposing_Hub.py` for
runnable examples covering: drug name, gene target, MOA keyword, disease
area, batch search, and JSON output.

```python
from importlib.machinery import SourceFileLoader
hub = SourceFileLoader("hub", "29_Drug_Repurposing_Hub.py").load_module()

# Single drug lookup
hits = hub.search("imatinib")
print(hub.summarize(hits, "imatinib"))

# Target-based search
hits = hub.search("EGFR")

# Batch
results = hub.search_batch(["metformin", "aspirin", "BRAF"])
```

## Data

- **Source**: Broad Institute Drug Repurposing Hub (https://repo-hub.broadinstitute.org/repurposing)
- **Drug file**: `repo-drug-annotation-20200324.txt` — tab-delimited, `!`-prefixed comment lines
  - Columns: `pert_iname`, `clinical_phase`, `moa`, `target`, `disease_area`, `indication`
- **Sample file**: `repo-sample-annotation-20240610.txt` — tab-delimited, `!`-prefixed comment lines
  - Columns include: `broad_id`, `pert_iname`, `InChIKey`, `pubchem_cid`, `smiles`, `vendor`, `purity`, etc.
- **Merge**: on `pert_iname`; first sample with non-empty `InChIKey` is kept per drug
- **Path**: `DATA_DIR` variable in `29_Drug_Repurposing_Hub.py`
- **Citation**: Corsello SM et al. *Nature Medicine* 23, 405–408 (2017). doi:10.1038/nm.4306
