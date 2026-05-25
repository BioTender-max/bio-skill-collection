---
schema: ../../bio-paper-schema.yaml
type: PaperSummary
skill: bio-binning-qc
title: "Recovery of genetic signatures of enteric pathogens from international sewage monitoring"
year: 2025
journal: "Nature Communications"
authors: "Panton J et al."
doi: "10.1038/s41467-025-59792-7"
url: "https://www.nature.com/articles/s41467-025-59792-7"
study_type: "application"
sample_type: "international sewage metagenomes"
sequencing_platform: "shotgun metagenomics"
tools_used:
  - metabat2
  - checkm2

tool_versions: "not reported"
datasets: "international sewage metagenomes"
workflow_summary: "MAGs were recovered from sewage metagenomes using MetaBAT2 and quality-checked with CheckM2."
key_parameters: "not reported"
qc_steps: "CheckM2 completeness/contamination estimates"
outputs: "MAGs supporting pathogen signature analysis"
code_availability: "not reported"
data_availability: "reported in the article"
limitations: "bin quality depends on assembly depth and community complexity"
notes: "Explicit MetaBAT2 and CheckM2 usage in a high-impact, 2025 application."
---

# Questionnaire Notes
- Methods summary extracted from the Nature Communications article description.

# Protocol Summary
## Workflow
Sewage metagenomes were binned with MetaBAT2 and checked with CheckM2 as part of pathogen surveillance workflows.

## QC and Outputs
CheckM2 QC metrics support selection of higher-quality MAGs for downstream analysis.

# Sources
- Nature Communications 2025 article on sewage metagenomes and enteric pathogen signatures.
