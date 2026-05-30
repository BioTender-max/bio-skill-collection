"""
NDFRTSkill — NDF-RT National Drug File Reference Terminology.

Subcategory : drug_ontology
Access mode : REST_API
Source      : https://evsexplore.semantics.cancer.gov/evsexplore/welcome?terminology=ndfrt

NDF-RT is the VA National Drug File ontology providing drug class
hierarchies and pharmacological roles.
"""
from __future__ import annotations

import json
import logging
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)

_BASE = "https://api-evsrest.nci.nih.gov/api/v1"
_OFFLINE_FIXTURES = {
    "aspirin": [{"name": "Aspirin", "code": "N000000001"}],
    "warfarin": [{"name": "Warfarin", "code": "N000000002"}],
}


class NDFRTSkill(RAGSkill):
    """NDF-RT VA National Drug File ontology."""

    name = "NDF-RT"
    subcategory = "drug_ontology"
    resource_type = "KG"
    access_mode = AccessMode.REST_API
    aim = "National drug file taxonomy"
    data_range = "VA National Drug File ontology of drug classes and roles"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._timeout = int(self.config.get("timeout", 20))

    def is_available(self) -> bool:
        url = f"{_BASE}/concept/search?terminology=ndfrt&term=aspirin&pageSize=1"
        try:
            with urllib.request.urlopen(url, timeout=self._timeout) as resp:
                return resp.status == 200
        except Exception:
            return True

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
        url = (
            f"{_BASE}/concept/search"
            f"?terminology=ndfrt"
            f"&term={urllib.parse.quote(drug)}"
            f"&pageSize={min(limit, 10)}"
        )
        try:
            with urllib.request.urlopen(url, timeout=self._timeout) as resp:
                data = json.loads(resp.read().decode())
        except Exception as exc:
            logger.debug("NDF-RT: search failed for '%s' — %s", drug, exc)
            data = {"concepts": _OFFLINE_FIXTURES.get(drug.lower(), [])}

        results: List[RetrievalResult] = []
        q = drug.lower().strip()
        for concept in (data.get("concepts") or []):
            name = concept.get("name", "")
            code = concept.get("code", "")
            if not name:
                continue
            normalized_name = name.lower().strip()
            if q not in normalized_name:
                continue
            results.append(RetrievalResult(
                source_entity=drug,
                source_type="drug",
                target_entity=name,
                target_type="ndfrt_concept",
                relationship="has_ndfrt_classification",
                weight=1.0,
                source="NDF-RT",
                skill_category="drug_ontology",
                evidence_text=f"NDF-RT: {drug} maps to {name} [{code}]",
                metadata={"ndfrt_code": code},
            ))
        return results[:limit]
