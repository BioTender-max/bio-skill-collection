# Small RNA Seq Technical Reference

## Purpose

This reference file provides deeper implementation notes for `small-rna-seq`.

## When To Read This File

- use when the user has miRNA or other small RNA sequencing data
- use when adapter-heavy preprocessing and short-read-specific QC are required
- use when the goal is differential miRNA analysis or target prediction follow-up

## Detailed Inputs

- small RNA FASTQ files
- adapter sequences
- reference miRNA annotations

## Detailed Outputs

- small RNA count matrix
- differential miRNA tables
- target candidate summaries

## Tooling Notes

- miRge3
- miRDeep2-style workflows
- pandas
- seaborn

## Detailed Workflow Notes

### 1. Handle short inserts carefully

Trim adapters and confirm read-length distributions before quantification.

### 2. Quantify annotated species

Map or assign reads to miRNAs and other small RNA classes with class-aware counting.

### 3. Perform count-aware comparisons

Use replicate-aware statistics for differential abundance.

### 4. Review library composition

Inspect proportions of miRNA, tRNA fragments, rRNA fragments, and other classes.

### 5. Prepare interpretation outputs

Export mature miRNA results and optional target-prediction inputs.

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Check replicate structure, outlier samples, and whether counts versus normalized values are being mixed.
- Export ranked or contrast-aware tables when downstream enrichment is likely.

## Common Failure Modes

- treating adapter-trimmed and untrimmed samples as comparable
- ignoring multi-mapping behavior for short RNAs
- reporting targets without clarifying they are predictions

## Optional Supplements

- None

## Conceptual Provenance

- small RNA sequencing workflows
- miRNA-focused analysis patterns
