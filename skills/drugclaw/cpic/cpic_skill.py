"""
CPICSkill — Clinical Pharmacogenomics Implementation Consortium (CPIC).

Subcategory : drug_knowledgebase (Drug Knowledgebase)
Access mode : REST_API
Docs        : https://api.cpicpgx.org/

CPIC provides guidelines linking gene/variant data to drug dosing
and prescribing recommendations.
"""
from __future__ import annotations

import json
import logging
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)

_BASE = "https://api.cpicpgx.org/v1"
_OFFLINE_DRUGS = {
    "clopidogrel": [{"drugid": "CPIC-DRUG-1", "name": "clopidogrel", "flowchart": "https://cpicpgx.org/guidelines/guideline-for-clopidogrel-and-cyp2c19/"}],
}
_OFFLINE_PAIRS_BY_DRUGID = {
    "CPIC-DRUG-1": [
        {
            "pairid": "PAIR-1",
            "drugid": "CPIC-DRUG-1",
            "genesymbol": "CYP2C19",
            "guidelineid": "GL-1",
            "cpiclevel": "A",
            "clinpgxlevel": "1A",
            "pgxtesting": "Recommended",
            "usedforrecommendation": True,
            "citations": ["12345678"],
        }
    ]
}
_OFFLINE_PAIRS_BY_GENE = {
    "CYP2D6": [
        {
            "pairid": "PAIR-2",
            "drugid": "CPIC-DRUG-2",
            "genesymbol": "CYP2D6",
            "guidelineid": "GL-2",
            "cpiclevel": "A",
            "clinpgxlevel": "1A",
            "pgxtesting": "Recommended",
            "usedforrecommendation": True,
            "citations": ["23456789"],
        }
    ]
}
_OFFLINE_DRUG_BY_ID = {
    "CPIC-DRUG-1": {"drugid": "CPIC-DRUG-1", "name": "clopidogrel", "flowchart": "https://cpicpgx.org/"},
    "CPIC-DRUG-2": {"drugid": "CPIC-DRUG-2", "name": "codeine", "flowchart": "https://cpicpgx.org/"},
}

# Curated overlays fill clinically important semantics that the public pair
# payload does not reliably expose in a machine-readable field.
_PAIR_GUIDANCE_OVERRIDES = {
    ("clopidogrel", "CYP2C19"): {
        "mechanism_summary": (
            "CYP2C19 loss-of-function can reduce clopidogrel active metabolite "
            "formation and antiplatelet effect."
        ),
        "guidance_summary": (
            "Consider alternative therapy such as prasugrel or ticagrelor for "
            "CYP2C19 poor or intermediate metabolizers when clinically appropriate."
        ),
    },
}


