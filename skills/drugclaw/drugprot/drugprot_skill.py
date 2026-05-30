"""
DrugProtSkill — DrugProt Drug-Protein Relation Extraction Corpus.

Subcategory : drug_nlp
Access mode : DATASET (local TSV files)
Source      : https://zenodo.org/record/5119892
Paper       : BioCreative VII Track 1 (2021)

DrugProt provides manually annotated drug-protein relations from biomedical
literature for relation extraction NLP benchmarks.

Config keys
-----------
tsv_path  : str  path to DrugProt entities+relations TSV or combined file
              Expected columns: pmid, entity1 (or drug), entity2 (or protein),
                                relation_type (or label), [sentence]
delimiter : str  column delimiter (default: "\t")
"""
from __future__ import annotations

import csv
import logging
import os
from collections import defaultdict
from typing import Any, Dict, List, Optional

from ...base import DatasetRAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)


class DrugProtSkill(DatasetRAGSkill):
    """DrugProt — drug-protein relation extraction corpus (BioCreative VII)."""

    name = "DrugProt"
    subcategory = "drug_nlp"
    resource_type = "Dataset"
    access_mode = AccessMode.DATASET
    aim = "Drug-protein relation corpus"
    data_range = "BioCreative VII drug-protein relation extraction corpus"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._rows: List[Dict] = []
        self._drug_index: Dict[str, List[int]] = defaultdict(list)

    def _load(self) -> None:
        path = self.config.get("tsv_path", "") or self.config.get("csv_path", "")
        if not path or not os.path.exists(path):
            logger.warning(
                "DrugProtSkill: file not found. "
                "Download from https://zenodo.org/record/5119892 "
                "and set config['tsv_path']."
            )
            return
        delim = self.config.get("delimiter", "\t")
        try:
            with open(path, newline="", encoding="utf-8", errors="ignore") as fh:
                for row in csv.DictReader(fh, delimiter=delim):
                    drug = (row.get("entity1", "") or row.get("drug", "") or
                            row.get("chemical", "")).strip()
                    if drug:
                        idx = len(self._rows)
                        self._rows.append(row)
                        self._drug_index[drug.lower()].append(idx)
            logger.info("DrugProt: loaded %d relation records", len(self._rows))
        except Exception as exc:
            logger.error("DrugProt: load failed — %s", exc)
            return

        self._build_fuzzy_index(self._drug_index.keys())

    def is_available(self) -> bool:
        self._ensure_loaded()
        return bool(self._rows)

    def retrieve(
        self,
        entities: Dict[str, List[str]],
        query: str = "",
        max_results: int = 20,
        **kwargs: Any,
    ) -> List[RetrievalResult]:
        self._ensure_loaded()
        results: List[RetrievalResult] = []
        seen: set = set()
        for drug in entities.get("drug", []):
            for idx in self._fuzzy_get(drug, self._drug_index):
                if len(results) >= max_results or idx in seen:
                    continue
                seen.add(idx)
                row = self._rows[idx]
                drug_name = (row.get("entity1", "") or row.get("drug", "") or
                             row.get("chemical", drug)).strip()
                protein = (row.get("entity2", "") or row.get("protein", "") or
                           row.get("gene", "")).strip()
                rel = (row.get("relation_type", "") or row.get("label", "") or
                       "drug_protein_relation").strip()
                sentence = row.get("sentence", "")[:200]
                results.append(RetrievalResult(
                    source_entity=drug_name,
                    source_type="drug",
                    target_entity=protein or "protein",
                    target_type="protein",
                    relationship=rel.lower().replace(" ", "_").replace("-", "_"),
                    weight=1.0,
                    source="DrugProt",
                    skill_category="drug_nlp",
                    evidence_text=f"DrugProt: {drug_name} {rel} {protein}" +
                                  (f" — {sentence}" if sentence else ""),
                    metadata={"relation_type": rel, "pmid": row.get("pmid", "")},
                ))
        return results

    def get_all_pairs(self) -> List[Dict[str, Any]]:
        self._ensure_loaded()
        return [
            {"drug": (r.get("entity1", "") or r.get("drug", "")).strip(),
             "disease": (r.get("entity2", "") or r.get("protein", "")).strip(),
             "label": r.get("relation_type", "")}
            for r in self._rows
        ]
