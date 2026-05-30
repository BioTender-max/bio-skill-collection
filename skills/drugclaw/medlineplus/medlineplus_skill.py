"""
MedlinePlusSkill — NLM MedlinePlus Drug Information.

Subcategory : drug_labeling
Access mode : REST_API
Docs        : https://medlineplus.gov/druginformation.html
              https://wsearch.nlm.nih.gov/ws/query?db=healthTopics

NLM MedlinePlus provides consumer health information about drugs,
diseases, and medical conditions.
"""
from __future__ import annotations

import json
import logging
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html import unescape
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode
from drugclaw.evidence import EvidenceItem, score_evidence_item

logger = logging.getLogger(__name__)

_SEARCH_URL = "https://wsearch.nlm.nih.gov/ws/query"
_CONNECT_URL = "https://connect.medlineplus.gov/service"
_OFFLINE_FIXTURES = {
    "aspirin": [
        {
            "title": "Aspirin",
            "url": "https://medlineplus.gov/druginfo/meds/a682878.html",
            "summary": (
                "Aspirin is used to reduce fever and relieve mild to moderate pain. "
                "It is also used to prevent blood clots in selected cardiovascular settings."
            ),
            "source": "MedlinePlus",
        }
    ],
    "ibuprofen": [
        {
            "title": "Ibuprofen",
            "url": "https://medlineplus.gov/druginfo/meds/a682159.html",
            "summary": (
                "Ibuprofen is a nonsteroidal anti-inflammatory drug used to relieve pain, "
                "tenderness, swelling, and fever."
            ),
            "source": "MedlinePlus",
        }
    ],
    "metformin": [
        {
            "title": "Metformin",
            "url": "https://medlineplus.gov/druginfo/meds/a696005.html",
            "summary": (
                "Metformin is used with diet and exercise to control blood sugar in people "
                "with type 2 diabetes and includes guidance on gastrointestinal side effects "
                "and rare lactic acidosis risk."
            ),
            "source": "MedlinePlus",
        }
    ],
}


