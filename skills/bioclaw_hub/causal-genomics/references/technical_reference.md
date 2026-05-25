# Causal Genomics Technical Reference

## Purpose

This reference file provides deeper implementation notes for `causal-genomics`.

## When To Read This File

- use when the task is causal variant, trait-to-gene, or mediation-style genomic inference
- use when GWAS and QTL summary data must be integrated
- use when the user needs statistical evidence about shared signals or directionality assumptions

## Detailed Inputs

- GWAS summary statistics
- QTL or molecular trait summary statistics
- LD reference

## Detailed Outputs

- colocalization results
- credible sets
- causal evidence summaries

## Tooling Notes

- summary-statistics workflows
- pandas
- numpy

## Detailed Workflow Notes

### 1. Harmonize summary statistics

Align alleles, genome builds, and variant IDs before combining datasets.

### 2. Pick the causal framework

Use fine-mapping, colocalization, mediation, or MR according to the question.

### 3. Test and compare signals

Quantify shared or potentially causal effects with the required assumptions stated clearly.

### 4. Review sensitivity

Inspect heterogeneity, pleiotropy, and LD-related caveats before interpretation.

### 5. Export assumption-aware results

Save summary tables with methods, assumptions, and confidence measures.

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Verify that modalities, samples, and model assumptions align before integration or inference.
- Export factors, scores, or model outputs together with interpretation context.

## Common Failure Modes

- treating statistical colocalization as definitive causal proof
- ignoring allele harmonization issues
- running MR without checking instrument quality and pleiotropy

## Optional Supplements

- None

## Conceptual Provenance

- causal genomics workflows
