"""
FDAOrangeBookSkill — FDA Orange Book REST API.

Subcategory : drug_knowledgebase
Access mode : REST_API
Source      : https://www.accessdata.fda.gov/scripts/cder/ob/

The FDA Orange Book lists FDA-approved drugs with bioequivalence data,
patent information, and exclusivity periods.
"""
from __future__ import annotations

import json
import logging
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)

_BASE = "https://api.fda.gov/drug/drugsfda.json"


class FDAOrangeBookSkill(RAGSkill):
    """FDA Orange Book — approved drugs with bioequivalence and patent info."""

    name = "FDA Orange Book"
    subcategory = "drug_knowledgebase"
    resource_type = "Database"
    access_mode = AccessMode.REST_API
    aim = "Approved drug products"
    data_range = "FDA-approved drugs with bioequivalence and patent info"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._timeout = int(self.config.get("timeout", 20))
        self._api_key = self.config.get("api_key", "")

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
        params = {
            "search": f'openfda.brand_name:"{drug}"+openfda.generic_name:"{drug}"',
            "limit": min(limit, 10),
        }
        if self._api_key:
            params["api_key"] = self._api_key
        url = _BASE + "?" + urllib.parse.urlencode(params)
        try:
            with urllib.request.urlopen(url, timeout=self._timeout) as resp:
                data = json.loads(resp.read().decode())
        except Exception as exc:
            logger.debug("FDA Orange Book: search failed for '%s' — %s", drug, exc)
            return []

        results: List[RetrievalResult] = []
        for result in data.get("results", []):
            brand_name = result.get("openfda", {}).get("brand_name", [drug])[0]
            generic_name = result.get("openfda", {}).get("generic_name", [""])
            generic = generic_name[0] if generic_name else ""
            app_num = result.get("application_number", "")
            sponsor = result.get("sponsor_name", "")
            results.append(RetrievalResult(
                source_entity=brand_name,
                source_type="drug",
                target_entity=generic or brand_name,
                target_type="drug",
                relationship="brand_of",
                weight=1.0,
                source="FDA Orange Book",
                skill_category="drug_knowledgebase",
                evidence_text=(
                    f"FDA Orange Book: {brand_name} (NDA/ANDA: {app_num}, "
                    f"sponsor: {sponsor})"
                ),
                metadata={
                    "application_number": app_num,
                    "sponsor": sponsor,
                    "generic_name": generic,
                },
            ))
        return results
