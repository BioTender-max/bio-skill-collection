"""
SIDER - Side Effect Resource
Category: Drug-centric | Type: DB | Subcategory: Adverse Drug Reaction (ADR)
Link: http://sideeffects.embl.de/
Paper: https://doi.org/10.1093/nar/gkv1075

Query local SIDER flat files. Accepts one entity or a list of entities
(drug name, STITCH ID, UMLS CUI, ATC code, or side-effect name) and
returns related records from SIDER tables.
"""

import os
import csv
import gzip
from pathlib import Path
from collections import defaultdict
from typing import Union

# ── Data path ────────────────────────────────────────────────────────
DATA_DIR = str(
    Path(__file__).resolve().parents[3] / "resources_metadata" / "adr" / "SIDER"
)

# ── Helpers ──────────────────────────────────────────────────────────

def _open_file(path: str):
    """Open plain or gzipped TSV transparently."""
    if path.endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8")
    return open(path, encoding="utf-8")


def _find_file(name: str) -> str:
    """Locate a file, trying both plain and .gz variants."""
    for ext in ("", ".gz"):
        p = os.path.join(DATA_DIR, name + ext)
        if os.path.exists(p):
            return p
    raise FileNotFoundError(f"Cannot find {name}[.gz] in {DATA_DIR}")


# ── Loaders (lazy, cached) ──────────────────────────────────────────

_cache: dict = {}


def _load_drug_names() -> dict:
    """Return {stitch_flat: drug_name} and {drug_name_lower: stitch_flat}."""
    if "drug_names" in _cache:
        return _cache["drug_names"]
    id2name, name2id = {}, {}
    with _open_file(_find_file("drug_names.tsv")) as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 2:
                sid, name = parts[0], parts[1]
                id2name[sid] = name
                name2id[name.lower()] = sid
    _cache["drug_names"] = {"id2name": id2name, "name2id": name2id}
    return _cache["drug_names"]


def _load_drug_atc() -> dict:
    """Return {stitch_flat: [atc_codes]} and {atc_code: [stitch_flats]}."""
    if "drug_atc" in _cache:
        return _cache["drug_atc"]
    id2atc = defaultdict(list)
    atc2id = defaultdict(list)
    with _open_file(_find_file("drug_atc.tsv")) as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 2:
                sid, atc = parts[0], parts[1]
                id2atc[sid].append(atc)
                atc2id[atc].append(sid)
    _cache["drug_atc"] = {"id2atc": dict(id2atc), "atc2id": dict(atc2id)}
    return _cache["drug_atc"]


def _load_side_effects() -> list[dict]:
    """Load meddra_all_se.tsv → list of record dicts."""
    if "all_se" in _cache:
        return _cache["all_se"]
    cols = ["stitch_flat", "stitch_stereo", "umls_label", "meddra_type",
            "umls_meddra", "side_effect"]
    rows = []
    with _open_file(_find_file("meddra_all_se.tsv")) as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 6:
                rows.append(dict(zip(cols, parts[:6])))
    _cache["all_se"] = rows
    return rows


def _load_indications() -> list[dict]:
    """Load meddra_all_indications.tsv → list of record dicts."""
    if "indications" in _cache:
        return _cache["indications"]
    cols = ["stitch_flat", "umls_label", "method", "concept_name",
            "meddra_type", "umls_meddra", "meddra_name"]
    rows = []
    with _open_file(_find_file("meddra_all_indications.tsv")) as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 7:
                rows.append(dict(zip(cols, parts[:7])))
    _cache["indications"] = rows
    return rows


def _load_freq() -> list[dict]:
    """Load meddra_freq.tsv → list of record dicts."""
    if "freq" in _cache:
        return _cache["freq"]
    cols = ["stitch_flat", "stitch_stereo", "umls_label", "placebo",
            "freq_desc", "freq_lower", "freq_upper",
            "meddra_type", "umls_meddra", "side_effect"]
    rows = []
    with _open_file(_find_file("meddra_freq.tsv")) as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 10:
                rows.append(dict(zip(cols, parts[:10])))
    _cache["freq"] = rows
    return rows


# ── Entity type detection ────────────────────────────────────────────

def _detect_type(entity: str) -> str:
    """
    Heuristic type detection:
      CIDxxxxxxx  → stitch_id
      Cxxxxxxx    → umls_cui
      [A-Z]##...  → atc_code   (e.g. N05BA01)
      otherwise   → text       (drug name or side-effect name)
    """
    e = entity.strip()
    if e.upper().startswith("CID"):
        return "stitch_id"
    if len(e) == 8 and e[0] == "C" and e[1:].isdigit():
        return "umls_cui"
    if len(e) == 7 and e[0].isalpha() and e[1:3].isdigit():
        return "atc_code"
    return "text"


# ── Core search ──────────────────────────────────────────────────────

