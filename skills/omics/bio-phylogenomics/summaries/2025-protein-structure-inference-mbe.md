---
schema: ../../bio-paper-schema.yaml
type: PaperSummary
skill: bio-phylogenomics
title: "Inferring deep evolutionary relationships with large-scale protein structure analyses"
year: 2025
journal: "Molecular Biology and Evolution"
authors: "Putnam NH et al."
doi: "10.1093/molbev/msaf149"
url: "https://academic.oup.com/mbe/article/42/7/msaf149/8149537"
study_type: "methods + application"
sample_type: "protein structure phylogenomics"
sequencing_platform: "not reported"
tools_used:
  - iqtree

tool_versions: "IQ-TREE"
datasets: "large-scale protein structure datasets"
workflow_summary: "Phylogenetic trees are reconstructed with IQ-TREE to support structure-based evolutionary analyses."
key_parameters: "not reported"
qc_steps: "bootstrap support and model selection"
outputs: "structure-informed phylogenetic trees"
code_availability: "reported in article"
data_availability: "reported in article"
limitations: "not reported"
notes: "Uses IQ-TREE for ML tree inference in a 2025 MBE paper."
---

# Questionnaire Notes
- Methods note IQ-TREE for tree reconstruction.

# Protocol Summary
## Workflow
IQ-TREE is used to infer maximum-likelihood phylogenies for structure-based evolutionary analyses.

## QC and Outputs
Bootstrap support and model selection underpin tree quality and robustness.

# Sources
- Molecular Biology and Evolution 2025 article.
