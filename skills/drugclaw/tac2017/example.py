"""
TAC 2017 ADR - Adverse Drug Reaction Extraction from Drug Labels
Category: Drug-centric | Type: Dataset | Subcategory: Drug NLP/Text Mining
Link: https://bionlp.nlm.nih.gov/tac2017adversereactions/

Parses FDA drug labels annotated with adverse reactions (Mentions,
Relations, Reactions with MedDRA normalization) from TAC 2017 ADR XML.

Skill interface:
  search(entity)        -> list[dict]   (single query)
  search_batch(entities) -> dict[str, list[dict]]
  summarize(hits, entity) -> str
  to_json(hits)          -> list[dict]
"""

import os
import re
from pathlib import Path
import xml.etree.ElementTree as ET
from collections import defaultdict

# ---------------------------------------------------------------------------
# Data path  (gold_xml = test set with annotations, train_xml = training set)
# ---------------------------------------------------------------------------
DATA_DIR = str(
    Path(__file__).resolve().parents[3]
    / "resources_metadata"
    / "drug_nlp"
    / "TAC2017ADR"
)
_ANNOTATED_DIRS = ["gold_xml", "train_xml"]

# ---------------------------------------------------------------------------
# Cache: populated on first call to _ensure_loaded()
# ---------------------------------------------------------------------------
_cache = {
    "labels": {},          # drug_name_lower -> label dict
    "adr_index": {},       # adr_str_lower  -> set of drug names
    "meddra_pt_index": {}, # meddra_pt_lower -> set of drug names
    "meddra_id_index": {}, # meddra_pt_id (str) -> set of drug names
    "loaded": False,
}


# ── XML Parsing ──────────────────────────────────────────────────────────────

def _parse_label(xml_path: str) -> dict | None:
    """Parse a single TAC 2017 ADR XML file into a structured dict."""
    try:
        tree = ET.parse(xml_path)
    except ET.ParseError:
        return None
    root = tree.getroot()
    drug = root.attrib.get("drug", os.path.splitext(os.path.basename(xml_path))[0])

    # Sections
    sections = {}
    text_el = root.find("Text")
    if text_el is not None:
        for sec in text_el.findall("Section"):
            sid = sec.attrib.get("id", "")
            sections[sid] = {
                "id": sid,
                "name": sec.attrib.get("name", ""),
                "text": (sec.text or "").strip(),
            }

    # Mentions
    mentions = {}
    mentions_el = root.find("Mentions")
    if mentions_el is not None:
        for m in mentions_el.findall("Mention"):
            mid = m.attrib.get("id", "")
            mentions[mid] = {
                "id": mid,
                "section": m.attrib.get("section", ""),
                "type": m.attrib.get("type", ""),
                "start": int(m.attrib.get("start", "0").split(",")[0]),
                "len": int(m.attrib.get("len", "0").split(",")[0]),
                "str": m.attrib.get("str", ""),
            }

    # Relations
    relations = []
    relations_el = root.find("Relations")
    if relations_el is not None:
        for r in relations_el.findall("Relation"):
            relations.append({
                "id": r.attrib.get("id", ""),
                "type": r.attrib.get("type", ""),
                "arg1": r.attrib.get("arg1", ""),
                "arg2": r.attrib.get("arg2", ""),
            })

    # Reactions (unique ADRs + MedDRA normalization)
    reactions = []
    reactions_el = root.find("Reactions")
    if reactions_el is not None:
        for rx in reactions_el.findall("Reaction"):
            norms = []
            for n in rx.findall("Normalization"):
                norms.append({
                    "meddra_pt": n.attrib.get("meddra_pt", ""),
                    "meddra_pt_id": n.attrib.get("meddra_pt_id", ""),
                    "meddra_llt": n.attrib.get("meddra_llt", ""),
                    "meddra_llt_id": n.attrib.get("meddra_llt_id", ""),
                    "flag": n.attrib.get("flag", ""),
                })
            reactions.append({
                "id": rx.attrib.get("id", ""),
                "str": rx.attrib.get("str", ""),
                "normalizations": norms,
            })

    # Derive positive ADRs (not negated, not hypothetical via DrugClass/Animal)
    negated_ids = set()
    hypo_by_animal_or_drugclass = set()
    for rel in relations:
        if rel["type"] == "Negated":
            negated_ids.add(rel["arg1"])
        elif rel["type"] == "Hypothetical":
            arg2_type = mentions.get(rel["arg2"], {}).get("type", "")
            if arg2_type in ("DrugClass", "Animal"):
                hypo_by_animal_or_drugclass.add(rel["arg1"])

    positive_adrs = set()
    for mid, m in mentions.items():
        if m["type"] == "AdverseReaction":
            if mid not in negated_ids and mid not in hypo_by_animal_or_drugclass:
                positive_adrs.add(m["str"].lower())

    return {
        "drug": drug,
        "sections": sections,
        "mentions": mentions,
        "relations": relations,
        "reactions": reactions,
        "positive_adrs": sorted(positive_adrs),
        "source_file": os.path.basename(xml_path),
    }


