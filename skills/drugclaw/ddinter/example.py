"""
DDInter - Drug-Drug Interaction Database (Local CSV)
Category: Drug-centric | Type: DB | Subcategory: Drug-Drug Interaction (DDI)
Link: https://ddinter2.scbdd.com/server/search/
Paper: https://academic.oup.com/nar/article/53/D1/D1356/7740584

DDInter is a comprehensive DDI database providing interaction severity levels
(Major / Moderate / Minor) between drug pairs.

Access method: Local CSV files (8 ATC-code partitions merged at load time).
"""

import csv
import json
import os
import re
from pathlib import Path
from typing import List, Dict, Optional, Union

# ---------------------------------------------------------------------------
# Data path
# ---------------------------------------------------------------------------
DATA_DIR = str(
    Path(__file__).resolve().parents[3] / "resources_metadata" / "ddi" / "DDInter"
)

# ---------------------------------------------------------------------------
# In-memory cache (lazy-loaded once)
# ---------------------------------------------------------------------------
_CACHE: Optional[list] = None          # list[dict]
_DRUG_INDEX: Optional[dict] = None     # drug_name_lower -> set of row indices
_ID_INDEX: Optional[dict] = None       # ddinter_id_lower -> set of row indices


def _load_all(data_dir: str = DATA_DIR) -> list:
    """Load and merge all ddinter_downloads_code_*.csv files. Lazy + cached."""
    global _CACHE, _DRUG_INDEX, _ID_INDEX
    if _CACHE is not None:
        return _CACHE

    rows: list = []
    files = sorted(f for f in os.listdir(data_dir)
                   if f.startswith("ddinter_downloads_code_") and f.endswith(".csv"))
    if not files:
        raise FileNotFoundError(f"No DDInter CSV files found in {data_dir}")

    for fname in files:
        path = os.path.join(data_dir, fname)
        with open(path, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for r in reader:
                rows.append(r)

    # Build indices
    _DRUG_INDEX = {}
    _ID_INDEX = {}
    for idx, r in enumerate(rows):
        for col_drug in ("Drug_A", "Drug_B"):
            key = r.get(col_drug, "").strip().lower()
            if key:
                _DRUG_INDEX.setdefault(key, set()).add(idx)
        for col_id in ("DDInterID_A", "DDInterID_B"):
            key = r.get(col_id, "").strip().lower()
            if key:
                _ID_INDEX.setdefault(key, set()).add(idx)

    _CACHE = rows
    print(f"[DDInter] Loaded {len(rows)} interaction rows from {len(files)} files.")
    return _CACHE


# ---------------------------------------------------------------------------
# Entity detection
# ---------------------------------------------------------------------------
_RE_DDINTER_ID = re.compile(r"^DDInter\d+$", re.IGNORECASE)


def _detect_type(entity: str) -> str:
    """Return 'id' or 'name'."""
    if _RE_DDINTER_ID.match(entity.strip()):
        return "id"
    return "name"


# ---------------------------------------------------------------------------
# Core query
# ---------------------------------------------------------------------------
def search(entity: str, data_dir: str = DATA_DIR, top_n: int = 50) -> list:
    """
    Search DDInter for interactions involving *entity*.

    Parameters
    ----------
    entity : str
        Drug name (substring match) or DDInter ID (exact match, e.g. DDInter582).
    data_dir : str
        Directory containing the CSV files.
    top_n : int
        Maximum number of rows returned (default 50).

    Returns
    -------
    list[dict]  – matching interaction rows.
    """
    rows = _load_all(data_dir)
    etype = _detect_type(entity)
    hits: list = []

    if etype == "id":
        key = entity.strip().lower()
        indices = _ID_INDEX.get(key, set())
        hits = [rows[i] for i in sorted(indices)]
    else:
        key = entity.strip().lower()
        # Try exact drug name index first
        indices = _DRUG_INDEX.get(key, set())
        if indices:
            hits = [rows[i] for i in sorted(indices)]
        else:
            # Fall back to substring search across Drug_A and Drug_B
            for r in rows:
                if (key in r.get("Drug_A", "").lower()
                        or key in r.get("Drug_B", "").lower()):
                    hits.append(r)

    return hits[:top_n]


def search_batch(entities: List[str], data_dir: str = DATA_DIR,
                 top_n: int = 50) -> Dict[str, list]:
    """Run search() for each entity. Returns {entity: [rows]}."""
    return {e: search(e, data_dir, top_n) for e in entities}


# ---------------------------------------------------------------------------
# Summarize (LLM-readable)
# ---------------------------------------------------------------------------
def summarize(hits: list, entity: str) -> str:
    """
    One-line-per-hit compact text summary suitable for LLM consumption.
    Groups results by severity level.
    """
    if not hits:
        return f"No DDI records found for '{entity}'."

    # Count by level
    level_counts: Dict[str, int] = {}
    for h in hits:
        lv = h.get("Level", "Unknown").strip()
        level_counts[lv] = level_counts.get(lv, 0) + 1

    lines = [f"DDInter results for '{entity}': {len(hits)} interaction(s) "
             f"[{', '.join(f'{v} {k}' for k, v in sorted(level_counts.items()))}]"]

    for h in hits:
        drug_a = h.get("Drug_A", "?")
        drug_b = h.get("Drug_B", "?")
        level = h.get("Level", "?")
        id_a = h.get("DDInterID_A", "")
        id_b = h.get("DDInterID_B", "")
        lines.append(f"  {drug_a} ({id_a}) + {drug_b} ({id_b}) => {level}")

    return "\n".join(lines)


def to_json(hits: list) -> list:
    """Return hits as a list of plain dicts (already native dicts)."""
    return [dict(h) for h in hits]


# ---------------------------------------------------------------------------
# Convenience helpers
# ---------------------------------------------------------------------------
def list_drugs(data_dir: str = DATA_DIR) -> list:
    """Return sorted unique drug names across all files."""
    rows = _load_all(data_dir)
    names = set()
    for r in rows:
        a = r.get("Drug_A", "").strip()
        b = r.get("Drug_B", "").strip()
        if a:
            names.add(a)
        if b:
            names.add(b)
    return sorted(names)


def get_interactions_between(drug_a: str, drug_b: str,
                             data_dir: str = DATA_DIR) -> list:
    """
    Return interactions specifically between two drugs (order-independent).
    """
    rows = _load_all(data_dir)
    a_low, b_low = drug_a.strip().lower(), drug_b.strip().lower()
    hits = []
    for r in rows:
        ra = r.get("Drug_A", "").strip().lower()
        rb = r.get("Drug_B", "").strip().lower()
        if (a_low in ra and b_low in rb) or (a_low in rb and b_low in ra):
            hits.append(r)
    return hits


# ===================================================================
# Runnable examples
# ===================================================================
if __name__ == "__main__":
    # --- Single drug search (dataset uses "Acetylsalicylic acid" for aspirin) ---
    print("=== Search: Acetylsalicylic acid ===")
    hits = search("Acetylsalicylic acid")
    print(summarize(hits, "Acetylsalicylic acid"))

    # --- DDInter ID search ---
    print("\n=== Search: DDInter582 (Dolutegravir) ===")
    hits = search("DDInter582")
    print(summarize(hits, "DDInter582"))

    # --- Pair interaction ---
    print("\n=== Pair: Acetylsalicylic acid + Ibuprofen ===")
    pair = get_interactions_between("Acetylsalicylic acid", "Ibuprofen")
    if pair:
        for p in pair:
            print(f"  {p['Drug_A']} + {p['Drug_B']} => {p['Level']}")
    else:
        print("  No direct interaction found.")

    # --- Batch search ---
    print("\n=== Batch: [Metformin, Ibuprofen] ===")
    batch = search_batch(["Metformin", "Ibuprofen"], top_n=5)
    for ent, rows in batch.items():
        print(summarize(rows, ent))

    # --- JSON output ---
    print("\n=== JSON (first 2 hits for Metformin) ===")
    hits = search("Metformin", top_n=2)
    print(json.dumps(to_json(hits), indent=2))
