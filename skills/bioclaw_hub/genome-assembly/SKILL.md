---
name: genome-assembly
description: Workflow for de novo assembly, scaffolding, polishing, contamination review, and assembly QC.
tool_type: python
primary_tool: assembly
---

# Genome Assembly

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `assembly` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for de novo assembly, scaffolding, polishing, contamination review, and assembly QC.

## When To Use This Skill

- use when the user needs a genome assembly from short, long, or hybrid reads
- use when the task includes scaffolding, polishing, or completeness evaluation
- use when final assembly statistics and contamination summaries are required

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

- short reads, long reads, or both
- optional reference or related genome
- sample context

## Expected Outputs

- assembled contigs or scaffolds
- assembly QC metrics
- contamination summaries

## Preferred Tools

- assembly toolchains
- polishing tools
- QUAST-like QC
- pandas

## Starter Pattern

```text
Preferred starting point: assembly
Inputs: short reads, long reads, or both, optional reference or related genome, sample context
Outputs: assembled contigs or scaffolds, assembly QC metrics, contamination summaries
```

## Workflow

### 1. Select assembly strategy

Choose short-read, long-read, hybrid, or metagenome assembly based on the data and target organism.

### 2. Assemble and polish

Run the appropriate assembler and follow with polishing suited to the sequencing platform.

### 3. Check contamination and completeness

Evaluate assembly size, contiguity, contamination, and expected completeness.

### 4. Annotate assembly context

Record strain, organism, ploidy, and sequencing assumptions that affect interpretation.

### 5. Export validated deliverables

Save FASTA outputs plus QC tables and summary figures.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `assembled contigs or scaffolds`
- `assembly QC metrics`
- `contamination summaries`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Record reference build, caller assumptions, and filtering rules in the final outputs.
- Separate raw calls from filtered or interpreted results.

## Anti-Patterns

- using an assembler mismatched to the data type
- treating N50 as the only QC metric
- skipping contamination screening

## Related Skills

- `Variant Calling`
- `Copy Number`
- `Long-Read Genomics`
- `Comparative Genomics`

## Optional Supplements

- None required for the first pass.
