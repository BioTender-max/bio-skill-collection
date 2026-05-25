---
name: multi-omics-integration
description: Workflow for integrating matched or partially matched omics layers into shared latent structure and cross-modal interpretation.
tool_type: python
primary_tool: MOFA+-style
---

# Multi-Omics Integration

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `MOFA+-style` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for integrating matched or partially matched omics layers into shared latent structure and cross-modal interpretation.

## When To Use This Skill

- use when the task is multi-omics factor discovery or integrated cohort analysis
- use when the user has two or more omics modalities that should be related jointly
- use when cross-modal factors or harmonized sample structure are needed

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

- multiple omics matrices
- sample metadata
- feature mapping resources

## Expected Outputs

- integrated latent factors
- cross-modal associations
- integrated visualizations

## Preferred Tools

- MOFA+-style approaches
- mixOmics-style approaches
- pandas
- numpy

## Starter Pattern

```text
Preferred starting point: MOFA+-style
Inputs: multiple omics matrices, sample metadata, feature mapping resources
Outputs: integrated latent factors, cross-modal associations, integrated visualizations
```

## Workflow

### 1. Check sample and feature alignment

Confirm which samples are shared and how features relate across modalities.

### 2. Normalize per modality

Handle each omics layer according to its data-generating properties before integration.

### 3. Choose integration model

Use a factor-based or correlation-based method matched to the question and data structure.

### 4. Interpret latent factors

Link integrated components back to biology, covariates, and modality-specific loadings.

### 5. Export separated artifacts

Save factors, loadings, and modality-aware summaries.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `integrated latent factors`
- `cross-modal associations`
- `integrated visualizations`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Verify that modalities, samples, and model assumptions align before integration or inference.
- Export factors, scores, or model outputs together with interpretation context.

## Anti-Patterns

- forcing direct feature comparability across unrelated omics types
- ignoring modality-specific QC before integration
- reporting latent factors without biological interpretation or covariate review

## Related Skills

- `Pathway Analysis`
- `Systems Biology`
- `Causal Genomics`
- `Machine Learning For Omics`

## Optional Supplements

- `reactome-database`
- `string-database`
