---
name: pathway-analysis
description: Workflow for enrichment testing, ranked-gene analysis, pathway scoring, and pathway-focused visualization across omics outputs.
tool_type: python
primary_tool: Reactome
---

# Pathway Analysis

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `Reactome` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for enrichment testing, ranked-gene analysis, pathway scoring, and pathway-focused visualization across omics outputs.

## When To Use This Skill

- use when the task is pathway enrichment or gene set interpretation
- use when the user has gene lists, ranked statistics, or pathway-scored samples
- use when Reactome, KEGG, GO, or similar resources are part of the deliverable

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

- gene lists or ranked statistics
- pathway databases
- optional sample-level matrices

## Expected Outputs

- enriched pathway tables
- pathway plots
- pathway interpretation summaries

## Preferred Tools

- Reactome and STRING resources
- pandas
- matplotlib
- seaborn

## Starter Pattern

```text
Preferred starting point: Reactome
Inputs: gene lists or ranked statistics, pathway databases, optional sample-level matrices
Outputs: enriched pathway tables, pathway plots, pathway interpretation summaries
```

## Workflow

### 1. Choose enrichment mode

Use over-representation for filtered gene lists and ranked methods for full signed statistics.

### 2. Match identifiers

Standardize gene IDs to the pathway database before testing.

### 3. Run enrichment and summarize

Report effect direction, significance, and pathway sizes.

### 4. Visualize selectively

Use dot plots, bar plots, or network summaries without overwhelming the reader.

### 5. Export pathway-ready tables

Save standardized pathway identifiers, scores, and member genes.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `enriched pathway tables`
- `pathway plots`
- `pathway interpretation summaries`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Verify that modalities, samples, and model assumptions align before integration or inference.
- Export factors, scores, or model outputs together with interpretation context.

## Anti-Patterns

- mixing identifier systems without conversion
- treating pathway databases as interchangeable without stating the source
- showing only p-values without effect direction or gene overlap context

## Related Skills

- `Multi-Omics Integration`
- `Systems Biology`
- `Causal Genomics`
- `Machine Learning For Omics`

## Optional Supplements

- `reactome-database`
- `string-database`
