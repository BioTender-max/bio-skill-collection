"""
WebMDReviewsSkill — WebMD Drug Reviews Dataset.

Subcategory : drug_review
Access mode : DATASET (local CSV)
Source      : https://www.kaggle.com/datasets/rohanharode07/webmd-drug-reviews-dataset
              Original: scrapped from WebMD.com; 362,806 patient reviews.

Config keys
-----------
csv_path : str  path to webmd_drug_reviews.csv
              Expected columns: drug (or Drug), condition (or Condition),
                                review (or Review, comment), rating (or Rating),
                                [date], [usefulCount], [sideEffects], [effectiveness]
delimiter : str  column delimiter (default: ",")
"""
from __future__ import annotations

import csv
import logging
import os
from collections import defaultdict
from typing import Any, Dict, List, Optional

from ...base import DatasetRAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)


class WebMDReviewsSkill(DatasetRAGSkill):
    """WebMD Drug Reviews — 362,000+ patient drug reviews."""

    name = "WebMD Drug Reviews"
    subcategory = "drug_review"
    resource_type = "Dataset"
    access_mode = AccessMode.DATASET
    aim = "Patient drug reviews (WebMD)"
    data_range = "362 000+ patient drug reviews from WebMD"
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
                "WebMDReviewsSkill: file not found. "
                "Download from https://www.kaggle.com/datasets/rohanharode07/webmd-drug-reviews-dataset "
                "and set config['csv_path']."
            )
            return
        delim = self.config.get("delimiter", ",")
        max_rows = int(self.config.get("max_rows", 100000))
        try:
            with open(path, newline="", encoding="utf-8", errors="ignore") as fh:
                for row in csv.DictReader(fh, delimiter=delim):
                    drug = (row.get("drug", "") or row.get("Drug", "") or
                            row.get("drugName", "")).strip()
                    if drug:
                        idx = len(self._rows)
                        self._rows.append(row)
                        self._drug_index[drug.lower()].append(idx)
                        condition = (row.get("condition", "") or row.get("Condition", "") or
                                     row.get("usedFor", "")).strip()
                        if condition:
                            self._condition_index[condition.lower()].append(idx)
                    if len(self._rows) >= max_rows:
                        break
            logger.info("WebMD Reviews: loaded %d reviews", len(self._rows))
        except Exception as exc:
            logger.error("WebMD Reviews: load failed — %s", exc)
            return

        self._build_fuzzy_index(self._drug_index.keys(), "_drug_fuzzy")
        self._build_fuzzy_index(self._condition_index.keys(), "_condition_fuzzy")

    def is_available(self) -> bool:
        return self._implemented

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
                drug = (row.get("drug", "") or row.get("Drug", "") or
                        row.get("drugName", "")).strip()
                condition = (row.get("condition", "") or row.get("Condition", "") or
                             row.get("usedFor", "")).strip()
                rating = row.get("rating", "") or row.get("Rating", "") or row.get("overallCondition", "")
                review = (row.get("review", "") or row.get("Review", "") or
                          row.get("comment", ""))[:300].strip()
                results.append(RetrievalResult(
                    source_entity=drug,
                    source_type="drug",
                    target_entity=condition or "general",
                    target_type="condition",
                    relationship="patient_review",
                    weight=1.0,
                    source="WebMD Drug Reviews",
                    skill_category="drug_review",
                    evidence_text=f"WebMD review for {drug}"
                                  + (f" [{condition}]" if condition else "")
                                  + (f" (rating={rating}/5)" if rating else "")
                                  + (f": {review}" if review else ""),
                    metadata={"rating": rating, "condition": condition},
                ))

        for drug in entities.get("drug", []):
            _add(self._fuzzy_get(drug, self._drug_index, "_drug_fuzzy"))
        for disease in entities.get("disease", []):
            _add(self._fuzzy_get(disease, self._condition_index, "_condition_fuzzy"))
        return results

    def get_all_pairs(self) -> List[Dict[str, Any]]:
        self._ensure_loaded()
        return [
            {
                "drug": (r.get("drug", "") or r.get("Drug", "") or r.get("drugName", "")).strip(),
                "disease": (r.get("condition", "") or r.get("Condition", "") or r.get("usedFor", "")).strip(),
                "label": r.get("rating", "") or r.get("Rating", ""),
            }
            for r in self._rows
        ]
