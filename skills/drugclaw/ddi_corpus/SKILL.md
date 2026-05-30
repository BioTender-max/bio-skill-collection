# DDI Corpus 2013 – Drug-Drug Interaction Query Skill

## Overview

| Field | Value |
|-------|-------|
| **Resource** | DDI Corpus 2013 |
| **Category** | Drug-centric / Drug NLP & Text Mining |
| **Source** | [GitHub](https://github.com/isegura/DDICorpus) |
| **Paper** | [Herrero-Zazo et al., 2013](https://www.sciencedirect.com/science/article/pii/S1532046413001123) |
| **Corpus Size** | ~2,740 unique entities, ~5,000 annotated DDI pairs |
| **Sources** | DrugBank descriptions + MEDLINE abstracts |

The DDI Corpus 2013 is the standard benchmark for drug-drug interaction (DDI) extraction from biomedical text. Each XML file contains sentences with annotated drug entities and pairwise DDI labels.

**DDI Types:**
- `mechanism` – pharmacokinetic mechanism described (e.g., altered absorption/metabolism)
- `effect` – clinical effect of the interaction (e.g., increased bleeding risk)
- `advise` – recommendation or warning about co-administration
- `int` – stated interaction without further detail

**Entity Types:** `drug`, `group`, `brand`, `drug_n` (active substance not approved for human use)

## Setup

**1. Download & extract** (one-time):

```bash
git clone https://github.com/isegura/DDICorpus.git
cd DDICorpus
unzip DDICorpus-2013.zip
```

**2. Set the corpus path** in `30_DDI_Corpus_2013.py`:

```python
CORPUS_ROOT = "/path/to/DDICorpus-master"  # contains DDICorpus/Train/ and DDICorpus/Test/
```

Or pass `--root` at runtime or set env var `DDI_CORPUS_ROOT`.

## Usage

### Python API

```python
from 30_DDI_Corpus_2013 import query_entities, list_all_entities, corpus_stats

# Query a single drug
result = query_entities("aspirin")

# Query multiple drugs at once
result = query_entities(["warfarin", "metformin", "digoxin"])

# List all entity names in the corpus
names = list_all_entities()

# Get corpus-level statistics
stats = corpus_stats()
```

### CLI (直接运行)

```bash
python 30_DDI_Corpus_2013.py
```

直接运行即输出 demo 结果（corpus 统计 → 单实体查询 → 批量查询 → 未找到示例）。
修改 `__main__` 块中的实体名即可自定义查询。

## Output Format

`query_entities` returns a JSON string. Each element:

```json
{
  "query": "aspirin",
  "found": true,
  "canonical_names": ["ASPIRIN", "Aspirin", "aspirin"],
  "entity_types": ["brand", "drug"],
  "total_interactions": 65,
  "interactions": [
    {
      "partner": "ketoprofen",
      "ddi_type": "mechanism",
      "sentence": "concurrent administration of aspirin decreased ketoprofen protein binding...",
      "source": "Train/DrugBank"
    }
  ],
  "example_sentences": ["..."]
}
```

If an entity is not found: `{"query": "xyz", "found": false}`.

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `entities` | *(required)* | `str` or `list[str]` — drug names to look up (case-insensitive) |
| `corpus_root` | `CORPUS_ROOT` | Path to the extracted DDICorpus-master directory |
| `max_interactions` | `20` | Maximum interaction records returned per entity |
| `max_sentences` | `5` | Maximum example sentences returned per entity |

## Dependencies

Python 3.10+ standard library only (`xml.etree.ElementTree`, `json`, `os`, `collections`). No third-party packages required.
