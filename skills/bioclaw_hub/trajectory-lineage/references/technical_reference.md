# Trajectory And Lineage Technical Reference

## Purpose

This reference file provides deeper implementation notes for `trajectory-lineage`.

## When To Read This File

- use when the user asks for pseudotime, lineage branching, or developmental progression
- use when the single-cell object already has a coherent embedding and annotations
- use when dynamic gene programs or branch-specific markers are needed

## Detailed Inputs

- processed single-cell object
- cluster labels
- optional time or perturbation metadata

## Detailed Outputs

- pseudotime assignments
- branch or lineage states
- dynamic gene programs

## Tooling Notes

- scanpy
- scvelo where velocity is available
- matplotlib

## Detailed Workflow Notes

### 1. Check topology assumptions

Ensure the embedding and cluster relationships support a trajectory-style interpretation.

### 2. Pick roots and branches carefully

Use prior biology or metadata to justify start states and branch structure.

### 3. Infer trajectories

Compute pseudotime or lineage paths and verify they align with marker trends.

### 4. Identify dynamic features

Report genes or modules that vary along pseudotime or across branches.

### 5. Visualize with context

Overlay trajectories on embeddings and summarize branch-specific biology.

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Review embeddings together with QC metrics and batch structure before labeling biology.
- Preserve the processed object with metadata and embeddings for downstream reuse.

## Common Failure Modes

- forcing linear trajectories on clearly disconnected states
- setting roots arbitrarily without stating the assumption
- claiming lineage causality from static data alone

## Optional Supplements

- `scvelo`

## Conceptual Provenance

- single-cell trajectory inference workflows
- temporal genomics trajectory modeling
- RNA velocity-style trajectory patterns
