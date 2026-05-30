---
name: knowledge-graph-builder
description: "Use this skill when users need to build, populate, or extend a domain-specific knowledge graph from literature and structured databases. Triggers include: 'build knowledge graph', 'extract claims from papers', 'ingest data into graph', 'batch extract claims', 'knowledge graph construction', 'populate graph from PubMed', 'extract structured claims', 'ingest atlas data', or any request involving knowledge graph population from scientific literature or biomedical databases. Covers both structured data ingestion (Phase 1) and LLM-based claim extraction from papers (Phase 2)."
license: MIT License (NeuroClaw custom skill – freely modifiable within the project)
layer: base
skill_type: tool
dependencies:
  - multi-search-engine
  - academic-research-hub
---
# Knowledge Graph Builder

## Overview

This skill provides a reusable framework for constructing domain-specific knowledge graphs by combining two complementary data pipelines:

- **Phase 1 — Structured Ingestion**: Import concepts and relations from curated databases, ontologies, and brain atlases (e.g., NeuroNames, MeSH, DisGeNET, Cognitive Atlas, Nilearn atlases).
- **Phase 2 — Literature Claim Extraction**: Use LLMs to extract structured scientific claims from PubMed paper abstracts, then resolve entities and ingest into the graph.
- **Phase 3 — Hypothesis Engine**: Traverse the graph to find novel connections, contradictions, and unexplored gaps — turning raw claims into testable research hypotheses.

The output is a directed knowledge graph (NetworkX DiGraph + JSON serialization) where nodes represent domain concepts and claims, and edges represent typed relationships with confidence scores and provenance.

**Primary implementation**: `neurooracle/` in the NeuroClaw project.

## Architecture

```
                    ┌─────────────────────┐
                    │  Knowledge Graph     │
                    │  (NetworkX DiGraph)  │
                    └──────┬──────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
┌────────▼────────┐ ┌─────▼──────────┐ ┌────▼─────────────┐
│  Phase 1:       │ │  Phase 2:      │ │  Phase 3:        │
│  Structured     │ │  Literature    │ │  Hypothesis      │
│  Data Ingestion │ │  Claim Extract │ │  Engine          │
└────────┬────────┘ └──────┬─────────┘ └────┬─────────────┘
         │                 │                 │
┌────────▼────────┐ ┌──────▼─────────┐ ┌────▼─────────────┐
│ - NeuroNames    │ │ - PubMed search│ │ - Path finding   │
│ - MeSH          │ │ - LLM extract  │ │ - Bridge discover│
│ - DisGeNET      │ │ - Entity resol │ │ - Contradictions │
│ - Cognitive Atl │ │ - Claim ingest │ │ - Gap detection  │
│ - Nilearn atlas │ │                │ │ - Ranking        │
└─────────────────┘ └────────────────┘ └──────────────────┘
```

## Key Design Decisions (Lessons Learned)

### 1. Schema Design: Three-Tier Nodes

The graph uses three types of nodes, all stored in the same DiGraph:

| Node Type | ID Format | Purpose |
|-----------|-----------|---------|
| **ConceptNode** | `NN:1234`, `CUI:xxx`, `MESH:D0001` | Domain concepts (brain regions, diseases, genes, drugs) |
| **Claim** | `CLM:abc123def456` | Structured scientific claims extracted from papers |
| **Edge** | (implicit) | Typed relationships between any two nodes |

**Why this matters**: Claims are stored as nodes (not just edges) so they can carry full metadata (evidence, p-value, sample size, conditions, population). Simplified edges are also generated for fast traversal.

### 2. Entity Resolution: 5-Level Matching

When ingesting claims, entity names must be resolved to existing concept IDs. Use a cascading strategy:

1. **Exact match** on preferred_name
2. **Case-insensitive** match
3. **Alias match** (check synonyms)
4. **Substring match** (entity contained in name or vice versa, prefer shortest name)
5. **Create new** concept if no match found

**Why not just use embeddings?** For small-to-medium graphs (<100K concepts), string matching is fast and predictable. SapBERT/FAISS alignment is recommended when UMLS is available and the graph exceeds 100K concepts.

### 3. LLM Extraction: Keep Prompts Short

