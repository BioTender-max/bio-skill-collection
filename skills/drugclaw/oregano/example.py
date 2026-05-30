"""
OREGANO - Knowledge Graph for Computational Drug Repurposing
Category: Drug-centric | Type: Knowledge Graph | Subcategory: Drug Repurposing
Link: https://zenodo.org/records/10103842

Queries the OREGANO knowledge graph (88,937 nodes, 824,231 links,
11 node types, 19 relation types) covering compounds, targets, genes,
diseases, phenotypes, pathways, indications, side effects, activities,
and effects -- including natural compounds.

Loads TSV triplets + cross-reference metadata locally; supports search
by OREGANO ID, external ID (DrugBank, UMLS, UniProt, KEGG, MeSH, etc.),
or free-text entity name.
"""

import csv
import os
import re
from pathlib import Path
from collections import defaultdict

# ── paths ──────────────────────────────────────────────────────────────
DATA_DIR = str(
    Path(__file__).resolve().parents[3]
    / "resources_metadata"
    / "drug_repurposing"
    / "OREGANO"
)
TRIPLET_FILE = os.path.join(DATA_DIR, "OREGANO_V2.1.tsv")

META_FILES = {
    "compound":    os.path.join(DATA_DIR, "COMPOUND.tsv"),
    "target":      os.path.join(DATA_DIR, "TARGET.tsv"),
    "gene":        os.path.join(DATA_DIR, "GENES.tsv"),
    "disease":     os.path.join(DATA_DIR, "DISEASES.tsv"),
    "phenotype":   os.path.join(DATA_DIR, "PHENOTYPES.tsv"),
    "pathway":     os.path.join(DATA_DIR, "PATHWAYS.tsv"),
    "indication":  os.path.join(DATA_DIR, "INDICATION.tsv"),
    "side_effect": os.path.join(DATA_DIR, "SIDE_EFFECT.tsv"),
    "activity":    os.path.join(DATA_DIR, "ACTIVITY.tsv"),
    "effect":      os.path.join(DATA_DIR, "EFFECT.tsv"),
}

# ── lazy-loaded global cache ───────────────────────────────────────────
_cache = {}


def _load_triplets(path=TRIPLET_FILE):
    """Load OREGANO_V2.1.tsv → list of (subject, predicate, object).
    Also builds subject_index and object_index for fast lookup."""
    triplets = []
    subj_idx = defaultdict(list)
    obj_idx = defaultdict(list)
    with open(path, encoding="utf-8") as fh:
        reader = csv.reader(fh, delimiter="\t")
        header = next(reader, None)  # skip header if present
        # Check if first row looks like data (not a header)
        if header and not any(
            h.lower() in ("subject", "predicate", "object", "subjet")
            for h in header
        ):
            # first row is data, not a header
            if len(header) >= 3:
                t = (header[0].strip(), header[1].strip(), header[2].strip())
                triplets.append(t)
                subj_idx[t[0]].append(len(triplets) - 1)
                obj_idx[t[2]].append(len(triplets) - 1)
        for row in reader:
            if len(row) < 3:
                continue
            t = (row[0].strip(), row[1].strip(), row[2].strip())
            triplets.append(t)
            subj_idx[t[0]].append(len(triplets) - 1)
            obj_idx[t[2]].append(len(triplets) - 1)
    return triplets, subj_idx, obj_idx


def _load_meta(path):
    """Load a cross-reference TSV. Returns:
       - rows: list[dict]  (column→value per entity)
       - id_col: name of the first column (OREGANO ID)
       - xref_index: {external_id_lower: oregano_id}
       - name_index: {name_lower: oregano_id}
    """
    rows = []
    xref_index = {}   # external_id (lower) → oregano_id
    name_index = {}    # human-readable name (lower) → oregano_id
    id_col = None
    with open(path, encoding="utf-8") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        id_col = reader.fieldnames[0] if reader.fieldnames else None
        for row in reader:
            rows.append(row)
            oid = row.get(id_col, "").strip()
            if not oid:
                continue
            for col, val in row.items():
                if not val or not val.strip():
                    continue
                v = val.strip()
                if col == id_col:
                    continue
                # If column looks like a name column, add to name_index
                col_l = col.lower()
                if "name" in col_l or "label" in col_l:
                    name_index[v.lower()] = oid
                # All values go into xref_index
                xref_index[v.lower()] = oid
    return rows, id_col, xref_index, name_index


