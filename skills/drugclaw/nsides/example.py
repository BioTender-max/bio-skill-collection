"""
nSIDES - Drug Side Effects & Adverse Drug Reactions
Category: Drug-centric | Type: DB | Subcategory: Adverse Drug Reaction (ADR)
Link: https://nsides.io/
Paper: https://doi.org/10.1016/j.medj.2025.100642

nSIDES is a family of databases for drug side effects:
  - OnSIDES : adverse events extracted from structured product labels (US/EU/UK/JP)
  - OffSIDES: off-label side effects mined from FAERS via propensity-score matching
  - KidSIDES: pediatric drug safety signals stratified by developmental phase

Local data:
  - OnSIDES  → SQLite database  (onsides.db)
  - OffSIDES → gzipped CSV      (OFFSIDES.csv.gz)
  - KidSIDES → gzipped CSVs     (ade_nichd.csv.gz + drug.csv.gz + event.csv.gz + dictionary.csv.gz)
"""

import csv
import gzip
import io
import json
import os
import sqlite3
from pathlib import Path
from typing import Union

# ── paths (adjust to your environment) ──────────────────────
DATA_DIR = str(
    Path(__file__).resolve().parents[3] / "resources_metadata" / "adr" / "nSIDES"
)

ONSIDES_DB   = os.path.join(DATA_DIR, "onsides.db")
OFFSIDES_GZ  = os.path.join(DATA_DIR, "OFFSIDES.csv.gz")
KIDSIDES_DIR = DATA_DIR  # ade_nichd.csv.gz, drug.csv.gz, event.csv.gz, dictionary.csv.gz


# ── internal caches ─────────────────────────────────────────
_offsides_index: dict[str, list[dict]] | None = None   # drug_name_lower → rows
_kidsides_drug:  dict | None = None                     # concept_id → name
_kidsides_event: dict | None = None                     # concept_id → name
_kidsides_phase: dict | None = None                     # nichd_code  → phase label


# ── OnSIDES helpers (SQLite) ────────────────────────────────

def _onsides_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(ONSIDES_DB)
    conn.row_factory = sqlite3.Row
    return conn


def search_onsides(drug_name: str, limit: int = 30) -> list[dict]:
    """Search OnSIDES by drug ingredient name (case-insensitive substring).

    Returns list of dicts: ingredient, effect, meddra_id, source, label_count.
    """
    if not os.path.isfile(ONSIDES_DB):
        return []
    sql = """
    SELECT
        ri.name                AS ingredient,
        ae.effect_meddra_id    AS meddra_id,
        ma.name                AS effect,
        pl.source              AS source,
        COUNT(DISTINCT pl.label_id) AS label_count
    FROM vocab_rxnorm_ingredient ri
    JOIN vocab_rxnorm_ingredient_to_product ip ON ri.rxnorm_id = ip.ingredient_id
    JOIN vocab_rxnorm_product               rp ON ip.product_id = rp.rxnorm_id
    JOIN product_to_rxnorm                  pr ON rp.rxnorm_id = pr.rxnorm_product_id
    JOIN product_label                      pl ON pr.label_id  = pl.label_id
    JOIN product_adverse_effect             ae ON pl.label_id  = ae.product_label_id
    JOIN vocab_meddra_adverse_effect        ma ON ae.effect_meddra_id = ma.meddra_id
    WHERE LOWER(ri.name) LIKE ?
    GROUP BY ri.name, ae.effect_meddra_id, ma.name, pl.source
    ORDER BY label_count DESC
    LIMIT ?
    """
    pattern = f"%{drug_name.strip().lower()}%"
    with _onsides_conn() as conn:
        rows = conn.execute(sql, (pattern, limit)).fetchall()
    return [dict(r) for r in rows]


# ── OFFSIDES helpers (gzipped CSV) ──────────────────────────

