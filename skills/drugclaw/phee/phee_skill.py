"""
PHEESkill — PHEE: A Dataset for Pharmacovigilance Event Extraction.

Subcategory : drug_nlp
Access mode : DATASET
Download    : https://github.com/ZhaoyueSun/PHEE
Paper       : Sun et al., "PHEE: A Dataset for Pharmacovigilance Event
              Extraction from Text" (EMNLP 2022)

PHEE provides sentence-level annotations for pharmacovigilance events,
covering Subject, Treatment (drug), and Effect (ADE/therapeutic outcome)
argument roles, extracted from biomedical literature.

Config keys
-----------
json_path  : str  path to PHEE JSON or JSON-lines file
             OR
tsv_path   : str  path to pre-processed TSV (drug, effect, event_type, sentence)
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


class PHEESkill(DatasetRAGSkill):
    """PHEE — pharmacovigilance event extraction dataset (EMNLP 2022)."""

    name = "PHEE"
    subcategory = "drug_nlp"
    resource_type = "Dataset"
    access_mode = AccessMode.DATASET
    aim = "Pharmacovigilance event corpus"
    data_range = "Pharmacovigilance event extraction corpus (EMNLP 2022)"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self._data: List[Tuple[str, str, str, str]] = []

    def _load(self) -> List[Tuple[str, str, str, str]]:
        """Load dataset; return list of (drug, effect, event_type, sentence) tuples."""
        records: List[Tuple[str, str, str, str]] = []
        max_rows = self.config.get("max_rows", 0)

        # Try JSON / JSON-lines
        json_path = self.config.get("json_path", "")
        if json_path and os.path.exists(json_path):
            try:
                with open(json_path, encoding="utf-8", errors="ignore") as fh:
                    content = fh.read().strip()
                    # Try full JSON array first
                    try:
                        data = json.loads(content)
                        items = data if isinstance(data, list) else [data]
                    except json.JSONDecodeError:
                        # Fall back to JSON-lines
                        items = [json.loads(l) for l in content.splitlines() if l.strip()]

                for obj in items:
                    drug = (obj.get("drug", "") or obj.get("treatment", "") or
                            obj.get("subject_drug", "")).strip()
                    effect = (obj.get("effect", "") or obj.get("ade", "") or
                              obj.get("adverse_effect", "") or
                              obj.get("therapeutic_outcome", "")).strip()
                    event_type = obj.get("event_type", "adverse_event").strip()
                    sentence = obj.get("sentence", obj.get("text", "")).strip()
                    if drug and effect:
                        records.append((drug, effect, event_type, sentence))
                    if max_rows and len(records) >= max_rows:
                        break
                logger.info("PHEE: loaded %d records from JSON", len(records))
                self._data = records
                return records
            except Exception as exc:
                logger.error("PHEE: JSON load failed — %s", exc)

        # Try TSV/CSV
        tsv = self.config.get("tsv_path", "") or self.config.get("csv_path", "")
        if tsv and os.path.exists(tsv):
            delim = self.config.get("delimiter", "\t")
            try:
                with open(tsv, newline="", encoding="utf-8", errors="ignore") as fh:
                    for row in csv.DictReader(fh, delimiter=delim):
                        drug = (row.get("drug", "") or row.get("treatment", "") or
                                row.get("Drug", "")).strip()
                        effect = (row.get("effect", "") or row.get("ade", "") or
                                  row.get("Effect", "")).strip()
                        event_type = (row.get("event_type", "") or
                                      row.get("EventType", "adverse_event")).strip()
                        sentence = row.get("sentence", row.get("text", "")).strip()
                        if drug and effect:
                            records.append((drug, effect, event_type, sentence))
                        if max_rows and len(records) >= max_rows:
                            break
                logger.info("PHEE: loaded %d records from TSV", len(records))
                self._data = records
                return records
            except Exception as exc:
                logger.error("PHEE: TSV load failed — %s", exc)

        if not json_path and not tsv:
            logger.warning(
                "PHEESkill: no file configured. "
                "Download from https://github.com/ZhaoyueSun/PHEE "
                "then set config['json_path'] or config['tsv_path']."
            )
        self._data = records
        return records

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

        for drug, effect, event_type, sentence in self._data:
            if len(results) >= max_results:
                break
            dl, el = drug.lower(), effect.lower()
            if drug_queries and dl not in drug_queries:
                if not any(q in dl for q in drug_queries):
                    continue
            if ade_queries and el not in ade_queries:
                if not any(q in el for q in ade_queries):
                    continue
            if not drug_queries and not ade_queries and q_lower:
                if q_lower not in dl and q_lower not in el:
                    continue
            results.append(RetrievalResult(
                source_entity=drug,
                source_type="drug",
                target_entity=effect,
                target_type="adverse_event",
                relationship=event_type.lower().replace(" ", "_"),
                weight=1.0,
                source="PHEE",
                skill_category="drug_nlp",
                evidence_text=f"PHEE: {drug} → {effect} [{event_type}]"
                              + (f" | {sentence[:120]}" if sentence else ""),
                metadata={"event_type": event_type, "sentence": sentence},
            ))
        return results

    def get_all_pairs(self) -> List[Dict[str, Any]]:
        self._ensure_loaded()
        return [
            {"drug": d, "effect": e, "event_type": et, "sentence": s}
            for d, e, et, s in self._data
        ]
