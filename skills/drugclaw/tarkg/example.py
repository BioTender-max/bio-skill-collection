"""
TarKG query example for canonical packaged resource output.

Default file: resources_metadata/dti/TarKG/tarkg.tsv
Columns: drug, target, relation, disease, pathway
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


DATA_PATH = str(
    Path(__file__).resolve().parents[3]
    / "resources_metadata"
    / "dti"
    / "TarKG"
    / "tarkg.tsv"
)


def load_tarkg(path: str = DATA_PATH) -> list[dict]:
    with open(path, newline="", encoding="utf-8", errors="ignore") as handle:
        return [dict(row) for row in csv.DictReader(handle, delimiter="\t")]


def query_entity(entity: str, rows: list[dict], limit: int = 50) -> dict:
    q = entity.strip().lower()
    if not q:
        return {"query": entity, "matched": False, "candidates": []}

    outgoing: list[dict] = []
    incoming: list[dict] = []
    candidates: list[str] = []

    for row in rows:
        drug = str(row.get("drug", "")).strip()
        target = str(row.get("target", "")).strip()
        relation = str(row.get("relation", "")).strip()
        disease = str(row.get("disease", "")).strip()
        pathway = str(row.get("pathway", "")).strip()

        drug_l = drug.lower()
        target_l = target.lower()
        disease_l = disease.lower()
        pathway_l = pathway.lower()

        if q in drug_l and len(outgoing) < limit:
            outgoing.append(
                {
                    "head_id": drug,
                    "relation": relation,
                    "tail_id": target,
                    "tail_name": target,
                    "disease": disease,
                    "pathway": pathway,
                }
            )
        if q in target_l and len(incoming) < limit:
            incoming.append(
                {
                    "head_id": drug,
                    "head_name": drug,
                    "relation": relation,
                    "tail_id": target,
                    "disease": disease,
                    "pathway": pathway,
                }
            )
        if q in disease_l or q in pathway_l:
            if drug and drug not in candidates:
                candidates.append(drug)
            if target and target not in candidates:
                candidates.append(target)

    matched = bool(outgoing or incoming or candidates)
    if not matched:
        return {"query": entity, "matched": False, "candidates": []}

    node_name = entity
    node_type = "entity"
    if outgoing:
        node_name = outgoing[0]["head_id"]
        node_type = "drug"
    elif incoming:
        node_name = incoming[0]["tail_id"]
        node_type = "target"

    return {
        "query": entity,
        "matched": True,
        "resolved_id": node_name,
        "node_info": {"node_id": node_name, "node_name": node_name, "node_type": node_type},
        "outgoing_edges": outgoing,
        "incoming_edges": incoming,
        "candidates": candidates[:20],
    }


def query_entities(entities: list[str], path: str = DATA_PATH, limit: int = 50) -> list[dict]:
    rows = load_tarkg(path)
    return [query_entity(entity, rows, limit=limit) for entity in entities]


if __name__ == "__main__":
    rows = load_tarkg()
    print(f"Loaded {len(rows)} TarKG triplets from {DATA_PATH}")
    demo = query_entities(["imatinib", "ABL1", "chronic myeloid leukemia"])
    print(json.dumps(demo, indent=2))
