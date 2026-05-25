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
name: biomni-research-agent
description: Bio-Research Generalist
license: MIT
metadata:
  author: Stanford (Snap Lab)
  source: "https://github.com/snap-stanford/Biomni"
  version: "1.0.0"
compatibility:
  - system: Python 3.9+
allowed-tools:
  - run_shell_command
  - web_fetch
  - python_repl
keywords:
  - biomni
  - automation
  - biomedical
  - reasoning
  - tools
measurable_outcome: Execute complex research tasks with >95% success rate and validated tool usage.
---

# Biomni (General Biomedical Agent)

A general-purpose biomedical AI agent capable of executing complex research workflows using over 150 tools and databases.

Biomni is a "General-Purpose" biomedical agent. Unlike specialized skills (e.g., just for folding proteins), Biomni acts as a high-level orchestrator that can break down complex open-ended research questions into solvable sub-tasks using a vast library of tools.

## When to Use This Skill

*   **Complex Questions**: "What are the potential drug targets for Alzheimer's related to mitochondrial dysfunction?"
*   **Multi-Step Research**: Tasks requiring literature search, data retrieval, and analysis in sequence.
*   **Exploratory Analysis**: When the exact path to the answer isn't known and requires "reasoning."

## Core Capabilities

1.  **Tool Use**: Access to 150+ tools, 105 software packages, and 59 databases.
2.  **Hypothesis Generation**: Can formulate scientific hypotheses and plan experiments to test them.
3.  **Plan & Execute**: Breaks down queries into a dependency graph of tasks.
4.  **Database QA**: High accuracy (74.4%) in querying biomedical databases.

## Workflow

1.  **Query Parsing**: The agent analyzes the user's natural language request.
2.  **Tool Selection**: It selects relevant tools (e.g., "Search GWAS Catalog", "Run GO Enrichment", "Fetch Uniprot Data").
3.  **Execution Loop**:
    *   Step 1: Get data.
    *   Step 2: Analyze data.
    *   Step 3: Refine plan based on intermediate results.
4.  **Synthesis**: Combines all findings into a comprehensive answer.

## Example Usage

**User**: "Identify genes associated with Type 2 Diabetes that are also expressed in the pancreas and have approved drugs."

**Agent Action**:
1.  Tool: `OpenTargets` -> Get T2D associated genes.
2.  Tool: `GTEx` -> Filter for high expression in Pancreas.
3.  Tool: `DrugBank` -> Intersect with drug targets.
4.  Result: Returns a list of genes (e.g., *GLP1R*, *DPP4*) and their drugs.

<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->