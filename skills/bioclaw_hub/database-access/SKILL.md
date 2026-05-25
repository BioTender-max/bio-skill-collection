---
name: database-access
description: Workflow for retrieving public omics datasets, sequences, annotations, and literature-linked biological resources.
tool_type: python
primary_tool: requests
---

# Database Access

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `requests` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for retrieving public omics datasets, sequences, annotations, and literature-linked biological resources.

## When To Use This Skill

- use when the task is downloading or querying public bioinformatics databases
- use when accessions, identifiers, or search terms must be resolved into data assets
- use when external references such as GEO, SRA, UniProt, Reactome, or PubMed are needed

## Quick Route

- If the input is raw or minimally processed data, start with validation and QC before any modeling.
- If the input is already processed, skip directly to the first workflow step that matches the user goal.
- If the user asks for a biological conclusion, always produce at least one QC or confidence artifact alongside the final result.


## Progressive Disclosure

- Read `references/technical_reference.md` when you need deeper tool-selection rules, environment adaptation notes, or extra validation guidance.
- Keep `SKILL.md` as the main execution path and load the reference file only when the task or failure mode needs the extra detail.


## Default Rules

- Prefer Python-first workflows unless the task explicitly requires something else.
- Keep intermediate and final outputs separated.
- Record software versions, reference builds, and key parameters when they affect interpretation.
- Favor reproducible tables and figures over one-off interactive-only outputs.

## Expected Inputs

- accessions or identifiers
- query terms
- optional species or database constraints

## Expected Outputs

- downloaded datasets
- linked metadata tables
- query result summaries

## Preferred Tools

- Entrez-style APIs
- UniProt access tools
- Reactome and PubMed resources
- pandas

## Starter Pattern

```python
import requests

resp = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi", params={
    "db": "gds",
    "term": "single cell liver",
    "retmode": "json",
})
print(resp.text[:500])
```

## Workflow

### 1. Pick the right database

Choose repositories based on whether the target is raw data, processed data, annotation, pathways, or literature.

### 2. Query reproducibly

Record identifiers, filters, and database versions or access dates.

### 3. Normalize returned metadata

Standardize result tables so downstream workflows can join on stable IDs.

### 4. Download only needed assets

Avoid bulk retrieval when a narrower dataset or accession list solves the task.

### 5. Export usable references

Save accession tables, metadata joins, and database provenance.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `downloaded datasets`
- `linked metadata tables`
- `query result summaries`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Record accession provenance, query parameters, and retrieval date or version.
- Verify that downloaded records map cleanly to the identifiers used downstream.

## Anti-Patterns

- mixing identifiers across databases without explicit mapping
- downloading oversized collections when a filtered subset is enough
- citing database content without recording provenance

## Related Skills

- `Sequence And Format IO`
- `Alignment And Mapping`
- `Read QC`
- `Reporting And Figure Export`

## Optional Supplements

- `pubmed-database`
- `reactome-database`
- `string-database`
