# Variant Calling Technical Reference

## Purpose

This reference file provides deeper implementation notes for `variant-calling`.

## When To Read This File

- use when the user asks for germline, somatic, or structural variant calling
- use when BAM or CRAM files and a reference genome are available
- use when VCF generation, filtering, annotation, or interpretation is needed

## Detailed Inputs

- aligned reads
- reference genome
- optional truth set or panel resources

## Detailed Outputs

- VCF files
- filtered variant tables
- annotation summaries

## Tooling Notes

- GATK-style workflows
- DeepVariant-style workflows
- bcftools
- pandas

## Detailed Workflow Notes

### 1. Define the variant task

Separate germline, somatic, and structural variant paths early because assumptions differ.

### 2. Check alignment quality

Review coverage, duplicate rates, contamination indicators, and reference compatibility before calling.

### 3. Call and filter variants

Use caller-appropriate best practices and keep raw versus filtered outputs distinct.

### 4. Annotate and prioritize

Attach gene, consequence, frequency, and clinical context before interpretation.

### 5. Export reproducible artifacts

Save VCFs, filter criteria, annotation tables, and QC summaries.

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Record reference build, caller assumptions, and filtering rules in the final outputs.
- Separate raw calls from filtered or interpreted results.

## Common Failure Modes

- mixing germline and somatic assumptions
- interpreting unfiltered calls as final findings
- forgetting to record the reference build and caller version

## Optional Supplements

- `pysam`
- `tiledbvcf`

## Conceptual Provenance

- variant-calling workflows
- clinical and research variant interpretation patterns
- alignment and VCF handling patterns
