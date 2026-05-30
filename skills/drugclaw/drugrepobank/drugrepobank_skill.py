"""
DrugRepoBankSkill — DrugRepoBank Drug Repurposing Repository.

Subcategory : drug_repurposing
Access mode : LOCAL_FILE
Source      : https://drugrepodb.idrblab.net/
              (also known as DrugRepoDB / DRDDB)

DrugRepoBank is a comprehensive resource of approved drugs with their
repurposing candidates, clinical trial evidence, and disease associations.

Config keys
-----------
csv_path  : str  path to DrugRepoBank CSV/TSV export
              Expected columns: Drug (or drug_name), Disease (or indication),
                                Status (or clinical_phase), [PMID], [Source]
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


class DrugRepoBankSkill(RAGSkill):
    """DrugRepoBank — curated drug repurposing data with clinical trial evidence."""

    name = "DrugRepoBank"
    subcategory = "drug_repurposing"
    resource_type = "Database"
    access_mode = AccessMode.LOCAL_FILE
    aim = "Repurposing repository"
    data_range = "Curated drug repurposing data with clinical trial evidence"
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
                "DrugRepoBankSkill: file not found. "
                "Download from https://drugrepodb.idrblab.net/ "
                "and set config['csv_path']."
            )
            return
        delim = self.config.get("delimiter", "\t" if path.endswith(".tsv") else ",")
        try:
            with open(path, newline="", encoding="utf-8", errors="ignore") as fh:
                for row in csv.DictReader(fh, delimiter=delim):
                    drug = (row.get("Drug", "") or row.get("drug_name", "") or
                            row.get("drug", "") or row.get("compound", "")).strip()
                    disease = (row.get("Disease", "") or row.get("indication", "") or
                               row.get("disease", "") or row.get("Indication", "")).strip()
                    if drug and disease:
                        idx = len(self._rows)
                        self._rows.append(row)
                        self._drug_index[drug.lower()].append(idx)
                        self._disease_index[disease.lower()].append(idx)
            logger.info("DrugRepoBank: loaded %d repurposing records", len(self._rows))
        except Exception as exc:
            logger.error("DrugRepoBank: load failed — %s", exc)
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
                drug = (row.get("Drug", "") or row.get("drug_name", "") or
                        row.get("drug", "")).strip()
                disease = (row.get("Disease", "") or row.get("indication", "") or
                           row.get("disease", "")).strip()
                status = (row.get("Status", "") or row.get("clinical_phase", "") or
                          row.get("phase", "")).strip()
                pmid = row.get("PMID", "") or row.get("pmid", "")
                results.append(RetrievalResult(
                    source_entity=drug,
                    source_type="drug",
                    target_entity=disease,
                    target_type="disease",
                    relationship="repurposed_for",
                    weight=1.0,
                    source="DrugRepoBank",
                    skill_category="drug_repurposing",
                    evidence_text=(
                        f"DrugRepoBank: {drug} repurposed for {disease}"
                        + (f" [{status}]" if status else "")
                    ),
                    sources=[f"PMID:{pmid}"] if pmid else [],
                    metadata={"status": status, "pmid": pmid},
                ))

        for drug in entities.get("drug", []):
            _add(self._fuzzy_get(drug, self._drug_index, "_drug_fuzzy"))
        for disease in entities.get("disease", []):
            _add(self._fuzzy_get(disease, self._disease_index, "_disease_fuzzy"))
        return results
