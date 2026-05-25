# Spatial Transcriptomics Technical Reference

## Purpose

This reference file provides deeper implementation notes for `spatial-transcriptomics`.

## When To Read This File

- use when the task is spatial transcriptomics analysis or spatially aware visualization
- use when coordinates, images, or spot-level expression are part of the dataset
- use when the user needs domains, deconvolution, or neighborhood summaries

## Detailed Inputs

- spatial expression data
- coordinates or histology images
- optional single-cell reference

## Detailed Outputs

- spatial domains
- deconvolution tables
- spatial maps and neighborhood results

## Tooling Notes

- scanpy-like spatial tooling
- image analysis utilities
- matplotlib
- seaborn

## Detailed Workflow Notes

### 1. Validate spatial assets

Confirm coordinate systems, image registration, and barcode alignment where applicable.

### 2. Preprocess expression and spatial structure

Normalize expression while preserving spatial coordinates and neighborhood information.

### 3. Choose a task path

Run domain detection, deconvolution, communication, or neighborhood analysis according to the question.

### 4. Visualize spatial biology

Generate maps that preserve physical context, legends, and scale.

### 5. Export interpretable artifacts

Save spatial labels, coordinates, and figure-ready outputs.

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Review embeddings together with QC metrics and batch structure before labeling biology.
- Preserve the processed object with metadata and embeddings for downstream reuse.

## Common Failure Modes

- dropping coordinate integrity during preprocessing
- treating deconvolution outputs as ground truth cell counts
- using overcrowded spatial plots without readable legends

## Optional Supplements

- `scanpy`

## Conceptual Provenance

- spatial transcriptomics workflows
- spatial omics task patterns
