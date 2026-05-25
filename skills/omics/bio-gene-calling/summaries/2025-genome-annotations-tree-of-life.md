---
schema: ../../bio-paper-schema.yaml
type: PaperSummary
skill: bio-gene-calling
title: "Building better genome annotations across the tree of life"
year: 2025
journal: "Genome Research"
authors: "Devine H et al."
doi: "10.1101/gr.280377.124"
url: "https://genome.cshlp.org/content/early/2025/05/12/gr.280377.124"
study_type: "benchmarking"
sample_type: "diverse eukaryotic genomes"
sequencing_platform: "multi-omic evidence"
tools_used:
  - braker
  - augustus

tool_versions: "BRAKER3"
datasets: "cross-phyla eukaryotic genomes"
workflow_summary: "The study evaluates genome annotation workflows across diverse lineages and highlights the role of BRAKER3 and AUGUSTUS in producing high-quality annotations."
key_parameters: "not reported"
qc_steps: "benchmarking gene model quality across taxa"
outputs: "comparative evaluation of gene annotations"
code_availability: "reported in article"
data_availability: "reported in article"
limitations: "results depend on input evidence and taxonomic breadth"
notes: "High-impact benchmarking study using BRAKER3/AUGUSTUS for gene calling across the tree of life."
---

# Questionnaire Notes
- Metadata from the Genome Research early-access page.

# Protocol Summary
## Workflow
The paper benchmarks genome annotation pipelines across taxonomic diversity, using BRAKER3 and AUGUSTUS to generate gene models and compare outcomes across lineages.

## QC and Outputs
QC relies on comparative benchmarking of gene model quality, emphasizing annotation robustness across broad phylogenetic ranges.

# Sources
- Genome Research 2025 article on tree-of-life genome annotations.
