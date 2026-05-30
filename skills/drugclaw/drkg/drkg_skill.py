"""
DRKGSkill — Drug Repurposing Knowledge Graph (DRKG).

Subcategory : drug_repurposing
Access mode : LOCAL_FILE
Source      : https://github.com/gnn4dr/DRKG

DRKG integrates information from six databases (DrugBank, Hetionet, GNBR,
STRING, IntAct, DGIdb) into a 97,238 entity × 5,874,261 triplet graph.

Config keys
-----------
drkg_tsv : str  absolute path to drkg.tsv
"""
from __future__ import annotations

import csv
import logging
import os
import re
from collections import defaultdict
from typing import Any, Dict, List, Optional, Set

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)


class DRKGSkill(RAGSkill):
    """DRKG — multi-relational biomedical drug repurposing KG."""

    name = "DRKG"
    subcategory = "drug_repurposing"
    resource_type = "KG"
    access_mode = AccessMode.LOCAL_FILE
    aim = "Drug repurposing KG"
    data_range = "Multi-relational KG integrating DrugBank, Hetionet, STRING, etc."
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._name_index: Dict[str, List[str]] = defaultdict(list)
        self._entity_info: Dict[str, tuple] = {}
        self._triplets: List[tuple] = []
        self._loaded = False

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        self._loaded = True
        tsv = self.config.get("drkg_tsv", "")
        if not tsv or not os.path.exists(tsv):
            logger.warning("DRKGSkill: drkg.tsv not found — set config['drkg_tsv']")
            return
        try:
            with open(tsv, newline="", encoding="utf-8") as fh:
                for line in fh:
                    parts = line.rstrip("\n").split("\t")
                    if len(parts) < 3:
                        continue
                    src, rel, tgt = parts[0], parts[1], parts[2]
                    self._triplets.append((src, rel, tgt))
                    self._register_entity(src)
                    self._register_entity(tgt)
            logger.info("DRKG: loaded %d triplets", len(self._triplets))
        except Exception as exc:
            logger.error("DRKG: load failed — %s", exc)

    def _register_entity(self, full: str) -> None:
        if full in self._entity_info:
            return
        parts = full.split("::", 1)
        etype, ename = (parts[0], parts[1]) if len(parts) == 2 else ("Unknown", full)
        self._entity_info[full] = (ename, _drkg_type(etype))
        self._name_index[ename.lower()].append(full)

    def is_available(self) -> bool:
        self._ensure_loaded()
        return bool(self._triplets)

    def retrieve(
        self,
        entities: Dict[str, List[str]],
        query: str = "",
        max_results: int = 50,
        **kwargs: Any,
    ) -> List[RetrievalResult]:
        self._ensure_loaded()
        candidate_full: Set[str] = set()
        for names in entities.values():
            for n in names:
                for full in self._name_index.get(n.lower(), []):
                    candidate_full.add(full)

        if not candidate_full:
            return []

        results: List[RetrievalResult] = []
        for src, rel, tgt in self._triplets:
            if len(results) >= max_results:
                break
            if src not in candidate_full and tgt not in candidate_full:
                continue
            src_name, src_type = self._entity_info.get(src, (src, "unknown"))
            tgt_name, tgt_type = self._entity_info.get(tgt, (tgt, "unknown"))
            results.append(RetrievalResult(
                source_entity=src_name,
                source_type=src_type,
                target_entity=tgt_name,
                target_type=tgt_type,
                relationship=_normalise_rel(rel),
                weight=1.0,
                source="DRKG",
                skill_category="drug_repurposing",
                evidence_text=f"DRKG: {src_name} --[{_normalise_rel(rel)}]--> {tgt_name}",
                metadata={"raw_relation": rel},
            ))
        return results


def _drkg_type(drkg_entity_type: str) -> str:
    return {
        "Compound": "drug", "Gene": "gene", "Disease": "disease",
        "Pathway": "pathway", "Anatomy": "anatomy",
        "Biological Process": "pathway", "Side Effect": "side_effect",
        "Pharmacologic Class": "drug_class", "Tax": "organism",
    }.get(drkg_entity_type, drkg_entity_type.lower())


def _normalise_rel(rel: str) -> str:
    parts = rel.split("::")
    label = parts[1] if len(parts) >= 2 else rel
    return re.sub(r"[^a-zA-Z0-9]", "_", label).lower().strip("_") or "related_to"