def _ensure_loaded():
    """Lazy-load and index all annotated XML files."""
    if _cache["loaded"]:
        return
    for subdir in _ANNOTATED_DIRS:
        dirpath = os.path.join(DATA_DIR, subdir)
        if not os.path.isdir(dirpath):
            continue
        for fname in sorted(os.listdir(dirpath)):
            if not fname.endswith(".xml"):
                continue
            label = _parse_label(os.path.join(dirpath, fname))
            if label is None:
                continue
            key = label["drug"].lower()
            _cache["labels"][key] = label

            # Index ADR strings
            for rx in label["reactions"]:
                adr_lower = rx["str"].lower()
                _cache["adr_index"].setdefault(adr_lower, set()).add(key)
                for n in rx["normalizations"]:
                    if n["meddra_pt"]:
                        pt_low = n["meddra_pt"].lower()
                        _cache["meddra_pt_index"].setdefault(pt_low, set()).add(key)
                    if n["meddra_pt_id"]:
                        _cache["meddra_id_index"].setdefault(n["meddra_pt_id"], set()).add(key)
                    if n["meddra_llt"]:
                        llt_low = n["meddra_llt"].lower()
                        _cache["meddra_pt_index"].setdefault(llt_low, set()).add(key)
                    if n["meddra_llt_id"]:
                        _cache["meddra_id_index"].setdefault(n["meddra_llt_id"], set()).add(key)

    _cache["loaded"] = True
    total = len(_cache["labels"])
    print(f"[TAC2017ADR] Loaded {total} annotated drug labels.")


# ── Entity-type detection ────────────────────────────────────────────────────

_RE_MEDDRA_ID = re.compile(r"^\d{8}$")   # 8-digit MedDRA code


def _detect_type(entity: str) -> str:
    """Return 'meddra_id', 'drug', 'adr', or 'text'."""
    e = entity.strip()
    if _RE_MEDDRA_ID.match(e):
        return "meddra_id"
    _ensure_loaded()
    if e.lower() in _cache["labels"]:
        return "drug"
    if e.lower() in _cache["adr_index"]:
        return "adr"
    return "text"


# ── Core search ──────────────────────────────────────────────────────────────

def search(entity: str) -> list[dict]:
    """
    Search TAC 2017 ADR by a single entity.

    Auto-detects type:
      - 8-digit number  → MedDRA ID lookup
      - Known drug name → return that drug's ADR profile
      - Known ADR string → return drugs with that ADR
      - Free text       → substring match on drug names, ADR strings, MedDRA PTs
    """
    _ensure_loaded()
    e = entity.strip()
    e_low = e.lower()
    etype = _detect_type(e)

    if etype == "drug":
        label = _cache["labels"][e_low]
        return [_label_to_hit(label)]

    if etype == "meddra_id":
        drugs = _cache["meddra_id_index"].get(e, set())
        return [_label_to_hit(_cache["labels"][d]) for d in sorted(drugs)]

    if etype == "adr":
        drugs = _cache["adr_index"].get(e_low, set())
        return [_label_to_hit(_cache["labels"][d], highlight_adr=e_low) for d in sorted(drugs)]

    # Free-text substring search across drug names, ADR strings, MedDRA PTs
    hits = []
    seen = set()
    # drug name substring
    for dname, label in _cache["labels"].items():
        if e_low in dname and dname not in seen:
            hits.append(_label_to_hit(label))
            seen.add(dname)
    # ADR string substring
    for adr_str, drug_set in _cache["adr_index"].items():
        if e_low in adr_str:
            for d in sorted(drug_set):
                if d not in seen:
                    hits.append(_label_to_hit(_cache["labels"][d], highlight_adr=adr_str))
                    seen.add(d)
    # MedDRA PT/LLT name substring
    for pt_name, drug_set in _cache["meddra_pt_index"].items():
        if e_low in pt_name:
            for d in sorted(drug_set):
                if d not in seen:
                    hits.append(_label_to_hit(_cache["labels"][d]))
                    seen.add(d)
    return hits


