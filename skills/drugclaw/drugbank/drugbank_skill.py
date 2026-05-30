"""
DrugBankSkill — DrugBank Comprehensive Drug Reference.

Subcategory : drug_knowledgebase (Drug Knowledgebase)
Access mode : REST_API (public endpoints, limited without API key)
Source      : https://go.drugbank.com/

DrugBank provides comprehensive drug information including structures,
pharmacology, targets, transporters, enzymes, and drug interactions.

Note: Full API access requires registration at drugbank.com.
      Public search is available without an API key.
"""
from __future__ import annotations

import json
import logging
import os
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode
from . import example as drugbank_example

logger = logging.getLogger(__name__)

_API_BASE = "https://api.drugbank.com/v1"
_PUBLIC_BASE = "https://www.drugbank.ca"


class DrugBankSkill(RAGSkill):
    """
    DrugBank comprehensive drug reference.

    Config keys
    -----------
    api_key : str   DrugBank API key (register at go.drugbank.com)
    timeout : int   (default 20)
    """

    name = "DrugBank"
    subcategory = "drug_knowledgebase"
    resource_type = "Database"
    access_mode = AccessMode.REST_API
    aim = "Comprehensive drug reference"
    data_range = "Drug structures, pharmacology, targets, interactions"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._api_key = self.config.get("api_key", "")
        self._timeout = int(self.config.get("timeout", 20))
        self._vocab_csv_path = str(self.config.get("vocab_csv_path", "")).strip()
        self._xml_path = str(self.config.get("xml_path", "")).strip()

    def _local_data_path(self) -> str:
        if self._xml_path and os.path.exists(self._xml_path):
            return self._xml_path
        if self._vocab_csv_path and os.path.exists(self._vocab_csv_path):
            return self._vocab_csv_path
        return ""

    def is_available(self) -> bool:
        return bool(self._api_key or self._local_data_path())

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

    def _search_drug(self, drug_name: str, limit: int) -> List[RetrievalResult]:
        if self._api_key:
            return self._api_search(drug_name, limit)
        local_path = self._local_data_path()
        if local_path:
            return self._local_search(drug_name, limit, local_path)
        return []

    def _api_search(self, drug_name: str, limit: int) -> List[RetrievalResult]:
        """Use DrugBank REST API (requires API key)."""
        url = (
            f"{_API_BASE}/drugs/search"
            f"?q={urllib.parse.quote(drug_name)}&fuzzy=true&per_page={limit}"
        )
        headers = {
            "Authorization": self._api_key,
            "Content-Type": "application/json",
        }
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                data = json.loads(resp.read().decode())
        except Exception as exc:
            logger.debug("DrugBank API: search failed for '%s' — %s", drug_name, exc)
            return []

        results: List[RetrievalResult] = []
        for drug in (data if isinstance(data, list) else data.get("drugs", [])):
            db_id = drug.get("drugbank_id", "")
            name = drug.get("name", drug_name)
            # Targets
            for tgt in drug.get("targets", []):
                tgt_name = tgt.get("name", "") or tgt.get("gene_name", "")
                action = tgt.get("actions", ["targets"])[0] if tgt.get("actions") else "targets"
                if tgt_name:
                    results.append(RetrievalResult(
                        source_entity=name,
                        source_type="drug",
                        target_entity=tgt_name,
                        target_type="protein",
                        relationship=action.lower().replace(" ", "_"),
                        weight=1.0,
                        source="DrugBank",
                        skill_category="drug_knowledgebase",
                        evidence_text=f"DrugBank: {name} {action} {tgt_name}",
                        metadata={"drugbank_id": db_id},
                    ))
            # Indications
            for ind in drug.get("indication", {}).get("indications", []):
                ind_name = ind.get("disease_name", "")
                if ind_name:
                    results.append(RetrievalResult(
                        source_entity=name,
                        source_type="drug",
                        target_entity=ind_name,
                        target_type="disease",
                        relationship="indicated_for",
                        weight=1.0,
                        source="DrugBank",
                        skill_category="drug_knowledgebase",
                        metadata={"drugbank_id": db_id},
                    ))
        return results[:limit]

    def _local_search(self, drug_name: str, limit: int, path: str) -> List[RetrievalResult]:
        """Use locally mirrored DrugBank data when available."""
        try:
            data = drugbank_example.load(path)
            hits = drugbank_example.search(data, drug_name)
        except Exception as exc:
            logger.debug("DrugBank local: search failed for '%s' — %s", drug_name, exc)
            return []

        results: List[RetrievalResult] = []
        for drug in hits[:limit]:
            name = drug.get("name", drug.get("Name", drug_name))
            db_id = drug.get("drugbank_id", drug.get("DrugBank ID", ""))
            desc = drug.get("description", "")

            for tgt in drug.get("targets", []):
                if len(results) >= limit:
                    break
                tgt_name = tgt.get("name", "")
                action = tgt.get("actions", ["targets"])[0] if tgt.get("actions") else "targets"
                if tgt_name:
                    results.append(RetrievalResult(
                        source_entity=name,
                        source_type="drug",
                        target_entity=tgt_name,
                        target_type="protein",
                        relationship=action.lower().replace(" ", "_"),
                        weight=1.0,
                        source="DrugBank",
                        skill_category="drug_knowledgebase",
                        evidence_text=f"DrugBank local: {name} {action} {tgt_name}",
                        metadata={"drugbank_id": db_id},
                    ))

            if len(results) >= limit:
                break

            if not results or all(r.metadata.get("drugbank_id") != db_id for r in results):
                results.append(RetrievalResult(
                    source_entity=name,
                    source_type="drug",
                    target_entity=drug.get("type", drug.get("drug-type", "drug")) or "drug",
                    target_type="drug_type",
                    relationship="classified_as",
                    weight=1.0,
                    source="DrugBank",
                    skill_category="drug_knowledgebase",
                    evidence_text=desc[:300] if desc else f"DrugBank local entry: {name}",
                    metadata={"drugbank_id": db_id},
                ))
        return results
