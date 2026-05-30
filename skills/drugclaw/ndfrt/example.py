"""
52 · NDF-RT — National Drug File Reference Terminology
Category: Drug-centric | Type: KG | Subcategory: Drug Ontology/Terminology
Link: https://evsexplore.semantics.cancer.gov/evsexplore/welcome?terminology=ndfrt
API:  https://api-evsrest.nci.nih.gov/api/v1  (no key required)

NDF-RT is an ontology maintained by the VA that encodes drug mechanisms of
action (MoA), physiological effects (PE), established pharmacologic classes
(EPC), chemical structures, and clinical indications (may_treat / may_prevent).

This module exposes search / search_batch / summarize / to_json following the
standard skill interface.  Input entity type is auto-detected.
"""

import re
import json
import urllib.request
import urllib.parse
from typing import Optional

EVS_BASE = "https://api-evsrest.nci.nih.gov/api/v1"
TERMINOLOGY = "ndfrt"
TIMEOUT = 15

# NDF-RT codes look like N0000000001 (N + 10 digits)
_RE_NDFRT_CODE = re.compile(r"^N\d{10}$", re.IGNORECASE)


# ── low-level helpers ────────────────────────────────────────────────

def _get_json(url: str) -> Optional[dict | list]:
    """GET *url* and return parsed JSON, or None on any HTTP error."""
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read())
    except Exception as exc:
        print(f"[NDF-RT] HTTP error for {url}: {exc}")
        return None


def _search_concepts(term: str, limit: int = 10) -> list[dict]:
    """Full-text concept search.  Returns list of concept dicts."""
    params = urllib.parse.urlencode({
        "terminology": TERMINOLOGY,
        "term": term,
        "pageSize": limit,
    })
    url = f"{EVS_BASE}/concept/search?{params}"
    data = _get_json(url)
    if data is None:
        return []
    return data.get("concepts", [])


def _get_concept(code: str, include: str = "full") -> Optional[dict]:
    """Retrieve a single concept by NDF-RT code with *include* detail level."""
    url = f"{EVS_BASE}/concept/{TERMINOLOGY}/{code}?include={include}"
    return _get_json(url)


def _get_children(code: str) -> list[dict]:
    """Return immediate child concepts of *code*."""
    data = _get_json(f"{EVS_BASE}/concept/{TERMINOLOGY}/{code}/children")
    if data is None:
        return []
    return data if isinstance(data, list) else data.get("concepts", [])


def _get_roots() -> list[dict]:
    """Return top-level root concepts in NDF-RT."""
    data = _get_json(f"{EVS_BASE}/concept/{TERMINOLOGY}/roots")
    if data is None:
        return []
    return data if isinstance(data, list) else data.get("concepts", [])


# ── entity detection ─────────────────────────────────────────────────

def _detect_type(entity: str) -> str:
    """Return 'code' if entity looks like an NDF-RT code, else 'text'."""
    if _RE_NDFRT_CODE.match(entity.strip()):
        return "code"
    return "text"


# ── extract helpers ──────────────────────────────────────────────────

def _extract_properties(concept: dict) -> dict[str, str]:
    """Flatten the properties list into {type: value}."""
    out: dict[str, str] = {}
    for p in concept.get("properties", []):
        key = p.get("type", "")
        val = p.get("value", "")
        if key and val:
            out[key] = val
    return out


def _extract_roles(concept: dict) -> list[dict]:
    """Extract role relationships (may_treat, has_MoA, etc.)."""
    roles: list[dict] = []
    for r in concept.get("roles", []):
        roles.append({
            "type": r.get("type", ""),
            "relatedCode": r.get("relatedCode", ""),
            "relatedName": r.get("relatedName", ""),
        })
    return roles


def _extract_parents(concept: dict) -> list[dict]:
    """Extract parent (ISA) relationships."""
    parents: list[dict] = []
    for p in concept.get("parents", []):
        parents.append({
            "code": p.get("code", ""),
            "name": p.get("name", ""),
        })
    return parents


def _extract_synonyms(concept: dict) -> list[str]:
    """Return a deduplicated list of synonym strings."""
    syns: set[str] = set()
    for s in concept.get("synonyms", []):
        name = s.get("name", "")
        if name:
            syns.add(name)
    return sorted(syns)


# ── public API ───────────────────────────────────────────────────────

