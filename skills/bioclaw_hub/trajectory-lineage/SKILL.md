---
name: trajectory-lineage
description: Workflow for pseudotime, lineage branching, and state-transition analysis in single-cell data.
tool_type: python
primary_tool: scanpy
---

# Trajectory And Lineage

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `scanpy` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for pseudotime, lineage branching, and state-transition analysis in single-cell data.

## When To Use This Skill

- use when the user asks for pseudotime, lineage branching, or developmental progression
- use when the single-cell object already has a coherent embedding and annotations
- use when dynamic gene programs or branch-specific markers are needed

## Quick Route

- If the input is raw or minimally processed data, start with validation and QC before any modeling.
- If the input is already processed, skip directly to the first workflow step that matches the user goal.
- If the user asks for a biological conclusion, always produce at least one QC or confidence artifact alongside the final result.


## Progressive Disclosure

- Read `references/technical_reference.md` when you need deeper tool-selection rules, environment adaptation notes, or extra validation guidance.
- Keep `SKILL.md` as the main execution path and load the reference file only when the task or failure mode needs the extra detail.


## Default Rules

- Prefer Python-first workflows unless the task explicitly requires something else.
- Keep intermediate and final outputs separated.
- Record software versions, reference builds, and key parameters when they affect interpretation.
- Favor reproducible tables and figures over one-off interactive-only outputs.

## Expected Inputs

- processed single-cell object
- cluster labels
- optional time or perturbation metadata

## Expected Outputs

- pseudotime assignments
- branch or lineage states
- dynamic gene programs

## Preferred Tools

- scanpy
- scvelo where velocity is available
- matplotlib

## Starter Pattern

```text
Preferred starting point: scanpy
Inputs: processed single-cell object, cluster labels, optional time or perturbation metadata
Outputs: pseudotime assignments, branch or lineage states, dynamic gene programs
```

## Workflow

### 1. Check topology assumptions

Ensure the embedding and cluster relationships support a trajectory-style interpretation.

### 2. Pick roots and branches carefully

Use prior biology or metadata to justify start states and branch structure.

### 3. Infer trajectories

Compute pseudotime or lineage paths and verify they align with marker trends.

### 4. Identify dynamic features

Report genes or modules that vary along pseudotime or across branches.

### 5. Visualize with context

Overlay trajectories on embeddings and summarize branch-specific biology.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `pseudotime assignments`
- `branch or lineage states`
- `dynamic gene programs`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Review embeddings together with QC metrics and batch structure before labeling biology.
- Preserve the processed object with metadata and embeddings for downstream reuse.

## Anti-Patterns

- forcing linear trajectories on clearly disconnected states
- setting roots arbitrarily without stating the assumption
- claiming lineage causality from static data alone

## Related Skills

- `scRNA Preprocessing And Clustering`
- `Cell Annotation`
- `Cell Communication`
- `Multiome And scATAC`

## Optional Supplements

- `scvelo`
