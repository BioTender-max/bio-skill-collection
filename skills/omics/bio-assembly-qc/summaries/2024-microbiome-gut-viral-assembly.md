---
schema: ../../bio-paper-schema.yaml
type: PaperSummary
skill: bio-assembly-qc
title: "Complementary insights into gut viral genomes recovered from short- and long-read metagenomes"
year: 2024
journal: "Microbiome"
authors: "Lee S et al."
doi: "10.1186/s40168-024-01981-z"
url: "https://microbiomejournal.biomedcentral.com/articles/10.1186/s40168-024-01981-z"
study_type: "benchmarking + application"
sample_type: "human fecal viromes"
sequencing_platform: "Illumina short-read and PacBio HiFi long-read"
tools_used:
  - megahit
  - flye (metaFlye)
  - spades (hybridSPAdes)

tool_versions: "not reported"
datasets: "95 VLP-enriched fecal samples, short- and long-read metagenomes"
workflow_summary: "Benchmark of short-read (MEGAHIT), long-read (metaFlye), and hybrid (hybridSPAdes) assemblers for viral genome recovery from paired Illumina and PacBio HiFi datasets."
key_parameters: "not reported"
qc_steps: "comparative evaluation of viral genome recovery and assembly quality"
outputs: "comparison of assembler recovery and quality for gut viral genomes"
code_availability: "not reported"
data_availability: "reported in the article and supplementary materials"
limitations: "viral recovery depends on read type and assembler choice"
notes: "Directly supports assembler selection for virome/metagenome assembly in this skill."
---

# Questionnaire Notes
- Tool usage, sample size, and sequencing platforms extracted from the Microbiome article.

# Protocol Summary
## Workflow
The study benchmarks MEGAHIT (short-read), metaFlye (long-read), and hybridSPAdes (hybrid) on paired Illumina and PacBio HiFi datasets to compare viral genome recovery from gut viromes.

## QC and Outputs
Assemblies are evaluated for viral genome recovery and quality, yielding comparative insights into assembler performance by read type.

# Sources
- Microbiome 2024 article on gut viral genome assembly benchmarking.
