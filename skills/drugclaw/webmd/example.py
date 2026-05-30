"""
WebMD Drug Reviews – Patient-Reported Drug Effectiveness and Side Effects
Category: Drug-centric | Type: Dataset | Subcategory: Drug Review / Patient Report
Link: https://www.kaggle.com/datasets/rohanharode07/webmd-drug-reviews-dataset

~362 k patient reviews scraped from WebMD (2007 – Mar 2020).
Each row carries a drug name, treated condition, free-text review & side-effect
description, demographic fields (Age, Sex), and three 1-5 star ratings
(Effectiveness, EaseofUse, Satisfaction).

Access: Download CSV from Kaggle → place at DATA_PATH below.
"""

import os
import csv
from pathlib import Path
from collections import defaultdict

DATA_PATH = str(
    Path(__file__).resolve().parents[3]
    / "resources_metadata"
    / "drug_review"
    / "WebMDDrugReviews"
    / "webmd.csv"
)

# ── helpers ────────────────────────────────────────────────────────────

def load_reviews(path: str = DATA_PATH) -> list[dict]:
    """Load the CSV into a list of dicts. Returns [] if file missing."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV not found: {path}")
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))


def _norm(text: str) -> str:
    return text.strip().lower()


def _match(field_val: str, query: str) -> bool:
    """Case-insensitive substring match."""
    return query in _norm(field_val)


# ── core query functions ───────────────────────────────────────────────

def search_by_drug(rows: list[dict], drug: str) -> list[dict]:
    """Return all reviews whose Drug field contains *drug* (case-insensitive)."""
    q = _norm(drug)
    return [r for r in rows if _match(r.get("Drug", ""), q)]


def search_by_condition(rows: list[dict], condition: str) -> list[dict]:
    """Return all reviews whose Condition field contains *condition*."""
    q = _norm(condition)
    return [r for r in rows if _match(r.get("Condition", ""), q)]


def search(rows: list[dict], entity: str) -> list[dict]:
    """Search by drug name first; if nothing found, fall back to condition."""
    hits = search_by_drug(rows, entity)
    if not hits:
        hits = search_by_condition(rows, entity)
    return hits


def search_batch(rows: list[dict], entities: list[str]) -> dict[str, list[dict]]:
    """Search multiple entities. Returns {entity: [matching rows]}."""
    return {e: search(rows, e) for e in entities}


# ── summarisation ──────────────────────────────────────────────────────

_RATING_COLS = ["Effectiveness", "EaseofUse", "Satisfaction"]


def summarize(hits: list[dict], entity: str) -> str:
    """One-paragraph summary: counts, avg ratings, top conditions/drugs."""
    if not hits:
        return f"No reviews found for '{entity}'."

    n = len(hits)
    # average ratings
    avgs = {}
    for col in _RATING_COLS:
        vals = []
        for r in hits:
            try:
                vals.append(float(r.get(col, "")))
            except ValueError:
                pass
        avgs[col] = round(sum(vals) / len(vals), 2) if vals else None

    # top conditions (when searching by drug) / top drugs (when searching by condition)
    cond_counts: dict[str, int] = defaultdict(int)
    drug_counts: dict[str, int] = defaultdict(int)
    for r in hits:
        c = r.get("Condition", "").strip()
        d = r.get("Drug", "").strip()
        if c:
            cond_counts[c] += 1
        if d:
            drug_counts[d] += 1

    top_conds = sorted(cond_counts, key=cond_counts.get, reverse=True)[:5]
    top_drugs = sorted(drug_counts, key=drug_counts.get, reverse=True)[:5]

    lines = [f"Entity: {entity}  |  Reviews matched: {n}"]
    for col in _RATING_COLS:
        if avgs[col] is not None:
            lines.append(f"  Avg {col}: {avgs[col]}")
    if top_conds:
        lines.append(f"  Top conditions: {', '.join(top_conds)}")
    if top_drugs:
        lines.append(f"  Top drugs: {', '.join(top_drugs)}")
    return "\n".join(lines)


def to_json(hits: list[dict]) -> list[dict]:
    """Return hits as a JSON-serialisable list (identity for csv.DictReader rows)."""
    return hits


# ── CLI demo ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    rows = load_reviews()
    print(f"Loaded {len(rows)} reviews.  Columns: {list(rows[0].keys())}\n")

    # --- single entity search (drug name) ---
    hits = search(rows, "Lipitor")
    print(summarize(hits, "Lipitor"))
    print()

    # --- single entity search (condition) ---
    hits = search(rows, "High Blood Pressure")
    print(summarize(hits, "High Blood Pressure"))
    print()

    # --- batch search ---
    results = search_batch(rows, ["Metformin", "Ibuprofen", "Prozac"])
    for entity, h in results.items():
        print(summarize(h, entity))
        print()

    # --- JSON output (first 2 rows) ---
    sample = search(rows, "Lipitor")[:2]
    import json
    print("JSON sample:\n", json.dumps(to_json(sample), indent=2, ensure_ascii=False))
