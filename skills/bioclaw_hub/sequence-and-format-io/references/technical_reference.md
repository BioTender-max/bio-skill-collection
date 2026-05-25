# Sequence And Format IO Technical Reference

## Purpose

This reference file provides deeper implementation notes for `sequence-and-format-io`.

## When To Read This File

- use when the task is file parsing, sequence manipulation, or format conversion
- use when FASTA, FASTQ, BED, GTF, BAM, or related files need validation or transformation
- use when a downstream omics workflow is blocked on messy input files

## Detailed Inputs

- sequence or annotation files
- format specifications
- optional metadata

## Detailed Outputs

- validated or converted files
- summary statistics
- format sanity-check reports

## Tooling Notes

- biopython
- pysam
- pandas
- basic shell utilities

## Detailed Workflow Notes

### 1. Identify file semantics

Do not assume a file is clean just because the extension looks right.

### 2. Validate core structure

Check headers, coordinates, indexing, compression, and identifier consistency.

### 3. Convert safely

Preserve metadata and line ordering where downstream tools depend on it.

### 4. Summarize content

Produce quick counts and sanity-check metrics after transformation.

### 5. Hand off clean artifacts

Save validated outputs with explicit naming and build context.

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Check coordinate systems, compression, and index consistency after every conversion.
- Run a lightweight sanity check before handing files to downstream tools.

## Common Failure Modes

- silently converting between 0-based and 1-based coordinate systems
- rewriting compressed indexed files without regenerating indexes
- dropping metadata columns during format conversion

## Optional Supplements

- `pysam`
- `biopython`

## Conceptual Provenance

- sequence I/O workflows
- genome interval handling patterns
- bioinformatics file utility patterns
