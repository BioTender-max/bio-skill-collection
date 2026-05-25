---
schema: ../../bio-paper-schema.yaml
type: PaperSummary
skill: bio-gene-calling
title: "A global catalog of whole genome sequences from the soil microbiome"
year: 2023
journal: "Nature Communications"
authors: "Leigh MB et al."
doi: "10.1038/s41467-023-43000-z"
url: "https://www.nature.com/articles/s41467-023-43000-z"
study_type: "resource"
sample_type: "soil metagenomes"
sequencing_platform: "shotgun metagenomics"
tools_used:
  - prodigal-gv

tool_versions: "Prodigal v2.6.3"
datasets: "soil metagenome assemblies"
workflow_summary: "The study predicts proteins from soil MAGs using Prodigal as part of building a global soil microbiome genome catalog."
key_parameters: "not reported"
qc_steps: "reported in article"
outputs: "predicted proteins and genome annotations"
code_availability: "reported in article"
data_availability: "reported in article"
limitations: "annotation quality depends on assembly completeness"
notes: "Prodigal is used for gene prediction in a large-scale soil microbiome resource."
---

# Questionnaire Notes
- Methods mention protein prediction with Prodigal in the soil genome catalog paper.

# Protocol Summary
## Workflow
Assemblies and MAGs from soil metagenomes are processed for gene prediction with Prodigal, providing protein sequences used in downstream annotation and cataloging.

## QC and Outputs
Outputs include predicted proteins and genome annotations used to build the soil microbiome catalog.

# Sources
- Nature Communications 2023 soil microbiome catalog article.
