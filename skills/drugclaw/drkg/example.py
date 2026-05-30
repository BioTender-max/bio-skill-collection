"""
DRKG – Drug Repurposing Knowledge Graph  query skill
Category: Drug-centric | Type: KG | Subcategory: Drug Repurposing
Link: https://github.com/gnn4dr/DRKG

DRKG is a comprehensive biomedical KG (97 238 entities, 5 874 261 triplets,
107 relation types) integrating DrugBank, Hetionet, GNBR, STRING, IntAct,
DGIdb and COVID-19 literature.

Access method: Local TSV files (drkg.tsv, relation_glossary.tsv, entity2src.tsv).
"""

import os
import re
import csv
from pathlib import Path
from collections import defaultdict

# ---------------------------------------------------------------------------
# Path configuration
# ---------------------------------------------------------------------------
DATA_DIR = str(
    Path(__file__).resolve().parents[3]
    / "resources_metadata"
    / "drug_repurposing"
    / "DRKG"
)
DRKG_TSV = os.path.join(DATA_DIR, "drkg.tsv")
GLOSSARY_TSV = os.path.join(DATA_DIR, "relation_glossary.tsv")
ENTITY2SRC_TSV = os.path.join(DATA_DIR, "entity2src.tsv")

# ---------------------------------------------------------------------------
# Module-level cache (lazy-loaded)
# ---------------------------------------------------------------------------
_cache = {}

# 13 canonical entity types in DRKG
ENTITY_TYPES = [
    "Anatomy", "Atc", "Biological Process", "Cellular Component",
    "Compound", "Disease", "Gene", "Molecular Function",
    "Pathway", "Pharmacologic Class", "Side Effect", "Symptom", "Tax",
]


# ===== loading helpers =====================================================

def _load_triplets(path: str = DRKG_TSV):
    """Load drkg.tsv and build head / tail indexes.

    Returns (head_idx, tail_idx) where each maps entity -> list of
    (head, relation, tail) tuples.
    """
    if "head_idx" in _cache:
        return _cache["head_idx"], _cache["tail_idx"]

    head_idx = defaultdict(list)
    tail_idx = defaultdict(list)
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) != 3:
                continue
            h, r, t = parts
            trip = (h, r, t)
            head_idx[h].append(trip)
            tail_idx[t].append(trip)
    _cache["head_idx"] = head_idx
    _cache["tail_idx"] = tail_idx
    return head_idx, tail_idx


def _load_glossary(path: str = GLOSSARY_TSV):
    """Load relation_glossary.tsv -> dict[relation_name, dict]."""
    if "glossary" in _cache:
        return _cache["glossary"]
    glossary = {}
    if not os.path.exists(path):
        _cache["glossary"] = glossary
        return glossary
    with open(path, encoding="utf-8") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        for row in reader:
            key = row.get("relation") or row.get("")
            if key:
                glossary[key.strip()] = {k.strip(): v.strip() for k, v in row.items() if v}
    _cache["glossary"] = glossary
    return glossary


def _load_entity2src(path: str = ENTITY2SRC_TSV):
    """Load entity2src.tsv -> dict[entity, source_string]."""
    if "entity2src" in _cache:
        return _cache["entity2src"]
    e2s = {}
    if not os.path.exists(path):
        _cache["entity2src"] = e2s
        return e2s
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2:
                e2s[parts[0].strip()] = parts[1].strip()
    _cache["entity2src"] = e2s
    return e2s


def _all_entities():
    """Return set of all entity strings that appear in the KG."""
    hi, ti = _load_triplets()
    if "all_ents" not in _cache:
        _cache["all_ents"] = set(hi.keys()) | set(ti.keys())
    return _cache["all_ents"]


# ===== entity resolution ===================================================

_PREFIX_MAP = {
    "DB":   "Compound",
    "DOID": "Disease",
    "MESH": "Disease",
    "GO":   None,          # could be BP / MF / CC – search all three
    "HP":   "Side Effect",
}


def _resolve_entity(query: str):
    """Resolve a user query to a list of matching DRKG entity strings.

    Resolution order:
      1. Exact match (entity string as-is in KG).
      2. Typed ID guess  – e.g. "DB00945" → "Compound::DB00945".
      3. Pure-digit guess – try "Gene::<digits>".
      4. Substring search – case-insensitive match across all entities.
    """
    all_ents = _all_entities()
    q = query.strip()

    # 1. exact
    if q in all_ents:
        return [q]

    # 2. prefix-based type guess
    for pfx, etype in _PREFIX_MAP.items():
        if q.upper().startswith(pfx):
            if etype:
                cand = f"{etype}::{q}"
                if cand in all_ents:
                    return [cand]
            else:
                # GO terms – try BP, MF, CC
                for et in ("Biological Process", "Molecular Function", "Cellular Component"):
                    cand = f"{et}::{q}"
                    if cand in all_ents:
                        return [cand]

    # 3. pure digit → Gene
    if re.fullmatch(r"\d+", q):
        cand = f"Gene::{q}"
        if cand in all_ents:
            return [cand]

    # 4. substring (case-insensitive)
    ql = q.lower()
    matches = [e for e in all_ents if ql in e.lower()]
    return sorted(matches)[:50]  # cap at 50


