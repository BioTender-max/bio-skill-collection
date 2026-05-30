"""
MecDDISkill — MecDDI Mechanistic DDI Database.

Subcategory : ddi
Access mode : LOCAL_FILE
Download    : https://mecddi.idrblab.net/download

MecDDI provides drug-drug interactions with detailed mechanistic explanations.
"""
from __future__ import annotations

import csv
import logging
import os
from collections import defaultdict
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)


class MecDDISkill(RAGSkill):
    """MecDDI — mechanistic DDI database with interaction mechanisms."""

    name = "MecDDI"
    subcategory = "ddi"
    resource_type = "Database"
    access_mode = AccessMode.LOCAL_FILE
    aim = "Mechanistic DDI database"
    data_range = "DDI database with mechanistic explanations"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._drug_index: Dict[str, List[Dict]] = defaultdict(list)
        self._loaded = False

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        self._loaded = True
        path = self.config.get("csv_path", "")
        if not path or not os.path.exists(path):
            logger.warning("MecDDISkill: file not found — set config['csv_path']")
            return
        try:
            with open(path, newline="", encoding="utf-8") as fh:
                for row in csv.DictReader(fh):
                    d1 = row.get("drug1", "") or row.get("Drug1", "")
                    d2 = row.get("drug2", "") or row.get("Drug2", "")
                    if d1: self._drug_index[d1.lower()].append(row)
                    if d2: self._drug_index[d2.lower()].append(row)
        except Exception as exc:
            logger.error("MecDDI: load failed — %s", exc)
            return

        self._build_fuzzy_index(self._drug_index.keys())

    def is_available(self) -> bool:
        self._ensure_loaded()
        return bool(self._drug_index)

    def retrieve(
        self,
        entities: Dict[str, List[str]],
        query: str = "",
        max_results: int = 20,
        **kwargs: Any,
    ) -> List[RetrievalResult]:
        self._ensure_loaded()
        results: List[RetrievalResult] = []
        for drug in entities.get("drug", []):
            for row in self._fuzzy_get(drug, self._drug_index):
                if len(results) >= max_results:
                    break
                d1 = row.get("drug1", "") or row.get("Drug1", "")
                d2 = row.get("drug2", "") or row.get("Drug2", "")
                mech = row.get("mechanism", "")
                results.append(RetrievalResult(
                    source_entity=d1,
                    source_type="drug",
                    target_entity=d2,
                    target_type="drug",
                    relationship="mechanistic_ddi",
                    weight=1.0,
                    source="MecDDI",
                    skill_category="ddi",
                    evidence_text=f"MecDDI: {d1} ↔ {d2}: {mech}",
                    metadata={"mechanism": mech},
                ))
        return results
