---
name: hi-c-3d-genomics
description: Workflow for Hi-C and related 3D genomics analyses including compartments, loops, TADs, differential contacts, and visualization.
tool_type: python
primary_tool: Hi-C
---

# Hi-C And 3D Genomics

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `Hi-C` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for Hi-C and related 3D genomics analyses including compartments, loops, TADs, differential contacts, and visualization.

## When To Use This Skill

- use when the task is Hi-C matrix analysis or 3D genome interpretation
- use when loops, compartments, or TADs must be called or compared
- use when contact-map figures or feature-level summaries are required

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

- Hi-C contact pairs or matrices
- genome bins
- condition metadata

## Expected Outputs

- compartments
- loops and TADs
- contact maps and differential summaries

## Preferred Tools

- Hi-C processing utilities
- numpy
- pandas
- matplotlib

## Starter Pattern

```text
Preferred starting point: Hi-C
Inputs: Hi-C contact pairs or matrices, genome bins, condition metadata
Outputs: compartments, loops and TADs, contact maps and differential summaries
```

## Workflow

### 1. Validate matrix resolution

Choose a resolution supported by coverage and the biological question.

### 2. Normalize contact structure

Apply appropriate normalization before calling global or local features.

### 3. Call 3D features

Infer compartments, TADs, or loops with methods matched to the resolution and assay.

### 4. Compare conditions carefully

Quantify differences only where coverage and normalization support fair comparison.

### 5. Produce readable maps

Export heatmaps and feature tables with clear genome coordinates and labels.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `compartments`
- `loops and TADs`
- `contact maps and differential summaries`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Check assay-specific QC such as enrichment quality, coverage behavior, or replicate consistency.
- Verify genome build, interval coordinates, and annotation compatibility.

## Anti-Patterns

- interpreting noisy low-coverage matrices at overly fine resolution
- comparing raw contacts without normalization
- mixing feature scales without stating the resolution

## Related Skills

- `ATAC Seq`
- `ChIP Seq`
- `Methylation Analysis`
- `Epitranscriptomics`

## Optional Supplements

- None required for the first pass.