def _load_offsides_index() -> dict[str, list[dict]]:
    """Build in-memory index: lowercase drug name → list of side-effect rows."""
    global _offsides_index
    if _offsides_index is not None:
        return _offsides_index
    if not os.path.isfile(OFFSIDES_GZ):
        _offsides_index = {}
        return _offsides_index
    idx: dict[str, list[dict]] = {}
    with gzip.open(OFFSIDES_GZ, "rt", encoding="utf-8", errors="replace") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            key = (row.get("drug_concept_name") or "").strip().lower()
            if not key:
                continue
            entry = {
                "drug_rxnorm_id":     row.get("drug_rxnorm_id", ""),
                "drug":               row.get("drug_concept_name", ""),
                "condition_meddra_id": row.get("condition_meddra_id", ""),
                "condition":          row.get("condition_concept_name", ""),
                "PRR":                _float(row.get("PRR")),
                "PRR_error":          _float(row.get("PRR_error")),
                "A": _int(row.get("A")),
                "B": _int(row.get("B")),
                "C": _int(row.get("C")),
                "D": _int(row.get("D")),
                "mean_reporting_frequency": _float(row.get("mean_reporting_frequency")),
            }
            idx.setdefault(key, []).append(entry)
    _offsides_index = idx
    return _offsides_index


def search_offsides(drug_name: str, limit: int = 20) -> list[dict]:
    """Search OFFSIDES by drug name (case-insensitive substring match).

    Returns list of dicts: drug, condition, PRR, A/B/C/D, mean_reporting_frequency.
    """
    idx = _load_offsides_index()
    query = drug_name.strip().lower()
    results: list[dict] = []
    for key, rows in idx.items():
        if query in key:
            results.extend(rows)
    results.sort(key=lambda r: r.get("PRR") or 0, reverse=True)
    return results[:limit]


# ── KidSIDES helpers (gzipped CSVs) ─────────────────────────

def _load_kidsides_dicts():
    """Load KidSIDES dictionary files (small, cached)."""
    global _kidsides_drug, _kidsides_event, _kidsides_phase
    if _kidsides_drug is not None:
        return

    _kidsides_drug = {}
    _kidsides_event = {}
    _kidsides_phase = {}

    drug_path = os.path.join(KIDSIDES_DIR, "drug.csv.gz")
    if os.path.isfile(drug_path):
        with gzip.open(drug_path, "rt", encoding="utf-8", errors="replace") as fh:
            for row in csv.DictReader(fh):
                cid = row.get("concept_id", "")
                name = row.get("concept_name", "")
                if cid and name:
                    _kidsides_drug[cid] = name

    event_path = os.path.join(KIDSIDES_DIR, "event.csv.gz")
    if os.path.isfile(event_path):
        with gzip.open(event_path, "rt", encoding="utf-8", errors="replace") as fh:
            for row in csv.DictReader(fh):
                cid = row.get("concept_id", "")
                name = row.get("concept_name", "")
                if cid and name:
                    _kidsides_event[cid] = name

    dict_path = os.path.join(KIDSIDES_DIR, "dictionary.csv.gz")
    if os.path.isfile(dict_path):
        with gzip.open(dict_path, "rt", encoding="utf-8", errors="replace") as fh:
            for row in csv.DictReader(fh):
                code = row.get("nichd", row.get("nichd_code", ""))
                label = row.get("description", row.get("label", ""))
                if code and label:
                    _kidsides_phase[code] = label


