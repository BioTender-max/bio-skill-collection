"""
DrugsComReviewsSkill — Drugs.com Drug Reviews Dataset (UCI).

Subcategory : drug_review
Access mode : DATASET (local CSV)
Source      : UCI Machine Learning Repository
              https://archive.ics.uci.edu/ml/datasets/Drug+Review+Dataset+%28Drugs.com%29
Paper       : Graber & Kallumadi (2018)

Config keys
-----------
csv_path  : str  path to drugsComTrain_raw.tsv or drugsComTest_raw.tsv
              Expected columns: drugName, condition, review, rating, date, usefulCount
delimiter : str  column delimiter (default: "\t")
"""
from __future__ import annotations

import csv
import logging
import os
from collections import defaultdict
from typing import Any, Dict, List, Optional

from ...base import DatasetRAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)


class DrugsComReviewsSkill(DatasetRAGSkill):
    """Drugs.com UCI drug reviews dataset — patient ratings and conditions."""

    name = "Drug Reviews (Drugs.com)"
    subcategory = "drug_review"
    resource_type = "Dataset"
    access_mode = AccessMode.DATASET
    aim = "Drug reviews dataset"
    data_range = "UCI/Drugs.com drug reviews with patient ratings"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._rows: List[Dict] = []
        self._drug_index: Dict[str, List[int]] = defaultdict(list)
        self._condition_index: Dict[str, List[int]] = defaultdict(list)

    def _load(self) -> None:
        path = self.config.get("csv_path", "")
        if not path or not os.path.exists(path):
            logger.warning(
                "DrugsComReviewsSkill: file not found. "
                "Download from https://archive.ics.uci.edu/ml/datasets/"
                "Drug+Review+Dataset+%28Drugs.com%29 "
                "and set config['csv_path']."
            )
            return
        delim = self.config.get("delimiter", "\t")
        max_rows = int(self.config.get("max_rows", 100000))
        try:
            with open(path, newline="", encoding="utf-8", errors="ignore") as fh:
                for row in csv.DictReader(fh, delimiter=delim):
                    drug = row.get("drugName", "").strip()
                    condition = row.get("condition", "").strip()
                    if drug:
                        idx = len(self._rows)
                        self._rows.append(row)
                        self._drug_index[drug.lower()].append(idx)
                        if condition:
                            self._condition_index[condition.lower()].append(idx)
                    if len(self._rows) >= max_rows:
                        break
            logger.info("Drugs.com Reviews: loaded %d reviews", len(self._rows))
        except Exception as exc:
            logger.error("Drugs.com Reviews: load failed — %s", exc)
            return

        self._build_fuzzy_index(self._drug_index.keys(), "_drug_fuzzy")
        self._build_fuzzy_index(self._condition_index.keys(), "_condition_fuzzy")

    def is_available(self) -> bool:
        self._ensure_loaded()
        return bool(self._rows)

    def retrieve(
        self,
        entities: Dict[str, List[str]],
        query: str = "",
        max_results: int = 10,
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
                drug = row.get("drugName", "").strip()
                condition = row.get("condition", "").strip()
                rating = row.get("rating", "")
                review = row.get("review", "")[:300].strip().replace("&#039;", "'")
                results.append(RetrievalResult(
                    source_entity=drug,
                    source_type="drug",
                    target_entity=condition or "general",
                    target_type="condition",
                    relationship="patient_review",
                    weight=1.0,
                    source="Drug Reviews (Drugs.com)",
                    skill_category="drug_review",
                    evidence_text=f"Drugs.com review for {drug}"
                                  + (f" [{condition}]" if condition else "")
                                  + (f" (rating={rating}/10)" if rating else "")
                                  + (f": {review}" if review else ""),
                    metadata={"rating": rating, "condition": condition,
                              "useful_count": row.get("usefulCount", "")},
                ))

        for drug in entities.get("drug", []):
            _add(self._fuzzy_get(drug, self._drug_index, "_drug_fuzzy"))
        for disease in entities.get("disease", []):
            _add(self._fuzzy_get(disease, self._condition_index, "_condition_fuzzy"))
        return results

    def get_all_pairs(self) -> List[Dict[str, Any]]:
        self._ensure_loaded()
        return [
            {"drug": r.get("drugName", ""), "disease": r.get("condition", ""),
             "label": r.get("rating", "")}
            for r in self._rows
        ]
