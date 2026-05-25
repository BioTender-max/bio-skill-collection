---
name: multiome-scatac
description: Workflow for paired or integrated single-cell RNA and ATAC analysis with multimodal latent spaces and regulatory interpretation.
tool_type: python
primary_tool: scanpy
---

# Multiome And scATAC

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `scanpy` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for paired or integrated single-cell RNA and ATAC analysis with multimodal latent spaces and regulatory interpretation.

## When To Use This Skill

- use when the task is scATAC, multiome RNA-ATAC, or multimodal single-cell integration
- use when gene activity, motif activity, or regulatory linkage is required
- use when the user needs a joint view across modalities rather than separate analyses

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

- multiome object or paired modalities
- ATAC fragments or peak matrix
- cell metadata

## Expected Outputs

- integrated embeddings
- modality-aware clusters
- motif or regulatory summaries

## Preferred Tools

- scanpy
- anndata
- scvi-tools where appropriate
- motif-analysis utilities

## Starter Pattern

```text
Preferred starting point: scanpy
Inputs: multiome object or paired modalities, ATAC fragments or peak matrix, cell metadata
Outputs: integrated embeddings, modality-aware clusters, motif or regulatory summaries
```

## Workflow

### 1. QC both modalities

Evaluate RNA and ATAC quality independently before joint integration.

### 2. Create harmonized features

Build peak, gene, or gene activity representations consistent across cells.

### 3. Integrate modalities

Use an approach suited to paired or unpaired multimodal data.

### 4. Interpret regulatory signals

Relate motif accessibility, gene activity, and expression patterns cautiously.

### 5. Export multimodal state summaries

Save joint embeddings, modality-specific QC, and regulatory annotations.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `integrated embeddings`
- `modality-aware clusters`
- `motif or regulatory summaries`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Review embeddings together with QC metrics and batch structure before labeling biology.
- Preserve the processed object with metadata and embeddings for downstream reuse.

## Anti-Patterns

- treating weak gene activity estimates as direct expression measurements
- integrating low-quality modalities without modality-specific QC
- reporting regulatory links without stating the evidence type

## Related Skills

- `scRNA Preprocessing And Clustering`
- `Cell Annotation`
- `Cell Communication`
- `Trajectory And Lineage`

## Optional Supplements

- `scvi-tools`
- `anndata`
