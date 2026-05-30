"""
DrugCombSkill — DrugComb Drug Combination Screening Data.

Subcategory : drug_combination
Access mode : LOCAL_FILE
Download    : https://drugcomb.fimm.fi/
Paper       : "DrugComb: an integrative cancer drug combination data portal" (2019)

Config keys
-----------
csv_path  : str  path to DrugComb summary CSV
              Expected columns: drug_row, drug_col, cell_line_name,
                                synergy_zip (or synergy_bliss, synergy_hsa, synergy_loewe),
                                [ic50_row], [ic50_col]
delimiter : str  column delimiter (default: auto-detect)
"""
from __future__ import annotations

import csv
import logging
import os
from pathlib import Path
from collections import defaultdict
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)


class DrugCombSkill(RAGSkill):
    """DrugComb — drug combination screening data across cancer cell lines."""

    name = "DrugComb"
    subcategory = "drug_combination"
    resource_type = "Database"
    access_mode = AccessMode.LOCAL_FILE
    aim = "Drug combination screening"
    data_range = "Drug combination screening data across cancer cell lines"
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
        path = self.config.get("csv_path", "") or self._discover_default_path()
        if not path or not os.path.exists(path):
            logger.warning(
                "DrugCombSkill: file not found. "
                "Download from https://drugcomb.fimm.fi/ "
                "and set config['csv_path']."
            )
            return
        delim = self.config.get("delimiter", "\t" if path.endswith(".tsv") else ",")
        try:
            with open(path, newline="", encoding="utf-8", errors="ignore") as fh:
                for row in csv.DictReader(fh, delimiter=delim):
                    d1 = (row.get("drug_row", "") or row.get("Drug1", "") or
                           row.get("drug1", "")).strip()
                    d2 = (row.get("drug_col", "") or row.get("Drug2", "") or
                           row.get("drug2", "")).strip()
                    if d1 and d2:
                        idx = len(self._rows)
                        self._rows.append(row)
                        self._drug_index[d1.lower()].append(idx)
                        self._drug_index[d2.lower()].append(idx)
            logger.info("DrugComb: loaded %d combination records", len(self._rows))
        except Exception as exc:
            logger.error("DrugComb: load failed — %s", exc)
            return

        self._build_fuzzy_index(self._drug_index.keys())

    def _discover_default_path(self) -> str:
        repo_root = Path(__file__).resolve().parents[3]
        base = repo_root / "resources_metadata" / "drug_combination" / "DrugComb"
        candidates = [
            base / "drugcomb_data_v1.5.csv",
            base / "drugcomb.csv",
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
                d1 = (row.get("drug_row", "") or row.get("Drug1", "") or row.get("drug1", "")).strip()
                d2 = (row.get("drug_col", "") or row.get("Drug2", "") or row.get("drug2", "")).strip()
                cell = (row.get("cell_line_name", "") or row.get("cell_line", "") or
                        row.get("CellLine", "")).strip()
                # Use ZIP synergy score preferentially
                score = (row.get("synergy_zip", "") or row.get("synergy_bliss", "") or
                         row.get("synergy_hsa", "") or row.get("synergy_loewe", "") or
                         row.get("Score", "")).strip()
                score_type = "ZIP" if row.get("synergy_zip") else (
                    "Bliss" if row.get("synergy_bliss") else "synergy")
                results.append(RetrievalResult(
                    source_entity=d1,
                    source_type="drug",
                    target_entity=d2,
                    target_type="drug",
                    relationship="drug_combination_screening",
                    weight=1.0,
                    source="DrugComb",
                    skill_category="drug_combination",
                    evidence_text=(
                        f"DrugComb: {d1} + {d2}"
                        + (f" in {cell}" if cell else "")
                        + (f" ({score_type}={score})" if score else "")
                    ),
                    metadata={
                        "cell_line": cell,
                        "synergy_score": score,
                        "score_type": score_type,
                    },
                ))
        return results
