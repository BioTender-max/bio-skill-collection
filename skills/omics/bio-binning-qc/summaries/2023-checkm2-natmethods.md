---
schema: ../../bio-paper-schema.yaml
type: PaperSummary
skill: bio-binning-qc
title: "CheckM2: a rapid, scalable and accurate tool for assessing microbial genome quality using machine learning"
year: 2023
journal: "Nature Methods"
authors: "Chklovski A et al."
doi: "10.1038/s41592-023-01940-w"
url: "https://www.nature.com/articles/s41592-023-01940-w"
study_type: "methods"
sample_type: "microbial genomes and MAGs"
sequencing_platform: "not reported"
tools_used:
  - checkm2

tool_versions: "not reported"
datasets: "large genome collections used for model training and benchmarking"
workflow_summary: "CheckM2 uses machine-learning models to estimate genome completeness and contamination for microbial genomes and MAGs."
key_parameters: "not reported"
qc_steps: "completeness and contamination estimates via ML models"
outputs: "genome quality metrics and classifications"
code_availability: "not reported"
data_availability: "reported in article"
limitations: "model performance depends on training data diversity"
notes: "Core QC tool for binning workflows in this skill."
---

# Questionnaire Notes
- Metadata extracted from the Nature Methods article page.

# Protocol Summary
## Workflow
CheckM2 provides ML-based completeness and contamination estimates for microbial genomes and MAGs, enabling rapid QC of bins.

## QC and Outputs
Outputs include genome quality metrics used to gate bins for downstream analyses.

# Sources
- Nature Methods 2023 CheckM2 article.
