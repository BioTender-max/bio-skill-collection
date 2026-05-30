"""
TTDSkill — Therapeutic Target Database (TTD).

Subcategory : dti (Drug-Target Interaction)
Access mode : LOCAL_FILE (pre-downloaded flat files from ttd.idrblab.cn)

TTD provides target and drug information for approved/clinical/experimental
drugs linked to therapeutic targets.

Download: https://ttd.idrblab.cn/downloads/
Config keys:
  drug_target_tsv : path to TTD_drug_target.txt or P1-01-TTD_target_download.txt
"""
from __future__ import annotations

import logging
import os
from collections import defaultdict
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)


class TTDSkill(RAGSkill):
    """
    Therapeutic Target Database — approved/clinical/experimental drug-target links.

    Config keys
    -----------
    drug_target_tsv : str  path to TTD drug-target flat file
    """

    name = "TTD"
    subcategory = "dti"
    resource_type = "Database"
    access_mode = AccessMode.LOCAL_FILE
    aim = "Therapeutic target database"
    data_range = "Approved/clinical/experimental targets with drug linkages"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._drug_index: Dict[str, List[Dict]] = defaultdict(list)
        self._target_index: Dict[str, List[Dict]] = defaultdict(list)
        self._loaded = False

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        self._loaded = True
        path = self.config.get("drug_target_tsv", "")
        if not path or not os.path.exists(path):
            logger.warning("TTDSkill: file not found — set config['drug_target_tsv']")
            return
        try:
            with open(path, encoding="utf-8", errors="ignore") as fh:
                headers = None
                for line in fh:
                    line = line.rstrip("\n")
                    if not line or line.startswith("#"):
                        continue
                    parts = line.split("\t")
                    if headers is None:
                        headers = [h.lower().strip() for h in parts]
                        continue
                    row = dict(zip(headers, parts))
                    drug = row.get("drug name", "") or row.get("drugname", "")
                    target = row.get("target name", "") or row.get("targetname", "")
                    if drug and target:
                        entry = {
                            "drug": drug,
                            "target": target,
                            "status": row.get("highest status", ""),
                            "target_id": row.get("targetid", ""),
                            "drug_id": row.get("drugid", ""),
                        }
                        self._drug_index[drug.lower()].append(entry)
                        self._target_index[target.lower()].append(entry)
        except Exception as exc:
            logger.error("TTD: load failed — %s", exc)
            return

        self._build_fuzzy_index(self._drug_index.keys(), "_drug_fuzzy")
        self._build_fuzzy_index(self._target_index.keys(), "_target_fuzzy")

    def is_available(self) -> bool:
        self._ensure_loaded()
        return bool(self._drug_index or self._target_index)

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
            for entry in self._fuzzy_get(drug, self._drug_index, "_drug_fuzzy"):
                if len(results) >= max_results:
                    break
                results.append(self._to_result(entry))

        for gene in entities.get("gene", []):
            for entry in self._fuzzy_get(gene, self._target_index, "_target_fuzzy"):
                if len(results) >= max_results:
                    break
                results.append(self._to_result(entry))

        return results

    def _to_result(self, entry: Dict) -> RetrievalResult:
        status = entry.get("status", "")
        rel = "targets"
        if status:
            rel = f"targets_({status.lower().replace(' ', '_')})"
        return RetrievalResult(
            source_entity=entry["drug"],
            source_type="drug",
            target_entity=entry["target"],
            target_type="protein",
            relationship=rel,
            weight=1.0,
            source="TTD",
            skill_category="dti",
            evidence_text=f"TTD: {entry['drug']} → {entry['target']} [{status}]",
            metadata={
                "target_id": entry.get("target_id", ""),
                "drug_id": entry.get("drug_id", ""),
                "highest_status": status,
            },
        )
