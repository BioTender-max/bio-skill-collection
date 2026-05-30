"""
07_DrugBank – Local DrugBank Query Skill
Category: Drug-centric | Type: DB | Subcategory: Drug Knowledgebase
Source : https://go.drugbank.com/releases/latest  (free account required)

Data location (fixed):
  XML : resources_metadata/drug_knowledgebase/DrugBank/full database.xml
  CSV : resources_metadata/drug_knowledgebase/DrugBank/drugbank vocabulary.csv

Supports two data formats (auto-selected, XML preferred):
  • Full XML  – rich fields (description, targets, interactions, categories …)
  • Vocabulary CSV – lightweight (DrugBank ID, name, CAS, synonyms …)
"""

import os, csv, json, re
from pathlib import Path
from typing import Union

# ── Config ──────────────────────────────────────────────────────────────
def _resolve_base_dir() -> Path:
    override = os.environ.get("DRUGBANK_DIR")
    if override:
        return Path(override)
    return (
        Path(__file__).resolve().parents[3]
        / "resources_metadata"
        / "drug_knowledgebase"
        / "DrugBank"
    )


_BASE = _resolve_base_dir()
VOCAB_PATH = str(_BASE / "drugbank vocabulary.csv")   # lightweight
XML_PATH   = str(_BASE / "full database.xml")         # rich fields
DATA_PATH  = XML_PATH if os.path.exists(XML_PATH) else VOCAB_PATH

# ── Loaders ─────────────────────────────────────────────────────────────

def load_vocab(path: str = DATA_PATH) -> list[dict]:
    """Load DrugBank vocabulary TSV/CSV into a list of dicts."""
    with open(path, newline="", encoding="utf-8") as f:
        sample = f.read(4096); f.seek(0)
        sep = "\t" if "\t" in sample else ","
        reader = csv.DictReader(f, delimiter=sep)
        return list(reader)


def _parse_drug_element(el, NS: str) -> dict:
    """Extract fields from a single <drug> element."""
    db_id = el.findtext(f"{NS}drugbank-id[@primary='true']") or ""
    name  = el.findtext(f"{NS}name") or ""
    desc  = (el.findtext(f"{NS}description") or "")[:300]
    cas   = el.findtext(f"{NS}cas-number") or ""
    dtype = el.get("type", "")
    groups = [g.text for g in el.findall(f"{NS}groups/{NS}group") if g.text]
    cats   = [c.findtext(f"{NS}category")
              for c in el.findall(f"{NS}categories/{NS}category")][:10]
    synonyms = [s.text for s in el.findall(
        f"{NS}synonyms/{NS}synonym") if s.text][:20]
    targets = []
    for t in el.findall(f"{NS}targets/{NS}target"):
        tid   = t.findtext(f"{NS}id") or ""
        tname = t.findtext(f"{NS}name") or ""
        actions = [a.text for a in t.findall(
            f"{NS}actions/{NS}action") if a.text]
        if tname:
            targets.append({"id": tid, "name": tname, "actions": actions})
    interactions = []
    for ix in el.findall(f"{NS}drug-interactions/{NS}drug-interaction"):
        ix_id   = ix.findtext(f"{NS}drugbank-id") or ""
        ix_name = ix.findtext(f"{NS}name") or ""
        ix_desc = (ix.findtext(f"{NS}description") or "")[:200]
        if ix_name:
            interactions.append({"drugbank_id": ix_id, "name": ix_name,
                                 "description": ix_desc})
    return {
        "drugbank_id": db_id, "name": name, "type": dtype,
        "cas_number": cas, "description": desc,
        "groups": groups, "categories": cats,
        "synonyms": synonyms,
        "targets": targets[:20],
        "interactions": interactions[:30],
    }


def load_xml(xml_path: str) -> list[dict]:
    """Stream-parse DrugBank full XML with iterparse (low memory).

    Uses iterparse + element.clear() so only one <drug> element is held
    in memory at a time.  Peak RSS ≈ 300-500 MB instead of 20+ GB.
    """
    import xml.etree.ElementTree as ET
    NS = "{http://www.drugbank.ca}"
    TAG = f"{NS}drug"
    drugs: list[dict] = []
    # depth tracking: only process top-level <drug>, skip nested <drug> in interactions
    depth = 0
    for event, el in ET.iterparse(xml_path, events=("start", "end")):
        if event == "start" and el.tag == TAG:
            depth += 1
        elif event == "end" and el.tag == TAG:
            depth -= 1
            if depth == 0:                       # top-level <drug> fully parsed
                drugs.append(_parse_drug_element(el, NS))
                el.clear()                       # free memory immediately
    print(f"  Parsed {len(drugs)} drugs from XML (iterparse, low-memory)")
    return drugs


def load(path: str = DATA_PATH) -> list[dict]:
    """Auto-detect format and load."""
    if path.endswith(".xml"):
        return load_xml(path)
    return load_vocab(path)

# ── Search ──────────────────────────────────────────────────────────────

_ID_RE = re.compile(r"^DB\d{5,}$", re.I)

def _match(record: dict, query: str) -> bool:
    q = query.strip().upper()
    # exact DrugBank ID
    if _ID_RE.match(q):
        rid = (record.get("drugbank_id") or record.get("DrugBank ID") or "").upper()
        return rid == q
    # substring on name / synonyms / CAS
    for key in ("name", "Name", "drug_name",
                "synonyms", "Synonyms",
                "cas_number", "CAS Number"):
        val = record.get(key)
        if val is None:
            continue
        if isinstance(val, list):
            val = " ".join(val)
        if q in val.upper():
            return True
    return False


def search(data: list[dict], entity: str) -> list[dict]:
    """Search records matching a single entity string."""
    return [r for r in data if _match(r, entity)]


def search_batch(data: list[dict],
                 entities: Union[str, list[str]]) -> dict[str, list[dict]]:
    """Search multiple entities. Accepts a list or comma-separated string."""
    if isinstance(entities, str):
        entities = [e.strip() for e in entities.split(",") if e.strip()]
    return {e: search(data, e) for e in entities}

# ── Output helpers ──────────────────────────────────────────────────────

def summarize(hits: list[dict], entity: str) -> str:
    if not hits:
        return f"[{entity}] No results."
    lines = [f"[{entity}] {len(hits)} hit(s):"]
    for h in hits[:10]:
        db_id = h.get("drugbank_id") or h.get("DrugBank ID", "")
        name  = h.get("name") or h.get("Name", "")
        parts = [db_id, name]
        if h.get("type"):
            parts.append(f"type={h['type']}")
        if h.get("groups"):
            parts.append(f"groups={','.join(h['groups'])}")
        if h.get("targets"):
            tnames = [t["name"] for t in h["targets"][:3]]
            parts.append(f"targets={';'.join(tnames)}")
        lines.append("  " + " | ".join(p for p in parts if p))
    return "\n".join(lines)


def to_json(hits: list[dict]) -> str:
    return json.dumps(hits, ensure_ascii=False, indent=2)

# ── CLI demo ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    data = load(DATA_PATH)
    print(f"Loaded {len(data)} records from {DATA_PATH}\n")

    # --- single query ---
    for q in ["DB00945", "aspirin"]:
        hits = search(data, q)
        print(summarize(hits, q), "\n")

    # --- batch query ---
    results = search_batch(data, ["metformin", "DB00316", "ibuprofen"])
    for entity, hits in results.items():
        print(summarize(hits, entity))
    print()

    # --- JSON output (first hit) ---
    sample = search(data, "aspirin")
    if sample:
        print("JSON sample (first hit):")
        print(to_json(sample[:1]))
