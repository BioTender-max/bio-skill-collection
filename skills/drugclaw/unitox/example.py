"""
UniTox – Unified Multi-Organ Drug Toxicity Annotation
Category: Drug-centric | Type: Dataset | Subcategory: Drug Toxicity
Source : https://zenodo.org/records/11627822
Paper  : https://doi.org/10.1101/2024.06.21.24309315

UniTox uses GPT-4o to process FDA drug labels and extract toxicity
ratings across eight organ-system toxicities (ternary: No / Low / High;
binary: Yes / No), with 85-96 % clinician concordance.

Access: local CSV (tab-separated).
"""

import csv
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Union

# ── Path to the local UniTox TSV ──────────────────────────────────────
DATA_PATH = str(
    Path(__file__).resolve().parents[3]
    / "resources_metadata"
    / "drug_toxicity"
    / "UniTox"
    / "UniTox.csv"
)

# ── Eight organ-system toxicity categories ────────────────────────────
TOXICITY_SYSTEMS = [
    "cardiotoxicity",
    "dermatological_toxicity",
    "hematological",
    "infertility",
    "liver_toxicity",
    "ototoxicity",
    "pulmonary_toxicity",
    "renal_toxicity",
]

# Column-name templates (dataset uses slightly irregular stems)
_TERNARY = {s: f"{s}_ternary_rating" for s in TOXICITY_SYSTEMS}
_BINARY  = {s: f"{s}_binary_rating"  for s in TOXICITY_SYSTEMS}
_REASON  = {
    "cardiotoxicity":          "cardiotoxicity_reasoning",
    "dermatological_toxicity":  "dermatological_toxicity_reasoning",
    "hematological":            "hematological_reasoning",
    "infertility":              "infertility_reasoning",
    "liver_toxicity":           "liver_toxicity_reasoning",
    "ototoxicity":              "ototoxicity_reasoning",
    "pulmonary_toxicity":       "pulmonary_toxicity_reasoning",
    "renal_toxicity":           "renal_toxicity_reasoning",
}

# ── Cache ─────────────────────────────────────────────────────────────
_cache: Dict[str, list] = {}


# ── Loader ────────────────────────────────────────────────────────────
def load_unitox(path: str = DATA_PATH) -> List[dict]:
    """Load UniTox CSV/TSV into a list of dicts (cached after first call).
    Auto-detects delimiter (tab vs comma) from the header line."""
    if path in _cache:
        return _cache[path]
    if not os.path.exists(path):
        raise FileNotFoundError(f"UniTox file not found: {path}")
    # Auto-detect delimiter from first line
    with open(path, encoding="utf-8-sig", errors="replace") as fh:
        first_line = fh.readline()
    delimiter = "\t" if "\t" in first_line else ","
    rows: List[dict] = []
    with open(path, newline="", encoding="utf-8-sig", errors="replace") as fh:
        reader = csv.DictReader(fh, delimiter=delimiter)
        for row in reader:
            rows.append(row)
    _cache[path] = rows
    return rows


# ── Entity-type detection ─────────────────────────────────────────────
_RE_UUID = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I
)
_RE_SMILES = re.compile(r"[=#\[\]@+\-\\\/][A-Za-z0-9]")


def _detect_type(entity: str) -> str:
    """Return 'spl_id', 'smiles', or 'name'."""
    e = entity.strip()
    if _RE_UUID.match(e):
        return "spl_id"
    if _RE_SMILES.search(e) and len(e) > 20:
        return "smiles"
    return "name"


# ── Search ────────────────────────────────────────────────────────────
def search(entity: str, path: str = DATA_PATH) -> List[dict]:
    """
    Search UniTox by a single entity.
    Auto-detects type:
      - UUID          → exact match on SPL_ID
      - SMILES string → exact match on smiles / all_smiles
      - anything else → case-insensitive substring on generic_name
    Returns list of matching row-dicts.
    """
    data = load_unitox(path)
    etype = _detect_type(entity)
    e = entity.strip()
    hits: List[dict] = []
    if etype == "spl_id":
        el = e.lower()
        hits = [r for r in data if r.get("SPL_ID", "").lower() == el]
    elif etype == "smiles":
        hits = [
            r for r in data
            if r.get("smiles", "") == e or r.get("all_smiles", "") == e
        ]
    else:  # name
        el = e.lower()
        hits = [r for r in data if el in r.get("generic_name", "").lower()]
    return hits


def search_batch(
    entities: List[str], path: str = DATA_PATH
) -> Dict[str, List[dict]]:
    """Search UniTox for a list of entities. Returns {entity: [rows]}."""
    return {e: search(e, path) for e in entities}