def search(entity: str, limit: int = 5) -> Optional[dict]:
    """Query NDF-RT for a single entity (drug name or NDF-RT code).

    Returns a dict with keys:
        entity, type, results (list of concept summaries)
    or None when the API is unreachable.
    """
    entity = entity.strip()
    etype = _detect_type(entity)

    if etype == "code":
        concept = _get_concept(entity)
        if concept is None:
            return {"entity": entity, "type": "code", "results": []}
        results = [_build_result(concept)]
        return {"entity": entity, "type": "code", "results": results}

    # free-text search
    hits = _search_concepts(entity, limit=limit)
    results: list[dict] = []
    for h in hits:
        code = h.get("code", "")
        # fetch full detail for each hit
        detail = _get_concept(code) if code else None
        if detail:
            results.append(_build_result(detail))
        else:
            results.append({
                "code": code,
                "name": h.get("name", ""),
                "kind": "",
                "properties": {},
                "roles": [],
                "parents": [],
                "synonyms": [],
            })
    return {"entity": entity, "type": "text", "results": results}


def search_batch(entities: list[str], limit: int = 3) -> dict[str, dict]:
    """Run search() for each entity.  Returns {entity: search_result}."""
    return {e: search(e, limit=limit) for e in entities}


def summarize(result: dict, entity: str = "") -> str:
    """One-line-per-concept compact summary for LLM context windows.

    Format:
        CODE Name [Kind] | roles: type→target, ... | parents: P1, P2
    """
    if result is None:
        return f"{entity}: no results"
    lines: list[str] = []
    label = entity or result.get("entity", "?")
    for r in result.get("results", []):
        parts: list[str] = []
        parts.append(f"{r.get('code','')} {r.get('name','')}")
        kind = r.get("kind", "")
        if kind:
            parts[0] += f" [{kind}]"
        # roles
        roles = r.get("roles", [])
        if roles:
            role_strs = [f"{rl['type']}→{rl['relatedName']}" for rl in roles[:8]]
            if len(roles) > 8:
                role_strs.append(f"…+{len(roles)-8}")
            parts.append("roles: " + ", ".join(role_strs))
        # parents
        parents = r.get("parents", [])
        if parents:
            par_strs = [p["name"] for p in parents[:4]]
            parts.append("parents: " + ", ".join(par_strs))
        lines.append(" | ".join(parts))
    if not lines:
        return f"{label}: no results"
    header = f"{label} ({len(lines)} hit{'s' if len(lines)>1 else ''}):"
    return header + "\n  " + "\n  ".join(lines)


def to_json(result: dict) -> list[dict]:
    """Return the results list from a search() dict, ready for JSON serialisation."""
    if result is None:
        return []
    return result.get("results", [])


# ── internal ─────────────────────────────────────────────────────────

def _build_result(concept: dict) -> dict:
    """Normalise a full-detail concept dict into a flat result dict."""
    props = _extract_properties(concept)
    return {
        "code": concept.get("code", ""),
        "name": concept.get("name", ""),
        "kind": props.get("Kind", props.get("Semantic_Type", "")),
        "properties": props,
        "roles": _extract_roles(concept),
        "parents": _extract_parents(concept),
        "synonyms": _extract_synonyms(concept),
    }


# ── runnable examples ────────────────────────────────────────────────

if __name__ == "__main__":
    # --- single drug search ---
    print("=== search('aspirin') ===")
    res = search("aspirin", limit=3)
    print(summarize(res, "aspirin"))

    # --- code lookup ---
    print("\n=== search('N0000145918') — aspirin by code ===")
    res2 = search("N0000145918")
    print(summarize(res2))

    # --- batch search ---
    print("\n=== search_batch(['metformin', 'warfarin']) ===")
    batch = search_batch(["metformin", "warfarin"], limit=2)
    for ent, r in batch.items():
        print(summarize(r, ent))
        print()

    # --- JSON output ---
    print("=== to_json (first result for aspirin) ===")
    res3 = search("aspirin", limit=1)
    print(json.dumps(to_json(res3)[:1], indent=2)[:600])

    # --- root concepts ---
    print("\n=== NDF-RT root concepts ===")
    roots = _get_roots()
    for r in roots[:5]:
        print(f"  {r.get('code')} | {r.get('name')}")