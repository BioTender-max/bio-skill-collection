"""
DrugCentralSkill — DrugCentral Drug Information Resource.

Subcategory : drug_knowledgebase (Drug Knowledgebase)
Access mode : REST_API
Docs        : https://drugcentral.org/api

DrugCentral provides FDA-approved drug information including indications,
pharmacology, targets, and drug-drug interactions.
"""
from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode
from . import example as drugcentral_example

logger = logging.getLogger(__name__)


class DrugCentralSkill(RAGSkill):
    """DrugCentral — FDA-approved drug information, indications, targets."""

    name = "DrugCentral"
    subcategory = "drug_knowledgebase"
    resource_type = "Database"
    access_mode = AccessMode.REST_API
    aim = "Drug information resource"
    data_range = "FDA-approved drug information, indications, targets"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._timeout = int(self.config.get("timeout", 20))
        self._structures_path = str(self.config.get("structures_path", "")).strip()
        self._targets_path = str(self.config.get("targets_path", "")).strip()
        self._approved_path = str(self.config.get("approved_path", "")).strip()

    def _has_local_data(self) -> bool:
        return bool(
            self._structures_path
            and os.path.exists(self._structures_path)
            and self._targets_path
            and os.path.exists(self._targets_path)
        )

    def is_available(self) -> bool:
        return self._has_local_data()

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
            results.extend(self._search_drug(drug, max_results - len(results)))
        return results

    def _search_drug(self, name: str, limit: int) -> List[RetrievalResult]:
        if not self._has_local_data():
            return []

        try:
            original_structures = drugcentral_example.STRUCTURES_FILE
            original_dti = drugcentral_example.DTI_FILE
            original_approved = drugcentral_example.APPROVED_FILE
            drugcentral_example.STRUCTURES_FILE = self._structures_path
            drugcentral_example.DTI_FILE = self._targets_path
            if self._approved_path:
                drugcentral_example.APPROVED_FILE = self._approved_path
            data = drugcentral_example.search(name)
        except Exception as exc:
            logger.debug("DrugCentral local: search failed for '%s' — %s", name, exc)
            return []
        finally:
            drugcentral_example.STRUCTURES_FILE = original_structures
            drugcentral_example.DTI_FILE = original_dti
            drugcentral_example.APPROVED_FILE = original_approved

        results: List[RetrievalResult] = []
        canonical = name
        structures = data.get("structures", []) if isinstance(data, dict) else []
        if structures:
            canonical = structures[0].get("INN", "") or canonical

        for tgt in data.get("targets", [])[:limit]:
            t_name = (
                tgt.get("GENE", "")
                or tgt.get("gene", "")
                or tgt.get("TARGET_NAME", "")
                or tgt.get("target_name", "")
            )
            act = (
                tgt.get("ACTION_TYPE", "")
                or tgt.get("action_type", "")
                or "targets"
            ).lower()
            if t_name:
                results.append(RetrievalResult(
                    source_entity=canonical,
                    source_type="drug",
                    target_entity=t_name,
                    target_type="protein",
                    relationship=act.replace(" ", "_"),
                    weight=1.0,
                    source="DrugCentral",
                    skill_category="drug_knowledgebase",
                    evidence_text=f"DrugCentral local: {canonical} {act} {t_name}",
                    metadata={
                        "act_type": tgt.get("ACT_TYPE", "") or tgt.get("act_type", ""),
                        "act_value": tgt.get("ACT_VALUE", "") or tgt.get("act_value", ""),
                    },
                ))
            if len(results) >= limit:
                break

        for approved in data.get("approved", []):
            if len(results) >= limit:
                break
            approved_name = approved.get("name", "").strip()
            indication_name = (
                str(approved.get("indication", "") or "").strip()
                or str(approved.get("indication_name", "") or "").strip()
                or str(approved.get("disease_name", "") or "").strip()
                or str(approved.get("approved_indication", "") or "").strip()
            )
            if indication_name:
                results.append(RetrievalResult(
                    source_entity=canonical,
                    source_type="drug",
                    target_entity=indication_name,
                    target_type="disease",
                    relationship="indicated_for",
                    weight=1.0,
                    source="DrugCentral",
                    skill_category="drug_knowledgebase",
                    evidence_text=f"DrugCentral local indication entry: {canonical} indicated for {indication_name}",
                    metadata={
                        "drugcentral_id": approved.get("id", ""),
                        "approved_name": approved_name,
                    },
                ))
            elif approved_name:
                results.append(RetrievalResult(
                    source_entity=canonical,
                    source_type="drug",
                    target_entity=approved_name,
                    target_type="approved_name",
                    relationship="has_approved_entry",
                    weight=1.0,
                    source="DrugCentral",
                    skill_category="drug_knowledgebase",
                    evidence_text=f"DrugCentral local approved entry: {approved_name}",
                    metadata={"drugcentral_id": approved.get("id", "")},
                ))

        return results[:limit]
