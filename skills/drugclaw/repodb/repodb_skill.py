"""
RepoDBSkill — RepoDB drug repositioning outcomes.

Subcategory : drug_repurposing
Access mode : DATASET (local CSV)
Download    : https://unmtid-shinyapps.net/shiny/repodb/
"""
from __future__ import annotations

import csv
import logging
import os
from collections import defaultdict
from typing import Any, Dict, List, Optional, Set

from ...base import DatasetRAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)


# 定义哪些列作为边的目标节点，以及对应的 target_type
EDGE_FIELDS = {
    "drugbank_id":    "drugbank_id",
    "ind_name":       "disease",
    "ind_id":         "disease_id",
    "NCT":            "clinical_trial",
    "status":         "status",
    "phase":          "phase",
    "DetailedStatus": "detailed_status",
}

class RepoDBSkill(DatasetRAGSkill):
    """RepoDB — labelled drug-disease repositioning pairs from clinical trials."""

    name = "RepoDB"
    subcategory = "drug_repurposing"
    resource_type = "Dataset"
    access_mode = AccessMode.DATASET
    aim = "Drug repositioning outcomes"
    data_range = "Labelled drug-disease repositioning pairs from clinical trials"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._rows: List[Dict] = []
        self._drug_index: Dict[str, List[int]] = defaultdict(list)
        self._disease_index: Dict[str, List[int]] = defaultdict(list)
        self._include_failed = bool(self.config.get("include_failed", False))
        self.EDGE_FIELDS = EDGE_FIELDS

    def _load(self) -> None:
        path = self.config.get("csv_path", "")
        if not path or not os.path.exists(path):
            logger.warning("RepoDBSkill: repodb.csv not found — set config['csv_path']")
            return
        try:
            with open(path, newline="", encoding="utf-8") as fh:
                for row in csv.DictReader(fh):
                    drug_name  = row.get("drug_name",   "").strip()
                    drugbank_id = row.get("drugbank_id", "").strip()
                    ind_name   = row.get("ind_name",    "").strip()
                    ind_id     = row.get("ind_id",      "").strip()

                    if not (drug_name or drugbank_id):
                        continue

                    idx = len(self._rows)
                    self._rows.append(row)

                    # 四个字段都建索引
                    if drug_name:
                        self._drug_index[drug_name.lower()].append(idx)
                    if drugbank_id:
                        self._drug_index[drugbank_id.lower()].append(idx)
                    if ind_name:
                        self._disease_index[ind_name.lower()].append(idx)
                    if ind_id:
                        self._disease_index[ind_id.lower()].append(idx)

            logger.info("RepoDB: loaded %d pairs", len(self._rows))
        except Exception as exc:
            logger.error("RepoDB: cannot load %s — %s", path, exc)
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
        max_results: int = 100,
        **kwargs: Any,
    ) -> List[RetrievalResult]:
        self._ensure_loaded()
        results: List[RetrievalResult] = []
        seen_rows: Set[tuple] = set()
        normalized_query = str(query or "").strip().lower()
        repurposing_query = any(
            marker in normalized_query
            for marker in (
                "repurposing",
                "repositioning",
                "reposition",
                "approved indication",
                "approved indications",
                "indication",
                "indications",
            )
        )

        def _build_edges(idx_list, query_entity: str):
            for idx in idx_list:
                row = self._rows[idx]
                status = row.get("status", "Unknown")
                if not self._include_failed and status != "Approved" and not repurposing_query:
                    continue

                drug_name = row.get("drug_name", "").strip()
                disease_name = row.get("ind_name", "").strip()
                if not drug_name or not disease_name:
                    continue

                row_key = (
                    drug_name.lower(),
                    disease_name.lower(),
                    row.get("NCT", "").strip().lower(),
                    status.strip().lower(),
                    row.get("phase", "").strip().lower(),
                )
                if row_key in seen_rows or len(results) >= max_results:
                    continue
                seen_rows.add(row_key)

                results.append(
                    RetrievalResult(
                        source_entity=drug_name,
                        source_type="drug",
                        target_entity=disease_name,
                        target_type="disease",
                        relationship="repurposing_evidence",
                        weight=1.0,
                        source="RepoDB",
                        skill_category="drug_repurposing",
                        evidence_text=(
                            f"RepoDB: {drug_name} repurposing evidence for {disease_name} "
                            f"(status={status}, phase={row.get('phase', '').strip() or 'Unknown'})"
                        ),
                        metadata={k: v.strip() for k, v in row.items()},
                    )
                )

        for drug in entities.get("drug", []):
            _build_edges(self._fuzzy_get(drug, self._drug_index, "_drug_fuzzy"), drug)

        for disease in entities.get("disease", []):
            _build_edges(self._fuzzy_get(disease, self._disease_index, "_disease_fuzzy"), disease)

        return results

    def get_all_pairs(self) -> List[Dict[str, Any]]:
        self._ensure_loaded()
        return [
            {"drug": r.get("drug_name", ""), "disease": r.get("ind_name", ""),
             "label": r.get("status", ""), "phase": r.get("phase", "")}
            for r in self._rows
        ]

    def get_approved_pairs(self) -> List[Dict[str, Any]]:
        return [p for p in self.get_all_pairs() if p["label"] == "Approved"]
