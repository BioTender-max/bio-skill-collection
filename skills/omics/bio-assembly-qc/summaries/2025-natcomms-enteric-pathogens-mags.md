---
schema: ../../bio-paper-schema.yaml
type: PaperSummary
skill: bio-assembly-qc
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
  - megahit
  - quast

tool_versions: "not reported"
datasets: "international sewage metagenomes"
workflow_summary: "Metagenomes were assembled with MEGAHIT and assembly quality assessed with QUAST as part of pathogen genome recovery workflows."
key_parameters: "not reported"
qc_steps: "assembly quality assessment with QUAST"
outputs: "assembled metagenomic contigs used for downstream pathogen signature recovery"
code_availability: "not reported"
data_availability: "reported in the article"
limitations: "accuracy depends on assembly quality and sample complexity"
notes: "Includes explicit use of MEGAHIT and QUAST in a high-impact application."
---

# Questionnaire Notes
- Methods summary (MEGAHIT assembly, QUAST evaluation) extracted from the Nature Communications article description.

# Protocol Summary
## Workflow
International sewage metagenomes were assembled using MEGAHIT and evaluated with QUAST to support recovery of genetic signatures of enteric pathogens.

## QC and Outputs
QUAST was used to assess assembly quality, providing QC context for downstream pathogen analysis.

# Sources
- Nature Communications 2025 article on sewage metagenomes and pathogen signatures.
