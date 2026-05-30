"""
RepurposeDrugs query example for canonical packaged resource output.

Default file: resources_metadata/drug_repurposing/RepurposeDrugs/repurposedrugs.csv
Columns: drug, disease, score, status, pmid
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


DATA_PATH = str(
    Path(__file__).resolve().parents[3]
    / "resources_metadata"
    / "drug_repurposing"
    / "RepurposeDrugs"
    / "repurposedrugs.csv"
)


def load_data(path: str = DATA_PATH) -> list[dict]:
    with open(path, newline="", encoding="utf-8", errors="ignore") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def search(rows: list[dict], entity: str, limit: int = 200) -> list[dict]:
    q = entity.strip()
    if not q:
        return []

    q_lower = q.lower()
    is_pmid = bool(re.fullmatch(r"\d{5,}", q))
    hits: list[dict] = []
    for row in rows:
        drug = str(row.get("drug", ""))
        disease = str(row.get("disease", ""))
        pmid = str(row.get("pmid", ""))

        matched = False
        if is_pmid and pmid == q:
            matched = True
        elif q_lower in drug.lower() or q_lower in disease.lower():
            matched = True

        if matched:
            hits.append(row)
            if len(hits) >= limit:
                break
    return hits


def search_batch(rows: list[dict], entities: list[str]) -> dict[str, list[dict]]:
    return {entity: search(rows, entity) for entity in entities}


def summarize(hits: list[dict], entity: str = "") -> str:
    if not hits:
        return f"RepurposeDrugs | {entity}: no results"

    lines = [f"RepurposeDrugs | {entity} ({len(hits)} hit(s))"]
    for row in hits[:20]:
        score = row.get("score", "")
        status = row.get("status", "")
        pmid = row.get("pmid", "")
        line = f"{row.get('drug', '?')} -> {row.get('disease', '?')}"
        if status:
            line += f" [{status}]"
        if score:
            line += f" (score={score})"
        if pmid:
            line += f" PMID:{pmid}"
        lines.append(f"  {line}")
    if len(hits) > 20:
        lines.append(f"  ... ({len(hits) - 20} more)")
    return "\n".join(lines)


def to_json(hits: list[dict]) -> list[dict]:
    return hits


if __name__ == "__main__":
    records = load_data()
    print(f"Loaded {len(records)} RepurposeDrugs rows")
    for term in ("imatinib", "systemic sclerosis", "34567890"):
        result = search(records, term)
        print(summarize(result, term))
        print()
    print(json.dumps(to_json(search(records, "metformin")[:2]), indent=2))
