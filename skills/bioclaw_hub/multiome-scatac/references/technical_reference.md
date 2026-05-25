# Multiome And scATAC Technical Reference

## Purpose

This reference file provides deeper implementation notes for `multiome-scatac`.

## When To Read This File

- use when the task is scATAC, multiome RNA-ATAC, or multimodal single-cell integration
- use when gene activity, motif activity, or regulatory linkage is required
- use when the user needs a joint view across modalities rather than separate analyses

## Detailed Inputs

- multiome object or paired modalities
- ATAC fragments or peak matrix
- cell metadata

## Detailed Outputs

- integrated embeddings
- modality-aware clusters
- motif or regulatory summaries

## Tooling Notes

- scanpy
- anndata
- scvi-tools where appropriate
- motif-analysis utilities

## Detailed Workflow Notes

### 1. QC both modalities

Evaluate RNA and ATAC quality independently before joint integration.

### 2. Create harmonized features

Build peak, gene, or gene activity representations consistent across cells.

### 3. Integrate modalities

Use an approach suited to paired or unpaired multimodal data.

### 4. Interpret regulatory signals

Relate motif accessibility, gene activity, and expression patterns cautiously.

### 5. Export multimodal state summaries

Save joint embeddings, modality-specific QC, and regulatory annotations.

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Review embeddings together with QC metrics and batch structure before labeling biology.
- Preserve the processed object with metadata and embeddings for downstream reuse.

## Common Failure Modes

- treating weak gene activity estimates as direct expression measurements
- integrating low-quality modalities without modality-specific QC
- reporting regulatory links without stating the evidence type

## Optional Supplements

- `scvi-tools`
- `anndata`

## Conceptual Provenance

- single-cell multimodal integration workflows
- single-cell ATAC analysis workflows
- ATAC-seq interpretation patterns
