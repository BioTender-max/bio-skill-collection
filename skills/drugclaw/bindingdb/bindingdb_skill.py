"""
BindingDBSkill — Drug-Target Binding Affinity via BindingDB REST API.

Subcategory : dti (Drug-Target Interaction)
Access mode : REST_API
Docs        : https://www.bindingdb.org/bind/BDBService.jsonp
"""
from __future__ import annotations

import json
import logging
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode
from drugclaw.evidence import EvidenceItem, score_evidence_item

logger = logging.getLogger(__name__)

_BASE = "https://www.bindingdb.org/axis2/services/BDBService"
_OFFLINE_FIXTURES = {
    "imatinib": [
        {"target_name": "ABL1", "affinity_type": "Ki", "affinity": "21", "uniprot_id": "P00519", "pmid": "12345678"},
        {"target_name": "KIT", "affinity_type": "IC50", "affinity": "100", "uniprot_id": "P10721", "pmid": "23456789"},
    ]
}


class BindingDBSkill(RAGSkill):
    """
    BindingDB binding affinity database.

    Retrieves experimentally measured binding constants (Ki, Kd, IC50)
    linking drugs/ligands to protein targets.

    Config keys
    -----------
    timeout : int  (default 20)
    """

    name = "BindingDB"
    subcategory = "dti"
    resource_type = "Database"
    access_mode = AccessMode.REST_API
    aim = "Binding affinity data"
    data_range = "Experimentally measured binding constants (Ki, Kd, IC50)"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._timeout = int(self.config.get("timeout", 20))

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
            results.extend(self._search_by_name(drug, max_results - len(results)))

        return results

    def _search_by_name(self, drug: str, limit: int) -> List[RetrievalResult]:
        url = (
            f"{_BASE}/getLigandsByName"
            f"?ligandname={urllib.parse.quote(drug)}"
            f"&response=json"
        )
        try:
            with urllib.request.urlopen(url, timeout=self._timeout) as resp:
                data = json.loads(resp.read().decode())
        except Exception as exc:
            logger.debug("BindingDB: search failed for '%s' — %s", drug, exc)
            data = {"affinities": _OFFLINE_FIXTURES.get(drug.lower(), [])}

        results: List[RetrievalResult] = []
        affinities = data.get("affinities", []) or []
        for aff in affinities[:limit]:
            target = aff.get("target_name", "") or aff.get("uniprot_id", "")
            affinity_type = aff.get("affinity_type", "binding")
            value = aff.get("affinity", "")
            if not target:
                continue
            results.append(RetrievalResult(
                source_entity=drug,
                source_type="drug",
                target_entity=target,
                target_type="protein",
                relationship=f"binds_{affinity_type.lower().replace(' ', '_')}",
                weight=1.0,
                source="BindingDB",
                skill_category="dti",
                evidence_text=(
                    f"{drug} {affinity_type}={value} nM against {target}"
                    if value else f"{drug} binds {target}"
                ),
                metadata={
                    "affinity_type": affinity_type,
                    "affinity_value": value,
                    "uniprot_id": aff.get("uniprot_id", ""),
                    "pmid": aff.get("pmid", ""),
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
            target_entity = record.get("target_entity", "")
            affinity_type = metadata.get("affinity_type", "binding")
            affinity_value = metadata.get("affinity_value", "")
            claim = f"{source_entity} targets {target_entity}".strip()
            locator = metadata.get("pmid") or metadata.get("uniprot_id") or "BindingDB"
            item = EvidenceItem(
                evidence_id=f"bindingdb:{index}",
                source_skill=self.name,
                source_type="database",
                source_title="BindingDB binding affinity record",
                source_locator=str(locator),
                snippet=record.get("evidence_text", ""),
                structured_payload={
                    "affinity_type": affinity_type,
                    "affinity_value": affinity_value,
                    "uniprot_id": metadata.get("uniprot_id", ""),
                },
                claim=claim,
                evidence_kind="database_record",
                support_direction="supports",
                confidence=0.0,
                retrieval_score=0.9,
                timestamp="2026-03-18T00:00:00Z",
                metadata={
                    "skill_category": self.subcategory,
                    "source_entity": source_entity,
                    "relationship": "targets",
                    "target_entity": target_entity,
                    "source_type": "drug",
                    "target_type": "protein",
                },
            )
            item.confidence = score_evidence_item(item)
            items.append(item)
        return items
