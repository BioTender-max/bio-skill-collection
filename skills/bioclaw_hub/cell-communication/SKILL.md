---
name: cell-communication
description: Workflow for ligand-receptor communication inference in single-cell or spatial data with sender-receiver summaries and cautious interpretation.
tool_type: python
primary_tool: pandas
---

# Cell Communication

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `pandas` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for ligand-receptor communication inference in single-cell or spatial data with sender-receiver summaries and cautious interpretation.

## When To Use This Skill

- use when the task is cell-cell communication or ligand-receptor analysis
- use when the dataset already has reasonable cell type annotations or spatial neighborhoods
- use when the user needs network, heatmap, or pathway-style communication outputs

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

- annotated single-cell or spatial object
- ligand-receptor resource
- group or condition metadata

## Expected Outputs

- interaction tables
- sender-receiver summaries
- communication visualizations

## Preferred Tools

- pandas
- networkx
- seaborn
- matplotlib

## Starter Pattern

```text
Preferred starting point: pandas
Inputs: annotated single-cell or spatial object, ligand-receptor resource, group or condition metadata
Outputs: interaction tables, sender-receiver summaries, communication visualizations
```

## Workflow

### 1. Confirm annotation quality

Communication analysis depends on robust cell labels or spatial domains.

### 2. Define comparison units

Choose whether to infer communication across clusters, cell types, neighborhoods, or conditions.

### 3. Run interaction scoring

Compute ligand-receptor evidence and apply filtering for expression support and redundancy.

### 4. Aggregate to interpretable views

Summarize signals by sender, receiver, pathway, or condition.

### 5. Report caveats

State clearly that inferred communication is hypothesis-generating unless validated experimentally.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `interaction tables`
- `sender-receiver summaries`
- `communication visualizations`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Review embeddings together with QC metrics and batch structure before labeling biology.
- Preserve the processed object with metadata and embeddings for downstream reuse.

## Anti-Patterns

- running communication analysis on unstable or weak annotations
- equating expression correlation with validated signaling
- reporting dense uninterpretable networks without summarization

## Related Skills

- `scRNA Preprocessing And Clustering`
- `Cell Annotation`
- `Trajectory And Lineage`
- `Multiome And scATAC`

## Optional Supplements

- `string-database`
