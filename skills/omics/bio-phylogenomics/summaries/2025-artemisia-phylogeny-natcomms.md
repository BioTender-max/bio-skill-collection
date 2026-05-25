---
schema: ../../bio-paper-schema.yaml
type: PaperSummary
skill: bio-phylogenomics
title: "The origin and diversification of Artemisia (Asteraceae): Robust phylogeny and temporal framework"
year: 2025
journal: "Nature Communications"
authors: "Qin X et al."
doi: "10.1038/s41467-025-62962-8"
url: "https://www.nature.com/articles/s41467-025-62962-8"
study_type: "application"
sample_type: "plant phylogenomics"
sequencing_platform: "not reported"
tools_used:
  - iqtree

tool_versions: "IQ-TREE"
datasets: "Artemisia genomic datasets"
workflow_summary: "Phylogenomic inference uses IQ-TREE to reconstruct maximum-likelihood trees for Artemisia diversification analyses."
key_parameters: "not reported"
qc_steps: "bootstrap support and model selection"
outputs: "phylogenetic trees and divergence time estimates"
code_availability: "reported in article"
data_availability: "reported in article"
limitations: "not reported"
notes: "Recent Nature Communications study explicitly using IQ-TREE."
---

# Questionnaire Notes
- Methods mention IQ-TREE for phylogeny inference.

# Protocol Summary
## Workflow
IQ-TREE is used to infer maximum-likelihood phylogenies that underpin diversification and timing analyses for Artemisia.

## QC and Outputs
Bootstrap support and model fit provide QC for tree robustness.

# Sources
- Nature Communications 2025 Artemisia phylogeny article.
