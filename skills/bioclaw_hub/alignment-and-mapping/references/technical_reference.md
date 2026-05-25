# Alignment And Mapping Technical Reference

## Purpose

This reference file provides deeper implementation notes for `alignment-and-mapping`.

## When To Read This File

- use when the task is sequence alignment or alignment file preparation
- use when FASTQ files must be mapped to a genome or transcriptome
- use when BAM or CRAM files and mapping metrics are the expected outputs

## Detailed Inputs

- FASTQ files
- reference genome or transcriptome
- alignment indexes

## Detailed Outputs

- sorted and indexed alignments
- mapping metrics
- downstream-ready BAM or CRAM files

## Tooling Notes

- bwa
- bowtie2
- hisat2
- STAR
- samtools
- pysam

## Detailed Workflow Notes

### 1. Choose the mapper

Match the aligner to DNA, RNA, read length, and splice-awareness needs.

### 2. Run alignment reproducibly

Capture all parameters that influence multi-mapping, splicing, and scoring.

### 3. Post-process alignments

Sort, index, mark or handle duplicates as appropriate, and compute mapping summaries.

### 4. Check mapping quality

Review alignment rate, insert sizes, and reference compatibility before downstream analysis.

### 5. Export standard artifacts

Save BAM or CRAM plus indexes and mapping reports.

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Confirm reference build, read-group metadata, and sort or index state before downstream analysis.
- Review mapping summaries before treating alignments as analysis-ready.

## Common Failure Modes

- using a DNA aligner for splice-aware RNA tasks without justification
- forgetting sort and index steps before downstream tools
- dropping read-group or sample metadata needed later

## Optional Supplements

- `pysam`

## Conceptual Provenance

- read alignment workflows
- pairwise and multiple alignment handling patterns
- alignment file management patterns
