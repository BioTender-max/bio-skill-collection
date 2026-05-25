# Pixi + Jupyter kernel setup (per-directory pixi.toml)

## Goal
The notebook should run in a **per-directory Pixi environment** so that:
- dependencies are reproducible,
- the correct kernel is auto-selected based on the nearest `pixi.toml`,
- teammates can run the notebook without manual interpreter hunting.

Pixi supports this with **pixi-kernel**, which searches for `pixi.toml` (or `pyproject.toml`) in the notebook’s directory or any parent directory and uses that environment to start the kernel.

## Recommended setup (JupyterLab)
From the notebook/project directory:

```bash
pixi init
pixi add python
pixi add jupyterlab pixi-kernel ipykernel
pixi run jupyter lab
```

Then select the Pixi kernel in JupyterLab.

## MANDATORY: Register a named kernel for the pixi environment

**Every Jupyter notebook MUST have a dedicated, registered kernel pointing to its pixi environment.** This is required for `nbconvert --execute`, headless runs, and correct environment resolution. Do this immediately after setting up dependencies — not as an afterthought.

### Steps

1. Ensure `ipykernel` is in `pixi.toml` (under `[pypi-dependencies]` or `[dependencies]`).

2. Register the kernel (run from the project root):
   ```bash
   pixi run python -m ipykernel install --user --name <project-name> --display-name "<Human-readable name> (pixi)"
   ```
   Example:
   ```bash
   pixi run python -m ipykernel install --user --name mcp_structures --display-name "MCP Structures (pixi)"
   ```

3. Set the kernel in the notebook metadata. Either:
   - Select it in JupyterLab’s kernel picker, or
   - Programmatically set it before first execution:
     ```python
     import json
     with open("notebooks/analysis.ipynb") as f:
         nb = json.load(f)
     nb["metadata"]["kernelspec"] = {
         "display_name": "<Human-readable name> (pixi)",
         "language": "python",
         "name": "<project-name>"
     }
     with open("notebooks/analysis.ipynb", "w") as f:
         json.dump(nb, f, indent=1)
     ```

4. Verify headless execution works:
   ```bash
   pixi run jupyter nbconvert --to notebook --execute notebooks/analysis.ipynb
   ```

### Why this matters
Without a registered kernel, `jupyter nbconvert --execute` falls back to a generic `python3` kernel that does NOT use the pixi environment. This causes `ModuleNotFoundError` for every pixi-managed dependency. The notebook may appear to work in JupyterLab (if pixi-kernel auto-resolves) but will fail in CI, headless runs, and `nbconvert`.

## Minimal `pixi.toml` conventions
- The `pixi.toml` should live in the **same directory as the notebook** (or a parent directory).
- Keep dependencies minimal; only add what the notebook imports.
- Prefer pinning versions for stability when notebooks are shared.

See `templates/pixi.toml` for a starting point.

## VS Code notes (if relevant)
Some Pixi kernel implementations may have limitations with VS Code kernel discovery. If VS Code can’t see the kernel, the fallback is often:
- run JupyterLab via `pixi run jupyter lab`, or
- explicitly install an ipykernel (project-specific) and select it.

(Only include these notes if the user uses VS Code.)

## Quick reproducibility check
- A fresh clone of the repo should be runnable with:
  1) `pixi install`
  2) `pixi run python -m ipykernel install --user --name <project-name> --display-name "<Name> (pixi)"`
  3) `pixi run jupyter nbconvert --to notebook --execute notebooks/analysis.ipynb`
