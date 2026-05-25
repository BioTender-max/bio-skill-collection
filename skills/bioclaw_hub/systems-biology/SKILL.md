---
name: systems-biology
description: Workflow for constraint-based metabolic modeling, context-specific models, gene essentiality, and systems-level interpretation.
tool_type: python
primary_tool: cobrapy
---

# Systems Biology

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `cobrapy` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for constraint-based metabolic modeling, context-specific models, gene essentiality, and systems-level interpretation.

## When To Use This Skill

- use when the task is flux balance analysis, metabolic reconstruction, or model-based systems biology
- use when transcriptomic or metabolomic data must be folded into pathway or network models
- use when the user needs model-derived pathway behavior rather than only enrichment analysis

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

- metabolic model
- omics-derived constraints
- reaction and metabolite annotations

## Expected Outputs

- flux solutions
- context-specific models
- pathway or essentiality summaries

## Preferred Tools

- cobrapy
- pandas
- network utilities

## Starter Pattern

```python
import cobra

model = cobra.io.read_sbml_model("model.xml")
solution = model.optimize()
print(solution.objective_value)
```

## Workflow

### 1. Validate the model

Check model format, reaction constraints, and biomass assumptions before analysis.

### 2. Integrate context

Incorporate condition- or tissue-specific evidence when the task calls for it.

### 3. Run systems analysis

Perform flux analysis, essentiality testing, or pathway-level model interrogation.

### 4. Interpret model outputs

Relate flux shifts or essential reactions back to the biological question.

### 5. Export model-derived summaries

Save flux tables, condition comparisons, and pathway views.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `flux solutions`
- `context-specific models`
- `pathway or essentiality summaries`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Verify that modalities, samples, and model assumptions align before integration or inference.
- Export factors, scores, or model outputs together with interpretation context.

## Anti-Patterns

- treating model predictions as direct measurements
- skipping feasibility checks before comparing conditions
- mixing curated and auto-generated models without documenting it

## Related Skills

- `Multi-Omics Integration`
- `Pathway Analysis`
- `Causal Genomics`
- `Machine Learning For Omics`

## Optional Supplements

- `cobrapy`
