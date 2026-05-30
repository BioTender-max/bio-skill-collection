"""
KEGG Drug - Approved Drugs and Their Molecular Mechanisms
Category: Drug-centric | Type: DB | Subcategory: Drug-Drug Interaction (DDI)
Link: https://www.genome.jp/kegg/
Paper: https://academic.oup.com/nar/article/38/suppl_1/D355/3112250
API docs: https://www.kegg.jp/kegg/docs/keggapi.html
No API key required (free for academic use).
"""

import urllib.request
import urllib.parse
import json
from typing import Union

KEGG_BASE = "https://rest.kegg.jp"


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def _get(url: str) -> str:
    with urllib.request.urlopen(url, timeout=20) as resp:
        return resp.read().decode("utf-8")


def _parse_section(entry_text: str, section: str) -> list[str]:
    """Extract a named section (e.g. TARGET, INTERACTION) from a KEGG flat-file entry."""
    lines, capture = [], False
    for line in entry_text.split("\n"):
        if line.startswith(section):
            capture = True
            rest = line[len(section):].strip()
            if rest:
                lines.append(rest)
        elif capture:
            if line.startswith(" "):
                lines.append(line.strip())
            else:
                capture = False
    return lines


def _parse_entry(entry_text: str) -> dict:
    """Parse a KEGG Drug flat-file entry into a structured dict."""
    info = {}
    for key in ("ENTRY", "NAME", "FORMULA", "EXACT_MASS", "MOL_WEIGHT",
                "EFFICACY", "COMMENT", "REMARK"):
        for line in entry_text.split("\n"):
            if line.startswith(key):
                info[key.lower()] = line[len(key):].strip()
                break
    info["targets"] = _parse_section(entry_text, "TARGET")
    info["interactions"] = _parse_section(entry_text, "INTERACTION")
    info["pathways"] = _parse_section(entry_text, "PATHWAY")
    info["classes"] = _parse_section(entry_text, "CLASS")
    return info


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def search(query: str, limit: int = 10) -> list[dict]:
    """Search KEGG Drug by name/keyword. Returns list of {id, name}."""
    url = f"{KEGG_BASE}/find/drug/{urllib.parse.quote(query)}"
    results = []
    for line in _get(url).strip().split("\n"):
        if "\t" in line:
            did, name = line.split("\t", 1)
            results.append({"id": did.strip(), "name": name.strip()})
    return results[:limit]


def get_entry(drug_id: str) -> dict:
    """Get parsed KEGG Drug entry for a single drug ID (e.g. 'dr:D00109' or 'D00109')."""
    url = f"{KEGG_BASE}/get/{drug_id}"
    raw = _get(url)
    info = _parse_entry(raw)
    info["drug_id"] = drug_id
    return info


def get_interactions(drug_id: str) -> list[str]:
    """Get drug-drug interaction lines for a single drug ID."""
    url = f"{KEGG_BASE}/get/{drug_id}"
    return _parse_section(_get(url), "INTERACTION")


def get_targets(drug_id: str) -> list[str]:
    """Get target genes/proteins for a single drug ID."""
    url = f"{KEGG_BASE}/get/{drug_id}"
    return _parse_section(_get(url), "TARGET")


def query(entities: Union[str, list[str]], fields: str = "all") -> list[dict]:
    """
    Unified query interface. Accepts one or more drug names/IDs.

    Parameters
    ----------
    entities : str or list[str]
        Drug name(s) to search, or KEGG Drug ID(s) (e.g. 'D00109').
    fields : str
        'all' (default) — return full parsed entry.
        'targets'       — return targets only.
        'interactions'  — return DDI only.

    Returns
    -------
    list[dict]  — one dict per entity with query results.
    """
    if isinstance(entities, str):
        entities = [entities]

    results = []
    for entity in entities:
        entity = entity.strip()
        if not entity:
            continue

        # Determine if entity is a KEGG Drug ID or a name to search
        is_id = entity.upper().startswith("D") and entity[1:].replace(":", "").isdigit()
        if entity.lower().startswith("dr:"):
            is_id = True

        if is_id:
            drug_ids = [entity]
        else:
            hits = search(entity, limit=1)
            if not hits:
                results.append({"query": entity, "error": "No match found"})
                continue
            drug_ids = [hits[0]["id"]]

        for did in drug_ids:
            try:
                if fields == "targets":
                    data = {"drug_id": did, "query": entity, "targets": get_targets(did)}
                elif fields == "interactions":
                    data = {"drug_id": did, "query": entity, "interactions": get_interactions(did)}
                else:
                    data = get_entry(did)
                    data["query"] = entity
                results.append(data)
            except Exception as e:
                results.append({"query": entity, "drug_id": did, "error": str(e)})

    return results


# ---------------------------------------------------------------------------
# Usage examples (LLM-friendly)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # --- Example 1: Query a single drug by name ---
    print("=== Single drug query: aspirin ===")
    out = query("aspirin")
    print(json.dumps(out, indent=2, ensure_ascii=False)[:600])

    # --- Example 2: Query multiple drugs at once ---
    print("\n=== Batch query: metformin, imatinib ===")
    out = query(["metformin", "imatinib"])
    for item in out:
        print(f"  {item.get('drug_id')}: {item.get('name', 'N/A')}")
        print(f"    targets: {item.get('targets', [])[:2]}")
        print(f"    interactions: {item.get('interactions', [])[:2]}")

    # --- Example 3: Query by KEGG Drug ID ---
    print("\n=== Query by ID: D00109 ===")
    out = query("D00109")
    print(json.dumps(out, indent=2, ensure_ascii=False)[:400])

    # --- Example 4: Only fetch targets ---
    print("\n=== Targets only: warfarin ===")
    out = query("warfarin", fields="targets")
    print(json.dumps(out, indent=2, ensure_ascii=False)[:400])

    # --- Example 5: Only fetch DDI ---
    print("\n=== Interactions only: warfarin ===")
    out = query("warfarin", fields="interactions")
    print(json.dumps(out, indent=2, ensure_ascii=False)[:400])