# ── Output helpers ────────────────────────────────────────────────────
def _rating_line(row: dict) -> str:
    """One-line toxicity profile: system=ternary(binary)."""
    parts = []
    for sys in TOXICITY_SYSTEMS:
        t = row.get(_TERNARY[sys], "?")
        b = row.get(_BINARY[sys], "?")
        label = sys.replace("_", " ").title()
        parts.append(f"{label}={t}({b})")
    return " | ".join(parts)


def summarize(hits: List[dict], entity: str = "") -> str:
    """
    Compact LLM-readable summary (ratings only, no reasoning).
    """
    header = f"UniTox results for '{entity}'" if entity else "UniTox results"
    if not hits:
        return f"{header}: no matches found."
    lines = [f"{header}: {len(hits)} match(es)"]
    for row in hits:
        name = row.get("generic_name", "?")
        lines.append(f"\n  Drug: {name}")
        lines.append(f"  SPL_ID: {row.get('SPL_ID', '?')}")
        lines.append(f"  Toxicity profile: {_rating_line(row)}")
    return "\n".join(lines)


def summarize_with_reasoning(
    hits: List[dict], entity: str = "", systems: Optional[List[str]] = None
) -> str:
    """
    Detailed summary including reasoning text for selected organ systems.
    If *systems* is None, include all eight systems.
    """
    header = f"UniTox results for '{entity}'" if entity else "UniTox results"
    if not hits:
        return f"{header}: no matches found."
    sel = systems or TOXICITY_SYSTEMS
    lines = [f"{header}: {len(hits)} match(es)"]
    for row in hits:
        name = row.get("generic_name", "?")
        lines.append(f"\n  Drug: {name}  (SPL_ID: {row.get('SPL_ID', '?')})")
        for sys in sel:
            if sys not in _REASON:
                continue
            label = sys.replace("_", " ").title()
            t = row.get(_TERNARY[sys], "?")
            b = row.get(_BINARY[sys], "?")
            reason = row.get(_REASON[sys], "").strip()
            # Truncate long reasoning for readability
            if len(reason) > 300:
                reason = reason[:297] + "..."
            lines.append(f"  [{label}] ternary={t}  binary={b}")
            if reason:
                lines.append(f"    Reasoning: {reason}")
    return "\n".join(lines)


def to_json(hits: List[dict], include_reasoning: bool = False) -> List[dict]:
    """
    Structured output. By default returns ratings + metadata only
    (no lengthy reasoning). Set include_reasoning=True for full rows.
    """
    if include_reasoning:
        return hits
    out = []
    for row in hits:
        rec: dict = {
            "generic_name": row.get("generic_name", ""),
            "smiles": row.get("smiles", ""),
            "SPL_ID": row.get("SPL_ID", ""),
        }
        for sys in TOXICITY_SYSTEMS:
            rec[f"{sys}_ternary"] = row.get(_TERNARY[sys], "")
            rec[f"{sys}_binary"]  = row.get(_BINARY[sys], "")
        out.append(rec)
    return out


# ── Convenience: list all drugs ───────────────────────────────────────
def list_drugs(path: str = DATA_PATH) -> List[str]:
    """Return sorted list of all generic_name values."""
    data = load_unitox(path)
    return sorted({r.get("generic_name", "") for r in data} - {""})


# ── CLI demo ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    import json

    # 0. Diagnostic: verify loading
    data = load_unitox()
    print(f"Loaded {len(data)} rows from {DATA_PATH}")
    if data:
        print(f"Columns: {list(data[0].keys())[:5]} ... ({len(data[0])} total)")
        print(f"First drug: {data[0].get('generic_name', '??')}")
    else:
        # Extra debug: show raw first 2 lines
        with open(DATA_PATH, encoding="utf-8-sig", errors="replace") as f:
            for i, line in enumerate(f):
                if i >= 2:
                    break
                print(f"  raw line {i}: {line[:200]!r}")
        raise SystemExit("No rows loaded – check file format above.")

    # 1. Single drug search (name)
    hits = search("metformin")
    print(summarize(hits, "metformin"))

    # 2. Batch search
    results = search_batch(["aspirin", "ibuprofen", "doxorubicin"])
    for ent, rows in results.items():
        print(summarize(rows, ent))

    # 3. JSON output
    hits = search("cisplatin")
    print(json.dumps(to_json(hits), indent=2))

    # 4. Detailed reasoning for specific organs
    hits = search("doxorubicin")
    print(summarize_with_reasoning(hits, "doxorubicin",
                                   systems=["cardiotoxicity", "hematological"]))

    # 5. List total drug count
    drugs = list_drugs()
    print(f"\nTotal drugs in UniTox: {len(drugs)}")
