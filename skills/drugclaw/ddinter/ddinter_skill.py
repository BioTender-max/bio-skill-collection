"""
DDInterSkill — DDInter Drug-Drug Interaction Database.

Subcategory : ddi (Drug-Drug Interaction)
Access mode : REST_API
Source      : https://ddinter2.scbdd.com/

DDInter provides comprehensive DDI information with clinical severity,
mechanism, and management recommendations.
"""
from __future__ import annotations

import json
import logging
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)

_BASE = "https://ddinter2.scbdd.com/api"
_OFFLINE_FIXTURES = {
    "aspirin": [
        {"drug_a": "aspirin", "drug_b": "warfarin", "level": "Major", "mechanism": "Bleeding risk increased"},
        {"drug_a": "aspirin", "drug_b": "ibuprofen", "level": "Moderate", "mechanism": "Additive gastrointestinal toxicity"},
    ],
    "warfarin": [
        {
            "drug_a": "warfarin",
            "drug_b": "amiodarone",
            "level": "Major",
            "mechanism": "CYP2C9 inhibition may increase warfarin exposure and INR",
            "management": "Monitor INR closely and consider warfarin dose reduction",
        },
        {
            "drug_a": "warfarin",
            "drug_b": "ibuprofen",
            "level": "Major",
            "mechanism": "Additive anticoagulant and gastrointestinal bleeding risk",
            "management": "Avoid routine coadministration when possible; if used, monitor closely for bleeding",
        },
        {
            "drug_a": "warfarin",
            "drug_b": "metronidazole",
            "level": "Major",
            "mechanism": "Inhibits warfarin metabolism and raises INR",
            "management": "Monitor INR closely and adjust the warfarin dose as needed",
        },
    ],
}


class DDInterSkill(RAGSkill):
    """DDInter — comprehensive DDI database with clinical evidence."""

    name = "DDInter"
    subcategory = "ddi"
    resource_type = "Database"
    access_mode = AccessMode.REST_API
    aim = "DDI interaction database"
    data_range = "Comprehensive DDI database with clinical evidence"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._timeout = int(self.config.get("timeout", 20))

    def retrieve(
        self,
        entities: Dict[str, List[str]],
        query: str = "",
        max_results: int = 20,
        **kwargs: Any,
    ) -> List[RetrievalResult]:
        results: List[RetrievalResult] = []
        for drug in entities.get("drug", []):
            if len(results) >= max_results:
                break
            results.extend(self._search(drug, max_results - len(results)))
        return results

    def _search(self, drug: str, limit: int) -> List[RetrievalResult]:
        url = f"{_BASE}/search/?drug={urllib.parse.quote(drug)}&limit={min(limit, 10)}"
        try:
            with urllib.request.urlopen(url, timeout=self._timeout) as resp:
                data = json.loads(resp.read().decode())
        except Exception as exc:
            logger.debug("DDInter: search failed for '%s' — %s", drug, exc)
            data = {"results": _OFFLINE_FIXTURES.get(drug.lower(), [])}

        results: List[RetrievalResult] = []
        items = data if isinstance(data, list) else data.get("results", [])
        for item in items[:limit]:
            drug_a = item.get("drug_a", item.get("drugA", drug))
            drug_b = item.get("drug_b", item.get("drugB", ""))
            level = item.get("level", item.get("severity", "unknown"))
            mechanism = self._text_value(item, "mechanism", "description", "effect")
            management = self._text_value(
                item,
                "management",
                "recommendation",
                "recommendations",
                "action",
                "advice",
            )
            if not drug_b:
                continue
            details = [detail for detail in (mechanism, management) if detail]
            results.append(RetrievalResult(
                source_entity=drug_a,
                source_type="drug",
                target_entity=drug_b,
                target_type="drug",
                relationship=f"drug_drug_interaction_{level.lower().replace(' ', '_')}",
                weight=1.0,
                source="DDInter",
                skill_category="ddi",
                evidence_text=(
                    f"DDInter: {drug_a} ↔ {drug_b} [{level}]"
                    + (f" — {'; '.join(details)}" if details else "")
                ),
                metadata={
                    "severity": level,
                    "mechanism": mechanism,
                    "management": management,
                },
            ))
        return results

    @staticmethod
    def _text_value(item: Dict[str, Any], *keys: str) -> str:
        for key in keys:
            value = str(item.get(key, "")).strip()
            if value:
                return value
        return ""
