"""
nSIDESSkill — nSIDES Adverse Drug Effects via REST API.

Subcategory : adr (Adverse Drug Reaction)
Access mode : REST_API
Docs        : https://nsides.io/

nSIDES provides on-label and off-label adverse drug effects derived
from FDA FAERS using statistical disproportionality analysis.
"""
from __future__ import annotations

import json
import logging
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)

_BASE = "https://nsides.io/api/v1"


class nSIDESSkill(RAGSkill):
    """nSIDES — on/off-label adverse effects via disproportionality analysis."""

    name = "nSIDES"
    subcategory = "adr"
    resource_type = "Database"
    access_mode = AccessMode.REST_API
    aim = "Adverse drug effects (broad)"
    data_range = "Off-label and on-label adverse effects via NLP on EHRs"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._timeout = int(self.config.get("timeout", 20))

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
        url = f"{_BASE}/drug?drug={urllib.parse.quote(drug)}&limit={limit}"
        try:
            with urllib.request.urlopen(url, timeout=self._timeout) as resp:
                data = json.loads(resp.read().decode())
        except Exception as exc:
            logger.debug("nSIDES: search failed for '%s' — %s", drug, exc)
            return []

        results: List[RetrievalResult] = []
        for item in (data if isinstance(data, list) else data.get("results", [])):
            se = item.get("outcome_concept_name", "") or item.get("side_effect", "")
            prr = item.get("prr", "")
            if not se:
                continue
            results.append(RetrievalResult(
                source_entity=drug,
                source_type="drug",
                target_entity=se,
                target_type="adverse_event",
                relationship="associated_with_adverse_event",
                weight=1.0,
                source="nSIDES",
                skill_category="adr",
                evidence_text=f"nSIDES: {drug} → {se}" + (f" (PRR={prr})" if prr else ""),
                metadata={"prr": prr, "source": "nSIDES"},
            ))
        return results[:limit]