LLMs (especially via proxy endpoints) return empty responses when prompts + expected output exceed the token window. Hard-won rules:

- **Truncate abstracts** to 2000 chars before sending to LLM
- **Keep extraction prompts concise** — list field names and allowed values, not verbose descriptions
- **Use `max_tokens=8192`** — 4096 is too small for papers with many claims
- **Fix `[[` double brackets** — a common LLM error when outputting JSON arrays
- **Temperature=0.1** for extraction consistency

### 4. Contextualized Triplets (MDKG-style)

Beyond simple (subject, predicate, object), extract:

- **Conditions**: list of conditions under which the claim holds (e.g., `["female only", "age > 65"]`)
- **Population**: study demographics (mean_age, gender distribution, sample size, cohort name)

This enables more nuanced graph queries and downstream hypothesis generation.

### 5. Checkpoint/Resume for Batch Jobs

Large-scale extraction (10 diseases x 27 years x 20 papers = 5400 papers) takes 10-60 hours. Always implement:

- Save checkpoint after each batch (disease+year)
- Track completed_diseases and completed_years
- Save graph periodically (every 5 years or after each disease)
- CSV export of paper metadata for audit trail

## Quick Reference

| Task | Command |
|------|---------|
| Ingest atlas data (Phase 1) | `python -m neurooracle.ingest_pipeline` |
| Generate brain atlas TSV | `python neurooracle/data/raw/generate_brain_atlas_nilearn.py` |
| Run single-disease extraction | `python -m neurooracle.batch_extract --diseases "Alzheimer's disease" --year-start 2024 --year-end 2024 --papers-per-year 5` |
| Run full batch extraction | `python -m neurooracle.batch_extract` |
| Resume from checkpoint | `python -m neurooracle.batch_extract` (auto-resumes) |
| Start fresh (ignore checkpoint) | `python -m neurooracle.batch_extract --no-resume` |
| Verbose logging | `python -m neurooracle.batch_extract -v` |
| Query graph stats | `python -c "from neurooracle import load_graph; g = load_graph(); print(g.stats())"` |
| **Batch generate hypotheses** | `python -m neurooracle.hypothesis_cli batch --output data/hypotheses.json` |
| **Rank saved hypotheses** | `python -m neurooracle.hypothesis_cli rank --input data/hypotheses.json --top 20` |
| Find hypothesis paths | `python -m neurooracle.hypothesis_cli paths "hippocampus" "Alzheimer Disease"` |
| Bridge discovery | `python -m neurooracle.hypothesis_cli bridge "hippocampus" --target-domain disease` |
| **Discover from concept** | `python -m neurooracle.hypothesis_cli discover "Alzheimer" --max-hops 3` |
| **Find trending evidence** | `python -m neurooracle.hypothesis_cli trending --since 2020 --direction strengthening` |
| Find contradictions | `python -m neurooracle.hypothesis_cli contradictions` |
| Detect gaps | `python -m neurooracle.hypothesis_cli gaps --domain-a neuroanatomy --domain-b disease` |
| Explore a concept | `python -m neurooracle.hypothesis_cli explore "hippocampus"` |

## Agent Reference Rule

When the agent needs knowledge graph implementation code, it should first consult the curated snippets in `skills/knowledge-graph-builder/scripts/` instead of writing from scratch.

Reference snippets available:
- `scripts/entity_resolution.py` → EntityResolver class with 5-level matching
- `scripts/graph_query.py` → CLI tool for graph queries (stats, search, neighbors, paths, domain)
- `scripts/hypothesis_cli_reference.py` → Hypothesis engine usage patterns (executable code in `neurooracle/hypothesis_cli.py`)
- `scripts/extraction_prompt_template.txt` → LLM extraction prompt template
- `scripts/new_data_source_template.py` → Template for adding new data sources

## Installation

```bash
# Core dependencies
pip install networkx requests openai

# Optional: for atlas generation
pip install nilearn nibabel

# Optional: for Biopython Entrez (PubMed)
pip install biopython

# Use the neuroclaw conda environment
conda activate neuroclaw
```

## Phase 1: Structured Data Ingestion

### Supported Data Sources