# ===== core API =============================================================

def search(query: str, *, limit: int = 200):
    """Search DRKG for a single entity.

    Returns dict with keys:
      entity   – resolved DRKG entity (or list if ambiguous)
      as_head  – triplets where entity is head  [(h, r, t), ...]
      as_tail  – triplets where entity is tail  [(h, r, t), ...]
    """
    hi, ti = _load_triplets()
    resolved = _resolve_entity(query)

    if not resolved:
        return {"entity": query, "resolved": [], "as_head": [], "as_tail": []}

    as_head, as_tail = [], []
    for ent in resolved:
        as_head.extend(hi.get(ent, []))
        as_tail.extend(ti.get(ent, []))

    return {
        "entity": query,
        "resolved": resolved,
        "as_head": as_head[:limit],
        "as_tail": as_tail[:limit],
    }


def search_batch(queries: list, *, limit: int = 200):
    """Search DRKG for a list of entities. Returns dict[query, result]."""
    return {q: search(q, limit=limit) for q in queries}


def get_sources(entity: str):
    """Return the data-source attribution for a resolved entity."""
    e2s = _load_entity2src()
    return e2s.get(entity, "unknown")


def get_relation_info(relation: str):
    """Return glossary info for a relation string."""
    gl = _load_glossary()
    return gl.get(relation, {})


def entity_types():
    """Return list of the 13 DRKG entity types."""
    return list(ENTITY_TYPES)


# ===== output helpers =======================================================

def _rel_short(r: str) -> str:
    """'DRUGBANK::target::Compound:Gene' → 'DRUGBANK::target'"""
    parts = r.split("::")
    return "::".join(parts[:2]) if len(parts) >= 2 else r


def summarize(result: dict, *, max_lines: int = 30) -> str:
    """Compact LLM-readable text summary of a search result."""
    lines = []
    ent = result["entity"]
    resolved = result.get("resolved", [])
    if not resolved:
        return f"No DRKG entities matched '{ent}'."

    lines.append(f"DRKG results for '{ent}' → resolved to {len(resolved)} entit(y|ies):")
    for re_ in resolved[:5]:
        src = get_sources(re_)
        lines.append(f"  {re_}  [source: {src}]")
    if len(resolved) > 5:
        lines.append(f"  ... and {len(resolved)-5} more")

    # group outgoing edges by relation
    out_rels = defaultdict(list)
    for h, r, t in result["as_head"]:
        out_rels[_rel_short(r)].append(t)
    in_rels = defaultdict(list)
    for h, r, t in result["as_tail"]:
        in_rels[_rel_short(r)].append(h)

    if out_rels:
        lines.append(f"Outgoing edges ({sum(len(v) for v in out_rels.values())}):")
        for rel, targets in sorted(out_rels.items(), key=lambda x: -len(x[1])):
            sample = ", ".join(targets[:3])
            extra = f" (+{len(targets)-3} more)" if len(targets) > 3 else ""
            lines.append(f"  --[{rel}]--> {sample}{extra}")
            if len(lines) >= max_lines:
                lines.append("  ... (truncated)")
                break

    if in_rels and len(lines) < max_lines:
        lines.append(f"Incoming edges ({sum(len(v) for v in in_rels.values())}):")
        for rel, sources in sorted(in_rels.items(), key=lambda x: -len(x[1])):
            sample = ", ".join(sources[:3])
            extra = f" (+{len(sources)-3} more)" if len(sources) > 3 else ""
            lines.append(f"  <--[{rel}]-- {sample}{extra}")
            if len(lines) >= max_lines:
                lines.append("  ... (truncated)")
                break

    return "\n".join(lines)


def to_json(result: dict) -> dict:
    """Structured JSON-friendly output."""
    return {
        "entity": result["entity"],
        "resolved": result.get("resolved", []),
        "as_head": [{"head": h, "relation": r, "tail": t} for h, r, t in result["as_head"]],
        "as_tail": [{"head": h, "relation": r, "tail": t} for h, r, t in result["as_tail"]],
    }


# ===== main demo ============================================================

if __name__ == "__main__":
    print("Loading DRKG triplets (this may take ~30 s on first run) ...")
    hi, ti = _load_triplets()
    print(f"  Loaded {sum(len(v) for v in hi.values()):,} triplets,  "
          f"{len(_all_entities()):,} unique entities\n")

    # --- single entity search ---
    for q in ["Compound::DB00945", "DB00945", "DOID:162", "1956", "aspirin"]:
        res = search(q)
        print(summarize(res))
        print()

    # --- batch search ---
    batch = search_batch(["DB00945", "Gene::1956", "DOID:162"])
    for q, res in batch.items():
        print(f"[batch] {q}: {len(res['as_head'])+len(res['as_tail'])} triplets")

    # --- relation glossary ---
    info = get_relation_info("DRUGBANK::target::Compound:Gene")
    print(f"\nRelation info: {info}")

    # --- JSON output ---
    import json
    res = search("Compound::DB00945", limit=5)
    print("\nJSON sample:")
    print(json.dumps(to_json(res), indent=2)[:600])
