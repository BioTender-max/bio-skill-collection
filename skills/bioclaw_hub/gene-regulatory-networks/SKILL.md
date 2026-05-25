---
name: gene-regulatory-networks
description: Workflow for regulatory network inference, regulon scoring, perturbation-aware comparison, and network visualization.
tool_type: python
primary_tool: arboreto-like
---

# Gene Regulatory Networks

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `arboreto-like` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for regulatory network inference, regulon scoring, perturbation-aware comparison, and network visualization.

## When To Use This Skill

- use when the task is GRN inference or regulon-level interpretation
- use when the data include expression matrices and optionally chromatin features or TF priors
- use when the user needs network-level summaries rather than only gene lists

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

- expression matrix
- optional accessibility data
- TF prior resources

## Expected Outputs

- inferred networks
- regulon activity tables
- network visualizations

## Preferred Tools

- arboreto-like GRN utilities
- networkx
- pandas
- seaborn

## Starter Pattern

```text
Preferred starting point: arboreto-like
Inputs: expression matrix, optional accessibility data, TF prior resources
Outputs: inferred networks, regulon activity tables, network visualizations
```

## Workflow

### 1. Choose the evidence model

Clarify whether inference is coexpression-based, prior-constrained, or multimodal.

### 2. Infer or score networks

Run network inference or regulon-scoring methods appropriate to the data type.

### 3. Compare across states

Summarize regulators and network changes across conditions, perturbations, or branches.

### 4. Visualize selectively

Plot subnetworks or regulator-centric views rather than full unreadable graphs.

### 5. Export confidence-aware outputs

Store edge weights, regulator scores, and evidence annotations.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `inferred networks`
- `regulon activity tables`
- `network visualizations`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Check assay-specific QC such as enrichment quality, coverage behavior, or replicate consistency.
- Verify genome build, interval coordinates, and annotation compatibility.

## Anti-Patterns

- presenting inferred networks as validated causal circuitry
- plotting whole dense networks without summarization
- mixing inference evidence types without labeling them

## Related Skills

- `ATAC Seq`
- `ChIP Seq`
- `Methylation Analysis`
- `Epitranscriptomics`

## Optional Supplements

- `arboreto`
