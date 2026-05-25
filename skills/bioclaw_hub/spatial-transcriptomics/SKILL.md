---
name: spatial-transcriptomics
description: Workflow for spatial transcriptomics preprocessing, domain detection, deconvolution, neighborhood analysis, and publication-ready maps.
tool_type: python
primary_tool: scanpy-like
---

# Spatial Transcriptomics

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `scanpy-like` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for spatial transcriptomics preprocessing, domain detection, deconvolution, neighborhood analysis, and publication-ready maps.

## When To Use This Skill

- use when the task is spatial transcriptomics analysis or spatially aware visualization
- use when coordinates, images, or spot-level expression are part of the dataset
- use when the user needs domains, deconvolution, or neighborhood summaries

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

- spatial expression data
- coordinates or histology images
- optional single-cell reference

## Expected Outputs

- spatial domains
- deconvolution tables
- spatial maps and neighborhood results

## Preferred Tools

- scanpy-like spatial tooling
- image analysis utilities
- matplotlib
- seaborn

## Starter Pattern

```text
Preferred starting point: scanpy-like
Inputs: spatial expression data, coordinates or histology images, optional single-cell reference
Outputs: spatial domains, deconvolution tables, spatial maps and neighborhood results
```

## Workflow

### 1. Validate spatial assets

Confirm coordinate systems, image registration, and barcode alignment where applicable.

### 2. Preprocess expression and spatial structure

Normalize expression while preserving spatial coordinates and neighborhood information.

### 3. Choose a task path

Run domain detection, deconvolution, communication, or neighborhood analysis according to the question.

### 4. Visualize spatial biology

Generate maps that preserve physical context, legends, and scale.

### 5. Export interpretable artifacts

Save spatial labels, coordinates, and figure-ready outputs.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `spatial domains`
- `deconvolution tables`
- `spatial maps and neighborhood results`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Review embeddings together with QC metrics and batch structure before labeling biology.
- Preserve the processed object with metadata and embeddings for downstream reuse.

## Anti-Patterns

- dropping coordinate integrity during preprocessing
- treating deconvolution outputs as ground truth cell counts
- using overcrowded spatial plots without readable legends

## Related Skills

- `scRNA Preprocessing And Clustering`
- `Cell Annotation`
- `Cell Communication`
- `Trajectory And Lineage`

## Optional Supplements

- `scanpy`
