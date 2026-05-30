"""
DrugMechDB Query Tool
Query drug mechanism-of-action paths by entity name, ID, or batch list.
Data source: https://github.com/SuLab/DrugMechDB (gh-pages branch, indication_paths.json)
"""

import json, re
from pathlib import Path
from collections import defaultdict

DATA_PATH = str(
    Path(__file__).resolve().parents[3]
    / "resources_metadata"
    / "drug_mechanism"
    / "DRUGMECHDB"
    / "indication_paths.json"
)

# ── ID prefix → entity type mapping ──────────────────────────────────────────
PREFIX_MAP = {
    "DB":       "Drug",        # DrugBank
    "MESH":     "Mixed",       # Drug / Disease / ChemicalSubstance
    "UniProt":  "Protein",
    "GO":       "BiologicalProcess/MolecularActivity/CellularComponent",
    "CHEBI":    "ChemicalSubstance",
    "HP":       "PhenotypicFeature",
    "UBERON":   "GrossAnatomicalStructure",
    "CL":       "Cell",
    "reactome": "Pathway",
    "InterPro": "GeneFamily",
    "PR":       "MacromolecularComplex",
    "taxonomy": "OrganismTaxon",
}

# ── Core data loader ─────────────────────────────────────────────────────────
def load(path=DATA_PATH):
    """Load DrugMechDB JSON. Returns list[dict], each dict is one mechanism path."""
    with open(path) as f:
        return json.load(f)

# ── Index builder (optional, speeds up repeated queries) ─────────────────────
def build_index(db):
    """
    Build lookup dicts for fast retrieval.
    Returns (by_id, by_name, by_drug, by_disease):
      - by_id[node_id] -> list of path indices
      - by_name[lowercase_name] -> list of path indices
      - by_drug[lowercase_drug] -> list of path indices
      - by_disease[lowercase_disease] -> list of path indices
    """
    by_id, by_name, by_drug, by_disease = (defaultdict(list) for _ in range(4))
    for i, rec in enumerate(db):
        g = rec["graph"]
        by_drug[g["drug"].lower()].append(i)
        by_disease[g["disease"].lower()].append(i)
        if g.get("drugbank"):
            by_id[g["drugbank"].upper()].append(i)
        if g.get("drug_mesh"):
            by_id[g["drug_mesh"].upper()].append(i)
        if g.get("disease_mesh"):
            by_id[g["disease_mesh"].upper()].append(i)
        for n in rec["nodes"]:
            by_id[n["id"].upper()].append(i)
            by_name[n["name"].lower()].append(i)
    return by_id, by_name, by_drug, by_disease

# ── Single entity search ─────────────────────────────────────────────────────
def search(db, entity, index=None):
    """
    Search paths matching an entity (name or ID).
    Auto-detects: if entity looks like an ID (contains ':' or starts with 'DB'),
    do exact ID match; otherwise do case-insensitive substring on names.

    Args:
        db: loaded database (list of path dicts)
        entity: query string, e.g. "imatinib", "UniProt:P00519", "DB00619", "MESH:D015464"
        index: optional pre-built index tuple from build_index()

    Returns:
        list of matching path dicts
    """
    q = entity.strip()
    is_id = bool(re.match(r"^(DB\d|MESH:|UniProt:|GO:|CHEBI:|HP:|UBERON:|CL:|reactome:|InterPro:|PR:|taxonomy:|Pfam:|TIGR:)", q, re.I))

    if index:
        by_id, by_name, by_drug, by_disease = index
        if is_id:
            idxs = by_id.get(q.upper(), [])
        else:
            ql = q.lower()
            # exact drug/disease name first, then substring on all node names
            idxs = by_drug.get(ql, []) + by_disease.get(ql, [])
            if not idxs:
                idxs = [i for name, indices in by_name.items() if ql in name for i in indices]
            idxs = sorted(set(idxs))
        return [db[i] for i in idxs]

    # No index: linear scan
    hits = []
    for rec in db:
        if is_id:
            match = (q.upper() == rec["graph"].get("drugbank", "").upper()
                     or q.upper() == rec["graph"].get("drug_mesh", "").upper()
                     or q.upper() == rec["graph"].get("disease_mesh", "").upper()
                     or any(q.upper() == n["id"].upper() for n in rec["nodes"]))
        else:
            ql = q.lower()
            match = (ql in rec["graph"]["drug"].lower()
                     or ql in rec["graph"]["disease"].lower()
                     or any(ql in n["name"].lower() for n in rec["nodes"]))
        if match:
            hits.append(rec)
    return hits

# ── Batch search ─────────────────────────────────────────────────────────────
def search_batch(db, entities, index=None):
    """
    Search multiple entities at once.
    Returns dict[entity_string -> list[path_dict]].
    """
    return {e: search(db, e, index) for e in entities}

# ── Compact summary formatter ────────────────────────────────────────────────
def summarize(paths, entity=""):
    """Return a concise text summary of search results."""
    if not paths:
        return f"No results for '{entity}'."
    lines = [f"=== {entity}: {len(paths)} path(s) ==="]
    for p in paths[:20]:  # cap display
        g = p["graph"]
        chain = " → ".join(f"{n['name']}[{n['label']}]" for n in p["nodes"])
        edges = " | ".join(l["key"] for l in p["links"])
        lines.append(f"  [{g['_id']}] {g['drug']} → {g['disease']}")
        lines.append(f"    path:  {chain}")
        lines.append(f"    edges: {edges}")
    if len(paths) > 20:
        lines.append(f"  ... and {len(paths)-20} more")
    return "\n".join(lines)

# ── JSON export helper ───────────────────────────────────────────────────────
def to_json(paths):
    """Convert path list to JSON-serializable list of dicts."""
    return [{"id": p["graph"]["_id"],
             "drug": p["graph"]["drug"],
             "disease": p["graph"]["disease"],
             "drugbank": p["graph"].get("drugbank"),
             "nodes": [{"id": n["id"], "label": n["label"], "name": n["name"]} for n in p["nodes"]],
             "links": [{"source": l["source"], "key": l["key"], "target": l["target"]} for l in p["links"]],
             } for p in paths]


if __name__ == "__main__":
    db = load()
    idx = build_index(db)
    print(f"Loaded {len(db)} paths\n")

    # --- Single entity queries ---
    # By drug name
    print(summarize(search(db, "imatinib", idx), "imatinib"))
    print()
    # By protein ID
    print(summarize(search(db, "UniProt:P00519", idx), "UniProt:P00519"))
    print()
    # By DrugBank ID
    print(summarize(search(db, "DB:DB00619", idx), "DB:DB00619"))
    print()
    # By disease name
    print(summarize(search(db, "asthma", idx), "asthma"))
    print()

    # --- Batch query ---
    results = search_batch(db, ["metformin", "MESH:D003920", "UniProt:P42336"], idx)
    for entity, paths in results.items():
        print(summarize(paths, entity))
        print()
