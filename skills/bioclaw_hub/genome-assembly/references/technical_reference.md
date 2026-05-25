# Genome Assembly Technical Reference

## Purpose

This reference file provides deeper implementation notes for `genome-assembly`.

## When To Read This File

- use when the user needs a genome assembly from short, long, or hybrid reads
- use when the task includes scaffolding, polishing, or completeness evaluation
- use when final assembly statistics and contamination summaries are required

## Detailed Inputs

- short reads, long reads, or both
- optional reference or related genome
- sample context

## Detailed Outputs

- assembled contigs or scaffolds
- assembly QC metrics
- contamination summaries

## Tooling Notes

- assembly toolchains
- polishing tools
- QUAST-like QC
- pandas

## Detailed Workflow Notes

### 1. Select assembly strategy

Choose short-read, long-read, hybrid, or metagenome assembly based on the data and target organism.

### 2. Assemble and polish

Run the appropriate assembler and follow with polishing suited to the sequencing platform.

### 3. Check contamination and completeness

Evaluate assembly size, contiguity, contamination, and expected completeness.

### 4. Annotate assembly context

Record strain, organism, ploidy, and sequencing assumptions that affect interpretation.

### 5. Export validated deliverables

Save FASTA outputs plus QC tables and summary figures.

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Record reference build, caller assumptions, and filtering rules in the final outputs.
- Separate raw calls from filtered or interpreted results.

## Common Failure Modes

- using an assembler mismatched to the data type
- treating N50 as the only QC metric
- skipping contamination screening

## Optional Supplements

- None

## Conceptual Provenance

- genome assembly workflows
