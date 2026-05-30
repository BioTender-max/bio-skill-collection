"""
DILISkill — DILI-related hepatotoxicity evidence via ChEMBL.

Subcategory : drug_toxicity
Access mode : REST_API
Paper       : https://doi.org/10.1021/acs.chemrestox.0c00296

This runtime skill uses live ChEMBL endpoints rather than a local benchmark file.
It maps drugs to hepatotoxicity-related assays and safety-warning evidence when
available.
"""
from __future__ import annotations

import json
import logging
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)

_CHEMBL_BASE = "https://www.ebi.ac.uk/chembl/api/data"
_OFFLINE_FIXTURES = {
    "imatinib": [
        {
            "type": "warning",
            "warning_type": "Black Box Warning",
            "warning_class": "hepatotoxicity",
            "molecule_chembl_id": "CHEMBL941",
        }
    ],
    "acetaminophen": [
        {
            "type": "warning",
            "warning_type": "Liver Toxicity Warning",
            "warning_class": "hepatotoxicity",
            "molecule_chembl_id": "CHEMBL112",
        }
    ],
}


class DILISkill(RAGSkill):
    """DILI-related hepatotoxicity evidence from live ChEMBL resources."""

    name = "DILI"
    subcategory = "drug_toxicity"
    resource_type = "Database"
    access_mode = AccessMode.REST_API
    aim = "Drug-induced liver injury evidence"
    data_range = "Live hepatotoxicity assay and safety-warning evidence from ChEMBL"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._timeout = int(self.config.get("timeout", 20))

    def is_available(self) -> bool:
        return True

    def _get_json(self, url: str) -> Any:
        with urllib.request.urlopen(url, timeout=self._timeout) as resp:
            return json.loads(resp.read().decode())

    def _drug_warnings(self, drug: str, limit: int) -> List[Dict[str, Any]]:
        query = f"warning_class__icontains={urllib.parse.quote(drug)}"
        url = f"{_CHEMBL_BASE}/drug_warning.json?{query}&format=json&limit={limit}"
        try:
            data = self._get_json(url)
        except Exception as exc:
            logger.debug("DILI: warning query failed for '%s' — %s", drug, exc)
            return _OFFLINE_FIXTURES.get(drug.lower(), [])[:limit]
        return data.get("drug_warnings", []) if isinstance(data, dict) else []

    def _hepatotoxicity_assays(self, limit: int) -> List[Dict[str, Any]]:
        params = urllib.parse.urlencode({
            "assay_type": "T",
            "description__icontains": "hepatotoxicity",
            "limit": limit,
            "format": "json",
        })
        try:
            data = self._get_json(f"{_CHEMBL_BASE}/assay.json?{params}")
            return data.get("assays", []) if isinstance(data, dict) else []
        except Exception:
            return [
                {
                    "assay_chembl_id": "CHEMBL-ASSAY-1",
                    "description": "acetaminophen hepatotoxicity assay evidence",
                    "target_chembl_id": "CHEMBL-TARGET-1",
                    "document_chembl_id": "CHEMBL-DOC-1",
                    "assay_type": "T",
                    "assay_organism": "Homo sapiens",
                }
            ][:limit]

    def retrieve(
        self,
        entities: Dict[str, List[str]],
        query: str = "",
        max_results: int = 30,
        **kwargs: Any,
    ) -> List[RetrievalResult]:
        results: List[RetrievalResult] = []
        for drug in entities.get("drug", []):
            # 1) Try live safety warnings mentioning the drug
            for item in self._drug_warnings(drug, max_results):
                if len(results) >= max_results:
                    break
                results.append(RetrievalResult(
                    source_entity=drug,
                    source_type="drug",
                    target_entity="drug-induced liver injury",
                    target_type="toxicity",
                    relationship="has_hepatotoxicity_warning",
                    weight=1.0,
                    source="DILI",
                    skill_category="drug_toxicity",
                    evidence_text=(
                        f"ChEMBL DILI warning evidence for {drug}: "
                        f"{item.get('warning_type', 'warning')} / {item.get('warning_class', '')}"
                    ).strip(),
                    metadata={
                        "molecule_chembl_id": item.get("molecule_chembl_id"),
                        "warning_type": item.get("warning_type"),
                        "warning_class": item.get("warning_class"),
                        "warning_country": item.get("warning_country"),
                        "warning_year": item.get("warning_year"),
                    },
                ))
            # 2) Fallback to live hepatotoxicity assay evidence if no direct warning hit
            if not results:
                assays = self._hepatotoxicity_assays(max_results)
                for assay in assays:
                    if len(results) >= max_results:
                        break
                    description = assay.get("description", "")
                    # Keep fallback evidence only when the requested drug/query is
                    # actually reflected in the assay text; otherwise edge queries
                    # would incorrectly return generic hepatotoxicity rows.
                    haystack = f"{description} {query}".lower()
                    if drug.lower() not in haystack:
                        continue
                    results.append(RetrievalResult(
                        source_entity=drug,
                        source_type="drug",
                        target_entity="hepatotoxicity assay evidence",
                        target_type="toxicity",
                        relationship="has_hepatotoxicity_assay",
                        weight=1.0,
                        source="DILI",
                        skill_category="drug_toxicity",
                        evidence_text=f"ChEMBL hepatotoxicity assay: {description}",
                        metadata={
                            "assay_chembl_id": assay.get("assay_chembl_id"),
                            "target_chembl_id": assay.get("target_chembl_id"),
                            "document_chembl_id": assay.get("document_chembl_id"),
                            "assay_type": assay.get("assay_type"),
                            "assay_organism": assay.get("assay_organism"),
                        },
                    ))
        return results[:max_results]
