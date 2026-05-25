---
name: machine-learning-for-omics
description: Workflow for predictive modeling, biomarker discovery, survival modeling, and explainability over omics-derived features.
tool_type: python
primary_tool: scikit-learn
---

# Machine Learning For Omics

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `scikit-learn` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for predictive modeling, biomarker discovery, survival modeling, and explainability over omics-derived features.

## When To Use This Skill

- use when the task is supervised learning on omics features
- use when the user needs a model, validation metrics, and interpretable feature importance
- use when the modeling objective is biomarker discovery, classification, regression, or survival prediction

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

- feature matrix
- labels or outcomes
- split or validation design

## Expected Outputs

- trained model
- validation metrics
- feature importance or explanation summaries

## Preferred Tools

- scikit-learn
- statsmodels
- survival tooling where needed
- shap when appropriate

## Starter Pattern

```text
Preferred starting point: scikit-learn
Inputs: feature matrix, labels or outcomes, split or validation design
Outputs: trained model, validation metrics, feature importance or explanation summaries
```

## Workflow

### 1. Define the prediction task

Clarify outcome type, class balance, leakage risks, and validation plan.

### 2. Build a reproducible split

Use train-validation-test or cross-validation schemes that respect cohort structure.

### 3. Train parsimonious models first

Start with robust baseline models before complex architectures.

### 4. Evaluate honestly

Report calibration, held-out performance, and failure modes instead of only one metric.

### 5. Explain cautiously

Use importance or explanation methods as interpretation aids, not proof of causality.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `trained model`
- `validation metrics`
- `feature importance or explanation summaries`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Verify that modalities, samples, and model assumptions align before integration or inference.
- Export factors, scores, or model outputs together with interpretation context.

## Anti-Patterns

- leakage across train and test sets
- high-dimensional modeling without strong regularization or validation
- presenting feature importance as mechanistic causality

## Related Skills

- `Multi-Omics Integration`
- `Pathway Analysis`
- `Systems Biology`
- `Causal Genomics`

## Optional Supplements

- `scikit-learn`
- `statsmodels`
