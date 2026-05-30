"""
MolecularTargetsSkill — CCDI Molecular Targets Platform (Pediatric Oncology).

Subcategory : dti (Drug-Target Interaction)
Access mode : REST_API (GraphQL)
Docs        : https://moleculartargets.ccdi.cancer.gov

NCI CCDI Molecular Targets Platform is an Open Targets instance focused
on preclinical pediatric oncology data.  Supports target, disease, drug
lookups, and free-text search via public GraphQL API.
"""
from __future__ import annotations

import json
import logging
import re
import urllib.request
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)

_BASE = "https://moleculartargets.ccdi.cancer.gov/api/v4/graphql"

_PAT_ENSEMBL = re.compile(r"^ENSG\d{11}$", re.I)
_PAT_DISEASE = re.compile(
    r"^(EFO_\d+|MONDO_\d+|Orphanet_\d+|HP_\d+|OTAR_\d+|DOID_\d+)$", re.I
)
_PAT_DRUG = re.compile(r"^CHEMBL\d+$", re.I)


class MolecularTargetsSkill(RAGSkill):
    """CCDI Molecular Targets Platform — pediatric oncology targets via GraphQL."""

    name = "Molecular Targets"
    subcategory = "dti"
    resource_type = "Database"
    access_mode = AccessMode.REST_API
    aim = "Pediatric oncology target-disease-drug associations"
    data_range = "NCI CCDI pediatric oncology targets, diseases, drugs"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._timeout = int(self.config.get("timeout", 30))

    def retrieve(
        self,
        entities: Dict[str, List[str]],
        query: str = "",
        max_results: int = 30,
        **kwargs: Any,
    ) -> List[RetrievalResult]:
        results: List[RetrievalResult] = []
        all_entities = []
        for etype, names in entities.items():
            for n in names:
                all_entities.append((etype, n))

        for etype, name in all_entities:
            if len(results) >= max_results:
                break
            results.extend(self._search(name, max_results - len(results)))
        return results

    def _detect_type(self, entity: str) -> str:
        e = entity.strip()
        if _PAT_ENSEMBL.match(e):
            return "target"
        if _PAT_DISEASE.match(e):
            return "disease"
        if _PAT_DRUG.match(e):
            return "drug"
        return "search"

    def _graphql(self, gql_query: str, variables: dict) -> Optional[dict]:
        payload = json.dumps({"query": gql_query, "variables": variables}).encode()
        req = urllib.request.Request(
            _BASE, data=payload,
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                body = json.loads(resp.read().decode())
            return body.get("data")
        except Exception as exc:
            logger.debug("MolecularTargets: API error — %s", exc)
            return None

    def _search(self, entity: str, limit: int) -> List[RetrievalResult]:
        etype = self._detect_type(entity)
        results: List[RetrievalResult] = []

        if etype == "search":
            q = 'query($q:String!,$p:Pagination){search(queryString:$q,page:$p){hits{id entity name description}}}'
            data = self._graphql(q, {"q": entity, "p": {"index": 0, "size": limit}})
            if data and data.get("search"):
                for hit in data["search"].get("hits", []):
                    results.append(RetrievalResult(
                        source_entity=entity,
                        source_type="query",
                        target_entity=hit.get("name", hit.get("id", "")),
                        target_type=hit.get("entity", "unknown"),
                        relationship="search_hit",
                        weight=1.0,
                        source="Molecular Targets",
                        skill_category="dti",
                        evidence_text=f"CCDI: {hit.get('name','')} — {(hit.get('description','') or '')[:100]}",
                        metadata={"id": hit.get("id"), "entity_type": hit.get("entity")},
                    ))
        elif etype == "target":
            q = 'query($id:String!){target(ensemblId:$id){id approvedSymbol approvedName biotype functionDescriptions}}'
            data = self._graphql(q, {"id": entity.strip()})
            if data and data.get("target"):
                t = data["target"]
                funcs = t.get("functionDescriptions") or []
                results.append(RetrievalResult(
                    source_entity=entity,
                    source_type="gene",
                    target_entity=t.get("approvedSymbol", entity),
                    target_type="protein",
                    relationship="target_info",
                    weight=1.0,
                    source="Molecular Targets",
                    skill_category="dti",
                    evidence_text=f"CCDI target: {t.get('approvedSymbol','')} ({t.get('approvedName','')}) — {funcs[0][:120] if funcs else ''}",
                    metadata={"biotype": t.get("biotype"), "ensembl_id": t.get("id")},
                ))
        elif etype == "drug":
            q = 'query($id:String!){drug(chemblId:$id){id name drugType maximumClinicalTrialPhase isApproved description}}'
            data = self._graphql(q, {"id": entity.strip()})
            if data and data.get("drug"):
                d = data["drug"]
                results.append(RetrievalResult(
                    source_entity=entity,
                    source_type="drug",
                    target_entity=d.get("name", entity),
                    target_type="drug_info",
                    relationship="drug_lookup",
                    weight=1.0,
                    source="Molecular Targets",
                    skill_category="dti",
                    evidence_text=f"CCDI drug: {d.get('name','')} type={d.get('drugType','')} phase={d.get('maximumClinicalTrialPhase','')}",
                    metadata={"chembl_id": d.get("id"), "approved": d.get("isApproved")},
                ))
        elif etype == "disease":
            q = 'query($id:String!){disease(efoId:$id){id name description therapeuticAreas{id name}}}'
            data = self._graphql(q, {"id": entity.strip()})
            if data and data.get("disease"):
                dis = data["disease"]
                results.append(RetrievalResult(
                    source_entity=entity,
                    source_type="disease",
                    target_entity=dis.get("name", entity),
                    target_type="disease_info",
                    relationship="disease_lookup",
                    weight=1.0,
                    source="Molecular Targets",
                    skill_category="dti",
                    evidence_text=f"CCDI disease: {dis.get('name','')} — {(dis.get('description','') or '')[:100]}",
                    metadata={"efo_id": dis.get("id")},
                ))
        return results[:limit]
