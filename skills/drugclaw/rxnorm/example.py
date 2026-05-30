"""
RxNorm - Drug Naming Standardization and Normalization
Category: Drug-centric | Type: DB | Subcategory: Drug Ontology/Terminology
Link: https://www.nlm.nih.gov/research/umls/rxnorm/
Paper: https://academic.oup.com/jamia/article-abstract/18/4/441/734170

RxNorm provides normalized names for clinical drugs. Maintained by the U.S.
National Library of Medicine.

API docs: https://lhncbc.nlm.nih.gov/RxNav/APIs/RxNormAPIs.html
No API key required.
"""

import urllib.request
import urllib.parse
import urllib.error
import json
from typing import Union

BASE_URL = "https://rxnav.nlm.nih.gov/REST"


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def _get_json(url: str) -> dict | None:
    """Fetch a URL and return parsed JSON, or None on HTTP error."""
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError:
        return None


def find_rxcui(drug_name: str) -> str | None:
    """Return the RxCUI for a drug name, or None if not found."""
    params = urllib.parse.urlencode({"name": drug_name})
    data = _get_json(f"{BASE_URL}/rxcui.json?{params}")
    if data is None:
        return None
    ids = data.get("idGroup", {}).get("rxnormId", [])
    return ids[0] if ids else None


def get_drug_info(rxcui: str) -> dict:
    """Get detailed information for an RxCUI."""
    return _get_json(f"{BASE_URL}/rxcui/{rxcui}/allinfo.json") or {}


def get_drug_interactions(rxcui: str) -> list[dict]:
    """Return interaction descriptions for an RxCUI."""
    data = _get_json(
        f"{BASE_URL}/interaction/interaction.json?rxcui={rxcui}"
    )
    if data is None:
        return []
    results = []
    for group in data.get("interactionTypeGroup", []):
        for itype in group.get("interactionType", []):
            for pair in itype.get("interactionPair", []):
                results.append({
                    "description": pair.get("description", ""),
                    "severity": pair.get("severity", ""),
                    "drugs": [
                        c.get("minConceptItem", {}).get("name", "")
                        for c in pair.get("interactionConcept", [])
                    ],
                })
    return results


def get_related_drugs(rxcui: str, relation_type: str = "BN") -> list[dict]:
    """Get related drugs (e.g., brand names) for an RxCUI."""
    data = _get_json(
        f"{BASE_URL}/rxcui/{rxcui}/related.json?tty={relation_type}"
    )
    if data is None:
        return []
    items = []
    for group in data.get("relatedGroup", {}).get("conceptGroup", []):
        for prop in group.get("conceptProperties", []):
            items.append({
                "rxcui": prop.get("rxcui"),
                "name": prop.get("name"),
                "tty": prop.get("tty"),
            })
    return items


def normalize_drug_name(drug_name: str) -> str:
    """Return the normalized RxNorm name for an approximate drug string."""
    params = urllib.parse.urlencode({"name": drug_name, "search": 1})
    data = _get_json(f"{BASE_URL}/approximateTerm.json?{params}")
    if data is None:
        return drug_name
    candidates = data.get("approximateGroup", {}).get("candidate", [])
    return candidates[0].get("name", drug_name) if candidates else drug_name


def _get_rxcui_name(rxcui: str) -> str | None:
    """Return the canonical name for an RxCUI, or None."""
    data = _get_json(f"{BASE_URL}/rxcui/{rxcui}/properties.json")
    if data is None:
        return None
    return data.get("properties", {}).get("name")


# ---------------------------------------------------------------------------
# Unified query: single entity or batch
# ---------------------------------------------------------------------------

def query(entity: Union[str, list[str]]) -> dict:
    """
    Query RxNorm for one or more drug names.

    Parameters
    ----------
    entity : str or list[str]
        A single drug name or a list of drug names.

    Returns
    -------
    dict  –  {drug_name: {rxcui, normalized_name, interactions, related}} for
             each input. If RxCUI lookup fails the entry still appears with
             rxcui=None.
    """
    names = [entity] if isinstance(entity, str) else entity
    results = {}
    for name in names:
        rxcui = find_rxcui(name)
        if rxcui:
            # Exact match found – get canonical name from properties
            normalized = _get_rxcui_name(rxcui) or name
            entry = {
                "rxcui": rxcui,
                "normalized_name": normalized,
                "interactions": get_drug_interactions(rxcui),
                "related": get_related_drugs(rxcui),
            }
        else:
            # No exact match – try approximate normalization
            normalized = normalize_drug_name(name)
            entry = {
                "rxcui": None,
                "normalized_name": normalized,
                "interactions": [],
                "related": [],
            }
        results[name] = entry
    return results


def summarize(results: dict) -> str:
    """Return a compact text summary of query() output."""
    lines = []
    for name, info in results.items():
        rxcui = info["rxcui"] or "N/A"
        norm = info["normalized_name"]
        n_int = len(info["interactions"])
        n_rel = len(info["related"])
        lines.append(f"- {name}: RxCUI={rxcui}, normalized='{norm}', "
                      f"interactions={n_int}, related={n_rel}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Usage examples (LLM-readable)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # --- Single entity ---
    print("=== Single entity: aspirin ===")
    res = query("aspirin")
    print(summarize(res))
    # Show first 2 interactions
    for ix in res["aspirin"]["interactions"][:2]:
        print(f"  interaction: {ix['description'][:]}")

    # --- Batch entities ---
    print("\n=== Batch entities ===")
    res = query(["tylenol", "metformin", "ibuprofen"])
    print(summarize(res))