---
schema: ../../bio-paper-schema.yaml
type: PaperSummary
skill: bio-reads-qc-mapping
title: "Systematic assessment of long-read RNA-seq methods for transcript identification and quantification"
year: 2024
journal: "Nature Methods"
authors: "Gao Y et al."
doi: "10.1038/s41592-024-02298-3"
url: "https://www.nature.com/articles/s41592-024-02298-3"
study_type: "benchmarking"
sample_type: "human RNA-seq"
sequencing_platform: "long-read (ONT/PacBio)"
tools_used:
  - minimap2

tool_versions: "not reported"
datasets: "long-read RNA-seq benchmark datasets"
workflow_summary: "Benchmark of long-read RNA-seq workflows for transcript identification/quantification that uses minimap2 for read alignment to reference genomes."
key_parameters: "not reported"
qc_steps: "alignment and quantification accuracy evaluation"
outputs: "performance comparisons for long-read RNA-seq methods"
code_availability: "not reported"
data_availability: "reported in article"
limitations: "results depend on library prep and sequencing platform"
notes: "Provides a high-impact example of minimap2 usage in long-read alignment pipelines."
---

# Questionnaire Notes
- Metadata extracted from the Nature Methods article page.

# Protocol Summary
## Workflow
The study compares long-read RNA-seq pipelines, using minimap2 for alignment as part of transcript identification and quantification benchmarks.

## QC and Outputs
QC focuses on alignment accuracy and transcript quantification performance across methods.

# Sources
- Nature Methods 2024 benchmarking paper.
