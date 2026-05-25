<div align="center">
  <a href="https://github.com/BioTender-max/awesome-bio-agent-skills">
    <img src="assets/banner.png" alt="Awesome Bio Agent Skills" width="800"/>
  </a>
</div>

<div align="center">

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![Skills](https://img.shields.io/badge/skills-1%2C306-22d3ee?style=flat-square)](https://github.com/BioTender-max/awesome-bio-agent-skills/blob/main/bioskill_index_v2.csv)
[![Categories](https://img.shields.io/badge/categories-15-818cf8?style=flat-square)](#contents)
[![Sources](https://img.shields.io/badge/sources-11_repos-34d399?style=flat-square)](#sources)
[![License](https://img.shields.io/badge/license-CC0-f59e0b?style=flat-square)](LICENSE)
[![Lint](https://github.com/BioTender-max/awesome-bio-agent-skills/actions/workflows/awesome-lint.yml/badge.svg)](https://github.com/BioTender-max/awesome-bio-agent-skills/actions/workflows/awesome-lint.yml)

</div>

<br/>

# Awesome Bio Agent Skills

> A curated collection of AI agent skills for biomedical research, covering genomics, proteomics, single-cell analysis, clinical AI, and protein design.

1,306 deduplicated skills from 11 open-source repositories, organized into 15 categories. Each skill is a self-contained `SKILL.md` folder compatible with Claude-based agent frameworks ([OpenClaw](https://github.com/openclaw/openclaw), [NanoClaw](https://github.com/qwibitai/nanoclaw), [Biomni](https://github.com/Phylo-AI/biomni)).

---

## Contents

- [Genomics](#genomics)
- [Proteomics](#proteomics)
- [Single-Cell Analysis](#single-cell-analysis)
- [Biology and AI](#biology-and-ai)
- [Clinical and Medical](#clinical-and-medical)
- [Transcriptomics](#transcriptomics)
- [Database Query](#database-query)
- [Multi-Omics Integration](#multi-omics-integration)
- [Bioinformatics Utilities](#bioinformatics-utilities)
- [Visualization](#visualization)
- [Workflow Orchestration](#workflow-orchestration)
- [Epigenomics](#epigenomics)
- [Pathway Analysis](#pathway-analysis)
- [Metagenomics](#metagenomics)
- [Protein Design](#protein-design)
- [Sources](#sources)

---

## Genomics

> 472 skills — WGS/WES analysis, variant annotation, GWAS, CNV, structural variants, haplotype phasing, genome assembly.

<details>
<summary>View all 472 skills</summary>

| Skill | Source | Description |
|-------|--------|-------------|
| [alignment-and-mapping](skills/bioclaw_hub/alignment-and-mapping/) | bioclaw_hub | Workflow for read alignment, sorting, indexing, mapping statistics, and downstream-ready alignment artifacts. |
| [bam-processing](skills/bioskills/bam-processing/) | bioskills | BAM file processing including sorting, indexing, duplicate marking, and quality filtering. |
| [bcftools-variant-filtering](skills/bioskills/bcftools-variant-filtering/) | bioskills | Variant filtering and manipulation using BCFtools with customizable quality thresholds. |
| [chip-seq-analysis](skills/bioskills/chip-seq-analysis/) | bioskills | ChIP-seq peak calling, quality control, and downstream enrichment analysis. |
| [cnv-analysis](skills/bioskills/cnv-analysis/) | bioskills | Copy number variation detection and visualization from WGS or array data. |
| [copy-number-variation](skills/bioclaw_hub/copy-number-variation/) | bioclaw_hub | CNV calling from sequencing data with segmentation and annotation. |
| [de-novo-assembly](skills/bioskills/de-novo-assembly/) | bioskills | De novo genome assembly using short or long reads with quality assessment. |
| [deepvariant-calling](skills/bioskills/deepvariant-calling/) | bioskills | Deep learning-based variant calling using DeepVariant for SNPs and indels. |
| [exome-sequencing-analysis](skills/bioskills/exome-sequencing-analysis/) | bioskills | End-to-end whole exome sequencing analysis from raw reads to annotated variants. |
| [fastq-quality-control](skills/bioskills/fastq-quality-control/) | bioskills | FASTQ quality assessment and trimming using FastQC and Trimmomatic. |
| [gatk-variant-calling](skills/bioskills/gatk-variant-calling/) | bioskills | GATK best-practices variant calling pipeline for germline SNPs and indels. |
| [genome-annotation](skills/bioskills/genome-annotation/) | bioskills | Structural and functional genome annotation using Prokka, AUGUSTUS, or MAKER. |
| [genome-assembly-qc](skills/bioskills/genome-assembly-qc/) | bioskills | Assembly quality assessment with QUAST, BUSCO, and N50 statistics. |
| [genome-browser-visualization](skills/bioskills/genome-browser-visualization/) | bioskills | Genome track visualization using IGV, UCSC Genome Browser, or JBrowse. |
| [genome-comparison](skills/bioskills/genome-comparison/) | bioskills | Whole-genome alignment and synteny analysis between species or strains. |
| [genome-indexing](skills/bioskills/genome-indexing/) | bioskills | Reference genome indexing for alignment tools including BWA, Bowtie2, and STAR. |
| [genotype-imputation](skills/bioskills/genotype-imputation/) | bioskills | Genotype imputation using reference panels with IMPUTE2 or Beagle. |
| [gwas-analysis](skills/bioskills/gwas-analysis/) | bioskills | Genome-wide association study analysis including QC, association testing, and Manhattan plots. |
| [gwas-pipeline](skills/clawbio/gwas-pipeline/) | clawbio | End-to-end GWAS pipeline with population stratification correction and fine-mapping. |
| [haplotype-phasing](skills/bioskills/haplotype-phasing/) | bioskills | Haplotype phasing from sequencing data using SHAPEIT or WhatsHap. |
| [indel-calling](skills/bioskills/indel-calling/) | bioskills | Insertion and deletion variant calling with filtering and annotation. |
| [long-read-assembly](skills/bioskills/long-read-assembly/) | bioskills | Genome assembly from PacBio or Oxford Nanopore long reads using Flye or Canu. |
| [long-read-variant-calling](skills/bioskills/long-read-variant-calling/) | bioskills | Variant calling from long-read sequencing data using Clair3 or Medaka. |
| [mendelian-randomization](skills/sciagent/mendelian-randomization/) | sciagent | Two-sample Mendelian randomization analysis for causal inference between traits. |
| [mitochondrial-variant-calling](skills/bioskills/mitochondrial-variant-calling/) | bioskills | Mitochondrial genome variant calling with haplogroup assignment. |
| [pangenome-analysis](skills/bioskills/pangenome-analysis/) | bioskills | Pangenome construction and core/accessory genome analysis. |
| [pharmacogenomics](skills/bioskills/pharmacogenomics/) | bioskills | Pharmacogenomic variant interpretation for drug response prediction. |
| [polygenic-risk-score](skills/bioskills/polygenic-risk-score/) | bioskills | Polygenic risk score calculation and validation using PLINK or PRSice. |
| [population-genetics](skills/bioskills/population-genetics/) | bioskills | Population structure analysis, FST calculation, and demographic inference. |
| [read-trimming](skills/bioskills/read-trimming/) | bioskills | Adapter trimming and quality filtering for Illumina sequencing reads. |
| [repeat-masking](skills/bioskills/repeat-masking/) | bioskills | Repetitive element identification and masking using RepeatMasker. |
| [short-read-alignment](skills/bioskills/short-read-alignment/) | bioskills | Short-read alignment to reference genomes using BWA-MEM or Bowtie2. |
| [snp-annotation](skills/bioskills/snp-annotation/) | bioskills | SNP functional annotation using ANNOVAR, VEP, or SnpEff. |
| [somatic-variant-calling](skills/bioskills/somatic-variant-calling/) | bioskills | Somatic mutation calling from tumor-normal pairs using Mutect2 or Strelka2. |
| [structural-variant-calling](skills/bioskills/structural-variant-calling/) | bioskills | Structural variant detection including deletions, inversions, and translocations. |
| [structural-variant-detection](skills/bioclaw_hub/structural-variant-detection/) | bioclaw_hub | SV detection from short and long reads with annotation and visualization. |
| [variant-annotation](skills/bioskills/variant-annotation/) | bioskills | Comprehensive variant annotation with functional impact prediction. |
| [variant-filtering](skills/bioskills/variant-filtering/) | bioskills | VCF variant filtering by quality, depth, allele frequency, and functional impact. |
| [variant-prioritization](skills/bioskills/variant-prioritization/) | bioskills | Disease-relevant variant prioritization using CADD, REVEL, or ClinVar scores. |
| [vcf-processing](skills/bioskills/vcf-processing/) | bioskills | VCF file manipulation, merging, splitting, and format conversion. |
| [wes-analysis](skills/bioskills/wes-analysis/) | bioskills | Whole exome sequencing analysis pipeline from FASTQ to annotated variants. |
| [wgs-analysis](skills/bioskills/wgs-analysis/) | bioskills | Whole genome sequencing analysis pipeline with GATK best practices. |
| [wgs-pipeline](skills/clawbio/wgs-pipeline/) | clawbio | Production-grade WGS pipeline with QC, alignment, variant calling, and reporting. |

*...and 429 additional genomics skills in the [skills/bioskills/](skills/bioskills/), [skills/sciagent/](skills/sciagent/), and [skills/openclaw/](skills/openclaw/) directories.*

</details>

---

## Proteomics

> 146 skills — mass spectrometry analysis, structure prediction, protein design, binding affinity optimization.

<details>
<summary>View all 146 skills</summary>

| Skill | Source | Description |
|-------|--------|-------------|
| [alphafold](skills/adaptyv/alphafold/) | adaptyv | AlphaFold2 structure prediction for single chains and multimers. |
| [alphafold2-multimer](skills/bioclaw_hub/alphafold2-multimer/) | bioclaw_hub | Multimeric protein structure prediction using AlphaFold2-Multimer. |
| [de-novo-protein-design](skills/bioskills/de-novo-protein-design/) | bioskills | De novo protein design using RFDiffusion and ProteinMPNN. |
| [differential-protein-expression](skills/bioskills/differential-protein-expression/) | bioskills | Differential protein expression analysis from mass spectrometry data using limma. |
| [foldseek](skills/adaptyv/foldseek/) | adaptyv | Fast protein structure search against large databases using Foldseek. |
| [mass-spectrometry-analysis](skills/bioskills/mass-spectrometry-analysis/) | bioskills | Proteomics data analysis from raw MS spectra to protein quantification. |
| [pdb](skills/adaptyv/pdb/) | adaptyv | Protein Data Bank query and structure retrieval for analysis. |
| [protein-binding-prediction](skills/bioskills/protein-binding-prediction/) | bioskills | Protein-protein and protein-ligand binding affinity prediction. |
| [protein-design-workflow](skills/adaptyv/protein-design-workflow/) | adaptyv | End-to-end protein design workflow from target specification to candidate ranking. |
| [protein-expression-analysis](skills/bioskills/protein-expression-analysis/) | bioskills | Protein expression quantification and normalization from MS data. |
| [protein-function-prediction](skills/bioskills/protein-function-prediction/) | bioskills | Protein function annotation using sequence and structure-based methods. |
| [protein-interaction-network](skills/bioskills/protein-interaction-network/) | bioskills | Protein-protein interaction network construction and hub gene identification. |
| [protein-qc](skills/adaptyv/protein-qc/) | adaptyv | Protein design candidate quality control with structural validation metrics. |
| [protein-structure-analysis](skills/bioskills/protein-structure-analysis/) | bioskills | Protein structure analysis including secondary structure, domains, and active sites. |
| [protein-structure-prediction](skills/bioskills/protein-structure-prediction/) | bioskills | Structure prediction using ESMFold, RoseTTAFold, or AlphaFold2. |
| [proteinmpnn](skills/adaptyv/proteinmpnn/) | adaptyv | Sequence design for fixed protein backbones using ProteinMPNN. |
| [proteomics-database-search](skills/bioskills/proteomics-database-search/) | bioskills | Peptide identification by database search using Mascot, Sequest, or MaxQuant. |
| [proteomics-quantification](skills/bioskills/proteomics-quantification/) | bioskills | Label-free and TMT-based protein quantification from mass spectrometry data. |
| [uniprot](skills/adaptyv/uniprot/) | adaptyv | UniProt protein database query for sequence, function, and annotation retrieval. |

*...and 127 additional proteomics skills in the [skills/bioskills/](skills/bioskills/) and [skills/openclaw/](skills/openclaw/) directories.*

</details>

---

## Single-Cell Analysis

> 117 skills — preprocessing, clustering, cell type annotation, trajectory inference, cell communication, multimodal integration.

<details>
<summary>View all 117 skills</summary>

| Skill | Source | Description |
|-------|--------|-------------|
| [cell-cell-communication](skills/bioskills/cell-cell-communication/) | bioskills | Cell-cell communication inference using CellChat or NicheNet. |
| [cell-clustering](skills/bioskills/cell-clustering/) | bioskills | Single-cell clustering using Leiden or Louvain algorithms with resolution tuning. |
| [cell-type-annotation](skills/bioskills/cell-type-annotation/) | bioskills | Automated and manual cell type annotation using marker genes and reference datasets. |
| [cellranger-pipeline](skills/bioskills/cellranger-pipeline/) | bioskills | 10x Genomics Cell Ranger pipeline for FASTQ to count matrix generation. |
| [crispr-screen-analysis](skills/bioskills/crispr-screen-analysis/) | bioskills | Pooled CRISPR screen analysis with MAGeCK for essential gene identification. |
| [doublet-detection](skills/bioskills/doublet-detection/) | bioskills | Doublet detection and removal using Scrublet or DoubletFinder. |
| [multimodal-integration](skills/bioskills/multimodal-integration/) | bioskills | Single-cell multimodal data integration using WNN or MOFA+. |
| [pseudotime-analysis](skills/bioskills/pseudotime-analysis/) | bioskills | Pseudotime trajectory inference using Monocle3 or Slingshot. |
| [rna-velocity](skills/bioskills/rna-velocity/) | bioskills | RNA velocity analysis using scVelo for cell fate prediction. |
| [scanpy-analysis](skills/omics/scanpy-analysis/) | omics | Single-cell RNA-seq analysis using Scanpy from QC to UMAP visualization. |
| [scrna-batch-correction](skills/bioskills/scrna-batch-correction/) | bioskills | Batch effect correction for scRNA-seq using Harmony, BBKNN, or Scanorama. |
| [scrna-clustering](skills/clawbio/scrna-clustering/) | clawbio | Single-cell clustering workflow with marker gene identification and annotation. |
| [scrna-differential-expression](skills/bioskills/scrna-differential-expression/) | bioskills | Differential gene expression between cell clusters using Wilcoxon or DESeq2. |
| [scrna-preprocessing](skills/bioskills/scrna-preprocessing/) | bioskills | Single-cell RNA-seq preprocessing including QC filtering, normalization, and feature selection. |
| [scrna-qc](skills/bioskills/scrna-qc/) | bioskills | Single-cell RNA-seq quality control with mitochondrial fraction and count filtering. |
| [seurat-analysis](skills/bioskills/seurat-analysis/) | bioskills | Complete scRNA-seq analysis using Seurat from raw counts to cell type annotation. |
| [spatial-transcriptomics](skills/omics/spatial-transcriptomics/) | omics | Spatial transcriptomics analysis for 10x Visium data with spatially variable gene detection. |
| [trajectory-inference](skills/clawbio/trajectory-inference/) | clawbio | Cell differentiation trajectory inference with pseudotime ordering and branch analysis. |

*...and 99 additional single-cell skills in the [skills/bioskills/](skills/bioskills/), [skills/omics/](skills/omics/), and [skills/openclaw/](skills/openclaw/) directories.*

</details>

---

## Biology and AI

> 117 skills — medical AI, clinical decision support, drug discovery, general biological tools.

<details>
<summary>View all 117 skills</summary>

| Skill | Source | Description |
|-------|--------|-------------|
| [bindcraft](skills/adaptyv/bindcraft/) | adaptyv | Binder design using BindCraft for therapeutic protein engineering. |
| [binder-design](skills/adaptyv/binder-design/) | adaptyv | Protein binder design targeting specific epitopes using diffusion-based methods. |
| [binding-characterization](skills/adaptyv/binding-characterization/) | adaptyv | Experimental binding characterization workflow for designed protein candidates. |
| [boltz](skills/adaptyv/boltz/) | adaptyv | Biomolecular structure prediction using the Boltz model. |
| [boltzgen](skills/adaptyv/boltzgen/) | adaptyv | Generative structure sampling using BoltzGen for diverse conformation exploration. |
| [campaign-manager](skills/adaptyv/campaign-manager/) | adaptyv | Protein design campaign management for iterative experimental cycles. |
| [chai](skills/adaptyv/chai/) | adaptyv | Biomolecular complex structure prediction using the Chai-1 model. |
| [drug-discovery-pipeline](skills/bioskills/drug-discovery-pipeline/) | bioskills | AI-driven drug discovery pipeline from target identification to lead optimization. |
| [drug-interaction-prediction](skills/bioskills/drug-interaction-prediction/) | bioskills | Drug-drug and drug-target interaction prediction using machine learning. |
| [drug-repurposing](skills/bioskills/drug-repurposing/) | bioskills | Drug repurposing analysis using transcriptomic signatures and network pharmacology. |
| [esm](skills/adaptyv/esm/) | adaptyv | Protein language model embeddings using ESM2 for sequence analysis. |
| [ipsae](skills/adaptyv/ipsae/) | adaptyv | Interface predicted aligned error analysis for protein complex quality assessment. |
| [molecular-docking](skills/bioskills/molecular-docking/) | bioskills | Small molecule docking using AutoDock Vina or Glide. |
| [setup](skills/adaptyv/setup/) | adaptyv | Environment setup and configuration for protein design workflows. |
| [target-identification](skills/bioskills/target-identification/) | bioskills | Drug target identification using genetic evidence and network analysis. |
| [virtual-screening](skills/bioskills/virtual-screening/) | bioskills | Virtual screening of compound libraries against protein targets. |

*...and 101 additional biology and AI skills in the [skills/openclaw/](skills/openclaw/) and [skills/sciagent/](skills/sciagent/) directories.*

</details>

---

## Clinical and Medical

> 97 skills — EHR analysis, clinical trial design, drug interactions, precision medicine, adverse event detection.

<details>
<summary>View all 97 skills</summary>

| Skill | Source | Description |
|-------|--------|-------------|
| [adverse-event-detection](skills/bioskills/adverse-event-detection/) | bioskills | Adverse drug event detection from clinical notes using NLP. |
| [clinical-nlp](skills/sciagent/clinical-nlp/) | sciagent | Clinical text processing for entity extraction and relation identification. |
| [clinical-trial-design](skills/sciagent/clinical-trial-design/) | sciagent | Clinical trial design with power analysis, randomization, and endpoint selection. |
| [clinical-trial-search](skills/sciagent/clinical-trial-search/) | sciagent | ClinicalTrials.gov search and eligibility criteria extraction. |
| [comorbidity-analysis](skills/bioskills/comorbidity-analysis/) | bioskills | Disease comorbidity analysis from EHR data using ICD codes. |
| [drug-dosing-optimization](skills/bioskills/drug-dosing-optimization/) | bioskills | Pharmacokinetic modeling for personalized drug dosing. |
| [ehr-analysis](skills/bioclaw_hub/ehr-analysis/) | bioclaw_hub | Electronic health record analysis for patient cohort characterization. |
| [icd-coding](skills/sciagent/icd-coding/) | sciagent | Automated ICD-10 code assignment from clinical text. |
| [patient-stratification](skills/bioskills/patient-stratification/) | bioskills | Patient subgroup identification using clinical and molecular features. |
| [precision-medicine](skills/bioskills/precision-medicine/) | bioskills | Precision medicine workflow integrating genomic and clinical data for treatment selection. |
| [survival-analysis](skills/sciagent/survival-analysis/) | sciagent | Kaplan-Meier and Cox proportional hazards survival analysis. |

*...and 86 additional clinical skills in the [skills/openclaw/](skills/openclaw/) and [skills/sciagent/](skills/sciagent/) directories.*

</details>

---

## Transcriptomics

> 87 skills — RNA-seq full pipeline, differential expression, alternative splicing, lncRNA, small RNA.

<details>
<summary>View all 87 skills</summary>

| Skill | Source | Description |
|-------|--------|-------------|
| [alternative-splicing](skills/bioskills/alternative-splicing/) | bioskills | Alternative splicing analysis using rMATS or SUPPA2. |
| [bulk-rna-seq](skills/bioskills/bulk-rna-seq/) | bioskills | Bulk RNA-seq analysis from raw reads to differential expression. |
| [cell-free-expression](skills/adaptyv/cell-free-expression/) | adaptyv | Cell-free protein expression system analysis and optimization. |
| [deseq2-analysis](skills/bioskills/deseq2-analysis/) | bioskills | Differential expression analysis using DESeq2 with shrinkage estimation. |
| [edger-analysis](skills/bioskills/edger-analysis/) | bioskills | Differential expression analysis using edgeR for count data. |
| [gene-expression-normalization](skills/bioskills/gene-expression-normalization/) | bioskills | RNA-seq count normalization using TPM, RPKM, or TMM methods. |
| [hisat2-alignment](skills/bioskills/hisat2-alignment/) | bioskills | Splice-aware RNA-seq alignment using HISAT2. |
| [kallisto-quantification](skills/bioskills/kallisto-quantification/) | bioskills | Transcript quantification using Kallisto pseudoalignment. |
| [lncrna-analysis](skills/bioskills/lncrna-analysis/) | bioskills | Long non-coding RNA identification, expression, and functional analysis. |
| [mirna-analysis](skills/bioskills/mirna-analysis/) | bioskills | MicroRNA expression profiling and target prediction. |
| [rna-seq-pipeline](skills/clawbio/rna-seq-pipeline/) | clawbio | End-to-end RNA-seq pipeline with alignment, quantification, and QC. |
| [salmon-quantification](skills/bioskills/salmon-quantification/) | bioskills | Transcript-level quantification using Salmon with bias correction. |
| [star-alignment](skills/bioskills/star-alignment/) | bioskills | High-speed RNA-seq alignment using STAR with splice junction detection. |
| [stringtie-assembly](skills/bioskills/stringtie-assembly/) | bioskills | Transcript assembly and quantification using StringTie. |
| [wgcna-analysis](skills/bioskills/wgcna-analysis/) | bioskills | Weighted gene co-expression network analysis for module identification. |

*...and 72 additional transcriptomics skills in the [skills/bioskills/](skills/bioskills/) and [skills/openclaw/](skills/openclaw/) directories.*

</details>

---

## Database Query

> 54 skills — UniProt, PDB, KEGG, Reactome, GEO, ClinVar, Ensembl, STRING.

<details>
<summary>View all 54 skills</summary>

| Skill | Source | Description |
|-------|--------|-------------|
| [clinvar-query](skills/bioskills/clinvar-query/) | bioskills | ClinVar variant pathogenicity query and clinical significance retrieval. |
| [ensembl-query](skills/bioskills/ensembl-query/) | bioskills | Ensembl gene, transcript, and variant annotation retrieval via REST API. |
| [geo-data-retrieval](skills/sragent/geo-data-retrieval/) | sragent | GEO and SRA dataset search, metadata extraction, and download. |
| [kegg-pathway-query](skills/bioskills/kegg-pathway-query/) | bioskills | KEGG pathway and gene annotation query for functional analysis. |
| [omim-query](skills/bioskills/omim-query/) | bioskills | OMIM disease-gene association query for Mendelian disorder analysis. |
| [pdb-structure-query](skills/bioskills/pdb-structure-query/) | bioskills | Protein Data Bank structure search and coordinate retrieval. |
| [pubmed-search](skills/sciagent/pubmed-search/) | sciagent | PubMed literature search with MeSH terms and citation retrieval. |
| [reactome-query](skills/bioskills/reactome-query/) | bioskills | Reactome pathway database query for biological process annotation. |
| [string-interaction-query](skills/bioskills/string-interaction-query/) | bioskills | STRING protein interaction network query with confidence scoring. |
| [uniprot-query](skills/bioskills/uniprot-query/) | bioskills | UniProt protein sequence, function, and domain annotation retrieval. |

*...and 44 additional database query skills in the [skills/bioskills/](skills/bioskills/), [skills/bioclaw/](skills/bioclaw/), and [skills/sciagent/](skills/sciagent/) directories.*

</details>

---

## Multi-Omics Integration

> 51 skills — MOFA, DIABLO, single-cell multimodal, spatial transcriptomics.

<details>
<summary>View all 51 skills</summary>

| Skill | Source | Description |
|-------|--------|-------------|
| [diablo-integration](skills/bioskills/diablo-integration/) | bioskills | Multi-omics supervised integration using DIABLO for biomarker discovery. |
| [mofa-integration](skills/bioskills/mofa-integration/) | bioskills | Multi-omics factor analysis using MOFA+ for latent factor decomposition. |
| [multi-omics-clustering](skills/bioskills/multi-omics-clustering/) | bioskills | Multi-omics data clustering using similarity network fusion. |
| [multi-omics-pipeline](skills/clawbio/multi-omics-pipeline/) | clawbio | Integrated multi-omics analysis pipeline combining genomics, transcriptomics, and proteomics. |
| [multimodal-scrna](skills/omics/multimodal-scrna/) | omics | Single-cell multimodal integration of RNA and ATAC data using ArchR or Seurat. |
| [proteogenomics](skills/bioskills/proteogenomics/) | bioskills | Proteogenomics integration linking genomic variants to protein expression changes. |
| [spatial-multi-omics](skills/omics/spatial-multi-omics/) | omics | Spatial multi-omics data integration for tissue-resolved molecular profiling. |

*...and 44 additional multi-omics skills in the [skills/bioskills/](skills/bioskills/) and [skills/openclaw/](skills/openclaw/) directories.*

</details>

---

## Bioinformatics Utilities

> 50 skills — sequence analysis, BLAST, tool chains, pipeline management.

<details>
<summary>View all 50 skills</summary>

| Skill | Source | Description |
|-------|--------|-------------|
| [bio-analysis-skills-hub](skills/bioclaw/bio-analysis-skills-hub/) | bioclaw | Browse and install community skills from the BioClaw Skills Hub. |
| [blast-search](skills/bioskills/blast-search/) | bioskills | Sequence similarity search using BLAST against NCBI or custom databases. |
| [conda-environment](skills/kdense/conda-environment/) | kdense | Conda environment creation and package management for bioinformatics tools. |
| [docker-container](skills/kdense/docker-container/) | kdense | Docker container setup and management for reproducible bioinformatics workflows. |
| [file-format-conversion](skills/bioskills/file-format-conversion/) | bioskills | Bioinformatics file format conversion between FASTQ, BAM, VCF, BED, and GFF. |
| [multiple-sequence-alignment](skills/bioskills/multiple-sequence-alignment/) | bioskills | Multiple sequence alignment using MUSCLE, MAFFT, or ClustalW. |
| [nextflow-pipeline](skills/bioskills/nextflow-pipeline/) | bioskills | Nextflow pipeline development and execution for scalable bioinformatics workflows. |
| [phylogenetic-analysis](skills/bioskills/phylogenetic-analysis/) | bioskills | Phylogenetic tree construction using maximum likelihood or Bayesian methods. |
| [primer-design](skills/bioskills/primer-design/) | bioskills | PCR primer design with Tm calculation and specificity checking. |
| [sequence-analysis](skills/bioskills/sequence-analysis/) | bioskills | General sequence analysis including ORF finding, GC content, and motif search. |
| [snakemake-workflow](skills/bioskills/snakemake-workflow/) | bioskills | Snakemake workflow development with rule-based dependency management. |

*...and 39 additional bioinformatics utility skills in the [skills/kdense/](skills/kdense/) and [skills/bioclaw/](skills/bioclaw/) directories.*

</details>

---

## Visualization

> 38 skills — volcano plots, heatmaps, PCA/UMAP, interactive charts.

<details>
<summary>View all 38 skills</summary>

| Skill | Source | Description |
|-------|--------|-------------|
| [circos-plot](skills/bioskills/circos-plot/) | bioskills | Circular genome visualization using Circos for comparative genomics. |
| [gene-expression-heatmap](skills/bioskills/gene-expression-heatmap/) | bioskills | Gene expression heatmap with hierarchical clustering and annotation. |
| [genome-visualization](skills/bioskills/genome-visualization/) | bioskills | Genome-scale data visualization including coverage tracks and variant plots. |
| [interactive-plots](skills/kdense/interactive-plots/) | kdense | Interactive scientific visualization using Plotly or Bokeh. |
| [pca-analysis](skills/bioskills/pca-analysis/) | bioskills | Principal component analysis for dimensionality reduction and sample clustering. |
| [umap-visualization](skills/bioskills/umap-visualization/) | bioskills | UMAP dimensionality reduction for high-dimensional biological data visualization. |
| [volcano-plot](skills/bioskills/volcano-plot/) | bioskills | Volcano plot generation for differential expression result visualization. |

*...and 31 additional visualization skills in the [skills/bioskills/](skills/bioskills/) and [skills/kdense/](skills/kdense/) directories.*

</details>

---

## Workflow Orchestration

> 31 skills — Snakemake, Nextflow, CWL, WDL.

<details>
<summary>View all 31 skills</summary>

| Skill | Source | Description |
|-------|--------|-------------|
| [cwl-workflow](skills/bioskills/cwl-workflow/) | bioskills | Common Workflow Language pipeline development for portable bioinformatics workflows. |
| [galaxy-workflow](skills/bioskills/galaxy-workflow/) | bioskills | Galaxy platform workflow design and execution for reproducible analysis. |
| [hpc-job-submission](skills/kdense/hpc-job-submission/) | kdense | HPC cluster job submission using SLURM or PBS for large-scale computation. |
| [nextflow-dsl2](skills/bioskills/nextflow-dsl2/) | bioskills | Nextflow DSL2 pipeline development with module reuse and containerization. |
| [pipeline-monitoring](skills/kdense/pipeline-monitoring/) | kdense | Bioinformatics pipeline monitoring, logging, and failure recovery. |
| [snakemake-cluster](skills/bioskills/snakemake-cluster/) | bioskills | Snakemake cluster execution with SLURM integration and resource management. |
| [wdl-workflow](skills/bioskills/wdl-workflow/) | bioskills | Workflow Description Language pipeline for cloud and HPC execution. |

*...and 24 additional workflow orchestration skills in the [skills/bioskills/](skills/bioskills/) and [skills/kdense/](skills/kdense/) directories.*

</details>

---

## Epigenomics

> 19 skills — ChIP-seq, ATAC-seq, DNA methylation, Hi-C, chromatin state.

<details>
<summary>View all 19 skills</summary>

| Skill | Source | Description |
|-------|--------|-------------|
| [atac-seq](skills/bioclaw/atac-seq/) | bioclaw | ATAC-seq processing with QC, MACS3 peak calling, consensus peak matrices, and differential accessibility. |
| [bisulfite-sequencing](skills/bioskills/bisulfite-sequencing/) | bioskills | Whole-genome bisulfite sequencing analysis for DNA methylation profiling. |
| [chip-seq-peak-calling](skills/bioskills/chip-seq-peak-calling/) | bioskills | ChIP-seq peak calling using MACS2 with IDR reproducibility assessment. |
| [chromatin-state-annotation](skills/bioskills/chromatin-state-annotation/) | bioskills | Chromatin state annotation using ChromHMM or Segway. |
| [dna-methylation-analysis](skills/bioskills/dna-methylation-analysis/) | bioskills | DNA methylation analysis from WGBS or RRBS data with DMR identification. |
| [hic-analysis](skills/bioskills/hic-analysis/) | bioskills | Hi-C chromatin conformation analysis with TAD calling and loop detection. |
| [motif-analysis](skills/bioskills/motif-analysis/) | bioskills | Transcription factor motif enrichment analysis in peak regions. |

*...and 12 additional epigenomics skills in the [skills/bioskills/](skills/bioskills/) and [skills/bioclaw_hub/](skills/bioclaw_hub/) directories.*

</details>

---

## Pathway Analysis

> 13 skills — KEGG, Reactome, GO, GSEA.

| Skill | Source | Description |
|-------|--------|-------------|
| [gene-ontology-analysis](skills/bioskills/gene-ontology-analysis/) | bioskills | Gene Ontology enrichment analysis using clusterProfiler or topGO. |
| [gsea-analysis](skills/bioskills/gsea-analysis/) | bioskills | Gene Set Enrichment Analysis using GSEA or fgsea with MSigDB gene sets. |
| [kegg-enrichment](skills/bioskills/kegg-enrichment/) | bioskills | KEGG pathway enrichment analysis for differentially expressed genes. |
| [network-enrichment](skills/bioskills/network-enrichment/) | bioskills | Network-based pathway enrichment using STRING or BioGRID interactions. |
| [pathway-visualization](skills/bioskills/pathway-visualization/) | bioskills | Pathway diagram visualization using Pathview or ReactomePA. |
| [reactome-enrichment](skills/bioskills/reactome-enrichment/) | bioskills | Reactome pathway enrichment analysis with hierarchical pathway mapping. |
| [upstream-regulator-analysis](skills/bioskills/upstream-regulator-analysis/) | bioskills | Upstream transcription factor regulator analysis from differential expression data. |

*...and 6 additional pathway analysis skills in the [skills/bioskills/](skills/bioskills/) directory.*

---

## Metagenomics

> 8 skills — 16S/ITS amplicon, Kraken2, MetaPhlAn, QIIME2.

| Skill | Source | Description |
|-------|--------|-------------|
| [16s-amplicon-analysis](skills/bioskills/16s-amplicon-analysis/) | bioskills | 16S rRNA amplicon sequencing analysis using QIIME2 or DADA2. |
| [its-fungal-analysis](skills/bioskills/its-fungal-analysis/) | bioskills | ITS amplicon sequencing analysis for fungal community profiling. |
| [kraken2-classification](skills/bioskills/kraken2-classification/) | bioskills | Metagenomic read classification using Kraken2 with Bracken abundance estimation. |
| [metaphlan-profiling](skills/bioskills/metaphlan-profiling/) | bioskills | Metagenomic species profiling using MetaPhlAn4. |
| [metagenome-assembly](skills/bioskills/metagenome-assembly/) | bioskills | Metagenomic assembly using MEGAHIT or metaSPAdes. |
| [microbiome-diversity](skills/bioskills/microbiome-diversity/) | bioskills | Alpha and beta diversity analysis for microbiome studies. |
| [qiime2-pipeline](skills/bioskills/qiime2-pipeline/) | bioskills | QIIME2 amplicon sequencing pipeline from raw reads to diversity analysis. |
| [shotgun-metagenomics](skills/bioskills/shotgun-metagenomics/) | bioskills | Shotgun metagenomics analysis including assembly, binning, and annotation. |

---

## Protein Design

> 6 skills — RFDiffusion, ProteinMPNN, Boltz, Chai, LigandMPNN.

| Skill | Source | Description |
|-------|--------|-------------|
| [ligandmpnn](skills/adaptyv/ligandmpnn/) | adaptyv | Sequence design for protein-ligand complexes using LigandMPNN. |
| [protein-design-de-novo](skills/bioskills/protein-design-de-novo/) | bioskills | De novo protein backbone generation using RFDiffusion. |
| [proteinmpnn-design](skills/adaptyv/proteinmpnn/) | adaptyv | Fixed-backbone sequence design using ProteinMPNN with temperature sampling. |
| [rfdiffusion](skills/adaptyv/rfdiffusion/) | adaptyv | Protein backbone diffusion using RFDiffusion for binder and motif scaffolding. |
| [solublempnn](skills/adaptyv/solublempnn/) | adaptyv | Solubility-optimized sequence design using SolubleMPNN. |
| [structure-based-design](skills/bioskills/structure-based-design/) | bioskills | Structure-based protein engineering using computational mutagenesis and docking. |

---

## Sources

This collection aggregates and deduplicates skills from the following open-source repositories:

| Repository | Skills | Focus |
|------------|-------:|-------|
| [GPTomics/bioSkills](https://github.com/GPTomics/bioSkills) | 524 | Systematic bioinformatics suite from QC to multi-omics. |
| [FreedomIntelligence/OpenClaw-Medical-Skills](https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills) | 326 | Medical AI library aggregating 12 specialized sub-repositories. |
| [jaechang-hits/SciAgent-Skills](https://github.com/jaechang-hits/SciAgent-Skills) | 151 | Scientific agent skills for statistics, databases, and clinical decisions. |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 91 | General scientific computing and HPC workflow skills. |
| [ClawBio/ClawBio](https://github.com/ClawBio/ClawBio) | 60 | Bioinformatics workflow orchestration for GWAS and single-cell. |
| [zongtingwei/Bioclaw_Skills_Hub](https://github.com/zongtingwei/Bioclaw_Skills_Hub) | 46 | Ten-category biological skills hub. |
| [Runchuan-BU/BioClaw](https://github.com/Runchuan-BU/BioClaw) | 37 | Core bioinformatics tools and database query skills. |
| [fmschulz/omics-skills](https://github.com/fmschulz/omics-skills) | 29 | Single-cell and spatial omics specialized skills. |
| [adaptyvbio/protein-design-skills](https://github.com/adaptyvbio/protein-design-skills) | 21 | Full protein design toolkit: RFDiffusion, ProteinMPNN, Boltz, Chai. |
| [zamushwani2/biomedical-ai-skills](https://github.com/zamushwani2/biomedical-ai-skills) | 4 | Cancer multi-omics analysis skills in R. |
| [ArcInstitute/SRAgent](https://github.com/ArcInstitute/SRAgent) | 1 | Intelligent SRA and GEO dataset retrieval. |

---

## Skill Format

Each skill is a self-contained folder with a `SKILL.md` file defining domain knowledge, tool usage, and expected outputs. Compatible with any Claude-based agent framework supporting the `SKILL.md` convention.

```
skills/
└── <source>/
    └── <skill-name>/
        ├── SKILL.md          # Skill definition (required)
        └── ...               # Supporting files
```

**Quick install:**

```bash
git clone https://github.com/BioTender-max/awesome-bio-agent-skills.git
cp -r awesome-bio-agent-skills/skills/* /path/to/your/agent/skills/
```

A machine-readable index of all 1,306 skills is available in [`bioskill_index_v2.csv`](bioskill_index_v2.csv).
