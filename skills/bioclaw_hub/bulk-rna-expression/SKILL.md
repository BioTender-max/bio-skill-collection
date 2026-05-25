---
name: bulk-rna-expression
description: Python-first workflow for bulk RNA-seq expression intake, normalization, sample QC, and downstream-ready matrices.
tool_type: python
primary_tool: pandas
---

# Bulk RNA Expression

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `pandas` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Python-first workflow for bulk RNA-seq expression intake, normalization, sample QC, and downstream-ready matrices.

## When To Use This Skill

- use when the task is bulk RNA-seq expression profiling before or alongside differential analysis
- use when the user has count matrices, transcript abundances, or aligned RNA-seq reads and needs expression summaries
- use when sample-level QC, PCA, or normalized matrices are required

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

- count matrix
- sample metadata
- optional BAM or quantification outputs

## Expected Outputs

- normalized matrix
- sample QC plots
- PCA or clustering summaries

## Preferred Tools

- pandas
- numpy
- seaborn
- matplotlib
- scanpy for matrix utilities when appropriate

## Starter Pattern

```text
Preferred starting point: pandas
Inputs: count matrix, sample metadata, optional BAM or quantification outputs
Outputs: normalized matrix, sample QC plots, PCA or clustering summaries
```

## Workflow

### 1. Validate matrix orientation

Confirm rows and columns, unique sample IDs, and whether counts are raw integers or already normalized.

### 2. Join metadata

Check condition labels, replicate structure, batch columns, and missing covariates before analysis.

### 3. Compute sample QC

Summarize library size, detected genes, missingness, outliers, and replicate similarity.

### 4. Normalize for exploration

Apply count-aware normalization or variance stabilization appropriate to the downstream method.

### 5. Export analysis-ready data

Save normalized matrices and QC tables for DE, enrichment, or reporting.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `normalized matrix`
- `sample QC plots`
- `PCA or clustering summaries`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Check replicate structure, outlier samples, and whether counts versus normalized values are being mixed.
- Export ranked or contrast-aware tables when downstream enrichment is likely.

## Anti-Patterns

- mixing raw counts and normalized values in the same table
- running DE directly on TPM values unless the method explicitly supports it
- skipping sample metadata validation before modeling

## Related Skills

- `RNA Quantification`
- `Differential Expression`
- `Alternative Splicing`
- `Small RNA Seq`

## Optional Supplements

- `pydeseq2`
- `pysam`
