"""
TAC2017ADRSkill — TAC 2017 Adverse Drug Reactions Extraction Corpus.

Subcategory : drug_nlp
Access mode : DATASET
Source      : https://bionlp.nlm.nih.gov/tac2017adversereactions/
Note        : Requires registration with NIST/TAC. Contact the organizers
              to request access to the data.

TAC 2017 Track 2 provides structured adverse drug reaction information
extracted from FDA drug labels, with sentence-level annotations of ADR terms
and MedDRA normalisation.

Config keys
-----------
tsv_path   : str  path to pre-processed TSV/CSV (drug, ade, section, label_id)
             OR
json_path  : str  path to JSON-lines file with {drug, ade, section, pmid} dicts
delimiter  : str  column delimiter for TSV (default: tab)
max_rows   : int  max rows to load (default: unlimited)
"""
from __future__ import annotations

import csv
import json
import logging
import os
from typing import Any, Dict, List, Optional, Tuple

from ...base import DatasetRAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)


class TAC2017ADRSkill(DatasetRAGSkill):
    """TAC 2017 ADR — FDA drug label adverse reaction extraction corpus."""

    name = "TAC 2017 ADR"
    subcategory = "drug_nlp"
    resource_type = "Dataset"
    access_mode = AccessMode.DATASET
    aim = "TAC ADR extraction corpus"
    data_range = "TAC 2017 adverse drug reaction extraction from FDA drug labels"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self._data: List[Tuple[str, str, str]] = []

    def _load(self) -> List[Tuple[str, str, str]]:
        """Load dataset; return list of (drug, ade, label) triples."""
        pairs: List[Tuple[str, str, str]] = []
        max_rows = self.config.get("max_rows", 0)

        # Try TSV/CSV first
        tsv = self.config.get("tsv_path", "") or self.config.get("csv_path", "")
        if tsv and os.path.exists(tsv):
            delim = self.config.get("delimiter", "\t")
            try:
                with open(tsv, newline="", encoding="utf-8", errors="ignore") as fh:
                    for row in csv.DictReader(fh, delimiter=delim):
                        drug = (row.get("drug", "") or row.get("Drug", "") or
                                row.get("drug_name", "")).strip()
                        ade = (row.get("ade", "") or row.get("ADE", "") or
                               row.get("reaction", "") or row.get("adr", "")).strip()
                        section = (row.get("section", "") or row.get("Section", "")).strip()
                        if drug and ade:
                            pairs.append((drug, ade, section))
                        if max_rows and len(pairs) >= max_rows:
                            break
                logger.info("TAC2017ADR: loaded %d records from TSV", len(pairs))
                self._data = pairs
                return pairs
            except Exception as exc:
                logger.error("TAC2017ADR: TSV load failed — %s", exc)

        # Try JSON-lines
        json_path = self.config.get("json_path", "")
        if json_path and os.path.exists(json_path):
            try:
                with open(json_path, encoding="utf-8", errors="ignore") as fh:
                    for line in fh:
                        line = line.strip()
                        if not line:
                            continue
                        obj = json.loads(line)
                        drug = (obj.get("drug", "") or obj.get("drug_name", "")).strip()
                        ade = (obj.get("ade", "") or obj.get("reaction", "") or
                               obj.get("adr", "")).strip()
                        section = obj.get("section", "")
                        if drug and ade:
                            pairs.append((drug, ade, section))
                        if max_rows and len(pairs) >= max_rows:
                            break
                logger.info("TAC2017ADR: loaded %d records from JSON", len(pairs))
                self._data = pairs
                return pairs
            except Exception as exc:
                logger.error("TAC2017ADR: JSON load failed — %s", exc)

        if not tsv and not json_path:
            logger.warning(
                "TAC2017ADRSkill: no file configured. "
                "Request data access at https://bionlp.nlm.nih.gov/tac2017adversereactions/ "
                "then set config['tsv_path'] or config['json_path']."
            )
        self._data = pairs
        return pairs

    def is_available(self) -> bool:
        self._ensure_loaded()
        return bool(self._data)

    def retrieve(
        self,
        entities: Dict[str, List[str]],
        query: str = "",
        max_results: int = 30,
        **kwargs: Any,
    ) -> List[RetrievalResult]:
        self._ensure_loaded()
        results: List[RetrievalResult] = []

        drug_queries = {d.lower() for d in entities.get("drug", [])}
        ade_queries = {a.lower() for a in entities.get("disease", []) + entities.get("ade", [])}
        q_lower = query.lower()

        for drug, ade, section in self._data:
            if len(results) >= max_results:
                break
            dl, al = drug.lower(), ade.lower()
            if drug_queries and dl not in drug_queries:
                if not any(q in dl for q in drug_queries):
                    continue
            if ade_queries and al not in ade_queries:
                if not any(q in al for q in ade_queries):
                    continue
            if not drug_queries and not ade_queries and q_lower:
                if q_lower not in dl and q_lower not in al:
                    continue
            results.append(RetrievalResult(
                source_entity=drug,
                source_type="drug",
                target_entity=ade,
                target_type="adverse_event",
                relationship="has_adverse_reaction",
                weight=1.0,
                source="TAC 2017 ADR",
                skill_category="drug_nlp",
                evidence_text=f"TAC2017: {drug} → {ade}"
                              + (f" [{section}]" if section else ""),
                metadata={"section": section},
            ))
        return results

    def get_all_pairs(self) -> List[Dict[str, Any]]:
        self._ensure_loaded()
        return [
            {"drug": d, "ade": a, "section": s, "label": "ADE"}
            for d, a, s in self._data
        ]
