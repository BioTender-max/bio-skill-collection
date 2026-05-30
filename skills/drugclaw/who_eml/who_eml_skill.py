"""
WHOEssentialMedicinesSkill — WHO Essential Medicines List.

Subcategory : drug_knowledgebase
Access mode : LOCAL_FILE (WHO EML download)
Source      : https://www.who.int/publications/i/item/WHO-MHP-HPS-EML-2023.02
"""
from __future__ import annotations

import csv
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)


class WHOEssentialMedicinesSkill(RAGSkill):
    """WHO Essential Medicines List — globally essential drug classification."""

    name = "WHO Essential Medicines List"
    subcategory = "drug_knowledgebase"
    resource_type = "Database"
    access_mode = AccessMode.LOCAL_FILE
    aim = "Essential medicines"
    data_range = "WHO list of essential medicines with therapeutic category"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._rows: List[Dict] = []
        self._loaded = False

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        self._loaded = True
        path = self.config.get("csv_path", "") or self._discover_default_path()
        if not path or not os.path.exists(path):
            logger.warning("WHOEMLSkill: file not found — set config['csv_path']")
            return
        try:
            with open(path, newline="", encoding="utf-8") as fh:
                self._rows = list(csv.DictReader(fh))
            logger.info("WHO EML: loaded %d rows", len(self._rows))
        except Exception as exc:
            logger.error("WHO EML: load failed — %s", exc)

    def _discover_default_path(self) -> str:
        repo_root = Path(__file__).resolve().parents[3]
        base = repo_root / "resources_metadata" / "drug_knowledgebase" / "WHO_EML"
        candidates = [
            base / "eml.csv",
            base / "eml_medicines.csv",
            base / "who_eml.csv",
            base / "medicines.csv",
        ]
        for path in candidates:
            if path.exists():
                return str(path)
        return ""

    def is_available(self) -> bool:
        self._ensure_loaded()
        return bool(self._rows)

    def retrieve(
        self,
        entities: Dict[str, List[str]],
        query: str = "",
        max_results: int = 20,
        **kwargs: Any,
    ) -> List[RetrievalResult]:
        self._ensure_loaded()
        results: List[RetrievalResult] = []
        drug_names_lower = {d.lower() for d in entities.get("drug", [])}

        for row in self._rows:
            if len(results) >= max_results:
                break
            drug = row.get("medicine", "") or row.get("drug", "") or row.get("name", "")
            category = row.get("therapeutic_category", "") or row.get("category", "")
            if not drug:
                continue
            if drug_names_lower and drug.lower() not in drug_names_lower:
                # partial match
                if not any(q in drug.lower() for q in drug_names_lower):
                    continue
            results.append(RetrievalResult(
                source_entity=drug,
                source_type="drug",
                target_entity=category or "essential_medicine",
                target_type="therapeutic_category",
                relationship="classified_as_essential",
                weight=1.0,
                source="WHO Essential Medicines List",
                skill_category="drug_knowledgebase",
                evidence_text=f"WHO EML: {drug} is classified as essential medicine [{category}]",
                metadata={k: v for k, v in row.items()},
            ))
        return results
