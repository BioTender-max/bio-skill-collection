"""
64_ChEBI.py – ChEBI (Chemical Entities of Biological Interest) query skill.

Category  : Drug-centric | Type: KG | Subcategory: Drug Ontology/Terminology
Link      : https://www.ebi.ac.uk/chebi/
Paper     : https://academic.oup.com/nar/article/54/D1/D1768/8349173
License   : CC BY 4.0

ChEBI is an open-access database and ontology of >195,000 molecular entities
(small chemical compounds) with names, structures, formulae, synonyms,
ontological roles, and cross-references to external databases.

Access method: ChEBI 2.0 REST API (JSON).  No API key required.
API docs  : https://www.ebi.ac.uk/chebi/backend/api/docs/
"""

import urllib.request
import urllib.parse
import json
import re
import time

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
CHEBI_BASE = "https://www.ebi.ac.uk/chebi/backend/api/public"
_HEADERS = {"Accept": "application/json", "User-Agent": "AgentLLM-ChEBI/1.0"}
_TIMEOUT = 20
MAX_RESULTS = 25  # cap per query to keep output LLM-readable


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------
def _get_json(url: str) -> dict:
    """GET *url*, return parsed JSON (or raise)."""
    req = urllib.request.Request(url, headers=_HEADERS)
    with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
        return json.loads(resp.read())


def _normalize_chebi_id(raw: str) -> str:
    """Accept '15422', 'CHEBI:15422', 'chebi:15422' -> 'CHEBI:15422'."""
    raw = raw.strip()
    m = re.match(r"(?i)chebi[:\s]*(\d+)", raw)
    if m:
        return f"CHEBI:{m.group(1)}"
    if raw.isdigit():
        return f"CHEBI:{raw}"
    return raw


def _is_chebi_id(q: str) -> bool:
    """Return True when *q* looks like a ChEBI numeric ID."""
    return bool(re.match(r"(?i)(chebi[:\s]*)?\d{1,7}$", q.strip()))


def _numeric_id(chebi_id: str) -> str:
    """'CHEBI:15422' -> '15422'."""
    return re.sub(r"\D", "", chebi_id)


# ---------------------------------------------------------------------------
# Core API wrappers  (verified against live ChEBI 2.0 REST, March 2026)
# ---------------------------------------------------------------------------
#
# Endpoint 1: GET .../public/es_search/?term=<query>&size=N&page=1
#   Response : {"results":[{"_id","_score","_source":{compound fields}},...],
#               "total": int, "number_pages": int}
#
# Endpoint 2: GET .../public/compound/CHEBI:<id>/
#   Response : full entity dict
#
# Endpoint 3: GET .../public/compounds/?chebi_ids=<id1>,<id2>,...
#   Response : {"<id1>":{"standardized_chebi_id","exists","data":{...}},...}
# ---------------------------------------------------------------------------

def search_chebi(query: str, max_results: int = MAX_RESULTS) -> list[dict]:
    """
    Search ChEBI via Elasticsearch full-text endpoint.

    Returns a flat list of compound dicts extracted from _source.
    """
    params = urllib.parse.urlencode({
        "term": query,
        "size": min(max_results, 200),
        "page": 1,
    })
    url = f"{CHEBI_BASE}/es_search/?{params}"
    data = _get_json(url)
    hits = data.get("results", [])
    out = []
    for h in hits[:max_results]:
        src = h.get("_source", h)
        src["_score"] = h.get("_score")
        out.append(src)
    return out


def get_entity(chebi_id: str) -> dict:
    """
    Retrieve the complete ChEBI entity by its ID.

    Accepts '15422', 'CHEBI:15422', or 'chebi:15422'.
    Returns full entity dict with name, definition, chemical_data,
    default_structure, names (synonyms), ontology_relations,
    database_accessions, roles_classification, etc.
    """
    cid = _normalize_chebi_id(chebi_id)
    url = f"{CHEBI_BASE}/compound/{urllib.parse.quote(cid, safe=':')}/"
    return _get_json(url)


def get_entities_batch(chebi_ids: list[str]) -> dict:
    """
    Retrieve multiple ChEBI entities in one call (up to ~50 IDs).

    Returns {numeric_id_str: entity_data_dict, ...}.
    """
    nums = [_numeric_id(_normalize_chebi_id(c)) for c in chebi_ids]
    params = urllib.parse.urlencode({"chebi_ids": ",".join(nums)})
    url = f"{CHEBI_BASE}/compounds/?{params}"
    raw = _get_json(url)
    out = {}
    for key, val in raw.items():
        if isinstance(val, dict) and val.get("exists"):
            out[key] = val.get("data", val)
        else:
            out[key] = val
    return out


# ---------------------------------------------------------------------------
# Public skill interface
# ---------------------------------------------------------------------------
def search(query: str, max_results: int = MAX_RESULTS) -> list[dict]:
    """
    Auto-detect input type and return results.

    * ChEBI ID  (e.g. 'CHEBI:15422', '27732')  -> full entity lookup.
    * Free text (e.g. 'aspirin', 'C9H8O4')     -> Elasticsearch search.
    """
    if _is_chebi_id(query):
        entity = get_entity(query)
        return [entity] if entity else []
    return search_chebi(query, max_results)


