"""
DrugMechDBSkill — Drug Mechanism of Action Database.

Subcategory : drug_mechanism (Drug Mechanism)
Access mode : REST_API (auto-downloads JSON from GitHub on first use)
Source      : https://github.com/SuLab/DrugMechDB

DrugMechDB provides curated drug mechanism-of-action paths representing
the biological mechanism by which a drug induces its primary indicated effect.

Config keys
-----------
local_path   : str   optional path to indication_paths.json
fetch_remote : bool  download from GitHub if local_path missing (default True)
"""
from __future__ import annotations

import json
import logging
import os
import urllib.request
from typing import Any, Dict, List, Optional

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)

_REMOTE_URL = (
    "https://raw.githubusercontent.com/SuLab/DrugMechDB/main/"
    "indication_paths.json"
)


class DrugMechDBSkill(RAGSkill):
    """DrugMechDB — curated drug MoA paths linking drugs to disease effects."""

    name = "DRUGMECHDB"
    subcategory = "drug_mechanism"
    resource_type = "Database"
    access_mode = AccessMode.REST_API
    aim = "Drug mechanism-of-action paths"
    data_range = "Curated MoA paths linking drugs to diseases via biological graphs"
    _implemented = True

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._paths: List[Dict] = []
        self._drug_index: Dict[str, List[int]] = {}
        self._loaded = False

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        self._loaded = True
        local = self.config.get("local_path", "")
        fetch = self.config.get("fetch_remote", True)

        if local and os.path.exists(local):
            self._load_from_file(local)
        elif fetch:
            self._load_from_remote()
        else:
            logger.warning("DrugMechDB: no data source configured")

    def _load_from_file(self, path: str) -> None:
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
            self._index_data(data)
            logger.info("DrugMechDB: loaded %d paths from %s", len(self._paths), path)
        except Exception as exc:
            logger.error("DrugMechDB: load failed — %s", exc)

    def _load_from_remote(self) -> None:
        try:
            with urllib.request.urlopen(_REMOTE_URL, timeout=30) as resp:
                data = json.loads(resp.read().decode())
            self._index_data(data)
            logger.info("DrugMechDB: downloaded %d paths from GitHub", len(self._paths))
        except Exception as exc:
            logger.warning("DrugMechDB: remote download failed — %s", exc)

    def _index_data(self, data: List[Dict]) -> None:
        for entry in data:
            idx = len(self._paths)
            self._paths.append(entry)
            drug = entry.get("drug", "")
            if drug:
                key = drug.lower()
                if key not in self._drug_index:
                    self._drug_index[key] = []
                self._drug_index[key].append(idx)
        self._build_fuzzy_index(self._drug_index.keys())

    def is_available(self) -> bool:
        return self._implemented

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
            for idx in self._fuzzy_get(drug, self._drug_index):
                if len(results) >= max_results:
                    break
                entry = self._paths[idx]
                results.extend(
                    self._path_to_results(entry, max_results - len(results))
                )

        return results

    def _path_to_results(self, entry: Dict, limit: int) -> List[RetrievalResult]:
        drug = entry.get("drug", "")
        disease = entry.get("disease", "")
        nodes = entry.get("nodes", [])
        edges = entry.get("links", []) or entry.get("edges", [])
        results: List[RetrievalResult] = []

        # Direct drug-disease relationship
        if drug and disease and len(results) < limit:
            results.append(RetrievalResult(
                source_entity=drug,
                source_type="drug",
                target_entity=disease,
                target_type="disease",
                relationship="treats",
                weight=1.0,
                source="DRUGMECHDB",
                skill_category="drug_mechanism",
                evidence_text=f"DrugMechDB: {drug} treats {disease} (curated MoA path)",
                sources=[entry.get("reference", "")],
            ))

        # Individual MoA path edges
        node_map = {n.get("id", ""): n.get("label", n.get("name", ""))
                    for n in nodes if isinstance(n, dict)}
        for edge in edges:
            if len(results) >= limit:
                break
            if isinstance(edge, dict):
                src_id = edge.get("source", edge.get("from", ""))
                tgt_id = edge.get("target", edge.get("to", ""))
                rel = edge.get("key", edge.get("label", "related_to"))
            else:
                continue
            src_name = node_map.get(str(src_id), str(src_id))
            tgt_name = node_map.get(str(tgt_id), str(tgt_id))
            if not src_name or not tgt_name:
                continue
            results.append(RetrievalResult(
                source_entity=src_name,
                source_type="entity",
                target_entity=tgt_name,
                target_type="entity",
                relationship=str(rel).lower().replace(" ", "_"),
                weight=1.0,
                source="DRUGMECHDB",
                skill_category="drug_mechanism",
                evidence_text=f"DrugMechDB MoA path: {src_name} → {rel} → {tgt_name}",
                metadata={"drug": drug, "disease": disease},
            ))
        return results
