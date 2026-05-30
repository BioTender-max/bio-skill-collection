"""
MecDDI - Mechanism-Based Drug-Drug Interaction Query Tool
Category: Drug-centric | Type: DB | Subcategory: Drug-Drug Interaction (DDI)
Source: https://mecddi.idrblab.net/download

Queries 7 mechanism-category TSV files:
  Affected Gastrointestinal Absorption, Affected Cellular Transport,
  Affected Organization Distribution, Affected Intra/Extra-Hepatic Metabolism,
  Affected Excretion Pathways, Pharmacodynamic Additive Effects,
  Pharmacodynamic Antagonistic Effects

Columns: A_Drug_ID, A_Drug_Name, B_Drug_ID, B_Drug_Name, Mechanism_Category
"""

import os
import csv
import json
from pathlib import Path
from typing import List, Dict, Optional, Union

DATA_DIR = str(
    Path(__file__).resolve().parents[3] / "resources_metadata" / "ddi" / "MecDDI"
)


def load_mecddi(data_dir: str = DATA_DIR) -> List[Dict]:
    """Load all TSV files under data_dir into a single list of dicts."""
    records = []
    for fname in sorted(os.listdir(data_dir)):
        if not fname.endswith((".tsv", ".txt", ".csv")):
            continue
        fpath = os.path.join(data_dir, fname)
        with open(fpath, newline="", encoding="utf-8", errors="replace") as f:
            # auto-detect delimiter
            sample = f.read(2048)
            f.seek(0)
            dialect = csv.Sniffer().sniff(sample, delimiters="\t,")
            reader = csv.DictReader(f, delimiter=dialect.delimiter)
            for row in reader:
                records.append(dict(row))
    return records


def search(records: List[Dict], entity: str) -> List[Dict]:
    """Search by drug ID or drug name (case-insensitive substring).

    Auto-detects input type:
      - Starts with 'D' + digits → match on A_Drug_ID or B_Drug_ID (exact)
      - Otherwise → substring match on A_Drug_Name or B_Drug_Name
    """
    entity_u = entity.strip().upper()
    hits = []
    is_id = entity_u.startswith("D") and entity_u[1:].isdigit()
    for r in records:
        if is_id:
            if r.get("A_Drug_ID", "").upper() == entity_u or r.get("B_Drug_ID", "").upper() == entity_u:
                hits.append(r)
        else:
            if (entity_u in r.get("A_Drug_Name", "").upper()
                    or entity_u in r.get("B_Drug_Name", "").upper()):
                hits.append(r)
    return hits


def search_batch(records: List[Dict], entities: List[str]) -> Dict[str, List[Dict]]:
    """Search multiple entities, return {entity: [hits]}."""
    return {e: search(records, e) for e in entities}


def summarize(hits: List[Dict], entity: str) -> str:
    """Return a concise text summary for LLM consumption."""
    if not hits:
        return f"No DDI records found for '{entity}'."
    lines = [f"MecDDI results for '{entity}': {len(hits)} interaction(s)"]
    seen = set()
    for r in hits:
        pair = (r.get("A_Drug_Name", ""), r.get("B_Drug_Name", ""))
        mech = r.get("Mechanism_Category", "")
        key = (*pair, mech)
        if key in seen:
            continue
        seen.add(key)
        lines.append(f"  {pair[0]} <-> {pair[1]}  [{mech}]")
    if len(seen) > 20:
        lines.append(f"  ... ({len(hits)} total, showing first unique pairs)")
    return "\n".join(lines)


def to_json(hits: List[Dict]) -> str:
    """Convert hits to JSON string."""
    return json.dumps(hits, ensure_ascii=False, indent=2)


# --------------- CLI / Usage Example ---------------
if __name__ == "__main__":
    print("Loading MecDDI data ...")
    data = load_mecddi()
    print(f"Loaded {len(data)} records from {DATA_DIR}\n")

    # --- Example 1: single drug name query ---
    entity = "Atropine"
    hits = search(data, entity)
    print(summarize(hits, entity))
    print()

    # --- Example 2: single drug ID query ---
    entity = "D0123"
    hits = search(data, entity)
    print(summarize(hits, entity))
    print()

    # --- Example 3: batch query ---
    entities = ["Meclizine", "Isocarboxazid", "D0853"]
    results = search_batch(data, entities)
    for ent, h in results.items():
        print(summarize(h, ent))
        print()

    # --- Example 4: JSON output (first 2 hits) ---
    hits = search(data, "Phenelzine")
    print("JSON sample:")
    print(to_json(hits[:2]))
