"""
OpenTargetsSkill — Open Targets Platform via GraphQL API.

Subcategory : dti (Drug-Target Interaction)
Access mode : REST_API (GraphQL)
Docs        : https://platform.opentargets.org/

Open Targets Platform provides evidence linking drugs to targets to diseases,
integrating genetic, genomic, and chemical data.
"""
from __future__ import annotations

import json
import logging
import re
import urllib.request
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode
from drugclaw.evidence import EvidenceItem, score_evidence_item

logger = logging.getLogger(__name__)

_GRAPHQL = "https://api.platform.opentargets.org/api/v4/graphql"


class OpenTargetsSkill(RAGSkill):
    """
    Open Targets Platform — drug-target evidence scores.

    Retrieves:
      - Drug → target associations with evidence scores
      - Target → disease associations
      - Drug mechanisms of action

    Config keys
    -----------
    timeout : int  (default 25)
    """

    name = "Open Targets Platform"
    subcategory = "dti"
    resource_type = "Database"
    access_mode = AccessMode.REST_API
    aim = "Drug-target evidence"
    data_range = "Curated + ML drug-target evidence scores"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._timeout = int(self.config.get("timeout", 25))

    def retrieve(
        self,
        entities: Dict[str, List[str]],
        query: str = "",
        max_results: int = 20,
        **kwargs: Any,
    ) -> List[RetrievalResult]:
        drugs = entities.get("drug", [])
        results: List[RetrievalResult] = []
        include_indications = self._query_requests_indications(query)
        include_mechanisms = (
            not include_indications
            or self._query_requests_mechanisms(query)
            or not str(query).strip()
        )

        for drug in drugs:
            if len(results) >= max_results:
                break
            results.extend(
                self._search_drug(
                    drug,
                    max_results - len(results),
                    include_mechanisms=include_mechanisms,
                    include_indications=include_indications,
                )
            )

        return results

    @staticmethod
    def _query_requests_indications(query: str) -> bool:
        lowered = str(query).strip().lower()
        return any(
            marker in lowered
            for marker in (
                "indication",
                "indications",
                "approved",
                "repurposing",
                "repositioning",
                "treat",
                "therapy",
                "disease",
            )
        )

    @staticmethod
    def _query_requests_mechanisms(query: str) -> bool:
        lowered = str(query).strip().lower()
        return any(
            marker in lowered
            for marker in (
                "target",
                "targets",
                "mechanism",
                "mechanism of action",
                "moa",
            )
        )

    @staticmethod
    def _stage_rank(stage: str) -> int:
        normalized = str(stage or "").strip().upper()
        rank_map = {
            "APPROVAL": 100,
            "PHASE_4": 90,
            "PHASE_3": 80,
            "PHASE_2_3": 75,
            "PHASE_2": 70,
            "PHASE_1_2": 65,
            "PHASE_1": 60,
            "EARLY_PHASE_1": 50,
            "UNKNOWN": 0,
        }
        if normalized in rank_map:
            return rank_map[normalized]
        match = re.search(r"PHASE_(\d)", normalized)
        if match:
            return int(match.group(1)) * 10
        return 0

    def _search_drug(
        self,
        drug_name: str,
        limit: int,
        *,
        include_mechanisms: bool,
        include_indications: bool,
    ) -> List[RetrievalResult]:
        """Search for drug and retrieve its targets via Open Targets GraphQL."""
        # Step 1: search for drug by name to get ChEMBL ID
        search_query = """
        {
          search(queryString: "%s", entityNames: ["drug"]) {
            hits {
              id
              name
              entity
            }
          }
        }
        """ % drug_name.replace('"', '')

        chembl_id = self._graphql(search_query, ["search", "hits"])
        if not chembl_id:
            return []
        drug_id = chembl_id[0].get("id", "")
        canonical_name = chembl_id[0].get("name", drug_name)
        if not drug_id:
            return []

        field_blocks: List[str] = []
        if include_mechanisms:
            field_blocks.append(
                """
            mechanismsOfAction {
              rows {
                mechanismOfAction
                actionType
                targets {
                  id
                  approvedName
                  approvedSymbol
                }
              }
            }
                """.rstrip()
            )
        if include_indications:
            field_blocks.append(
                """
            indications {
              rows {
                disease {
                  id
                  name
                }
                maxClinicalStage
              }
            }
                """.rstrip()
            )
        if not field_blocks:
            field_blocks.append(
                """
            mechanismsOfAction {
              rows {
                mechanismOfAction
                actionType
                targets {
                  id
                  approvedName
                  approvedSymbol
                }
              }
            }
                """.rstrip()
            )

        drug_query = """
        {
          drug(chemblId: "%s") {
            id
            name
%s
          }
        }
        """ % (drug_id, "\n".join(field_blocks))

        drug_data = self._graphql(drug_query, ["drug"])
        if not drug_data:
            return []
        drug_info = drug_data[0] if isinstance(drug_data, list) else drug_data

        results: List[RetrievalResult] = []

        # Mechanisms of action
        if include_mechanisms:
            for row in (drug_info.get("mechanismsOfAction") or {}).get("rows", []):
                mechanism = row.get("mechanismOfAction", "").strip()
                action_type = row.get("actionType", "targets").lower().replace(" ", "_")
                for tgt in row.get("targets", []):
                    if len(results) >= limit:
                        break
                    tgt_name = tgt.get("approvedName") or tgt.get("approvedSymbol", "")
                    if not tgt_name:
                        continue
                    evidence_text = (
                        f"{canonical_name} {action_type} {tgt_name} "
                        f"(Open Targets MoA)"
                    )
                    if mechanism:
                        evidence_text = (
                            f"{canonical_name} {action_type} {tgt_name} "
                            f"via {mechanism} (Open Targets MoA)"
                        )
                    results.append(RetrievalResult(
                        source_entity=canonical_name,
                        source_type="drug",
                        target_entity=tgt_name,
                        target_type="protein",
                        relationship=action_type,
                        weight=1.0,
                        source="Open Targets Platform",
                        skill_category="dti",
                        evidence_text=evidence_text,
                        metadata={
                            "chembl_id": drug_id,
                            "target_id": tgt.get("id", ""),
                            "gene_symbol": tgt.get("approvedSymbol", ""),
                            "mechanism_of_action": mechanism,
                        },
                    ))

        if include_indications and len(results) < limit:
            indication_rows = list((drug_info.get("indications") or {}).get("rows", []))
            indication_rows.sort(
                key=lambda row: (
                    -self._stage_rank(row.get("maxClinicalStage", "")),
                    str((row.get("disease") or {}).get("name", "")).lower(),
                )
            )
            seen_diseases = set()
            for row in indication_rows:
                if len(results) >= limit:
                    break
                disease = row.get("disease") or {}
                disease_name = str(disease.get("name") or "").strip()
                if not disease_name:
                    continue
                disease_key = disease_name.lower()
                if disease_key in seen_diseases:
                    continue
                seen_diseases.add(disease_key)
                stage = str(row.get("maxClinicalStage") or "UNKNOWN").strip().upper()
                relationship = "indicated_for" if stage == "APPROVAL" else "investigated_for"
                results.append(RetrievalResult(
                    source_entity=canonical_name,
                    source_type="drug",
                    target_entity=disease_name,
                    target_type="disease",
                    relationship=relationship,
                    weight=1.0,
                    source="Open Targets Platform",
                    skill_category="dti",
                    evidence_text=(
                        f"{canonical_name} {relationship} {disease_name} "
                        f"(Open Targets max stage {stage})"
                    ),
                    metadata={
                        "chembl_id": drug_id,
                        "disease_id": disease.get("id", ""),
                        "max_clinical_stage": stage,
                    },
                ))

        return results

    def _graphql(self, query: str, path: List[str]):
        """Execute a GraphQL query and traverse path in the result."""
        try:
            payload = json.dumps({"query": query}).encode()
            req = urllib.request.Request(
                _GRAPHQL,
                data=payload,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                data = json.loads(resp.read().decode())
        except Exception as exc:
            logger.debug("OpenTargets: GraphQL failed — %s", exc)
            return None

        node = data.get("data", {})
        for key in path:
            if isinstance(node, dict):
                node = node.get(key)
            elif isinstance(node, list) and node:
                node = node[0].get(key) if isinstance(node[0], dict) else None
            else:
                return None
        return node

    def build_evidence_items(
        self,
        records: List[Dict[str, Any]],
        query: str = "",
    ) -> List[EvidenceItem]:
        items: List[EvidenceItem] = []
        for index, record in enumerate(records, start=1):
            metadata = record.get("metadata", {})
            relationship = record.get("relationship", "")
            source_entity = record.get("source_entity", "")
            target_entity = record.get("target_entity", "")
            predictive = relationship == "linked_target"
            item = EvidenceItem(
                evidence_id=f"opentargets:{index}",
                source_skill=self.name,
                source_type="prediction" if predictive else "database",
                source_title="Open Targets Platform drug-target evidence",
                source_locator=(
                    f"{metadata.get('chembl_id', '')}:{metadata.get('target_id', '')}".strip(":")
                    or "Open Targets Platform"
                ),
                snippet=record.get("evidence_text", ""),
                structured_payload={
                    "chembl_id": metadata.get("chembl_id", ""),
                    "target_id": metadata.get("target_id", ""),
                    "disease_id": metadata.get("disease_id", ""),
                    "gene_symbol": metadata.get("gene_symbol", ""),
                    "mechanism_of_action": metadata.get("mechanism_of_action", ""),
                    "max_clinical_stage": metadata.get("max_clinical_stage", ""),
                    "relationship": relationship,
                },
                claim=f"{source_entity} {relationship} {target_entity}".strip(),
                evidence_kind="model_prediction" if predictive else "database_record",
                support_direction="supports",
                confidence=0.0,
                retrieval_score=0.55 if predictive else (
                    0.84 if metadata.get("max_clinical_stage") == "APPROVAL" else 0.78
                ),
                timestamp="2026-03-18T00:00:00Z",
                metadata={
                    "skill_category": self.subcategory,
                    "source_entity": source_entity,
                    "relationship": relationship,
                    "target_entity": target_entity,
                    "source_type": "drug",
                    "target_type": record.get("target_type", "protein"),
                    "mechanism_of_action": metadata.get("mechanism_of_action", ""),
                    "max_clinical_stage": metadata.get("max_clinical_stage", ""),
                },
            )
            item.confidence = score_evidence_item(item)
            items.append(item)
        return items
