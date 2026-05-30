"""
ChEMBL - Drug Bioactivity and Target Data
Category: Drug-centric | Type: DB | Subcategory: Drug-Target Interaction (DTI)
Link: https://www.ebi.ac.uk/chembl/
Paper: https://doi.org/10.1093/nar/gkad1004

ChEMBL is a manually curated database of bioactive molecules with drug-like
properties, containing binding, functional, and ADMET data.

API docs: https://chembl.gitbook.io/chembl-interface-documentation/web-services/chembl-data-web-services
No API key required.
"""

import urllib.request
import urllib.parse
import json
from typing import Union

BASE_URL = "https://www.ebi.ac.uk/chembl/api/data"


def _fetch(url: str) -> dict:
    """Internal helper: fetch JSON from URL."""
    with urllib.request.urlopen(url, timeout=15) as resp:
        return json.loads(resp.read())


# ── Molecule ────────────────────────────────────────────────

def get_molecule(chembl_id: str) -> dict:
    """Retrieve molecule data by ChEMBL ID (e.g. 'CHEMBL25')."""
    return _fetch(f"{BASE_URL}/molecule/{chembl_id}.json")


def search_molecules(name: str, limit: int = 5) -> list[dict]:
    """Search molecules by preferred name substring. Returns list of molecule dicts."""
    params = urllib.parse.urlencode({"pref_name__icontains": name, "limit": limit})
    data = _fetch(f"{BASE_URL}/molecule.json?{params}")
    return data.get("molecules", [])


# ── Bioactivity ─────────────────────────────────────────────

def get_bioactivities(chembl_id: str, limit: int = 10) -> list[dict]:
    """Get bioactivity records for a molecule ChEMBL ID. Returns list of activity dicts."""
    params = urllib.parse.urlencode({"molecule_chembl_id": chembl_id, "limit": limit})
    data = _fetch(f"{BASE_URL}/activity.json?{params}")
    return data.get("activities", [])


# ── Target ──────────────────────────────────────────────────

def get_target(chembl_id: str) -> dict:
    """Retrieve target data by ChEMBL target ID (e.g. 'CHEMBL203')."""
    return _fetch(f"{BASE_URL}/target/{chembl_id}.json")


def search_targets(gene_name: str, limit: int = 5) -> list[dict]:
    """Search drug targets by gene/protein name substring. Returns list of target dicts."""
    params = urllib.parse.urlencode({"target_synonym__icontains": gene_name, "limit": limit})
    data = _fetch(f"{BASE_URL}/target.json?{params}")
    return data.get("targets", [])


# ── Batch wrappers ──────────────────────────────────────────

def query_molecules(entities: Union[str, list[str]], limit: int = 5) -> dict:
    """
    Query molecule info for one or more entities.
    - If entity looks like a ChEMBL ID (starts with 'CHEMBL'), fetch directly.
    - Otherwise, search by name.
    Returns: {entity: [molecule_dicts]} 
    """
    if isinstance(entities, str):
        entities = [entities]
    results = {}
    for e in entities:
        e_stripped = e.strip()
        try:
            if e_stripped.upper().startswith("CHEMBL"):
                mol = get_molecule(e_stripped.upper())
                results[e_stripped] = [mol]
            else:
                results[e_stripped] = search_molecules(e_stripped, limit=limit)
        except Exception as exc:
            results[e_stripped] = [{"error": str(exc)}]
    return results


def query_targets(entities: Union[str, list[str]], limit: int = 5) -> dict:
    """
    Query target info for one or more entities.
    - If entity looks like a ChEMBL ID, fetch directly.
    - Otherwise, search by gene/protein name.
    Returns: {entity: [target_dicts]}
    """
    if isinstance(entities, str):
        entities = [entities]
    results = {}
    for e in entities:
        e_stripped = e.strip()
        try:
            if e_stripped.upper().startswith("CHEMBL"):
                tgt = get_target(e_stripped.upper())
                results[e_stripped] = [tgt]
            else:
                results[e_stripped] = search_targets(e_stripped, limit=limit)
        except Exception as exc:
            results[e_stripped] = [{"error": str(exc)}]
    return results


def query_bioactivities(chembl_ids: Union[str, list[str]], limit: int = 10) -> dict:
    """
    Get bioactivity data for one or more molecule ChEMBL IDs.
    Returns: {chembl_id: [activity_dicts]}
    """
    if isinstance(chembl_ids, str):
        chembl_ids = [chembl_ids]
    results = {}
    for cid in chembl_ids:
        cid_stripped = cid.strip().upper()
        try:
            results[cid_stripped] = get_bioactivities(cid_stripped, limit=limit)
        except Exception as exc:
            results[cid_stripped] = [{"error": str(exc)}]
    return results


# ── Summarizers (LLM-friendly compact output) ──────────────

def summarize_molecule(mol: dict) -> str:
    """One-line summary of a molecule dict."""
    props = mol.get("molecule_properties") or {}
    return (
        f"{mol.get('molecule_chembl_id', '?')} | "
        f"{mol.get('pref_name', 'N/A')} | "
        f"MW={props.get('full_mwt', '?')} | "
        f"AlogP={props.get('alogp', '?')} | "
        f"RO5_viol={props.get('num_ro5_violations', '?')}"
    )


def summarize_activity(act: dict) -> str:
    """One-line summary of an activity dict."""
    return (
        f"{act.get('molecule_chembl_id', '?')} -> "
        f"{act.get('target_chembl_id', '?')} ({act.get('target_pref_name', '?')}) | "
        f"{act.get('standard_type', '?')}={act.get('standard_value', '?')} "
        f"{act.get('standard_units', '')}"
    )


def summarize_target(tgt: dict) -> str:
    """One-line summary of a target dict."""
    return (
        f"{tgt.get('target_chembl_id', '?')} | "
        f"{tgt.get('pref_name', 'N/A')} | "
        f"type={tgt.get('target_type', '?')} | "
        f"organism={tgt.get('organism', '?')}"
    )


# ── Usage examples ──────────────────────────────────────────

if __name__ == "__main__":

    # 1. Single molecule by ChEMBL ID
    print("=== Single molecule: CHEMBL25 (Aspirin) ===")
    res = query_molecules("CHEMBL25")
    for mol in res["CHEMBL25"]:
        print(f"  {summarize_molecule(mol)}")

    # 2. Batch molecule search by name
    print("\n=== Batch molecule search: ibuprofen, metformin ===")
    res = query_molecules(["ibuprofen", "metformin"], limit=3)
    for entity, mols in res.items():
        print(f"  [{entity}]")
        for mol in mols:
            print(f"    {summarize_molecule(mol)}")

    # 3. Bioactivities for multiple molecules
    print("\n=== Bioactivities: CHEMBL25, CHEMBL1642 ===")
    res = query_bioactivities(["CHEMBL25", "CHEMBL1642"], limit=3)
    for cid, acts in res.items():
        print(f"  [{cid}]")
        for act in acts:
            print(f"    {summarize_activity(act)}")

    # 4. Single target by gene name
    print("\n=== Target search: EGFR ===")
    res = query_targets("EGFR", limit=3)
    for entity, tgts in res.items():
        print(f"  [{entity}]")
        for tgt in tgts:
            print(f"    {summarize_target(tgt)}")

    # 5. Batch target lookup by ChEMBL ID
    print("\n=== Batch target lookup: CHEMBL203, CHEMBL204 ===")
    res = query_targets(["CHEMBL203", "CHEMBL204"])
    for entity, tgts in res.items():
        print(f"  [{entity}]")
        for tgt in tgts:
            print(f"    {summarize_target(tgt)}")