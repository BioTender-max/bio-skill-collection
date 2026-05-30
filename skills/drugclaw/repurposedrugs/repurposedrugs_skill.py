"""
RepurposeDrugsSkill — RepurposeDrugs Open Drug Repurposing Portal.

Subcategory : drug_repurposing
Access mode : LOCAL_FILE
Source      : https://repurposedrugs.org/

RepurposeDrugs is an open portal aggregating disease-drug associations
from clinical trials, systematic reviews, and computational predictions.

Config keys
-----------
csv_path  : str  path to RepurposeDrugs CSV/TSV export
              Expected columns: drug (or Drug), disease (or Disease),
                                score (or confidence), status, [pmid]
delimiter : str  column delimiter (default: auto-detect from extension)
"""
from __future__ import annotations

import csv
import logging
import os
from collections import defaultdict
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)


class RepurposeDrugsSkill(RAGSkill):
    """RepurposeDrugs — open drug repurposing portal with disease-drug associations."""

    name = "RepurposeDrugs"
    subcategory = "drug_repurposing"
    resource_type = "Database"
    access_mode = AccessMode.LOCAL_FILE
    aim = "Repurposing portal"
    data_range = "Open drug repurposing portal with disease-drug associations"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._rows: List[Dict] = []
        self._drug_index: Dict[str, List[int]] = defaultdict(list)
        self._disease_index: Dict[str, List[int]] = defaultdict(list)
        self._loaded = False

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        self._loaded = True
        path = self.config.get("csv_path", "")
        if not path or not os.path.exists(path):
            logger.warning(
                "RepurposeDrugsSkill: file not found. "
                "Download from https://repurposedrugs.org/ "
                "and set config['csv_path']."
            )
            return
        delim = self.config.get("delimiter", "\t" if path.endswith(".tsv") else ",")
        try:
            with open(path, newline="", encoding="utf-8", errors="ignore") as fh:
                for row in csv.DictReader(fh, delimiter=delim):
                    drug = (row.get("drug", "") or row.get("Drug", "") or
                            row.get("compound", "")).strip()
                    disease = (row.get("disease", "") or row.get("Disease", "") or
                               row.get("indication", "")).strip()
                    if drug and disease:
                        idx = len(self._rows)
                        self._rows.append(row)
                        self._drug_index[drug.lower()].append(idx)
                        self._disease_index[disease.lower()].append(idx)
            logger.info("RepurposeDrugs: loaded %d records", len(self._rows))
        except Exception as exc:
            logger.error("RepurposeDrugs: load failed — %s", exc)
            return

        self._build_fuzzy_index(self._drug_index.keys(), "_drug_fuzzy")
        self._build_fuzzy_index(self._disease_index.keys(), "_disease_fuzzy")

    def is_available(self) -> bool:
        self._ensure_loaded()
        return bool(self._rows)

    def retrieve(
        self,
        entities: Dict[str, List[str]],
        query: str = "",
        max_results: int = 30,
        **kwargs: Any,
    ) -> List[RetrievalResult]:
        self._ensure_loaded()
        results: List[RetrievalResult] = []
        seen: set = set()

        def _add(idxs):
            for idx in idxs:
                if len(results) >= max_results or idx in seen:
                    return
                seen.add(idx)
                row = self._rows[idx]
                drug = (row.get("drug", "") or row.get("Drug", "")).strip()
                disease = (row.get("disease", "") or row.get("Disease", "")).strip()
                status = (row.get("status", "") or row.get("Status", "")).strip()
                score = row.get("score", "") or row.get("confidence", "")
                results.append(RetrievalResult(
                    source_entity=drug,
                    source_type="drug",
                    target_entity=disease,
                    target_type="disease",
                    relationship="repurposed_for",
                    weight=float(score) if score else 1.0,
                    source="RepurposeDrugs",
                    skill_category="drug_repurposing",
                    evidence_text=(
                        f"RepurposeDrugs: {drug} → {disease}"
                        + (f" [{status}]" if status else "")
                        + (f" (score={score})" if score else "")
                    ),
                    metadata={"status": status, "score": score},
                ))

        for drug in entities.get("drug", []):
            _add(self._fuzzy_get(drug, self._drug_index, "_drug_fuzzy"))
        for disease in entities.get("disease", []):
            _add(self._fuzzy_get(disease, self._disease_index, "_disease_fuzzy"))
        return results
