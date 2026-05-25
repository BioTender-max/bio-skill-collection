---
name: microbiome-amplicon
description: Workflow for amplicon microbiome analysis including denoising, taxonomy assignment, diversity analysis, and differential abundance.
tool_type: mixed
primary_tool: QIIME2-style
---

# Microbiome Amplicon

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `QIIME2-style` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for amplicon microbiome analysis including denoising, taxonomy assignment, diversity analysis, and differential abundance.

## When To Use This Skill

- use when the task is 16S, ITS, or other amplicon-based microbiome profiling
- use when denoising, taxonomy assignment, and diversity metrics are required
- use when the user needs cohort-level differential abundance or community structure summaries

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

- amplicon FASTQ files
- sample metadata
- taxonomy database

## Expected Outputs

- ASV or OTU tables
- taxonomy assignments
- diversity and differential abundance summaries

## Preferred Tools

- QIIME2-style workflows
- pandas
- scikit-bio
- seaborn

## Starter Pattern

```text
Preferred starting point: QIIME2-style
Inputs: amplicon FASTQ files, sample metadata, taxonomy database
Outputs: ASV or OTU tables, taxonomy assignments, diversity and differential abundance summaries
```

## Workflow

### 1. Preprocess reads

Trim primers or adapters and denoise reads into ASVs or OTUs.

### 2. Assign taxonomy

Use a suitable taxonomy model or reference database for the marker type.

### 3. Compute diversity

Calculate alpha and beta diversity with metadata-aware comparisons.

### 4. Compare groups

Run differential abundance with methods matched to compositional data constraints.

### 5. Export community reports

Save tables, ordinations, and taxonomy summaries.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `ASV or OTU tables`
- `taxonomy assignments`
- `diversity and differential abundance summaries`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Review sample contamination, depth differences, and database choice before comparing communities.
- State clearly whether outputs are relative abundance, counts, or derived functions.

## Anti-Patterns

- treating relative abundance changes as absolute shifts without context
- using a taxonomy database mismatched to the marker region
- running differential abundance without accounting for compositional effects

## Related Skills

- `Metagenomics`
- `Pathogen Epidemiological Genomics`
- `Phylogenetics`

## Optional Supplements

- `scikit-bio`
