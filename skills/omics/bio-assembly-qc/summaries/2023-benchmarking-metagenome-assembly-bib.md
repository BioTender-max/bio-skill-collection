---
schema: ../../bio-paper-schema.yaml
type: PaperSummary
skill: bio-assembly-qc
title: "Benchmarking genome assembly methods on metagenomic sequencing data"
year: 2023
journal: "Briefings in Bioinformatics"
authors: "Zhang Z et al."
doi: "10.1093/bib/bbad087"
url: "https://academic.oup.com/bib/article/24/2/bbad087/7077274"
study_type: "benchmarking"
sample_type: "simulated, mock, and human gut metagenomes"
sequencing_platform: "Illumina/BGISEQ short-read; PacBio/ONT long-read; linked-read"
tools_used:
  - megahit
  - spades (metaSPAdes)
  - flye (metaFlye)
  - other assemblers

tool_versions: "not reported"
datasets: "simulation, mock communities, human gut microbiomes"
workflow_summary: "Benchmark of 19 assembly tools across short-, linked-, long-read, and hybrid datasets with comparative evaluation of contiguity and MAG recovery."
key_parameters: "not reported"
qc_steps: "assembly quality metrics and MAG recovery comparisons"
outputs: "comparative performance guidance for assembler selection"
code_availability: "not reported"
data_availability: "not reported"
limitations: "results depend on dataset characteristics and sequencing technology"
notes: "Highlights MEGAHIT and metaSPAdes performance differences across depth/complexity; includes long-read assemblers like metaFlye."
---

# Questionnaire Notes
- Tool mentions and benchmark scope extracted from the Briefings in Bioinformatics article abstract and introduction.

# Protocol Summary
## Workflow
The study benchmarks 19 metagenome assemblers across simulated, mock, and human gut datasets spanning short-read, linked-read, and long-read platforms. It reports comparative performance and practical guidance for assembler selection, including short-read (MEGAHIT, metaSPAdes) and long-read (metaFlye) methods.

## QC and Outputs
Assembly quality metrics and MAG recovery comparisons are used to assess tradeoffs between contiguity, completeness, and technology choice.

# Sources
- Briefings in Bioinformatics 2023 benchmarking paper.
