"""
CADECSkill — CSIRO Adverse Drug Event Corpus (CADEC).

Subcategory : drug_nlp
Access mode : DATASET (local files)
Source      : https://data.csiro.au/collection/csiro:10948v3
Paper       : Karimi et al. (2015), J. Biomed. Inform.

CADEC contains annotated adverse drug events from social media (AskAPatient),
covering drug entities, adverse events, symptoms, and diseases.

Config keys
-----------
csv_path  : str  path to CADEC pre-parsed CSV
              Expected columns: drug, adverse_event (or ae), text, [label]
tsv_path  : str  alternative TSV path
delimiter : str  column delimiter (default: auto-detect)
"""
from __future__ import annotations

import csv
import logging
import os
from collections import defaultdict
from typing import Any, Dict, List, Optional

from ...base import DatasetRAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)


class CADECSkill(DatasetRAGSkill):
    """CADEC — CSIRO annotated drug side-effect corpus from social media."""

    name = "CADEC"
    subcategory = "drug_nlp"
    resource_type = "Dataset"
    access_mode = AccessMode.DATASET
    aim = "Clinical ADE corpus"
    data_range = "CSIRO annotated drug side-effect corpus from social media"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._rows: List[Dict] = []
        self._drug_index: Dict[str, List[int]] = defaultdict(list)

    def _load(self) -> None:
        path = self.config.get("csv_path", "") or self.config.get("tsv_path", "")
        if not path or not os.path.exists(path):
            logger.warning(
                "CADECSkill: file not found. "
                "Download from https://data.csiro.au/collection/csiro:10948v3 "
                "and set config['csv_path']."
            )
            return
        delim = self.config.get("delimiter", "\t" if path.endswith(".tsv") else ",")
        try:
            with open(path, newline="", encoding="utf-8", errors="ignore") as fh:
                for row in csv.DictReader(fh, delimiter=delim):
                    drug = (row.get("drug", "") or row.get("Drug", "") or
                            row.get("medication", "")).strip()
                    if drug:
                        idx = len(self._rows)
                        self._rows.append(row)
                        self._drug_index[drug.lower()].append(idx)
            logger.info("CADEC: loaded %d records", len(self._rows))
        except Exception as exc:
            logger.error("CADEC: load failed — %s", exc)
            return

        self._build_fuzzy_index(self._drug_index.keys())

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
        for drug in entities.get("drug", []):
            for idx in self._fuzzy_get(drug, self._drug_index):
                if len(results) >= max_results:
                    break
                row = self._rows[idx]
                drug_name = (row.get("drug", "") or row.get("Drug", drug)).strip()
                ae = (row.get("adverse_event", "") or row.get("ae", "") or
                      row.get("ADE", "")).strip()
                text = row.get("text", "")[:200]
                results.append(RetrievalResult(
                    source_entity=drug_name,
                    source_type="drug",
                    target_entity=ae or "side_effect",
                    target_type="adverse_event",
                    relationship="social_media_ade",
                    weight=1.0,
                    source="CADEC",
                    skill_category="drug_nlp",
                    evidence_text=f"CADEC: {drug_name} -> {ae}" +
                                  (f" — {text}" if text else ""),
                    metadata={"label": row.get("label", "")},
                ))
        return results

    def get_all_pairs(self) -> List[Dict[str, Any]]:
        self._ensure_loaded()
        return [
            {"drug": (r.get("drug", "") or r.get("Drug", "")).strip(),
             "disease": (r.get("adverse_event", "") or r.get("ae", "")).strip(),
             "label": r.get("label", "positive_ade")}
            for r in self._rows
        ]
