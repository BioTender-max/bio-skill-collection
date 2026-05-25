# Long-Read Genomics Technical Reference

## Purpose

This reference file provides deeper implementation notes for `long-read-genomics`.

## When To Read This File

- use when the dataset is nanopore or PacBio long-read sequencing
- use when structural variants, phasing, polishing, or long-read methylation are part of the task
- use when long-read-specific QC and alignment assumptions must be respected

## Detailed Inputs

- long-read FASTQ or raw data
- reference genome
- sample metadata

## Detailed Outputs

- aligned long-read files
- polished consensus or assembly updates
- long-read variant summaries

## Tooling Notes

- long-read aligners
- Clair3-like SV or small-variant tools
- medaka-like polishing tools
- pandas

## Detailed Workflow Notes

### 1. Assess long-read quality

Check read length, quality distributions, and platform-specific artifacts.

### 2. Choose a long-read path

Separate reference alignment, de novo assembly, and methylation-aware analyses as needed.

### 3. Run long-read-aware calling or polishing

Use tools designed for long-read error profiles.

### 4. Interpret platform-specific outputs

Report read-support and confidence metrics appropriate to long-read data.

### 5. Export standard artifacts

Save BAM or CRAM, polished sequences, and variant or methylation summaries.

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Record reference build, caller assumptions, and filtering rules in the final outputs.
- Separate raw calls from filtered or interpreted results.

## Common Failure Modes

- using short-read assumptions for long-read error profiles
- skipping platform-specific QC
- mixing nanopore and PacBio outputs without documenting differences

## Optional Supplements

- `pysam`

## Conceptual Provenance

- long-read sequencing workflows
