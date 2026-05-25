# Methylation Analysis Technical Reference

## Purpose

This reference file provides deeper implementation notes for `methylation-analysis`.

## When To Read This File

- use when the task is DNA methylation calling or differential methylation
- use when bisulfite or long-read methylation data must be summarized at loci or regions
- use when methylation QC and DMR export are required

## Detailed Inputs

- methylation-aware sequencing reads
- reference genome
- sample metadata

## Detailed Outputs

- methylation calls
- DMR tables
- sample and locus QC plots

## Tooling Notes

- Bismark-like workflows
- pandas
- matplotlib
- seaborn

## Detailed Workflow Notes

### 1. Check assay-specific preprocessing

Use the correct alignment or calling path for bisulfite versus direct methylation detection.

### 2. Summarize methylation levels

Aggregate calls at CpG, region, or feature level appropriate to the study question.

### 3. Run differential analysis

Test differences using replicate-aware region-based methods when possible.

### 4. Inspect biological context

Annotate DMRs to promoters, enhancers, or other regions before interpretation.

### 5. Export report-ready outputs

Save calls, DMR tables, and locus-level example plots.

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Check assay-specific QC such as enrichment quality, coverage behavior, or replicate consistency.
- Verify genome build, interval coordinates, and annotation compatibility.

## Common Failure Modes

- mixing assay types without documenting the calling method
- reporting regional changes without effect direction and coverage context
- ignoring low-coverage loci during interpretation

## Optional Supplements

- None

## Conceptual Provenance

- DNA methylation analysis workflows
