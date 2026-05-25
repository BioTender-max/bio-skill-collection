---
schema: ../../bio-paper-schema.yaml
type: PaperSummary
skill: bio-gene-calling
title: "BRAKER3: Fully automated genome annotation using RNA-seq and protein evidence with GeneMark-ETP, AUGUSTUS, and TSEBRA"
year: 2024
journal: "Genome Research"
authors: "Gabriel L et al."
doi: "10.1101/gr.278090.123"
url: "https://genome.cshlp.org/lookup/doi/10.1101/gr.278090.123"
study_type: "methods"
sample_type: "eukaryotic genomes"
sequencing_platform: "RNA-seq + protein evidence"
tools_used:
  - braker
  - augustus

tool_versions: "BRAKER3 (2024 release)"
datasets: "11 benchmark eukaryotic genomes"
workflow_summary: "BRAKER3 integrates GeneMark-ETP with AUGUSTUS and TSEBRA to annotate protein-coding genes using RNA-seq and protein evidence, with iterative model training per genome."
key_parameters: "not reported"
qc_steps: "benchmarking with transcript-level F1 and comparative evaluation against other pipelines"
outputs: "annotated protein-coding gene models"
code_availability: "BRAKER3 GitHub and container images"
data_availability: "reported in article"
limitations: "performance depends on evidence quality and genome complexity"
notes: "Core gene-calling pipeline that directly uses AUGUSTUS and BRAKER3."
---

# Questionnaire Notes
- Metadata and abstract from Genome Research.

# Protocol Summary
## Workflow
BRAKER3 combines GeneMark-ETP, AUGUSTUS, and TSEBRA to train and predict eukaryotic gene models using RNA-seq and protein evidence. The pipeline iteratively fits genome-specific parameters and outputs protein-coding gene annotations.

## QC and Outputs
Accuracy is evaluated using transcript-level metrics and benchmarking across multiple genomes, producing final gene models suitable for downstream annotation.

# Sources
- Genome Research 2024 BRAKER3 article.
