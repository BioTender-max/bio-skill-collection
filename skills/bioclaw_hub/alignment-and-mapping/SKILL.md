---
name: alignment-and-mapping
description: Workflow for read alignment, sorting, indexing, mapping statistics, and downstream-ready alignment artifacts.
tool_type: mixed
primary_tool: samtools
---

# Alignment And Mapping

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `samtools` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for read alignment, sorting, indexing, mapping statistics, and downstream-ready alignment artifacts.

## When To Use This Skill

- use when the task is sequence alignment or alignment file preparation
- use when FASTQ files must be mapped to a genome or transcriptome
- use when BAM or CRAM files and mapping metrics are the expected outputs

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

- FASTQ files
- reference genome or transcriptome
- alignment indexes

## Expected Outputs

- sorted and indexed alignments
- mapping metrics
- downstream-ready BAM or CRAM files

## Preferred Tools

- bwa
- bowtie2
- hisat2
- STAR
- samtools
- pysam

## Starter Pattern

```bash
bwa mem ref.fa sample_R1.fastq.gz sample_R2.fastq.gz | samtools sort -o sample.bam
samtools index sample.bam
samtools flagstat sample.bam > sample.flagstat.txt
```

## Workflow

### 1. Choose the mapper

Match the aligner to DNA, RNA, read length, and splice-awareness needs.

### 2. Run alignment reproducibly

Capture all parameters that influence multi-mapping, splicing, and scoring.

### 3. Post-process alignments

Sort, index, mark or handle duplicates as appropriate, and compute mapping summaries.

### 4. Check mapping quality

Review alignment rate, insert sizes, and reference compatibility before downstream analysis.

### 5. Export standard artifacts

Save BAM or CRAM plus indexes and mapping reports.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `sorted and indexed alignments`
- `mapping metrics`
- `downstream-ready BAM or CRAM files`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Confirm reference build, read-group metadata, and sort or index state before downstream analysis.
- Review mapping summaries before treating alignments as analysis-ready.

## Anti-Patterns

- using a DNA aligner for splice-aware RNA tasks without justification
- forgetting sort and index steps before downstream tools
- dropping read-group or sample metadata needed later

## Related Skills

- `Sequence And Format IO`
- `Read QC`
- `Database Access`
- `Reporting And Figure Export`

## Optional Supplements

- `pysam`