def search_kidsides(drug_name: str, limit: int = 20) -> list[dict]:
    """Search KidSIDES by drug name (substring match on dictionary).

    Returns list of dicts: drug, event, nichd_phase, gam_score, …
    """
    _load_kidsides_dicts()
    query_lower = drug_name.strip().lower()

    # find matching drug concept IDs
    matched_ids = set()
    for cid, name in (_kidsides_drug or {}).items():
        if query_lower in name.lower():
            matched_ids.add(cid)
    if not matched_ids:
        return []

    ade_path = os.path.join(KIDSIDES_DIR, "ade_nichd.csv.gz")
    if not os.path.isfile(ade_path):
        return []

    results: list[dict] = []
    with gzip.open(ade_path, "rt", encoding="utf-8", errors="replace") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            dcid = row.get("drug_concept_id", "")
            if dcid not in matched_ids:
                continue
            ecid = row.get("event_concept_id", "")
            nichd = row.get("nichd", row.get("nichd_code", ""))
            results.append({
                "drug":       (_kidsides_drug or {}).get(dcid, dcid),
                "event":      (_kidsides_event or {}).get(ecid, ecid),
                "nichd_phase": (_kidsides_phase or {}).get(nichd, nichd),
                "gam_score":  _float(row.get("gam_score", row.get("score"))),
                "ror":        _float(row.get("ror")),
                "ror_lower":  _float(row.get("ror_lower")),
                "ror_upper":  _float(row.get("ror_upper")),
            })
            if len(results) >= limit:
                break
    return results


# ── parsing helpers ─────────────────────────────────────────

def _float(v) -> float | None:
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (ValueError, TypeError):
        return None

def _int(v) -> int | None:
    if v is None or v == "":
        return None
    try:
        return int(v)
    except (ValueError, TypeError):
        return None


# ── unified interface ───────────────────────────────────────

def search(entity: str, limit: int = 20) -> dict:
    """Query all available nSIDES sources for a drug entity.

    Parameters
    ----------
    entity : str
        Drug name (e.g. "aspirin", "metformin").
    limit : int
        Max results per source.

    Returns
    -------
    dict with keys: entity, onsides, offsides, kidsides.
    """
    return {
        "entity":   entity,
        "onsides":  search_onsides(entity, limit=limit),
        "offsides": search_offsides(entity, limit=limit),
        "kidsides": search_kidsides(entity, limit=limit),
    }


def search_batch(entities: list[str], limit: int = 20) -> list[dict]:
    """Query multiple drug entities."""
    return [search(e, limit=limit) for e in entities]


def summarize(result: dict) -> str:
    """Compact text summary from a single search() result."""
    lines = [f"=== {result['entity']} ==="]

    # OnSIDES
    ons = result.get("onsides", [])
    if ons:
        lines.append(f"  OnSIDES ({len(ons)} label-extracted ADEs):")
        for r in ons[:8]:
            src = r.get("source", "?")
            cnt = r.get("label_count", "")
            lines.append(f"    - {r['effect']} [{src}, {cnt} labels]")
    else:
        lines.append("  OnSIDES: (no results)")

    # OFFSIDES
    off = result.get("offsides", [])
    if off:
        lines.append(f"  OffSIDES ({len(off)} off-label signals):")
        for r in off[:8]:
            prr = r.get("PRR")
            prr_s = f" PRR={prr:.2f}" if prr else ""
            lines.append(f"    - {r['condition']}{prr_s}")
    else:
        lines.append("  OffSIDES: (no results)")

    # KidSIDES
    kid = result.get("kidsides", [])
    if kid:
        lines.append(f"  KidSIDES ({len(kid)} pediatric signals):")
        for r in kid[:8]:
            phase = r.get("nichd_phase", "?")
            ror = r.get("ror")
            ror_s = f" ROR={ror:.2f}" if ror else ""
            lines.append(f"    - {r['event']} [{phase}]{ror_s}")
    else:
        lines.append("  KidSIDES: (no results)")

    return "\n".join(lines)


def to_json(result: dict) -> str:
    """JSON serialization for pipeline use."""
    return json.dumps(result, ensure_ascii=False, indent=2, default=str)


# ── usage example ───────────────────────────────────────────

if __name__ == "__main__":
    # --- single entity ---
    print("=== Single query: aspirin ===")
    res = search("aspirin", limit=5)
    print(summarize(res))

    # --- batch query ---
    print("\n=== Batch query ===")
    for r in search_batch(["metformin", "ibuprofen"], limit=3):
        print(summarize(r))
        print()
