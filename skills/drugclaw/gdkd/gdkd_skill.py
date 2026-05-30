"""
GDKDSkill — Genomics-Drug Knowledge Database (GDKD).

Subcategory : dti (Drug-Target Interaction)
Access mode : LOCAL_FILE (Synapse platform download)
Source      : https://www.synapse.org/#!Synapse:syn2370773

GDKD integrates genomics and drug data for target identification.
"""
from __future__ import annotations

import csv
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)


class GDKDSkill(RAGSkill):
    """GDKD — Genomics-Drug Knowledge Database (Synapse download)."""

    name = "GDKD"
    subcategory = "dti"
    resource_type = "Database"
    access_mode = AccessMode.LOCAL_FILE
    aim = "Genomics-drug knowledge"
    data_range = "Genomics-Drug Knowledge Database from Synapse"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._rows: List[Dict] = []
        self._loaded = False

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        self._loaded = True
        path = self.config.get("csv_path", "") or self._discover_default_path()
        if not path or not os.path.exists(path):
            logger.warning("GDKDSkill: file not found — set config['csv_path']")
            return
        try:
            with open(path, newline="", encoding="utf-8") as fh:
                self._rows = list(csv.DictReader(fh))
            logger.info("GDKD: loaded %d rows", len(self._rows))
        except Exception as exc:
            logger.error("GDKD: load failed — %s", exc)

    def _discover_default_path(self) -> str:
        repo_root = Path(__file__).resolve().parents[3]
        base = repo_root / "resources_metadata" / "dti" / "GDKD"
        candidates = [
            base / "gdkd.csv",
            base / "CCLE_drug_data.csv",
            base / "ccle_drug_data.csv",
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
        drugs_lower = {d.lower() for d in entities.get("drug", [])}

        for row in self._rows:
            if len(results) >= max_results:
                break
            drug = row.get("drug", "") or row.get("compound", "")
            target = row.get("gene", "") or row.get("target", "")
            if not drug or not target:
                continue
            if drug.lower() in drugs_lower:
                results.append(RetrievalResult(
                    source_entity=drug,
                    source_type="drug",
                    target_entity=target,
                    target_type="gene",
                    relationship="drug_gene_interaction",
                    weight=1.0,
                    source="GDKD",
                    skill_category="dti",
                    metadata={k: v for k, v in row.items() if k not in ("drug", "gene", "target", "compound")},
                ))
        return results
