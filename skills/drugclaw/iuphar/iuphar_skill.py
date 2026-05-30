"""
IUPHARSkill — IUPHAR/BPS Guide to Pharmacology REST API.

Subcategory : drug_knowledgebase (Drug Knowledgebase)
Access mode : REST_API
Docs        : https://www.guidetopharmacology.org/webServices.jsp

Expert-curated pharmacological targets, ligands, and their interactions.
"""
from __future__ import annotations

import json
import logging
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)

_BASE = "https://www.guidetopharmacology.org/services"


class IUPHARSkill(RAGSkill):
    """IUPHAR/BPS Guide to Pharmacology — expert-curated pharmacology."""

    name = "IUPHAR/BPS Guide to Pharmacology"
    subcategory = "drug_knowledgebase"
    resource_type = "Database"
    access_mode = AccessMode.REST_API
    aim = "Pharmacology reference"
    data_range = "Expert-curated targets, drugs, and pharmacological data"
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
            results.extend(self._search_ligand(drug, max_results - len(results)))
        return results

    def _search_ligand(self, name: str, limit: int) -> List[RetrievalResult]:
        # Search for ligand by name
        url = f"{_BASE}/ligands?name={urllib.parse.quote(name)}&type=Approved"
        try:
            with urllib.request.urlopen(url, timeout=self._timeout) as resp:
                ligands = json.loads(resp.read().decode())
        except Exception as exc:
            logger.debug("IUPHAR: ligand search failed for '%s' — %s", name, exc)
            return []

        if not ligands:
            return []

        results: List[RetrievalResult] = []
        for lig in ligands[:3]:  # top 3 matches
            lig_id = lig.get("ligandId", "")
            lig_name = lig.get("name", name)
            if not lig_id:
                continue

            # Get interactions for this ligand
            int_url = f"{_BASE}/interactions?ligandId={lig_id}&type=primary_target"
            try:
                with urllib.request.urlopen(int_url, timeout=self._timeout) as resp:
                    interactions = json.loads(resp.read().decode())
            except Exception:
                continue

            for iact in interactions[:limit]:
                target_name = iact.get("targetGeneName") or iact.get("targetName", "")
                action = iact.get("type", "interacts").lower().replace(" ", "_")
                if not target_name:
                    continue
                results.append(RetrievalResult(
                    source_entity=lig_name,
                    source_type="drug",
                    target_entity=target_name,
                    target_type="protein",
                    relationship=action,
                    weight=1.0,
                    source="IUPHAR/BPS Guide to Pharmacology",
                    skill_category="drug_knowledgebase",
                    evidence_text=(
                        f"IUPHAR: {lig_name} {action} {target_name} "
                        f"(affinity: {iact.get('affinityMedian', 'N/A')})"
                    ),
                    metadata={
                        "ligand_id": lig_id,
                        "target_id": iact.get("targetId", ""),
                        "affinity": iact.get("affinityMedian", ""),
                        "units": iact.get("affinityUnits", ""),
                    },
                ))
                if len(results) >= limit:
                    break
        return results
