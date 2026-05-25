---
name: imaging-mass-cytometry
description: Workflow for multiplexed imaging or IMC segmentation, phenotyping, and spatial summarization.
tool_type: python
primary_tool: image
---

# Imaging Mass Cytometry

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `image` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for multiplexed imaging or IMC segmentation, phenotyping, and spatial summarization.

## When To Use This Skill

- use when the task is imaging mass cytometry or related multiplexed tissue imaging
- use when segmentation, cell phenotyping, and spatial summaries are needed
- use when the deliverable includes cell-level features plus tissue-level maps

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

- marker images
- panel metadata
- segmentation masks or raw images

## Expected Outputs

- cell-level feature tables
- phenotype assignments
- spatial plots

## Preferred Tools

- image analysis utilities
- pandas
- numpy
- matplotlib

## Starter Pattern

```text
Preferred starting point: image
Inputs: marker images, panel metadata, segmentation masks or raw images
Outputs: cell-level feature tables, phenotype assignments, spatial plots
```

## Workflow

### 1. Validate panel and images

Confirm marker-channel mapping, image integrity, and segmentation assets.

### 2. Segment and quantify cells

Produce cell-level intensities and morphological features.

### 3. Phenotype cells

Assign cell states using marker panels and thresholding or clustering logic.

### 4. Summarize spatial organization

Compute neighborhood or region-level patterns when the question requires them.

### 5. Export image-linked outputs

Save cell tables, masks, and visualization overlays.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `cell-level feature tables`
- `phenotype assignments`
- `spatial plots`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Check missingness, batch effects, and identification or annotation confidence before differential interpretation.
- Keep feature-level and summarized entity-level outputs distinct.

## Anti-Patterns

- using poorly validated segmentation as if it were exact
- hiding threshold assumptions in phenotype calls
- reporting only heatmaps without spatial context

## Related Skills

- `Proteomics`
- `Metabolomics`
- `Structural Biology`

## Optional Supplements

- None required for the first pass.
