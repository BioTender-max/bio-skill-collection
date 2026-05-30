"""
OpenFDASkill — FDA Drug Labels via openFDA REST API.

Subcategory : drug_labeling (Drug Labeling/Info)
Access mode : REST_API
Docs        : https://open.fda.gov/apis/drug/label/

Searches FDA drug labels for adverse reactions, indications, warnings,
and mechanism-of-action data.
"""
from __future__ import annotations

import json
import logging
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)

_BASE = "https://api.fda.gov/drug/label.json"
_FIELDS = [
    ("adverse_reactions", "has_adverse_reaction"),
    ("indications_and_usage", "indicated_for"),
    ("boxed_warning", "has_warning"),
    ("warnings", "has_warning"),
    ("warnings_and_precautions", "has_warning"),
    ("contraindications", "has_contraindication"),
    ("mechanism_of_action", "has_mechanism"),
    ("drug_interactions", "interacts_with"),
    ("use_in_specific_populations", "use_in_special_population"),
    ("dosage_and_administration", "has_dosing_guidance"),
]
_OFFLINE_FIXTURES = {
    "metformin": {
        "brand_name": "Metformin",
        "sections": [
            (
                "indications_and_usage",
                "indicated_for",
                "Used as an adjunct to diet and exercise to improve glycemic control in adults and pediatric patients with type 2 diabetes mellitus.",
            ),
            (
                "warnings",
                "has_warning",
                "Postmarketing cases of metformin-associated lactic acidosis have been reported; assess renal function and risk factors before use.",
            ),
            (
                "contraindications",
                "has_contraindication",
                "Metformin is contraindicated in patients with severe renal impairment and in acute or chronic metabolic acidosis.",
            ),
            (
                "adverse_reactions",
                "has_adverse_reaction",
                "Common adverse reactions include diarrhea, nausea, vomiting, flatulence, and abdominal discomfort.",
            ),
            (
                "use_in_specific_populations",
                "use_in_special_population",
                "Assess renal function more frequently in older adults and other patients at risk for lactic acidosis.",
            ),
            (
                "drug_interactions",
                "interacts_with",
                "Carbonic anhydrase inhibitors and other drugs that impair renal function may increase the risk of lactic acidosis; monitor patients closely.",
            ),
        ],
    }
}


def _normalize_string_list(value: Any) -> List[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value or "").strip()
    return [text] if text else []


def _is_combination_product(*, brand_name: str, generic_names: List[str]) -> bool:
    candidate_text = [brand_name] + list(generic_names)
    normalized_candidates = [text.lower() for text in candidate_text if text]
    if len(generic_names) > 1:
        return True
    return any(
        separator in text
        for text in normalized_candidates
        for separator in (" and ", "/", ";", ",")
    )


def _truncate_label_text(text: Any, limit: int = 500) -> str:
    normalized = str(text or "")
    if len(normalized) <= limit:
        return normalized

    clipped = normalized[:limit]
    if (
        limit < len(normalized)
        and clipped
        and not clipped[-1].isspace()
        and not normalized[limit].isspace()
    ):
        last_space = clipped.rfind(" ")
        if last_space > 0:
            clipped = clipped[:last_space]
    return clipped.rstrip()


class OpenFDASkill(RAGSkill):
    """openFDA Human Drug label search."""

    name = "openFDA Human Drug"
    subcategory = "drug_labeling"
    resource_type = "Database"
    access_mode = AccessMode.REST_API
    aim = "FDA drug label search"
    data_range = "Structured FDA drug labels (adverse events, dosing, warnings)"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._api_key = self.config.get("api_key", "")
        self._timeout = int(self.config.get("timeout", 15))

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
            results.extend(self._search_label(drug, max_results - len(results)))
        return results

    def _search_label(self, drug: str, limit: int) -> List[RetrievalResult]:
        params = {
            "search": f'openfda.brand_name:"{drug}"+openfda.generic_name:"{drug}"',
            "limit": min(limit, 5),
        }
        if self._api_key:
            params["api_key"] = self._api_key
        url = _BASE + "?" + urllib.parse.urlencode(params)

        try:
            with urllib.request.urlopen(url, timeout=self._timeout) as resp:
                data = json.loads(resp.read().decode())
        except Exception as exc:
            logger.debug("OpenFDA: label search failed for '%s' — %s", drug, exc)
            return self._offline_results(drug, limit)

        results: List[RetrievalResult] = []
        for label in data.get("results", [])[:limit]:
            openfda_payload = label.get("openfda", {}) or {}
            brand_names = _normalize_string_list(openfda_payload.get("brand_name", [drug]))
            brand_name = brand_names[0] if brand_names else drug
            generic_names = _normalize_string_list(openfda_payload.get("generic_name", []))
            product_types = _normalize_string_list(openfda_payload.get("product_type", []))
            identity_metadata = {
                "queried_drug": drug.strip().lower(),
                "brand_name": brand_name,
                "generic_names": generic_names,
                "is_combination_product": _is_combination_product(
                    brand_name=brand_name,
                    generic_names=generic_names,
                ),
                "openfda_product_type": product_types[0] if product_types else "",
            }
            for field, relationship in _FIELDS:
                text_list = label.get(field, [])
                if not text_list:
                    continue
                raw_text = text_list[0] if isinstance(text_list, list) else text_list
                text = _truncate_label_text(raw_text)
                results.append(RetrievalResult(
                    source_entity=brand_name,
                    source_type="drug",
                    target_entity=field.replace("_", " "),
                    target_type="label_section",
                    relationship=relationship,
                    weight=1.0,
                    source="openFDA Human Drug",
                    skill_category="drug_labeling",
                    evidence_text=text,
                    metadata={
                        "field": field,
                        **identity_metadata,
                    },
                ))
        return results or self._offline_results(drug, limit)

    def _offline_results(self, drug: str, limit: int) -> List[RetrievalResult]:
        fixture = _OFFLINE_FIXTURES.get(drug.strip().lower())
        if fixture is None:
            return []

        results: List[RetrievalResult] = []
        brand_name = fixture.get("brand_name", drug)
        for field, relationship, text in fixture.get("sections", [])[:limit]:
            results.append(RetrievalResult(
                source_entity=brand_name,
                source_type="drug",
                target_entity=field.replace("_", " "),
                target_type="label_section",
                relationship=relationship,
                weight=1.0,
                source="openFDA Human Drug",
                skill_category="drug_labeling",
                evidence_text=text,
                metadata={
                    "field": field,
                    "queried_drug": drug.strip().lower(),
                    "brand_name": brand_name,
                    "generic_names": [brand_name.lower()],
                    "is_combination_product": False,
                    "openfda_product_type": "",
                    "offline_fallback": True,
                },
            ))
        return results
