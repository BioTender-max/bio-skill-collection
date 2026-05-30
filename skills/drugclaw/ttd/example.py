"""
TTD - Therapeutic Target Database
Category: Drug-centric | Type: DB | Subcategory: Drug-Target Interaction (DTI)
Link: https://ttd.idrblab.cn/
Paper: https://academic.oup.com/nar/article/52/D1/D1465/7275004

TTD provides therapeutic protein/nucleic acid targets, targeted diseases,
pathway information, and drugs (approved/clinical/experimental).

Data directory (4 files required):
  P1-01-TTD_target_download.txt  — Target info (UniProt, gene, function, disease, pathway)
  P2-01-TTD_target_drug.txt      — Target ↔ Drug links (with clinical status)
  P1-06-Target_disease.txt       — Target ↔ Disease links
  P1-07-Drug_disease.txt         — Drug ↔ Disease links
"""

import os
import json
from pathlib import Path
from collections import defaultdict
from typing import Union

DATA_DIR = str(
    Path(__file__).resolve().parents[3] / "resources_metadata" / "dti" / "TTD"
)


# ── Parsers ──────────────────────────────────────────────────────────────────

def _parse_block_file(fpath: str) -> list[dict]:
    """
    Parse TTD block-format file (blank-line separated records).
    Line format: <ID>\t<KEY>\t<VALUE>
    Multi-value keys are collected into lists.
    """
    records, current = [], {}
    with open(fpath, encoding="utf-8", errors="replace") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                if current:
                    records.append(current)
                    current = {}
                continue
            parts = line.split("\t")
            if len(parts) < 3:
                continue
            key, val = parts[1].strip(), parts[2].strip()
            if key in current:
                if isinstance(current[key], list):
                    current[key].append(val)
                else:
                    current[key] = [current[key], val]
            else:
                current[key] = val
    if current:
        records.append(current)
    return records


def _parse_tsv_file(fpath: str) -> list[dict]:
    """
    Parse TTD simple TSV files (first non-comment line = header).
    """
    rows, headers = [], None
    with open(fpath, encoding="utf-8", errors="replace") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            cols = line.split("\t")
            if headers is None:
                headers = cols
                continue
            rows.append(dict(zip(headers, cols)))
    return rows


# ── Index builder ─────────────────────────────────────────────────────────────

def _build_indexes(data_dir: str) -> dict:
    """Load all 4 files and build lookup indexes. Called once per query."""

    targets = _parse_block_file(os.path.join(data_dir, "P1-01-TTD_target_download.txt"))
    td_records = _parse_block_file(os.path.join(data_dir, "P2-01-TTD_target_drug.txt"))
    target_disease_rows = _parse_tsv_file(os.path.join(data_dir, "P1-06-Target_disease.txt"))
    drug_disease_rows = _parse_tsv_file(os.path.join(data_dir, "P1-07-Drug_disease.txt"))

    # target_id → [{drug_id, drug_name, clinical_status}]
    tid_to_drugs = defaultdict(list)
    # drug_name_lower → [{ttd_target_id, target_name, clinical_status, drug_id}]
    drug_to_targets = defaultdict(list)
    # drug_name_lower → drug_id (first seen)
    drug_to_id = {}

    for rec in td_records:
        tid    = rec.get("TTDTARGET", "")
        did    = rec.get("DRUGID", "")
        dname  = rec.get("DRUGNAME", "")
        tname  = rec.get("TARGNAME", "")
        status = rec.get("DRUG_CLINSTATUS", "")
        if tid and dname:
            tid_to_drugs[tid].append({"drug_id": did, "drug_name": dname, "clinical_status": status})
        if dname:
            dl = dname.lower()
            drug_to_targets[dl].append({"ttd_target_id": tid, "target_name": tname,
                                        "clinical_status": status, "drug_id": did})
            drug_to_id.setdefault(dl, did)

    # disease_lower → [{ttd_target_id, target_name}]
    disease_to_targets = defaultdict(list)
    for row in target_disease_rows:
        dis   = (row.get("Disease Name") or row.get("DiseaseName") or "").strip()
        tid   = (row.get("TTD Target ID") or row.get("TTDTARGET") or "").strip()
        tname = (row.get("Target Name") or "").strip()
        if dis:
            disease_to_targets[dis.lower()].append({"ttd_target_id": tid, "target_name": tname})

    # disease_lower → [drug_name]
    disease_to_drugs = defaultdict(list)
    # drug_name_lower → [disease_name]
    drug_to_diseases = defaultdict(list)
    for row in drug_disease_rows:
        dis   = (row.get("Disease Name") or row.get("DiseaseName") or "").strip()
        dname = (row.get("Drug Name") or row.get("DrugName") or "").strip()
        if dis and dname:
            disease_to_drugs[dis.lower()].append(dname)
            drug_to_diseases[dname.lower()].append(dis)

    return {
        "targets": targets,
        "tid_to_drugs": tid_to_drugs,
        "drug_to_targets": drug_to_targets,
        "drug_to_id": drug_to_id,
        "drug_to_diseases": drug_to_diseases,
        "disease_to_targets": disease_to_targets,
        "disease_to_drugs": disease_to_drugs,
    }