def search_batch(queries: list[str], max_results: int = MAX_RESULTS) -> dict:
    """
    Run queries for each item in *queries*.

    If ALL queries are ChEBI IDs, uses the efficient batch endpoint
    (/compounds/?chebi_ids=...).  Otherwise falls back to per-query
    search() with polite delay.

    Returns {query_string: [results, ...], ...}.
    """
    # Fast path: all IDs -> single batch call
    if all(_is_chebi_id(q) for q in queries):
        batch = get_entities_batch(queries)
        out = {}
        for q in queries:
            num = _numeric_id(_normalize_chebi_id(q))
            val = batch.get(num, {})
            out[q] = [val] if isinstance(val, dict) and val else []
        return out

    # Mixed: iterate
    out: dict[str, list[dict]] = {}
    for q in queries:
        try:
            out[q] = search(q, max_results)
        except Exception as exc:
            out[q] = [{"error": str(exc)}]
        time.sleep(0.3)
    return out


def summarize(results: list[dict], label: str = "") -> str:
    """
    One-line-per-hit compact text summary for LLM consumption.
    """
    if not results:
        return f"[ChEBI] No results{' for ' + label if label else ''}."
    lines = [f"[ChEBI] {len(results)} result(s){' for ' + repr(label) if label else ''}:"]
    for r in results[:MAX_RESULTS]:
        cid = r.get("chebi_accession") or r.get("id") or "?"
        name = r.get("ascii_name") or r.get("name") or ""
        # chemical_data may be nested dict or flat
        chem = r.get("chemical_data", {})
        if isinstance(chem, dict):
            formula = chem.get("formula", "") or r.get("formula", "")
            mass = chem.get("mass", "") or r.get("mass", "")
            charge = chem.get("charge") if chem.get("charge") else r.get("charge", "")
        else:
            formula = r.get("formula", "")
            mass = r.get("mass", "")
            charge = r.get("charge", "")
        # structure
        struct = r.get("default_structure", {})
        if isinstance(struct, dict):
            smiles = (struct.get("smiles") or r.get("smiles") or "")[:60]
        else:
            smiles = (r.get("smiles") or "")[:60]
        defn = (r.get("definition") or "")[:120]
        star = r.get("stars") or ""

        parts = [str(cid)]
        if name:
            parts.append(name)
        if formula:
            parts.append(f"formula={formula}")
        if mass:
            parts.append(f"mass={mass}")
        if charge not in ("", None, 0):
            parts.append(f"charge={charge}")
        if smiles:
            parts.append(f"SMILES={smiles}")
        if defn:
            parts.append(f"def={defn}")
        if star:
            parts.append(f"star={star}")
        lines.append("  " + " | ".join(parts))
    return "\n".join(lines)


def to_json(results: list[dict]) -> list[dict]:
    """Return results as a JSON-serialisable list (identity for API data)."""
    return results


# ---------------------------------------------------------------------------
# Runnable examples
# ---------------------------------------------------------------------------
if __name__ == "__main__":

    # --- 1. Single entity by ChEBI ID ---
    print("=== 1. Get entity by ChEBI ID (ATP, CHEBI:15422) ===")
    try:
        hits = search("CHEBI:15422")
        print(summarize(hits, "CHEBI:15422"))
    except Exception as e:
        print(f"  Error: {e}")

    # --- 2. Search by name ---
    print("\n=== 2. Search by name: 'aspirin' ===")
    try:
        hits = search("aspirin", max_results=5)
        print(summarize(hits, "aspirin"))
    except Exception as e:
        print(f"  Error: {e}")

    # --- 3. Search by formula ---
    print("\n=== 3. Search by formula: 'C9H8O4' ===")
    try:
        hits = search("C9H8O4", max_results=5)
        print(summarize(hits, "C9H8O4"))
    except Exception as e:
        print(f"  Error: {e}")

    # --- 4. Batch search (all IDs -> efficient single call) ---
    print("\n=== 4. Batch search (IDs) ===")
    try:
        batch = search_batch(["CHEBI:27732", "CHEBI:15422", "CHEBI:6809"])
        for q, res in batch.items():
            print(summarize(res, q))
    except Exception as e:
        print(f"  Error: {e}")

    # --- 5. Batch search (mixed IDs and names) ---
    print("\n=== 5. Batch search (mixed) ===")
    try:
        batch = search_batch(["CHEBI:27732", "metformin", "ibuprofen"],
                             max_results=3)
        for q, res in batch.items():
            print(summarize(res, q))
    except Exception as e:
        print(f"  Error: {e}")

    # --- 6. JSON output snippet ---
    print("\n=== 6. JSON output for caffeine (CHEBI:27732) ===")
    try:
        hits = search("27732")
        j = to_json(hits)
        if j:
            brief = {k: j[0][k] for k in
                     ("chebi_accession", "name", "definition",
                      "chemical_data", "stars") if k in j[0]}
            print(json.dumps(brief, indent=2)[:600])
    except Exception as e:
        print(f"  Error: {e}")