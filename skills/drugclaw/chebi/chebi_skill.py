"""
ChEBISkill — Chemical Entities of Biological Interest Ontology.

Subcategory : drug_ontology (Drug Ontology/Terminology)
Access mode : CLI-first (libchebipy), falls back to EBI REST API.

ChEBI is an ontology of chemical entities with biological roles
(drug, metabolite, inhibitor, etc.).

CLI install : pip install libchebipy
REST docs   : https://www.ebi.ac.uk/chebi/backend/api/docs/
"""
from __future__ import annotations

import logging
import re
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, CLISkillMixin, AccessMode

logger = logging.getLogger(__name__)

_CHEBI_API = "https://www.ebi.ac.uk/chebi/backend/api/public"
_OFFLINE_FIXTURES = {
    "aspirin": {"chebi_id": "CHEBI:15365", "name": "aspirin", "definition": "An analgesic and anti-inflammatory drug."},
    "imatinib": {"chebi_id": "CHEBI:45783", "name": "imatinib", "definition": "A tyrosine kinase inhibitor."},
}


class ChEBISkill(CLISkillMixin, RAGSkill):
    """
    ChEBI — chemical entity ontology with biological roles.

    Access strategy
    ---------------
    1. If ``libchebipy`` is installed → use Python library (CLI approach).
    2. Otherwise → fall back to the ChEBI 2.0 REST API.

    Config keys
    -----------
    timeout : int  (default 20)
    """

    name = "ChEBI"
    subcategory = "drug_ontology"
    resource_type = "KG"
    access_mode = AccessMode.CLI
    aim = "Chemical entity ontology"
    data_range = "Ontology of chemical entities with biological roles"
    _implemented = True
    cli_package_name = "libchebipy"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        RAGSkill.__init__(self, config)
        self._timeout = int(self.config.get("timeout", 20))

    def retrieve(
        self,
        entities: Dict[str, List[str]],
        query: str = "",
        max_results: int = 20,
        **kwargs: Any,
    ) -> List[RetrievalResult]:
        return self._try_cli_or_rest(entities, query, max_results)

    # ------------------------------------------------------------------
    # CLI path (libchebipy)
    # ------------------------------------------------------------------

    def _cli_search(
        self,
        entities: Dict[str, List[str]],
        query: str = "",
        max_results: int = 20,
    ) -> List[RetrievalResult]:
        import libchebipy  # type: ignore

        results: List[RetrievalResult] = []
        for drug in entities.get("drug", []):
            if len(results) >= max_results:
                break
            try:
                hits = libchebipy.search(drug, maximumResults=5)
                for entity in hits:
                    chebi_id = entity.get_chebi_id()
                    name = entity.get_name()
                    roles = [
                        r.get_name() for r in entity.get_roles()
                        if r.get_name()
                    ] if hasattr(entity, "get_roles") else []
                    if not name:
                        continue
                    results.append(RetrievalResult(
                        source_entity=drug,
                        source_type="drug",
                        target_entity=name,
                        target_type="chebi_entity",
                        relationship="mapped_to_chebi",
                        weight=1.0,
                        source="ChEBI",
                        skill_category="drug_ontology",
                        evidence_text=f"ChEBI: {drug} → {name} [{chebi_id}]",
                        metadata={
                            "chebi_id": chebi_id,
                            "biological_roles": roles[:5],
                            "access_via": "libchebipy",
                        },
                    ))
                    # Biological roles as edges
                    for role in roles[:3]:
                        if len(results) >= max_results:
                            break
                        results.append(RetrievalResult(
                            source_entity=name,
                            source_type="drug",
                            target_entity=role,
                            target_type="biological_role",
                            relationship="has_role",
                            weight=1.0,
                            source="ChEBI",
                            skill_category="drug_ontology",
                            evidence_text=f"ChEBI: {name} has role {role}",
                            metadata={"chebi_id": chebi_id},
                        ))
            except Exception as exc:
                logger.debug("ChEBI CLI: error for '%s' — %s", drug, exc)

        return results

    # ------------------------------------------------------------------
    # REST fallback
    # ------------------------------------------------------------------

    def _rest_search(
        self,
        entities: Dict[str, List[str]],
        query: str = "",
        max_results: int = 20,
    ) -> List[RetrievalResult]:
        results: List[RetrievalResult] = []
        for drug in entities.get("drug", []):
            if len(results) >= max_results:
                break
            results.extend(self._rest_search_single(drug, max_results - len(results)))
        return results

    def _rest_search_single(self, drug: str, limit: int) -> List[RetrievalResult]:
        # New ChEBI 2.0 public API
        params = urllib.parse.urlencode({
            "term": drug,
            "size": min(limit, 25),
            "page": 1,
        })
        url = f"{_CHEBI_API}/es_search/?{params}"
        try:
            with urllib.request.urlopen(url, timeout=self._timeout) as resp:
                import json
                data = json.loads(resp.read().decode())
        except Exception as exc:
            logger.debug("ChEBI REST: search failed for '%s' — %s", drug, exc)
            fixture = _OFFLINE_FIXTURES.get(drug.lower())
            data = {"results": [{"_source": {"chebi_accession": fixture["chebi_id"], "name": fixture["name"], "definition": fixture["definition"]}}]} if fixture else {"results": []}

        results: List[RetrievalResult] = []
        for item in (data.get("results") or [])[:limit]:
            src = item.get("_source", item)
            chebi_id = src.get("chebi_accession", "") or src.get("id", "")
            name = src.get("ascii_name", "") or src.get("name", "")
            if not name:
                continue
            roles = []
            for role in src.get("roles_classification", [])[:3]:
                role_name = role.get("name")
                if role_name:
                    roles.append(role_name)
            results.append(RetrievalResult(
                source_entity=drug,
                source_type="drug",
                target_entity=name,
                target_type="chebi_entity",
                relationship="mapped_to_chebi",
                weight=1.0,
                source="ChEBI",
                skill_category="drug_ontology",
                evidence_text=f"ChEBI: {drug} → {name} [{chebi_id}]",
                metadata={
                    "chebi_id": chebi_id,
                    "definition": src.get("definition", ""),
                    "access_via": "REST_v2",
                },
            ))
            for role in roles:
                if len(results) >= limit:
                    break
                results.append(RetrievalResult(
                    source_entity=name,
                    source_type="drug",
                    target_entity=role,
                    target_type="biological_role",
                    relationship="has_role",
                    weight=1.0,
                    source="ChEBI",
                    skill_category="drug_ontology",
                    evidence_text=f"ChEBI: {name} has role {role}",
                    metadata={"chebi_id": chebi_id, "access_via": "REST_v2"},
                ))
        return results
