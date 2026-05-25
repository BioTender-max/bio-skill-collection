---
name: phasing-imputation
description: Workflow for haplotype phasing, genotype imputation, reference-panel matching, and imputation QC.
tool_type: python
primary_tool: phasing
---

# Phasing And Imputation

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `phasing` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for haplotype phasing, genotype imputation, reference-panel matching, and imputation QC.

## When To Use This Skill

- use when the task is genotype phasing or imputation from array or sequence-derived variant data
- use when the study requires haplotypes, imputed markers, or downstream association-ready genotypes
- use when reference panel choice and QC are central to the analysis

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

- VCF genotype data
- sample metadata
- reference panel

## Expected Outputs

- phased genotypes
- imputed genotype set
- imputation QC metrics

## Preferred Tools

- phasing tools
- imputation tools
- bcftools
- pandas

## Starter Pattern

```text
Preferred starting point: phasing
Inputs: VCF genotype data, sample metadata, reference panel
Outputs: phased genotypes, imputed genotype set, imputation QC metrics
```

## Workflow

### 1. Validate cohort and reference compatibility

Choose a reference panel matched to ancestry and build.

### 2. Phase genotypes

Produce haplotype-aware inputs appropriate for the imputation engine.

### 3. Impute variants

Run imputation and retain quality metrics such as INFO or dosage confidence.

### 4. Filter post-imputation

Apply frequency and quality thresholds aligned with the downstream use case.

### 5. Export association-ready outputs

Save phased or imputed VCFs and QC summaries.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `phased genotypes`
- `imputed genotype set`
- `imputation QC metrics`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Record reference build, caller assumptions, and filtering rules in the final outputs.
- Separate raw calls from filtered or interpreted results.

## Anti-Patterns

- using a poorly matched reference panel without documenting the limitation
- keeping low-confidence imputed sites as if they were observed genotypes
- forgetting genome build harmonization

## Related Skills

- `Variant Calling`
- `Copy Number`
- `Long-Read Genomics`
- `Genome Assembly`

## Optional Supplements

- None required for the first pass.
