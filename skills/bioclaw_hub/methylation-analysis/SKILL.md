---
name: methylation-analysis
description: Workflow for methylation alignment or calling, DMR analysis, methylation QC, and locus-level interpretation.
tool_type: mixed
primary_tool: Bismark-like
---

# Methylation Analysis

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `Bismark-like` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for methylation alignment or calling, DMR analysis, methylation QC, and locus-level interpretation.

## When To Use This Skill

- use when the task is DNA methylation calling or differential methylation
- use when bisulfite or long-read methylation data must be summarized at loci or regions
- use when methylation QC and DMR export are required

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

- methylation-aware sequencing reads
- reference genome
- sample metadata

## Expected Outputs

- methylation calls
- DMR tables
- sample and locus QC plots

## Preferred Tools

- Bismark-like workflows
- pandas
- matplotlib
- seaborn

## Starter Pattern

```text
Preferred starting point: Bismark-like
Inputs: methylation-aware sequencing reads, reference genome, sample metadata
Outputs: methylation calls, DMR tables, sample and locus QC plots
```

## Workflow

### 1. Check assay-specific preprocessing

Use the correct alignment or calling path for bisulfite versus direct methylation detection.

### 2. Summarize methylation levels

Aggregate calls at CpG, region, or feature level appropriate to the study question.

### 3. Run differential analysis

Test differences using replicate-aware region-based methods when possible.

### 4. Inspect biological context

Annotate DMRs to promoters, enhancers, or other regions before interpretation.

### 5. Export report-ready outputs

Save calls, DMR tables, and locus-level example plots.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `methylation calls`
- `DMR tables`
- `sample and locus QC plots`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Check assay-specific QC such as enrichment quality, coverage behavior, or replicate consistency.
- Verify genome build, interval coordinates, and annotation compatibility.

## Anti-Patterns

- mixing assay types without documenting the calling method
- reporting regional changes without effect direction and coverage context
- ignoring low-coverage loci during interpretation

## Related Skills

- `ATAC Seq`
- `ChIP Seq`
- `Epitranscriptomics`
- `Hi-C And 3D Genomics`

## Optional Supplements

- None required for the first pass.
