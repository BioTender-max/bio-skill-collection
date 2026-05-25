# ⚙️ ClawBio Pipelines

[![Skills](https://img.shields.io/badge/Skills-60-00d4aa?style=flat-square&logo=databricks&logoColor=white)](https://github.com/ClawBio/ClawBio)
[![Source](https://img.shields.io/badge/Source-ClawBio%2FClawBio-0079d3?style=flat-square&logo=github&logoColor=white)](https://github.com/ClawBio/ClawBio)

> 生信流程编排与协调技能 · Bioinformatics pipeline orchestration skills
> `GWAS · Single-cell · Structural biology · Ancestry · Pharmacogenomics`

---

## Skills List

| 文件夹 · Folder | 技能名称 · Skill | 描述 · Description |
|-----------------|-----------------|-------------------|
| `affinity-proteomics` | **affinity-proteomics** | Unified analysis pipeline for affinity-based proteomics platforms — Olink (PEA, NPX) and SomaLogic SomaScan (SOMAmer, |
| `analyze-fasta` | **analyze-fasta** | Analyze a single FASTA file (nucleotide or protein), compute sequence-level metrics (GC, ORFs, MW, pI, GRAVY, secondary-structure fractions) with B... |
| `archaic-introgression` | **archaic-introgression** | Detect Neanderthal and Denisovan introgression segments from modern human genomes |
| `bgpt-mcp` | **bgpt-mcp** | Search scientific papers via the BGPT MCP server and retrieve structured experimental data — methods, results, |
| `bio-orchestrator` | **bio-orchestrator** | Meta-agent that routes bioinformatics requests to specialised sub-skills. Handles file type detection, analysis |
| `bioconductor-bridge` | **bioconductor-bridge** | Bioconductor package discovery, workflow recommendation, setup inspection, and starter code generation grounded |
| `cell-detection` | **cell-detection** | Cell segmentation in fluorescence microscopy images. Supports Cellpose/cpsam (Cellpose 4.0) with additional backends |
| `claw-ancestry-pca` | **claw-ancestry-pca** | Ancestry decomposition PCA against the Simons Genome Diversity Project |
| `claw-metagenomics` | **claw-metagenomics** | Shotgun metagenomics profiling — taxonomy, resistome, and functional pathways |
| `claw-semantic-sim` | **claw-semantic-sim** | Semantic Similarity Index for disease research literature using PubMedBERT embeddings |
| `clinical-trial-finder` | **clinical-trial-finder** | Find clinical trials for a gene, variant, or condition from ClinicalTrials.gov + EUCTR, with FHIR R4 output |
| `clinical-variant-reporter` | **clinical-variant-reporter** | Classify germline variants from VCF/BCF files according to the ACMG/AMP 2015 28-criteria evidence framework and |
| `clinpgx` | **clinpgx** | Query the ClinPGx API for pharmacogenomic gene-drug data, clinical annotations, CPIC guidelines, and FDA drug |
| `crispr-screen-triage` | **crispr-screen-triage** | Deterministic CRISPR screen hit ranking from local guide-level count tables |
| `de-summary` | **de-summary** | Summarise pre-computed differential expression results with ranked gene lists, biological themes, and publication-ready |
| `diff-visualizer` | **diff-visualizer** | Rich downstream visualisation and reporting for bulk RNA-seq differential expression and scRNA marker/contrast |
| `dnasp` | **dnasp** | - |
| `drug-photo` | **drug-photo** | Medication photo to personalised PGx dosage card via Claude vision — snap a pill, get genotype-informed guidance |
| `equity-scorer` | **equity-scorer** | Compute HEIM diversity and equity metrics from VCF or ancestry data. Generates heterozygosity, FST, PCA plots, |
| `fine-mapping` | **fine-mapping** | Statistical fine-mapping of GWAS loci using SuSiE, SuSiE-inf, and Approximate Bayes Factors to identify credible |
| `flow-bio` | **flow-bio** | Flow.bio API bridge — authenticate, browse pipelines/samples/projects, search, upload data, launch pipeline executions, |
| `galaxy-bridge` | **galaxy-bridge** | Galaxy tool discovery, intelligent recommendation, and execution — 8,000+ bioinformatics tools from usegalaxy.org |
| `genome-compare` | **genome-compare** | Compare your genome to George Church (PGP-1) and estimate ancestry composition via IBS and EM admixture |
| `genome-match` | **genome-match** | Score genetic compatibility across all male-female pairings in a Genomebook generation |
| `gwas-catalog-region-fetch` | **gwas-catalog-region-fetch** | \| |
| `gwas-lookup` | **gwas-lookup** | Federated variant lookup across 9 genomic databases — GWAS Catalog, Open Targets, PheWeb (UKB, FinnGen, BBJ), |
| `gwas-pipeline` | **gwas-pipeline** | End-to-end GWAS automation wrapping PLINK2 for genotype QC and REGENIE for two-step whole-genome regression association |
| `gwas-prs` | **gwas-prs** | Calculate polygenic risk scores from DTC genetic data using the PGS Catalog |
| `illumina-bridge` | **illumina-bridge** | Import DRAGEN-exported Illumina result bundles into ClawBio for local tertiary analysis and downstream routing. |
| `lit-synthesizer` | **lit-synthesizer** | Search PubMed and bioRxiv for bioinformatics literature, synthesise results into a structured report, and build |
| `mendelian-randomisation` | **mendelian-randomisation** | Two-sample Mendelian Randomisation from GWAS summary statistics with IVW, MR-Egger, weighted median/mode, and |
| `methylation-clock` | **methylation-clock** | Compute epigenetic age from DNA methylation arrays using PyAging clocks from GEO accessions or local files. |
| `multiqc-reporter` | **multiqc-reporter** | Aggregates QC reports from any bioinformatics tool outputs (FastQC, fastp, STAR, Picard, samtools, etc.) into |
| `ncbi-datasets` | **ncbi-datasets** | - |
| `nfcore-rnaseq-wrapper` | **nfcore-rnaseq-wrapper** | Wrapper skill for running nf-core/rnaseq bulk RNA-seq preprocessing from FASTQ or BAM inputs with strict preflight, reproducibility outputs, and do... |
| `nfcore-scrnaseq-wrapper` | **nfcore-scrnaseq-wrapper** | Wrapper skill for running nf-core/scrnaseq upstream single-cell RNA-seq preprocessing from FASTQ with strict preflight, reproducibility outputs, an... |
| `nutrigx-advisor` | **nutrigx-advisor** | Personalised nutrition report from consumer genetic data (23andMe, AncestryDNA, VCF) — interrogates nutritionally-relevant |
| `omics-target-evidence-mapper` | **omics-target-evidence-mapper** | Aggregate public target-level evidence across omics and translational sources for research triage. |
| `pharmgx-reporter` | **pharmgx-reporter** | Pharmacogenomic report from DTC genetic data (23andMe/AncestryDNA) — 12 genes, 31 SNPs, 51 drugs |
| `profile-report` | **profile-report** | Unified personal genomic profile report — reads a PatientProfile JSON and synthesizes all skill results into |
| `proteomics-clock` | **proteomics-clock** | Compute organ-specific biological age from Olink proteomic data using Goeminne et al. (2025) elastic net aging |
| `proteomics-de` | **proteomics-de** | Differential expression analysis for label-free quantitative (LFQ) intensity data with standard MaxQuant and |
| `pubmed-summariser` | **pubmed-summariser** | Search PubMed for a gene name or disease term and generate a structured research briefing of the top recent English-language |
| `rare-disease-rnaseq` | **rare-disease-rnaseq** | Blood RNA-seq expression-outlier detection for rare-disease diagnostics. Cases scored against a control reference panel; outliers ranked and filter... |
| `recombinator` | **recombinator** | Produce offspring genomes from parent pairs via meiotic recombination, mutation, and clinical evaluation |
| `repro-enforcer` | **repro-enforcer** | Export any bioinformatics analysis as a reproducible bundle with Conda environment, Singularity container definition, |
| `rnaseq-de` | **rnaseq-de** | Differential expression analysis for bulk RNA-seq and pseudo-bulk count matrices with QC, PCA, and contrast testing. |
| `scrna-embedding` | **scrna-embedding** | Local scVI/scANVI-based single-cell latent embedding and batch-aware integration from raw-count .h5ad or 10x |
| `scrna-orchestrator` | **scrna-orchestrator** | Local Scanpy pipeline for single-cell RNA-seq QC, optional doublet detection, clustering, marker discovery, optional |
| `seq-wrangler` | **seq-wrangler** | NGS read QC, alignment, and BAM processing pipeline. Wraps FastQC, BWA/Bowtie2/Minimap2, SAMtools, and MultiQC for automated read-to-BAM workflows." |
| `skill-builder` | **skill-builder** | Scaffold a new ClawBio skill from a spec file (JSON/YAML) or interactively — generates SKILL.md, Python skeleton, tests, and updates catalog.json |
| `soul2dna` | **soul2dna** | Compile SOUL.md character profiles into synthetic diploid genomes (.genome.json) via trait-to-allele mapping |
| `struct-predictor` | **struct-predictor** | Protein structure prediction with Boltz-2. Accepts YAML inputs (single protein or multi-chain complex), runs |
| `target-validation-scorer` | **target-validation-scorer** | Evidence-grounded target validation scoring with GO/NO-GO decisions for drug discovery campaigns |
| `turingdb-graph` | **turingdb-graph** | Build, query, and analyse biomedical knowledge graphs in TuringDB, a columnar graph database with git-like versioning. |
| `ukb-navigator` | **ukb-navigator** | Semantic search across UK Biobank's 12,000+ data fields and publications — find the right variables for your |
| `variant-annotation` | **variant-annotation** | Annotate VCF variants with Ensembl VEP REST, ClinVar significance, gnomAD/population frequency context, and prioritized |
| `vcf-annotator` | **vcf-annotator** | Annotate VCF variants with Ensembl VEP, ClinVar, and gnomAD. Ranks variants by impact (HIGH/MODERATE/LOW/MODIFIER) and generates a reproducible rep... |
| `wes-clinical-report-en` | **wes-clinical-report-en** | Generates professional clinical PDF reports in English from WES (Whole Exome Sequencing) data with clinical interpretation |
| `wes-clinical-report-es` | **wes-clinical-report-es** | Generates professional clinical PDF reports in Spanish from WES (Whole Exome Sequencing) data with clinical interpretation, |

---
*60 skills · Source: [ClawBio/ClawBio](https://github.com/ClawBio/ClawBio)*
