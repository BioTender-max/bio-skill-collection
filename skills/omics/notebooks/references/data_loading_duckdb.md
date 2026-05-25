# Data loading patterns (DuckDB + TSV/Parquet)

## Directory conventions
Recommended project layout:

```
project/
  pixi.toml
  notebooks/
    01_analysis.ipynb
  data/
    raw/
      events.tsv
    processed/
      features.parquet
    analytics.duckdb
```

The notebook should treat the **project root** as the anchor for all paths.

## Project root detection (robust)
In a notebook, `Path.cwd()` depends on how Jupyter was launched. Prefer a small helper that searches upward for `pixi.toml` (or `.git`) and uses that as the root.

```python
from pathlib import Path

def find_project_root(start: Path | None = None) -> Path:
    start = (start or Path.cwd()).resolve()
    markers = {"pixi.toml", "pyproject.toml", ".git"}
    for p in [start, *start.parents]:
        if any((p / m).exists() for m in markers):
            return p
    return start

PROJECT_ROOT = find_project_root()
DATA_DIR = PROJECT_ROOT / "data"
```

Always display the resolved root early:
```python
print("PROJECT_ROOT:", PROJECT_ROOT)
```

## File existence checks (fail fast)
Before loading:

```python
path = DATA_DIR / "raw" / "events.tsv"
assert path.exists(), f"Missing file: {path}"
```

## TSV/CSV loading (pandas)
```python
import pandas as pd

events = pd.read_csv(DATA_DIR / "raw" / "events.tsv", sep="\t")
```

## DuckDB: connect + read files safely
Use DuckDB for heavy SQL and to avoid loading giant datasets into RAM.

```python
import duckdb

DB_PATH = DATA_DIR / "analytics.duckdb"
con = duckdb.connect(str(DB_PATH))
```

### Important: absolute paths for DuckDB file reads
To avoid working-directory surprises, pass **absolute** paths into DuckDB:

```python
events_path = (DATA_DIR / "raw" / "events.tsv").resolve()
con.execute(
    "CREATE OR REPLACE TABLE events AS SELECT * FROM read_csv_auto(?);",
    [str(events_path)],
)
```

Same idea for Parquet:

```python
parquet_path = (DATA_DIR / "processed" / "features.parquet").resolve()
df = con.execute("SELECT * FROM read_parquet(?) LIMIT 100;", [str(parquet_path)]).df()
```

## Minimal validation checks (always include)
After loading data, include a small “sanity” cell:
- shape / row count
- missingness
- key uniqueness

Example:

```python
print("events rows:", len(events))
print(events.isna().mean().sort_values(ascending=False).head(10))
```

## Keep SQL readable
- Put long SQL in triple-quoted strings.
- Use CTEs.
- Name intermediate tables/views.

If SQL grows big, move it to `.sql` files (see `templates/duckdb_bootstrap.sql`).
