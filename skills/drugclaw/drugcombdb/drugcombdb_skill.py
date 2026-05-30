"""
DrugCombDBSkill — DrugCombDB Drug Combination Database.

Subcategory : drug_combination
Access mode : LOCAL_FILE
Download    : http://drugcombdb.idrblab.net/main/
Paper       : "DrugCombDB: a comprehensive database of drug combinations" (2019)

Config keys
-----------
csv_path  : str  path to DrugCombDB CSV file
              Expected columns: Drug1, Drug2, Cell (or CellLine), Synergy (or Score),
                                [Mechanism], [PMID]
delimiter : str  column delimiter (default: auto-detect)
"""
from __future__ import annotations

import csv
import logging
import os
from collections import defaultdict
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)


class DrugCombDBSkill(RAGSkill):
    """DrugCombDB — drug combination synergy/antagonism records."""

    name = "DrugCombDB"
    subcategory = "drug_combination"
    resource_type = "Database"
    access_mode = AccessMode.LOCAL_FILE
    aim = "Drug combination database"
    data_range = "Human/animal drug combination synergy/antagonism records"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._rows: List[Dict] = []
        self._drug_index: Dict[str, List[int]] = defaultdict(list)
        self._loaded = False

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        self._loaded = True
        path = self.config.get("csv_path", "")
        if not path or not os.path.exists(path):
            logger.warning(
                "DrugCombDBSkill: file not found. "
                "Download from http://drugcombdb.idrblab.net/ "
                "and set config['csv_path']."
            )
            return
        delim = self.config.get("delimiter", "\t" if path.endswith(".tsv") else ",")
        try:
            with open(path, newline="", encoding="utf-8", errors="ignore") as fh:
                for row in csv.DictReader(fh, delimiter=delim):
                    d1 = (row.get("Drug1", "") or row.get("drug1", "") or
                           row.get("Drug_1", "")).strip()
                    d2 = (row.get("Drug2", "") or row.get("drug2", "") or
                           row.get("Drug_2", "")).strip()
                    if d1 and d2:
                        idx = len(self._rows)
                        self._rows.append(row)
                        self._drug_index[d1.lower()].append(idx)
                        self._drug_index[d2.lower()].append(idx)
            logger.info("DrugCombDB: loaded %d drug-combination records", len(self._rows))
        except Exception as exc:
            logger.error("DrugCombDB: load failed — %s", exc)
            return

        self._build_fuzzy_index(self._drug_index.keys())

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

        for drug in entities.get("drug", []):
            for idx in self._fuzzy_get(drug, self._drug_index):
                if len(results) >= max_results or idx in seen:
                    continue
                seen.add(idx)
                row = self._rows[idx]
                d1 = (row.get("Drug1", "") or row.get("drug1", "") or
                       row.get("Drug_1", "")).strip()
                d2 = (row.get("Drug2", "") or row.get("drug2", "") or
                       row.get("Drug_2", "")).strip()
                synergy = (row.get("Synergy", "") or row.get("synergy_score", "") or
                           row.get("Score", "") or row.get("CSS", "")).strip()
                cell = (row.get("Cell", "") or row.get("CellLine", "") or
                        row.get("cell_line", "")).strip()
                synergy_type = (row.get("SynergyType", "") or row.get("Combination_type", "")).strip()
                rel = "drug_combination_synergy" if not synergy_type else f"drug_combination_{synergy_type.lower().replace(' ', '_')}"
                evidence = f"DrugCombDB: {d1} + {d2}"
                if cell:
                    evidence += f" in {cell}"
                if synergy:
                    evidence += f" (score={synergy})"
                results.append(RetrievalResult(
                    source_entity=d1,
                    source_type="drug",
                    target_entity=d2,
                    target_type="drug",
                    relationship=rel,
                    weight=1.0,
                    source="DrugCombDB",
                    skill_category="drug_combination",
                    evidence_text=evidence,
                    metadata={
                        "synergy_score": synergy,
                        "cell_line": cell,
                        "synergy_type": synergy_type,
                        "pmid": row.get("PMID", ""),
                    },
                ))
        return results
