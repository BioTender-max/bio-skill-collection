---
name: rna-quantification
description: Workflow for gene and transcript quantification from RNA-seq reads using alignment-based or alignment-free tools.
tool_type: mixed
primary_tool: salmon
---

# RNA Quantification

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `salmon` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for gene and transcript quantification from RNA-seq reads using alignment-based or alignment-free tools.

## When To Use This Skill

- use when the user needs counts or transcript abundances from FASTQ files
- use when the task is featureCounts, salmon, kallisto, or tximport-style quantification
- use when quantification outputs need to be prepared for DE or expression reporting

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
- annotation GTF or GFF

## Expected Outputs

- gene counts
- transcript abundances
- quantification QC summaries

## Preferred Tools

- salmon
- kallisto
- featureCounts
- tximport-style imports
- pandas

## Starter Pattern

```bash
salmon quant \
  -i transcriptome_index \
  -l A \
  -1 sample_R1.fastq.gz \
  -2 sample_R2.fastq.gz \
  -o quant/sample
```

## Workflow

### 1. Choose quantification strategy

Prefer alignment-free quantification for speed and transcript-level abundance, and alignment-based counting when genomic alignment is already available.

### 2. Verify references

Ensure transcriptome, genome, and annotation versions are consistent before quantification.

### 3. Run quantification

Capture both abundance tables and tool-specific mapping or assignment rates.

### 4. Aggregate to analysis level

Convert transcript-level outputs to gene-level summaries only when the downstream task calls for it.

### 5. Prepare outputs

Standardize sample IDs and produce a count or abundance matrix plus QC metadata.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `gene counts`
- `transcript abundances`
- `quantification QC summaries`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Check replicate structure, outlier samples, and whether counts versus normalized values are being mixed.
- Export ranked or contrast-aware tables when downstream enrichment is likely.

## Anti-Patterns

- combining references from different releases
- dropping assignment-rate QC when quantification quality is uncertain
- using abundance estimates as counts without tracking the distinction

## Related Skills

- `Bulk RNA Expression`
- `Differential Expression`
- `Alternative Splicing`
- `Small RNA Seq`

## Optional Supplements

- `pysam`
