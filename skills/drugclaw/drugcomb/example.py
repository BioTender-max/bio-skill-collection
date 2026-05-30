"""
DrugComb query example for canonical packaged resource output.

Default file: resources_metadata/drug_combination/DrugComb/drugcomb.csv
Columns: drug_row, drug_col, cell_line_name, synergy_zip, synergy_bliss
"""

import csv
import json
import re
from pathlib import Path
from typing import Optional

DATA_PATH = str(
    Path(__file__).resolve().parents[3]
    / "resources_metadata"
    / "drug_combination"
    / "DrugComb"
    / "drugcomb.csv"
)

# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------

def load_drugcomb(path: str = DATA_PATH) -> list[dict]:
    """Load DrugComb summary CSV into a list of dicts (streaming, low-memory
    peak during load). Returns list[dict] where each dict is one row."""
    rows = []
    with open(path, newline="", encoding="utf-8", errors="replace") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            rows.append(row)
    return rows


def columns(data: list[dict]) -> list[str]:
    """Return column names from loaded data."""
    if data:
        return list(data[0].keys())
    return []


# ---------------------------------------------------------------------------
# Entity auto-detection
# ---------------------------------------------------------------------------

def _detect_type(entity: str) -> str:
    """Detect entity type from input string.

    Returns one of: 'block_id', 'cid', 'cell_line', 'drug'.
    Heuristic:
      - pure digits and len <= 10        → block_id
      - 'CID' prefix or pure large int   → cid  (PubChem CID)
      - contains common cell-line tokens  → cell_line
      - otherwise                         → drug  (free-text drug name)
    """
    s = entity.strip()
    if re.fullmatch(r"\d{1,10}", s):
        return "block_id"
    if re.fullmatch(r"(?i)CID:?\s*\d+", s):
        return "cid"
    # Common cell-line naming patterns: e.g. A549, MCF-7, HeLa, NCI-H460
    if re.search(r"(?i)^(MCF|HeLa|A549|NCI|MDA|U2OS|HCT|HL-60|K562|PC-?3|DU-?145|LNCAP|OVCAR|SK-|SW-|T47D|BT-|COLO|HCC|JIMT|TMD)", s):
        return "cell_line"
    return "drug"


# ---------------------------------------------------------------------------
# Search helpers (case-insensitive substring)
# ---------------------------------------------------------------------------

def _match_drug(row: dict, term: str) -> bool:
    """True if *term* is a case-insensitive substring of drug_row or drug_col."""
    t = term.lower()
    dr = (row.get("drug_row") or "").lower()
    dc = (row.get("drug_col") or "").lower()
    return t in dr or t in dc


def _match_cell(row: dict, term: str) -> bool:
    t = term.lower()
    cl = (row.get("cell_line_name") or "").lower()
    return t in cl


def _match_block(row: dict, term: str) -> bool:
    return (row.get("block_id") or "") == term.strip()


def _match_cid(row: dict, term: str) -> bool:
    cid = re.sub(r"(?i)^CID:?\s*", "", term.strip())
    rc = (row.get("drug_row_cid") or row.get("cid_row") or "")
    cc = (row.get("drug_col_cid") or row.get("cid_col") or "")
    return rc == cid or cc == cid


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def search(data: list[dict], entity: str, limit: int = 200) -> list[dict]:
    """Search DrugComb rows matching *entity*. Auto-detects entity type.

    Returns up to *limit* matching rows (dicts).
    """
    etype = _detect_type(entity)
    matcher = {
        "drug": _match_drug,
        "cell_line": _match_cell,
        "block_id": _match_block,
        "cid": _match_cid,
    }[etype]

    hits = []
    for row in data:
        if matcher(row, entity):
            hits.append(row)
            if len(hits) >= limit:
                break
    return hits


def search_batch(data: list[dict], entities: list[str],
                 limit_per_entity: int = 100) -> dict[str, list[dict]]:
    """Search multiple entities. Returns {entity: [rows]}."""
    results = {}
    for ent in entities:
        results[ent] = search(data, ent, limit=limit_per_entity)
    return results


# ---------------------------------------------------------------------------
# Compact LLM-readable output
# ---------------------------------------------------------------------------

_SYNERGY_KEYS = ["synergy_zip", "synergy_bliss", "synergy_loewe", "synergy_hsa"]
_SCORE_KEYS = ["css_ri", "css", "S_mean", "S_max", "ic50_row", "ic50_col"]


def _fmt_num(val: Optional[str], digits: int = 2) -> str:
    if val is None or val == "":
        return "NA"
    try:
        return f"{float(val):.{digits}f}"
    except ValueError:
        return val


def summarize(hits: list[dict], entity: str, max_lines: int = 30) -> str:
    """Return a compact text summary suitable for LLM context windows.

    Format per line:
      DrugA + DrugB | Cell: <cell> | ZIP=<z> BLISS=<b> LOEWE=<l> HSA=<h> | CSS=<c>
    """
    if not hits:
        return f"{entity}: no results"
    lines = [f"{entity}: {len(hits)} hit(s)"]
    for row in hits[:max_lines]:
        d1 = row.get("drug_row", "?")
        d2 = row.get("drug_col", "?")
        cl = row.get("cell_line_name", "?")
        syn_parts = []
        for k in _SYNERGY_KEYS:
            short = k.replace("synergy_", "").upper()
            syn_parts.append(f"{short}={_fmt_num(row.get(k))}")
        css_val = row.get("css_ri") or row.get("css") or ""
        study = row.get("study_name", "")
        line = f"  {d1} + {d2} | Cell:{cl} | {' '.join(syn_parts)} | CSS={_fmt_num(css_val)}"
        if study:
            line += f" | Study:{study}"
        lines.append(line)
    if len(hits) > max_lines:
        lines.append(f"  ... ({len(hits) - max_lines} more rows omitted)")
    return "\n".join(lines)


def to_json(hits: list[dict]) -> list[dict]:
    """Return hits as a JSON-serialisable list (passthrough for dicts)."""
    return hits


# ---------------------------------------------------------------------------
# Main: runnable usage examples
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== DrugComb Skill: Loading data ===")
    data = load_drugcomb()
    print(f"Loaded {len(data)} rows, {len(columns(data))} columns")
    print(f"Columns: {columns(data)[:20]} ...")

    # --- single drug search ---
    print("\n--- search('5-FU') ---")
    hits = search(data, "5-FU")
    print(summarize(hits, "5-FU"))

    # --- cell-line search ---
    print("\n--- search('A549') ---")
    hits = search(data, "A549")
    print(summarize(hits, "A549"))

    # --- batch search ---
    print("\n--- search_batch(['imatinib', 'sorafenib']) ---")
    batch = search_batch(data, ["imatinib", "sorafenib"], limit_per_entity=5)
    for ent, rows in batch.items():
        print(summarize(rows, ent))

    # --- JSON output ---
    print("\n--- to_json (first 2 hits for 'vorinostat') ---")
    hits = search(data, "vorinostat")
    print(json.dumps(to_json(hits[:2]), indent=2))
