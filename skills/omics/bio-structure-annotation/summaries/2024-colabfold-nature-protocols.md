---
schema: ../../bio-paper-schema.yaml
type: PaperSummary
skill: bio-structure-annotation
title: "ColabFold: making protein folding accessible to all"
year: 2024
journal: "Nature Protocols"
authors: "Mirdita M et al."
doi: "10.1038/s41596-024-01015-0"
url: "https://www.nature.com/articles/s41596-024-01015-0"
study_type: "methods"
sample_type: "protein sequences"
sequencing_platform: "not reported"
tools_used:
  - colabfold

tool_versions: "ColabFold"
datasets: "protein sequences and MSAs"
workflow_summary: "ColabFold provides a streamlined workflow for protein structure prediction using fast MSA generation and AlphaFold-based inference."
key_parameters: "not reported"
qc_steps: "confidence metrics (pLDDT, PAE)"
outputs: "predicted protein structures and confidence scores"
code_availability: "reported in article"
data_availability: "reported in article"
limitations: "not reported"
notes: "Protocol-focused paper for ColabFold workflows."
---

# Questionnaire Notes
- Metadata from Nature Protocols 2024 article page.

# Protocol Summary
## Workflow
ColabFold provides accessible structure prediction pipelines with fast MSA generation and AlphaFold-based inference, delivering structure models and confidence metrics.

## QC and Outputs
QC relies on pLDDT and PAE confidence metrics; outputs are predicted structures with associated scores.

# Sources
- Nature Protocols 2024 ColabFold article.
