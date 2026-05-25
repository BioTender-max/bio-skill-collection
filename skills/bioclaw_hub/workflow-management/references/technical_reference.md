# Workflow Management Technical Reference

## Purpose

This reference file provides deeper implementation notes for `workflow-management`.

## When To Read This File

- use when the task is to organize or run a reproducible omics pipeline
- use when Nextflow, Snakemake, CWL, or WDL style workflows are involved
- use when a one-off analysis should be turned into a repeatable pipeline

## Detailed Inputs

- pipeline definitions
- sample sheets
- environment descriptions

## Detailed Outputs

- reproducible workflow runs
- execution logs
- portable pipeline assets

## Tooling Notes

- Nextflow
- Snakemake
- CWL
- WDL

## Detailed Workflow Notes

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

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Verify config, manifests, and sample sheets before launching a full run.
- Retain logs, versions, and the exact workflow entrypoint used for the run.

## Common Failure Modes

- hardcoding sample-specific paths into pipeline logic
- mixing environment setup and workflow semantics in one opaque script
- running pipelines without recording versions and configs

## Optional Supplements

- None

## Conceptual Provenance

- workflow-management patterns for reproducible omics pipelines
