# Epitranscriptomics Technical Reference

## Purpose

This reference file provides deeper implementation notes for `epitranscriptomics`.

## When To Read This File

- use when the task is MeRIP-seq, direct RNA modification analysis, or differential RNA modification
- use when enriched IP and input comparisons need to be modeled carefully
- use when the user needs modification-aware plots and transcript-level context

## Detailed Inputs

- modification-enriched reads
- input reads
- transcript annotations

## Detailed Outputs

- modification peaks
- differential modification results
- transcript-level plots

## Tooling Notes

- peak-calling tools
- pandas
- matplotlib

## Detailed Workflow Notes

### 1. Validate assay design

Confirm IP and input matching, replicate availability, and transcript annotation consistency.

### 2. Call modification features

Detect modification-enriched regions with assay-aware models.

### 3. Compare conditions

Test differential modification while separating abundance changes from modification-specific changes where possible.

### 4. Visualize representative transcripts

Plot peaks or signal tracks over transcripts to support interpretation.

### 5. Export clearly labeled outputs

Separate modification results from standard expression results in all tables and plots.

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Check assay-specific QC such as enrichment quality, coverage behavior, or replicate consistency.
- Verify genome build, interval coordinates, and annotation compatibility.

## Common Failure Modes

- equating expression shifts with modification shifts
- calling differential modification without matched inputs or replicates where possible
- overstating transcript-level resolution when the assay is region-based

## Optional Supplements

- None

## Conceptual Provenance

- RNA modification workflows