| Source | Data Type | Entity Type | Edge Type |
|--------|-----------|-------------|-----------|
| NeuroNames / Nilearn atlases | Brain region hierarchy | neuroanatomy | part_of |
| MeSH (desc*.xml) | Medical subject headings | disease, anatomy | is_a |
| DisGeNET (TSV) | Gene-disease associations | gene | gene_associated_with_disease |
| Cognitive Atlas (API) | Tasks, concepts, disorders | cognitive_function, paradigm | — |
| UMLS (pending) | Unified medical language system | all types | various |

### Adding a New Data Source

Create a new file in `neurooracle/ingestion/` following this pattern:

```python
"""Ingest data from [SOURCE] into the knowledge graph."""

from ..schema import ConceptNode, Edge, DomainTag
from ..graph_manager import KnowledgeGraph

def ingest_source(kg: KnowledgeGraph, data_path: str) -> dict:
    """Parse source data and add to graph.

    Returns summary dict with counts.
    """
    concepts_added = 0
    edges_added = 0

    # 1. Parse raw data
    records = parse_data(data_path)

    # 2. Create ConceptNodes
    for record in records:
        node = ConceptNode(
            id=record["id"],
            preferred_name=record["name"],
            domain_tags=[DomainTag.DISEASE.value],
            source_vocab="my_source",
            aliases=record.get("synonyms", []),
        )
        kg.add_concept(node)
        concepts_added += 1

    # 3. Create Edges (if hierarchical)
    for record in records:
        if record.get("parent_id"):
            edge = Edge(
                source_id=record["id"],
                target_id=record["parent_id"],
                relation_type="is_a",
                source="my_source",
            )
            kg.add_edge(edge)
            edges_added += 1

    return {"concepts_added": concepts_added, "edges_added": edges_added}
```

### Atlas Generation (Nilearn)

Use `scripts/generate_atlas.py` as a template for generating brain region hierarchies from Nilearn built-in atlases. Key points:

- Start with a manual hierarchy of core brain regions (~100-200)
- Augment with atlas labels (Talairach, Harvard-Oxford, AAL, Dosenbach, Pauli, Seitzman)
- Handle SSL issues by patching `requests.Session.verify` before Nilearn calls
- Output: TSV with columns: NN_ID, Name, Latin_Name, Synonyms, Parent_ID, Brodmann_area

## Phase 2: Literature Claim Extraction

### Pipeline: PubMed Search → LLM Extraction → Entity Resolution → Ingestion

```
PubMed query → PMIDs → XML parse → (abstract, PaperRef)
                                         │
                                    LLM extraction
                                         │
                                  [Claim objects]
                                         │
                                  Entity resolution
                                         │
                              Graph ingestion (nodes + edges)
```

### PubMed Search Strategy

For each disease+year combination, search with neuroimaging focus:

```
({disease}[Title/Abstract])
AND ("brain imaging"[Title/Abstract] OR "neuroimaging"[Title/Abstract]
     OR "MRI"[Title/Abstract] OR "fMRI"[Title/Abstract] OR "PET"[Title/Abstract])
AND {year}:{year}[pdat]
```

Rate limit: 0.4s between NCBI API calls (3 req/sec without API key).

### LLM Extraction Prompt Design

See `scripts/extraction_prompt_template.txt` for the recommended prompt structure. Key fields to extract:

