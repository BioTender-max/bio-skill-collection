"""
34_CADEC.py – Query the CADEC (CSIRO Adverse Drug Event Corpus)
Category: Drug-centric | Type: Dataset | Subcategory: Drug NLP/Text Mining
Source : https://data.csiro.au/collection/csiro:10948

Provides search / search_batch / summarize / to_json over a pre-built
cadec_combined.json (produced by build_cadec_json.py from BRAT files).
"""

import json, os, re
from pathlib import Path

DATA_PATH = str(
    Path(__file__).resolve().parents[3]
    / "resources_metadata"
    / "drug_nlp"
    / "CADEC"
    / "data"
    / "cadec"
    / "cadec_combined.json"
)

# ── data loading ─────────────────────────────────────────────────────

_data = None

def load_cadec(path=DATA_PATH):
    """Load cadec_combined.json → list[dict].  Cached after first call."""
    global _data
    if _data is not None:
        return _data
    with open(path, encoding="utf-8") as f:
        _data = json.load(f)
    return _data

# ── entity type detection ────────────────────────────────────────────

_MEDDRA_RE  = re.compile(r"^\d{8}$")          # 8-digit MedDRA code
_SCT_RE     = re.compile(r"^\d{6,18}$")       # 6-18 digit SNOMED CT
_DOCID_RE   = re.compile(r"^[A-Z0-9_.]+$", re.I)  # e.g. LIPITOR.1

def _detect(entity):
    e = entity.strip()
    if _MEDDRA_RE.match(e):
        return "meddra_code"
    if _SCT_RE.match(e):
        return "sct_code"
    return "text"

# ── search ───────────────────────────────────────────────────────────

def search(entity, data=None):
    """Search CADEC for a single entity.

    Auto-detects input type:
      - 8-digit number  → MedDRA code lookup
      - 6-18 digit number → SNOMED CT code lookup
      - free text → substring match on entity text, type, or document text

    Returns list[dict] of matching annotation records.
    Each record: {doc_id, entity_id, type, text, start, end,
                  normalizations, doc_snippet}
    """
    if data is None:
        data = load_cadec()
    e = entity.strip()
    etype = _detect(e)
    hits = []

    for doc in data:
        doc_id = doc["doc_id"]
        full_text = doc["text"]
        for ent in doc["entities"]:
            matched = False
            if etype == "meddra_code":
                for n in ent.get("normalizations", []):
                    if n["code"] == e and n["resource"].upper().startswith("MEDDRA"):
                        matched = True; break
            elif etype == "sct_code":
                for n in ent.get("normalizations", []):
                    if n["code"] == e and n["resource"].upper().startswith("SCT"):
                        matched = True; break
            else:  # free text
                el = e.lower()
                if (el in ent.get("text", "").lower()
                    or el in ent.get("type", "").lower()):
                    matched = True
                # also match doc_id (e.g. "LIPITOR")
                if not matched and el in doc_id.lower():
                    matched = True

            if matched:
                snippet_start = max(0, ent["start"] - 40)
                snippet_end   = min(len(full_text), ent["end"] + 40)
                hits.append({
                    "doc_id":          doc_id,
                    "entity_id":       ent["id"],
                    "type":            ent["type"],
                    "text":            ent["text"],
                    "start":           ent["start"],
                    "end":             ent["end"],
                    "normalizations":  ent.get("normalizations", []),
                    "doc_snippet":     full_text[snippet_start:snippet_end].replace("\n", " ")
                })
    return hits


def search_batch(entities, data=None):
    """Search CADEC for a list of entities.
    Returns dict[str, list[dict]]."""
    if data is None:
        data = load_cadec()
    return {e: search(e, data) for e in entities}

# ── output helpers ───────────────────────────────────────────────────

def summarize(hits, entity=""):
    """Compact text summary for LLM consumption."""
    if not hits:
        return f"No CADEC results for '{entity}'."
    lines = [f"CADEC results for '{entity}': {len(hits)} hit(s)"]
    seen = set()
    for h in hits:
        key = (h["doc_id"], h["entity_id"])
        if key in seen:
            continue
        seen.add(key)
        norms = ", ".join(
            f"{n['resource']}:{n['code']}({n['preferred_term']})"
            for n in h["normalizations"]
        ) or "none"
        lines.append(
            f"  [{h['type']}] \"{h['text']}\" "
            f"(doc={h['doc_id']}, norm={norms}) "
            f"ctx=\"...{h['doc_snippet']}...\""
        )
        if len(seen) >= 20:
            lines.append(f"  ... and {len(hits)-20} more")
            break
    return "\n".join(lines)


def to_json(hits):
    """Return hits as a JSON-serialisable list[dict]."""
    return hits


# ── main demo ────────────────────────────────────────────────────────

if __name__ == "__main__":
    data = load_cadec()
    print(f"Loaded {len(data)} documents from CADEC\n")

    # --- single entity: drug name ---
    h = search("lipitor", data)
    print(summarize(h, "lipitor"))
    print()

    # --- single entity: ADR text ---
    h = search("headache", data)
    print(summarize(h, "headache"))
    print()

    # --- single entity: MedDRA code ---
    h = search("10019211", data)
    print(summarize(h, "10019211"))
    print()

    # --- batch search ---
    results = search_batch(["lipitor", "nausea", "diclofenac"], data)
    for ent, hits in results.items():
        print(f"{ent}: {len(hits)} hit(s)")
    print()

    # --- JSON output ---
    h = search("lipitor", data)
    print(f"to_json sample (first record): {json.dumps(to_json(h)[:1], indent=2)}")
