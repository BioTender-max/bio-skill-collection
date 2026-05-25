# Reporting And Figure Export Technical Reference

## Purpose

This reference file provides deeper implementation notes for `reporting-and-figure-export`.

## When To Read This File

- use when the task is to turn analysis outputs into a clear report or deliverable
- use when plots and tables must be exported in publication- or presentation-ready form
- use when a notebook, Quarto report, or figure bundle is needed

## Detailed Inputs

- analysis tables
- plots
- metadata
- interpretation notes

## Detailed Outputs

- QC or analysis reports
- exported figures
- deliverable-ready tables

## Tooling Notes

- matplotlib
- seaborn
- Quarto-style or notebook reporting
- pandas

## Detailed Workflow Notes

### 1. Separate raw outputs from presentation outputs

Keep the analysis artifacts intact and build curated exports on top.

### 2. Standardize figure formatting

Use consistent fonts, labels, color legends, and vector output when possible.

### 3. Assemble compact reports

Summarize key methods, QC, main findings, and file provenance.

### 4. Export tables cleanly

Write machine-readable and human-readable result tables with stable column names.

### 5. Preserve reproducibility

Record how the report and figures were generated.

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Validate file structure and metadata before handing outputs to downstream tools.
- Retain provenance for every conversion, query, or pipeline execution step.

## Common Failure Modes

- copy-pasting plots without recording how they were made
- using unreadable legends, tiny fonts, or raster-only outputs when vector is possible
- mixing exploratory and final figures without labeling them

## Optional Supplements

- `seaborn`
- `plotly`

## Conceptual Provenance

- bioinformatics reporting workflows
- publication-quality figure and export patterns
