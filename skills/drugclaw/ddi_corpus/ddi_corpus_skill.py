"""
DDICorpusSkill — DDI Corpus 2013.

Subcategory : drug_nlp
Access mode : DATASET (local XML or pre-parsed CSV/TSV)
Source      : https://github.com/isegura/DDICorpus
Paper       : Herrero-Zazo et al. (2013), J. Biomed. Inform.

The DDI Corpus 2013 contains annotated DDI information from drug labels and
MEDLINE abstracts. Used for DDI extraction NLP benchmarks.

Config keys
-----------
tsv_path : str  path to pre-parsed TSV (columns: drug1, drug2, ddi_type, sentence)
csv_path : str  alternative CSV path
delimiter : str  column delimiter (default: "\t" for TSV, "," for CSV)
"""
from __future__ import annotations

import csv
import logging
import os
from collections import defaultdict
from typing import Any, Dict, List, Optional

from ...base import DatasetRAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)


class DDICorpusSkill(DatasetRAGSkill):
    """DDI Corpus 2013 — annotated drug-drug interaction extraction corpus."""

    name = "DDI Corpus 2013"
    subcategory = "drug_nlp"
    resource_type = "Dataset"
    access_mode = AccessMode.DATASET
    aim = "DDI extraction corpus"
    data_range = "Annotated DDI extraction corpus from drug labels/MEDLINE"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._rows: List[Dict] = []
        self._drug_index: Dict[str, List[int]] = defaultdict(list)

    def _load(self) -> None:
        path = self.config.get("tsv_path", "") or self.config.get("csv_path", "")
        if not path or not os.path.exists(path):
            logger.warning(
                "DDICorpusSkill: file not found. "
                "Download from https://github.com/isegura/DDICorpus "
                "and set config['tsv_path'] (pre-parsed TSV with: "
                "drug1, drug2, ddi_type, sentence)."
            )
            return
        delim = self.config.get("delimiter", "\t" if path.endswith(".tsv") else ",")
        try:
            with open(path, newline="", encoding="utf-8", errors="ignore") as fh:
                for row in csv.DictReader(fh, delimiter=delim):
                    d1 = (row.get("drug1", "") or row.get("Drug1", "") or
                           row.get("e1", "")).strip()
                    d2 = (row.get("drug2", "") or row.get("Drug2", "") or
                           row.get("e2", "")).strip()
                    if d1 and d2:
                        idx = len(self._rows)
                        self._rows.append(row)
                        self._drug_index[d1.lower()].append(idx)
                        self._drug_index[d2.lower()].append(idx)
            logger.info("DDI Corpus 2013: loaded %d annotated pairs", len(self._rows))
        except Exception as exc:
            logger.error("DDI Corpus 2013: load failed — %s", exc)
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
        seen: set = set()
        for drug in entities.get("drug", []):
            for idx in self._fuzzy_get(drug, self._drug_index):
                if len(results) >= max_results or idx in seen:
                    continue
                seen.add(idx)
                row = self._rows[idx]
                d1 = (row.get("drug1", "") or row.get("Drug1", "") or
                       row.get("e1", "")).strip()
                d2 = (row.get("drug2", "") or row.get("Drug2", "") or
                       row.get("e2", "")).strip()
                ddi_type = (row.get("ddi_type", "") or row.get("DDI_type", "") or
                            row.get("type", "ddi")).strip()
                sentence = row.get("sentence", "")[:200]
                results.append(RetrievalResult(
                    source_entity=d1,
                    source_type="drug",
                    target_entity=d2,
                    target_type="drug",
                    relationship=f"ddi_{ddi_type.lower().replace(' ', '_')}",
                    weight=1.0,
                    source="DDI Corpus 2013",
                    skill_category="drug_nlp",
                    evidence_text=f"DDI Corpus: {d1} {ddi_type} {d2}" +
                                  (f" — {sentence}" if sentence else ""),
                    metadata={"ddi_type": ddi_type},
                ))
        return results

    def get_all_pairs(self) -> List[Dict[str, Any]]:
        self._ensure_loaded()
        return [
            {"drug": (r.get("drug1", "") or r.get("e1", "")).strip(),
             "disease": (r.get("drug2", "") or r.get("e2", "")).strip(),
             "label": r.get("ddi_type", "ddi")}
            for r in self._rows
        ]
