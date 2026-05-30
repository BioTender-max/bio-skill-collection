"""
RxNormSkill — NLM RxNorm Drug Normalization REST API.

Subcategory : drug_ontology (Drug Ontology/Terminology)
Access mode : REST_API
Docs        : https://lhncbc.nlm.nih.gov/RxNav/APIs/RxNormAPIs.html

RxNorm provides normalized drug names with RxCUI identifiers linking
to NDC codes, clinical concepts, and pharmacological classes.
"""
from __future__ import annotations

import json
import logging
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)

_BASE = "https://rxnav.nlm.nih.gov/REST"


class RxNormSkill(RAGSkill):
    """RxNorm — normalized drug names with RxCUI identifiers."""

    name = "RxNorm"
    subcategory = "drug_ontology"
    resource_type = "Database"
    access_mode = AccessMode.REST_API
    aim = "Drug name normalization"
    data_range = "NLM normalized drug names linking to NDC, RxCUI, and clinical concepts"
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
        # 1. Get RxCUI
        rxcui = self._get_rxcui(drug)
        if not rxcui:
            return []

        results: List[RetrievalResult] = []

        # 2. Get drug info
        info_url = f"{_BASE}/rxcui/{rxcui}/allProperties.json?prop=ALL"
        try:
            with urllib.request.urlopen(info_url, timeout=self._timeout) as resp:
                info = json.loads(resp.read().decode())
        except Exception:
            info = {}

        props = info.get("propConceptGroup", {}).get("propConcept", [])
        for prop in props[:limit]:
            p_name = prop.get("propName", "")
            p_value = prop.get("propValue", "")
            if not p_name or not p_value:
                continue
            results.append(RetrievalResult(
                source_entity=drug,
                source_type="drug",
                target_entity=p_value,
                target_type=p_name.lower().replace(" ", "_"),
                relationship=f"has_{p_name.lower().replace(' ', '_')}",
                weight=1.0,
                source="RxNorm",
                skill_category="drug_ontology",
                evidence_text=f"RxNorm: {drug} ({p_name}) = {p_value}",
                metadata={"rxcui": rxcui, "prop_name": p_name},
            ))

        # 3. Get drug class
        class_url = f"{_BASE}/rxcui/{rxcui}/related.json?rela=has_doseformgroup"
        try:
            with urllib.request.urlopen(class_url, timeout=self._timeout) as resp:
                class_data = json.loads(resp.read().decode())
        except Exception:
            class_data = {}

        for group in class_data.get("relatedGroup", {}).get("conceptGroup", []):
            for concept in group.get("conceptProperties", []):
                name = concept.get("name", "")
                if name and len(results) < limit:
                    results.append(RetrievalResult(
                        source_entity=drug,
                        source_type="drug",
                        target_entity=name,
                        target_type="dose_form",
                        relationship="has_dose_form",
                        weight=1.0,
                        source="RxNorm",
                        skill_category="drug_ontology",
                        metadata={"rxcui": rxcui},
                    ))

        return results[:limit]

    def _get_rxcui(self, name: str) -> Optional[str]:
        url = (
            f"{_BASE}/rxcui.json"
            f"?name={urllib.parse.quote(name)}&search=2"
        )
        try:
            with urllib.request.urlopen(url, timeout=self._timeout) as resp:
                data = json.loads(resp.read().decode())
            id_group = data.get("idGroup", {})
            rxcui_list = id_group.get("rxnormId", [])
            return rxcui_list[0] if rxcui_list else None
        except Exception as exc:
            logger.debug("RxNorm: RxCUI lookup failed for '%s' — %s", name, exc)
            return None
