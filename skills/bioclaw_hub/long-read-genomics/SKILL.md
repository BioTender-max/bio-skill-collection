---
name: long-read-genomics
description: Workflow for nanopore or PacBio long-read QC, alignment, polishing, methylation-aware analysis, and structural variant discovery.
tool_type: mixed
primary_tool: long-read
---

# Long-Read Genomics

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `long-read` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for nanopore or PacBio long-read QC, alignment, polishing, methylation-aware analysis, and structural variant discovery.

## When To Use This Skill

- use when the dataset is nanopore or PacBio long-read sequencing
- use when structural variants, phasing, polishing, or long-read methylation are part of the task
- use when long-read-specific QC and alignment assumptions must be respected

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

- long-read FASTQ or raw data
- reference genome
- sample metadata

## Expected Outputs

- aligned long-read files
- polished consensus or assembly updates
- long-read variant summaries

## Preferred Tools

- long-read aligners
- Clair3-like SV or small-variant tools
- medaka-like polishing tools
- pandas

## Starter Pattern

```text
Preferred starting point: long-read
Inputs: long-read FASTQ or raw data, reference genome, sample metadata
Outputs: aligned long-read files, polished consensus or assembly updates, long-read variant summaries
```

## Workflow

### 1. Assess long-read quality

Check read length, quality distributions, and platform-specific artifacts.

### 2. Choose a long-read path

Separate reference alignment, de novo assembly, and methylation-aware analyses as needed.

### 3. Run long-read-aware calling or polishing

Use tools designed for long-read error profiles.

### 4. Interpret platform-specific outputs

Report read-support and confidence metrics appropriate to long-read data.

### 5. Export standard artifacts

Save BAM or CRAM, polished sequences, and variant or methylation summaries.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `aligned long-read files`
- `polished consensus or assembly updates`
- `long-read variant summaries`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Record reference build, caller assumptions, and filtering rules in the final outputs.
- Separate raw calls from filtered or interpreted results.

## Anti-Patterns

- using short-read assumptions for long-read error profiles
- skipping platform-specific QC
- mixing nanopore and PacBio outputs without documenting differences

## Related Skills

- `Variant Calling`
- `Copy Number`
- `Genome Assembly`
- `Comparative Genomics`

## Optional Supplements

- `pysam`
