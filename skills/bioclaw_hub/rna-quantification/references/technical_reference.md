# RNA Quantification Technical Reference

## Purpose

This reference file provides deeper implementation notes for `rna-quantification`.

## When To Read This File

- use when the user needs counts or transcript abundances from FASTQ files
- use when the task is featureCounts, salmon, kallisto, or tximport-style quantification
- use when quantification outputs need to be prepared for DE or expression reporting

## Detailed Inputs

- FASTQ files
- reference genome or transcriptome
- annotation GTF or GFF

## Detailed Outputs

- gene counts
- transcript abundances
- quantification QC summaries

## Tooling Notes

- salmon
- kallisto
- featureCounts
- tximport-style imports
- pandas

## Detailed Workflow Notes

### 1. Choose quantification strategy

Prefer alignment-free quantification for speed and transcript-level abundance, and alignment-based counting when genomic alignment is already available.

### 2. Verify references

Ensure transcriptome, genome, and annotation versions are consistent before quantification.

### 3. Run quantification

Capture both abundance tables and tool-specific mapping or assignment rates.

### 4. Aggregate to analysis level

Convert transcript-level outputs to gene-level summaries only when the downstream task calls for it.

### 5. Prepare outputs

Standardize sample IDs and produce a count or abundance matrix plus QC metadata.

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Check replicate structure, outlier samples, and whether counts versus normalized values are being mixed.
- Export ranked or contrast-aware tables when downstream enrichment is likely.

## Common Failure Modes

- combining references from different releases
- dropping assignment-rate QC when quantification quality is uncertain
- using abundance estimates as counts without tracking the distinction

## Optional Supplements

- `pysam`

## Conceptual Provenance

- RNA quantification workflows
- alignment-derived counting patterns
- RNA-seq quantification task patterns
