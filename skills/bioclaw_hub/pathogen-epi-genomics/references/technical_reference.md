# Pathogen Epidemiological Genomics Technical Reference

## Purpose

This reference file provides deeper implementation notes for `pathogen-epi-genomics`.

## When To Read This File

- use when the task is pathogen surveillance, lineage assignment, or outbreak genomics
- use when sample metadata include time, geography, or host context
- use when genomic comparison must be linked to epidemiological interpretation

## Detailed Inputs

- pathogen genomes or read sets
- collection metadata
- reference resources

## Detailed Outputs

- lineage assignments
- cluster or outbreak summaries
- surveillance-ready tables or figures

## Tooling Notes

- phylogenetics utilities
- variant and lineage-calling tools
- pandas

## Detailed Workflow Notes

### 1. Standardize metadata

Ensure time, location, and sample identifiers are consistent before analysis.

### 2. Generate comparable genomic summaries

Call variants or consensus sequences in a way that supports cross-sample comparison.

### 3. Assign lineages or clusters

Use pathogen-appropriate nomenclature and clustering logic.

### 4. Link genomics to epidemiology

Summarize genomic findings with explicit metadata context and caution around transmission claims.

### 5. Export surveillance outputs

Save lineage tables, phylogenies, and cluster summaries.

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Review sample contamination, depth differences, and database choice before comparing communities.
- State clearly whether outputs are relative abundance, counts, or derived functions.

## Common Failure Modes

- claiming direct transmission from genomics alone
- mixing consensus builds or lineage schemes without stating it
- ignoring metadata QC in outbreak analyses

## Optional Supplements

- `phylogenetics`

## Conceptual Provenance

- pathogen surveillance and epidemiological genomics workflows
