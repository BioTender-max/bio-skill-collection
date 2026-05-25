# Alternative Splicing Technical Reference

## Purpose

This reference file provides deeper implementation notes for `alternative-splicing`.

## When To Read This File

- use when the task is differential splicing, isoform switching, or splice-aware QC
- use when aligned RNA-seq reads and transcript annotations are available
- use when the user needs event summaries, PSI-like metrics, or sashimi-style visualization

## Detailed Inputs

- aligned RNA-seq reads
- splice junction summaries
- transcript annotation

## Detailed Outputs

- event tables
- isoform usage summaries
- sashimi or splice plots

## Tooling Notes

- splice-aware quantification tools
- pandas
- matplotlib
- genome track plotting utilities

## Detailed Workflow Notes

### 1. Confirm splice-aware inputs

Verify junction extraction, transcript annotation, and sample group definitions.

### 2. Choose analysis level

Use event-level methods for exon or junction usage and isoform-level methods for transcript switching.

### 3. Quantify splicing changes

Compute condition-specific splice usage and test for differential splicing.

### 4. Inspect representative loci

Plot junction-supported events to verify that statistical hits reflect visible changes.

### 5. Export interpretable results

Save event IDs, effect estimates, significance values, and plot-ready loci.

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Check replicate structure, outlier samples, and whether counts versus normalized values are being mixed.
- Export ranked or contrast-aware tables when downstream enrichment is likely.

## Common Failure Modes

- interpreting isoform changes without read support at informative junctions
- mixing event- and transcript-level interpretations without stating which was used
- skipping locus-level review of top hits

## Optional Supplements

- `pysam`

## Conceptual Provenance

- alternative splicing workflows
