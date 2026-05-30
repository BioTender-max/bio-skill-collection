"""
SemaTyP - Drug-Disease Association Knowledge Graph
Category: Drug-centric | Type: KG | Subcategory: Drug-Disease Associations
Link: https://github.com/ShengtianSang/SemaTyP
Paper: https://link.springer.com/article/10.1186/s12859-018-2167-5

SemaTyP is a knowledge graph linking drugs, diseases, and targets extracted
from SemMedDB literature mining, combined with TTD curated associations,
for drug discovery and repositioning.

Access: Local files (download from GitHub).
"""

import os
import json
from pathlib import Path
from collections import defaultdict
from typing import Union

# ── Point this to your local SemaTyP-main directory ──────────────────────
DATA_DIR = os.environ.get(
    "SEMATYP_DATA_DIR",
    str(
        Path(__file__).resolve().parents[3]
        / "resources_metadata"
        / "drug_disease"
        / "SemaTyP"
        / "SemaTyP-main"
    ),
)


# ---------------------------------------------------------------------------
# Lazy-loaded data store
# ---------------------------------------------------------------------------

class _Store:
    """Singleton that loads and indexes all SemaTyP data on first access."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._loaded = False
        return cls._instance

    # ── index containers ──
    # predications: entity_lower -> list of triple dicts
    # ttd_drug_disease: drug_lower -> list of {drug, disease, icd9, icd10, ttdid}
    # processed maps: entity_lower -> list of partner strings

    def _ensure(self):
        if self._loaded:
            return
        self.pred_by_entity = defaultdict(list)     # predications.txt
        self.ttd_drug_disease = defaultdict(list)    # TTD drug-disease
        self.ttd_target_disease = defaultdict(list)  # TTD target-disease
        self.proc_drug_disease = defaultdict(list)   # processed/drug_disease
        self.proc_disease_drug = defaultdict(list)   # processed/disease_drug
        self.proc_disease_targets = defaultdict(list) # processed/disease_targets

        self._load_predications()
        self._load_ttd_drug_disease()
        self._load_ttd_target_disease()
        self._load_processed("drug_disease",     self.proc_drug_disease)
        self._load_processed("disease_drug",     self.proc_disease_drug)
        self._load_processed("disease_targets",  self.proc_disease_targets)
        self._loaded = True

    # ── loaders ──

    def _load_predications(self):
        path = os.path.join(DATA_DIR, "data", "SemmedDB", "predications.txt")
        if not os.path.isfile(path):
            return
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 4:
                    continue
                subj    = parts[0].strip()
                obj     = parts[1].strip()
                context = parts[2].strip() if len(parts) > 2 else ""
                pred    = parts[3].strip() if len(parts) > 3 else ""
                s_type  = parts[4].strip() if len(parts) > 4 else ""
                o_type  = parts[5].strip() if len(parts) > 5 else ""
                rec = {"subject": subj, "object": obj, "predicate": pred,
                       "context": context, "subj_type": s_type, "obj_type": o_type}
                self.pred_by_entity[subj.lower()].append(rec)
                self.pred_by_entity[obj.lower()].append(rec)

    def _load_ttd_drug_disease(self):
        path = os.path.join(DATA_DIR, "data", "TTD", "drug-disease_TTD2016.txt")
        if not os.path.isfile(path):
            return
        with open(path, encoding="utf-8", errors="replace") as f:
            header = True
            for line in f:
                if header:
                    header = False
                    continue
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 3:
                    continue
                ttdid   = parts[0].strip()
                drug    = parts[1].strip()
                disease = parts[2].strip()
                icd9    = parts[3].strip() if len(parts) > 3 else ""
                icd10   = parts[4].strip() if len(parts) > 4 else ""
                rec = {"ttdid": ttdid, "drug": drug, "disease": disease,
                       "icd9": icd9, "icd10": icd10}
                self.ttd_drug_disease[drug.lower()].append(rec)
                self.ttd_drug_disease[disease.lower()].append(rec)

    def _load_ttd_target_disease(self):
        path = os.path.join(DATA_DIR, "data", "TTD", "target-disease_TTD2016.txt")
        if not os.path.isfile(path):
            return
        with open(path, encoding="utf-8", errors="replace") as f:
            header = True
            for line in f:
                if header:
                    header = False
                    continue
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 3:
                    continue
                rec = {"target_id": parts[0].strip(),
                       "target": parts[1].strip(),
                       "disease": parts[2].strip()}
                if len(parts) > 3:
                    rec["icd9"] = parts[3].strip()
                if len(parts) > 4:
                    rec["icd10"] = parts[4].strip()
                self.ttd_target_disease[rec["target"].lower()].append(rec)
                self.ttd_target_disease[rec["disease"].lower()].append(rec)

    def _load_processed(self, name: str, store: dict):
        path = os.path.join(DATA_DIR, "data", "processed", name)
        if not os.path.isfile(path):
            return
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                parts = line.rstrip("\n").split("\t")
                if len(parts) >= 2:
                    key = parts[0].strip()
                    val = parts[1].strip()
                    rest = [p.strip() for p in parts[2:]] if len(parts) > 2 else []
                    store[key.lower()].append({"from": key, "to": val, "extra": rest})
                    store[val.lower()].append({"from": key, "to": val, "extra": rest})


_store = _Store()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_predications(entity: str, limit: int = 50) -> list[dict]:
    """Get SemMedDB predication triples involving an entity."""
    _store._ensure()
    return _store.pred_by_entity.get(entity.lower(), [])[:limit]


def get_ttd_drug_disease(entity: str) -> list[dict]:
    """Get TTD drug-disease associations involving a drug or disease name."""
    _store._ensure()
    return _store.ttd_drug_disease.get(entity.lower(), [])


def get_ttd_target_disease(entity: str) -> list[dict]:
    """Get TTD target-disease associations involving a target or disease name."""
    _store._ensure()
    return _store.ttd_target_disease.get(entity.lower(), [])


def get_processed_drug_disease(entity: str) -> list[dict]:
    """Get processed drug-disease links."""
    _store._ensure()
    return _store.proc_drug_disease.get(entity.lower(), [])


def get_processed_disease_drug(entity: str) -> list[dict]:
    """Get processed disease-drug links."""
    _store._ensure()
    return _store.proc_disease_drug.get(entity.lower(), [])


def get_processed_disease_targets(entity: str) -> list[dict]:
    """Get processed disease-target links."""
    _store._ensure()
    return _store.proc_disease_targets.get(entity.lower(), [])


def query(entities: Union[str, list[str]], fields: str = "all",
          pred_limit: int = 50) -> list[dict]:
    """
    Unified query interface. Accepts one or more entity names (drug, disease,
    gene/target, or any biomedical concept in SemMedDB).

    Parameters
    ----------
    entities : str or list[str]
        Entity name(s) to search (case-insensitive).
    fields : str
        'all'          — all sources.
        'predications' — SemMedDB KG triples only.
        'ttd'          — TTD curated associations only.
        'processed'    — processed drug-disease / disease-target only.
    pred_limit : int
        Max predication triples per entity (default 50).

    Returns
    -------
    list[dict] — one dict per entity with query results.
    """
    if isinstance(entities, str):
        entities = [entities]

    results = []
    for entity in entities:
        entity = entity.strip()
        if not entity:
            continue

        record = {"query": entity}
        try:
            if fields in ("all", "predications"):
                preds = get_predications(entity, limit=pred_limit)
                record["predications"] = preds
                record["predication_count"] = len(preds)

            if fields in ("all", "ttd"):
                record["ttd_drug_disease"] = get_ttd_drug_disease(entity)
                record["ttd_target_disease"] = get_ttd_target_disease(entity)

            if fields in ("all", "processed"):
                record["processed_drug_disease"] = get_processed_drug_disease(entity)
                record["processed_disease_drug"] = get_processed_disease_drug(entity)
                record["processed_disease_targets"] = get_processed_disease_targets(entity)

        except Exception as e:
            record["error"] = str(e)

        results.append(record)

    return results


# ---------------------------------------------------------------------------
# Usage examples (LLM-friendly)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # --- Example 1: Query a single drug ---
    print("=== Single drug: aspirin ===")
    out = query("aspirin")
    print(json.dumps(out, indent=2, ensure_ascii=False)[:800])

    # --- Example 2: Query multiple entities ---
    print("\n=== Batch query: metformin, diabetes ===")
    out = query(["metformin", "diabetes"])
    for item in out:
        print(f"  {item['query']}:")
        print(f"    predications:    {item.get('predication_count', 0)}")
        print(f"    ttd_drug_dis:    {len(item.get('ttd_drug_disease', []))}")
        print(f"    ttd_target_dis:  {len(item.get('ttd_target_disease', []))}")
        print(f"    proc_drug_dis:   {len(item.get('processed_drug_disease', []))}")
        print(f"    proc_dis_drug:   {len(item.get('processed_disease_drug', []))}")
        print(f"    proc_dis_target: {len(item.get('processed_disease_targets', []))}")

    # --- Example 3: KG predications only ---
    print("\n=== Predications only: imatinib ===")
    out = query("imatinib", fields="predications", pred_limit=5)
    print(json.dumps(out, indent=2, ensure_ascii=False)[:600])

    # --- Example 4: TTD curated only ---
    print("\n=== TTD only: Schizophrenia ===")
    out = query("Schizophrenia", fields="ttd")
    print(json.dumps(out, indent=2, ensure_ascii=False)[:600])

    # --- Example 5: Processed associations only ---
    print("\n=== Processed only: cancer ===")
    out = query("cancer", fields="processed")
    print(json.dumps(out, indent=2, ensure_ascii=False)[:600])