def search_batch(entities: list[str]) -> dict[str, list[dict]]:
    """Search multiple entities, return {entity: [hits]}."""
    return {e: search(e) for e in entities}


# ── Output helpers ───────────────────────────────────────────────────────────

def _label_to_hit(label: dict, highlight_adr: str = "") -> dict:
    """Convert a parsed label to a compact hit dict for output."""
    reactions_out = []
    for rx in label["reactions"]:
        entry = {"adr": rx["str"]}
        for n in rx["normalizations"]:
            if n["meddra_pt"]:
                entry["meddra_pt"] = n["meddra_pt"]
                entry["meddra_pt_id"] = n["meddra_pt_id"]
            if n["meddra_llt"]:
                entry["meddra_llt"] = n["meddra_llt"]
                entry["meddra_llt_id"] = n["meddra_llt_id"]
            if n["flag"]:
                entry["flag"] = n["flag"]
        if highlight_adr and rx["str"].lower() == highlight_adr:
            entry["matched"] = True
        reactions_out.append(entry)

    mention_types = defaultdict(int)
    for m in label["mentions"].values():
        mention_types[m["type"]] += 1

    return {
        "drug": label["drug"],
        "source_file": label["source_file"],
        "sections": [s["name"] for s in label["sections"].values()],
        "mention_counts": dict(mention_types),
        "num_reactions": len(label["reactions"]),
        "positive_adrs": label["positive_adrs"],
        "reactions": reactions_out,
    }


def summarize(hits: list[dict], entity: str) -> str:
    """Return a compact text summary for LLM consumption."""
    if not hits:
        return f"No results for '{entity}' in TAC 2017 ADR."
    lines = [f"=== TAC 2017 ADR results for '{entity}' ({len(hits)} label(s)) ==="]
    for h in hits:
        lines.append(f"\nDrug: {h['drug']}  (file: {h['source_file']})")
        lines.append(f"  Sections: {', '.join(h['sections'])}")
        lines.append(f"  Mentions: {h['mention_counts']}")
        lines.append(f"  Positive ADRs ({len(h['positive_adrs'])}): "
                      + ", ".join(h["positive_adrs"][:15])
                      + ("..." if len(h["positive_adrs"]) > 15 else ""))
        lines.append(f"  Reactions with MedDRA ({h['num_reactions']}):")
        for rx in h["reactions"][:10]:
            pt = rx.get("meddra_pt", "N/A")
            pt_id = rx.get("meddra_pt_id", "")
            flag = f" [{rx['flag']}]" if rx.get("flag") else ""
            mark = " *" if rx.get("matched") else ""
            lines.append(f"    - {rx['adr']} → {pt} ({pt_id}){flag}{mark}")
        if h["num_reactions"] > 10:
            lines.append(f"    ... and {h['num_reactions'] - 10} more")
    return "\n".join(lines)


def to_json(hits: list[dict]) -> list[dict]:
    """Return structured JSON-serializable output."""
    return hits


# ── Convenience: list all drugs / stats ──────────────────────────────────────

def list_drugs() -> list[str]:
    """Return sorted list of all drug names in the dataset."""
    _ensure_loaded()
    return sorted(_cache["labels"].keys())


def stats() -> dict:
    """Return dataset-level statistics."""
    _ensure_loaded()
    total_labels = len(_cache["labels"])
    total_reactions = sum(len(l["reactions"]) for l in _cache["labels"].values())
    unique_adrs = len(_cache["adr_index"])
    unique_pts = len(_cache["meddra_pt_index"])
    return {
        "num_labels": total_labels,
        "total_reactions": total_reactions,
        "unique_adr_strings": unique_adrs,
        "unique_meddra_terms": unique_pts,
    }


# ── Main: runnable examples ──────────────────────────────────────────────────

if __name__ == "__main__":
    # --- Dataset overview ---
    print(stats())
    print(f"First 10 drugs: {list_drugs()[:10]}\n")

    # --- Search by drug name ---
    hits = search("ACTEMRA")
    print(summarize(hits, "ACTEMRA"))

    # --- Search by ADR string ---
    hits = search("headache")
    print(summarize(hits, "headache"))

    # --- Search by MedDRA PT ID (8-digit) ---
    hits = search("10019211")  # Headache
    print(summarize(hits, "10019211"))

    # --- Batch search ---
    batch = search_batch(["ENBREL", "nausea", "10002198"])
    for ent, res in batch.items():
        print(summarize(res, ent))

    # --- JSON output ---
    hits = search("choline")
    import json
    print(json.dumps(to_json(hits), indent=2)[:800])
