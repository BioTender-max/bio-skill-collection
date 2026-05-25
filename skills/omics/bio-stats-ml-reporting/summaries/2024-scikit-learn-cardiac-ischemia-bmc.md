---
schema: ../../bio-paper-schema.yaml
type: PaperSummary
skill: bio-stats-ml-reporting
title: "The use of scikit-learn and Imbalanced-learn to improve a classification method for emergency identification of cardiac ischemia"
year: 2024
journal: "BMC Bioinformatics"
authors: "Paez EA et al."
doi: "10.1186/s12859-024-05716-5"
url: "https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-024-05716-5"
study_type: "methods + application"
sample_type: "clinical ECG data"
sequencing_platform: "not applicable"
tools_used:
  - scikit-learn

tool_versions: "not reported"
datasets: "clinical datasets for ischemia classification"
workflow_summary: "The study builds and evaluates machine-learning classifiers using scikit-learn, with imbalance handling for emergency cardiac ischemia detection."
key_parameters: "not reported"
qc_steps: "cross-validation and evaluation metrics"
outputs: "classification models and performance metrics"
code_availability: "reported in article"
data_availability: "reported in article"
limitations: "reported in article"
notes: "Direct scikit-learn usage in a biomedical classification workflow."
---

# Questionnaire Notes
- Metadata and abstract from BMC Bioinformatics article.

# Protocol Summary
## Workflow
scikit-learn classifiers are trained and evaluated with imbalance-aware preprocessing to improve emergency ischemia classification.

## QC and Outputs
QC includes cross-validation and standard performance metrics; outputs are model performance summaries.

# Sources
- BMC Bioinformatics 2024 scikit-learn article.
