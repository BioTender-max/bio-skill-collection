---
name: metabolomics
description: Workflow for untargeted or targeted metabolomics including preprocessing, normalization, annotation, statistics, and pathway mapping.
tool_type: mixed
primary_tool: MS-DIAL/XCMS
---

# Metabolomics

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `MS-DIAL/XCMS` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for untargeted or targeted metabolomics including preprocessing, normalization, annotation, statistics, and pathway mapping.

## When To Use This Skill

- use when the task is LC-MS or GC-MS metabolomics
- use when the user needs feature tables, annotation, differential analysis, or pathway mapping
- use when targeted and untargeted workflows must be kept conceptually separate

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

- metabolomics raw files
- sample metadata
- annotation databases

## Expected Outputs

- feature tables
- annotated metabolites
- statistical and pathway summaries

## Preferred Tools

- XCMS-like preprocessing
- MS-DIAL-style workflows
- pandas
- seaborn

## Starter Pattern

```python
import pandas as pd

feature_df = pd.read_csv("feature_table.csv")
sample_cols = [c for c in feature_df.columns if c.startswith("sample_")]
matrix = feature_df[sample_cols]
```

## Workflow

### 1. Choose targeted or untargeted path

Treat identification certainty, normalization, and comparisons differently by assay type.

### 2. Preprocess raw signals

Perform peak detection, alignment, feature grouping, and QC filtering.

### 3. Normalize and annotate

Apply batch-aware normalization and attach annotation confidence levels.

### 4. Run statistics and interpretation

Test condition effects and map metabolites to pathways when biologically justified.

### 5. Export layered results

Keep raw features, annotated metabolites, and pathway outputs in separate tables.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `feature tables`
- `annotated metabolites`
- `statistical and pathway summaries`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Check missingness, batch effects, and identification or annotation confidence before differential interpretation.
- Keep feature-level and summarized entity-level outputs distinct.

## Anti-Patterns

- overstating metabolite identity when annotation confidence is weak
- mixing targeted concentrations with untargeted relative abundances without stating it
- skipping QC samples and batch review

## Related Skills

- `Proteomics`
- `Imaging Mass Cytometry`
- `Structural Biology`

## Optional Supplements

- `metabolomics-workbench-database`
