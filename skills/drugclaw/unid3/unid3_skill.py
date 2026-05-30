"""
UniD3Skill — UniD3 Multi-KG Drug Discovery Knowledge Graph.

Subcategory : drug_knowledgebase (Drug Knowledgebase)
Access mode : LOCAL_FILE (GraphML files)
Source      : https://github.com/QSong-github/UniD3

UniD3 integrates 150 000+ PubMed articles into a multi-KG covering
drug-disease matching, drug effectiveness, and drug-target analysis.

Config keys
-----------
graphml_paths : dict   {graph_name: path_to_graphml_file}
               e.g. {'UniD3_Level1_DDM': '/data/UniD3_L1T1.graphml', ...}
"""
from __future__ import annotations

import logging
import os
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Tuple

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)



class UniD3Skill(RAGSkill):
    """
    UniD3 drug discovery knowledge graph.

    Supports multiple graph files (L1/L2, DDM/DEA/DTA variants).
    """

    name = "UniD3"
    subcategory = "drug_knowledgebase"
    resource_type = "KG"
    access_mode = AccessMode.LOCAL_FILE
    aim = "Drug discovery knowledge graph"
    data_range = "Multi-KG + drug-disease datasets from 150 000+ PubMed articles"
    _implemented = True

    # Key → (description, entity types)
    GRAPH_TYPES = {
        "UniD3_Level1_DDM": ("Drug-Disease Matching L1", "drug", "disease"),
        "UniD3_Level1_DEA": ("Drug Effectiveness Assessment L1", "drug", "effect"),
        "UniD3_Level1_DTA": ("Drug-Target Analysis L1", "drug", "target"),
        "UniD3_Level2_DDM": ("Drug-Disease Matching L2", "drug", "disease"),
        "UniD3_Level2_DEA": ("Drug Effectiveness Assessment L2", "drug", "effect"),
        "UniD3_Level2_DTA": ("Drug-Target Analysis L2", "drug", "target"),
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._graphs: Dict[str, List[Tuple]] = {}  # name -> [(src, rel, tgt, src_type, tgt_type)]
        self._name_index: Dict[str, List[Tuple]] = {}
        self._loaded = False

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        self._loaded = True
        # paths: Dict[str, str] = self.config.get("graphml_paths", {}) or {}
        paths: Dict[str, str] = self.config or {}
        # print(f"UniD3: loading graphs from config paths: {paths}")
        for gname, gpath in paths.items():
            if not gpath or not os.path.exists(gpath):
                logger.debug("UniD3: graph '%s' path not found: %s", gname, gpath)
                continue
            triplets = self._parse_graphml(gpath, gname)
            # print(f"UniD3: loaded {len(triplets)} triplets from {gname}")
            self._graphs[gname] = triplets
            logger.info("UniD3: loaded %d triplets from %s", len(triplets), gname)

        # Build name index
        for gname, triplets in self._graphs.items():
            for src, rel, tgt, stype, ttype in triplets:
                if src not in self._name_index:
                    self._name_index[src.lower()] = []
                self._name_index[src.lower()].append(
                    (src, rel, tgt, stype, ttype, gname)
                )

    def _parse_graphml(self, path: str, gname: str) -> List[Tuple]:
        try:
            tree = ET.parse(path)
            root = tree.getroot()
        except Exception as exc:
            logger.error("UniD3: cannot parse %s — %s", path, exc)
            return []

        # 动态提取命名空间，兼容不同 GraphML 文件
        ns_match = root.tag  # e.g. "{http://graphml.graphdrawing.org/xmlns}graphml"
        ns = ""
        if ns_match.startswith("{"):
            ns = ns_match[:ns_match.index("}") + 1]  # "{http://...}"

        _, src_type, tgt_type = self.GRAPH_TYPES.get(gname, (gname, "drug", "entity"))

        # 收集 node id → {key: value} 映射
        # 同时解析 key definitions
        key_defs: Dict[str, str] = {}  # key id → attr.name
        for key_elem in root.iter(f"{ns}key"):
            kid = key_elem.get("id", "")
            attr_name = key_elem.get("attr.name", "")
            key_defs[kid] = attr_name

        nodes: Dict[str, Dict[str, str]] = {}
        for node in root.iter(f"{ns}node"):
            nid = node.get("id", "").strip('"')
            data_map: Dict[str, str] = {}
            for data in node.iter(f"{ns}data"):
                key_id = data.get("key", "")
                attr_name = key_defs.get(key_id, key_id)
                data_map[attr_name] = (data.text or "").strip('"')
            nodes[nid] = data_map

        # 收集边
        triplets: List[Tuple] = []
        for edge in root.iter(f"{ns}edge"):
            src_id = edge.get("source", "").strip('"')
            tgt_id = edge.get("target", "").strip('"')
            src = src_id
            tgt = tgt_id
            rel = "related_to"
            for data in edge.iter(f"{ns}data"):
                key_id = data.get("key", "")
                attr_name = key_defs.get(key_id, key_id)
                if attr_name == "description" and data.text:
                    rel = data.text.strip('"')

            # 用 entity_type 覆盖默认类型
            actual_src_type = nodes.get(src, {}).get("entity_type", src_type)
            actual_tgt_type = nodes.get(tgt, {}).get("entity_type", tgt_type)
            triplets.append((src, rel, tgt, actual_src_type, actual_tgt_type))

        return triplets

    def is_available(self) -> bool:
        return self._implemented

    def retrieve(
        self,
        entities: Dict[str, List[str]],
        query: str = "",
        max_results: int = 50,
        **kwargs: Any,
    ) -> List[RetrievalResult]:
        self._ensure_loaded()
        results: List[RetrievalResult] = []
        all_names = [n.lower() for names in entities.values() for n in names]

        for name_lower in all_names:
            for entry in self._name_index.get(name_lower, []):
                if len(results) >= max_results:
                    break
                src, rel, tgt, stype, ttype, gname = entry
                results.append(RetrievalResult(
                    source_entity=src,
                    source_type=stype,
                    target_entity=tgt,
                    target_type=ttype,
                    relationship=rel.lower().replace(" ", "_").replace("-", "_"),
                    weight=1.0,
                    source="UniD3",
                    skill_category="drug_knowledgebase",
                    evidence_text=f"UniD3 ({gname}): {src} → {tgt}",
                    metadata={"graph": gname},
                ))
        return results
