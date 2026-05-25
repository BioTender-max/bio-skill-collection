<!--
# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

-->

---
name: kragen-knowledge-graph
description: Graph-RAG Solver
keywords:
  - knowledge-graph
  - RAG
  - reasoning
  - graph-of-thoughts
  - biomedical-qa
measurable_outcome: Return a reasoning path and an answer supported by ≥3 knowledge graph nodes for complex biomedical questions with <5s latency.
license: MIT
metadata:
  author: Bioinformatics Oxford
  version: "1.0.0"
compatibility:
  - system: Python 3.9+
allowed-tools:
  - run_shell_command
  - web_fetch
---

# KRAGEN (Knowledge Graph Enhanced RAG)

A knowledge graph-enhanced Retrieval-Augmented Generation system for biomedical problem solving, using Graph-of-Thoughts (GoT) reasoning.

## When to Use

*   **Complex Reasoning**: Questions requiring multi-hop deduction (e.g., "How does gene A influence disease B via protein C?").
*   **Hypothesis Verification**: Checking if a proposed mechanism is supported by existing knowledge graphs.
*   **Literature Synthesis**: Combining facts from structured DBs and unstructured text.

## Core Capabilities

1.  **Graph Retrieval**: Query biomedical knowledge graphs (e.g., PrimeKG, SPOKE).
2.  **Graph-of-Thoughts**: structured reasoning over retrieved nodes.
3.  **Vector DB Integration**: Combines graph data with vector embeddings for hybrid search.

## Workflow

1.  **Input**: Natural language question.
2.  **Retrieval**: Fetch relevant sub-graph and similar text chunks.
3.  **Reasoning**: LLM traverses the graph to find connecting paths.
4.  **Answer**: Generate response with citation of graph nodes.

## Example Usage

**User**: "Explain the mechanism connecting BRCA1 mutations to ovarian cancer."

**Agent Action**:
```bash
python -m kragen.solve --question "BRCA1 mutations to ovarian cancer mechanism"
```


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->