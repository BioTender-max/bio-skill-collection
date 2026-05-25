# Phasing And Imputation Technical Reference

## Purpose

This reference file provides deeper implementation notes for `phasing-imputation`.

## When To Read This File

- use when the task is genotype phasing or imputation from array or sequence-derived variant data
- use when the study requires haplotypes, imputed markers, or downstream association-ready genotypes
- use when reference panel choice and QC are central to the analysis

## Detailed Inputs

- VCF genotype data
- sample metadata
- reference panel

## Detailed Outputs

- phased genotypes
- imputed genotype set
- imputation QC metrics

## Tooling Notes

- phasing tools
- imputation tools
- bcftools
- pandas

## Detailed Workflow Notes

### 1. Validate cohort and reference compatibility

Choose a reference panel matched to ancestry and build.

### 2. Phase genotypes

Produce haplotype-aware inputs appropriate for the imputation engine.

### 3. Impute variants

Run imputation and retain quality metrics such as INFO or dosage confidence.

### 4. Filter post-imputation

Apply frequency and quality thresholds aligned with the downstream use case.

### 5. Export association-ready outputs

Save phased or imputed VCFs and QC summaries.

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Record reference build, caller assumptions, and filtering rules in the final outputs.
- Separate raw calls from filtered or interpreted results.

## Common Failure Modes

- using a poorly matched reference panel without documenting the limitation
- keeping low-confidence imputed sites as if they were observed genotypes
- forgetting genome build harmonization

## Optional Supplements

- None

## Conceptual Provenance

- phasing and imputation workflows
