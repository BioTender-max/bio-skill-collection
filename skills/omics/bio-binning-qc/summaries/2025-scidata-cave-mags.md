---
schema: ../../bio-paper-schema.yaml
type: PaperSummary
skill: bio-binning-qc
title: "Reconstruction of 1,979 high-quality prokaryotic MAGs from 297 subterranean caves around the world"
year: 2025
journal: "Scientific Data"
authors: "Zheng R et al."
doi: "10.1038/s41597-025-04460-8"
url: "https://www.nature.com/articles/s41597-025-04460-8"
study_type: "resource"
sample_type: "subterranean cave metagenomes"
sequencing_platform: "shotgun metagenomics"
tools_used:
  - metabat2
  - semibin2
  - checkm2

tool_versions: "not reported"
datasets: "297 cave metagenomes"
workflow_summary: "Reads were assembled and binned with MetaBAT2 and SemiBin2 as part of a large-scale MAG reconstruction pipeline for cave metagenomes."
key_parameters: "not reported"
qc_steps: "quality assessment and MIMAG thresholds for MAGs"
outputs: "1,979 high-quality prokaryotic MAGs"
code_availability: "not reported"
data_availability: "reported in the article"
limitations: "bin quality depends on assembly depth and sample complexity"
notes: "Large-scale application using MetaBAT2 and SemiBin2, aligned with binning/QC skill requirements."
---

# Questionnaire Notes
- Pipeline steps extracted from Scientific Data methods lines describing assembly and binning tools.

# Protocol Summary
## Workflow
Metagenomic reads from 297 caves were assembled and binned using MetaBAT2 and SemiBin2; downstream QC applied MIMAG-style thresholds to retain high-quality MAGs.

## QC and Outputs
Quality assessment and filtering yielded 1,979 high-quality MAGs from global cave environments.

# Sources
- Scientific Data 2025 article describing the cave MAG dataset and pipeline.
