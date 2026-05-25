---
schema: ../../bio-paper-schema.yaml
type: PaperSummary
skill: bio-gene-calling
title: "Soil metagenomes as a strategic resource for novel microbial genes and biochemistry"
year: 2025
journal: "Nature Biotechnology"
authors: "Nayfach S et al."
doi: "10.1038/s41587-025-02810-w"
url: "https://www.nature.com/articles/s41587-025-02810-w"
study_type: "resource"
sample_type: "soil metagenomes"
sequencing_platform: "long-read metagenomics"
tools_used:
  - trnascan-se

tool_versions: "tRNAscan-SE 2.0.9"
datasets: "large-scale soil metagenome assemblies"
workflow_summary: "Genome annotation includes tRNA gene prediction using tRNAscan-SE as part of a large-scale soil metagenome resource."
key_parameters: "not reported"
qc_steps: "reported in article"
outputs: "tRNA annotations and genome features"
code_availability: "reported in article"
data_availability: "reported in article"
limitations: "annotations depend on assembly quality"
notes: "Explicit tRNAscan-SE usage listed in tool and code availability for a 2025 high-impact study."
---

# Questionnaire Notes
- Tool list and code availability for the Nature Biotechnology 2025 soil metagenome resource includes tRNAscan-SE 2.0.9.

# Protocol Summary
## Workflow
tRNAscan-SE is used to identify tRNA genes during annotation of soil metagenome assemblies, supporting downstream functional analysis.

## QC and Outputs
Outputs include tRNA annotations and genome features integrated into the soil metagenome resource.

# Sources
- Nature Biotechnology 2025 soil metagenome resource paper.
