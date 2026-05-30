"""
GDSCSkill — Genomics of Drug Sensitivity in Cancer (GDSC).

Subcategory : drug_molecular_property
Access mode : LOCAL_FILE
Download    : https://ftp.sanger.ac.uk/pub/project/cancerrxgene/releases/current_release/
Paper       : Yang et al., Nucleic Acids Research, 2013

GDSC provides drug sensitivity resources and curated compound metadata
including drug names, synonyms, targets, and target pathways.

Config keys
-----------
csv_path  : str  path to a GDSC CSV file.
              Supported formats:
                1. screened_compounds_rel_8.4.csv
                   Columns: DRUG_NAME, SYNONYMS, TARGET, TARGET_PATHWAY
                2. fitted dose response CSV (if converted from XLSX)
                   Columns such as DRUG_NAME, CELL_LINE_NAME, LN_IC50 / IC50
delimiter : str  column delimiter (default: auto-detect from extension)
"""
from __future__ import annotations

import csv
import logging
import os
from collections import defaultdict
from math import exp
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)


class GDSCSkill(RAGSkill):
    """GDSC — compound metadata and sensitivity profiles across cancer models."""

    name = "GDSC"
    subcategory = "drug_molecular_property"
    resource_type = "Dataset"
    access_mode = AccessMode.LOCAL_FILE
    aim = "Cancer drug target and sensitivity resource"
    data_range = "GDSC compound metadata plus fitted drug sensitivity profiles"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._rows: List[Dict] = []
        self._drug_index: Dict[str, List[int]] = defaultdict(list)
        self._synonym_index: Dict[str, List[int]] = defaultdict(list)
        self._loaded = False

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        self._loaded = True
        path = self.config.get("csv_path", "")
        if not path or not os.path.exists(path):
            logger.warning(
                "GDSCSkill: file not found. "
                "Download from https://www.cancerrxgene.org/downloads/bulk_download "
                "and set config['csv_path']."
            )
            return
        delim = self.config.get("delimiter", "\t" if path.endswith(".tsv") else ",")
        try:
            with open(path, newline="", encoding="utf-8", errors="ignore") as fh:
                for row in csv.DictReader(fh, delimiter=delim):
                    drug = (row.get("DRUG_NAME", "") or row.get("drug_name", "") or
                            row.get("Drug", "")).strip()
                    if drug:
                        idx = len(self._rows)
                        self._rows.append(row)
                        self._drug_index[drug.lower()].append(idx)
                        synonyms = row.get("SYNONYMS", "") or row.get("synonyms", "")
                        for syn in [s.strip() for s in synonyms.split(",") if s.strip()]:
                            self._synonym_index[syn.lower()].append(idx)
            logger.info("GDSC: loaded %d drug-cell sensitivity records", len(self._rows))
        except Exception as exc:
            logger.error("GDSC: load failed — %s", exc)
            return

        self._build_fuzzy_index(self._drug_index.keys())

    def is_available(self) -> bool:
        self._ensure_loaded()
        return bool(self._rows)

    def retrieve(
        self,
        entities: Dict[str, List[str]],
        query: str = "",
        max_results: int = 30,
        **kwargs: Any,
    ) -> List[RetrievalResult]:
        self._ensure_loaded()
        results: List[RetrievalResult] = []

        for drug in entities.get("drug", []):
            idxs = self._fuzzy_get(drug, self._drug_index)
            if not idxs:
                idxs = list(self._synonym_index.get(drug.lower(), []))
            for idx in idxs:
                if len(results) >= max_results:
                    break
                row = self._rows[idx]
                drug_name = (row.get("DRUG_NAME", "") or row.get("drug_name", "") or
                             row.get("Drug", drug)).strip()
                target = (row.get("TARGET", "") or row.get("DRUG_TARGETS", "") or
                          row.get("drug_targets", "")).strip()
                pathway = (row.get("TARGET_PATHWAY", "") or row.get("PATHWAY_NAME", "") or
                           row.get("target_pathway", "")).strip()
                synonyms = (row.get("SYNONYMS", "") or row.get("synonyms", "")).strip()
                cell_line = (row.get("CELL_LINE_NAME", "") or row.get("cell_line_name", "") or
                             row.get("CellLine", "")).strip()
                ln_ic50 = row.get("LN_IC50", "") or row.get("ln_ic50", "")
                ic50_raw = row.get("IC50", "") or row.get("ic50", "")
                if ln_ic50:
                    try:
                        ic50_val = f"{exp(float(ln_ic50)):.3f} µM"
                    except ValueError:
                        ic50_val = ln_ic50
                else:
                    ic50_val = ic50_raw
                auc = row.get("AUC", "") or row.get("auc", "")
                cancer_type = row.get("TCGA_DESC", "") or row.get("cancer_type", "")
                if target:
                    results.append(RetrievalResult(
                        source_entity=drug_name,
                        source_type="drug",
                        target_entity=target,
                        target_type="target",
                        relationship="has_target",
                        weight=1.0,
                        source="GDSC",
                        skill_category="drug_molecular_property",
                        evidence_text=(
                            f"GDSC: {drug_name} targets {target}"
                            + (f" via pathway {pathway}" if pathway else "")
                        ),
                        metadata={
                            "target": target,
                            "target_pathway": pathway,
                            "synonyms": synonyms,
                            "drug_id": row.get("DRUG_ID", ""),
                            "screening_site": row.get("SCREENING_SITE", ""),
                        },
                    ))
                elif cell_line:
                    results.append(RetrievalResult(
                        source_entity=drug_name,
                        source_type="drug",
                        target_entity=cell_line,
                        target_type="cell_line",
                        relationship="has_ic50_sensitivity",
                        weight=1.0,
                        source="GDSC",
                        skill_category="drug_molecular_property",
                        evidence_text=(
                            f"GDSC: {drug_name} IC50={ic50_val} in {cell_line}"
                            + (f" ({cancer_type})" if cancer_type else "")
                        ),
                        metadata={
                            "ic50": ic50_val,
                            "auc": auc,
                            "cell_line": cell_line,
                            "cancer_type": cancer_type,
                            "drug_id": row.get("DRUG_ID", ""),
                        },
                    ))
        return results
