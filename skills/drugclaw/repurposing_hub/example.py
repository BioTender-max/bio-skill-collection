"""
Drug Repurposing Hub - Broad Institute Curated Drug Collection
Category: Drug-centric | Type: DB | Subcategory: Drug Repurposing
Link: https://repo-hub.broadinstitute.org/repurposing
Paper: https://www.nature.com/articles/nm.4306

The Drug Repurposing Hub is a curated and annotated collection of >6,000
FDA-approved drugs, clinical trial drugs, and pre-clinical tool compounds,
maintained by the Broad Institute.  Each compound is annotated with
mechanism of action (MOA), molecular targets, clinical phase, disease area,
and indication.

Access method: Local TSV files (tab-delimited, '!' comment lines).
"""

import csv
import os
import re
from pathlib import Path

# ---------- paths (edit for your environment) ----------------------------
DATA_DIR = str(
    Path(__file__).resolve().parents[3]
    / "resources_metadata"
    / "drug_repurposing"
    / "DrugRepurposingHub"
)
DRUG_FILE = os.path.join(DATA_DIR, "repo-drug-annotation-20200324.txt")
SAMPLE_FILE = os.path.join(DATA_DIR, "repo-sample-annotation-20240610.txt")

# ---------- loading helpers ----------------------------------------------

def _read_tsv(fpath):
    """Read a Broad-style TSV (skip lines starting with '!')."""
    with open(fpath, encoding="utf-8", errors="replace") as fh:
        lines = [ln for ln in fh if not ln.startswith("!")]
    return list(csv.DictReader(lines, delimiter="\t"))


_cache = {}  # key -> list[dict]


def load_drugs(path=DRUG_FILE):
    """Load drug annotation table.  Cached after first call."""
    if "drugs" not in _cache:
        _cache["drugs"] = _read_tsv(path)
    return _cache["drugs"]


def load_samples(path=SAMPLE_FILE):
    """Load sample annotation table.  Cached after first call."""
    if "samples" not in _cache:
        _cache["samples"] = _read_tsv(path)
    return _cache["samples"]


def load_merged():
    """Return drugs with sample-level chemical identifiers merged in.

    Merge key is ``pert_iname``.  One drug may have multiple samples
    (different Broad IDs / vendors); we keep the first sample with a
    non-empty ``InChIKey`` or ``pubchem_cid``.
    """
    if "merged" in _cache:
        return _cache["merged"]

    drugs = load_drugs()
    samples = load_samples()

    # build lookup: pert_iname -> best sample row
    sample_map = {}
    for s in samples:
        name = (s.get("pert_iname") or "").strip().lower()
        if not name:
            continue
        if name not in sample_map:
            sample_map[name] = s
        else:
            # prefer row with InChIKey filled
            if s.get("InChIKey") and not sample_map[name].get("InChIKey"):
                sample_map[name] = s

    merged = []
    for d in drugs:
        row = dict(d)
        key = (d.get("pert_iname") or "").strip().lower()
        samp = sample_map.get(key, {})
        for col in ("broad_id", "InChIKey", "pubchem_cid", "smiles",
                     "deprecated_broad_id", "vendor", "catalog_no",
                     "purity", "expected_mass"):
            if col in samp:
                row[col] = samp[col]
        merged.append(row)
    _cache["merged"] = merged
    return merged


# ---------- entity detection ---------------------------------------------

_BROAD_RE = re.compile(r"^BRD-[A-Z]\d{8}", re.I)
_INCHIKEY_RE = re.compile(r"^[A-Z]{14}-[A-Z]{10}-[A-Z]$")
_GENE_RE = re.compile(
    r"^[A-Z][A-Z0-9]{1,10}$"  # heuristic: 2-11 uppercase alphanum
)

