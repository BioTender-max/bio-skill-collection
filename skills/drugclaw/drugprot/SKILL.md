# 31_DrugProt — Drug-Protein Relation Query

## Overview

Query drug/chemical and gene/protein entities in the **BioCreative VII DrugProt** dataset. Returns annotated relations (e.g., INHIBITOR, ACTIVATOR, SUBSTRATE) between chemicals and genes/proteins from biomedical literature.

- **Source**: <https://zenodo.org/records/5119892>
- **Paper**: <https://pmc.ncbi.nlm.nih.gov/articles/PMC10683943/>
- **Coverage**: 15,000 PubMed abstracts (3,500 training + 750 development + 10,750 test-background), 13 relation types

## Data Location

```
DrugClaw/
├── skills/drug_nlp/drugprot/
│   └── example.py                  ← helper script
└── resources_metadata/drug_nlp/DrugProt/
    └── drugprot-gs-training-development/
        ├── training/
        │   ├── drugprot_training_abstracs.tsv
        │   ├── drugprot_training_entities.tsv
        │   └── drugprot_training_relations.tsv
        ├── development/
        │   ├── drugprot_development_abstracs.tsv
        │   ├── drugprot_development_entities.tsv
        │   └── drugprot_development_relations.tsv
        └── test-background/
            ├── test_background_abstracts.tsv
            └── test_background_entities.tsv
```

Use the repo-local `resources_metadata/drug_nlp/DrugProt/drugprot-gs-training-development` path, or override it with the `DRUGPROT_DIR` environment variable if your dataset lives elsewhere.

All three splits are loaded by default. Note: `test-background` has no relations file (relations are the prediction target).

## Quick Start

```python
from importlib.util import spec_from_file_location, module_from_spec

# Load module
spec = spec_from_file_location("drugprot", "/path/to/skills/drug_nlp/drugprot/example.py")
dp = module_from_spec(spec)
spec.loader.exec_module(dp)

# Load dataset (one-time, ~2 s)
ds = dp.load_dataset("/path/to/drugprot-gs-training-development")

# Query single entity
results = dp.query_entities(ds, "aspirin")
print(dp.format_results(results))

# Query multiple entities
results = dp.query_entities(ds, ["metformin", "insulin", "EGFR"])
print(dp.format_results(results))
```

## API

### `load_dataset(base_dir, splits=["training","development","test-background"]) -> dict`

Loads and indexes all TSV files. Returns a dict with keys: `abstracts`, `entities`, `relations`, `name_index`.

### `query_entities(dataset, names, case_sensitive=False) -> list[dict]`

| Parameter | Type | Description |
|---|---|---|
| `dataset` | `dict` | Output of `load_dataset()` |
| `names` | `str` or `list[str]` | Entity name(s) to query |
| `case_sensitive` | `bool` | Default `False`; falls back to substring match if exact match fails |

**Returns** a list of result dicts, one per query name:

```json
[
  {
    "query": "aspirin",
    "matches": [
      {
        "pmid": "12345678",
        "entity_id": "T3",
        "entity_type": "CHEMICAL",
        "entity_text": "aspirin",
        "relations": [
          {
            "relation_type": "INHIBITOR",
            "partner_id": "T12",
            "partner_text": "COX-2",
            "partner_type": "GENE-Y",
            "role": "arg1(chemical)"
          }
        ],
        "article_title": "Effects of aspirin on ..."
      }
    ]
  }
]
```

### `format_results(results, max_matches=5) -> str`

Formats query results into a concise, LLM-readable plain-text summary.

## Relation Types

| Type | Description |
|---|---|
| INHIBITOR | Chemical inhibits gene/protein |
| ACTIVATOR | Chemical activates gene/protein |
| AGONIST | Chemical is an agonist |
| ANTAGONIST | Chemical is an antagonist |
| SUBSTRATE | Chemical is a substrate |
| PRODUCT-OF | Chemical is a product of enzyme |
| INDIRECT-DOWNREGULATOR | Chemical indirectly downregulates |
| INDIRECT-UPREGULATOR | Chemical indirectly upregulates |
| DIRECT-REGULATOR | Chemical directly regulates |
| PART-OF | Chemical is part of protein complex |
| COFACTOR | Chemical acts as cofactor |
| NOT | Negative relation |
| UNDEFINED | Undefined relation |

## CLI Usage

```bash
export DRUGPROT_DIR=/path/to/drugprot-gs-training-development
python 31_DrugProt.py aspirin insulin p53
```
