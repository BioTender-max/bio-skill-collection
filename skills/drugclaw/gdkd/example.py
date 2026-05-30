"""
GDKD query example for canonical packaged resource output.

Default file: resources_metadata/dti/GDKD/gdkd.csv
Columns: drug, gene, score, source
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


DATA_PATH = str(
    Path(__file__).resolve().parents[3]
    / "resources_metadata"
    / "dti"
    / "GDKD"
    / "gdkd.csv"
)


def load_gdkd(path: str = DATA_PATH) -> list[dict]:
    with open(path, newline="", encoding="utf-8", errors="ignore") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def search(rows: list[dict], entity: str, limit: int = 100) -> list[dict]:
    q = entity.strip().lower()
    if not q:
        return []
    hits: list[dict] = []
    for row in rows:
        drug = str(row.get("drug", "")).lower()
        gene = str(row.get("gene", "")).lower()
        if q in drug or q in gene:
            hits.append(row)
            if len(hits) >= limit:
                break
    return hits


def search_batch(rows: list[dict], entities: list[str]) -> dict[str, list[dict]]:
    return {entity: search(rows, entity) for entity in entities}


def summarize(hits: list[dict], entity: str = "") -> str:
    if not hits:
        return f"GDKD | {entity}: no results"
    lines = [f"GDKD | {entity} ({len(hits)} hit(s))"]
    for row in hits[:20]:
        score = row.get("score", "")
        source = row.get("source", "")
        detail = f"{row.get('drug', '?')} -> {row.get('gene', '?')}"
        if score:
            detail += f" (score={score})"
        if source:
            detail += f" [{source}]"
        lines.append(f"  {detail}")
    if len(hits) > 20:
        lines.append(f"  ... ({len(hits) - 20} more)")
    return "\n".join(lines)


def to_json(hits: list[dict]) -> list[dict]:
    return hits


if __name__ == "__main__":
    records = load_gdkd()
    print(f"Loaded {len(records)} GDKD rows")
    for term in ("imatinib", "ABL1"):
        result = search(records, term)
        print(summarize(result, term))
        print()
    print(json.dumps(to_json(search(records, "egfr")[:2]), indent=2))
