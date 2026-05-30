# 32_ADE_Corpus

## Overview

**ADE Corpus V2** — Adverse Drug Event relation extraction dataset from annotated PubMed case reports.

| Field | Value |
|-------|-------|
| Category | Drug-centric |
| Subcategory | Drug NLP / Text Mining |
| Source | [GitHub](https://github.com/trunghlt/AdverseDrugReaction/tree/master/ADE-Corpus-V2) |
| Paper | [ACL 2016](https://aclanthology.org/C16-1084/) |
| Local Path | `resources_metadata/drug_nlp/ADECorpus/ADE-Corpus-V2` |

## Data Files

| File | Content |
|------|---------|
| `DRUG-AE.rel` | Drug ↔ Adverse Event relation pairs with source sentences |
| `DRUG-DOSE.rel` | Drug ↔ Dose relation pairs with source sentences |
| `ADE-NEG.txt` | Negative examples (sentences without adverse events) |

## Quick Start

```python
from 32_ADE_Corpus import ADECorpus  # or rename to ade_corpus

corpus = ADECorpus()

# Single entity
print(corpus.query("aspirin"))

# Multiple entities
print(corpus.query(["lithium", "hepatotoxicity"]))

# Corpus statistics
print(corpus.stats())
```

## Query Input / Output

### Input

`corpus.query(entities)` — accepts `str` or `list[str]`.  
Each entity is matched case-insensitively against both drug names and adverse event names.

### Output (JSON)

```json
{
  "aspirin": {
    "entity": "aspirin",
    "matched_as_drug": true,
    "matched_as_adverse_event": false,
    "total_mentions": 42,
    "adverse_events": ["bleeding", "tinnitus", "..."],
    "doses": ["100mg", "..."],
    "related_drugs": null,
    "pubmed_ids": ["12345678", "..."],
    "sample_sentences": ["A 65-year-old patient developed ..."]
  }
}
```

| Field | Description |
|-------|-------------|
| `matched_as_drug` | Entity found as a drug name |
| `matched_as_adverse_event` | Entity found as an adverse event name |
| `total_mentions` | Total matching records |
| `adverse_events` | List of associated adverse events (when matched as drug) |
| `doses` | List of associated doses (when matched as drug) |
| `related_drugs` | List of drugs causing this event (when matched as AE) |
| `pubmed_ids` | Up to 10 source PubMed IDs |
| `sample_sentences` | Up to 3 example sentences |

## Notes

- All matching is **case-insensitive**.
- `query()` returns a **JSON string** directly consumable by LLMs.
- `stats()` returns corpus-level counts (total relations, unique drugs/AEs).
- No external dependencies — stdlib only (`os`, `json`, `collections`).