def _ensure_loaded():
    """Lazy-load all data on first call."""
    if _cache:
        return
    print("[OREGANO] Loading triplets …")
    triplets, subj_idx, obj_idx = _load_triplets()
    _cache["triplets"] = triplets
    _cache["subj_idx"] = subj_idx
    _cache["obj_idx"] = obj_idx

    # Collect all node IDs for quick membership test
    all_ids = set()
    for s, _, o in triplets:
        all_ids.add(s)
        all_ids.add(o)
    _cache["all_ids"] = all_ids

    # Load cross-reference metadata
    meta = {}
    xref_all = {}   # external_id (lower) → oregano_id
    name_all = {}   # name (lower) → oregano_id
    id_to_type = {} # oregano_id → entity_type
    id_to_row = {}  # oregano_id → metadata dict
    for etype, fpath in META_FILES.items():
        if not os.path.isfile(fpath):
            continue
        rows, id_col, xref_index, name_index = _load_meta(fpath)
        meta[etype] = {"rows": rows, "id_col": id_col}
        xref_all.update(xref_index)
        name_all.update(name_index)
        for row in rows:
            oid = row.get(id_col, "").strip()
            if oid:
                id_to_type[oid] = etype
                id_to_row[oid] = row
    _cache["meta"] = meta
    _cache["xref_all"] = xref_all
    _cache["name_all"] = name_all
    _cache["id_to_type"] = id_to_type
    _cache["id_to_row"] = id_to_row
    print(f"[OREGANO] Loaded {len(triplets)} triplets, "
          f"{len(all_ids)} unique nodes, "
          f"{len(id_to_type)} annotated entities.")


def _resolve_entity(query):
    """Resolve a user query to one or more OREGANO node IDs.
    Returns list of (oregano_id, match_method) tuples."""
    _ensure_loaded()
    q = query.strip()
    results = []

    # 1. Direct OREGANO ID match
    if q in _cache["all_ids"]:
        results.append((q, "oregano_id"))
        return results

    # 2. External ID exact match (case-insensitive)
    ql = q.lower()
    if ql in _cache["xref_all"]:
        results.append((_cache["xref_all"][ql], "xref_exact"))
        return results

    # 3. Name exact match (case-insensitive)
    if ql in _cache["name_all"]:
        results.append((_cache["name_all"][ql], "name_exact"))
        return results

    # 4. Substring search in names and xrefs (fallback)
    for name_lower, oid in _cache["name_all"].items():
        if ql in name_lower:
            results.append((oid, "name_substring"))
    if not results:
        for xid_lower, oid in _cache["xref_all"].items():
            if ql in xid_lower:
                results.append((oid, "xref_substring"))
    # Deduplicate
    seen = set()
    deduped = []
    for oid, method in results:
        if oid not in seen:
            seen.add(oid)
            deduped.append((oid, method))
    return deduped[:50]  # cap


def _get_triplets_for_id(oregano_id):
    """Return all triplets where oregano_id appears as subject or object."""
    _ensure_loaded()
    indices = set()
    indices.update(_cache["subj_idx"].get(oregano_id, []))
    indices.update(_cache["obj_idx"].get(oregano_id, []))
    return [_cache["triplets"][i] for i in sorted(indices)]


def _describe_id(oregano_id):
    """Return metadata dict for an OREGANO ID, or minimal stub."""
    _ensure_loaded()
    info = {"oregano_id": oregano_id}
    etype = _cache["id_to_type"].get(oregano_id)
    if etype:
        info["entity_type"] = etype
        row = _cache["id_to_row"].get(oregano_id, {})
        for k, v in row.items():
            if v and v.strip():
                info[k] = v.strip()
    return info


# ── public API ─────────────────────────────────────────────────────────

