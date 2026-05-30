"""
45_STITCH — Search Tool for Interactions of Chemicals
Category: Drug-centric | Type: KG | Subcategory: Drug-Target Interaction (DTI)
Link: http://stitch.embl.de/
Paper: https://doi.org/10.1093/nar/gkv1277

STITCH integrates chemical-protein interaction data from experiments, databases,
and text mining, covering direct (binding) and indirect (functional) interactions.

API docs : http://stitch.embl.de/api/  (same schema as STRING API)
Base URLs: http://stitch.embl.de/api   (primary, includes chemical data)
           https://string-db.org/api   (fallback)
No API key required.
"""

import urllib.request
import urllib.parse
import json
import re
from typing import Union

# Primary: stitch.embl.de includes chemical–protein data.
# Fallback: string-db.org (STITCH data merged into STRING 12+).
API_BASES = [
    "http://stitch.embl.de/api",
    "https://string-db.org/api",
]
TIMEOUT = 20
DEFAULT_SPECIES = 9606          # Homo sapiens
DEFAULT_SCORE   = 400           # medium confidence
DEFAULT_LIMIT   = 10


# ── Low-level helpers ───────────────────────────────────────────────────

def _get_json(path: str, params: dict) -> list | dict:
    """Try each API base until one succeeds; return parsed JSON."""
    qs = urllib.parse.urlencode(params)
    last_err = None
    for base in API_BASES:
        url = f"{base}/json/{path}?{qs}"
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "STITCH-Skill/1.0",
                "Accept": "application/json",
            })
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return json.loads(resp.read())
        except Exception as e:
            last_err = e
            continue
    raise ConnectionError(f"All API bases failed for /{path}: {last_err}")


_CID_RE = re.compile(r"^CID[ms]\d+$", re.IGNORECASE)
_STRING_RE = re.compile(r"^\d+\.ENSP\d+$")


def _detect_type(entity: str) -> str:
    """
    Auto-detect entity type by pattern.
      CIDm00001983 / CIDs00001983 → 'stitch_id'
      9606.ENSP00000352121         → 'string_id'
      anything else                → 'name'
    """
    e = entity.strip()
    if _CID_RE.match(e):
        return "stitch_id"
    if _STRING_RE.match(e):
        return "string_id"
    return "name"


# ── Core API wrappers ──────────────────────────────────────────────────

def resolve(name: str, species: int = DEFAULT_SPECIES) -> list[dict]:
    """
    Resolve a chemical/protein name to STITCH identifiers.
    Returns list of dicts with keys: queryItem, queryIndex, preferredName,
    stringId, ncbiTaxonId, taxonName, annotation, etc.
    """
    return _get_json("resolve", {
        "identifier": name,
        "species": species,
    })


def resolve_batch(names: list[str],
                  species: int = DEFAULT_SPECIES) -> list[dict]:
    """Resolve multiple names in one call via /resolveList."""
    return _get_json("resolveList", {
        "identifiers": "\r".join(names),
        "species": species,
    })


def get_interactors(identifier: str, species: int = DEFAULT_SPECIES,
                    limit: int = DEFAULT_LIMIT,
                    required_score: int = DEFAULT_SCORE) -> list[dict]:
    """
    Get interaction partners for a chemical or protein.
    Returns list of dicts with keys: stringId_A, stringId_B, preferredName_A,
    preferredName_B, ncbiTaxonId, score, nscore, fscore, pscore, ascore,
    escore, dscore, tscore.
    """
    return _get_json("interactors", {
        "identifier": identifier,
        "species": species,
        "limit": limit,
        "required_score": required_score,
    })


def get_actions(identifier: str, species: int = DEFAULT_SPECIES,
                limit: int = DEFAULT_LIMIT,
                required_score: int = DEFAULT_SCORE) -> list[dict]:
    """
    Get action partners (activation, inhibition, binding, etc.).
    Returns list of dicts with keys: stringId_A, stringId_B, preferredName_A,
    preferredName_B, mode, action, is_directional, a_is_acting, score.
    """
    return _get_json("actions", {
        "identifier": identifier,
        "species": species,
        "limit": limit,
        "required_score": required_score,
    })


