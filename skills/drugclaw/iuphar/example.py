"""
IUPHAR/BPS Guide to Pharmacology - Expert-Curated Pharmacological Data
Category: Drug-centric | Type: DB | Subcategory: Drug Knowledgebase
Link: https://www.guidetopharmacology.org/
Paper: https://pubmed.ncbi.nlm.nih.gov/41160876/
API docs: https://www.guidetopharmacology.org/webServices.jsp
No API key required.
"""

import urllib.request
import urllib.error
import urllib.parse
import json

BASE_URL = "https://www.guidetopharmacology.org/services"
TIMEOUT = 15


# ── low-level helpers ────────────────────────────────────────────────

def _get(path: str, params: dict | None = None) -> dict | list:
    """GET request to IUPHAR REST API; returns parsed JSON.
    Returns [] on 404 (no results) so callers can fall through safely."""
    url = f"{BASE_URL}/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return []
        raise


# ── core query functions ─────────────────────────────────────────────

def search_ligand(name: str) -> list[dict]:
    """Search ligands (drugs/compounds) by name. Returns list of ligand dicts."""
    return _get("ligands", {"name": name})


def get_ligand(ligand_id: int) -> dict:
    """Get full detail for one ligand by its numeric ID."""
    return _get(f"ligands/{ligand_id}")


def search_target(name: str) -> list[dict]:
    """Search targets by name substring. Returns list of target dicts."""
    return _get("targets", {"name": name})


def get_target(target_id: int) -> dict:
    """Get full detail for one target by its numeric ID."""
    return _get(f"targets/{target_id}")


def get_interactions(target_id: int) -> list[dict]:
    """Get all ligand–target interactions for a given target ID."""
    return _get(f"targets/{target_id}/interactions")


# ── entity-oriented wrappers (single / batch) ───────────────────────

def query_entity(entity: str) -> dict:
    """
    Query a single entity (drug/compound name or target name).
    Auto-detects type: tries ligand search first, falls back to target search.
    Returns:
        {"entity": str, "type": "ligand"|"target"|"not_found",
         "results": [...], "interactions": [...]}
    """
    out = {"entity": entity, "type": "not_found", "results": [], "interactions": []}

    # 1) try ligand
    hits = search_ligand(entity)
    if hits:
        out["type"] = "ligand"
        out["results"] = [_slim_ligand(h) for h in hits]
        return out

    # 2) try target
    hits = search_target(entity)
    if hits:
        out["type"] = "target"
        out["results"] = [_slim_target(h) for h in hits]
        # attach top interactions for first hit
        tid = hits[0].get("targetId")
        if tid:
            try:
                ixns = get_interactions(tid)
                out["interactions"] = [_slim_interaction(i) for i in ixns[:10]]
            except Exception:
                pass
        return out

    return out


def query_entities(entities: list[str]) -> dict[str, dict]:
    """Batch wrapper: query a list of entity names. Returns {name: result}."""
    return {e: query_entity(e) for e in entities}


# ── summarise (LLM-friendly text) ───────────────────────────────────

def summarize(result: dict) -> str:
    """Turn a query_entity result into concise readable text."""
    e = result["entity"]
    if result["type"] == "not_found":
        return f"[{e}] Not found in IUPHAR."

    lines = [f"[{e}] Type: {result['type']}"]
    for r in result["results"][:5]:
        lines.append(f"  • {r}")
    if result.get("interactions"):
        lines.append("  Interactions:")
        for ix in result["interactions"][:5]:
            lines.append(f"    – {ix}")
    return "\n".join(lines)


# ── slim formatters (keep only useful fields) ────────────────────────

def _slim_ligand(d: dict) -> dict:
    return {k: d.get(k) for k in
            ("ligandId", "name", "type", "approved", "inn",
             "species", "radioactive", "labelled")}


def _slim_target(d: dict) -> dict:
    return {k: d.get(k) for k in
            ("targetId", "name", "abbreviation", "type",
             "familyIds", "subunitIds", "geneIds")}


def _slim_interaction(d: dict) -> dict:
    return {k: d.get(k) for k in
            ("ligandId", "targetId", "type", "action",
             "actionComment", "affinityRange", "affinity",
             "affinityType", "endogenous", "species")}


# ── usage examples ───────────────────────────────────────────────────

if __name__ == "__main__":

    # --- single entity query (ligand) ---
    r = query_entity("morphine")
    print(summarize(r))

    # --- single entity query (target) ---
    r = query_entity("5-HT1A receptor")
    print(summarize(r))

    # --- batch query ---
    results = query_entities(["aspirin", "GABA receptor", "ibuprofen"])
    for name, res in results.items():
        print(summarize(res))
        print()

    # --- direct ligand detail by ID ---
    detail = get_ligand(1455)      # morphine ligand ID
    print(json.dumps(_slim_ligand(detail), indent=2))

    # --- direct target interactions by ID ---
    ixns = get_interactions(1)     # target ID 1
    for ix in ixns[:3]:
        print(_slim_interaction(ix))