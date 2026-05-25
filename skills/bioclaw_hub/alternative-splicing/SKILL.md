---
name: alternative-splicing
description: Workflow for event-level and isoform-level splicing analysis with sashimi-ready outputs and splice QC.
tool_type: python
primary_tool: splice-aware
---

# Alternative Splicing

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `splice-aware` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for event-level and isoform-level splicing analysis with sashimi-ready outputs and splice QC.

## When To Use This Skill

- use when the task is differential splicing, isoform switching, or splice-aware QC
- use when aligned RNA-seq reads and transcript annotations are available
- use when the user needs event summaries, PSI-like metrics, or sashimi-style visualization

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

- aligned RNA-seq reads
- splice junction summaries
- transcript annotation

## Expected Outputs

- event tables
- isoform usage summaries
- sashimi or splice plots

## Preferred Tools

- splice-aware quantification tools
- pandas
- matplotlib
- genome track plotting utilities

## Starter Pattern

```text
Preferred starting point: splice-aware
Inputs: aligned RNA-seq reads, splice junction summaries, transcript annotation
Outputs: event tables, isoform usage summaries, sashimi or splice plots
```

## Workflow

### 1. Confirm splice-aware inputs

Verify junction extraction, transcript annotation, and sample group definitions.

### 2. Choose analysis level

Use event-level methods for exon or junction usage and isoform-level methods for transcript switching.

### 3. Quantify splicing changes

Compute condition-specific splice usage and test for differential splicing.

### 4. Inspect representative loci

Plot junction-supported events to verify that statistical hits reflect visible changes.

### 5. Export interpretable results

Save event IDs, effect estimates, significance values, and plot-ready loci.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `event tables`
- `isoform usage summaries`
- `sashimi or splice plots`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Check replicate structure, outlier samples, and whether counts versus normalized values are being mixed.
- Export ranked or contrast-aware tables when downstream enrichment is likely.

## Anti-Patterns

- interpreting isoform changes without read support at informative junctions
- mixing event- and transcript-level interpretations without stating which was used
- skipping locus-level review of top hits

## Related Skills

- `Bulk RNA Expression`
- `RNA Quantification`
- `Differential Expression`
- `Small RNA Seq`

## Optional Supplements

- `pysam`