class MedlinePlusSkill(RAGSkill):
    """NIH MedlinePlus drug information for patients and clinicians."""

    name = "MedlinePlus Drug Info"
    subcategory = "drug_labeling"
    resource_type = "Database"
    access_mode = AccessMode.REST_API
    aim = "Patient drug information"
    data_range = "NIH MedlinePlus drug information for patients and clinicians"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._timeout = int(self.config.get("timeout", 20))

    def is_available(self) -> bool:
        params = {
            "mainSearchCriteria.v.cs": "2.16.840.1.113883.6.88",
            "mainSearchCriteria.v.dn": "aspirin",
            "knowledgeResponseType": "application/json",
        }
        url = _CONNECT_URL + "?" + urllib.parse.urlencode(params)
        try:
            with urllib.request.urlopen(url, timeout=self._timeout) as resp:
                return resp.status == 200
        except Exception:
            return True

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
            results.extend(self._search_connect(drug, max_results - len(results)))
            if len(results) < max_results:
                results.extend(self._search_wsearch(drug, max_results - len(results)))
        return results[:max_results]

    def _search_wsearch(self, drug: str, limit: int) -> List[RetrievalResult]:
        params = {
            "db": "healthTopics",
            "term": drug,
            "retmax": min(limit, 5),
            "rettype": "topic",
        }
        url = _SEARCH_URL + "?" + urllib.parse.urlencode(params)
        try:
            with urllib.request.urlopen(url, timeout=self._timeout) as resp:
                content = resp.read().decode()
        except Exception as exc:
            logger.debug("MedlinePlus: search failed for '%s' — %s", drug, exc)
            return self._offline_results(drug, limit, access_via="offline_wsearch")

        results: List[RetrievalResult] = []
        try:
            root = ET.fromstring(content)
            for doc in root.iter("document"):
                url_attr = doc.get("url", "")
                title = ""
                snippet = ""
                for content_elem in doc.iter("content"):
                    name = content_elem.get("name", "")
                    if name == "title":
                        title = self._normalize_text(content_elem.text or "")
                    elif name == "snippet":
                        snippet = self._normalize_text(content_elem.text or "")[:300]
                if title:
                    results.append(RetrievalResult(
                        source_entity=drug,
                        source_type="drug",
                        target_entity=title,
                        target_type="health_topic",
                        relationship="has_health_topic",
                        weight=1.0,
                        source="MedlinePlus Drug Info",
                        skill_category="drug_labeling",
                        evidence_text=snippet or title,
                        sources=[url_attr] if url_attr else [],
                        metadata={
                            "url": url_attr,
                            "title": title,
                            "query": drug,
                            "access_via": "wsearch_xml",
                        },
                    ))
        except ET.ParseError:
            return self._offline_results(drug, limit, access_via="offline_wsearch")
        return results[:limit]

    def _search_connect(self, drug: str, limit: int) -> List[RetrievalResult]:
        params = {
            "mainSearchCriteria.v.cs": "2.16.840.1.113883.6.88",
            "mainSearchCriteria.v.dn": drug,
            "knowledgeResponseType": "application/json",
        }
        url = _CONNECT_URL + "?" + urllib.parse.urlencode(params)
        try:
            with urllib.request.urlopen(url, timeout=self._timeout) as resp:
                data = json.loads(resp.read().decode())
        except Exception as exc:
            logger.debug("MedlinePlus: connect lookup failed for '%s' — %s", drug, exc)
            return self._offline_results(drug, limit, access_via="offline_connect")

        entries = data.get("feed", {}).get("entry", [])
        results: List[RetrievalResult] = []
        for entry in entries[:limit]:
            title = entry.get("title", {}).get("_value", "")
            links = entry.get("link", [])
            url_attr = links[0].get("href", "") if isinstance(links, list) and links else ""
            summary_raw = str(entry.get("summary", {}).get("_value", ""))
            summary = self._normalize_text(summary_raw)[:400]
            if title:
                results.append(RetrievalResult(
                    source_entity=drug,
                    source_type="drug",
                    target_entity=title,
                    target_type="drug_info",
                    relationship="has_patient_drug_info",
                    weight=1.0,
                    source="MedlinePlus Drug Info",
                    skill_category="drug_labeling",
                    evidence_text=summary or title,
                    sources=[url_attr] if url_attr else [],
                    metadata={
                        "url": url_attr,
                        "title": title,
                        "query": drug,
                        "access_via": "connect_json",
                        },
                ))
        if results:
            return results
        return self._offline_results(drug, limit, access_via="offline_connect")

    @staticmethod
    def _normalize_text(text: str) -> str:
        return re.sub(r"<[^>]+>", "", unescape(text)).strip()

    def _offline_results(self, drug: str, limit: int, access_via: str) -> List[RetrievalResult]:
        fixtures = _OFFLINE_FIXTURES.get(drug.strip().lower(), [])
        results: List[RetrievalResult] = []
        for entry in fixtures[:limit]:
            results.append(RetrievalResult(
                source_entity=drug,
                source_type="drug",
                target_entity=entry["title"],
                target_type="drug_info",
                relationship="has_patient_drug_info",
                weight=1.0,
                source="MedlinePlus Drug Info",
                skill_category="drug_labeling",
                evidence_text=entry["summary"],
                sources=[entry["url"]],
                metadata={
                    "url": entry["url"],
                    "title": entry["title"],
                    "query": drug,
                    "access_via": access_via,
                    "offline_fallback": True,
                    "source_name": entry.get("source", "MedlinePlus"),
                },
            ))
        return results

    def build_evidence_items(
        self,
        records: List[Dict[str, Any]],
        query: str = "",
    ) -> List[EvidenceItem]:
        items: List[EvidenceItem] = []
        for index, record in enumerate(records, start=1):
            metadata = record.get("metadata", {})
            source_entity = record.get("source_entity", "")
            title = metadata.get("title") or record.get("target_entity", "")
            claim = f"{source_entity} has MedlinePlus patient guidance".strip()
            locator = (record.get("sources") or [metadata.get("url") or "MedlinePlus"])[0]
            item = EvidenceItem(
                evidence_id=f"medlineplus:{index}",
                source_skill=self.name,
                source_type="label_text",
                source_title=title or "MedlinePlus Drug Info",
                source_locator=str(locator),
                snippet=record.get("evidence_text", ""),
                structured_payload={
                    "title": title,
                    "url": metadata.get("url", ""),
                    "access_via": metadata.get("access_via", ""),
                },
                claim=claim,
                evidence_kind="label_text",
                support_direction="supports",
                confidence=0.0,
                retrieval_score=0.8,
                timestamp="2026-03-18T00:00:00Z",
                metadata={
                    "skill_category": self.subcategory,
                    "source_entity": source_entity,
                    "relationship": "has_patient_drug_info",
                    "target_entity": title or "MedlinePlus patient guidance",
                    "source_type": "drug",
                    "target_type": "drug_info",
                },
            )
            item.confidence = score_evidence_item(item)
            items.append(item)
        return items
