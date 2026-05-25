---
schema: ../../bio-paper-schema.yaml
type: PaperSummary
skill: bio-reads-qc-mapping
title: "Efficient end-to-end long-read sequence mapping using minimap2-fpga integrated with hardware accelerated chaining"
year: 2023
journal: "Scientific Reports"
authors: "Jin H et al."
doi: "10.1038/s41598-023-47354-8"
url: "https://www.nature.com/articles/s41598-023-47354-8"
study_type: "methods"
sample_type: "long-read mapping benchmarks"
sequencing_platform: "long-read (ONT/PacBio)"
tools_used:
  - minimap2

tool_versions: "minimap2"
datasets: "long-read mapping benchmark datasets"
workflow_summary: "Accelerated minimap2 mapping implemented on FPGA hardware; evaluates mapping throughput and accuracy for long-read datasets."
key_parameters: "not reported"
qc_steps: "mapping accuracy and throughput comparisons"
outputs: "accelerated mapping workflows and performance metrics"
code_availability: "not reported"
data_availability: "reported in article"
limitations: "hardware-specific implementation"
notes: "Demonstrates minimap2 usage in long-read mapping workflows, relevant to this skill’s mapping step."
---

# Questionnaire Notes
- Metadata extracted from the Scientific Reports article page.

# Protocol Summary
## Workflow
The study implements minimap2 on FPGA hardware to accelerate long-read mapping, reporting throughput and accuracy gains relative to CPU implementations.

## QC and Outputs
QC focuses on mapping accuracy and performance benchmarks for long-read datasets.

# Sources
- Scientific Reports 2023 Minimap2-FPGA article.
