---
schema: ../../bio-paper-schema.yaml
type: PaperSummary
skill: bio-binning-qc
title: "SemiBin2: self-supervised metagenomic binning with short- and long-read data"
year: 2023
journal: "Bioinformatics"
authors: "Pan S et al."
doi: "10.1093/bioinformatics/btad209"
url: "https://pubmed.ncbi.nlm.nih.gov/37096854/"
study_type: "methods"
sample_type: "metagenomes (short- and long-read)"
sequencing_platform: "short-read and long-read"
tools_used:
  - semibin2

tool_versions: "not reported"
datasets: "multiple metagenome benchmark datasets"
workflow_summary: "SemiBin2 applies self-supervised learning to metagenomic binning for both short- and long-read assemblies."
key_parameters: "not reported"
qc_steps: "bin quality evaluation against benchmark datasets"
outputs: "improved binning performance and MAG recovery"
code_availability: "not reported"
data_availability: "not reported"
limitations: "performance depends on assembly and dataset characteristics"
notes: "Primary methods paper for SemiBin2; supports this skill's binning workflows."
---

# Questionnaire Notes
- Paper metadata extracted from the PubMed entry.

# Protocol Summary
## Workflow
SemiBin2 introduces a self-supervised learning approach for metagenomic binning that supports both short-read and long-read data.

## QC and Outputs
The paper reports improved binning performance on benchmark datasets, yielding higher-quality MAGs.

# Sources
- PubMed entry for SemiBin2 (Bioinformatics 2023).
