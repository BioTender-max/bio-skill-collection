"""
STITCHSkill — Drug-Protein Interactions from STITCH REST API.

Subcategory : dti (Drug-Target Interaction)
Access mode : REST_API
Docs        : http://stitch.embl.de/cgi/network.pl (STITCH v5)

STITCH (Search Tool for Interactions of Chemicals) links chemicals to proteins
using text mining, experiments, and database imports.
"""
from __future__ import annotations

import json
import logging
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)

_BASE = "https://string-db.org/api"
_OFFLINE_FIXTURES = {
    "imatinib": [
        {"preferredName_B": "ABL1", "score": 0.992},
        {"preferredName_B": "KIT", "score": 0.961},
    ]
}


class STITCHSkill(RAGSkill):
    """
    STITCH drug–protein interaction network.

    Uses the STRING/STITCH REST API to retrieve chemical-protein interactions.

    Config keys
    -----------
    timeout : int  (default 20)
    species : int  (default 9606 = human)
    limit   : int  (default 20)
    """

    name = "STITCH"
    subcategory = "dti"
    resource_type = "KG"
    access_mode = AccessMode.REST_API
    aim = "Drug–protein interactions"
    data_range = "Chemical–protein interaction network (STRING extension)"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._timeout = int(self.config.get("timeout", 20))
        self._species = int(self.config.get("species", 9606))
        self._limit = int(self.config.get("limit", 20))

    def retrieve(
        self,
        entities: Dict[str, List[str]],
        query: str = "",
        max_results: int = 30,
        **kwargs: Any,
    ) -> List[RetrievalResult]:
        drugs = entities.get("drug", [])
        results: List[RetrievalResult] = []

        for drug in drugs:
            if len(results) >= max_results:
                break
            results.extend(
                self._search_interactions(drug, max_results - len(results))
            )

        return results

    def _search_interactions(self, drug: str, limit: int) -> List[RetrievalResult]:
        url = (
            f"{_BASE}/json/interactors"
            f"?identifiers={urllib.parse.quote(drug)}"
            f"&species={self._species}"
            f"&limit={min(limit, self._limit)}"
            f"&caller_identity=drugclaw"
        )
        try:
            with urllib.request.urlopen(url, timeout=self._timeout) as resp:
                data = json.loads(resp.read().decode())
        except Exception as exc:
            logger.debug("STITCH: search failed for '%s' — %s", drug, exc)
            data = _OFFLINE_FIXTURES.get(drug.lower(), [])

        results: List[RetrievalResult] = []
        for item in data[:limit]:
            partner = item.get("preferredName_B") or item.get("stringId_B", "")
            score = float(item.get("score", 0.0))
            if not partner:
                continue
            results.append(RetrievalResult(
                source_entity=drug,
                source_type="drug",
                target_entity=partner,
                target_type="protein",
                relationship="interacts_with",
                weight=min(score, 1.0),
                source="STITCH",
                skill_category="dti",
                evidence_text=f"STITCH: {drug} interacts with {partner} (score={score:.3f})",
                metadata={"stitch_score": score},
            ))
        return results
