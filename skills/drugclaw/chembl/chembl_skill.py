"""
ChEMBLSkill — Drug-Target Interaction via ChEMBL.

Subcategory : dti (Drug-Target Interaction)
Access mode : CLI-first (chembl_webresource_client), falls back to REST API.

Inspired by OpenClaw Medical Skills' approach of preferring installed
Python-package CLI tools over raw HTTP requests.

CLI install : pip install chembl_webresource_client
REST docs   : https://www.ebi.ac.uk/chembl/api/data/docs
"""
from __future__ import annotations

import json
import logging
import math
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, CLISkillMixin, AccessMode

logger = logging.getLogger(__name__)

_BASE = "https://www.ebi.ac.uk/chembl/api/data"


class ChEMBLSkill(CLISkillMixin, RAGSkill):
    """
    ChEMBL drug–target bioactivity database.

    Access strategy
    ---------------
    1. If ``chembl_webresource_client`` is installed → use its Python API
       (which wraps the same REST endpoints but handles pagination, retries,
       and data normalisation automatically — the OpenClaw CLI approach).
    2. Otherwise → fall back to direct REST calls.

    Config keys
    -----------
    timeout  : int  (default 20)
    """

    name = "ChEMBL"
    subcategory = "dti"
    resource_type = "Database"
    access_mode = AccessMode.CLI
    aim = "Bioactivity reasoning"
    data_range = "Drug–target IC50/Ki/EC50 across 14 000+ targets"
    _implemented = True
    cli_package_name = "chembl_webresource_client"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        RAGSkill.__init__(self, config)
        self._timeout = int(self.config.get("timeout", 20))

    # ------------------------------------------------------------------
    # RAGSkill.retrieve → dispatches to CLI or REST
    # ------------------------------------------------------------------

    def retrieve(
        self,
        entities: Dict[str, List[str]],
        query: str = "",
        max_results: int = 30,
        **kwargs: Any,
    ) -> List[RetrievalResult]:
        return self._try_cli_or_rest(entities, query, max_results)

    # ------------------------------------------------------------------
    # CLI path (chembl_webresource_client)
    # ------------------------------------------------------------------

    def _cli_search(
        self,
        entities: Dict[str, List[str]],
        query: str = "",
        max_results: int = 30,
    ) -> List[RetrievalResult]:
        """Use chembl_webresource_client Python API."""
        from chembl_webresource_client.new_client import new_client  # type: ignore

        molecule = new_client.molecule
        activity = new_client.activity

        drugs = entities.get("drug", [])
        results: List[RetrievalResult] = []

        for drug in drugs:
            if len(results) >= max_results:
                break
            try:
                # Search molecule by preferred name
                mols = molecule.filter(pref_name__iexact=drug).only(
                    ["molecule_chembl_id", "pref_name"]
                )[:1]
                if not mols:
                    mols = molecule.search(drug)[:1]
                if not mols:
                    continue
                mol = mols[0]
                chembl_id = mol.get("molecule_chembl_id", "")
                mol_name = mol.get("pref_name") or drug

                # Fetch activities
                raw_limit = min(max(max_results * 4, 40), 100)
                acts = activity.filter(
                    molecule_chembl_id=chembl_id
                ).only([
                    "target_pref_name", "standard_type",
                    "standard_value", "standard_units",
                    "target_chembl_id", "assay_chembl_id",
                ])[:raw_limit]

                for act in self._select_ranked_activities(
                    list(acts),
                    limit=max_results - len(results),
                ):
                    target_name = act.get("target_pref_name") or act.get(
                        "target_chembl_id", ""
                    )
                    if not target_name:
                        continue
                    activity_type = act.get("standard_type", "activity")
                    value = act.get("standard_value", "")
                    units = act.get("standard_units", "")
                    results.append(RetrievalResult(
                        source_entity=mol_name,
                        source_type="drug",
                        target_entity=target_name,
                        target_type="protein",
                        relationship=f"has_{activity_type.lower()}_activity",
                        weight=1.0,
                        source="ChEMBL",
                        skill_category="dti",
                        evidence_text=(
                            f"{mol_name} {activity_type}={value}{units} "
                            f"against {target_name}"
                        ),
                        metadata={
                            "chembl_id": chembl_id,
                            "activity_type": activity_type,
                            "value": value,
                            "units": units,
                            "target_chembl_id": act.get("target_chembl_id"),
                            "assay_chembl_id": act.get("assay_chembl_id"),
                            "access_via": "chembl_webresource_client",
                        },
                    ))
            except Exception as exc:
                logger.debug("ChEMBL CLI: error for '%s' — %s", drug, exc)

        return results

    # ------------------------------------------------------------------
    # REST fallback path
    # ------------------------------------------------------------------

    def _rest_search(
        self,
        entities: Dict[str, List[str]],
        query: str = "",
        max_results: int = 30,
    ) -> List[RetrievalResult]:
        drugs = entities.get("drug", [])
        results: List[RetrievalResult] = []

        for drug in drugs:
            if len(results) >= max_results:
                break
            chembl_id = self._rest_find_molecule(drug)
            if not chembl_id:
                continue
            acts = self._rest_get_activities(chembl_id, max_results - len(results))
            results.extend(acts)

        return results

    def _rest_find_molecule(self, name: str) -> Optional[str]:
        url = (
            f"{_BASE}/molecule/search.json"
            f"?q={urllib.parse.quote(name)}&limit=1"
        )
        try:
            with urllib.request.urlopen(url, timeout=self._timeout) as resp:
                data = json.loads(resp.read().decode())
            mols = data.get("molecules", [])
            return mols[0]["molecule_chembl_id"] if mols else None
        except Exception as exc:
            logger.debug("ChEMBL REST: molecule search failed for '%s' — %s", name, exc)
            return None

    def _rest_get_activities(
        self, chembl_id: str, limit: int
    ) -> List[RetrievalResult]:
        raw_limit = min(max(limit * 4, 40), 100)
        url = (
            f"{_BASE}/activity.json"
            f"?molecule_chembl_id={chembl_id}"
            f"&limit={raw_limit}"
            f"&format=json"
        )
        try:
            with urllib.request.urlopen(url, timeout=self._timeout) as resp:
                data = json.loads(resp.read().decode())
        except Exception as exc:
            logger.debug("ChEMBL REST: activity fetch failed for %s — %s", chembl_id, exc)
            return []

        results: List[RetrievalResult] = []
        for act in self._select_ranked_activities(data.get("activities", []), limit=limit):
            target_name = act.get("target_pref_name") or act.get(
                "target_chembl_id", ""
            )
            mol_name = act.get("molecule_pref_name") or chembl_id
            activity_type = act.get("standard_type", "activity")
            value = act.get("standard_value", "")
            units = act.get("standard_units", "")
            if not target_name:
                continue
            results.append(RetrievalResult(
                source_entity=mol_name,
                source_type="drug",
                target_entity=target_name,
                target_type="protein",
                relationship=f"has_{activity_type.lower()}_activity",
                weight=1.0,
                source="ChEMBL",
                skill_category="dti",
                evidence_text=(
                    f"{mol_name} {activity_type}={value}{units} against {target_name}"
                ),
                metadata={
                    "chembl_id": chembl_id,
                    "activity_type": activity_type,
                    "value": value,
                    "units": units,
                    "target_chembl_id": act.get("target_chembl_id"),
                    "assay_chembl_id": act.get("assay_chembl_id"),
                    "access_via": "REST",
                },
            ))
        return results

    @classmethod
    def _select_ranked_activities(
        cls,
        activities: List[Dict[str, Any]],
        *,
        limit: int,
    ) -> List[Dict[str, Any]]:
        if limit <= 0 or not activities:
            return []

        best_by_target: Dict[str, Dict[str, Any]] = {}
        for activity in activities:
            target_name = str(
                activity.get("target_pref_name") or activity.get("target_chembl_id") or ""
            ).strip()
            if not target_name:
                continue
            target_key = target_name.lower()
            existing = best_by_target.get(target_key)
            if existing is None or cls._activity_sort_key(activity) < cls._activity_sort_key(existing):
                best_by_target[target_key] = activity

        ranked = sorted(best_by_target.values(), key=cls._activity_sort_key)
        return ranked[:limit]

    @classmethod
    def _activity_sort_key(cls, activity: Dict[str, Any]) -> tuple[Any, ...]:
        activity_type = str(activity.get("standard_type") or "").strip().upper()
        target_name = str(
            activity.get("target_pref_name") or activity.get("target_chembl_id") or ""
        ).strip()
        target_priority = cls._target_name_priority(target_name)
        activity_priority = {
            "KI": 0,
            "KD": 0,
            "IC50": 1,
            "EC50": 2,
            "POTENCY": 3,
        }.get(activity_type, 9)
        value = cls._coerce_numeric(activity.get("standard_value"))
        potency_value = value if value is not None and value > 0 else math.inf
        return (
            activity_priority,
            target_priority,
            potency_value,
            target_name.lower(),
        )

    @staticmethod
    def _target_name_priority(target_name: str) -> int:
        lowered = str(target_name or "").strip().lower()
        if not lowered:
            return 9
        generic_family_names = {
            "platelet-derived growth factor receptor",
            "protein kinase c alpha type",
            "protein kinase c delta type",
            "camp-dependent protein kinase (pka)",
        }
        if lowered in generic_family_names:
            return 5
        return 0

    @staticmethod
    def _coerce_numeric(value: Any) -> float | None:
        try:
            if value is None or value == "":
                return None
            return float(value)
        except (TypeError, ValueError):
            return None
