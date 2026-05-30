"""
Open Targets Platform - Drug-Target Association for Disease Therapy
Category: Drug-centric | Type: DB | Subcategory: Drug-Target Interaction (DTI)
Link: https://platform.opentargets.org/
Paper: https://doi.org/10.1093/nar/gkac1046

Open Targets integrates genetic, genomic, and chemical data to identify and
prioritize drug targets for human diseases.

API docs: https://api.platform.opentargets.org/api/v4/graphql/browser
GraphQL endpoint: https://api.platform.opentargets.org/api/v4/graphql
No API key required.
"""

import urllib.request
import json
from typing import Union

GRAPHQL_URL = "https://api.platform.opentargets.org/api/v4/graphql"


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------

def run_query(query: str, variables: dict = None) -> dict:
    """Send a GraphQL query and return parsed JSON."""
    payload = {"query": query, "variables": variables or {}}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        GRAPHQL_URL, data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def _detect_type(entity: str) -> str:
    """Auto-detect entity type by ID prefix.

    Returns: 'target' | 'drug' | 'search'
    """
    e = entity.strip()
    if e.upper().startswith("ENSG"):
        return "target"
    if e.upper().startswith("CHEMBL"):
        return "drug"
    return "search"


# ---------------------------------------------------------------------------
# Core query functions
# ---------------------------------------------------------------------------

def get_target_info(ensembl_id: str) -> dict:
    """Get target info by Ensembl gene ID (e.g. ENSG00000146648)."""
    gql = """
    query($ensemblId: String!) {
      target(ensemblId: $ensemblId) {
        id
        approvedName
        approvedSymbol
        biotype
        associatedDiseases(page: {index: 0, size: 5}) {
          rows { disease { name } score }
        }
      }
    }
    """
    return run_query(gql, {"ensemblId": ensembl_id})


def get_drug_info(chembl_id: str) -> dict:
    """Get drug info by ChEMBL ID (e.g. CHEMBL941)."""
    gql = """
    query($chemblId: String!) {
      drug(chemblId: $chemblId) {
        id
        name
        drugType
        maximumClinicalTrialPhase
        indications {
          count
          rows { disease { name } maxPhaseForIndication }
        }
      }
    }
    """
    return run_query(gql, {"chemblId": chembl_id})


def search_entities(term: str) -> dict:
    """Free-text search across targets and drugs."""
    gql = """
    query($q: String!) {
      search(queryString: $q, entityNames: ["target", "drug"], page: {index: 0, size: 5}) {
        hits { id name entity description }
      }
    }
    """
    return run_query(gql, {"q": term})


# ---------------------------------------------------------------------------
# Unified interface
# ---------------------------------------------------------------------------

def query(entity: str) -> dict:
    """Query Open Targets with a single entity string.

    Auto-detects type by prefix:
      ENSG...   -> target lookup
      CHEMBL... -> drug lookup
      otherwise -> free-text search
    Returns a compact dict with entity, type, and data.
    """
    etype = _detect_type(entity)
    if etype == "target":
        raw = get_target_info(entity)
        t = raw.get("data", {}).get("target")
        if not t:
            return {"entity": entity, "type": "target", "found": False}
        return {
            "entity": entity, "type": "target", "found": True,
            "symbol": t["approvedSymbol"],
            "name": t["approvedName"],
            "biotype": t["biotype"],
            "top_diseases": [
                {"disease": r["disease"]["name"], "score": round(r["score"], 4)}
                for r in t.get("associatedDiseases", {}).get("rows", [])
            ],
        }
    elif etype == "drug":
        raw = get_drug_info(entity)
        d = raw.get("data", {}).get("drug")
        if not d:
            return {"entity": entity, "type": "drug", "found": False}
        return {
            "entity": entity, "type": "drug", "found": True,
            "name": d["name"],
            "drug_type": d["drugType"],
            "max_phase": d["maximumClinicalTrialPhase"],
            "indications": [
                {"disease": r["disease"]["name"], "phase": r["maxPhaseForIndication"]}
                for r in d.get("indications", {}).get("rows", [])[:5]
            ],
        }
    else:
        raw = search_entities(entity)
        hits = raw.get("data", {}).get("search", {}).get("hits", [])
        return {
            "entity": entity, "type": "search", "found": len(hits) > 0,
            "hits": [
                {"id": h["id"], "name": h["name"], "entity_type": h["entity"],
                 "description": h.get("description", "")}
                for h in hits
            ],
        }


def query_batch(entities: list[str]) -> list[dict]:
    """Query Open Targets for a list of entities. Returns list of result dicts."""
    return [query(e) for e in entities]


def summarize(result: dict) -> str:
    """Return a compact one-line summary string for a query result."""
    if not result.get("found"):
        return f"[{result['type']}] {result['entity']}: not found"
    if result["type"] == "target":
        diseases = ", ".join(
            f"{d['disease']}({d['score']})" for d in result["top_diseases"][:3]
        )
        return (f"[target] {result['symbol']} ({result['name']}, {result['biotype']}) "
                f"| diseases: {diseases}")
    if result["type"] == "drug":
        indications = ", ".join(
            f"{i['disease']}(ph{i['phase']})" for i in result["indications"][:3]
        )
        return (f"[drug] {result['name']} ({result['drug_type']}, "
                f"max_phase={result['max_phase']}) | indications: {indications}")
    # search
    hits = "; ".join(f"{h['id']}={h['name']}({h['entity_type']})" for h in result["hits"][:5])
    return f"[search] '{result['entity']}': {hits}"


# ---------------------------------------------------------------------------
# Usage examples
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # --- Single entity queries ---
    for entity_id in ["ENSG00000146648", "CHEMBL941", "BRCA1"]:
        res = query(entity_id)
        print(summarize(res))

    # --- Batch query ---
    print("\n--- Batch ---")
    batch = query_batch(["ENSG00000141510", "CHEMBL25", "CHEMBL941", "TP53"])
    for r in batch:
        print(summarize(r))

    # --- Raw JSON output ---
    print("\n--- JSON (single) ---")
    print(json.dumps(query("CHEMBL941"), indent=2))