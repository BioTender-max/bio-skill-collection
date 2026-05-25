---
name: workflow-management
description: Workflow for orchestrating reproducible omics pipelines with workflow engines and clear execution provenance.
tool_type: mixed
primary_tool: Nextflow
---

# Workflow Management

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `Nextflow` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for orchestrating reproducible omics pipelines with workflow engines and clear execution provenance.

## When To Use This Skill

- use when the task is to organize or run a reproducible omics pipeline
- use when Nextflow, Snakemake, CWL, or WDL style workflows are involved
- use when a one-off analysis should be turned into a repeatable pipeline

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

- pipeline definitions
- sample sheets
- environment descriptions

## Expected Outputs

- reproducible workflow runs
- execution logs
- portable pipeline assets

## Preferred Tools

- Nextflow
- Snakemake
- CWL
- WDL

## Starter Pattern

```bash
nextflow run main.nf \
  --input samplesheet.csv \
  --outdir results/
```

## Workflow

### 1. Define the workflow boundary

State inputs, outputs, parameters, and expected execution environment clearly.

### 2. Choose an engine

Use the engine already established by the project unless there is a strong reason not to.

### 3. Separate config from logic

Keep sample sheets, resources, and environment settings outside the core task definitions.

### 4. Capture provenance

Retain logs, software versions, and execution metadata for reruns.

### 5. Export reusable workflow assets

Save configs, manifests, and run summaries in a stable structure.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `reproducible workflow runs`
- `execution logs`
- `portable pipeline assets`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Verify config, manifests, and sample sheets before launching a full run.
- Retain logs, versions, and the exact workflow entrypoint used for the run.

## Anti-Patterns

- hardcoding sample-specific paths into pipeline logic
- mixing environment setup and workflow semantics in one opaque script
- running pipelines without recording versions and configs

## Related Skills

- `Sequence And Format IO`
- `Alignment And Mapping`
- `Read QC`
- `Database Access`

## Optional Supplements

- None required for the first pass.
