---
name: epitranscriptomics
description: Workflow for RNA modification analysis such as m6A peak calling, differential modification, and transcript-level visualization.
tool_type: mixed
primary_tool: peak-calling
---

# Epitranscriptomics

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `peak-calling` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for RNA modification analysis such as m6A peak calling, differential modification, and transcript-level visualization.

## When To Use This Skill

- use when the task is MeRIP-seq, direct RNA modification analysis, or differential RNA modification
- use when enriched IP and input comparisons need to be modeled carefully
- use when the user needs modification-aware plots and transcript-level context

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

- modification-enriched reads
- input reads
- transcript annotations

## Expected Outputs

- modification peaks
- differential modification results
- transcript-level plots

## Preferred Tools

- peak-calling tools
- pandas
- matplotlib

## Starter Pattern

```text
Preferred starting point: peak-calling
Inputs: modification-enriched reads, input reads, transcript annotations
Outputs: modification peaks, differential modification results, transcript-level plots
```

## Workflow

### 1. Validate assay design

Confirm IP and input matching, replicate availability, and transcript annotation consistency.

### 2. Call modification features

Detect modification-enriched regions with assay-aware models.

### 3. Compare conditions

Test differential modification while separating abundance changes from modification-specific changes where possible.

### 4. Visualize representative transcripts

Plot peaks or signal tracks over transcripts to support interpretation.

### 5. Export clearly labeled outputs

Separate modification results from standard expression results in all tables and plots.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `modification peaks`
- `differential modification results`
- `transcript-level plots`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Check assay-specific QC such as enrichment quality, coverage behavior, or replicate consistency.
- Verify genome build, interval coordinates, and annotation compatibility.

## Anti-Patterns

- equating expression shifts with modification shifts
- calling differential modification without matched inputs or replicates where possible
- overstating transcript-level resolution when the assay is region-based

## Related Skills

- `ATAC Seq`
- `ChIP Seq`
- `Methylation Analysis`
- `Hi-C And 3D Genomics`

## Optional Supplements

- None required for the first pass.
