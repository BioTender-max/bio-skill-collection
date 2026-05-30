"""
OREGANOSkill — Drug Repurposing Candidates with Clinical Evidence.

Subcategory : drug_repurposing
Access mode : LOCAL_FILE
Source      : https://github.com/fusion-jena/OREGANO
Paper       : "OREGANO: a knowledge graph for biomedical literature mining" (2022)

Download the dataset from GitHub and configure the path below.

Config keys
-----------
csv_path : str  path to oregano_drug_disease.csv or equivalent TSV/CSV file
              Expected columns: drug, disease, type (or relation), [evidence]
"""
from __future__ import annotations

import csv
import logging
import os
from collections import defaultdict
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)


class OREGANOSkill(RAGSkill):
    """
    OREGANO — drug repurposing predictions with clinical evidence.

    Expects a CSV/TSV file with at minimum: drug, disease columns.

    Config keys
    -----------
    csv_path  : str   path to OREGANO drug-disease CSV/TSV
    delimiter : str   column delimiter (default: auto-detect from extension)
    """

    name = "OREGANO"
    subcategory = "drug_repurposing"
    resource_type = "Database"
    access_mode = AccessMode.LOCAL_FILE
    aim = "Drug repurposing candidates"
    data_range = "Drug repurposing predictions with clinical evidence"
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
                "OREGANOSkill: file not found. "
                "Download from https://github.com/fusion-jena/OREGANO "
                "and set config['csv_path']."
            )
            return
        delim = self.config.get("delimiter", "\t" if path.endswith(".tsv") else ",")
        try:
            with open(path, newline="", encoding="utf-8") as fh:
                for row in csv.DictReader(fh, delimiter=delim):
                    drug = (
                        row.get("drug", "") or row.get("Drug", "") or
                        row.get("drug_name", "") or row.get("compound", "")
                    ).strip()
                    disease = (
                        row.get("disease", "") or row.get("Disease", "") or
                        row.get("disease_name", "") or row.get("indication", "")
                    ).strip()
                    if drug and disease:
                        idx = len(self._rows)
                        self._rows.append(row)
                        self._drug_index[drug.lower()].append(idx)
                        self._disease_index[disease.lower()].append(idx)
            logger.info("OREGANO: loaded %d drug-disease pairs", len(self._rows))
        except Exception as exc:
            logger.error("OREGANO: load failed — %s", exc)
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
        seen_idxs: set = set()

        def _add(idxs):
            for idx in idxs:
                if len(results) >= max_results or idx in seen_idxs:
                    return
                seen_idxs.add(idx)
                row = self._rows[idx]
                drug = (
                    row.get("drug", "") or row.get("Drug", "") or
                    row.get("drug_name", "") or row.get("compound", "")
                ).strip()
                disease = (
                    row.get("disease", "") or row.get("Disease", "") or
                    row.get("disease_name", "") or row.get("indication", "")
                ).strip()
                rel_type = (
                    row.get("type", "") or row.get("relation", "") or
                    row.get("association_type", "repurposing_candidate")
                ).strip().lower().replace(" ", "_") or "repurposing_candidate"
                evidence = row.get("evidence", "") or row.get("source", "")
                results.append(RetrievalResult(
                    source_entity=drug,
                    source_type="drug",
                    target_entity=disease,
                    target_type="disease",
                    relationship=rel_type,
                    weight=1.0,
                    source="OREGANO",
                    skill_category="drug_repurposing",
                    evidence_text=f"OREGANO: {drug} → {disease} [{rel_type}]"
                                  + (f" (evidence: {evidence})" if evidence else ""),
                    metadata={k: v for k, v in row.items()
                               if k not in ("drug", "Drug", "disease", "Disease")},
                ))

        for drug in entities.get("drug", []):
            _add(self._fuzzy_get(drug, self._drug_index, "_drug_fuzzy"))
        for disease in entities.get("disease", []):
            _add(self._fuzzy_get(disease, self._disease_index, "_disease_fuzzy"))
        return results
