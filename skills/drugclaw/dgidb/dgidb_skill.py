"""
DGIdbSkill — Drug-Gene Interaction Database via GraphQL API.

Subcategory : dti (Drug-Target Interaction)
Access mode : REST_API (GraphQL endpoint)
Docs        : https://dgidb.org/api/graphql

DGIdb aggregates drug-gene interaction data from NCI, ClinVar, ChEMBL,
PharmGKB, and many other sources.
"""
from __future__ import annotations

import json
import logging
import urllib.request
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)

_GRAPHQL = "https://dgidb.org/api/graphql"

_QUERY_TEMPLATE = """
{{
  genes(names: {gene_list}) {{
    nodes {{
      name
      interactions {{
        drug {{
          name
          conceptId
        }}
        interactionTypes {{
          type
          directionality
        }}
        publications {{
          pmid
        }}
        sources {{
          sourceDbName
        }}
      }}
    }}
  }}
  drugs(names: {drug_list}) {{
    nodes {{
      name
      conceptId
      interactions {{
        gene {{
          name
        }}
        interactionTypes {{
          type
          directionality
        }}
        publications {{
          pmid
        }}
        sources {{
          sourceDbName
        }}
      }}
    }}
  }}
}}
"""


class DGIdbSkill(RAGSkill):
    """
    DGIdb drug–gene interaction database.

    Retrieves drug-gene interactions from a GraphQL endpoint.
    Supports both drug-centric and gene-centric queries.

    Config keys
    -----------
    timeout : int  (default 20)
    """

    name = "DGIdb"
    subcategory = "dti"
    resource_type = "Database"
    access_mode = AccessMode.REST_API
    aim = "Drug–gene interactions"
    data_range = "Curated drug–gene interaction database (NCI, ClinVar, etc.)"
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
        genes = entities.get("gene", [])

        if not drugs and not genes:
            return []

        def _fmt_list(lst: List[str]) -> str:
            return "[" + ", ".join(f'"{x}"' for x in lst) + "]"

        gql_query = _QUERY_TEMPLATE.format(
            gene_list=_fmt_list(genes) if genes else '[]',
            drug_list=_fmt_list(drugs) if drugs else '[]',
        )

        try:
            payload = json.dumps({"query": gql_query}).encode()
            req = urllib.request.Request(
                _GRAPHQL,
                data=payload,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                data = json.loads(resp.read().decode())
        except Exception as exc:
            logger.debug("DGIdb: GraphQL request failed — %s", exc)
            return []

        results: List[RetrievalResult] = []
        gql_data = data.get("data", {})

        # Drug-centric results
        for drug_node in (gql_data.get("drugs") or {}).get("nodes", []):
            drug_name = drug_node.get("name", "")
            for iact in drug_node.get("interactions", []):
                if len(results) >= max_results:
                    break
                gene_name = (iact.get("gene") or {}).get("name", "")
                if not gene_name:
                    continue
                itypes = iact.get("interactionTypes", []) or []
                rel = (itypes[0].get("type", "interacts") if itypes else "interacts").lower()
                pmids = [p["pmid"] for p in (iact.get("publications") or []) if p.get("pmid")]
                sources_used = [s["sourceDbName"] for s in (iact.get("sources") or []) if s.get("sourceDbName")]
                results.append(RetrievalResult(
                    source_entity=drug_name,
                    source_type="drug",
                    target_entity=gene_name,
                    target_type="gene",
                    relationship=rel,
                    weight=1.0,
                    source="DGIdb",
                    skill_category="dti",
                    evidence_text=f"DGIdb: {drug_name} {rel} {gene_name}",
                    sources=[f"PMID:{p}" for p in pmids[:5]],
                    metadata={"dgidb_sources": sources_used},
                ))

        # Gene-centric results
        for gene_node in (gql_data.get("genes") or {}).get("nodes", []):
            gene_name = gene_node.get("name", "")
            for iact in gene_node.get("interactions", []):
                if len(results) >= max_results:
                    break
                drug_info = iact.get("drug") or {}
                d_name = drug_info.get("name", "")
                if not d_name:
                    continue
                itypes = iact.get("interactionTypes", []) or []
                rel = (itypes[0].get("type", "interacts") if itypes else "interacts").lower()
                pmids = [p["pmid"] for p in (iact.get("publications") or []) if p.get("pmid")]
                results.append(RetrievalResult(
                    source_entity=d_name,
                    source_type="drug",
                    target_entity=gene_name,
                    target_type="gene",
                    relationship=rel,
                    weight=1.0,
                    source="DGIdb",
                    skill_category="dti",
                    evidence_text=f"DGIdb: {d_name} {rel} {gene_name}",
                    sources=[f"PMID:{p}" for p in pmids[:5]],
                ))

        return results[:max_results]
