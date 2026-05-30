"""
LiverToxSkill — LiverTox DILI Information via NCBI API.

Subcategory : drug_toxicity
Access mode : REST_API
Source      : https://www.ncbi.nlm.nih.gov/books/NBK547852/

LiverTox provides clinical descriptions of drug-induced liver injury
for over 1000 prescription and non-prescription drugs.
"""
from __future__ import annotations

import json
import logging
import os
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)

_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
_EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
_EINFO = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"


class LiverToxSkill(RAGSkill):
    """LiverTox — NCBI clinical descriptions of drug-induced liver injury."""

    name = "LiverTox"
    subcategory = "drug_toxicity"
    resource_type = "Database"
    access_mode = AccessMode.REST_API
    aim = "Drug-induced liver injury"
    data_range = "NCBI LiverTox clinical descriptions of DILI by drug"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._timeout = int(self.config.get("timeout", 20))
        self._fixture_index: Dict[str, List[Dict[str, str]]] = {}
        self._fixture_loaded = False

    def _ensure_fixture_loaded(self) -> None:
        if self._fixture_loaded:
            return
        self._fixture_loaded = True
        path = self.config.get("fixture_path", "")
        if not path or not os.path.exists(path):
            return
        try:
            with open(path, encoding="utf-8") as fh:
                rows = json.load(fh)
            for row in rows:
                drug = str(row.get("drug", "")).strip().lower()
                if drug:
                    self._fixture_index.setdefault(drug, []).append({
                        "title": str(row.get("title", "")).strip(),
                        "ncbi_book_id": str(row.get("ncbi_book_id", "")).strip(),
                    })
        except Exception as exc:
            logger.debug("LiverTox: fixture load failed — %s", exc)

    def is_available(self) -> bool:
        self._ensure_fixture_loaded()
        return bool(self._fixture_index)

    def retrieve(
        self,
        entities: Dict[str, List[str]],
        query: str = "",
        max_results: int = 10,
        **kwargs: Any,
    ) -> List[RetrievalResult]:
        results: List[RetrievalResult] = []
        for drug in entities.get("drug", []):
            if len(results) >= max_results:
                break
            results.extend(self._search(drug, max_results - len(results)))
        return results

    def _search(self, drug: str, limit: int) -> List[RetrievalResult]:
        self._ensure_fixture_loaded()
        fixture_rows = self._fixture_index.get(drug.lower(), [])
        if fixture_rows:
            results: List[RetrievalResult] = []
            for row in fixture_rows[:limit]:
                book_id = row.get("ncbi_book_id", "")
                title = row.get("title", drug)
                results.append(RetrievalResult(
                    source_entity=drug,
                    source_type="drug",
                    target_entity="drug-induced liver injury",
                    target_type="toxicity",
                    relationship="may_cause_dili",
                    weight=1.0,
                    source="LiverTox",
                    skill_category="drug_toxicity",
                    evidence_text=f"LiverTox: {title}",
                    sources=[f"https://www.ncbi.nlm.nih.gov/books/{book_id}/"] if book_id else [],
                    metadata={"ncbi_book_id": book_id, "title": title},
                ))
            return results

        # Search NCBI books for LiverTox entries
        params = {
            "db": "books",
            "term": f'"{drug}"[Title] AND livertox[Book]',
            "retmax": min(limit, 5),
            "retmode": "json",
        }
        url = _ESEARCH + "?" + urllib.parse.urlencode(params)
        try:
            with urllib.request.urlopen(url, timeout=self._timeout) as resp:
                data = json.loads(resp.read().decode())
        except Exception as exc:
            logger.debug("LiverTox: search failed for '%s' — %s", drug, exc)
            return []

        ids = data.get("esearchresult", {}).get("idlist", [])
        if not ids:
            return []

        results: List[RetrievalResult] = []
        # Get summaries
        sum_url = (
            f"{_EINFO}?db=books&id={','.join(ids[:limit])}&retmode=json"
        )
        try:
            with urllib.request.urlopen(sum_url, timeout=self._timeout) as resp:
                sum_data = json.loads(resp.read().decode())
        except Exception:
            return []

        for book_id, summary in sum_data.get("result", {}).items():
            if book_id == "uids":
                continue
            title = summary.get("title", drug)
            results.append(RetrievalResult(
                source_entity=drug,
                source_type="drug",
                target_entity="drug-induced liver injury",
                target_type="toxicity",
                relationship="may_cause_dili",
                weight=1.0,
                source="LiverTox",
                skill_category="drug_toxicity",
                evidence_text=f"LiverTox: {title}",
                sources=[f"https://www.ncbi.nlm.nih.gov/books/{book_id}/"],
                metadata={"ncbi_book_id": book_id, "title": title},
            ))
        return results
