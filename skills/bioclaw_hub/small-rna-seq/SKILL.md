---
name: small-rna-seq
description: Workflow for small RNA and miRNA preprocessing, quantification, differential analysis, and target-oriented interpretation.
tool_type: mixed
primary_tool: miRge3
---

# Small RNA Seq

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `miRge3` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for small RNA and miRNA preprocessing, quantification, differential analysis, and target-oriented interpretation.

## When To Use This Skill

- use when the user has miRNA or other small RNA sequencing data
- use when adapter-heavy preprocessing and short-read-specific QC are required
- use when the goal is differential miRNA analysis or target prediction follow-up

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

- small RNA FASTQ files
- adapter sequences
- reference miRNA annotations

## Expected Outputs

- small RNA count matrix
- differential miRNA tables
- target candidate summaries

## Preferred Tools

- miRge3
- miRDeep2-style workflows
- pandas
- seaborn

## Starter Pattern

```text
Preferred starting point: miRge3
Inputs: small RNA FASTQ files, adapter sequences, reference miRNA annotations
Outputs: small RNA count matrix, differential miRNA tables, target candidate summaries
```

## Workflow

### 1. Handle short inserts carefully

Trim adapters and confirm read-length distributions before quantification.

### 2. Quantify annotated species

Map or assign reads to miRNAs and other small RNA classes with class-aware counting.

### 3. Perform count-aware comparisons

Use replicate-aware statistics for differential abundance.

### 4. Review library composition

Inspect proportions of miRNA, tRNA fragments, rRNA fragments, and other classes.

### 5. Prepare interpretation outputs

Export mature miRNA results and optional target-prediction inputs.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `small RNA count matrix`
- `differential miRNA tables`
- `target candidate summaries`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Check replicate structure, outlier samples, and whether counts versus normalized values are being mixed.
- Export ranked or contrast-aware tables when downstream enrichment is likely.

## Anti-Patterns

- treating adapter-trimmed and untrimmed samples as comparable
- ignoring multi-mapping behavior for short RNAs
- reporting targets without clarifying they are predictions

## Related Skills

- `Bulk RNA Expression`
- `RNA Quantification`
- `Differential Expression`
- `Alternative Splicing`

## Optional Supplements

- None required for the first pass.
