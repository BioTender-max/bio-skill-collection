"""DILIrankSkill — FDA DILIrank Dataset (local)."""
from __future__ import annotations
import csv, logging, os
from collections import defaultdict
from typing import Any, Dict, List, Optional
from ...base import RAGSkill, RetrievalResult, AccessMode
logger = logging.getLogger(__name__)

class DILIrankSkill(RAGSkill):
    name = "DILIrank"; subcategory = "drug_toxicity"; resource_type = "Dataset"
    access_mode = AccessMode.LOCAL_FILE; aim = "DILI severity ranking"
    data_range = "FDA DILI severity ranking (most-DILI-concern to no-DILI-concern)"
    _implemented = True
    def __init__(self, config=None):
        super().__init__(config); self._drug_index=defaultdict(list); self._rows=[]; self._loaded=False
    def _ensure_loaded(self):
        if self._loaded: return
        self._loaded = True
        path = self.config.get("csv_path","")
        if not path or not os.path.exists(path): logger.warning("DILIrankSkill: set config['csv_path']"); return
        try:
            with open(path, newline="", encoding="utf-8") as fh:
                for row in csv.DictReader(fh):
                    drug = (row.get("Drug Name","") or row.get("drug","")).strip()
                    if drug: idx=len(self._rows); self._rows.append(row); self._drug_index[drug.lower()].append(idx)
        except Exception as e: logger.error("DILIrank load failed: %s", e); return
        self._build_fuzzy_index(self._drug_index.keys())
    def is_available(self): self._ensure_loaded(); return bool(self._rows)
    def retrieve(self, entities, query="", max_results=30, **kwargs):
        self._ensure_loaded(); results=[]
        for drug in entities.get("drug",[]):
            for idx in self._fuzzy_get(drug, self._drug_index):
                if len(results)>=max_results: break
                row=self._rows[idx]; rank=row.get("vDILIConcern","") or row.get("DILI Concern","")
                results.append(RetrievalResult(
                    source_entity=drug,
                    source_type="drug",
                    target_entity=rank or "DILI",
                    target_type="dili_concern",
                    relationship="has_dili_concern",
                    weight=1.0,
                    source="DILIrank",
                    evidence_text=f"DILIrank: {drug} → {rank}",
                    skill_category="drug_toxicity",
                    metadata={"rank":rank},
                ))
        return results
