"""
ADE Corpus V2 - Adverse Drug Event Query Tool
Category: Drug-centric | Type: Dataset | Subcategory: Drug NLP/Text Mining
Source: https://github.com/trunghlt/AdverseDrugReaction/tree/master/ADE-Corpus-V2
Paper: https://aclanthology.org/C16-1084/

Query interface for the ADE Corpus v2. Accepts one or more entity names
(drug or adverse event) and returns all related annotations.
"""

import os
import json
from pathlib import Path
from collections import defaultdict
from typing import Union

# === CONFIGURE THIS PATH ===
DATA_DIR = str(
    Path(__file__).resolve().parents[3]
    / "resources_metadata"
    / "drug_nlp"
    / "ADECorpus"
    / "ADE-Corpus-V2"
)


def _load_drug_ae(data_dir: str) -> list[dict]:
    """Parse DRUG-AE.rel into structured records."""
    path = os.path.join(data_dir, "DRUG-AE.rel")
    records = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            parts = [p.strip() for p in line.strip().split("|")]
            if len(parts) >= 8:
                records.append({
                    "pubmed_id": parts[0],
                    "sentence": parts[1],
                    "adverse_event": parts[4],
                    "drug": parts[7],
                    "source": "DRUG-AE.rel",
                })
    return records


def _load_drug_dose(data_dir: str) -> list[dict]:
    """Parse DRUG-DOSE.rel into structured records."""
    path = os.path.join(data_dir, "DRUG-DOSE.rel")
    if not os.path.exists(path):
        return []
    records = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            parts = [p.strip() for p in line.strip().split("|")]
            if len(parts) >= 8:
                records.append({
                    "pubmed_id": parts[0],
                    "sentence": parts[1],
                    "dose": parts[4],
                    "drug": parts[7],
                    "source": "DRUG-DOSE.rel",
                })
    return records


def _load_neg(data_dir: str) -> list[dict]:
    """Parse ADE-NEG.txt (negative examples without ADE)."""
    path = os.path.join(data_dir, "ADE-NEG.txt")
    if not os.path.exists(path):
        return []
    records = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            parts = [p.strip() for p in line.strip().split("|")]
            if len(parts) >= 2:
                records.append({
                    "pubmed_id": parts[0] if parts[0] != "NEG" else "",
                    "sentence": parts[1],
                    "label": "no_ade",
                    "source": "ADE-NEG.txt",
                })
    return records


def _build_index(ae_records, dose_records):
    """Build case-insensitive lookup indexes for drugs and adverse events."""
    drug_idx = defaultdict(list)
    ae_idx = defaultdict(list)
    for r in ae_records:
        drug_idx[r["drug"].lower()].append(r)
        ae_idx[r["adverse_event"].lower()].append(r)
    for r in dose_records:
        drug_idx[r["drug"].lower()].append(r)
    return drug_idx, ae_idx


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

class ADECorpus:
    """
    Queryable wrapper for ADE Corpus V2.

    Usage:
        corpus = ADECorpus()
        result = corpus.query("aspirin")
        result = corpus.query(["aspirin", "hepatotoxicity"])
    """

    def __init__(self, data_dir: str = DATA_DIR):
        self.ae_records = _load_drug_ae(data_dir)
        self.dose_records = _load_drug_dose(data_dir)
        self.drug_idx, self.ae_idx = _build_index(self.ae_records, self.dose_records)

    def query(self, entities: Union[str, list[str]]) -> str:
        """
        Query by one or more entity names (drug or adverse event).
        Returns a JSON string ready for LLM consumption.
        """
        if isinstance(entities, str):
            entities = [entities]
        results = {}
        for entity in entities:
            results[entity] = self._query_single(entity)
        return json.dumps(results, indent=2, ensure_ascii=False)

    def _query_single(self, entity: str) -> dict:
        key = entity.lower()
        drug_hits = self.drug_idx.get(key, [])
        ae_hits = self.ae_idx.get(key, [])

        # Deduplicate adverse events and doses for this drug
        adverse_events = sorted({r["adverse_event"] for r in drug_hits if "adverse_event" in r})
        doses = sorted({r["dose"] for r in drug_hits if "dose" in r})
        related_drugs = sorted({r["drug"] for r in ae_hits})

        # Collect unique PubMed IDs
        all_hits = drug_hits + ae_hits
        pubmed_ids = sorted({r["pubmed_id"] for r in all_hits if r.get("pubmed_id")})

        # Sample sentences (max 3)
        seen = set()
        sample_sentences = []
        for r in all_hits:
            s = r["sentence"]
            if s not in seen:
                seen.add(s)
                sample_sentences.append(s)
            if len(sample_sentences) >= 3:
                break

        return {
            "entity": entity,
            "matched_as_drug": len(drug_hits) > 0,
            "matched_as_adverse_event": len(ae_hits) > 0,
            "total_mentions": len(all_hits),
            "adverse_events": adverse_events if adverse_events else None,
            "doses": doses if doses else None,
            "related_drugs": related_drugs if related_drugs else None,
            "pubmed_ids": pubmed_ids[:10],
            "sample_sentences": sample_sentences,
        }

    def stats(self) -> str:
        """Return corpus-level statistics as JSON."""
        return json.dumps({
            "drug_ae_relations": len(self.ae_records),
            "drug_dose_relations": len(self.dose_records),
            "unique_drugs": len(self.drug_idx),
            "unique_adverse_events": len(self.ae_idx),
        }, indent=2)


# ---------------------------------------------------------------------------
# Usage example
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    corpus = ADECorpus()
    print("=== Corpus Stats ===")
    print(corpus.stats())

    # Single entity query
    print("\n=== Query: aspirin ===")
    print(corpus.query("aspirin"))

    # Multi-entity query
    print("\n=== Query: [lithium, hepatotoxicity] ===")
    print(corpus.query(["lithium", "hepatotoxicity"]))
