"""
MolecularTargetsDataSkill — NCI DTP Molecular Target (Protein) Data.

Subcategory : dti (Drug-Target Interaction)
Access mode : LOCAL_FILE
Source      : https://wiki.nci.nih.gov/spaces/NCIDTPdata/pages/155845004

Protein expression across the NCI-60 cancer cell line panel from the
NCI Developmental Therapeutics Program.

Config keys
-----------
data_path : str  absolute path to WEB_DATA_PROTEIN.TXT
"""
from __future__ import annotations

import csv
import logging
import os
import re
from collections import defaultdict
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)

_COLUMNS = [
    "MOLTID", "GENE", "TITLE", "MOLTNBR", "PANELNBR", "CELLNBR",
    "pname", "cellname", "ENTITY_MEASURED", "GeneID", "UNITS",
    "METHOD", "VALUE", "TEXT",
]


class MolecularTargetsDataSkill(RAGSkill):
    """NCI DTP — protein expression across NCI-60 cell lines."""

    name = "Molecular Targets Data"
    subcategory = "dti"
    resource_type = "Database"
    access_mode = AccessMode.LOCAL_FILE
    aim = "NCI-60 protein expression for drug target analysis"
    data_range = "Protein expression across NCI-60 cancer cell lines"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._records: List[dict] = []
        self._gene_index: Dict[str, List[int]] = defaultdict(list)
        self._loaded = False

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        self._loaded = True
        path = self.config.get("data_path", "")
        if not path or not os.path.exists(path):
            logger.warning("MolecularTargetsDataSkill: data file not found — set config['data_path']")
            return
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                reader = csv.reader(fh)
                for i, row in enumerate(reader):
                    if not row or row[0].startswith("#"):
                        continue
                    rec = {}
                    for j, col in enumerate(_COLUMNS):
                        rec[col] = row[j].strip() if j < len(row) else ""
                    try:
                        rec["VALUE"] = float(rec["VALUE"])
                    except (ValueError, TypeError):
                        pass
                    self._records.append(rec)
                    gene = rec["GENE"].lower()
                    if gene:
                        self._gene_index[gene].append(len(self._records) - 1)
            logger.info("MolecularTargetsData: loaded %d records", len(self._records))
        except Exception as exc:
            logger.error("MolecularTargetsData: load failed — %s", exc)

    def is_available(self) -> bool:
        self._ensure_loaded()
        return bool(self._records)

    def retrieve(
        self,
        entities: Dict[str, List[str]],
        query: str = "",
        max_results: int = 50,
        **kwargs: Any,
    ) -> List[RetrievalResult]:
        self._ensure_loaded()
        results: List[RetrievalResult] = []

        for names in entities.values():
            for name in names:
                if len(results) >= max_results:
                    return results
                indices = self._gene_index.get(name.lower(), [])
                for idx in indices:
                    if len(results) >= max_results:
                        break
                    rec = self._records[idx]
                    val = rec.get("VALUE", "")
                    units = rec.get("UNITS", "")
                    cell = rec.get("cellname", "")
                    results.append(RetrievalResult(
                        source_entity=name,
                        source_type="gene",
                        target_entity=cell,
                        target_type="cell_line",
                        relationship="protein_expression",
                        weight=1.0,
                        source="Molecular Targets Data",
                        skill_category="dti",
                        evidence_text=f"NCI-60: {rec.get('GENE','')} in {cell} = {val}{units} ({rec.get('METHOD','')})",
                        metadata={
                            "moltid": rec.get("MOLTID"),
                            "panel": rec.get("pname"),
                            "entity_measured": rec.get("ENTITY_MEASURED"),
                            "method": rec.get("METHOD"),
                            "value": val,
                            "units": units,
                        },
                    ))
        return results
