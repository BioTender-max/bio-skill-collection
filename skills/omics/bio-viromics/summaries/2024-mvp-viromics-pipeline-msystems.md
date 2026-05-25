---
schema: ../../bio-paper-schema.yaml
type: PaperSummary
skill: bio-viromics
title: "MVP: a modular viromics pipeline to identify, filter, cluster, annotate, and bin viruses from metagenomes"
year: 2024
journal: "mSystems"
authors: "Coclet C et al."
doi: "10.1128/msystems.00888-24"
url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC11498083/"
study_type: "methods"
sample_type: "metagenomes and viromes"
sequencing_platform: "not reported"
tools_used:
  - genomad
  - checkv

tool_versions: "not reported"
datasets: "metagenome case study (wetland sediment)"
workflow_summary: "MVP v1.0 integrates geNomad for viral detection and CheckV for quality assessment in a modular pipeline covering viral identification, clustering, annotation, and binning."
key_parameters: "not reported"
qc_steps: "CheckV quality estimates for viral contigs"
outputs: "viral contig catalogs, annotations, and summary reports"
code_availability: "https://gitlab.com/ccoclet/mvp"
data_availability: "reported in article"
limitations: "not reported"
notes: "Comprehensive viromics pipeline using geNomad and CheckV, aligned with this skill."
---

# Questionnaire Notes
- Metadata and tool integration details from the mSystems 2024 MVP paper (PMC).

# Protocol Summary
## Workflow
MVP v1.0 is a modular viromics pipeline that integrates geNomad for viral detection and CheckV for genome quality assessment, with modules for clustering, annotation, and binning.

## QC and Outputs
CheckV provides quality estimates that guide filtering and reporting of viral contigs across the pipeline.

# Sources
- mSystems 2024 MVP pipeline paper (PMC).
