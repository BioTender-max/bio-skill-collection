# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#   kernelspec:
#     display_name: Pixi - Python (ipykernel)
#     language: python
#     name: python
# ---

# %% [markdown]
# # <NOTEBOOK TITLE>
#
# **Purpose (3 lines max):**
# - What question does this notebook answer?
# - What decision or artifact does it support?
# - What is “done” for this notebook?
#
# **Outputs produced:**
# - Table(s): <describe>
# - Figure(s): <describe>
# - File(s): <describe path(s) if exported>

# %% [markdown]
# ## Reproducibility
# - Kernel/environment is defined by `pixi.toml` in this directory (Pixi + pixi-kernel).
# - To re-run: **Restart Kernel & Run All**.
# - Any randomness is seeded below.

# %%
from __future__ import annotations

from pathlib import Path
import random

import numpy as np
import pandas as pd

# Optional: DuckDB for SQL analytics
import duckdb

# Plotting
import matplotlib.pyplot as plt
import matplotlib as mpl
from cycler import cycler

# %% [markdown]
# ## Configuration
# - Resolve `PROJECT_ROOT` from the nearest `pixi.toml` / `pyproject.toml` / `.git`.
# - Define `DATA_DIR` and `OUT_DIR`.
# - Set random seeds.

# %%
def find_project_root(start: Path | None = None) -> Path:
    start = (start or Path.cwd()).resolve()
    markers = {"pixi.toml", "pyproject.toml", ".git"}
    for p in [start, *start.parents]:
        if any((p / m).exists() for m in markers):
            return p
    return start

PROJECT_ROOT = find_project_root()
DATA_DIR = PROJECT_ROOT / "data"
OUT_DIR = PROJECT_ROOT / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SEED = 7
random.seed(SEED)
np.random.seed(SEED)

print("PROJECT_ROOT:", PROJECT_ROOT)
print("DATA_DIR:", DATA_DIR)
print("OUT_DIR:", OUT_DIR)

# %% [markdown]
# ## Plot styling
# - Apply a compact style with minimal whitespace.
# - Use a cohesive, non-default palette.

# %%
PALETTE = ["#0B1320", "#2C7DA0", "#5C4D7D", "#F1C453", "#E85D75", "#43AA8B"]

def set_plot_style() -> None:
    mpl.rcParams.update({
        "figure.dpi": 120,
        "savefig.dpi": 200,
        "figure.figsize": (8, 4.5),
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": cycler(color=PALETTE),
        "figure.constrained_layout.use": True,
    })

set_plot_style()

# %% [markdown]
# ## Data
# Describe your data sources:
# - Files: `data/raw/...` (TSV/CSV/Parquet)
# - Database: `data/analytics.duckdb` (or in-memory)
#
# Document:
# - refresh cadence
# - key columns
# - expected row counts / ranges

# %% [markdown]
# ## Load data
# - Load raw files using paths anchored to `DATA_DIR`.
# - Fail fast if files are missing.
# - Show a compact preview and shape.

# %%
# Example TSV (replace with your actual file)
raw_path = DATA_DIR / "raw" / "events.tsv"
if raw_path.exists():
    events = pd.read_csv(raw_path, sep="\t")
    display(events.head())
    print("events shape:", events.shape)
else:
    print("Missing example file:", raw_path)

# %% [markdown]
# ## DuckDB bootstrap (optional)
# - Connect to a file-backed DuckDB (recommended for repeatability) or use `:memory:`.
# - Use absolute paths when passing file paths into DuckDB.

# %%
db_path = DATA_DIR / "analytics.duckdb"
con = duckdb.connect(str(db_path))
con.execute("SELECT 1 AS ok").df()

# %% [markdown]
# ## Validate data
# - Check missingness and key uniqueness.
# - Confirm assumptions before analysis.

# %%
def null_rate(df: pd.DataFrame) -> pd.Series:
    return df.isna().mean().sort_values(ascending=False)

if "events" in globals():
    display(null_rate(events).head(10))

# %% [markdown]
# ## Analysis
# - Keep steps small and linear.
# - Each code cell should do one thing.

# %%
# TODO: analysis code here

# %% [markdown]
# ## Results
# - Present final tables/figures.
# - Export any artifacts to `OUT_DIR`.

# %%
# Example placeholder plot
if "events" in globals() and len(events.columns) > 0:
    fig, ax = plt.subplots(figsize=(7.5, 4.0))
    events.iloc[:, 0].value_counts().head(20).plot(kind="bar", ax=ax)
    ax.set_title("Top values (first column)")
    ax.set_xlabel(events.columns[0])
    ax.set_ylabel("count")
    fig.savefig(OUT_DIR / "top_values.png", bbox_inches="tight", pad_inches=0.05)

# %% [markdown]
# ## Conclusions & next steps
# - Summarize what you found (3–6 bullets).
# - List concrete next actions.
