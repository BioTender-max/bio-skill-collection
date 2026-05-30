"""
DrugRepoBank - Drug Repurposing Evidence Compilation
Category: Drug-centric | Type: DB | Subcategory: Drug Repurposing
Link: https://awi.cuhk.edu.cn/DrugRepoBank/php/index.php
Paper: https://academic.oup.com/database/article/doi/10.1093/database/baae051/7712639

DrugRepoBank collects and curates drug repurposing candidates and evidence from
experimental, computational, and clinical sources.  Four local CSV tables:
  Drug.csv               – drug identifiers & structures
  DrugTargetInteraction  – drug ↔ target links with MOA
  Literature.csv         – repurposing evidence per drug–disease pair
  Targets.csv            – target annotations & pathways

Access method: Local CSV files downloaded from the DrugRepoBank website.
"""

import csv
import os
import re
import json
from pathlib import Path
from typing import Optional

# ── data paths ──────────────────────────────────────────────────────────
DATA_DIR = str(
    Path(__file__).resolve().parents[3]
    / "resources_metadata"
    / "drug_repurposing"
    / "DrugRepoBank"
)
DRUG_PATH = os.path.join(DATA_DIR, "Drug.csv")
DTI_PATH = os.path.join(DATA_DIR, "DrugTargetInteraction.csv")
LIT_PATH = os.path.join(DATA_DIR, "Literature.csv")
TARGET_PATH = os.path.join(DATA_DIR, "Targets.csv")


# ── CSV loader ──────────────────────────────────────────────────────────
def _load_csv(path: str) -> list[dict]:
    """Load a CSV file and return a list of row-dicts."""
    with open(path, newline="", encoding="utf-8", errors="replace") as fh:
        reader = csv.DictReader(fh)
        return list(reader)


def load_all() -> dict:
    """Load all four tables and return them in a dict keyed by table name."""
    return {
        "drug": _load_csv(DRUG_PATH),
        "dti": _load_csv(DTI_PATH),
        "lit": _load_csv(LIT_PATH),
        "target": _load_csv(TARGET_PATH),
    }


# ── entity type detection ───────────────────────────────────────────────
_PATTERNS = [
    (re.compile(r"^DB\d{5,}$", re.I), "drugbank_id"),
    (re.compile(r"^T\d{4,}$"), "target_id"),
    (re.compile(r"^[A-Z0-9]+_[A-Z]+$"), "uniprot_id"),
    (re.compile(r"^CHEMBL\d+$", re.I), "chembl_id"),
    (re.compile(r"^\d{3,}$"), "pubchem_cid"),
]


def detect_entity_type(entity: str) -> str:
    """Return one of: drugbank_id, target_id, uniprot_id, chembl_id,
    pubchem_cid, or free_text."""
    e = entity.strip()
    for pat, etype in _PATTERNS:
        if pat.match(e):
            return etype
    return "free_text"


# ── core search ─────────────────────────────────────────────────────────
def _ci(a: str, b: str) -> bool:
    """Case-insensitive substring match."""
    return b.lower() in a.lower()


def _search_drug(tables: dict, entity: str, etype: str) -> list[dict]:
    col_map = {
        "drugbank_id": "DrugBank_ID",
        "chembl_id": "ChEMBL ID",
        "pubchem_cid": "PubChem_Compound_ID",
    }
    rows = tables["drug"]
    if etype in col_map:
        col = col_map[etype]
        return [r for r in rows if (r.get(col) or "").strip().upper() == entity.upper()]
    # free_text: match Name
    return [r for r in rows if _ci(r.get("Name", ""), entity)]


def _search_target(tables: dict, entity: str, etype: str) -> list[dict]:
    rows = tables["target"]
    if etype == "target_id":
        return [r for r in rows if (r.get("TargetID") or "").upper() == entity.upper()]
    if etype == "uniprot_id":
        return [r for r in rows if (r.get("UniprotID") or "").upper() == entity.upper()]
    # free_text: match TargetName or TargetGeneName
    return [r for r in rows if _ci(r.get("TargetName", ""), entity)
            or _ci(r.get("TargetGeneName", ""), entity)]


