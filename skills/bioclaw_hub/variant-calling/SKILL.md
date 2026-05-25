---
name: variant-calling
description: Workflow for small-variant and structural-variant discovery, filtering, annotation, and interpretation from sequencing data.
tool_type: mixed
primary_tool: GATK-style
---

# Variant Calling

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `GATK-style` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for small-variant and structural-variant discovery, filtering, annotation, and interpretation from sequencing data.

## When To Use This Skill

- use when the user asks for germline, somatic, or structural variant calling
- use when BAM or CRAM files and a reference genome are available
- use when VCF generation, filtering, annotation, or interpretation is needed

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

- aligned reads
- reference genome
- optional truth set or panel resources

## Expected Outputs

- VCF files
- filtered variant tables
- annotation summaries

## Preferred Tools

- GATK-style workflows
- DeepVariant-style workflows
- bcftools
- pandas

## Starter Pattern

```text
Preferred starting point: GATK-style
Inputs: aligned reads, reference genome, optional truth set or panel resources
Outputs: VCF files, filtered variant tables, annotation summaries
```

## Workflow

### 1. Define the variant task

Separate germline, somatic, and structural variant paths early because assumptions differ.

### 2. Check alignment quality

Review coverage, duplicate rates, contamination indicators, and reference compatibility before calling.

### 3. Call and filter variants

Use caller-appropriate best practices and keep raw versus filtered outputs distinct.

### 4. Annotate and prioritize

Attach gene, consequence, frequency, and clinical context before interpretation.

### 5. Export reproducible artifacts

Save VCFs, filter criteria, annotation tables, and QC summaries.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `VCF files`
- `filtered variant tables`
- `annotation summaries`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Record reference build, caller assumptions, and filtering rules in the final outputs.
- Separate raw calls from filtered or interpreted results.

## Anti-Patterns

- mixing germline and somatic assumptions
- interpreting unfiltered calls as final findings
- forgetting to record the reference build and caller version

## Related Skills

- `Copy Number`
- `Long-Read Genomics`
- `Genome Assembly`
- `Comparative Genomics`

## Optional Supplements

- `pysam`
- `tiledbvcf`
