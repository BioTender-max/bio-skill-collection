# Comparative Genomics Technical Reference

## Purpose

This reference file provides deeper implementation notes for `comparative-genomics`.

## When To Read This File

- use when the task is cross-genome comparison or evolutionary inference
- use when assembled genomes and annotations are available for multiple taxa or strains
- use when the user needs orthologs, synteny blocks, or positive-selection style summaries

## Detailed Inputs

- assemblies
- gene annotations
- optional phylogenetic context

## Detailed Outputs

- ortholog tables
- synteny outputs
- evolutionary comparison summaries

## Tooling Notes

- orthology tools
- alignment and phylogeny utilities
- pandas

## Detailed Workflow Notes

### 1. Define comparison scale

Clarify whether the task is gene-level, synteny-level, or phylogenomic.

### 2. Standardize annotations

Use consistent naming, feature models, and assemblies before comparing genomes.

### 3. Infer shared and divergent elements

Run orthology, synteny, or evolutionary analyses appropriate to the question.

### 4. Interpret in biological context

Separate technical annotation differences from genuine biological divergence.

### 5. Export concise comparison artifacts

Save tables and figures that highlight conserved versus lineage-specific patterns.

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Record reference build, caller assumptions, and filtering rules in the final outputs.
- Separate raw calls from filtered or interpreted results.

## Common Failure Modes

- comparing genomes with incompatible annotation quality without caveats
- overstating adaptive evolution from weak evidence
- mixing orthology and homology claims carelessly

## Optional Supplements

- None

## Conceptual Provenance

- comparative genomics workflows
