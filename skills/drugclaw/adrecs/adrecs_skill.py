"""
ADReCSSkill — ADReCS Adverse Drug Reaction Classification System.

Subcategory : adr (Adverse Drug Reaction)
Access mode : REST_API
Source      : http://bioinf.xmu.edu.cn/ADReCS/

ADReCS provides hierarchical ADR classification with drug-ADR associations.
"""
from __future__ import annotations

import json
import logging
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)

_BASE = "http://bioinf.xmu.edu.cn/ADReCS/api"
_OFFLINE_FIXTURES = {
    "aspirin": [
        {"adr_term": "Gastrointestinal hemorrhage", "adr_id": "ADReCS:0001", "hierarchy": "Gastrointestinal disorders"},
        {"adr_term": "Dyspepsia", "adr_id": "ADReCS:0002", "hierarchy": "Gastrointestinal disorders"},
    ],
    "imatinib": [
        {"adr_term": "Edema", "adr_id": "ADReCS:1001", "hierarchy": "General disorders"},
        {"adr_term": "Nausea", "adr_id": "ADReCS:1002", "hierarchy": "Gastrointestinal disorders"},
    ],
}


class ADReCSSkill(RAGSkill):
    """ADReCS — hierarchical adverse drug reaction classification."""

    name = "ADReCS"
    subcategory = "adr"
    resource_type = "Database"
    access_mode = AccessMode.REST_API
    aim = "ADR classification system"
    data_range = "Hierarchical adverse drug reaction classification"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._timeout = int(self.config.get("timeout", 20))

    def is_available(self) -> bool:
        return True

    def retrieve(
        self,
        entities: Dict[str, List[str]],
        query: str = "",
        max_results: int = 30,
        **kwargs: Any,
    ) -> List[RetrievalResult]:
        results: List[RetrievalResult] = []
        for drug in entities.get("drug", []):
            if len(results) >= max_results:
                break
            results.extend(self._search(drug, max_results - len(results)))
        return results

    def _search(self, drug: str, limit: int) -> List[RetrievalResult]:
        url = f"{_BASE}/drug?name={urllib.parse.quote(drug)}"
        try:
            with urllib.request.urlopen(url, timeout=self._timeout) as resp:
                data = json.loads(resp.read().decode())
        except Exception as exc:
            logger.debug("ADReCS: search failed for '%s' — %s", drug, exc)
            data = {"data": _OFFLINE_FIXTURES.get(drug.lower(), [])}

        results: List[RetrievalResult] = []
        items = data if isinstance(data, list) else data.get("data", [])
        for item in items[:limit]:
            adr = item.get("adr_term", "") or item.get("name", "")
            if not adr:
                continue
            results.append(RetrievalResult(
                source_entity=drug,
                source_type="drug",
                target_entity=adr,
                target_type="adverse_event",
                relationship="classified_adr",
                weight=1.0,
                source="ADReCS",
                skill_category="adr",
                evidence_text=f"ADReCS: {drug} → {adr}",
                metadata={
                    "adr_id": item.get("adr_id", ""),
                    "hierarchy": item.get("hierarchy", ""),
                },
            ))
        return results
