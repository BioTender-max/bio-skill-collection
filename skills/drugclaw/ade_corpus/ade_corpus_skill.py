"""
ADECorpusSkill — ADE Corpus (Adverse Drug Events).

Subcategory : drug_nlp
Access mode : DATASET (local CSV)
Source      : https://github.com/trunghlt/AdverseDrugReaction
              Original: Gurulingappa et al. (2012), J. Biomed. Inform.

The ADE Corpus contains annotated drug-ADE pairs from case reports,
widely used for ADE extraction NLP benchmarks.

Config keys
-----------
csv_path  : str  path to ADE-Corpus-V2/DRUG-AE.rel or equivalent CSV/TSV
              For DRUG-AE.rel, columns are pipe-separated: no | drug | ae | neg |...
              For CSV export: drug, adverse_event (or ae), sentence, [pmid]
delimiter : str  column delimiter (default: auto-detect; "|" for .rel files)
"""
from __future__ import annotations

import csv
import logging
import os
from collections import defaultdict
from typing import Any, Dict, List, Optional

from ...base import DatasetRAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)


class ADECorpusSkill(DatasetRAGSkill):
    """ADE Corpus — annotated adverse drug event corpus from case reports."""

    name = "ADE Corpus"
    subcategory = "drug_nlp"
    resource_type = "Dataset"
    access_mode = AccessMode.DATASET
    aim = "Adverse drug event corpus"
    data_range = "Annotated adverse drug event corpus from case reports"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._rows: List[Dict] = []
        self._drug_index: Dict[str, List[int]] = defaultdict(list)

    def _load(self) -> None:
        path = self.config.get("csv_path", "") or self.config.get("rel_path", "")
        if not path or not os.path.exists(path):
            logger.warning(
                "ADECorpusSkill: file not found. "
                "Download from https://github.com/trunghlt/AdverseDrugReaction "
                "and set config['csv_path'] (CSV) or config['rel_path'] (DRUG-AE.rel)."
            )
            return
        # Detect format from extension
        is_rel = path.endswith(".rel") or self.config.get("format") == "rel"
        delim = self.config.get("delimiter", "|" if is_rel else ",")
        try:
            with open(path, newline="", encoding="utf-8", errors="ignore") as fh:
                if is_rel:
                    # DRUG-AE.rel: doc_id|drug|ae|neg|drug_offset|ae_offset
                    for line in fh:
                        parts = line.strip().split("|")
                        if len(parts) >= 3:
                            drug = parts[1].strip()
                            ae = parts[2].strip()
                            neg = parts[3].strip() if len(parts) > 3 else "0"
                            if drug and ae and neg == "0":
                                row = {"drug": drug, "adverse_event": ae,
                                       "pmid": parts[0].split(".")[0]}
                                idx = len(self._rows)
                                self._rows.append(row)
                                self._drug_index[drug.lower()].append(idx)
                else:
                    for row in csv.DictReader(fh, delimiter=delim):
                        drug = (row.get("drug", "") or row.get("Drug", "")).strip()
                        if drug:
                            idx = len(self._rows)
                            self._rows.append(row)
                            self._drug_index[drug.lower()].append(idx)
            logger.info("ADE Corpus: loaded %d drug-ADE pairs", len(self._rows))
        except Exception as exc:
            logger.error("ADE Corpus: load failed — %s", exc)
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
                sentence = row.get("sentence", "")[:200]
                pmid = row.get("pmid", "")
                results.append(RetrievalResult(
                    source_entity=drug_name,
                    source_type="drug",
                    target_entity=ae or "adverse_event",
                    target_type="adverse_event",
                    relationship="causes_adverse_event",
                    weight=1.0,
                    source="ADE Corpus",
                    skill_category="drug_nlp",
                    evidence_text=f"ADE Corpus: {drug_name} causes {ae}" +
                                  (f" — {sentence}" if sentence else ""),
                    sources=[f"PMID:{pmid}"] if pmid else [],
                    metadata={"pmid": pmid},
                ))
        return results

    def get_all_pairs(self) -> List[Dict[str, Any]]:
        self._ensure_loaded()
        return [
            {"drug": (r.get("drug", "") or r.get("Drug", "")).strip(),
             "disease": (r.get("adverse_event", "") or r.get("ae", "")).strip(),
             "label": "positive_ade"}
            for r in self._rows
        ]