def search(query):
    """Search OREGANO by any entity string (OREGANO ID, external ID like
    DrugBank/UniProt/KEGG/MeSH/UMLS, or free-text name).

    Returns dict with keys:
      query, resolved_ids, metadata, triplets (as_subject, as_object).
    """
    _ensure_loaded()
    resolved = _resolve_entity(query)
    if not resolved:
        return {"query": query, "resolved_ids": [], "metadata": [],
                "triplets": {"as_subject": [], "as_object": []}}

    all_meta = []
    as_subject = []
    as_object = []
    for oid, method in resolved:
        all_meta.append(_describe_id(oid))
        for s, p, o in _get_triplets_for_id(oid):
            entry = {"subject": s, "predicate": p, "object": o}
            if s == oid:
                as_subject.append(entry)
            if o == oid:
                as_object.append(entry)
    return {
        "query": query,
        "resolved_ids": [{"oregano_id": oid, "match": m} for oid, m in resolved],
        "metadata": all_meta,
        "triplets": {"as_subject": as_subject, "as_object": as_object},
    }


def search_batch(queries):
    """Search multiple entities. Returns dict[query_str → search result]."""
    return {q: search(q) for q in queries}


def summarize(result):
    """Compact LLM-readable summary of a search result."""
    q = result["query"]
    ids = result["resolved_ids"]
    if not ids:
        return f"{q}: no matches in OREGANO."

    parts = [f"## {q}"]
    for meta in result["metadata"]:
        oid = meta.get("oregano_id", "?")
        etype = meta.get("entity_type", "unknown")
        extras = {k: v for k, v in meta.items()
                  if k not in ("oregano_id", "entity_type") and v}
        xrefs = ", ".join(f"{k}={v}" for k, v in list(extras.items())[:6])
        parts.append(f"  ID={oid} type={etype}" + (f" ({xrefs})" if xrefs else ""))

    subj = result["triplets"]["as_subject"]
    obj_ = result["triplets"]["as_object"]
    if subj:
        grouped = defaultdict(list)
        for t in subj:
            grouped[t["predicate"]].append(t["object"])
        for pred, objs in list(grouped.items())[:10]:
            shown = objs[:5]
            tail = f" (+{len(objs)-5})" if len(objs) > 5 else ""
            parts.append(f"  -[{pred}]-> {', '.join(shown)}{tail}")
    if obj_:
        grouped = defaultdict(list)
        for t in obj_:
            grouped[t["predicate"]].append(t["subject"])
        for pred, subjs in list(grouped.items())[:10]:
            shown = subjs[:5]
            tail = f" (+{len(subjs)-5})" if len(subjs) > 5 else ""
            parts.append(f"  <-[{pred}]- {', '.join(shown)}{tail}")
    return "\n".join(parts)


def to_json(result):
    """Return the full result dict (already JSON-serializable)."""
    return result


def get_stats():
    """Return graph-level statistics."""
    _ensure_loaded()
    triplets = _cache["triplets"]
    preds = defaultdict(int)
    for _, p, _ in triplets:
        preds[p] += 1
    etypes = defaultdict(int)
    for oid, et in _cache["id_to_type"].items():
        etypes[et] += 1
    return {
        "total_triplets": len(triplets),
        "unique_nodes": len(_cache["all_ids"]),
        "annotated_entities": len(_cache["id_to_type"]),
        "predicate_counts": dict(preds),
        "entity_type_counts": dict(etypes),
    }


# ── main ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # --- Single search: free-text drug name ---
    r = search("metformin")
    print(summarize(r))
    print()

    # --- Single search: DrugBank ID ---
    r = search("DB00331")
    print(summarize(r))
    print()

    # --- Batch search ---
    batch = search_batch(["aspirin", "metformin", "BRCA1"])
    for q, res in batch.items():
        print(summarize(res))
        print()

    # --- JSON output for pipeline ---
    r = search("ibuprofen")
    import json
    print(json.dumps(to_json(r), indent=2)[:800])
    print()

    # --- Graph stats ---
    stats = get_stats()
    print(f"Triplets: {stats['total_triplets']}, "
          f"Nodes: {stats['unique_nodes']}, "
          f"Annotated: {stats['annotated_entities']}")
    print("Predicates:", list(stats["predicate_counts"].keys())[:10])
    print("Entity types:", stats["entity_type_counts"])
