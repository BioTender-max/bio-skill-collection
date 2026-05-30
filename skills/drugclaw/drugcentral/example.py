"""
18_DrugCentral – DrugCentral Comprehensive Drug Pharmacology Query
Category: Drug-centric | Type: DB | Subcategory: Drug Knowledgebase
Link: https://drugcentral.org/
Paper: https://academic.oup.com/nar/article/51/D1/D1276/6885038

DrugCentral integrates structure, bioactivity, regulatory, pharmacological
action, and disease indication data for approved drugs (FDA, EMA, PMDA).

Data files (from https://drugcentral.org/download):
  • structures.smiles.tsv          – SMILES, InChI, InChIKey, ID, INN, CAS_RN
  • drug.target.interaction.tsv    – drug-target interaction profiles
  • FDA+EMA+PMDA_Approved.csv      – approval status (ID, drug_name)

No API key required. All data freely available.
"""

import os
import csv
import gzip
import json
import re
from pathlib import Path
from typing import Union

# ── Config ──────────────────────────────────────────────────────────────
def _resolve_data_dir() -> str:
    override = os.environ.get("DRUGCENTRAL_DIR")
    if override:
        return override
    return str(
        Path(__file__).resolve().parents[3]
        / "resources_metadata"
        / "drug_knowledgebase"
        / "DrugCentral"
    )


DATA_DIR = _resolve_data_dir()

STRUCTURES_FILE = os.path.join(DATA_DIR, "structures.smiles.tsv")
DTI_FILE        = os.path.join(DATA_DIR, "drug.target.interaction.tsv")
APPROVED_FILE   = os.path.join(DATA_DIR, "FDA+EMA+PMDA_Approved.csv")

# ── Lazy-loaded caches ──────────────────────────────────────────────────
_cache: dict = {}


def _load_structures(path: str = STRUCTURES_FILE) -> list[dict]:
    """Load structures.smiles.tsv → list[dict].
    Columns: SMILES, InChI, InChIKey, ID, INN, CAS_RN
    """
    if "structures" in _cache:
        return _cache["structures"]
    rows = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for r in reader:
            # normalise ID to int string
            if r.get("ID"):
                r["ID"] = r["ID"].strip()
            rows.append(r)
    _cache["structures"] = rows
    return rows


def _load_dti(path: str = DTI_FILE) -> list[dict]:
    """Load drug.target.interaction.tsv.gz → list[dict].
    Auto-detects columns from header line.
    """
    if "dti" in _cache:
        return _cache["dti"]
    rows = []
    opener = gzip.open if path.endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for r in reader:
            rows.append(r)
    _cache["dti"] = rows
    return rows


def _load_approved(path: str = APPROVED_FILE) -> dict:
    """Load approved CSV → {id_str: drug_name}."""
    if "approved" in _cache:
        return _cache["approved"]
    mapping: dict[str, str] = {}
    if not os.path.exists(path):
        _cache["approved"] = mapping
        return mapping
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                mapping[row[0].strip()] = row[1].strip()
    _cache["approved"] = mapping
    return mapping


# ── Input detection ─────────────────────────────────────────────────────

_PAT_DC_ID  = re.compile(r"^\d{1,5}$")                        # DrugCentral numeric ID
_PAT_CAS    = re.compile(r"^\d{2,7}-\d{2}-\d$")               # CAS registry number
_PAT_INCHI  = re.compile(r"^[A-Z]{14}(-[A-Z]{10}(-[A-Z])?)?$")  # InChIKey (full or prefix)


def _detect_type(entity: str) -> str:
    """Return: 'dc_id' | 'cas' | 'inchikey' | 'text'."""
    e = entity.strip()
    if _PAT_DC_ID.match(e):
        return "dc_id"
    if _PAT_CAS.match(e):
        return "cas"
    if _PAT_INCHI.match(e):
        return "inchikey"
    return "text"


# ── Core search ─────────────────────────────────────────────────────────

def _search_structures(entity: str) -> list[dict]:
    """Search structures file by auto-detected entity type."""
    structs = _load_structures()
    etype = _detect_type(entity)
    e = entity.strip()
    hits = []
    if etype == "dc_id":
        hits = [r for r in structs if r.get("ID") == e]
    elif etype == "cas":
        hits = [r for r in structs if r.get("CAS_RN", "").strip() == e]
    elif etype == "inchikey":
        eu = e.upper()
        hits = [r for r in structs if (r.get("InChIKey") or "").upper().startswith(eu)]
    else:  # free text → substring on INN
        el = e.lower()
        hits = [r for r in structs if el in (r.get("INN") or "").lower()]
    return hits


