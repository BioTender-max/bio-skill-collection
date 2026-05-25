---
name: read-qc
description: Workflow for sequencing read QC, trimming, contamination screening, and pre-alignment cleanup.
tool_type: python
primary_tool: fastp
---

# Read QC

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `fastp` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for sequencing read QC, trimming, contamination screening, and pre-alignment cleanup.

## When To Use This Skill

- use when the task is FASTQ quality assessment or cleanup before analysis
- use when the user needs trimming, contamination review, or read-level reports
- use when downstream pipelines depend on deciding whether data quality is acceptable

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

- raw FASTQ files
- adapter sequences
- optional sequencing metadata

## Expected Outputs

- QC reports
- filtered or trimmed reads
- contamination summaries

## Preferred Tools

- fastp
- FastQC-style reports
- pandas
- matplotlib

## Starter Pattern

```text
Preferred starting point: fastp
Inputs: raw FASTQ files, adapter sequences, optional sequencing metadata
Outputs: QC reports, filtered or trimmed reads, contamination summaries
```

## Workflow

### 1. Profile raw reads

Inspect quality scores, adapter content, duplication, and GC behavior before trimming.

### 2. Trim or filter judiciously

Apply adapter removal and quality filtering with settings matched to the assay.

### 3. Screen contamination

Check for host, ribosomal, or other unwanted content if the study design calls for it.

### 4. Re-evaluate after cleanup

Confirm that trimming improved quality without over-truncating useful reads.

### 5. Export both reports and cleaned reads

Keep raw and cleaned QC records for reproducibility.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `QC reports`
- `filtered or trimmed reads`
- `contamination summaries`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Validate file structure and metadata before handing outputs to downstream tools.
- Retain provenance for every conversion, query, or pipeline execution step.

## Anti-Patterns

- trimming aggressively without checking length distributions afterward
- assuming all contamination is removable without assay-specific review
- running downstream analysis on reads that failed basic QC without documenting it

## Related Skills

- `Sequence And Format IO`
- `Alignment And Mapping`
- `Database Access`
- `Reporting And Figure Export`

## Optional Supplements

- None required for the first pass.