def _detect(entity):
    """Return (field_hint, query_value)."""
    e = entity.strip()
    if _BROAD_RE.match(e):
        return "broad_id", e
    if _INCHIKEY_RE.match(e):
        return "InChIKey", e
    # all-caps short token -> likely gene/target (e.g. EGFR, BRAF)
    if _GENE_RE.match(e) and len(e) <= 10:
        return "target", e
    return "text", e.lower()


# ---------- search -------------------------------------------------------

def search(entity, use_samples=True):
    """Search the Drug Repurposing Hub for *entity*.

    Auto-detects entity type:
      - ``BRD-*``       → Broad compound ID (exact on broad_id)
      - InChIKey        → exact on InChIKey
      - GENE-like token → substring on ``target``
      - anything else   → substring on pert_iname, moa, indication, disease_area

    Returns a list of matching dict rows.
    """
    data = load_merged() if use_samples else load_drugs()
    kind, val = _detect(entity)

    hits = []
    if kind == "broad_id":
        for r in data:
            if (r.get("broad_id") or "").upper().startswith(val.upper()):
                hits.append(r)
    elif kind == "InChIKey":
        for r in data:
            if (r.get("InChIKey") or "") == val:
                hits.append(r)
    elif kind == "target":
        pattern = val.upper()
        for r in data:
            targets = (r.get("target") or "").upper()
            # target field uses ' | ' as separator
            tlist = [t.strip() for t in targets.split("|")]
            if pattern in tlist:
                hits.append(r)
    else:  # free text
        for r in data:
            searchable = "\t".join([
                (r.get("pert_iname") or ""),
                (r.get("moa") or ""),
                (r.get("indication") or ""),
                (r.get("disease_area") or ""),
            ]).lower()
            if val in searchable:
                hits.append(r)
    return hits


def search_batch(entities, use_samples=True):
    """Search multiple entities.  Returns dict[entity] -> list[dict]."""
    return {e: search(e, use_samples=use_samples) for e in entities}


# ---------- output helpers -----------------------------------------------

def summarize(hits, entity=""):
    """Return a compact, LLM-readable text summary."""
    if not hits:
        return f"No results for '{entity}'."
    lines = [f"Drug Repurposing Hub: {len(hits)} hit(s) for '{entity}'"]
    for h in hits[:20]:
        parts = [
            h.get("pert_iname", "?"),
            f"Phase={h.get('clinical_phase', '')}",
            f"MOA={h.get('moa', '')}",
            f"Target={h.get('target', '')}",
        ]
        area = h.get("disease_area", "")
        ind = h.get("indication", "")
        if area:
            parts.append(f"Area={area}")
        if ind:
            parts.append(f"Ind={ind}")
        brd = h.get("broad_id", "")
        if brd:
            parts.append(f"BRD={brd}")
        lines.append("  " + " | ".join(parts))
    if len(hits) > 20:
        lines.append(f"  ... and {len(hits) - 20} more")
    return "\n".join(lines)


def to_json(hits):
    """Return hits as a list of plain dicts (JSON-serialisable)."""
    return [dict(h) for h in hits]


# ---------- main demo ----------------------------------------------------

if __name__ == "__main__":
    # 1. Search by drug name
    hits = search("imatinib")
    print(summarize(hits, "imatinib"))
    print()

    # 2. Search by gene target
    hits = search("EGFR")
    print(summarize(hits, "EGFR"))
    print()

    # 3. Search by MOA keyword
    hits = search("HDAC inhibitor")
    print(summarize(hits, "HDAC inhibitor"))
    print()

    # 4. Search by disease area
    hits = search("oncology")
    print(f"'oncology' → {len(hits)} compounds")
    print()

    # 5. Batch search
    results = search_batch(["metformin", "aspirin", "BRAF"])
    for ent, rows in results.items():
        print(f"{ent}: {len(rows)} hit(s)")
    print()

    # 6. JSON output
    hits = search("sirolimus")
    import json
    print(json.dumps(to_json(hits)[:2], indent=2))
