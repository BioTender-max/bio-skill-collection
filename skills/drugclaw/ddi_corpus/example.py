"""
DDI Corpus 2013 – Drug-Drug Interaction Extraction NLP Benchmark
Category: Drug-centric | Type: Dataset | Subcategory: Drug NLP/Text Mining
Source: https://github.com/isegura/DDICorpus
Paper:  https://www.sciencedirect.com/science/article/pii/S1532046413001123

Provides entity-level querying over the DDI Corpus 2013 XML annotations.
Given one or more drug/entity names, returns all annotated DDI information
(interaction partners, DDI types, source sentences, entity types).
"""

import os
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from collections import defaultdict
from typing import Union

# ── Configure this path to your local DDICorpus-master root ──────────────
CORPUS_ROOT = str(
    Path(__file__).resolve().parents[3]
    / "resources_metadata"
    / "drug_nlp"
    / "DDICorpus2013"
    / "DDICorpus-master"
)


# ── Internal helpers ─────────────────────────────────────────────────────

def _xml_dirs(corpus_root: str) -> list[str]:
    """Return all XML directories (Train + Test, DrugBank + MedLine)."""
    base = os.path.join(corpus_root, "DDICorpus")
    candidates = [
        os.path.join(base, "Train", "DrugBank"),
        os.path.join(base, "Train", "MedLine"),
        os.path.join(base, "Test", "Test for DDI Extraction task", "DrugBank"),
        os.path.join(base, "Test", "Test for DDI Extraction task", "MedLine"),
    ]
    return [d for d in candidates if os.path.isdir(d)]


def _build_index(corpus_root: str) -> dict:
    """
    Parse all XML files and build a lookup index.

    Returns dict keyed by lowercase entity name:
    {
        "aspirin": {
            "canonical_names": {"Aspirin", "aspirin"},
            "entity_types": {"drug"},
            "interactions": [
                {
                    "partner": "warfarin",
                    "ddi_type": "effect",
                    "sentence": "Aspirin may increase the anticoagulant effect of warfarin.",
                    "source": "DrugBank/Train"
                }, ...
            ],
            "sentences": ["...", ...]   # all sentences mentioning this entity
        }
    }
    """
    index = defaultdict(lambda: {
        "canonical_names": set(),
        "entity_types": set(),
        "interactions": [],
        "sentences": set(),
    })

    for xml_dir in _xml_dirs(corpus_root):
        # Derive split/source label  e.g. "Train/DrugBank"
        parts = xml_dir.replace(corpus_root, "").strip(os.sep).split(os.sep)
        source_label = "/".join(p for p in parts if p not in ("DDICorpus", "Test for DDI Extraction task"))

        for fname in os.listdir(xml_dir):
            if not fname.endswith(".xml"):
                continue
            tree = ET.parse(os.path.join(xml_dir, fname))
            for sentence in tree.getroot().findall(".//sentence"):
                text = sentence.get("text", "")

                # Map entity-id → (name, type) for this sentence
                eid_map = {}
                for ent in sentence.findall("entity"):
                    ename = ent.get("text", "")
                    etype = ent.get("type", "")
                    eid_map[ent.get("id")] = (ename, etype)

                    key = ename.lower()
                    index[key]["canonical_names"].add(ename)
                    index[key]["entity_types"].add(etype)
                    index[key]["sentences"].add(text)

                # Collect positive DDI pairs
                for pair in sentence.findall("pair"):
                    if pair.get("ddi") != "true":
                        continue
                    e1_name, _ = eid_map.get(pair.get("e1"), ("?", "?"))
                    e2_name, _ = eid_map.get(pair.get("e2"), ("?", "?"))
                    ddi_type = pair.get("type", "unknown")

                    for anchor, partner in [(e1_name, e2_name), (e2_name, e1_name)]:
                        index[anchor.lower()]["interactions"].append({
                            "partner": partner,
                            "ddi_type": ddi_type,
                            "sentence": text,
                            "source": source_label,
                        })

    # Convert sets to sorted lists for JSON serialisation
    for v in index.values():
        v["canonical_names"] = sorted(v["canonical_names"])
        v["entity_types"] = sorted(v["entity_types"])
        v["sentences"] = sorted(v["sentences"])

    return dict(index)


# Module-level cache
_INDEX_CACHE: dict | None = None


def _get_index(corpus_root: str | None = None) -> dict:
    global _INDEX_CACHE
    if _INDEX_CACHE is None:
        root = corpus_root or CORPUS_ROOT
        _INDEX_CACHE = _build_index(root)
    return _INDEX_CACHE


# ── Public API ───────────────────────────────────────────────────────────

def query_entities(
    entities: Union[str, list[str]],
    corpus_root: str | None = None,
    max_interactions: int = 20,
    max_sentences: int = 5,
) -> str:
    """
    Query DDI Corpus 2013 for one or more drug/entity names.

    Args:
        entities:  A single entity name (str) or a list of names.
        corpus_root: Override the default corpus path.
        max_interactions: Cap on returned interactions per entity.
        max_sentences: Cap on returned example sentences per entity.

    Returns:
        A JSON string (LLM-readable) with results for each queried entity.
    """
    if isinstance(entities, str):
        entities = [entities]

    index = _get_index(corpus_root)
    results = []

    for name in entities:
        key = name.strip().lower()
        if key not in index:
            results.append({"query": name, "found": False})
            continue

        entry = index[key]
        # Deduplicate interactions by (partner, ddi_type)
        seen = set()
        unique_interactions = []
        for inter in entry["interactions"]:
            sig = (inter["partner"].lower(), inter["ddi_type"])
            if sig not in seen:
                seen.add(sig)
                unique_interactions.append(inter)

        results.append({
            "query": name,
            "found": True,
            "canonical_names": entry["canonical_names"],
            "entity_types": entry["entity_types"],
            "total_interactions": len(unique_interactions),
            "interactions": unique_interactions[:max_interactions],
            "example_sentences": entry["sentences"][:max_sentences],
        })

    return json.dumps(results, indent=2, ensure_ascii=False)


def list_all_entities(corpus_root: str | None = None) -> list[str]:
    """Return a sorted list of all unique entity names in the corpus."""
    index = _get_index(corpus_root)
    return sorted(index.keys())


def corpus_stats(corpus_root: str | None = None) -> str:
    """Return high-level corpus statistics as JSON."""
    index = _get_index(corpus_root)
    total_entities = len(index)
    entities_with_ddi = sum(1 for v in index.values() if v["interactions"])
    all_types = set()
    total_pairs = 0
    for v in index.values():
        for inter in v["interactions"]:
            all_types.add(inter["ddi_type"])
            total_pairs += 1
    return json.dumps({
        "total_unique_entities": total_entities,
        "entities_with_interactions": entities_with_ddi,
        "total_interaction_records": total_pairs // 2,  # each pair counted twice
        "ddi_types": sorted(all_types),
    }, indent=2)


# ── Demo ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # 1. Corpus-level statistics
    print("=== Corpus Statistics ===")
    print(corpus_stats())

    # 2. Query a single entity
    print("\n=== Single Query: aspirin ===")
    print(query_entities("aspirin"))

    # 3. Query multiple entities at once
    print("\n=== Batch Query: warfarin, metformin, digoxin ===")
    print(query_entities(["warfarin", "metformin", "digoxin"]))

    # 4. Entity not found
    print("\n=== Not Found: some_fake_drug ===")
    print(query_entities("some_fake_drug"))
