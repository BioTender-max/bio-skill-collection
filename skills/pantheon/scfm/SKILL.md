---
id: scfm_skills_index
name: Single-Cell Foundation Models Skills Index
description: |
  Workflow guidance and model reference for single-cell foundation models
  (scGPT, Geneformer, UCE, scBERT, etc.). Covers model selection,
  validation-first workflow, and per-model I/O contracts.
tags: [scfm, foundation-models, scGPT, geneformer, UCE, embeddings]
---

# Single-Cell Foundation Models (SCFM)

Workflow and model reference for embedding and integration with single-cell
foundation models.

## Available Skills

### SCFM Workflow

Validation-first workflow for foundation model usage: profile, validate, run, interpret.

**Skill file**: [workflow.md](./workflow.md)

### SCFM Model Reference

Per-model reference cards with I/O contracts, gene ID schemes, and hardware requirements.

**Skill file**: [models.md](./models.md)

### Detailed Model Documentation

In-depth specs for individual models (scBERT, scGPT, Geneformer, UCE, etc.).

**Docs folder**: [_docs/](./_docs/)

## When to Use

- You want FM embeddings (e.g., `obsm["X_uce"]`, `obsm["X_scGPT"]`)
- You need model selection based on gene ID scheme and species
- You want a validation-first workflow before heavy inference
