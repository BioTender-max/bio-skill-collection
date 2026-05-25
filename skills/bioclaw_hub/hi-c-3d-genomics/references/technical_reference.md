# Hi-C And 3D Genomics Technical Reference

## Purpose

This reference file provides deeper implementation notes for `hi-c-3d-genomics`.

## When To Read This File

- use when the task is Hi-C matrix analysis or 3D genome interpretation
- use when loops, compartments, or TADs must be called or compared
- use when contact-map figures or feature-level summaries are required

## Detailed Inputs

- Hi-C contact pairs or matrices
- genome bins
- condition metadata

## Detailed Outputs

- compartments
- loops and TADs
- contact maps and differential summaries

## Tooling Notes

- Hi-C processing utilities
- numpy
- pandas
- matplotlib

## Detailed Workflow Notes

### 1. Validate matrix resolution

Choose a resolution supported by coverage and the biological question.

### 2. Normalize contact structure

Apply appropriate normalization before calling global or local features.

### 3. Call 3D features

Infer compartments, TADs, or loops with methods matched to the resolution and assay.

### 4. Compare conditions carefully

Quantify differences only where coverage and normalization support fair comparison.

### 5. Produce readable maps

Export heatmaps and feature tables with clear genome coordinates and labels.

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Check assay-specific QC such as enrichment quality, coverage behavior, or replicate consistency.
- Verify genome build, interval coordinates, and annotation compatibility.

## Common Failure Modes

- interpreting noisy low-coverage matrices at overly fine resolution
- comparing raw contacts without normalization
- mixing feature scales without stating the resolution

## Optional Supplements

- None

## Conceptual Provenance

- 3D genomics and Hi-C workflows