# ── Query API ─────────────────────────────────────────────────────────────────

def query(
    entities: Union[str, list[str]],
    entity_type: str = "auto",
    data_dir: str = DATA_DIR,
) -> list[dict]:
    """
    Query TTD for one or more entities. Returns a list of result dicts.

    Parameters
    ----------
    entities : str | list[str]
        Entity name(s) or ID(s). Accepted:
          - Gene / protein name  e.g. "EGFR", "BCR-ABL"
          - Drug name            e.g. "Imatinib", "Gefitinib"
          - Disease name         e.g. "Lung cancer", "Diabetes mellitus"
          - TTD Target ID        e.g. "TTDTARGET00001"
          - TTD Drug ID          e.g. "D0Y4GH"
    entity_type : "auto" | "target" | "drug" | "disease"
        Restrict search type. "auto" tries target → drug → disease in order.
    data_dir : str
        Path to directory containing the 4 TTD flat files.

    Returns
    -------
    list[dict]  — one dict per queried entity (LLM-readable, JSON-safe).
    """
    if isinstance(entities, str):
        entities = [entities]

    idx = _build_indexes(data_dir)
    results = []
    matched = set()

    # ── Target search ─────────────────────────────────────────────────────
    if entity_type in ("target", "auto"):
        for rec in idx["targets"]:
            tid     = rec.get("TTDTARGET", "")
            tname   = rec.get("TARGNAME", "") or ""
            gene    = rec.get("GENENAME", "") or ""
            uniprot = rec.get("UNIPROID", "") or ""
            searchable = " ".join([tid, tname, gene, uniprot]).lower()

            for e in entities:
                if e in matched:
                    continue
                if e.lower() in searchable:
                    matched.add(e)
                    results.append({
                        "query": e,
                        "entity_type": "target",
                        "ttd_id": tid,
                        "name": tname,
                        "uniprot": uniprot,
                        "gene": gene,
                        "target_type": rec.get("TARGTYPE", ""),
                        "function": rec.get("FUNCTION", ""),
                        "disease": rec.get("INDICATI", "") or rec.get("DISEASE", ""),
                        "pathway": rec.get("BIOCLASS", "") or rec.get("PATHWAY", ""),
                        "drugs": idx["tid_to_drugs"].get(tid, []),
                    })

    # ── Drug search ───────────────────────────────────────────────────────
    if entity_type in ("drug", "auto"):
        for e in entities:
            if e in matched:
                continue
            el = e.lower()
            if el in idx["drug_to_targets"]:
                matched.add(e)
                results.append({
                    "query": e,
                    "entity_type": "drug",
                    "drug_id": idx["drug_to_id"].get(el, ""),
                    "drug_name": e,
                    "targets": idx["drug_to_targets"][el],
                    "diseases": list(dict.fromkeys(idx["drug_to_diseases"].get(el, []))),
                })

    # ── Disease search ────────────────────────────────────────────────────
    if entity_type in ("disease", "auto"):
        for e in entities:
            if e in matched:
                continue
            el = e.lower()
            all_disease_keys = set(idx["disease_to_targets"]) | set(idx["disease_to_drugs"])
            hit_key = el if el in all_disease_keys else None
            if hit_key is None:
                candidates = [k for k in all_disease_keys if el in k or k in el]
                hit_key = candidates[0] if candidates else None
            if hit_key:
                matched.add(e)
                results.append({
                    "query": e,
                    "entity_type": "disease",
                    "disease_name": hit_key,
                    "targets": idx["disease_to_targets"].get(hit_key, []),
                    "drugs": list(dict.fromkeys(idx["disease_to_drugs"].get(hit_key, []))),
                })

    # ── Not found ─────────────────────────────────────────────────────────
    for e in entities:
        if e not in matched:
            results.append({"query": e, "entity_type": "not_found",
                            "message": "No match found in TTD."})

    return results


def query_json(
    entities: Union[str, list[str]],
    entity_type: str = "auto",
    data_dir: str = DATA_DIR,
) -> str:
    """Same as query() but returns a compact JSON string (for LLM consumption)."""
    return json.dumps(query(entities, entity_type, data_dir), ensure_ascii=False, indent=2)


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    entities = sys.argv[1:] if len(sys.argv) > 1 else ["EGFR", "Imatinib", "Lung cancer"]
    print(f"Querying TTD for: {entities}\n")
    print(query_json(entities))
