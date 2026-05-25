---
name: reporting-and-figure-export
description: Workflow for packaging analysis outputs into reproducible reports, clean tables, and publication-ready figure exports.
tool_type: python
primary_tool: matplotlib
---

# Reporting And Figure Export

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `matplotlib` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for packaging analysis outputs into reproducible reports, clean tables, and publication-ready figure exports.

## When To Use This Skill

- use when the task is to turn analysis outputs into a clear report or deliverable
- use when plots and tables must be exported in publication- or presentation-ready form
- use when a notebook, Quarto report, or figure bundle is needed

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

- analysis tables
- plots
- metadata
- interpretation notes

## Expected Outputs

- QC or analysis reports
- exported figures
- deliverable-ready tables

## Preferred Tools

- matplotlib
- seaborn
- Quarto-style or notebook reporting
- pandas

## Starter Pattern

```text
Preferred starting point: matplotlib
Inputs: analysis tables, plots, metadata, interpretation notes
Outputs: QC or analysis reports, exported figures, deliverable-ready tables
```

## Workflow

### 1. Separate raw outputs from presentation outputs

Keep the analysis artifacts intact and build curated exports on top.

### 2. Standardize figure formatting

Use consistent fonts, labels, color legends, and vector output when possible.

### 3. Assemble compact reports

Summarize key methods, QC, main findings, and file provenance.

### 4. Export tables cleanly

Write machine-readable and human-readable result tables with stable column names.

### 5. Preserve reproducibility

Record how the report and figures were generated.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `QC or analysis reports`
- `exported figures`
- `deliverable-ready tables`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Validate file structure and metadata before handing outputs to downstream tools.
- Retain provenance for every conversion, query, or pipeline execution step.

## Anti-Patterns

- copy-pasting plots without recording how they were made
- using unreadable legends, tiny fonts, or raster-only outputs when vector is possible
- mixing exploratory and final figures without labeling them

## Related Skills

- `Sequence And Format IO`
- `Alignment And Mapping`
- `Read QC`
- `Database Access`

## Optional Supplements

- `seaborn`
- `plotly`
