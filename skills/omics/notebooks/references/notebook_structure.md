# Notebook structure and markdown style

## KISS principles for notebooks
A notebook should read like a short technical memo:
- **One notebook = one goal.** If it has two unrelated goals, split it.
- **Linear execution.** Cells must run top → bottom on a fresh kernel.
- **Small cells.** Prefer many small, named steps over one huge cell.
- **Minimal global state.** Keep “configuration” in one early cell; avoid mutating globals later.

> If a notebook can’t be reliably “Restart & Run All”, it is not done.

## Mandatory section order (default)
Use this as the default outline unless the user requests otherwise.

1. **Title**
2. **Purpose (3 lines max)**
3. **What this notebook will produce** (artifacts/figures/tables)
4. **Environment / Reproducibility notes**
   - kernel / pixi manifest location
   - how to rerun end-to-end
5. **Data**
   - sources (files, DBs, APIs), ownership, refresh cadence
   - schema expectations + keys
6. **Load & validate data**
7. **Analysis / EDA / Modeling**
8. **Results**
9. **Conclusions + next steps**

## Markdown above every code cell (hard rule)
Every code cell must be preceded by a markdown cell that answers:
- **What is this cell doing?** (1 sentence)
- **Why does it matter?** (1 sentence)
- **What should I see?** (1 bullet: shape, table, plot, file)

### Example pattern
Markdown cell:

- Load the raw TSV into a DataFrame (no transformations yet).
- Sanity-check row count and column names.
- Expected: a `(rows, cols)` printout and `df.head()`.

Code cell:
```python
df = pd.read_csv(DATA_DIR / "events.tsv", sep="\t")
display(df.head())
print(df.shape)
```

## Notebook voice and formatting
- Use **short headings** and **bulleted lists**.
- Prefer **imperative verbs** (“Load…”, “Validate…”, “Plot…”, “Export…”).
- Avoid long essays; markdown should guide, not drown.

### “Beautiful markdown” checklist
- Use consistent heading hierarchy (`#`, `##`, `###`).
- Use short paragraphs + bullets.
- Use callouts sparingly (e.g., `> Note:`).
- Never leave a code cell without a preceding markdown cell.
- In marimo `.py` notebooks, write markdown as one clean `mo.md(r"""...""")` block. Do not leave stray quoted-string fragments inside markdown text.
- Remove trailing empty cells and placeholder cells before final verification.

## Cell sizing limits (recommended)
- Target **≤ 25 lines** per code cell.
- If a cell grows, extract helpers into functions or modules.
- Prefer functions with docstrings for multi-step logic.

## Output discipline
- Print/display only what’s useful.
- For wide tables, show `df.head(10)` or select columns.
- For EDA summaries, show 1–2 compact tables, not 10.

## Randomness & determinism
If the notebook includes any stochastic step:
- set a seed (`numpy`, Python `random`, ML framework),
- state it in markdown and in a config cell.
