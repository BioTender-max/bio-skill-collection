"""
ATCSkill — WHO ATC/DDD Classification REST API.

Subcategory : drug_ontology
Access mode : REST_API
Source      : https://atcddd.fhi.no/atc_ddd_index/

The Anatomical Therapeutic Chemical (ATC) classification system and
Defined Daily Dose (DDD) measurement unit for drug utilization studies.
"""
from __future__ import annotations

import json
import logging
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)

_BASE = "https://atcddd.fhi.no/atc_ddd_index"


class ATCSkill(RAGSkill):
    """WHO ATC/DDD drug classification system."""

    name = "ATC/DDD"
    subcategory = "drug_ontology"
    resource_type = "Database"
    access_mode = AccessMode.REST_API
    aim = "WHO drug classification"
    data_range = "ATC classification + daily doses"
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
        # ATC website has no clean JSON API; use NLM RxNav ATC endpoint
        url = (
            f"https://rxnav.nlm.nih.gov/REST/rxcui.json"
            f"?name={urllib.parse.quote(drug)}&search=2"
        )
        try:
            with urllib.request.urlopen(url, timeout=self._timeout) as resp:
                data = json.loads(resp.read().decode())
            rxcui_list = data.get("idGroup", {}).get("rxnormId", [])
            if not rxcui_list:
                return []
            rxcui = rxcui_list[0]
        except Exception as exc:
            logger.debug("ATC: RxCUI lookup failed for '%s' — %s", drug, exc)
            return []

        # Get ATC codes via RxNorm
        atc_url = f"https://rxnav.nlm.nih.gov/REST/rxcui/{rxcui}/property.json?propName=ATC"
        try:
            with urllib.request.urlopen(atc_url, timeout=self._timeout) as resp:
                atc_data = json.loads(resp.read().decode())
        except Exception as exc:
            logger.debug("ATC: property lookup failed — %s", exc)
            return []

        results: List[RetrievalResult] = []
        prop_group = atc_data.get("propConceptGroup", {})
        for prop in (prop_group.get("propConcept") or []):
            atc_code = prop.get("propValue", "")
            if not atc_code:
                continue
            results.append(RetrievalResult(
                source_entity=drug,
                source_type="drug",
                target_entity=atc_code,
                target_type="atc_code",
                relationship="has_atc_classification",
                weight=1.0,
                source="ATC/DDD",
                skill_category="drug_ontology",
                evidence_text=f"ATC/DDD: {drug} → {atc_code}",
                metadata={"rxcui": rxcui},
            ))
        return results[:limit]
