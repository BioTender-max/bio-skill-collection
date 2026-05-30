"""
DrugCombDB query example for canonical packaged resource output.

Default file: resources_metadata/drug_combination/DrugCombDB/drugcombdb.csv
Columns: Drug1, Drug2, Cell, Synergy, SynergyType, PMID
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


DATA_PATH = str(
    Path(__file__).resolve().parents[3]
    / "resources_metadata"
    / "drug_combination"
    / "DrugCombDB"
    / "drugcombdb.csv"
)

_CACHE: list[dict] | None = None


def load_data(path: str = DATA_PATH) -> list[dict]:
    with open(path, newline="", encoding="utf-8", errors="ignore") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _rows() -> list[dict]:
    global _CACHE
    if _CACHE is None:
        _CACHE = load_data()
    return _CACHE


def search_drug(drug_name: str, limit: int = 20) -> list[dict]:
    q = drug_name.strip().lower()
    if not q:
        return []
    hits: list[dict] = []
    for row in _rows():
        d1 = str(row.get("Drug1", "")).lower()
        d2 = str(row.get("Drug2", "")).lower()
        if q in d1 or q in d2:
            hits.append(row)
            if len(hits) >= limit:
                break
    return hits


def search_cell_line(cell: str, limit: int = 20) -> list[dict]:
    q = cell.strip().lower()
    if not q:
        return []
    hits: list[dict] = []
    for row in _rows():
        if q in str(row.get("Cell", "")).lower():
            hits.append(row)
            if len(hits) >= limit:
                break
    return hits


def search_drug_pair(drug1: str, drug2: str, limit: int = 50) -> list[dict]:
    d1 = drug1.strip().lower()
    d2 = drug2.strip().lower()
    if not d1 or not d2:
        return []
    hits: list[dict] = []
    for row in _rows():
        r1 = str(row.get("Drug1", "")).lower()
        r2 = str(row.get("Drug2", "")).lower()
        if (d1 in r1 and d2 in r2) or (d1 in r2 and d2 in r1):
            hits.append(row)
            if len(hits) >= limit:
                break
    return hits


def get_by_pmid(pmid: str, limit: int = 20) -> list[dict]:
    q = pmid.strip()
    if not q:
        return []
    return [row for row in _rows() if str(row.get("PMID", "")) == q][:limit]


def search(entity: str, limit: int = 20) -> list[dict]:
    token = entity.strip()
    if not token:
        return []
    if re.fullmatch(r"\d{5,}", token):
        return get_by_pmid(token, limit=limit)
    if re.search(r"[0-9]", token):
        return search_cell_line(token, limit=limit)
    return search_drug(token, limit=limit)


def search_batch(entities: list[str], limit: int = 20) -> dict[str, list[dict]]:
    return {entity: search(entity, limit=limit) for entity in entities}


def summarize(results: list[dict], entity: str) -> str:
    if not results:
        return f"DrugCombDB | {entity}: no results"
    lines = [f"DrugCombDB | {entity} ({len(results)} hit(s))"]
    for row in results[:20]:
        drug1 = row.get("Drug1", "?")
        drug2 = row.get("Drug2", "?")
        cell = row.get("Cell", "")
        synergy = row.get("Synergy", "")
        synergy_type = row.get("SynergyType", "")
        pmid = row.get("PMID", "")
        line = f"{drug1} + {drug2}"
        if cell:
            line += f" | Cell={cell}"
        if synergy:
            line += f" | Synergy={synergy}"
        if synergy_type:
            line += f" | Type={synergy_type}"
        if pmid:
            line += f" | PMID={pmid}"
        lines.append(f"  {line}")
    if len(results) > 20:
        lines.append(f"  ... ({len(results) - 20} more)")
    return "\n".join(lines)


def to_json(results: list[dict]) -> list[dict]:
    return results


if __name__ == "__main__":
    print(f"Loaded {len(_rows())} DrugCombDB rows from {DATA_PATH}")
    demo = search_batch(["imatinib", "K562", "12345678"])
    for term, rows in demo.items():
        print(summarize(rows, term))
        print()
    print(json.dumps(to_json(search_drug_pair("imatinib", "dasatinib")[:2]), indent=2))
