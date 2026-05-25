#!/usr/bin/env python3

"""
Lint notebook structure for "KISS + Markdown-first" requirements.

Rules (default):
- Every code cell must be preceded by a non-empty markdown cell.
- The notebook should start with a markdown title/intro cell.
- Warn on code cells > N lines (default N=50).

Optional:
- --require-local-pixi: require pixi.toml in the same directory as the notebook.

Usage:
  python scripts/lint_notebook_structure.py notebooks/01_analysis.ipynb
"""
from __future__ import annotations

import argparse
from pathlib import Path

import nbformat


def is_nonempty_markdown(cell) -> bool:
    if cell.get("cell_type") != "markdown":
        return False
    src = (cell.get("source") or "").strip()
    return len(src) > 0


def lint_notebook(path: Path, *, max_code_lines: int = 50, require_local_pixi: bool = False) -> list[str]:
    nb = nbformat.read(str(path), as_version=4)
    errors: list[str] = []
    warnings: list[str] = []

    cells = nb.get("cells", [])
    if not cells:
        errors.append("Notebook has no cells.")
        return errors

    if not is_nonempty_markdown(cells[0]):
        errors.append("First cell must be a non-empty markdown intro/title cell.")

    for i, cell in enumerate(cells):
        if cell.get("cell_type") != "code":
            continue

        # Rule: preceding cell must be non-empty markdown
        if i == 0 or not is_nonempty_markdown(cells[i - 1]):
            errors.append(f"Code cell #{i} must be preceded by a non-empty markdown cell.")

        # Warn on large code cells
        src = cell.get("source") or ""
        n_lines = len(src.splitlines())
        if n_lines > max_code_lines:
            warnings.append(f"Code cell #{i} has {n_lines} lines (> {max_code_lines}). Consider splitting it.")

    if require_local_pixi:
        pixi_path = path.parent / "pixi.toml"
        if not pixi_path.exists():
            errors.append(f"Missing pixi.toml next to notebook: expected {pixi_path}")

    return errors + [f"WARNING: {w}" for w in warnings]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("notebook", type=Path)
    ap.add_argument("--max-code-lines", type=int, default=50)
    ap.add_argument("--require-local-pixi", action="store_true")
    args = ap.parse_args()

    nb_path: Path = args.notebook
    if not nb_path.exists():
        raise SystemExit(f"Notebook not found: {nb_path}")

    msgs = lint_notebook(
        nb_path,
        max_code_lines=args.max_code_lines,
        require_local_pixi=args.require_local_pixi,
    )

    if not msgs:
        print("OK: Notebook passes structure lint.")
        return

    # Print all messages; non-warning messages are errors.
    has_error = any(not m.startswith("WARNING:") for m in msgs)
    for m in msgs:
        print(m)

    raise SystemExit(1 if has_error else 0)


if __name__ == "__main__":
    main()
