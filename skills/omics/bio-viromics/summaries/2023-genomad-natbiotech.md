---
schema: ../../bio-paper-schema.yaml
type: PaperSummary
skill: bio-viromics
title: "Identification of mobile genetic elements with geNomad"
year: 2023
journal: "Nature Biotechnology"
authors: "Camargo AP et al."
doi: "10.1038/s41587-023-01953-y"
url: "https://pubmed.ncbi.nlm.nih.gov/37991586/"
study_type: "methods"
sample_type: "mobile genetic elements and viral contigs"
sequencing_platform: "not reported"
tools_used:
  - genomad

tool_versions: "not reported"
datasets: "benchmark datasets for viral/MGE identification"
workflow_summary: "geNomad introduces a framework for detecting viral and other mobile genetic elements in genomic and metagenomic datasets."
key_parameters: "not reported"
qc_steps: "benchmarking against reference datasets"
outputs: "classified viral and MGE contigs"
code_availability: "https://github.com/apcamargo/genomad"
data_availability: "reported in article"
limitations: "not reported"
notes: "Core viromics method for viral contig identification."
---

# Questionnaire Notes
- Metadata from PubMed and Nature Biotechnology listing.

# Protocol Summary
## Workflow
geNomad provides a workflow to identify viral and other mobile genetic elements in genomic and metagenomic assemblies using built-in classifiers and reference models.

## QC and Outputs
Benchmarking against reference datasets supports quality assessment of viral contig calls.

# Sources
- Nature Biotechnology 2023 geNomad paper (PubMed).
