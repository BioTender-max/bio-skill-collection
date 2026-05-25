---
name: pathogen-epi-genomics
description: Workflow for outbreak-style pathogen genomics, surveillance, lineage assignment, and transmission-oriented comparative analysis.
tool_type: python
primary_tool: phylogenetics
---

# Pathogen Epidemiological Genomics

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `phylogenetics` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for outbreak-style pathogen genomics, surveillance, lineage assignment, and transmission-oriented comparative analysis.

## When To Use This Skill

- use when the task is pathogen surveillance, lineage assignment, or outbreak genomics
- use when sample metadata include time, geography, or host context
- use when genomic comparison must be linked to epidemiological interpretation

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

- pathogen genomes or read sets
- collection metadata
- reference resources

## Expected Outputs

- lineage assignments
- cluster or outbreak summaries
- surveillance-ready tables or figures

## Preferred Tools

- phylogenetics utilities
- variant and lineage-calling tools
- pandas

## Starter Pattern

```text
Preferred starting point: phylogenetics
Inputs: pathogen genomes or read sets, collection metadata, reference resources
Outputs: lineage assignments, cluster or outbreak summaries, surveillance-ready tables or figures
```

## Workflow

### 1. Standardize metadata

Ensure time, location, and sample identifiers are consistent before analysis.

### 2. Generate comparable genomic summaries

Call variants or consensus sequences in a way that supports cross-sample comparison.

### 3. Assign lineages or clusters

Use pathogen-appropriate nomenclature and clustering logic.

### 4. Link genomics to epidemiology

Summarize genomic findings with explicit metadata context and caution around transmission claims.

### 5. Export surveillance outputs

Save lineage tables, phylogenies, and cluster summaries.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `lineage assignments`
- `cluster or outbreak summaries`
- `surveillance-ready tables or figures`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Review sample contamination, depth differences, and database choice before comparing communities.
- State clearly whether outputs are relative abundance, counts, or derived functions.

## Anti-Patterns

- claiming direct transmission from genomics alone
- mixing consensus builds or lineage schemes without stating it
- ignoring metadata QC in outbreak analyses

## Related Skills

- `Metagenomics`
- `Microbiome Amplicon`
- `Phylogenetics`

## Optional Supplements

- `phylogenetics`
