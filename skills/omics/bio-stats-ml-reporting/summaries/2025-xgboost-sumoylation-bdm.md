---
schema: ../../bio-paper-schema.yaml
type: PaperSummary
skill: bio-stats-ml-reporting
title: "Deep learning-based feature extraction and XGBoost for sumoylation site prediction"
year: 2025
journal: "BioData Mining"
authors: "Miao Z et al."
doi: "10.1186/s13040-025-00409-8"
url: "https://biodatamining.biomedcentral.com/articles/10.1186/s13040-025-00409-8"
study_type: "methods"
sample_type: "protein sequence datasets"
sequencing_platform: "not applicable"
tools_used:
  - xgboost

tool_versions: "not reported"
datasets: "sumoylation site prediction benchmarks"
workflow_summary: "Deep feature extraction is combined with XGBoost classification to predict sumoylation sites in proteins."
key_parameters: "not reported"
qc_steps: "cross-validation and evaluation metrics"
outputs: "model performance metrics and predictions"
code_availability: "reported in article"
data_availability: "reported in article"
limitations: "reported in article"
notes: "XGBoost used for bioinformatics site prediction tasks."
---

# Questionnaire Notes
- Metadata from BioData Mining 2025 article.

# Protocol Summary
## Workflow
Deep learning features are extracted from protein sequences and passed to XGBoost classifiers for sumoylation site prediction.

## QC and Outputs
QC includes cross-validation and standard ML evaluation metrics; outputs are prediction performance results.

# Sources
- BioData Mining 2025 XGBoost sumoylation study.
