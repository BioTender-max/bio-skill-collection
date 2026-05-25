---
name: sequence-and-format-io
description: Workflow for foundational sequence parsing, conversion, compression handling, and interval-aware file validation.
tool_type: python
primary_tool: biopython
---

# Sequence And Format IO

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `biopython` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for foundational sequence parsing, conversion, compression handling, and interval-aware file validation.

## When To Use This Skill

- use when the task is file parsing, sequence manipulation, or format conversion
- use when FASTA, FASTQ, BED, GTF, BAM, or related files need validation or transformation
- use when a downstream omics workflow is blocked on messy input files

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

- sequence or annotation files
- format specifications
- optional metadata

## Expected Outputs

- validated or converted files
- summary statistics
- format sanity-check reports

## Preferred Tools

- biopython
- pysam
- pandas
- basic shell utilities

## Starter Pattern

```text
Preferred starting point: biopython
Inputs: sequence or annotation files, format specifications, optional metadata
Outputs: validated or converted files, summary statistics, format sanity-check reports
```

## Workflow

### 1. Identify file semantics

Do not assume a file is clean just because the extension looks right.

### 2. Validate core structure

Check headers, coordinates, indexing, compression, and identifier consistency.

### 3. Convert safely

Preserve metadata and line ordering where downstream tools depend on it.

### 4. Summarize content

Produce quick counts and sanity-check metrics after transformation.

### 5. Hand off clean artifacts

Save validated outputs with explicit naming and build context.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `validated or converted files`
- `summary statistics`
- `format sanity-check reports`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Check coordinate systems, compression, and index consistency after every conversion.
- Run a lightweight sanity check before handing files to downstream tools.

## Anti-Patterns

- silently converting between 0-based and 1-based coordinate systems
- rewriting compressed indexed files without regenerating indexes
- dropping metadata columns during format conversion

## Related Skills

- `Alignment And Mapping`
- `Read QC`
- `Database Access`
- `Reporting And Figure Export`

## Optional Supplements

- `pysam`
- `biopython`
