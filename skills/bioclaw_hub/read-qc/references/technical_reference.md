# Read QC Technical Reference

## Purpose

This reference file provides deeper implementation notes for `read-qc`.

## When To Read This File

- use when the task is FASTQ quality assessment or cleanup before analysis
- use when the user needs trimming, contamination review, or read-level reports
- use when downstream pipelines depend on deciding whether data quality is acceptable

## Detailed Inputs

- raw FASTQ files
- adapter sequences
- optional sequencing metadata

## Detailed Outputs

- QC reports
- filtered or trimmed reads
- contamination summaries

## Tooling Notes

- fastp
- FastQC-style reports
- pandas
- matplotlib

## Detailed Workflow Notes

### 1. Profile raw reads

Inspect quality scores, adapter content, duplication, and GC behavior before trimming.

### 2. Trim or filter judiciously

Apply adapter removal and quality filtering with settings matched to the assay.

### 3. Screen contamination

Check for host, ribosomal, or other unwanted content if the study design calls for it.

### 4. Re-evaluate after cleanup

Confirm that trimming improved quality without over-truncating useful reads.

### 5. Export both reports and cleaned reads

Keep raw and cleaned QC records for reproducibility.

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Validate file structure and metadata before handing outputs to downstream tools.
- Retain provenance for every conversion, query, or pipeline execution step.

## Common Failure Modes

- trimming aggressively without checking length distributions afterward
- assuming all contamination is removable without assay-specific review
- running downstream analysis on reads that failed basic QC without documenting it

## Optional Supplements

- None

## Conceptual Provenance

- read quality-control workflows
