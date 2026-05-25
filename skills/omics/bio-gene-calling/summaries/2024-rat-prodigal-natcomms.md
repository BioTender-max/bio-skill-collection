---
schema: ../../bio-paper-schema.yaml
type: PaperSummary
skill: bio-gene-calling
title: "Integrating taxonomic signals from MAGs and contigs improves read annotation and taxonomic profiling of metagenomes"
year: 2024
journal: "Nature Communications"
authors: "Hauptfeld E et al."
doi: "10.1038/s41467-024-47155-1"
url: "https://www.nature.com/articles/s41467-024-47155-1"
study_type: "methods + application"
sample_type: "groundwater metagenomes"
sequencing_platform: "shotgun metagenomics"
tools_used:
  - prodigal-gv

tool_versions: "not reported"
datasets: "CAMI2 mouse gut datasets; groundwater metagenomes"
workflow_summary: "CAT/BAT predict ORFs using Prodigal before taxonomic annotation; RAT integrates contig/MAG and read-level annotations."
key_parameters: "not reported"
qc_steps: "reported in article"
outputs: "ORFs, taxonomic profiles, and read annotations"
code_availability: "CAT/BAT/RAT in CAT_pack"
data_availability: "reported in article"
limitations: "dependent on assembly and database completeness"
notes: "Explicit Prodigal usage for ORF prediction in a high-impact 2024 study."
---

# Questionnaire Notes
- Methods and notes report CAT/BAT ORF prediction with Prodigal.

# Protocol Summary
## Workflow
CAT/BAT predict ORFs with Prodigal as part of contig/MAG annotation; RAT integrates these annotations with read-level homology search to improve taxonomic profiling.

## QC and Outputs
The workflow outputs ORFs and taxonomic profiles; QC depends on assembly and database quality.

# Sources
- Nature Communications 2024 RAT paper.
