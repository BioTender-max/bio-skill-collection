# Microbiome Amplicon Technical Reference

## Purpose

This reference file provides deeper implementation notes for `microbiome-amplicon`.

## When To Read This File

- use when the task is 16S, ITS, or other amplicon-based microbiome profiling
- use when denoising, taxonomy assignment, and diversity metrics are required
- use when the user needs cohort-level differential abundance or community structure summaries

## Detailed Inputs

- amplicon FASTQ files
- sample metadata
- taxonomy database

## Detailed Outputs

- ASV or OTU tables
- taxonomy assignments
- diversity and differential abundance summaries

## Tooling Notes

- QIIME2-style workflows
- pandas
- scikit-bio
- seaborn

## Detailed Workflow Notes

### 1. Preprocess reads

Trim primers or adapters and denoise reads into ASVs or OTUs.

### 2. Assign taxonomy

Use a suitable taxonomy model or reference database for the marker type.

### 3. Compute diversity

Calculate alpha and beta diversity with metadata-aware comparisons.

### 4. Compare groups

Run differential abundance with methods matched to compositional data constraints.

### 5. Export community reports

Save tables, ordinations, and taxonomy summaries.

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Review sample contamination, depth differences, and database choice before comparing communities.
- State clearly whether outputs are relative abundance, counts, or derived functions.

## Common Failure Modes

- treating relative abundance changes as absolute shifts without context
- using a taxonomy database mismatched to the marker region
- running differential abundance without accounting for compositional effects

## Optional Supplements

- `scikit-bio`

## Conceptual Provenance

- amplicon microbiome workflows
- community diversity and differential abundance patterns
