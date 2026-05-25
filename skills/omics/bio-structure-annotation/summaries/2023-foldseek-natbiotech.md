---
schema: ../../bio-paper-schema.yaml
type: PaperSummary
skill: bio-structure-annotation
title: "Fast and accurate protein structure search with Foldseek"
year: 2023
journal: "Nature Biotechnology"
authors: "van Kempen M et al."
doi: "10.1038/s41587-023-01773-0"
url: "https://www.nature.com/articles/s41587-023-01773-0"
study_type: "methods"
sample_type: "protein structures"
sequencing_platform: "not reported"
tools_used:
  - foldseek

tool_versions: "Foldseek"
datasets: "protein structure databases"
workflow_summary: "Foldseek enables fast structure similarity search across large structure collections, supporting structure-based annotation and clustering."
key_parameters: "not reported"
qc_steps: "benchmarking against structural alignment baselines"
outputs: "structure search hits and annotations"
code_availability: "reported in article"
data_availability: "reported in article"
limitations: "not reported"
notes: "Core structure search tool for annotation workflows."
---

# Questionnaire Notes
- Metadata from the Nature Biotechnology article page.

# Protocol Summary
## Workflow
Foldseek performs rapid structure searches against large protein structure databases, enabling structure-based annotation and similarity analysis.

## QC and Outputs
Benchmarking against structural alignment baselines validates accuracy; outputs include ranked structure hits.

# Sources
- Nature Biotechnology 2023 Foldseek article.
