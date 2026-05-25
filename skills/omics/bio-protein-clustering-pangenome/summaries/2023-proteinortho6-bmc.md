---
schema: ../../bio-paper-schema.yaml
type: PaperSummary
skill: bio-protein-clustering-pangenome
title: "Proteinortho6: faster large-scale orthology detection using MMseqs2"
year: 2023
journal: "BMC Bioinformatics"
authors: "Lemke S et al."
doi: "10.1186/s12859-023-05298-6"
url: "https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-023-05298-6"
study_type: "methods"
sample_type: "orthology detection across genomes"
sequencing_platform: "not reported"
tools_used:
  - proteinortho
  - mmseqs2

tool_versions: "Proteinortho6"
datasets: "orthology benchmarks"
workflow_summary: "Proteinortho6 integrates MMseqs2 to accelerate orthology detection at large scale for pangenome and orthogroup analysis."
key_parameters: "not reported"
qc_steps: "benchmarking accuracy and runtime"
outputs: "orthogroups and pangenome matrices"
code_availability: "reported in article"
data_availability: "reported in article"
limitations: "not reported"
notes: "Directly aligns with protein clustering and pangenome workflows."
---

# Questionnaire Notes
- Metadata from BMC Bioinformatics article.

# Protocol Summary
## Workflow
Proteinortho6 integrates MMseqs2 for rapid orthology detection across many genomes, enabling large-scale protein clustering and pangenome construction.

## QC and Outputs
Benchmarking assesses accuracy and runtime performance, producing orthogroups and pangenome matrices.

# Sources
- BMC Bioinformatics 2023 Proteinortho6 article.
