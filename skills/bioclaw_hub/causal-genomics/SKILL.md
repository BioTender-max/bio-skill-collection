---
name: causal-genomics
description: Workflow for fine-mapping, colocalization, mediation, pleiotropy analysis, and Mendelian randomization.
tool_type: mixed
primary_tool: summary-statistics
---

# Causal Genomics

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `summary-statistics` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for fine-mapping, colocalization, mediation, pleiotropy analysis, and Mendelian randomization.

## When To Use This Skill

- use when the task is causal variant, trait-to-gene, or mediation-style genomic inference
- use when GWAS and QTL summary data must be integrated
- use when the user needs statistical evidence about shared signals or directionality assumptions

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

- GWAS summary statistics
- QTL or molecular trait summary statistics
- LD reference

## Expected Outputs

- colocalization results
- credible sets
- causal evidence summaries

## Preferred Tools

- summary-statistics workflows
- pandas
- numpy

## Starter Pattern

```text
Preferred starting point: summary-statistics
Inputs: GWAS summary statistics, QTL or molecular trait summary statistics, LD reference
Outputs: colocalization results, credible sets, causal evidence summaries
```

## Workflow

### 1. Harmonize summary statistics

Align alleles, genome builds, and variant IDs before combining datasets.

### 2. Pick the causal framework

Use fine-mapping, colocalization, mediation, or MR according to the question.

### 3. Test and compare signals

Quantify shared or potentially causal effects with the required assumptions stated clearly.

### 4. Review sensitivity

Inspect heterogeneity, pleiotropy, and LD-related caveats before interpretation.

### 5. Export assumption-aware results

Save summary tables with methods, assumptions, and confidence measures.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `colocalization results`
- `credible sets`
- `causal evidence summaries`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Verify that modalities, samples, and model assumptions align before integration or inference.
- Export factors, scores, or model outputs together with interpretation context.

## Anti-Patterns

- treating statistical colocalization as definitive causal proof
- ignoring allele harmonization issues
- running MR without checking instrument quality and pleiotropy

## Related Skills

- `Multi-Omics Integration`
- `Pathway Analysis`
- `Systems Biology`
- `Machine Learning For Omics`

## Optional Supplements

- None required for the first pass.
