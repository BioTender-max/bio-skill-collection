---
schema: ../../bio-paper-schema.yaml
type: PaperSummary
skill: bio-annotation
title: "Integrating taxonomic signals from MAGs and contigs improves read annotation and taxonomic profiling of metagenomes"
year: 2024
journal: "Nature Communications"
authors: "Hauptfeld E et al."
doi: "10.1038/s41467-024-47155-1"
url: "https://www.nature.com/articles/s41467-024-47155-1"
study_type: "methods + application"
sample_type: "groundwater metagenomes"
sequencing_platform: "shotgun metagenomics"
tools_used:
  - diamond
tool_versions: "not reported"
datasets: "CAMI2 mouse gut datasets; groundwater metagenomes"
workflow_summary: "Reads are mapped to contigs, contigs are binned into MAGs, MAGs/contigs are annotated with CAT/BAT, and unassigned reads are annotated via DIAMOND against protein databases to improve taxonomic profiles."
key_parameters: "RAT -mcr/-mc modes; DIAMOND for read annotation; CAT/BAT for contigs/MAGs"
qc_steps: "recommend using high-quality assemblies and MAGs with low contamination (<10%)"
outputs: "integrated taxonomic profiles with improved sensitivity/precision"
code_availability: "CAT/BAT/RAT in CAT_pack (GitHub)"
data_availability: "reported in paper and supplements"
limitations: "accuracy depends on assembly/binning quality and database completeness"
notes: "Direct use of DIAMOND for homology-based read annotation aligns with this skill."
---

# Questionnaire Notes
- Extracted from the Nature Communications 2024 RAT paper.
- Focus on DIAMOND-based read annotation for taxonomy inference.

# Protocol Summary
## Workflow
RAT integrates contig/MAG annotations and direct read annotation. Reads are mapped to contigs, contigs are binned into MAGs, and CAT/BAT provide annotations; remaining reads are annotated with DIAMOND against protein databases to refine taxonomic profiles.

## QC and Outputs
The authors recommend using high-quality assemblies and low-contamination MAGs. Outputs are integrated taxonomic profiles with improved sensitivity and precision in complex metagenomes.

# Sources
- Nature Communications article and methods.
- PubMed abstract and figure captions.
