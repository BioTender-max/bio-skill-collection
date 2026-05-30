"""
TarKGSkill — Target Knowledge Graph (TarKG).

Subcategory : dti (Drug-Target Interaction)
Access mode : LOCAL_FILE
Source      : https://tarkg.ddtmlab.org/

TarKG is a drug-target KG linking drug targets to diseases through
biological pathways and functional annotations.
"""
from __future__ import annotations

import csv
import logging
import os
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)


class TarKGSkill(RAGSkill):
    """
    TarKG — drug-target knowledge graph with pathway context.

    Expects a TSV/CSV file with columns: drug, target, relation, [disease], [pathway]

    Config keys
    -----------
    tsv_path : str  path to TarKG triplet file
    """

    name = "TarKG"
    subcategory = "dti"
    resource_type = "KG"
    access_mode = AccessMode.LOCAL_FILE
    aim = "Target knowledge graph"
    data_range = "Drug-target KG linking targets to diseases via pathways"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._triplets: List[Dict] = []
        self._loaded = False

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        self._loaded = True
        path = self.config.get("tsv_path", "")
        if not path or not os.path.exists(path):
            logger.warning("TarKGSkill: file not found — set config['tsv_path']")
            return
        try:
            with open(path, newline="", encoding="utf-8") as fh:
                reader = csv.DictReader(fh, delimiter="\t")
                for row in reader:
                    self._triplets.append(dict(row))
            logger.info("TarKG: loaded %d triplets", len(self._triplets))
        except Exception as exc:
            logger.error("TarKG: load failed — %s", exc)

    def is_available(self) -> bool:
        self._ensure_loaded()
        return bool(self._triplets)

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
        genes_lower = {g.lower() for g in entities.get("gene", [])}

        for row in self._triplets:
            if len(results) >= max_results:
                break
            drug = row.get("drug", "") or row.get("source", "")
            target = row.get("target", "") or row.get("destination", "")
            rel = row.get("relation", "drug_target_interaction")
            if not drug or not target:
                continue
            if drug.lower() in drugs_lower or target.lower() in genes_lower:
                results.append(RetrievalResult(
                    source_entity=drug,
                    source_type="drug",
                    target_entity=target,
                    target_type="protein",
                    relationship=rel.lower().replace(" ", "_"),
                    weight=1.0,
                    source="TarKG",
                    skill_category="dti",
                    evidence_text=f"TarKG: {drug} --[{rel}]--> {target}",
                    metadata={k: v for k, v in row.items()
                               if k not in ("drug", "target", "relation", "source", "destination")},
                ))
        return results
