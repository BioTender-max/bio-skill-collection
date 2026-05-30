"""
PharmKGSkill — Pharmaceutical Knowledge Graph.

Subcategory : drug_knowledgebase (Drug Knowledgebase)
Access mode : LOCAL_FILE
Source      : https://github.com/MindRank-Biotech/PharmKG

PharmKG is a multi-relational pharmaceutical KG covering drugs, genes,
diseases, and pathways, built for drug discovery research.

Config keys
-----------
train_tsv : str  path to PharmKG train.tsv
  (columns: head \t relation \t tail)
"""
from __future__ import annotations

import csv
import logging
import os
from pathlib import Path
from collections import defaultdict
from typing import Any, Dict, List, Optional, Set

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)


class PharmKGSkill(RAGSkill):
    """PharmKG pharmaceutical knowledge graph."""

    name = "PharmKG"
    subcategory = "drug_knowledgebase"
    resource_type = "KG"
    access_mode = AccessMode.LOCAL_FILE
    aim = "Pharmaceutical knowledge graph"
    data_range = "Multi-relational drug KG (drug-gene-disease-pathway)"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._triplets: List[tuple] = []  # (head, rel, tail)
        self._name_index: Dict[str, List[int]] = defaultdict(list)
        self._loaded = False

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        self._loaded = True
        tsv = self.config.get("train_tsv", "") or self._discover_default_path()
        if not tsv or not os.path.exists(tsv):
            logger.warning("PharmKGSkill: train.tsv not found — set config['train_tsv']")
            return
        try:
            with open(tsv, newline="", encoding="utf-8") as fh:
                reader = csv.reader(fh, delimiter="\t")
                for row in reader:
                    if len(row) < 3:
                        continue
                    head, rel, tail = row[0], row[1], row[2]
                    idx = len(self._triplets)
                    self._triplets.append((head, rel, tail))
                    self._name_index[head.lower()].append(idx)
                    self._name_index[tail.lower()].append(idx)
            logger.info("PharmKG: loaded %d triplets", len(self._triplets))
        except Exception as exc:
            logger.error("PharmKG: load failed — %s", exc)

    def _discover_default_path(self) -> str:
        repo_root = Path(__file__).resolve().parents[3]
        base = repo_root / "resources_metadata" / "drug_knowledgebase" / "PharmKG"
        candidates = [
            base / "train.tsv",
            base / "PharmKG" / "train.tsv",
            base / "PharmKG-8k" / "train.tsv",
            base / "PharmKG-master" / "train.tsv",
        ]
        for path in candidates:
            if path.exists():
                return str(path)
        return ""

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
        seen: Set[int] = set()
        results: List[RetrievalResult] = []

        for names in entities.values():
            for name in names:
                for idx in self._name_index.get(name.lower(), []):
                    if idx in seen or len(results) >= max_results:
                        break
                    seen.add(idx)
                    head, rel, tail = self._triplets[idx]
                    results.append(RetrievalResult(
                        source_entity=head,
                        source_type="entity",
                        target_entity=tail,
                        target_type="entity",
                        relationship=rel.lower().replace(" ", "_").replace("-", "_"),
                        weight=1.0,
                        source="PharmKG",
                        skill_category="drug_knowledgebase",
                        evidence_text=f"PharmKG: {head} — {rel} → {tail}",
                        metadata={
                            "head": head,
                            "relation": rel,
                            "tail": tail,
                        },
                    ))
        return results
