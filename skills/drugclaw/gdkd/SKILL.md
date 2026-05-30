---
name: GDKD-query
description: >
  Query the Gene-Drug Knowledge Database (GDKD) for variant-specific
  gene–drug associations in oncology. Use when the user asks about
  cancer genomic biomarkers, drug sensitivity/resistance by gene or
  variant, targetable mutations, or clinical evidence for cancer
  therapeutics.
---

# GDKD Query Skill

Search canonical GDKD rows by drug or gene entity.
Auto-detects input type by pattern:

| Input Pattern | Detected As | Match Logic |
|---|---|---|
| `ABL1`, `EGFR` | Gene symbol | substring on `gene` |
| `imatinib`, `erlotinib` | Drug name | substring on `drug` |
| anything else | Free text | substring on `drug` OR `gene` |

## API

| Function | Input | Returns |
|---|---|---|
| `load_gdkd(path)` | CSV path | `list[dict]` |
| `search(rows, entity)` | single entity string | `list[dict]` |
| `search_batch(rows, entities)` | list of entity strings | `dict[str, list[dict]]` |
| `summarize(hits, entity)` | rows + label | compact text |
| `to_json(hits)` | rows | `list[dict]` |

## Usage

See `if __name__ == "__main__"` block in `example.py` for runnable
examples.

## Data

- **Source**: GDKD normalized full-package output
- **Paper**: Dienstmann et al., *Cancer Discovery* 2015;5(2):118-123
- **Format**: CSV
- **Columns**: `drug`, `gene`, `score`, `source`
- **Path**: `resources_metadata/dti/GDKD/gdkd.csv` (default `DATA_PATH` in `example.py`)
