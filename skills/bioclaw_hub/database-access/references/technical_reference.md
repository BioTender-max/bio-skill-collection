# Database Access Technical Reference

## Purpose

This reference file provides deeper implementation notes for `database-access`.

## When To Read This File

- use when the task is downloading or querying public bioinformatics databases
- use when accessions, identifiers, or search terms must be resolved into data assets
- use when external references such as GEO, SRA, UniProt, Reactome, or PubMed are needed

## Detailed Inputs

- accessions or identifiers
- query terms
- optional species or database constraints

## Detailed Outputs

- downloaded datasets
- linked metadata tables
- query result summaries

## Tooling Notes

- Entrez-style APIs
- UniProt access tools
- Reactome and PubMed resources
- pandas

## Detailed Workflow Notes

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

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Record accession provenance, query parameters, and retrieval date or version.
- Verify that downloaded records map cleanly to the identifiers used downstream.

## Common Failure Modes

- mixing identifiers across databases without explicit mapping
- downloading oversized collections when a filtered subset is enough
- citing database content without recording provenance

## Optional Supplements

- `pubmed-database`
- `reactome-database`
- `string-database`

## Conceptual Provenance

- bioinformatics database access workflows
- literature and pathway lookup patterns
- public dataset retrieval patterns