def _search_dti(dc_ids: set) -> list[dict]:
    """Get target interactions for a set of DrugCentral IDs."""
    if not os.path.exists(DTI_FILE):
        return []
    dti = _load_dti()
    # Try common column names for drug ID
    id_col = None
    if dti:
        first = dti[0]
        for c in ("STRUCT_ID", "struct_id", "ID", "drug_id", "DrugCentral_Id"):
            if c in first:
                id_col = c
                break
    if not id_col:
        return []
    return [r for r in dti if r.get(id_col, "").strip() in dc_ids]


def search(entity: str) -> dict:
    """Search DrugCentral by a single entity.
    Returns dict with keys: entity, type, structures, targets, approved.
    """
    e = entity.strip()
    etype = _detect_type(e)
    structs = _search_structures(e)

    # Collect DC IDs from structure hits
    dc_ids = {r["ID"] for r in structs if r.get("ID")}

    # Target interactions
    targets = _search_dti(dc_ids) if dc_ids else []

    # Approval status
    approved_map = _load_approved()
    approval = []
    for did in dc_ids:
        if did in approved_map:
            approval.append({"id": did, "name": approved_map[did], "approved": True})

    return {
        "entity": e,
        "type": etype,
        "structures": structs[:50],
        "targets": targets[:50],
        "approved": approval,
    }


def search_batch(entities: Union[list, str]) -> dict:
    """Search multiple entities. Accepts list or comma-separated string."""
    if isinstance(entities, str):
        entities = [x.strip() for x in entities.split(",") if x.strip()]
    return {e: search(e) for e in entities}


# ── Summariser (LLM-friendly) ──────────────────────────────────────────

def summarize(result: dict, entity: str = "") -> str:
    """Compact text summary for LLM consumption."""
    e = entity or result.get("entity", "?")
    lines = [f"=== DrugCentral: {e} (type={result.get('type','?')}) ==="]

    structs = result.get("structures", [])
    if not structs:
        lines.append("  No structure hits.")
        return "\n".join(lines)

    for s in structs[:10]:
        parts = [f"ID={s.get('ID','')}"]
        if s.get("INN"):
            parts.append(f"INN={s['INN']}")
        if s.get("CAS_RN"):
            parts.append(f"CAS={s['CAS_RN']}")
        if s.get("InChIKey"):
            parts.append(f"InChIKey={s['InChIKey'][:14]}…")
        lines.append("  " + " | ".join(parts))

    # Approval
    approvals = result.get("approved", [])
    if approvals:
        names = [a["name"] for a in approvals[:5]]
        lines.append(f"  Approved: {', '.join(names)}")

    # Targets
    targets = result.get("targets", [])
    if targets:
        lines.append(f"  Targets ({len(targets)} hits):")
        seen = set()
        for t in targets[:20]:
            gene = (t.get("GENE") or t.get("gene") or
                    t.get("TARGET_NAME") or t.get("target_name") or "?")
            act  = (t.get("ACTION_TYPE") or t.get("action_type") or "")
            key = f"{gene}|{act}"
            if key in seen:
                continue
            seen.add(key)
            val = t.get("ACT_VALUE") or t.get("act_value") or ""
            unit = t.get("ACT_UNIT") or t.get("act_unit") or ""
            atype = t.get("ACT_TYPE") or t.get("act_type") or ""
            detail = f" ({atype}={val}{unit})" if val else ""
            lines.append(f"    {gene}: {act}{detail}")
    elif structs:
        lines.append("  Targets: (DTI file not loaded or no interactions)")

    return "\n".join(lines)


def to_json(result: dict) -> str:
    """Return JSON string of search result."""
    return json.dumps(result, ensure_ascii=False, indent=2, default=str)


# ── Main ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("DrugCentral Query Skill – Demo")
    print(f"DATA_DIR = {DATA_DIR}")
    print("=" * 60)

    # --- Single search: drug name ---
    print("\n>>> search('aspirin')")
    r = search("aspirin")
    print(summarize(r))

    # --- Single search: DrugCentral ID ---
    print("\n>>> search('2')")
    r = search("2")
    print(summarize(r))

    # --- Single search: CAS number ---
    print("\n>>> search('50-78-2')")
    r = search("50-78-2")
    print(summarize(r))

    # --- Single search: InChIKey prefix ---
    print("\n>>> search('BSYNRYMUTXBXSQ')")
    r = search("BSYNRYMUTXBXSQ")
    print(summarize(r))

    # --- Batch search ---
    print("\n>>> search_batch(['metformin', 'ibuprofen', '50-78-2'])")
    batch = search_batch(["metformin", "ibuprofen", "50-78-2"])
    for entity, res in batch.items():
        print(summarize(res, entity))
        print()

    # --- JSON output ---
    print("\n>>> to_json (first result, structures only)")
    r = search("aspirin")
    mini = {"entity": r["entity"], "structures": r["structures"][:1]}
    print(to_json(mini))
