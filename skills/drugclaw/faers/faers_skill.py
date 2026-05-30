"""
FAERSSkill — FDA Adverse Event Reporting System.

Subcategory : adr (Adverse Drug Reaction)
Access mode : API (openFDA REST API, no key required for basic use)

FAERS collects spontaneous reports of adverse events and medication errors.
This skill queries the openFDA drug/event endpoint in real time.

API docs: https://open.fda.gov/apis/drug/event/

Config keys
-----------
top_n      : int   number of top reactions to retrieve per drug (default 20)
timeout    : int   HTTP request timeout in seconds (default 15)
api_key    : str   optional openFDA API key for higher rate limits
"""
from __future__ import annotations

import json
import logging
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)

_BASE_URL = "https://api.fda.gov/drug/event.json"


class FAERSSkill(RAGSkill):
    """FAERS drug safety surveillance via openFDA API."""

    name = "FAERS"
    subcategory = "adr"
    resource_type = "API"
    access_mode = AccessMode.REST_API
    aim = "Post-market drug safety surveillance"
    data_range = "FDA spontaneous adverse event reports (all marketed drugs)"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._top_n: int = int(self.config.get("top_n", 20))
        self._timeout: int = int(self.config.get("timeout", 15))
        self._api_key: str = self.config.get("api_key", "")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_url(self, params: Dict[str, str]) -> str:
        """Construct a full openFDA URL, injecting api_key when configured."""
        if self._api_key:
            params["api_key"] = self._api_key
        return f"{_BASE_URL}?{urllib.parse.urlencode(params)}"

    def _get(self, url: str) -> Dict:
        """Execute a GET request and return the parsed JSON body."""
        logger.debug("FAERS GET %s", url)
        with urllib.request.urlopen(url, timeout=self._timeout) as resp:
            return json.loads(resp.read())

    def _count_reactions(self, drug_name: str) -> List[Dict[str, Any]]:
        """Return top-N MedDRA reaction terms and their report counts for a drug."""
        params = {
            "search": f'patient.drug.medicinalproduct:"{drug_name}"',
            "count": "patient.reaction.reactionmeddrapt.exact",
            "limit": str(self._top_n),
        }
        url = self._build_url(params)
        try:
            data = self._get(url)
            return data.get("results", [])
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                logger.info("FAERS: no records found for drug '%s'", drug_name)
            else:
                logger.warning("FAERS: HTTP %d for drug '%s'", exc.code, drug_name)
        except Exception as exc:
            logger.error("FAERS: request failed for '%s' — %s", drug_name, exc)
        return []

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def is_available(self) -> bool:
        return self._implemented

    def retrieve(
        self,
        entities: Dict[str, List[str]],
        query: str = "",
        max_results: int = 30,
        **kwargs: Any,
    ) -> List[RetrievalResult]:
        """
        Query the openFDA API for each drug in *entities['drug']* and return
        the top adverse reactions as RetrievalResult objects.

        Parameters
        ----------
        entities    : must contain key 'drug' with a list of drug name strings
        query       : unused (kept for interface compatibility)
        max_results : cap on the total number of results returned
        """
        results: List[RetrievalResult] = []

        for drug in entities.get("drug", []):
            if len(results) >= max_results:
                break

            for item in self._count_reactions(drug):
                if len(results) >= max_results:
                    break

                reaction: str = item.get("term", "").strip()
                count: int = int(item.get("count", 0))

                if not reaction:
                    continue

                # Normalise weight to [0, 1] using log-scale relative to top_n
                # (purely indicative; callers can re-rank on metadata.report_count)
                results.append(RetrievalResult(
                    source_entity=drug,
                    source_type="drug",
                    target_entity=reaction,
                    target_type="adverse_event",
                    relationship="causes_adverse_event",
                    weight=1.0,
                    source="FAERS",
                    skill_category="adr",
                    evidence_text=(
                        f"FAERS: {drug} associated with "
                        f"{reaction} ({count:,} spontaneous reports)"
                    ),
                    metadata={"report_count": count},
                ))

        return results

    def get_metadata(self) -> Dict[str, Any]:
        """Return dataset-level metadata: total record count and last-updated date."""
        try:
            url = self._build_url({"limit": "1"})
            data = self._get(url)
            meta = data.get("meta", {})
            res = meta.get("results", {})
            return {
                "total": res.get("total"),
                "last_updated": meta.get("last_updated"),
            }
        except Exception as exc:
            logger.error("FAERS: metadata fetch failed — %s", exc)
            return {}

    def get_all_pairs(self) -> List[Dict[str, Any]]:
        """
        Not supported for API access mode — the openFDA dataset is too large
        to enumerate in full. Use retrieve() with specific drug entities instead.
        """
        raise NotImplementedError(
            "FAERSSkill (API mode) does not support get_all_pairs(). "
            "Call retrieve(entities={'drug': [<name>, ...]}) instead."
        )