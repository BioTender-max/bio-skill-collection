# Bulk RNA Expression Technical Reference

## Purpose

This reference file provides deeper implementation notes for `bulk-rna-expression`.

## When To Read This File

- use when the task is bulk RNA-seq expression profiling before or alongside differential analysis
- use when the user has count matrices, transcript abundances, or aligned RNA-seq reads and needs expression summaries
- use when sample-level QC, PCA, or normalized matrices are required

## Detailed Inputs

- count matrix
- sample metadata
- optional BAM or quantification outputs

## Detailed Outputs

- normalized matrix
- sample QC plots
- PCA or clustering summaries

## Tooling Notes

- pandas
- numpy
- seaborn
- matplotlib
- scanpy for matrix utilities when appropriate

## Detailed Workflow Notes

### 1. Validate matrix orientation

Confirm rows and columns, unique sample IDs, and whether counts are raw integers or already normalized.

### 2. Join metadata

Check condition labels, replicate structure, batch columns, and missing covariates before analysis.

### 3. Compute sample QC

Summarize library size, detected genes, missingness, outliers, and replicate similarity.

### 4. Normalize for exploration

Apply count-aware normalization or variance stabilization appropriate to the downstream method.

### 5. Export analysis-ready data

Save normalized matrices and QC tables for DE, enrichment, or reporting.

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Check replicate structure, outlier samples, and whether counts versus normalized values are being mixed.
- Export ranked or contrast-aware tables when downstream enrichment is likely.

## Common Failure Modes

- mixing raw counts and normalized values in the same table
- running DE directly on TPM values unless the method explicitly supports it
- skipping sample metadata validation before modeling

## Optional Supplements

- `pydeseq2`
- `pysam`

## Conceptual Provenance

- bulk transcriptomics matrix handling patterns
- RNA quantification workflows
- bulk RNA QC and expression summarization patterns
