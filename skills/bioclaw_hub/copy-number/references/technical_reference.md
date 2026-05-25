# Copy Number Technical Reference

## Purpose

This reference file provides deeper implementation notes for `copy-number`.

## When To Read This File

- use when the task is CNV calling or copy-number visualization
- use when coverage-based segment inference is needed for tumor or cohort samples
- use when the user needs gene-level CNV summaries or segment plots

## Detailed Inputs

- coverage or ratio data
- target bins or intervals
- sample metadata

## Detailed Outputs

- CNV segments
- gene-level CNV tables
- CNV plots

## Tooling Notes

- CNVkit-style workflows
- GATK CNV-style workflows
- pandas
- matplotlib

## Detailed Workflow Notes

### 1. Confirm assay context

Clarify tumor-normal versus tumor-only design and target capture versus genome-wide coverage.

### 2. Generate or import coverage summaries

Build bin- or target-level signals suitable for segmentation.

### 3. Call segments

Infer copy-number segments and classify gains, losses, or focal events.

### 4. Annotate to genes and loci

Map segments to biologically relevant genes and recurrent regions.

### 5. Report with visualization

Produce chromosome-level plots and gene-centric summaries.

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Record reference build, caller assumptions, and filtering rules in the final outputs.
- Separate raw calls from filtered or interpreted results.

## Common Failure Modes

- treating noisy ratio shifts as confident focal events without segmentation support
- ignoring tumor purity or ploidy context when it matters
- reporting copy-number calls without genome build and binning details

## Optional Supplements

- None

## Conceptual Provenance

- copy-number workflows
- coverage- and segmentation-based CNV patterns