| Field | Description |
|-------|-------------|
| subject / object | Entity names |
| subject_type / object_type | Entity category (brain_region, disease, gene, ...) |
| predicate | Relationship type (reduces, increases, correlates_with, ...) |
| negated | Whether the claim states NO relationship |
| effect_metric / effect_size | Statistical effect (Cohen's d, r, OR, ...) |
| p_value | Statistical significance |
| sample_size | Study sample size |
| study_type | fMRI, PET, GWAS, meta_analysis, ... |
| conditions | List of contextual conditions |
| population | Study demographics |
| raw_sentence | Source sentence from abstract |

### Entity Resolution During Ingestion

When a claim references "hippocampus" and the graph already has `NN:11` (preferred_name="Hippocampus"), the entity resolver matches them. If no match is found, a new concept node is created with prefix `CLM_CONCEPT:`.

This means the graph grows organically: atlas data provides the backbone, and claim extraction fills in relationships and discovers new entities.

### Claim Node vs. Simplified Edge

Each claim generates **three** graph elements:

1. **Claim node** (`CLM:abc123`): full metadata (evidence, conditions, population, raw text)
2. **Simplified edge** (subject → object): for fast multi-hop traversal
3. **About edges** (claim → subject, claim → object): for provenance queries

## Output Files

| File | Description |
|------|-------------|
| `data/knowledge_graph.json` | Full graph (concepts + edges + metadata) |
| `data/papers_metadata.csv` | Paper records: pmid, doi, title, authors, year, journal, disease, abstract_length, n_claims, timestamp |
| `data/batch_checkpoint.json` | Resume checkpoint: completed_diseases, completed_years, totals |

## Complementary / Related Skills

- `academic-research-hub` → paper search (arXiv, PubMed, Semantic Scholar)
- `research-idea` → consumes knowledge graph for hypothesis generation
- `method-design` → uses graph structure for method comparison

## Reference

- MDKG paper: Gao et al., "Large language model powered knowledge graph construction for mental health exploration." Nature Communications (2025). PMID: 40804250
- NeuroNames: Brain region hierarchy
- MeSH: Medical Subject Headings (NLM)
- DisGeNET: Gene-disease association database
- Cognitive Atlas: Cognitive paradigm ontology
- Nilearn: Python brain atlas library

## Phase 3: Hypothesis Engine

The hypothesis engine **batch-generates** hypotheses across the entire graph, **persists** them to JSON, and **ranks** by novelty, evidence, testability, and confidence. See `neurooracle/hypothesis_engine.py` for the implementation.

### Workflow

```
batch_generate() → save_hypotheses() → rank_hypotheses() → (Phase 5: convert to analysis tasks)
```

### Capabilities

| Function | Description |
|----------|-------------|
| `batch_generate()` | Traverse entire graph, generate hypotheses across all domain pairs |
| `save_hypotheses()` / `load_hypotheses()` | Persist to JSON for iterative re-ranking |
| `rank_hypotheses()` | Sort by composite score (4 dimensions) |
| `find_paths(src, tgt)` | Interactive: multi-hop path finding |
| `bridge_discovery(concept, domain)` | Interactive: cross-domain connection discovery |
| `discover_hypotheses(concept)` | Find hypotheses radiating from a single concept to all reachable domains |
| `find_trending(since_year, direction)` | Find concept pairs with strengthening/weakening evidence over time |
| `contradiction_detection()` | Find opposing claims on same concept pair |
| `gap_detection(domain_a, domain_b)` | Find 2-hop concept pairs with no direct edge |

### Scoring (4 Dimensions)

Each hypothesis is scored on four dimensions:

| Dimension | Weight | What it measures |
|-----------|--------|------------------|
| **Confidence** | 0.25 | Edge confidence × study type quality × replicability |
| **Novelty** | 0.25 | Cross-domain paths, rare relations, few supporting papers |
| **Evidence** | 0.25 | p-value strength, sample size, effect size presence |
| **Testability** | 0.25 | Can NeuroClaw execute this? Modality detection (sMRI, EEG, fMRI, PET, DTI), brain region specificity |

Composite ranking: `confidence^0.25 * evidence^0.25 * novelty^0.25 * testability^0.25`

### Default Domain Pairs

The batch generator explores these cross-domain pairs:
- neuroanatomy ↔ disease
- neuroanatomy ↔ cognitive_function
- disease ↔ gene
- disease ↔ drug
- disease ↔ biomarker
- gene ↔ disease
- drug ↔ disease
- cognitive_function ↔ disease
- neurotransmitter ↔ disease

## Future Work

- **SapBERT entity alignment** with UMLS (cosine similarity > 0.9)
- **LLM-based hypothesis summarization** — use LLM to generate natural language hypothesis descriptions
- **Result feedback loop**: validated hypotheses write back to graph
- ~~**Temporal analysis**~~: implemented as `find_trending()` — tracks strengthening/weakening evidence trends across publication years

---
Created At: 2026-05-04 20:28 HKT
Last Updated At: 2026-05-06 14:46 HKT
Author: chengwang96