def _search_dti(tables: dict, entity: str, etype: str) -> list[dict]:
    rows = tables["dti"]
    if etype == "drugbank_id":
        # DrugID in DTI uses TTD-style IDs; match via PubChem bridge
        drug_hits = _search_drug(tables, entity, etype)
        pcids = {r.get("PubChem_Compound_ID", "").strip() for r in drug_hits}
        return [r for r in rows if (r.get("PubchemID") or "").strip() in pcids]
    if etype == "pubchem_cid":
        return [r for r in rows if (r.get("PubchemID") or "").strip() == entity.strip()]
    if etype == "target_id":
        return [r for r in rows if (r.get("TargetID") or "").upper() == entity.upper()]
    if etype == "uniprot_id":
        return [r for r in rows if (r.get("UniprotID") or "").upper() == entity.upper()]
    # free_text: try drug name → PubChem bridge, then target name
    drug_hits = _search_drug(tables, entity, "free_text")
    pcids = {r.get("PubChem_Compound_ID", "").strip() for r in drug_hits}
    dti_by_drug = [r for r in rows if (r.get("PubchemID") or "").strip() in pcids]
    # also match target side
    tgt_hits = _search_target(tables, entity, "free_text")
    tids = {r.get("TargetID", "") for r in tgt_hits}
    uids = {r.get("UniprotID", "") for r in tgt_hits}
    dti_by_tgt = [r for r in rows
                  if (r.get("TargetID") or "") in tids
                  or (r.get("UniprotID") or "") in uids]
    seen = set()
    merged = []
    for r in dti_by_drug + dti_by_tgt:
        key = (r.get("DrugID", ""), r.get("TargetID", ""), r.get("UniprotID", ""))
        if key not in seen:
            seen.add(key)
            merged.append(r)
    return merged


def _search_lit(tables: dict, entity: str, etype: str) -> list[dict]:
    rows = tables["lit"]
    if etype == "drugbank_id":
        return [r for r in rows if (r.get("DrugID") or "").strip().upper() == entity.upper()]
    if etype == "pubchem_cid":
        return [r for r in rows if (r.get("PubChemID") or "").strip() == entity.strip()]
    # free_text: match DrugName, Target, Disease, or NewDisease
    return [r for r in rows if _ci(r.get("DrugName", ""), entity)
            or _ci(r.get("Target", ""), entity)
            or _ci(r.get("Disease", ""), entity)
            or _ci(r.get("NewDisease", ""), entity)]


def search(tables: dict, entity: str) -> dict:
    """
    Search DrugRepoBank for a single entity string.
    Auto-detects entity type.  Returns dict with keys:
      entity, entity_type, drug, target, dti, literature
    Each value is a list of matching row-dicts (may be empty).
    """
    entity = entity.strip()
    etype = detect_entity_type(entity)
    return {
        "entity": entity,
        "entity_type": etype,
        "drug": _search_drug(tables, entity, etype),
        "target": _search_target(tables, entity, etype),
        "dti": _search_dti(tables, entity, etype),
        "literature": _search_lit(tables, entity, etype),
    }


def search_batch(tables: dict, entities: list[str]) -> dict[str, dict]:
    """Search multiple entities. Returns {entity: search_result}."""
    return {e: search(tables, e) for e in entities}