def get_interactions(identifiers: list[str],
                     species: int = DEFAULT_SPECIES,
                     required_score: int = DEFAULT_SCORE) -> list[dict]:
    """
    Get pairwise interactions among a set of chemicals / proteins.
    Uses /interactionsList endpoint.
    """
    return _get_json("interactionsList", {
        "identifiers": "\r".join(identifiers),
        "species": species,
        "required_score": required_score,
    })


# ── Unified query interface ────────────────────────────────────────────

def search(entity: str, species: int = DEFAULT_SPECIES,
           limit: int = DEFAULT_LIMIT,
           required_score: int = DEFAULT_SCORE) -> dict:
    """
    Unified entry point.  Auto-detects entity type and returns:
      {
        "query": <original query>,
        "resolved_id": <STITCH / STRING ID used>,
        "resolved_name": <preferred name>,
        "interactors": [...],
        "actions": [...]
      }
    """
    etype = _detect_type(entity)
    resolved_id = entity.strip()
    resolved_name = entity.strip()

    # resolve free-text names first
    if etype == "name":
        hits = resolve(entity, species)
        if not hits:
            return {"query": entity, "resolved_id": None,
                    "resolved_name": None, "interactors": [], "actions": []}
        best = hits[0]
        resolved_id = best.get("stringId") or best.get("id", entity)
        resolved_name = best.get("preferredName", entity)

    # fetch interactors + actions
    interactors = []
    actions = []
    try:
        interactors = get_interactors(resolved_id, species, limit, required_score)
    except Exception:
        pass
    try:
        actions = get_actions(resolved_id, species, limit, required_score)
    except Exception:
        pass

    return {
        "query": entity,
        "resolved_id": resolved_id,
        "resolved_name": resolved_name,
        "interactors": interactors,
        "actions": actions,
    }


def search_batch(entities: Union[str, list[str]],
                 species: int = DEFAULT_SPECIES,
                 limit: int = DEFAULT_LIMIT,
                 required_score: int = DEFAULT_SCORE) -> dict[str, dict]:
    """Search multiple entities. Accepts a list or comma-separated string."""
    if isinstance(entities, str):
        entities = [e.strip() for e in entities.split(",") if e.strip()]
    return {e: search(e, species, limit, required_score) for e in entities}


# ── Output helpers ─────────────────────────────────────────────────────

def summarize(result: dict, entity: str | None = None) -> str:
    """Compact, LLM-readable text summary of a search() result."""
    q = entity or result.get("query", "?")
    rid = result.get("resolved_id")
    rname = result.get("resolved_name")
    if not rid:
        return f"[{q}] No match in STITCH."

    lines = [f"[{q}] → {rname} ({rid})"]

    intrs = result.get("interactors", [])
    if intrs:
        lines.append(f"  Interactors ({len(intrs)}):")
        for p in intrs[:15]:
            name_b = p.get("preferredName_B", p.get("stringId_B", "?"))
            score  = p.get("score", "?")
            lines.append(f"    {name_b}  score={score}")

    acts = result.get("actions", [])
    if acts:
        lines.append(f"  Actions ({len(acts)}):")
        for a in acts[:15]:
            name_b = a.get("preferredName_B", a.get("stringId_B", "?"))
            mode   = a.get("mode", "?")
            score  = a.get("score", "?")
            lines.append(f"    {name_b}  mode={mode}  score={score}")

    return "\n".join(lines)


def to_json(result: dict | list) -> str:
    """Return JSON string for pipeline consumption."""
    return json.dumps(result, ensure_ascii=False, indent=2)


# ── CLI demo ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    # --- single query: free-text name ---
    print("=== search('aspirin') ===")
    r = search("aspirin")
    print(summarize(r))
    print()

    # --- single query: STITCH CID ---
    print("=== search('CIDm00002244') ===")  # aspirin merged CID
    r2 = search("CIDm00002244")
    print(summarize(r2))
    print()

    # --- batch query ---
    print("=== search_batch ===")
    results = search_batch(["ibuprofen", "metformin", "CIDm00002244"])
    for ent, res in results.items():
        print(summarize(res, ent))
        print()

    # --- JSON output ---
    print("=== to_json (first result) ===")
    first = search("caffeine", limit=3)
    print(to_json(first))