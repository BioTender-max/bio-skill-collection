---
name: copy-number
description: Workflow for copy-number estimation, segmentation, annotation, and visualization in sequencing-based assays.
tool_type: mixed
primary_tool: CNVkit-style
---

# Copy Number

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `CNVkit-style` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for copy-number estimation, segmentation, annotation, and visualization in sequencing-based assays.

## When To Use This Skill

- use when the task is CNV calling or copy-number visualization
- use when coverage-based segment inference is needed for tumor or cohort samples
- use when the user needs gene-level CNV summaries or segment plots

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

- coverage or ratio data
- target bins or intervals
- sample metadata

## Expected Outputs

- CNV segments
- gene-level CNV tables
- CNV plots

## Preferred Tools

- CNVkit-style workflows
- GATK CNV-style workflows
- pandas
- matplotlib

## Starter Pattern

```text
Preferred starting point: CNVkit-style
Inputs: coverage or ratio data, target bins or intervals, sample metadata
Outputs: CNV segments, gene-level CNV tables, CNV plots
```

## Workflow

### 1. Confirm assay context

Clarify tumor-normal versus tumor-only design and target capture versus genome-wide coverage.

### 2. Generate or import coverage summaries

Build bin- or target-level signals suitable for segmentation.

### 3. Call segments

Infer copy-number segments and classify gains, losses, or focal events.

### 4. Annotate to genes and loci

Map segments to biologically relevant genes and recurrent regions.

### 5. Report with visualization

Produce chromosome-level plots and gene-centric summaries.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `CNV segments`
- `gene-level CNV tables`
- `CNV plots`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Record reference build, caller assumptions, and filtering rules in the final outputs.
- Separate raw calls from filtered or interpreted results.

## Anti-Patterns

- treating noisy ratio shifts as confident focal events without segmentation support
- ignoring tumor purity or ploidy context when it matters
- reporting copy-number calls without genome build and binning details

## Related Skills

- `Variant Calling`
- `Long-Read Genomics`
- `Genome Assembly`
- `Comparative Genomics`

## Optional Supplements

- None required for the first pass.