# ── compact LLM-readable output ────────────────────────────────────────
def summarize(result: dict) -> str:
    """One-paragraph LLM-readable summary of a search() result."""
    e = result["entity"]
    etype = result["entity_type"]
    parts = [f"[{e}] (detected as {etype})"]

    # drug info
    drugs = result["drug"]
    if drugs:
        d = drugs[0]
        parts.append(f"Drug: {d.get('Name','')} | {d.get('DrugBank_ID','')} | "
                      f"Groups={d.get('Drug Groups','')} | "
                      f"PubChem={d.get('PubChem_Compound_ID','')}")

    # target info
    targets = result["target"]
    if targets:
        for t in targets[:5]:
            parts.append(f"Target: {t.get('TargetName','')} | {t.get('TargetGeneName','')} | "
                          f"{t.get('UniprotID','')} | Type={t.get('TargetType','')}")

    # DTI
    dtis = result["dti"]
    if dtis:
        dti_strs = [f"{r.get('UniprotID','')}({r.get('MOA','')},{r.get('Highest_status','')})"
                    for r in dtis[:10]]
        parts.append(f"DTI({len(dtis)}): " + "; ".join(dti_strs))

    # literature (repurposing evidence)
    lits = result["literature"]
    if lits:
        lit_strs = []
        for r in lits[:10]:
            ev_types = []
            for k in ("Insilico", "Invitro", "Invivo", "Clinicaltrial"):
                if (r.get(k) or "").strip():
                    ev_types.append(k)
            ev_tag = ",".join(ev_types) if ev_types else "n/a"
            lit_strs.append(f"{r.get('DrugName','')}→{r.get('NewDisease','') or r.get('Disease','')}[{ev_tag}]")
        parts.append(f"Repurpose({len(lits)}): " + "; ".join(lit_strs))

    if len(parts) == 1:
        parts.append("No results found.")
    return " | ".join(parts)


def to_json(result: dict) -> str:
    """Return search() result as a JSON string (compact)."""
    # trim heavy fields for pipeline use
    slim = {
        "entity": result["entity"],
        "entity_type": result["entity_type"],
        "drug": [{k: v for k, v in r.items()
                  if k in ("DrugBank_ID", "Name", "Drug Groups",
                           "PubChem_Compound_ID", "ChEMBL ID", "SMILES")}
                 for r in result["drug"]],
        "target": [{k: v for k, v in r.items()
                    if k in ("TargetID", "UniprotID", "TargetName",
                             "TargetGeneName", "TargetType")}
                   for r in result["target"]],
        "dti": result["dti"],
        "literature": [{k: v for k, v in r.items()
                        if k in ("DrugName", "DrugID", "Target", "Disease",
                                 "NewDisease", "NewDirectTarget",
                                 "NewIndirectTarget", "Evidence",
                                 "Insilico", "Invitro", "Invivo",
                                 "Clinicaltrial", "PMID")}
                       for r in result["literature"]],
    }
    return json.dumps(slim, indent=2, ensure_ascii=False)


# ── main: runnable examples ─────────────────────────────────────────────
if __name__ == "__main__":
    tables = load_all()
    print(f"Loaded: Drug={len(tables['drug'])} DTI={len(tables['dti'])} "
          f"Lit={len(tables['lit'])} Target={len(tables['target'])}")

    # 1) Search by drug name
    print("\n=== search('metformin') ===")
    r = search(tables, "metformin")
    print(summarize(r))

    # 2) Search by DrugBank ID
    print("\n=== search('DB00945') ===")
    r = search(tables, "DB00945")
    print(summarize(r))

    # 3) Search by target ID
    print("\n=== search('T47101') ===")
    r = search(tables, "T47101")
    print(summarize(r))

    # 4) Search by UniProt ID
    print("\n=== search('FGFR1_HUMAN') ===")
    r = search(tables, "FGFR1_HUMAN")
    print(summarize(r))

    # 5) Search by ChEMBL ID
    print("\n=== search('CHEMBL2103749') ===")
    r = search(tables, "CHEMBL2103749")
    print(summarize(r))

    # 6) Search by disease (free text)
    print("\n=== search('breast cancer') ===")
    r = search(tables, "breast cancer")
    print(summarize(r))

    # 7) Batch search
    print("\n=== search_batch ===")
    batch = search_batch(tables, ["aspirin", "DB06145", "FGFR1_HUMAN"])
    for ent, res in batch.items():
        print(summarize(res))

    # 8) JSON output
    print("\n=== to_json('aspirin') ===")
    r = search(tables, "aspirin")
    print(to_json(r)[:500], "...")
