---
name: comparative-genomics
description: Workflow for orthology, synteny, ancestral reconstruction, and evolutionary comparison across genomes.
tool_type: python
primary_tool: orthology
---

# Comparative Genomics

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `orthology` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for orthology, synteny, ancestral reconstruction, and evolutionary comparison across genomes.

## When To Use This Skill

- use when the task is cross-genome comparison or evolutionary inference
- use when assembled genomes and annotations are available for multiple taxa or strains
- use when the user needs orthologs, synteny blocks, or positive-selection style summaries

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

- assemblies
- gene annotations
- optional phylogenetic context

## Expected Outputs

- ortholog tables
- synteny outputs
- evolutionary comparison summaries

## Preferred Tools

- orthology tools
- alignment and phylogeny utilities
- pandas

## Starter Pattern

```text
Preferred starting point: orthology
Inputs: assemblies, gene annotations, optional phylogenetic context
Outputs: ortholog tables, synteny outputs, evolutionary comparison summaries
```

## Workflow

### 1. Define comparison scale

Clarify whether the task is gene-level, synteny-level, or phylogenomic.

### 2. Standardize annotations

Use consistent naming, feature models, and assemblies before comparing genomes.

### 3. Infer shared and divergent elements

Run orthology, synteny, or evolutionary analyses appropriate to the question.

### 4. Interpret in biological context

Separate technical annotation differences from genuine biological divergence.

### 5. Export concise comparison artifacts

Save tables and figures that highlight conserved versus lineage-specific patterns.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `ortholog tables`
- `synteny outputs`
- `evolutionary comparison summaries`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Record reference build, caller assumptions, and filtering rules in the final outputs.
- Separate raw calls from filtered or interpreted results.

## Anti-Patterns

- comparing genomes with incompatible annotation quality without caveats
- overstating adaptive evolution from weak evidence
- mixing orthology and homology claims carelessly

## Related Skills

- `Variant Calling`
- `Copy Number`
- `Long-Read Genomics`
- `Genome Assembly`

## Optional Supplements

- None required for the first pass.
