---
schema: ../../bio-paper-schema.yaml
type: PaperSummary
skill: bio-viromics
title: "Massive expansion of pig gut virome catalog using long-read metagenomics and long-read viral enrichment"
year: 2024
journal: "npj Biofilms and Microbiomes"
authors: "Tang K et al."
doi: "10.1038/s41522-024-00554-0"
url: "https://www.nature.com/articles/s41522-024-00554-0"
study_type: "application"
sample_type: "pig gut virome"
sequencing_platform: "long-read metagenomics"
tools_used:
  - virsorter2
  - checkv

tool_versions: "not reported"
datasets: "pig gut virome datasets with long-read enrichment"
workflow_summary: "The study uses VirSorter2 to identify viral sequences and CheckV to assess viral genome quality in a long-read virome cataloging pipeline."
key_parameters: "not reported"
qc_steps: "viral genome quality estimation with CheckV"
outputs: "expanded pig gut virome catalog"
code_availability: "not reported"
data_availability: "reported in article"
limitations: "not reported"
notes: "High-impact virome application using VirSorter2 and CheckV."
---

# Questionnaire Notes
- Tool usage inferred from the article text referencing VirSorter2 and CheckV.

# Protocol Summary
## Workflow
VirSorter2 is used to identify viral sequences from long-read metagenomes, followed by CheckV-based quality assessment to curate a pig gut virome catalog.

## QC and Outputs
CheckV provides quality estimates for viral genomes, supporting curation of the expanded virome catalog.

# Sources
- npj Biofilms and Microbiomes 2024 pig gut virome article.
