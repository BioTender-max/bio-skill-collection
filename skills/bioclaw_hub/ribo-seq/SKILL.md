---
name: ribo-seq
description: Workflow for ribosome profiling, P-site aware preprocessing, periodicity checks, ORF detection, and translation efficiency analysis.
tool_type: python
primary_tool: ribo-seq
---

# Ribo Seq

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `ribo-seq` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for ribosome profiling, P-site aware preprocessing, periodicity checks, ORF detection, and translation efficiency analysis.

## When To Use This Skill

- use when the task is ribosome profiling or translation efficiency analysis
- use when matched RNA-seq is available for translation-vs-expression comparisons
- use when periodicity and P-site validation are necessary before biological claims

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

- ribo-seq reads
- optional matched RNA-seq
- transcript annotation

## Expected Outputs

- periodicity metrics
- ORF candidates
- translation efficiency summaries

## Preferred Tools

- ribo-seq preprocessing utilities
- pandas
- matplotlib

## Starter Pattern

```text
Preferred starting point: ribo-seq
Inputs: ribo-seq reads, optional matched RNA-seq, transcript annotation
Outputs: periodicity metrics, ORF candidates, translation efficiency summaries
```

## Workflow

### 1. Validate read quality and offsets

Establish read-length distributions and P-site offsets before counting footprints.

### 2. Check periodicity

Confirm expected triplet periodicity and frame enrichment.

### 3. Quantify translation signal

Compute footprint abundance at transcript or ORF level and compare with matched RNA when available.

### 4. Identify translated features

Report canonical or novel ORFs with explicit evidence criteria.

### 5. Export clear diagnostics

Save periodicity plots, TE tables, and prioritized translated features.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `periodicity metrics`
- `ORF candidates`
- `translation efficiency summaries`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Check replicate structure, outlier samples, and whether counts versus normalized values are being mixed.
- Export ranked or contrast-aware tables when downstream enrichment is likely.

## Anti-Patterns

- making translation claims without periodicity evidence
- comparing unmatched RNA and ribo data as if they were paired
- ignoring read-length-specific behavior

## Related Skills

- `Bulk RNA Expression`
- `RNA Quantification`
- `Differential Expression`
- `Alternative Splicing`

## Optional Supplements

- None required for the first pass.
