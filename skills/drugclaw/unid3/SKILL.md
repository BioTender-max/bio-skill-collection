# UniD3 - Drug Discovery Knowledge Graph

## Overview

UniD3 is a multi-knowledge-graph built from 150,000+ PubMed articles, stored as 6 GraphML files. It supports drug-disease matching, effectiveness assessment, and drug-target analysis.

- **Source**: https://github.com/QSong-github/UniD3
- **Local path**: `resources_metadata/drug_knowledgebase/UniD3`
- **Format**: GraphML (6 files, e.g. `UniD3_L1T1.graphml`)
- **Dependency**: `networkx`

## Node Schema

Each node contains:

| Field | Description |
|-------|-------------|
| `entity` | Node name (e.g. `RESPIRATORY DISEASES`) |
| `entity_type` | Type label (e.g. `DISEASE`, `DRUG`, `GENE`, `HOST`, `BIOLOGICAL PROCESS`) |
| `description` | Free-text description from PubMed articles |
| `source_id` | Chunk ID linking back to source article |

## Edge Schema

Each edge contains:

| Field | Description |
|-------|-------------|
| `source` / `target` | Connected entity names |
| `weight` | Relation strength (float) |
| `description` | Relationship description |
| `keywords` | Associated keywords |
| `source_id` | Source chunk ID |

## API Reference

### `list_graphs() → list[str]`

Return names of all 6 GraphML files.

```python
from UniD3 import list_graphs
list_graphs()
# → ["UniD3_L1T1", "UniD3_L1T2", "UniD3_L2T1", ...]
```

### `query_entities(entities, graph_names=None) → list[dict]`

Look up one or more entities by name (case-insensitive).

```python
from UniD3 import query_entities

# Single entity
query_entities("RESPIRATORY DISEASES")

# Multiple entities
query_entities(["CALVES", "INFLAMMATION MODULATION"])

# Restrict to specific graph
query_entities("CALVES", graph_names=["UniD3_L1T1"])
```

**Returns** list of dicts: `{entity, entity_type, description, source_id, graph}`

### `get_neighbors(entity, graph_names=None) → list[dict]`

Get all direct neighbors and connecting edge info for an entity.

```python
from UniD3 import get_neighbors
get_neighbors("CALVES")
```

**Returns** list of dicts: `{graph, neighbor: {entity, entity_type, description, source_id}, edge: {source, target, weight, description, keywords, source_id}}`

### `search_by_type(entity_type, graph_names=None, limit=50) → list[dict]`

Filter entities by type.

```python
from UniD3 import search_by_type
search_by_type("DISEASE", limit=10)
search_by_type("DRUG", graph_names=["UniD3_L1T1"])
```

### `search_by_keyword(keyword, graph_names=None, limit=50) → list[dict]`

Substring match over entity names and descriptions.

```python
from UniD3 import search_by_keyword
search_by_keyword("inflammation")
search_by_keyword("cancer", limit=20)
```

## Typical Workflow

```python
from UniD3 import query_entities, get_neighbors, search_by_type

# Step 1: Find a drug entity
hits = query_entities("ASPIRIN")

# Step 2: Explore its neighborhood (related diseases, targets, etc.)
neighbors = get_neighbors("ASPIRIN")

# Step 3: Filter neighbors by type
diseases = [n for n in neighbors if n["neighbor"]["entity_type"] == "DISEASE"]
```
