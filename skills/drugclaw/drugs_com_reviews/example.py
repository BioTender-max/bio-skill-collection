"""
Skill 16 – DrugLib.com Drug Review Dataset (UCI #461)
Query patient drug reviews by drug name or medical condition.
"""

import csv
import os
import re
from pathlib import Path
from collections import defaultdict

# ── data path ──────────────────────────────────────────────────────
DATA_DIR = str(
    Path(__file__).resolve().parents[3]
    / "resources_metadata"
    / "drug_review"
    / "DrugReviews"
)
TRAIN_FILE = os.path.join(DATA_DIR, "drugLibTrain_raw.tsv")
TEST_FILE  = os.path.join(DATA_DIR, "drugLibTest_raw.tsv")

COLUMNS = [
    "row_id", "urlDrugName", "rating", "effectiveness",
    "sideEffects", "condition", "benefitsReview",
    "sideEffectsReview", "commentsReview",
]

# ── load ───────────────────────────────────────────────────────────
_cache: list[dict] | None = None


def load_reviews() -> list[dict]:
    """Load and merge train+test TSV files. Cached after first call."""
    global _cache
    if _cache is not None:
        return _cache

    rows: list[dict] = []
    for fp in (TRAIN_FILE, TEST_FILE):
        with open(fp, encoding="utf-8", errors="replace") as fh:
            reader = csv.DictReader(fh, delimiter="\t", fieldnames=COLUMNS)
            next(reader, None)                       # skip header
            for r in reader:
                # normalise rating to int when possible
                try:
                    r["rating"] = int(r["rating"])
                except (ValueError, TypeError):
                    r["rating"] = None
                rows.append(r)
    _cache = rows
    return _cache


# ── entity detection ───────────────────────────────────────────────
def _detect_type(entity: str) -> str:
    """Heuristic: if the term looks like a condition (multi-word / common
    medical suffixes) route to condition search; otherwise treat as drug."""
    e = entity.strip().lower()
    condition_hints = (
        "disease", "disorder", "syndrome", "infection", "pain",
        "cancer", "diabetes", "hypertension", "depression", "anxiety",
        "asthma", "arthritis", "migraine", "allergy", "insomnia",
        "nausea", "obesity", "acne", "gerd", "copd",
    )
    if any(h in e for h in condition_hints):
        return "condition"
    if len(e.split()) >= 3:
        return "condition"
    return "drug"


# ── search ─────────────────────────────────────────────────────────
def search(entity: str, data: list[dict] | None = None) -> list[dict]:
    """Search reviews by a single drug name or condition (auto-detected).
    Returns list of matching review dicts.
    """
    if data is None:
        data = load_reviews()
    e = entity.strip().lower()
    etype = _detect_type(e)
    field = "condition" if etype == "condition" else "urlDrugName"
    return [r for r in data if e in (r.get(field) or "").lower()]


def search_batch(entities: list[str],
                 data: list[dict] | None = None) -> dict[str, list[dict]]:
    """Search for multiple entities. Returns {entity: [hits]}."""
    if data is None:
        data = load_reviews()
    return {ent: search(ent, data) for ent in entities}


# ── output helpers ─────────────────────────────────────────────────
def summarize(hits: list[dict], entity: str) -> str:
    """Return a compact, LLM-readable text summary of search results."""
    if not hits:
        return f"No reviews found for '{entity}'."

    n = len(hits)
    ratings = [h["rating"] for h in hits if h["rating"] is not None]
    avg_rating = sum(ratings) / len(ratings) if ratings else None

    # effectiveness distribution
    eff = defaultdict(int)
    for h in hits:
        eff[h.get("effectiveness", "Unknown")] += 1

    # side-effects distribution
    se = defaultdict(int)
    for h in hits:
        se[h.get("sideEffects", "Unknown")] += 1

    # top conditions (if searching by drug)
    conds = defaultdict(int)
    for h in hits:
        c = (h.get("condition") or "").strip()
        if c:
            conds[c] += 1
    top_conds = sorted(conds.items(), key=lambda x: -x[1])[:5]

    lines = [
        f"== DrugLib Reviews: '{entity}' ({n} reviews) ==",
        f"Avg rating: {avg_rating:.1f}/9" if avg_rating else "Avg rating: N/A",
        "Effectiveness: " + ", ".join(f"{k} ({v})" for k, v in sorted(eff.items(), key=lambda x: -x[1])),
        "Side effects:  " + ", ".join(f"{k} ({v})" for k, v in sorted(se.items(), key=lambda x: -x[1])),
    ]
    if top_conds:
        lines.append("Top conditions: " + ", ".join(f"{c} ({n})" for c, n in top_conds))

    # sample review excerpt (first non-empty benefitsReview)
    for h in hits[:5]:
        txt = (h.get("benefitsReview") or "").strip().strip('"')
        if txt and len(txt) > 20:
            lines.append(f"Sample review: \"{txt[:200]}{'...' if len(txt)>200 else ''}\"")
            break

    return "\n".join(lines)


def to_json(hits: list[dict]) -> list[dict]:
    """Return hits as a clean list of dicts (JSON-serialisable)."""
    keep = [
        "urlDrugName", "rating", "effectiveness", "sideEffects",
        "condition", "benefitsReview", "sideEffectsReview", "commentsReview",
    ]
    return [{k: h.get(k) for k in keep} for h in hits]


# ── main ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    data = load_reviews()
    print(f"Loaded {len(data)} reviews\n")

    # 1) search by drug name
    hits = search("lamictal", data)
    print(summarize(hits, "lamictal"))
    print()

    # 2) search by condition
    hits = search("bipolar disorder", data)
    print(summarize(hits, "bipolar disorder"))
    print()

    # 3) batch search
    results = search_batch(["biaxin", "sinus infection"], data)
    for ent, h in results.items():
        print(summarize(h, ent))
        print()

    # 4) JSON output (first 2 records)
    import json
    hits = search("biaxin", data)
    print(json.dumps(to_json(hits)[:2], indent=2))