def search(entity: str) -> dict:
    """
    Query SIDER for a single entity.

    Returns dict with keys: entity, entity_type, drug_name, stitch_id,
    atc_codes, side_effects (list), indications (list), freq (list).
    """
    etype = _detect_type(entity)
    dn = _load_drug_names()
    atc_data = _load_drug_atc()

    # Resolve to stitch_flat id(s)
    stitch_ids = set()
    drug_name = None

    if etype == "stitch_id":
        stitch_ids.add(entity.strip())
        drug_name = dn["id2name"].get(entity.strip())
    elif etype == "umls_cui":
        cui = entity.strip()
        # Search SE and indications for this CUI
        se_rows = [r for r in _load_side_effects()
                   if r["umls_label"] == cui or r["umls_meddra"] == cui]
        ind_rows = [r for r in _load_indications()
                    if r["umls_label"] == cui or r["umls_meddra"] == cui]
        for r in se_rows + ind_rows:
            stitch_ids.add(r["stitch_flat"])
        return {
            "entity": entity, "entity_type": "umls_cui",
            "matched_stitch_ids": sorted(stitch_ids),
            "side_effects": se_rows[:50],
            "indications": ind_rows[:50],
            "note": "Showing up to 50 records per category."
        }
    elif etype == "atc_code":
        ids = atc_data["atc2id"].get(entity.strip().upper(), [])
        stitch_ids.update(ids)
    else:  # text — match drug name or side-effect name
        key = entity.strip().lower()
        # Try exact drug name match first
        if key in dn["name2id"]:
            stitch_ids.add(dn["name2id"][key])
            drug_name = entity.strip()
        else:
            # Substring match on drug names
            for nm, sid in dn["name2id"].items():
                if key in nm:
                    stitch_ids.add(sid)
                    if drug_name is None:
                        drug_name = dn["id2name"].get(sid, nm)
            # Also substring match on side-effect names
            if not stitch_ids:
                se_hits = [r for r in _load_side_effects()
                           if key in r["side_effect"].lower()]
                ind_hits = [r for r in _load_indications()
                            if key in r.get("meddra_name", "").lower()
                            or key in r.get("concept_name", "").lower()]
                return {
                    "entity": entity, "entity_type": "side_effect_text",
                    "side_effects": se_hits[:50],
                    "indications": ind_hits[:50],
                    "note": "Matched as side-effect / indication text. Up to 50 records shown."
                }

    if not stitch_ids:
        return {"entity": entity, "entity_type": etype, "found": False}

    # Gather info for resolved stitch IDs
    sid_set = stitch_ids
    se = [r for r in _load_side_effects() if r["stitch_flat"] in sid_set]
    ind = [r for r in _load_indications() if r["stitch_flat"] in sid_set]
    fq = [r for r in _load_freq() if r["stitch_flat"] in sid_set]
    atc_codes = []
    for sid in sid_set:
        atc_codes.extend(atc_data["id2atc"].get(sid, []))

    if drug_name is None and sid_set:
        drug_name = dn["id2name"].get(next(iter(sid_set)))

    return {
        "entity": entity,
        "entity_type": etype,
        "drug_name": drug_name,
        "stitch_ids": sorted(sid_set),
        "atc_codes": sorted(set(atc_codes)),
        "side_effects": se[:50],
        "indications": ind[:50],
        "freq": fq[:50],
        "note": "Up to 50 records shown per category."
    }


def search_batch(entities: list[str]) -> dict[str, dict]:
    """Query SIDER for multiple entities. Returns {entity: result_dict}."""
    return {e: search(e) for e in entities}


def summarize(result: dict) -> str:
    """Return a concise human-readable summary of one search result."""
    lines = [f"Entity: {result['entity']}  (type: {result.get('entity_type', '?')})"]
    if result.get("found") is False:
        lines.append("  No records found.")
        return "\n".join(lines)
    if result.get("drug_name"):
        lines.append(f"  Drug: {result['drug_name']}")
    if result.get("stitch_ids"):
        lines.append(f"  STITCH IDs: {', '.join(result['stitch_ids'][:5])}")
    if result.get("matched_stitch_ids"):
        lines.append(f"  Matched STITCH IDs: {', '.join(result['matched_stitch_ids'][:5])}")
    if result.get("atc_codes"):
        lines.append(f"  ATC codes: {', '.join(result['atc_codes'])}")
    se = result.get("side_effects", [])
    if se:
        names = sorted({r.get("side_effect") or r.get("meddra_name", "") for r in se})
        lines.append(f"  Side effects ({len(names)}): {', '.join(names[:10])}{'...' if len(names)>10 else ''}")
    ind = result.get("indications", [])
    if ind:
        names = sorted({r.get("meddra_name") or r.get("concept_name", "") for r in ind})
        lines.append(f"  Indications ({len(names)}): {', '.join(names[:10])}{'...' if len(names)>10 else ''}")
    fq = result.get("freq", [])
    if fq:
        lines.append(f"  Freq records: {len(fq)}")
    return "\n".join(lines)


def to_json(result: dict) -> dict:
    """Pass-through (already dict). Useful for pipeline integration."""
    return result


# ── Usage examples ───────────────────────────────────────────────────

if __name__ == "__main__":
    # Example 1: Query by drug name
    res = search("aspirin")
    print(summarize(res))
    print()

    # Example 2: Query by STITCH ID
    res = search("CID100000085")
    print(summarize(res))
    print()

    # Example 3: Query by side-effect name
    res = search("headache")
    print(summarize(res))
    print()

    # Example 4: Batch query
    results = search_batch(["metformin", "ibuprofen", "C0011849"])
    for entity, r in results.items():
        print(summarize(r))
        print()
