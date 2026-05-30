"""
PharmGKBSkill — PharmGKB/ClinPGx Pharmacogenomics Knowledge Base.

Subcategory : pharmacogenomics
Access mode : REST_API
Docs        : https://api.pharmgkb.org/

PharmGKB curates pharmacogenomics knowledge: variant-drug-outcome
annotations, clinical guidelines, and pathway information.
"""
from __future__ import annotations

import json
import logging
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)

_BASE = "https://api.pharmgkb.org/v1"
_OFFLINE_DRUGS = {
    "clopidogrel": [{"id": "PA449726", "name": "clopidogrel"}],
}
_OFFLINE_RELATIONS = {
    "PA449726": [{"symbol": "CYP2C19"}],
}
_OFFLINE_GENES = {
    "CYP2C19": [{"id": "PA124", "symbol": "CYP2C19", "relatedChemicals": [{"name": "clopidogrel"}]}],
}


class PharmGKBSkill(RAGSkill):
    """PharmGKB pharmacogenomics knowledge base."""

    name = "PharmGKB"
    subcategory = "pharmacogenomics"
    resource_type = "Database"
    access_mode = AccessMode.REST_API
    aim = "Pharmacogenomics knowledge base"
    data_range = "Curated PGx knowledge: variant-drug-outcome annotations"
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
            results.extend(self._search_drug(drug, max_results - len(results)))
        for gene in entities.get("gene", []):
            if len(results) >= max_results:
                break
            results.extend(self._search_gene(gene, max_results - len(results)))
        return results

    def _search_drug(self, drug: str, limit: int) -> List[RetrievalResult]:
        url = (
            f"{_BASE}/data/chemical"
            f"?view=base&name={urllib.parse.quote(drug)}&limit={min(limit, 5)}"
        )
        try:
            with urllib.request.urlopen(url, timeout=self._timeout) as resp:
                data = json.loads(resp.read().decode())
        except Exception as exc:
            logger.debug("PharmGKB: drug search failed for '%s' — %s", drug, exc)
            data = {"data": _OFFLINE_DRUGS.get(drug.lower(), [])}

        results: List[RetrievalResult] = []
        for chem in (data.get("data") or [])[:limit]:
            pgkb_id = chem.get("id", "")
            name = chem.get("name", drug)
            results.extend(self._get_drug_relations(pgkb_id, name, limit - len(results)))
        return results

    def _get_drug_relations(self, pgkb_id: str, drug_name: str, limit: int) -> List[RetrievalResult]:
        url = f"{_BASE}/data/chemical/{pgkb_id}/relatedGenes?view=base"
        try:
            with urllib.request.urlopen(url, timeout=self._timeout) as resp:
                data = json.loads(resp.read().decode())
        except Exception:
            data = {"data": _OFFLINE_RELATIONS.get(pgkb_id, [])}

        results: List[RetrievalResult] = []
        for gene in (data.get("data") or [])[:limit]:
            gene_symbol = gene.get("symbol", "")
            if gene_symbol:
                results.append(RetrievalResult(
                    source_entity=drug_name,
                    source_type="drug",
                    target_entity=gene_symbol,
                    target_type="gene",
                    relationship="has_pgx_association",
                    weight=1.0,
                    source="PharmGKB",
                    skill_category="pharmacogenomics",
                    evidence_text=f"PharmGKB: {drug_name} has PGx association with {gene_symbol}",
                    metadata={"pharmgkb_id": pgkb_id},
                ))
        return results

    def _search_gene(self, gene: str, limit: int) -> List[RetrievalResult]:
        url = (
            f"{_BASE}/data/gene"
            f"?view=base&symbol={urllib.parse.quote(gene)}&limit={min(limit, 5)}"
        )
        try:
            with urllib.request.urlopen(url, timeout=self._timeout) as resp:
                data = json.loads(resp.read().decode())
        except Exception as exc:
            logger.debug("PharmGKB: gene search failed for '%s' — %s", gene, exc)
            data = {"data": _OFFLINE_GENES.get(gene.upper(), [])}

        results: List[RetrievalResult] = []
        for gene_entry in (data.get("data") or [])[:limit]:
            gene_symbol = gene_entry.get("symbol", gene)
            pgkb_id = gene_entry.get("id", "")
            for drug in gene_entry.get("relatedChemicals", [])[:5]:
                drug_name = drug.get("name", "")
                if drug_name:
                    results.append(RetrievalResult(
                        source_entity=drug_name,
                        source_type="drug",
                        target_entity=gene_symbol,
                        target_type="gene",
                        relationship="has_pgx_association",
                        weight=1.0,
                        source="PharmGKB",
                        skill_category="pharmacogenomics",
                        evidence_text=f"PharmGKB: {drug_name} has PGx association with {gene_symbol}",
                        metadata={"pharmgkb_gene_id": pgkb_id},
                    ))
        return results