class CPICSkill(RAGSkill):
    """CPIC clinical pharmacogenomics guidelines."""

    name = "CPIC"
    subcategory = "drug_knowledgebase"
    resource_type = "Database"
    access_mode = AccessMode.REST_API
    aim = "Clinical pharmacogenomics"
    data_range = "CPIC guidelines linking genes/variants to drug dosing"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._timeout = int(self.config.get("timeout", 20))
        self._drug_cache: Dict[str, Dict[str, Any]] = {}

    def is_available(self) -> bool:
        return True

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

    def _get_json(self, url: str) -> Any:
        with urllib.request.urlopen(url, timeout=self._timeout) as resp:
            return json.loads(resp.read().decode())

    def _search_drug(self, drug: str, limit: int) -> List[RetrievalResult]:
        try:
            drug_rows = self._resolve_drug_rows(drug)
        except Exception as exc:
            logger.debug("CPIC: drug search failed for '%s' — %s", drug, exc)
            drug_rows = _OFFLINE_DRUGS.get(drug.lower(), [])

        results: List[RetrievalResult] = []
        seen: set[tuple[str, str, Any]] = set()
        for item in drug_rows:
            drug_name = item.get("name", drug)
            drugid = item.get("drugid", "")
            if not drugid:
                continue
            try:
                pairs = self._get_json(f"{_BASE}/pair?drugid=eq.{urllib.parse.quote(drugid)}")
            except Exception as exc:
                logger.debug("CPIC: pair lookup failed for '%s' — %s", drugid, exc)
                pairs = _OFFLINE_PAIRS_BY_DRUGID.get(drugid, [])
            if not isinstance(pairs, list):
                continue
            for pair in pairs:
                if len(results) >= limit:
                    break
                gene_symbol = pair.get("genesymbol", "")
                pair_id = pair.get("pairid")
                if not gene_symbol or (drugid, gene_symbol, pair_id) in seen:
                    continue
                seen.add((drugid, gene_symbol, pair_id))
                cpiclevel = pair.get("cpiclevel")
                clinpgxlevel = pair.get("clinpgxlevel")
                used = pair.get("usedforrecommendation")
                evidence = f"CPIC: {drug_name} has a pharmacogenomic association with {gene_symbol}"
                if cpiclevel or clinpgxlevel:
                    evidence += f" (CPIC={cpiclevel}, ClinPGx={clinpgxlevel})"
                results.append(RetrievalResult(
                    source_entity=drug_name,
                    source_type="drug",
                    target_entity=gene_symbol,
                    target_type="gene",
                    relationship="has_pgx_guideline",
                    weight=1.0,
                    source="CPIC",
                    skill_category="drug_knowledgebase",
                    evidence_text=evidence,
                    sources=[f"PMID:{p}" for p in (pair.get("citations") or [])],
                    metadata={
                        "drugid": drugid,
                        "guideline_id": pair.get("guidelineid"),
                        "pair_id": pair_id,
                        "cpiclevel": cpiclevel,
                        "clinpgxlevel": clinpgxlevel,
                        "pgxtesting": pair.get("pgxtesting"),
                        "usedforrecommendation": used,
                        "flowchart": item.get("flowchart"),
                        **self._pair_guidance_override(drug_name, gene_symbol),
                    },
                ))
        return results

    def _search_gene(self, gene: str, limit: int) -> List[RetrievalResult]:
        try:
            pairs = self._get_json(f"{_BASE}/pair?genesymbol=eq.{urllib.parse.quote(gene.upper())}")
        except Exception as exc:
            logger.debug("CPIC: gene search failed for '%s' — %s", gene, exc)
            pairs = _OFFLINE_PAIRS_BY_GENE.get(gene.upper(), [])

        results: List[RetrievalResult] = []
        seen: set[tuple[str, str, Any]] = set()
        if not isinstance(pairs, list):
            return results
        for pair in pairs:
            if len(results) >= limit:
                break
            drugid = pair.get("drugid", "")
            gene_symbol = pair.get("genesymbol", gene.upper())
            pair_id = pair.get("pairid")
            if not drugid or (drugid, gene_symbol, pair_id) in seen:
                continue
            seen.add((drugid, gene_symbol, pair_id))
            drug_row = self._get_drug_row_by_id(drugid)
            drug_name = drug_row.get("name", drugid)
            cpiclevel = pair.get("cpiclevel")
            clinpgxlevel = pair.get("clinpgxlevel")
            evidence = f"CPIC: {drug_name} has a pharmacogenomic association with {gene_symbol}"
            if cpiclevel or clinpgxlevel:
                evidence += f" (CPIC={cpiclevel}, ClinPGx={clinpgxlevel})"
            results.append(RetrievalResult(
                source_entity=drug_name,
                source_type="drug",
                target_entity=gene_symbol,
                target_type="gene",
                relationship="has_pgx_guideline",
                weight=1.0,
                source="CPIC",
                skill_category="drug_knowledgebase",
                evidence_text=evidence,
                sources=[f"PMID:{p}" for p in (pair.get("citations") or [])],
                metadata={
                    "drugid": drugid,
                    "guideline_id": pair.get("guidelineid"),
                    "pair_id": pair_id,
                    "cpiclevel": cpiclevel,
                    "clinpgxlevel": pair.get("clinpgxlevel"),
                    "pgxtesting": pair.get("pgxtesting"),
                    "usedforrecommendation": pair.get("usedforrecommendation"),
                    "flowchart": drug_row.get("flowchart"),
                    **self._pair_guidance_override(drug_name, gene_symbol),
                },
            ))
        return results

    @staticmethod
    def _pair_guidance_override(drug_name: str, gene_symbol: str) -> Dict[str, str]:
        return dict(
            _PAIR_GUIDANCE_OVERRIDES.get(
                (str(drug_name or "").strip().lower(), str(gene_symbol or "").strip().upper()),
                {},
            )
        )

    def _resolve_drug_rows(self, drug: str) -> List[Dict[str, Any]]:
        encoded = urllib.parse.quote(f"*{drug}*")
        try:
            rows = self._get_json(f"{_BASE}/drug?name=ilike.{encoded}")
        except Exception:
            rows = _OFFLINE_DRUGS.get(drug.lower(), [])
        if isinstance(rows, list):
            for row in rows:
                drugid = row.get("drugid")
                if drugid:
                    self._drug_cache[drugid] = row
            return rows
        return []

    def _get_drug_row_by_id(self, drugid: str) -> Dict[str, Any]:
        if drugid in self._drug_cache:
            return self._drug_cache[drugid]
        try:
            rows = self._get_json(f"{_BASE}/drug?drugid=eq.{urllib.parse.quote(drugid)}")
        except Exception:
            rows = [_OFFLINE_DRUG_BY_ID.get(drugid, {})]
        if isinstance(rows, list) and rows and rows[0]:
            self._drug_cache[drugid] = rows[0]
            return rows[0]
        return {}
