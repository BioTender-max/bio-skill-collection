"""
SIDERSkill — Side Effect Resource (SIDER).

Subcategory : adr (Adverse Drug Reaction)
Access mode : LOCAL_FILE
Download    : http://sideeffects.embl.de/

SIDER contains drug–side-effect associations extracted from FDA package inserts.
Uses STITCH IDs internally.

Config keys
-----------
se_tsv          : str   path to meddra_all_se.tsv
name_to_stitch  : dict  {drug_name_lower: stitch_id} mapping (optional)
"""
from __future__ import annotations

import csv
import logging
import os
from collections import defaultdict
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)


class SIDERSkill(RAGSkill):
    """SIDER drug–side-effect associations from package inserts."""

    name = "SIDER"
    subcategory = "adr"
    resource_type = "Database"
    access_mode = AccessMode.LOCAL_FILE
    aim = "Side effect resource"
    data_range = "Drug–side-effect associations from package inserts"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        # stitch_id -> list of side effects
        self._stitch_to_se: Dict[str, List[str]] = defaultdict(list)
        # drug_name_lower -> stitch_id
        self._name_map: Dict[str, str] = {}
        self._loaded = False

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        self._loaded = True
        tsv = self.config.get("se_tsv", "")
        if not tsv or not os.path.exists(tsv):
            logger.warning(
                "SIDERSkill: meddra_all_se.tsv not found. "
                "Set config['se_tsv'] = '<path>/meddra_all_se.tsv'."
            )
            return
        try:
            with open(tsv, newline="", encoding="utf-8") as fh:
                for row in csv.reader(fh, delimiter="\t"):
                    if len(row) < 5:
                        continue
                    stitch_flat, stitch_stereo, umls_cui, meddra_type, se_name = (
                        row[0], row[1], row[2], row[3], row[4]
                    )
                    if meddra_type.lower() == "pt":  # preferred term only
                        self._stitch_to_se[stitch_flat].append(se_name)
            logger.info("SIDER: loaded %d drug entries", len(self._stitch_to_se))
        except Exception as exc:
            logger.error("SIDER: load failed — %s", exc)

        # Custom name → stitch_id map from config
        for name, sid in (self.config.get("name_to_stitch") or {}).items():
            self._name_map[name.lower()] = sid

    def is_available(self) -> bool:
        self._ensure_loaded()
        return bool(self._stitch_to_se)

    def retrieve(
        self,
        entities: Dict[str, List[str]],
        query: str = "",
        max_results: int = 30,
        **kwargs: Any,
    ) -> List[RetrievalResult]:
        self._ensure_loaded()
        results: List[RetrievalResult] = []

        for drug in entities.get("drug", []):
            stitch_id = self._name_map.get(drug.lower(), "")
            if not stitch_id:
                continue
            for se in self._stitch_to_se.get(stitch_id, []):
                if len(results) >= max_results:
                    break
                results.append(RetrievalResult(
                    source_entity=drug,
                    source_type="drug",
                    target_entity=se,
                    target_type="side_effect",
                    relationship="has_side_effect",
                    weight=1.0,
                    source="SIDER",
                    skill_category="adr",
                    evidence_text=f"SIDER: {drug} has documented side effect: {se}",
                    metadata={"stitch_id": stitch_id},
                ))
        return results
