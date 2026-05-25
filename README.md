<div align="center">

<img src="https://raw.githubusercontent.com/BioTender-max/bio-skill-collection/main/assets/banner.png" alt="Bio Skill Collection" width="100%"/>

<br/>

[![GitHub Stars](https://img.shields.io/github/stars/BioTender-max/bio-skill-collection?style=for-the-badge&logo=github&color=gold)](https://github.com/BioTender-max/bio-skill-collection/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/BioTender-max/bio-skill-collection?style=for-the-badge&logo=github&color=blue)](https://github.com/BioTender-max/bio-skill-collection/network/members)
[![Skills Count](https://img.shields.io/badge/Skills-1306-brightgreen?style=for-the-badge&logo=databricks&logoColor=white)](https://github.com/BioTender-max/bio-skill-collection/tree/main/skills)
[![Sources](https://img.shields.io/badge/Sources-11_Repos-0079d3?style=for-the-badge&logo=github&logoColor=white)](https://github.com/BioTender-max/bio-skill-collection#-整合来源--sources)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

<h2>Bio Skill Collection</h2>

**全网最大生物医学 AI Agent 技能合集**

*The largest open-source biomedical AI agent skill collection — 1306 curated skills from 11 top repositories*

*1306 curated skills · Genomics · Proteomics · Single-Cell · Clinical · Drug Discovery · Protein Design*

</div>

---

## 🧬 What Is This? 关于本仓库

**Bio Skill Collection** is a curated aggregation of **1306 AI agent skills** covering the full spectrum of biomedical and bioinformatics research. Skills are sourced from **11 top open-source repositories** across GitHub, deduplicated, and organized into 15 categories.

**Bio Skill Collection** 系统性整合了 GitHub 上所有主流生物医学 AI Agent 技能仓库，经过去重与质量筛选，形成覆盖 **15 大类** 的完整技能集合。

Each skill is a self-contained folder with a `SKILL.md` file that:

- Teaches the agent specialized domain knowledge and workflows · 传授专业领域知识与工作流
- Connects to real databases, APIs, and computational tools · 对接真实数据库、API 与计算工具
- Produces structured, scientifically relevant outputs · 生成结构化、科学相关的输出

> This collection aggregates skills from **11 open-source repositories** spanning genomics pipelines, clinical workflows, protein design, and cutting-edge AI-driven drug discovery — giving your AI agent capabilities comparable to a team of specialized research scientists.
>
> 本合集聚合自 **11 个开源仓库**，涵盖基因组流程、临床工作流、蛋白质设计与 AI 驱动药物发现，让你的 AI Agent 具备媲美专业科研团队的能力。

---

## 🚀 Installation 安装

### Prerequisites 前置要求

- A Claude-based agent framework (e.g. [OpenClaw](https://github.com/openclaw/openclaw), [NanoClaw](https://github.com/qwibitai/nanoclaw), or [Biomni](https://github.com/Phylo-AI/biomni)) · 任意支持 SKILL.md 格式的 Claude Agent 框架
- Git

### Quick Start 快速开始

```bash
# Clone the repository · 克隆仓库
git clone https://github.com/BioTender-max/bio-skill-collection.git

# Copy skills to your agent workspace · 复制技能到 Agent 工作目录
cp -r bio-skill-collection/skills/* /path/to/your/agent/skills/
```

### For OpenClaw / NanoClaw Users

OpenClaw loads skills from two locations · OpenClaw 从两个位置加载技能：

| Priority 优先级 | Path 路径 | Scope 范围 |
|---|---|---|
| High 高 | `<workspace>/skills/` | Per-workspace (recommended) · 工作区级（推荐） |
| Low 低 | `~/.openclaw/skills/` | Global, shared across all agents · 全局共享 |

```bash
# Per-workspace install (recommended) · 工作区安装（推荐）
cp -r bio-skill-collection/skills/* <your-workspace>/skills/

# Or global install · 或全局安装
cp -r bio-skill-collection/skills/* ~/.openclaw/skills/
```

---

## 📊 Skills Overview 技能概览

| Category 类别 | Count 数量 | Highlights 涵盖方向 |
|---|:---:|---|
| 🧬 Genomics 基因组学 | **472** | WGS/WES · 变异注释 · GWAS · CNV · 结构变异 · 基因组组装 |
| 🔬 Proteomics 蛋白质组学 | **146** | 质谱分析 · 结构预测 · 蛋白质设计 · 结合亲和力优化 |
| 🔵 Single-Cell 单细胞 | **117** | 预处理 · 聚类 · 细胞注释 · 轨迹推断 · 细胞通讯 |
| 🧫 Biology & AI 生物学与AI | **117** | 医学AI · 临床决策 · 药物发现 · 通用生物工具 |
| 🏥 Clinical 临床医学 | **97** | EHR · 临床试验 · 药物相互作用 · 精准医学 |
| 📊 Transcriptomics 转录组学 | **87** | RNA-seq · 差异表达 · 可变剪接 · lncRNA |
| 🗄️ Databases 数据库查询 | **54** | UniProt · PDB · KEGG · ClinVar · GEO · Ensembl |
| 🔗 Multi-Omics 多组学整合 | **51** | MOFA · DIABLO · 单细胞多模态 · 空间转录组 |
| 🧪 Bioinformatics 生信通用 | **50** | 序列分析 · BLAST · 工具链 · 流程管理 |
| 📈 Visualization 可视化 | **38** | 火山图 · 热图 · PCA/UMAP · 交互式图表 |
| ⚙️ Workflow 流程编排 | **31** | Snakemake · Nextflow · CWL · WDL |
| 🧫 Epigenomics 表观组学 | **19** | ChIP-seq · ATAC-seq · DNA甲基化 · Hi-C |
| 🌿 Pathway 通路分析 | **13** | KEGG · Reactome · GO · GSEA |
| 🦠 Metagenomics 宏基因组 | **8** | 16S/ITS · Kraken2 · MetaPhlAn · QIIME2 |
| 🧩 Protein Design 蛋白质设计 | **6** | RFDiffusion · ProteinMPNN · Boltz · Chai |
| **Total 合计** | **1306** | |

---

## 🌐 Sources 整合来源

| Repository 仓库 | Skills | Highlights 特色 |
|---|:---:|---|
| [GPTomics/bioSkills](https://github.com/GPTomics/bioSkills) | **524** | 最系统纯生信套件，QC → 多组学全流程 · Most systematic bioinformatics suite |
| [FreedomIntelligence/OpenClaw-Medical-Skills](https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills) | **326** | 最大医学AI技能库，聚合12+子仓库 · Largest medical AI skill library |
| [jaechang-hits/SciAgent-Skills](https://github.com/jaechang-hits/SciAgent-Skills) | **151** | 科研Agent，统计·数据库·临床决策 · Scientific agent skills |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | **91** | 科学计算通用技能库 · General scientific computing |
| [ClawBio/ClawBio](https://github.com/ClawBio/ClawBio) | **60** | 生信流程编排与协调 · Bioinformatics pipeline orchestration |
| [zongtingwei/Bioclaw_Skills_Hub](https://github.com/zongtingwei/Bioclaw_Skills_Hub) | **46** | 社区贡献纯生物十大类 · Community-contributed biology skills |
| [Runchuan-BU/BioClaw](https://github.com/Runchuan-BU/BioClaw) | **37** | 生信核心工具与数据库查询 · Core bioinformatics tools |
| [fmschulz/omics-skills](https://github.com/fmschulz/omics-skills) | **29** | 单细胞与空间组学专项 · Single-cell & spatial omics |
| [adaptyvbio/protein-design-skills](https://github.com/adaptyvbio/protein-design-skills) | **21** | 蛋白质设计全套（RFDiffusion·Boltz·Chai）· Full protein design toolkit |
| [zamushwani2/biomedical-ai-skills](https://github.com/zamushwani2/biomedical-ai-skills) | **4** | 癌症多组学R分析 · Cancer multi-omics R analysis |
| [ArcInstitute/SRAgent](https://github.com/ArcInstitute/SRAgent) | **1** | SRA/GEO智能检索 · Intelligent SRA/GEO retrieval |

> 原始发现 **1926** 个，跨仓库去重后保留 **1306** 个，同名技能优先保留质量更高的来源版本。
> *1926 skills discovered across all sources; 1306 retained after cross-repository deduplication.*

---

## 🗂️ Table of Contents 目录

### 🧬 Genomics 基因组学
- [Genomics 基因组学](#-genomics-基因组学)

### 🔬 Proteomics 蛋白质组学
- [Proteomics 蛋白质组学](#-proteomics-蛋白质组学)

### 🔵 Single-Cell 单细胞
- [Single-Cell 单细胞](#-single-cell-单细胞)

### 🧫 Biology & AI
- [Biology & AI 生物学与AI](#-biology--ai-生物学与ai)

### 🏥 Clinical 临床医学
- [Clinical 临床医学](#-clinical-临床医学)

### 📊 Transcriptomics 转录组学
- [Transcriptomics 转录组学](#-transcriptomics-转录组学)

### 🗄️ Databases 数据库
- [Databases 数据库查询](#️-databases-数据库查询)

### 🔗 Multi-Omics 多组学
- [Multi-Omics 多组学整合](#-multi-omics-多组学整合)

### 🧪 Bioinformatics 生信通用
- [Bioinformatics 生信通用](#-bioinformatics-生信通用)

### 📈 Visualization 可视化
- [Visualization 可视化](#-visualization-可视化)

### ⚙️ Workflow 流程编排
- [Workflow 流程编排](#️-workflow-流程编排)

### 🧫 Epigenomics 表观组学
- [Epigenomics 表观组学](#-epigenomics-表观组学)

### 🌿 Pathway 通路分析
- [Pathway 通路分析](#-pathway-通路分析)

### 🦠 Metagenomics 宏基因组
- [Metagenomics 宏基因组](#-metagenomics-宏基因组)

### 🧩 Protein Design 蛋白质设计
- [Protein Design 蛋白质设计](#-protein-design-蛋白质设计)

---

## 📋 Skills List 技能列表
<br/>
## 🧬 Genomics 基因组学
<br/>

<details>
<summary><b>Click to expand · 点击展开 (472 skills)</b></summary>

| Skill | Source 来源 | Description 描述 |
|-------|-------------|------------------|
| [alignment-and-mapping](skills/bioclaw_hub/alignment-and-mapping/) | `bioclaw_hub` | Workflow for read alignment, sorting, indexing, mapping statistics, and downstream-ready alignment artifacts. |
| [analyze-fasta](skills/clawbio/analyze-fasta/) | `clawbio` | Analyze a single FASTA file (nucleotide or protein), compute sequence-level metrics (GC, ORFs, MW, pI, GRAVY, seconda... |
| [archaic-introgression](skills/clawbio/archaic-introgression/) | `clawbio` | Detect Neanderthal and Denisovan introgression segments from modern human genomes |
| [archs4-database](skills/sciagent/archs4-database/) | `sciagent` | Query ARCHS4 REST API for uniformly processed RNA-seq expression, tissue patterns, co-expression across 1M+ human/mou... |
| [astropy-astronomy](skills/sciagent/astropy-astronomy/) | `sciagent` | Core Python library for astronomy/astrophysics: units with dimensional analysis, celestial coordinate transforms (ICR... |
| [bakta-genome-annotation](skills/sciagent/bakta-genome-annotation/) | `sciagent` | Annotate bacterial and archaeal genomes and plasmids with Bakta's Prodigal/HMM/diamond pipeline. Identifies CDS, ncRN... |
| [bcftools-variant-manipulation](skills/sciagent/bcftools-variant-manipulation/) | `sciagent` | CLI for VCF/BCF: filter, merge, annotate, query, normalize, compute stats. Core post-variant-calling: quality filteri... |
| [bedtools-genomic-intervals](skills/sciagent/bedtools-genomic-intervals/) | `sciagent` | Genomic interval ops on BED/BAM/GFF/VCF. Find overlaps, merge intervals, compute coverage, extract FASTA, find neares... |
| [bgpt-paper-search](skills/kdense/bgpt-paper-search/) | `kdense` | Search scientific papers and retrieve structured experimental data extracted from full-text studies via the BGPT MCP ... |
| [bio-alignment-amplicon-clipping](skills/bioskills/alignment-amplicon-clipping/) | `bioskills` | Trim PCR primers from aligned reads in amplicon-panel BAMs using samtools ampliconclip. Use when processing SARS-CoV-... |
| [bio-alignment-files-bam-statistics](skills/openclaw/bio-alignment-files-bam-statistics/) | `openclaw` | Generate alignment statistics using samtools flagstat, stats, depth, and coverage. Use when assessing alignment quali... |
| [bio-alignment-filtering](skills/bioskills/alignment-filtering/) | `bioskills` | Filter alignments by flags, mapping quality, and regions using samtools view and pysam. Use when extracting specific ... |
| [bio-alignment-indexing](skills/bioskills/alignment-indexing/) | `bioskills` | Create and use BAI/CSI indices for BAM/CRAM files using samtools and pysam. Use when enabling random access to alignm... |
| [bio-alignment-io](skills/bioskills/alignment-io/) | `bioskills` | Read, write, and convert multiple sequence alignment files using Biopython Bio.AlignIO. Supports Clustal, PHYLIP, Sto... |
| [bio-alignment-msa-parsing](skills/bioskills/msa-parsing/) | `bioskills` | Parse and analyze multiple sequence alignments using Biopython. Extract sequences, identify conserved regions, analyz... |
| [bio-alignment-msa-statistics](skills/bioskills/msa-statistics/) | `bioskills` | Calculate alignment statistics including sequence identity, conservation scores, substitution matrices, and similarit... |
| [bio-alignment-multiple](skills/bioskills/multiple-alignment/) | `bioskills` | Perform multiple sequence alignment using MAFFT, MUSCLE5, ClustalOmega, or T-Coffee. Guides tool and algorithm select... |
| [bio-alignment-pairwise](skills/bioskills/pairwise-alignment/) | `bioskills` | Perform pairwise sequence alignment using Biopython Bio.Align.PairwiseAligner. Use when comparing two sequences, find... |
| [bio-alignment-sorting](skills/bioskills/alignment-sorting/) | `bioskills` | Sort alignment files by coordinate or read name using samtools and pysam. Use when preparing BAM files for indexing, ... |
| [bio-alignment-structural](skills/bioskills/structural-alignment/) | `bioskills` | Align protein structures using Foldseek 3Di, TM-align, US-align, DALI, or Foldmason for structural MSA. Predict, scor... |
| [bio-alignment-trimming](skills/bioskills/alignment-trimming/) | `bioskills` | Trim multiple sequence alignments using ClipKIT, trimAl, BMGE, Divvier, or HMMcleaner with mode selection guidance pe... |
| [bio-alignment-validation](skills/bioskills/alignment-validation/) | `bioskills` | Validate alignment quality with insert size distribution, proper pairing rates, GC bias, strand balance, and other po... |
| [bio-assembly-qc](skills/omics/bio-assembly-qc/) | `omics` | Assemble genomes/metagenomes and produce assembly QC artifacts. |
| [bio-atac-seq-allele-specific-accessibility](skills/bioskills/allele-specific-accessibility/) | `bioskills` | Detect allele-specific chromatin accessibility from ATAC-seq using WASP, GATK ASEReadCounter, or RASQUAL. Use when ma... |
| [bio-atac-seq-atac-peak-calling](skills/bioskills/atac-peak-calling/) | `bioskills` | Call accessible chromatin regions from ATAC-seq BAM files using MACS3, MACS2, Genrich, or HMMRATAC. Use when identify... |
| [bio-atac-seq-consensus-peakset](skills/bioskills/consensus-peakset/) | `bioskills` | Build a differential-ready consensus peakset from per-replicate ATAC-seq peaks using iterative overlap removal, fixed... |
| [bio-bam-statistics](skills/bioskills/bam-statistics/) | `bioskills` | Generate alignment statistics using samtools flagstat, stats, depth, coverage, and mosdepth. Use when assessing align... |
| [bio-basecalling](skills/bioskills/basecalling/) | `bioskills` | Convert raw Nanopore signal data (FAST5/POD5) to nucleotide sequences using Dorado basecaller. Covers model selection... |
| [bio-bedgraph-handling](skills/bioskills/bedgraph-handling/) | `bioskills` | Create, manipulate, and convert bedGraph files for genome browser visualization. Covers bedGraph format, conversion t... |
| [bio-binning-qc](skills/omics/bio-binning-qc/) | `omics` | Perform metagenomic binning with QuickBin, refinement, and QC with completeness/contamination checks. |
| [bio-biomart-queries](skills/bioskills/biomart-queries/) | `bioskills` | Bulk-query Ensembl BioMart (and other BioMart instances) for cross-database ID mapping, gene/transcript/exon coordina... |
| [bio-causal-genomics-colocalization-analysis](skills/bioskills/colocalization-analysis/) | `bioskills` | Test whether two or more traits share a causal variant at a locus using Bayesian colocalization (coloc.abf, coloc.sus... |
| [bio-causal-genomics-effector-gene-prioritization](skills/bioskills/effector-gene-prioritization/) | `bioskills` | Maps GWAS-implicated loci to candidate effector (causal) genes by integrating variant-to-gene (V2G) features via Open... |
| [bio-causal-genomics-fine-mapping](skills/bioskills/fine-mapping/) | `bioskills` | Resolves GWAS associations to candidate causal variants and credible sets via SuSiE, susie_rss, FINEMAP, CAVIAR, DAP-... |
| [bio-causal-genomics-genetic-correlation](skills/bioskills/genetic-correlation/) | `bioskills` | Estimate bivariate genetic correlation (rg) between traits from GWAS summary statistics or individual-level genotypes... |
| [bio-causal-genomics-genomic-sem](skills/bioskills/genomic-sem/) | `bioskills` | Fits structural equation models to GWAS summary statistics using GenomicSEM (Grotzinger 2019), including common-facto... |
| [bio-causal-genomics-mediation-analysis](skills/bioskills/mediation-analysis/) | `bioskills` | Decompose total effects into direct and indirect paths through mediators using mediation, CMAverse 4-way, HIMA/HIMA2 ... |
| [bio-causal-genomics-mendelian-randomization](skills/bioskills/mendelian-randomization/) | `bioskills` | Estimate causal effects of an exposure on an outcome from GWAS summary statistics using genetic instruments. Implemen... |
| [bio-causal-genomics-pleiotropy-detection](skills/bioskills/pleiotropy-detection/) | `bioskills` | Detect and adjust for horizontal pleiotropy in two-sample Mendelian randomization by distinguishing uncorrelated (UHP... |
| [bio-causal-genomics-proteome-mr-drug-target](skills/bioskills/proteome-mr-drug-target/) | `bioskills` | Runs cis-pQTL Mendelian randomization for drug-target validation using UKB-PPP (Olink), deCODE (SomaScan), Fenland, I... |
| [bio-causal-genomics-transcriptome-wide-association](skills/bioskills/transcriptome-wide-association/) | `bioskills` | Performs gene-level association from GWAS summary statistics via genetically predicted tissue expression using FUSION... |
| [bio-cfdna-preprocessing](skills/bioskills/cfdna-preprocessing/) | `bioskills` | Preprocesses cell-free DNA sequencing data including adapter trimming, alignment optimized for short fragments, and U... |
| [bio-chipseq-allele-specific-binding](skills/bioskills/allele-specific-binding/) | `bioskills` | Detects allele-specific transcription factor or histone modification binding from heterozygous-variant ChIP-seq using... |
| [bio-chipseq-chip-deep-learning](skills/bioskills/chip-deep-learning/) | `bioskills` | Trains and applies base-resolution deep learning models on ChIP-seq / ChIP-nexus / CUT&RUN data. Uses BPNet (Avsec 20... |
| [bio-chipseq-peak-calling](skills/bioskills/peak-calling/) | `bioskills` | Calls ChIP-seq peaks with MACS3, MACS2, HOMER, or SPP across narrow (TF) and broad (histone) modes. Handles input con... |
| [bio-chipseq-visualization](skills/bioskills/chipseq-visualization/) | `bioskills` | Visualizes ChIP-seq data using deepTools (computeMatrix, plotHeatmap, plotProfile, bamCoverage, bamCompare), pyGenome... |
| [bio-clinical-biostatistics-adaptive-designs](skills/bioskills/adaptive-designs/) | `bioskills` | Designs adaptive clinical trials including group-sequential (O'Brien-Fleming, Pocock, Lan-DeMets spending), sample-si... |
| [bio-clinical-biostatistics-categorical-tests](skills/bioskills/categorical-tests/) | `bioskills` | Tests associations between categorical variables in clinical data using chi-square, Fisher's exact, Boschloo, Cochran... |
| [bio-clinical-biostatistics-power-sample-size](skills/bioskills/power-and-sample-size/) | `bioskills` | Computes sample size and power for clinical trials including continuous, binary, and time-to-event endpoints; superio... |
| [bio-clinical-databases-acmg-classification](skills/bioskills/acmg-classification/) | `bioskills` | Applies ACMG/AMP 2015 framework with ClinGen SVI specifications, Tavtigian 2018/2020 Bayesian point system, Abou Tayo... |
| [bio-clinical-databases-clinvar-lookup](skills/bioskills/clinvar-lookup/) | `bioskills` | Queries ClinVar for variant pathogenicity classifications, ClinGen VCEP curations, and somatic-vs-germline interpreta... |
| [bio-clinical-databases-dbsnp-queries](skills/bioskills/dbsnp-queries/) | `bioskills` | Resolves rsIDs, navigates RsMergeArch/SNPHistory merge chains, and converts between rsID, SPDI, HGVS, and VCF represe... |
| [bio-clinical-databases-gnomad-frequencies](skills/bioskills/gnomad-frequencies/) | `bioskills` | Queries gnomAD v4 (807k samples), v3, v2.1.1, and constraint metrics with grpmax FAF95, bottleneck-group exclusion, L... |
| [bio-clinical-databases-hla-typing](skills/bioskills/hla-typing/) | `bioskills` | Calls HLA class I and class II alleles at 2/4/6/8-field resolution from WGS/WES/RNA-seq/long-read data using OptiType... |
| [bio-clinical-databases-msi-detection](skills/bioskills/msi-detection/) | `bioskills` | Calls microsatellite instability from WES/WGS/targeted-panel with MSIsensor, MSIsensor-pro, MSIsensor-ct (panel-aware... |
| [bio-clinical-databases-myvariant-queries](skills/bioskills/myvariant-queries/) | `bioskills` | Queries myvariant.info BioThings aggregator for ClinVar, gnomAD, dbSNP, dbNSFP, COSMIC, CADD, and CIViC annotations i... |
| [bio-clinical-databases-pharmacogenomics](skills/bioskills/pharmacogenomics/) | `bioskills` | Queries PharmGKB / CPIC / DPWG for drug-gene interactions; calls CYP2D6/CYP2C9/CYP2C19/DPYD/TPMT/NUDT15/UGT1A1/SLCO1B... |
| [bio-clinical-databases-somatic-signatures](skills/bioskills/somatic-signatures/) | `bioskills` | Extracts and assigns COSMIC v3.4 mutational signatures (84 SBS / 11 DBS / 18 ID / 24 CN / 16 SV) from somatic VCFs us... |
| [bio-clinical-databases-tumor-mutational-burden](skills/bioskills/tumor-mutational-burden/) | `bioskills` | Calculates tumor mutational burden from WES/WGS/panel data with Friends of Cancer Research harmonization equations, p... |
| [bio-clinical-databases-variant-prioritization](skills/bioskills/variant-prioritization/) | `bioskills` | Prioritizes rare-disease variants from trio/quad WES/WGS with de novo (DeNovoGear, Triodenovo), compound-heterozygous... |
| [bio-clip-seq-clip-alignment](skills/bioskills/clip-alignment/) | `bioskills` | Align preprocessed CLIP-seq reads (eCLIP, iCLIP, iCLIP2, PAR-CLIP) to genome with STAR or bowtie2 using crosslink-pre... |
| [bio-clip-seq-clip-deep-learning](skills/bioskills/clip-deep-learning/) | `bioskills` | Predict RBP binding from RNA sequence using deep learning models (RBPNet sequence-to-signal, RNAProt RNN, GraphProt2 ... |
| [bio-clip-seq-clip-peak-calling](skills/bioskills/clip-peak-calling/) | `bioskills` | Call protein-RNA binding sites from CLIP-seq BAM with CLIPper, PureCLIP, Skipper, Piranha, omniCLIP, CTK, CLAM, or Pa... |
| [bio-clip-seq-clip-preprocessing](skills/bioskills/clip-preprocessing/) | `bioskills` | Preprocess CLIP-seq reads (eCLIP, iCLIP, iCLIP2, iCLIP3, irCLIP, PAR-CLIP, FLASH) with protocol-specific UMI extracti... |
| [bio-clip-seq-crosslink-site-detection](skills/bioskills/crosslink-site-detection/) | `bioskills` | Detect single-nucleotide crosslink (CL) sites in CLIP-seq data using truncation patterns (iCLIP/eCLIP CITS), crosslin... |
| [bio-comparative-genomics-ancestral-reconstruction](skills/bioskills/ancestral-reconstruction/) | `bioskills` | Reconstruct ancestral states at internal phylogenetic nodes for sequences (PAML codeml, IQ-TREE --ancestral, GRASP, F... |
| [bio-comparative-genomics-comparative-annotation-projection](skills/bioskills/comparative-annotation-projection/) | `bioskills` | Project gene annotations across genomes using TOGA (Kirilenko 2023 whole-genome-alignment chain-based projection with... |
| [bio-comparative-genomics-gene-family-evolution](skills/bioskills/gene-family-evolution/) | `bioskills` | Model gene-family birth-death dynamics across a species tree using CAFE5 (Mendes et al 2020 Bioinformatics 36:5516 ga... |
| [bio-comparative-genomics-gene-tree-species-tree-reconciliation](skills/bioskills/gene-tree-species-tree-reconciliation/) | `bioskills` | Reconcile gene trees against a species tree under probabilistic models of duplication, transfer, and loss (DTL) using... |
| [bio-comparative-genomics-genome-distance-and-species-delineation](skills/bioskills/genome-distance-and-species-delineation/) | `bioskills` | Compute genome-to-genome distances (ANI, AAI, dDDH, k-mer Mash) and assign taxonomic classifications using skani (Sha... |
| [bio-comparative-genomics-hgt-detection](skills/bioskills/hgt-detection/) | `bioskills` | Detect horizontal gene transfer (HGT / LGT) using compositional methods (GC%, codon usage, tetranucleotide z-scores v... |
| [bio-comparative-genomics-introgression-detection](skills/bioskills/introgression-detection/) | `bioskills` | Detect introgression and admixture between species or populations using Dsuite (Malinsky 2021 fast D-statistics), Pat... |
| [bio-comparative-genomics-ortholog-inference](skills/bioskills/ortholog-inference/) | `bioskills` | Infer orthologous genes and gene families across species using OrthoFinder3 (HOG-based phylogenetic orthology), Sonic... |
| [bio-comparative-genomics-pangenome-analysis](skills/bioskills/pangenome-analysis/) | `bioskills` | Build and analyze pangenomes for prokaryotes (Panaroo, PPanGGOLiN, PEPPAN, GET_HOMOLOGUES, anvi'o pangenomics) and eu... |
| [bio-comparative-genomics-positive-selection](skills/bioskills/positive-selection/) | `bioskills` | Detect positive (diversifying / episodic / pervasive) selection using codon dN/dS frameworks. Implements PAML codeml ... |
| [bio-comparative-genomics-synteny-analysis](skills/bioskills/synteny-analysis/) | `bioskills` | Detect syntenic blocks and structural rearrangements between genomes using MCScanX (Wang 2012), JCVI/MCScan (Tang 200... |
| [bio-comparative-genomics-whole-genome-alignment](skills/bioskills/whole-genome-alignment/) | `bioskills` | Build whole-genome alignments using Progressive Cactus (Armstrong 2020 reference-free clade-level WGA), Minigraph-Cac... |
| [bio-comparative-genomics-whole-genome-duplication](skills/bioskills/whole-genome-duplication/) | `bioskills` | Detect, date, and contextualize whole-genome duplication (WGD / paleopolyploidy) events using wgd v2 (Chen & Zwaenepo... |
| [bio-conformer-generation](skills/bioskills/conformer-generation/) | `bioskills` | Generates 3D conformer ensembles using RDKit ETKDGv3 with knowledge-enhanced distance geometry, MMFF94/UFF force-fiel... |
| [bio-consensus-sequences](skills/bioskills/consensus-sequences/) | `bioskills` | Generate consensus FASTA sequences by applying VCF variants to a reference using bcftools consensus. Use when creatin... |
| [bio-copy-number-allele-specific-copy-number](skills/bioskills/allele-specific-copy-number/) | `bioskills` | Infer integer allele-specific copy number, tumor purity, and ploidy from tumor sequencing by jointly modeling read de... |
| [bio-copy-number-cnv-annotation](skills/bioskills/cnv-annotation/) | `bioskills` | Annotate copy number variant segments with overlapping genes, dosage-sensitivity scores, cancer driver databases, pop... |
| [bio-copy-number-cnv-visualization](skills/bioskills/cnv-visualization/) | `bioskills` | Visualize copy number profiles, segments, allele-specific tracks, and cohort patterns from CNVkit, GATK, ASCAT, FACET... |
| [bio-copy-number-cnvkit-analysis](skills/bioskills/cnvkit-analysis/) | `bioskills` | Detect somatic and germline copy number variants from targeted, exome, and whole-genome sequencing with CNVkit, a rea... |
| [bio-copy-number-focal-amplification-ecdna](skills/bioskills/focal-amplification-ecdna/) | `bioskills` | Resolve the architecture of focal oncogene amplifications — extrachromosomal DNA (ecDNA), breakage-fusion-bridge (BFB... |
| [bio-copy-number-gatk-cnv](skills/bioskills/gatk-cnv/) | `bioskills` | Call copy number variants with the GATK best-practices workflows — the somatic CNV pipeline (CollectReadCounts, Denoi... |
| [bio-copy-number-germline-cnv-interpretation](skills/bioskills/germline-cnv-interpretation/) | `bioskills` | Classify constitutional (germline) copy number variants for clinical reporting using the 2019 ACMG/ClinGen technical ... |
| [bio-copy-number-hrd-scoring](skills/bioskills/hrd-scoring/) | `bioskills` | Quantify homologous recombination deficiency (HRD) from tumor copy number using the three genomic-scar metrics — loss... |
| [bio-copy-number-subclonal-copy-number](skills/bioskills/subclonal-copy-number/) | `bioskills` | Resolve subclonal copy number, whole-genome doubling, and copy-number tumor evolution from bulk sequencing with Batte... |
| [bio-crispr-screens-bagel-essentiality](skills/bioskills/bagel-essentiality/) | `bioskills` | Identifies essential genes from CRISPR-Cas9 fitness screens using BAGEL2 (Kim & Hart 2021 Genome Med), a Bayesian cla... |
| [bio-crispr-screens-base-editing-analysis](skills/bioskills/base-editing-analysis/) | `bioskills` | Analyzes base-editing screens for variant function. Covers library design (Sanson 2020 GRACE, Hanna 2021 BRCA1/2 SNV ... |
| [bio-crispr-screens-copy-number-correction](skills/bioskills/copy-number-correction/) | `bioskills` | Corrects the gene-independent copy-number artifact in CRISPR-Cas9 screens (Aguirre 2016 / Munoz 2016 Cancer Discov) w... |
| [bio-crispr-screens-crispresso-editing](skills/bioskills/crispresso-editing/) | `bioskills` | Quantifies CRISPR editing outcomes with CRISPResso2 (Clement 2019 Nat Biotechnol) across Cas9-nuclease (indels, HDR),... |
| [bio-crispr-screens-drugz-chemogenomic](skills/bioskills/drugz-chemogenomic/) | `bioskills` | Analyzes CRISPR drug-modifier (chemogenomic) screens with drugZ (Li & Hart 2019 Genome Med), a bidirectional Z-score ... |
| [bio-crispr-screens-hit-calling](skills/bioskills/hit-calling/) | `bioskills` | Cross-method decision tree for calling hits in pooled CRISPR screens. Catalogs statistical models (MAGeCK RRA, MAGeCK... |
| [bio-crispr-screens-in-vivo-screens](skills/bioskills/in-vivo-screens/) | `bioskills` | Designs and analyzes in vivo CRISPR screens in animal tumor models, organoids, and immune-cell adoptive transfers. Co... |
| [bio-crispr-screens-jacks-analysis](skills/bioskills/jacks-analysis/) | `bioskills` | Runs JACKS (Joint Analysis of CRISPR/Cas9 Knockout Screens; Allen et al 2019 Genome Research) which models per-sgRNA ... |
| [bio-crispr-screens-library-design](skills/bioskills/library-design/) | `bioskills` | Designs pooled sgRNA libraries for CRISPR knockout, interference (CRISPRi), activation (CRISPRa), Cas12a multiplex, b... |
| [bio-crispr-screens-mageck-analysis](skills/bioskills/mageck-analysis/) | `bioskills` | Analyzes pooled CRISPR screens with MAGeCK (Li et al 2014), covering count generation (mageck count), the RRA two-con... |
| [bio-crispr-screens-prime-editing-screens](skills/bioskills/prime-editing-screens/) | `bioskills` | Designs and analyzes pooled prime-editor (PE) screens for installing precise genetic variants without bystander confo... |
| [bio-ctdna-mutation-detection](skills/bioskills/ctdna-mutation-detection/) | `bioskills` | Detects somatic mutations in circulating tumor DNA using variant callers optimized for low allele fractions with UMI-... |
| [bio-data-visualization-circos-plots](skills/bioskills/circos-plots/) | `bioskills` | Build circular genome visualizations using circlize (R), pyCirclize (Python), or Circos (Perl CLI) with ideogram trac... |
| [bio-data-visualization-distribution-plots](skills/bioskills/distribution-plots/) | `bioskills` | Plot per-group distributions of continuous data using boxplots, violins, beeswarms, quasirandom jitter, and raincloud... |
| [bio-data-visualization-flow-and-transition-plots](skills/bioskills/flow-and-transition-plots/) | `bioskills` | Build Sankey, alluvial, river, and CONSORT-style flow diagrams to visualize cohort transitions, cell-state changes, o... |
| [bio-data-visualization-genome-browser-tracks](skills/openclaw/bio-data-visualization-genome-browser-tracks/) | `openclaw` | Generate genome browser visualizations using pyGenomeTracks or IGV batch scripting for publication figures. Use when ... |
| [bio-data-visualization-genome-tracks](skills/bioskills/genome-tracks/) | `bioskills` | Build genome-browser-style multi-track figures with pyGenomeTracks (config-driven), Gviz (R), and IGV batch screensho... |
| [bio-data-visualization-heatmaps-clustering](skills/bioskills/heatmaps-clustering/) | `bioskills` | Build clustered heatmaps for expression matrices and other features-by-samples data with rigorous distance/linkage/sc... |
| [bio-data-visualization-lollipop-protein-maps](skills/bioskills/lollipop-protein-maps/) | `bioskills` | Plot per-gene mutation distributions on a protein-domain map (lollipop / needle plots) showing mutation position, rec... |
| [bio-data-visualization-manhattan-qq-locuszoom](skills/bioskills/manhattan-qq-locuszoom/) | `bioskills` | Build Manhattan, Miami, QQ, and locuszoom-style regional plots from GWAS, TWAS, PWAS, and QTL summary statistics with... |
| [bio-data-visualization-oncoprint-mutation-matrices](skills/bioskills/oncoprint-mutation-matrices/) | `bioskills` | Build OncoPrint and co-mutation matrix plots from somatic-variant cohorts using ComplexHeatmap, maftools, and comut.p... |
| [bio-data-visualization-upset-plots](skills/bioskills/upset-plots/) | `bioskills` | Build UpSet plots to visualize set intersections beyond 4 sets (where Venn fails) using ComplexUpset (modern, ggplot2... |
| [bio-de-visualization](skills/bioskills/de-visualization/) | `bioskills` | Visualize differential expression results using DESeq2/edgeR built-in functions. Covers plotMA, plotDispEsts, plotCou... |
| [bio-duplicate-handling](skills/bioskills/duplicate-handling/) | `bioskills` | Mark and remove PCR/optical duplicates using samtools fixmate and markdup. Use when preparing alignments for variant ... |
| [bio-ecological-genomics-biodiversity-metrics](skills/bioskills/biodiversity-metrics/) | `bioskills` | Calculates species richness, diversity, and turnover using the Hill number framework with iNEXT coverage-based rarefa... |
| [bio-ecological-genomics-community-ecology](skills/bioskills/community-ecology/) | `bioskills` | Analyzes community composition using constrained ordination (CCA, RDA, db-RDA), variance partitioning (varpart), indi... |
| [bio-ecological-genomics-conservation-genetics](skills/bioskills/conservation-genetics/) | `bioskills` | Assesses genetic health of populations for conservation using effective population size estimation (GONE2 for recent ... |
| [bio-ecological-genomics-edna-metabarcoding](skills/bioskills/edna-metabarcoding/) | `bioskills` | Processes environmental DNA metabarcoding data from raw amplicon reads to species occurrence tables using OBITools3, ... |
| [bio-ecological-genomics-landscape-genomics](skills/bioskills/landscape-genomics/) | `bioskills` | Tests genotype-environment associations and identifies loci under local adaptation using LFMM2 (LEA), pcadapt outlier... |
| [bio-ecological-genomics-species-delimitation](skills/bioskills/species-delimitation/) | `bioskills` | Delimits species boundaries from molecular data using distance-based (ASAP), tree-based (bPTP, GMYC), and coalescent ... |
| [bio-ensembl-rest](skills/bioskills/ensembl-rest/) | `bioskills` | Query the Ensembl REST API for gene/transcript/protein lookup, sequence retrieval, comparative genomics (Compara), va... |
| [bio-entrez-fetch](skills/bioskills/entrez-fetch/) | `bioskills` | Retrieve records from NCBI databases using Biopython Bio.Entrez (EFetch, ESummary). Use when downloading sequences, f... |
| [bio-entrez-link](skills/bioskills/entrez-link/) | `bioskills` | Find cross-database references between NCBI databases using Biopython Bio.Entrez (ELink). Use when navigating gene to... |
| [bio-entrez-search](skills/bioskills/entrez-search/) | `bioskills` | Search NCBI databases using Biopython Bio.Entrez (ESearch, EInfo, EGQuery, ESpell). Use when finding records by keywo... |
| [bio-epidemiological-genomics-amr-surveillance](skills/bioskills/amr-surveillance/) | `bioskills` | Detect and track antimicrobial resistance genes using AMRFinderPlus and ResFinder with epidemiological context. Monit... |
| [bio-epidemiological-genomics-pathogen-typing](skills/bioskills/pathogen-typing/) | `bioskills` | Perform multi-locus sequence typing (MLST), core genome MLST, and SNP-based strain typing for bacterial isolate chara... |
| [bio-epidemiological-genomics-phylodynamics](skills/bioskills/phylodynamics/) | `bioskills` | Construct time-scaled phylogenies and infer evolutionary dynamics using TreeTime and BEAST2 for outbreak analysis. Es... |
| [bio-epidemiological-genomics-transmission-inference](skills/bioskills/transmission-inference/) | `bioskills` | Infer pathogen transmission networks and identify likely transmission pairs using TransPhylo and outbreak reconstruct... |
| [bio-epidemiological-genomics-variant-surveillance](skills/bioskills/variant-surveillance/) | `bioskills` | Assign pathogen lineages and track variants using Nextclade and pangolin for viral surveillance. Monitor variant prev... |
| [bio-epitranscriptomics-merip-preprocessing](skills/bioskills/merip-preprocessing/) | `bioskills` | Align and QC MeRIP-seq IP and input samples for m6A analysis. Use when preparing MeRIP-seq data for peak calling or d... |
| [bio-epitranscriptomics-modification-visualization](skills/bioskills/modification-visualization/) | `bioskills` | Create metagene plots and browser tracks for RNA modification data. Use when visualizing m6A distribution patterns ar... |
| [bio-experimental-design-batch-design](skills/bioskills/batch-design/) | `bioskills` | Designs experiments to minimize and account for batch effects using balanced layouts and blocking strategies. Use whe... |
| [bio-experimental-design-multiple-testing](skills/bioskills/multiple-testing/) | `bioskills` | Applies multiple testing correction methods including FDR, Bonferroni, and q-value for genomics data. Use when filter... |
| [bio-experimental-design-power-analysis](skills/bioskills/power-analysis/) | `bioskills` | Calculates statistical power and minimum sample sizes for RNA-seq, ATAC-seq, and other sequencing experiments. Use wh... |
| [bio-experimental-design-sample-size](skills/bioskills/sample-size/) | `bioskills` | Estimates required sample sizes for differential expression, ChIP-seq, methylation, and proteomics studies. Use when ... |
| [bio-expression-matrix-gene-id-mapping](skills/bioskills/gene-id-mapping/) | `bioskills` | Convert between gene identifier systems including Ensembl, Entrez, HGNC symbols, and UniProt. Use when mapping IDs fo... |
| [bio-expression-matrix-metadata-joins](skills/bioskills/metadata-joins/) | `bioskills` | Merge sample metadata with count matrices and add gene annotations. Use when preparing data for differential expressi... |
| [bio-fastq-quality](skills/bioskills/fastq-quality/) | `bioskills` | Work with FASTQ quality scores using Biopython. Use when analyzing read quality, filtering by quality, trimming low-q... |
| [bio-flow-cytometry-cytometry-qc](skills/bioskills/cytometry-qc/) | `bioskills` | Comprehensive quality control for flow cytometry and CyTOF data. Covers flow rate stability, signal drift, margin eve... |
| [bio-format-conversion](skills/bioskills/format-conversion/) | `bioskills` | Convert between sequence file formats (FASTA, FASTQ, GenBank, EMBL) using Biopython Bio.SeqIO. Use when changing file... |
| [bio-free-energy-calculations](skills/bioskills/free-energy-calculations/) | `bioskills` | Performs alchemical free-energy calculations including relative binding free energy (RBFE / FEP+) and absolute bindin... |
| [bio-gatk-variant-calling](skills/bioskills/gatk-variant-calling/) | `bioskills` | Variant calling with GATK HaplotypeCaller following best practices. Covers germline SNP/indel calling, GVCF workflow ... |
| [bio-genome-annotation-annotation-transfer](skills/bioskills/annotation-transfer/) | `bioskills` | Transfer gene annotations between genome assemblies using Liftoff for same-species annotation liftover and MiniProt f... |
| [bio-genome-annotation-eukaryotic-gene-prediction](skills/bioskills/eukaryotic-gene-prediction/) | `bioskills` | Predict protein-coding genes in eukaryotic genomes using BRAKER3 for combined RNA-seq and protein evidence, or GALBA ... |
| [bio-genome-annotation-functional-annotation](skills/bioskills/functional-annotation/) | `bioskills` | Assign GO terms, KEGG orthologs, Pfam domains, and EC numbers to predicted proteins using eggNOG-mapper and InterProS... |
| [bio-genome-annotation-ncrna-annotation](skills/bioskills/ncrna-annotation/) | `bioskills` | Identify non-coding RNAs including tRNAs, rRNAs, snoRNAs, and regulatory RNAs using Infernal covariance model searche... |
| [bio-genome-annotation-prokaryotic-annotation](skills/bioskills/prokaryotic-annotation/) | `bioskills` | Annotate bacterial and archaeal genomes with Bakta for comprehensive structural and functional annotation, or Prokka ... |
| [bio-genome-annotation-repeat-annotation](skills/bioskills/repeat-annotation/) | `bioskills` | Identify and classify repetitive elements and transposable elements using RepeatModeler for de novo repeat library co... |
| [bio-genome-assembly-assembly-polishing](skills/bioskills/assembly-polishing/) | `bioskills` | Polish genome assemblies to reduce errors using short reads (Pilon), long reads (Racon), or ONT-specific tools (medak... |
| [bio-genome-assembly-assembly-qc](skills/bioskills/assembly-qc/) | `bioskills` | Assess genome assembly quality using QUAST for contiguity metrics and BUSCO for completeness. Essential for evaluatin... |
| [bio-genome-assembly-contamination-detection](skills/bioskills/contamination-detection/) | `bioskills` | Detect contamination and assess genome quality using CheckM, CheckM2, GTDB-Tk, and GUNC for metagenome-assembled geno... |
| [bio-genome-assembly-hifi-assembly](skills/bioskills/hifi-assembly/) | `bioskills` | High-quality genome assembly from PacBio HiFi reads using hifiasm with phasing support. Use when building reference-q... |
| [bio-genome-assembly-long-read-assembly](skills/bioskills/long-read-assembly/) | `bioskills` | De novo genome assembly from Oxford Nanopore or PacBio long reads using Flye and Canu. Produces highly contiguous ass... |
| [bio-genome-assembly-metagenome-assembly](skills/bioskills/metagenome-assembly/) | `bioskills` | Metagenome assembly from long reads using metaFlye and metaSPAdes with binning strategies. Use when reconstructing ge... |
| [bio-genome-assembly-scaffolding](skills/bioskills/scaffolding/) | `bioskills` | Scaffold contigs into chromosome-level assemblies using Hi-C data with YaHS, 3D-DNA, SALSA2, and validate with BUSCO ... |
| [bio-genome-assembly-short-read-assembly](skills/bioskills/short-read-assembly/) | `bioskills` | De novo genome assembly from Illumina short reads using SPAdes. Covers bacterial, fungal, and small eukaryotic genome... |
| [bio-genome-engineering-base-editing-design](skills/bioskills/base-editing-design/) | `bioskills` | Design guides for cytosine and adenine base editing using editing window optimization and BE-Hive outcome prediction.... |
| [bio-genome-engineering-grna-design](skills/bioskills/grna-design/) | `bioskills` | Design guide RNAs for CRISPR-Cas9/Cas12a experiments using CRISPRscan and local scoring algorithms. Score guides for ... |
| [bio-genome-engineering-hdr-template-design](skills/bioskills/hdr-template-design/) | `bioskills` | Design homology-directed repair donor templates for CRISPR knock-ins using primer3-py. Create ssODN, dsDNA, or plasmi... |
| [bio-genome-engineering-off-target-prediction](skills/bioskills/off-target-prediction/) | `bioskills` | Predict CRISPR off-target sites using Cas-OFFinder and CFD scoring algorithms. Identify potential unintended cleavage... |
| [bio-genome-engineering-prime-editing-design](skills/bioskills/prime-editing-design/) | `bioskills` | Design pegRNAs for prime editing using PrimeDesign algorithms. Generate spacer, PBS, and RT template sequences for pr... |
| [bio-genome-intervals-bed-file-basics](skills/bioskills/bed-file-basics/) | `bioskills` | BED file format fundamentals, creation, validation, and basic operations. Covers BED3 through BED12 formats, coordina... |
| [bio-genome-intervals-bigwig-tracks](skills/bioskills/bigwig-tracks/) | `bioskills` | Create and read bigWig browser tracks for visualizing continuous genomic data. Convert bedGraph to bigWig, extract si... |
| [bio-genome-intervals-coverage-analysis](skills/bioskills/coverage-analysis/) | `bioskills` | Calculate read depth and coverage across genomic intervals using bedtools genomecov and coverage. Generate bedGraph f... |
| [bio-genome-intervals-gtf-gff-handling](skills/bioskills/gtf-gff-handling/) | `bioskills` | Parse, query, and convert GTF and GFF3 annotation files. Extract gene, transcript, and exon coordinates using gffread... |
| [bio-genome-intervals-interval-arithmetic](skills/bioskills/interval-arithmetic/) | `bioskills` | Core interval arithmetic operations including intersect, subtract, merge, complement, map, and groupby using bedtools... |
| [bio-genome-intervals-proximity-operations](skills/bioskills/proximity-operations/) | `bioskills` | Find nearest features, search within windows, and extend intervals using closest, window, flank, and slop operations.... |
| [bio-hi-c-analysis-contact-pairs](skills/bioskills/contact-pairs/) | `bioskills` | Process Hi-C read pairs using pairtools. Parse alignments, filter duplicates, classify pairs, and generate contact st... |
| [bio-hi-c-analysis-hic-visualization](skills/bioskills/hic-visualization/) | `bioskills` | Visualize Hi-C contact matrices, TADs, loops, and genomic features using matplotlib, cooltools, and HiCExplorer. Crea... |
| [bio-immunoinformatics-epitope-prediction](skills/bioskills/epitope-prediction/) | `bioskills` | Predict B-cell and T-cell epitopes using BepiPred, IEDB tools, and structure-based methods for vaccine and antibody d... |
| [bio-liquid-biopsy-pipeline](skills/bioskills/liquid-biopsy-pipeline/) | `bioskills` | Cell-free DNA analysis pipeline from plasma sequencing to tumor monitoring. Preprocesses cfDNA reads, analyzes fragme... |
| [bio-local-blast](skills/bioskills/local-blast/) | `bioskills` | Build local BLAST databases and run searches using NCBI BLAST+ command-line tools. Use when running >50 queries, buil... |
| [bio-long-read-sequencing-clair3-variants](skills/bioskills/clair3-variants/) | `bioskills` | Deep learning-based variant calling from long reads using Clair3 for SNPs and small indels. Use when calling germline... |
| [bio-long-read-sequencing-isoseq-analysis](skills/bioskills/isoseq-analysis/) | `bioskills` | Analyze PacBio Iso-Seq data for full-length isoform discovery and quantification. Use when characterizing transcript ... |
| [bio-long-read-splicing](skills/bioskills/long-read-splicing/) | `bioskills` | Analyzes alternative splicing from PacBio Iso-Seq (HiFi, Kinnex/MAS-Iso-seq) and Oxford Nanopore (direct cDNA, direct... |
| [bio-longitudinal-monitoring](skills/bioskills/longitudinal-monitoring/) | `bioskills` | Tracks ctDNA dynamics over time for treatment response monitoring using serial liquid biopsy samples. Analyzes tumor ... |
| [bio-longread-alignment](skills/bioskills/long-read-alignment/) | `bioskills` | Align long reads using minimap2 for Oxford Nanopore and PacBio data. Supports various presets for different read type... |
| [bio-longread-medaka](skills/bioskills/medaka-polishing/) | `bioskills` | Polish assemblies and call variants from Oxford Nanopore data using medaka. Uses neural networks trained on specific ... |
| [bio-longread-qc](skills/bioskills/long-read-qc/) | `bioskills` | Quality control for long-read sequencing data using NanoPlot, NanoStat, and chopper. Generate QC reports, filter read... |
| [bio-longread-structural-variants](skills/bioskills/structural-variants/) | `bioskills` | Detect structural variants from long-read alignments using Sniffles, cuteSV, and SVIM. Use when detecting deletions, ... |
| [bio-machine-learning-omics-classifiers](skills/bioskills/omics-classifiers/) | `bioskills` | Builds classification models for omics data using RandomForest, XGBoost, and logistic regression with sklearn-compati... |
| [bio-metabolomics-msdial-preprocessing](skills/bioskills/msdial-preprocessing/) | `bioskills` | MS-DIAL-based metabolomics preprocessing as alternative to XCMS. Covers peak detection, alignment, annotation, and ex... |
| [bio-metabolomics-pathway-mapping](skills/bioskills/pathway-mapping/) | `bioskills` | Map metabolites to biological pathways using KEGG, Reactome, and MetaboAnalyst. Perform pathway enrichment and topolo... |
| [bio-metabolomics-xcms-preprocessing](skills/bioskills/xcms-preprocessing/) | `bioskills` | XCMS3 workflow for LC-MS/MS metabolomics preprocessing. Covers peak detection, retention time alignment, corresponden... |
| [bio-metagenomics-abundance](skills/bioskills/abundance-estimation/) | `bioskills` | Species abundance estimation using Bracken with Kraken2 output. Redistributes reads from higher taxonomic levels to s... |
| [bio-metagenomics-amr-detection](skills/bioskills/amr-detection/) | `bioskills` | Detect antimicrobial resistance genes using AMRFinderPlus, ResFinder, and CARD. Screen isolates and metagenomes for r... |
| [bio-metagenomics-functional-profiling](skills/bioskills/functional-profiling/) | `bioskills` | Profile functional potential of metagenomes using HUMAnN3 and similar tools. Use when obtaining pathway abundances, g... |
| [bio-metagenomics-kraken](skills/bioskills/kraken-classification/) | `bioskills` | Taxonomic classification of metagenomic reads using Kraken2. Fast k-mer based classification against RefSeq database.... |
| [bio-metagenomics-metaphlan](skills/bioskills/metaphlan-profiling/) | `bioskills` | Marker gene-based taxonomic profiling using MetaPhlAn 4. Provides accurate species-level relative abundances using cl... |
| [bio-metagenomics-strain-tracking](skills/bioskills/strain-tracking/) | `bioskills` | Track bacterial strains using MASH, sourmash, fastANI, and inStrain. Compare genomes, detect contamination, and monit... |
| [bio-metagenomics-visualization](skills/bioskills/metagenome-visualization/) | `bioskills` | Visualize metagenomic profiles using R (phyloseq, microbiome) and Python (matplotlib, seaborn). Create stacked bar pl... |
| [bio-methylation-bismark-alignment](skills/bioskills/bismark-alignment/) | `bioskills` | Bisulfite sequencing read alignment using Bismark with bowtie2/hisat2. Handles genome preparation and produces BAM fi... |
| [bio-methylation-calling](skills/bioskills/methylation-calling/) | `bioskills` | Extract methylation calls from Bismark BAM files using bismark_methylation_extractor. Generates per-cytosine reports ... |
| [bio-methylation-methylkit](skills/bioskills/methylkit-analysis/) | `bioskills` | DNA methylation analysis with methylKit in R. Import Bismark coverage files, filter by coverage, normalize samples, a... |
| [bio-microbiome-amplicon-processing](skills/bioskills/amplicon-processing/) | `bioskills` | Amplicon sequence variant (ASV) inference from 16S rRNA or ITS amplicon sequencing using DADA2. Covers quality filter... |
| [bio-microbiome-diversity-analysis](skills/bioskills/diversity-analysis/) | `bioskills` | Alpha and beta diversity analysis for microbiome data. Calculate within-sample richness, evenness, and between-sample... |
| [bio-microbiome-functional-prediction](skills/bioskills/functional-prediction/) | `bioskills` | Predict metagenome functional content from 16S rRNA marker gene data using PICRUSt2. Infer KEGG, MetaCyc, and EC abun... |
| [bio-multi-omics-data-harmonization](skills/bioskills/data-harmonization/) | `bioskills` | Preprocessing and harmonization of multi-omics data before integration. Covers normalization, batch correction, featu... |
| [bio-ncbi-datasets-cli](skills/bioskills/ncbi-datasets-cli/) | `bioskills` | Download genome assemblies, gene records, and ortholog data from NCBI using the modern Datasets v2 CLI (replaces asse... |
| [bio-ortholog-inference](skills/bioskills/ortholog-inference/) | `bioskills` | Pull pre-computed ortholog calls from public databases (OrthoDB, Ensembl Compara, OMA browser, eggNOG, PANTHER, KEGG ... |
| [bio-outlier-splicing-detection](skills/bioskills/outlier-splicing-detection/) | `bioskills` | Detects aberrant splicing in single rare-disease patients vs a control panel using FRASER 2.0 (Bioconductor; Beta-bin... |
| [bio-paired-end-fastq](skills/bioskills/paired-end-fastq/) | `bioskills` | Handle paired-end FASTQ files (R1/R2) using Biopython. Use when working with Illumina paired reads, synchronizing pai... |
| [bio-pharmacophore-modeling](skills/bioskills/pharmacophore-modeling/) | `bioskills` | Builds and applies 3D pharmacophore models using RDKit Pharm3D, the apo2ph4 receptor-based workflow (Heider et al 202... |
| [bio-phasing-imputation-genotype-imputation](skills/bioskills/genotype-imputation/) | `bioskills` | Impute missing genotypes using reference panels with Beagle or Minimac4. Use when increasing variant density for GWAS... |
| [bio-phasing-imputation-haplotype-phasing](skills/bioskills/haplotype-phasing/) | `bioskills` | Phase genotypes into haplotypes using Beagle or SHAPEIT. Resolves which alleles are inherited together on each chromo... |
| [bio-phasing-imputation-imputation-qc](skills/bioskills/imputation-qc/) | `bioskills` | Quality control of phasing and imputation results. Filter by INFO scores, assess accuracy, and prepare imputed data f... |
| [bio-phasing-imputation-reference-panels](skills/bioskills/reference-panels/) | `bioskills` | Download, prepare, and manage reference panels for phasing and imputation. Covers 1000 Genomes, HRC, and TOPMed panel... |
| [bio-phylo-bayesian-inference](skills/bioskills/bayesian-inference/) | `bioskills` | Run Bayesian phylogenetic analysis with MrBayes, BEAST2, RevBayes, and PhyloBayes including MCMC convergence diagnost... |
| [bio-phylo-distance-calculations](skills/bioskills/distance-calculations/) | `bioskills` | Compute evolutionary distances and build phylogenetic trees using Biopython Bio.Phylo.TreeConstruction. Use when crea... |
| [bio-phylo-modern-tree-inference](skills/bioskills/modern-tree-inference/) | `bioskills` | Build maximum likelihood phylogenetic trees using IQ-TREE2 and RAxML-NG with expert model selection, branch support a... |
| [bio-phylogenomics](skills/omics/bio-phylogenomics/) | `omics` | Build marker gene alignments and phylogenetic trees. |
| [bio-pileup-generation](skills/bioskills/pileup-generation/) | `bioskills` | Generate pileup data for variant calling using samtools mpileup and pysam. Use when preparing data for variant callin... |
| [bio-population-genetics-association-testing](skills/bioskills/association-testing/) | `bioskills` | Genome-wide association studies (GWAS) with PLINK. Perform case-control and quantitative trait association testing us... |
| [bio-population-genetics-linkage-disequilibrium](skills/bioskills/linkage-disequilibrium/) | `bioskills` | Calculate linkage disequilibrium statistics (r², D'), perform LD pruning for population structure analysis, identify ... |
| [bio-population-genetics-plink-basics](skills/bioskills/plink-basics/) | `bioskills` | PLINK file formats, format conversion, and quality control filtering for population genetics. Convert between VCF, BE... |
| [bio-population-genetics-scikit-allel-analysis](skills/bioskills/scikit-allel-analysis/) | `bioskills` | Python population genetics with scikit-allel. Read VCF files, compute allele frequencies, calculate diversity statist... |
| [bio-population-genetics-selection-statistics](skills/bioskills/selection-statistics/) | `bioskills` | Detect signatures of natural selection using Fst, Tajima's D, iHS, XP-EHH, and other selection statistics. Calculate ... |
| [bio-protein-clustering-pangenome](skills/omics/bio-protein-clustering-pangenome/) | `omics` | Cluster proteins into orthogroups and derive pangenome matrices. |
| [bio-proteomics-proteomics-qc](skills/bioskills/proteomics-qc/) | `bioskills` | Quality control and assessment for proteomics data. Use when evaluating proteomics data quality before downstream ana... |
| [bio-proteomics-ptm-analysis](skills/bioskills/ptm-analysis/) | `bioskills` | Post-translational modification analysis including phosphorylation, acetylation, and ubiquitination. Covers site loca... |
| [bio-reaction-enumeration](skills/bioskills/reaction-enumeration/) | `bioskills` | Enumerates virtual chemical libraries via reaction SMARTS transformations using RDKit and Reaction templates, with ex... |
| [bio-read-alignment-bowtie2-alignment](skills/bioskills/bowtie2-alignment/) | `bioskills` | Align short reads using Bowtie2 with local or end-to-end modes. Supports gapped alignment. Use when aligning ChIP-seq... |
| [bio-read-alignment-bwa-alignment](skills/bioskills/bwa-alignment/) | `bioskills` | Align DNA short reads to reference genomes using bwa-mem2, the faster successor to BWA-MEM. Use when aligning DNA sho... |
| [bio-read-alignment-hisat2-alignment](skills/bioskills/hisat2-alignment/) | `bioskills` | Align RNA-seq reads with HISAT2, a memory-efficient splice-aware aligner. Use when STAR's memory requirements are too... |
| [bio-read-alignment-star-alignment](skills/bioskills/star-alignment/) | `bioskills` | Align RNA-seq reads with STAR (Spliced Transcripts Alignment to a Reference). Supports two-pass mode for novel splice... |
| [bio-read-qc-adapter-trimming](skills/bioskills/adapter-trimming/) | `bioskills` | Remove sequencing adapters from FASTQ files using Cutadapt and Trimmomatic. Supports single-end and paired-end reads,... |
| [bio-read-qc-contamination-screening](skills/bioskills/contamination-screening/) | `bioskills` | Detect sample contamination and cross-species reads using FastQ Screen. Screen reads against multiple reference genom... |
| [bio-read-qc-fastp-workflow](skills/bioskills/fastp-workflow/) | `bioskills` | All-in-one read preprocessing with fastp including adapter trimming, quality filtering, deduplication, base correctio... |
| [bio-read-qc-quality-reports](skills/bioskills/quality-reports/) | `bioskills` | Generate and interpret quality reports from FASTQ files using FastQC and MultiQC. Assess per-base quality, adapter co... |
| [bio-read-sequences](skills/bioskills/read-sequences/) | `bioskills` | Read biological sequence files (FASTA, FASTQ, GenBank, EMBL, ABI, SFF) using Biopython Bio.SeqIO. Use when parsing se... |
| [bio-reads-qc-mapping](skills/omics/bio-reads-qc-mapping/) | `omics` | Ingest, QC, and map reads with reproducible outputs. Use for raw read processing and coverage stats. |
| [bio-reference-operations](skills/bioskills/reference-operations/) | `bioskills` | Generate consensus sequences and manage reference files using samtools. Use when creating consensus from alignments, ... |
| [bio-remote-homology](skills/bioskills/remote-homology/) | `bioskills` | Detect distant homologs using profile and structure-aware methods that go beyond standard BLAST. Use when sequence id... |
| [bio-reporting-automated-qc-reports](skills/bioskills/automated-qc-reports/) | `bioskills` | Generates standardized quality control reports by aggregating metrics from FastQC, alignment, and other tools using M... |
| [bio-restriction-mapping](skills/bioskills/restriction-mapping/) | `bioskills` | Create restriction maps showing enzyme cut positions on DNA sequences using Biopython Bio.Restriction. Visualize cut ... |
| [bio-ribo-seq-riboseq-preprocessing](skills/bioskills/riboseq-preprocessing/) | `bioskills` | Preprocess ribosome profiling data including adapter trimming, size selection, rRNA removal, and alignment. Use when ... |
| [bio-rna-quantification-alignment-free-quant](skills/bioskills/alignment-free-quant/) | `bioskills` | Quantify transcript expression using pseudo-alignment with Salmon or kallisto. Use when quantifying transcripts with ... |
| [bio-rna-quantification-count-matrix-qc](skills/bioskills/count-matrix-qc/) | `bioskills` | Quality control and exploration of RNA-seq count matrices before differential expression. Check for outliers, batch e... |
| [bio-rna-quantification-featurecounts-counting](skills/bioskills/featurecounts-counting/) | `bioskills` | Count reads per gene from aligned BAM files using Subread featureCounts. Use when processing BAM files from STAR/HISA... |
| [bio-rna-structure-secondary-structure-prediction](skills/bioskills/secondary-structure-prediction/) | `bioskills` | Predicts RNA secondary structures using minimum free energy folding and partition function analysis with ViennaRNA (R... |
| [bio-sam-bam-basics](skills/bioskills/sam-bam-basics/) | `bioskills` | View, convert, and understand SAM/BAM/CRAM alignment files using samtools and pysam. Use when inspecting alignments, ... |
| [bio-sashimi-plots](skills/bioskills/sashimi-plots/) | `bioskills` | Creates sashimi-style plots showing RNA-seq read coverage and splice junction counts using ggsashimi (general-purpose... |
| [bio-shape-similarity](skills/bioskills/shape-similarity/) | `bioskills` | Performs 3D shape-based similarity searching using ROCS (OpenEye), USRCAT (ultra-fast), Open3DAlign (RDKit), ESPSim (... |
| [bio-small-rna-seq-mirge3-analysis](skills/bioskills/mirge3-analysis/) | `bioskills` | Fast miRNA quantification with isomiR detection and A-to-I editing analysis using miRge3. Use when quantifying known ... |
| [bio-splice-variant-prediction](skills/bioskills/splice-variant-prediction/) | `bioskills` | Predicts whether a DNA variant alters mRNA splicing using sequence-based deep-learning tools — SpliceAI (10kb context... |
| [bio-splicing-pipeline](skills/bioskills/splicing-pipeline/) | `bioskills` | End-to-end alternative splicing analysis from FASTQ to differential splicing results for short-read bulk RNA-seq. Ali... |
| [bio-splicing-qc](skills/bioskills/splicing-qc/) | `bioskills` | Assesses RNA-seq data quality specifically for alternative splicing analysis. QC layers include experimental design a... |
| [bio-splicing-quantification](skills/bioskills/splicing-quantification/) | `bioskills` | Quantifies alternative splicing as PSI (percent spliced in) from RNA-seq using rMATS-turbo (BAM-based event), SUPPA2 ... |
| [bio-systems-biology-flux-balance-analysis](skills/bioskills/flux-balance-analysis/) | `bioskills` | Perform flux balance analysis (FBA) and flux variability analysis (FVA) on genome-scale metabolic models using COBRAp... |
| [bio-systems-biology-metabolic-reconstruction](skills/bioskills/metabolic-reconstruction/) | `bioskills` | Build genome-scale metabolic models from genome sequences using CarveMe and gapseq for automated reconstruction. Gene... |
| [bio-systems-biology-model-curation](skills/bioskills/model-curation/) | `bioskills` | Validate, gap-fill, and curate genome-scale metabolic models using memote for quality scores and COBRApy for manual c... |
| [bio-tcr-bcr-analysis-mixcr-analysis](skills/bioskills/mixcr-analysis/) | `bioskills` | Perform V(D)J alignment and clonotype assembly from TCR-seq or BCR-seq data using MiXCR. Use when processing raw immu... |
| [bio-tcr-bcr-analysis-vdjtools-analysis](skills/bioskills/vdjtools-analysis/) | `bioskills` | Calculate immune repertoire diversity metrics, compare samples, and track clonal dynamics using VDJtools. Use when an... |
| [bio-temporal-genomics-circadian-rhythms](skills/bioskills/circadian-rhythms/) | `bioskills` | Detects circadian and ultradian rhythms in time-series omics data using CosinorPy cosinor models, MetaCycle (JTK_CYCL... |
| [bio-temporal-genomics-periodicity-detection](skills/bioskills/periodicity-detection/) | `bioskills` | Discovers periodic signals of unknown period in time-series omics data using Lomb-Scargle periodograms (scipy), autoc... |
| [bio-temporal-genomics-temporal-clustering](skills/bioskills/temporal-clustering/) | `bioskills` | Clusters genes by temporal expression profile shape using Mfuzz soft clustering, TCseq, and DEGreport degPatterns. Gr... |
| [bio-temporal-genomics-temporal-grn](skills/bioskills/temporal-grn/) | `bioskills` | Infers dynamic gene regulatory networks from bulk time-series expression data using Granger causality (statsmodels), ... |
| [bio-tumor-fraction-estimation](skills/bioskills/tumor-fraction-estimation/) | `bioskills` | Estimates circulating tumor DNA fraction from shallow whole-genome sequencing using ichorCNA. Detects copy number alt... |
| [bio-uniprot-access](skills/bioskills/uniprot-access/) | `bioskills` | Query UniProt's REST API (post-2022 endpoint at rest.uniprot.org) for protein sequences, annotations, GO terms, cross... |
| [bio-variant-annotation](skills/bioskills/variant-annotation/) | `bioskills` | Comprehensive variant annotation using bcftools annotate/csq, VEP, SnpEff, and ANNOVAR. Add database annotations, pre... |
| [bio-variant-calling](skills/bioskills/variant-calling/) | `bioskills` | Call SNPs and indels from aligned reads using bcftools mpileup and call. Use when detecting variants from BAM files o... |
| [bio-variant-calling-clinical-interpretation](skills/bioskills/clinical-interpretation/) | `bioskills` | Clinical variant interpretation using ClinVar, ACMG guidelines, and pathogenicity predictors. Prioritize variants for... |
| [bio-variant-calling-deepvariant](skills/bioskills/deepvariant/) | `bioskills` | Deep learning-based variant calling with Google DeepVariant. Provides high accuracy for germline SNPs and indels from... |
| [bio-variant-calling-filtering-best-practices](skills/bioskills/filtering-best-practices/) | `bioskills` | Comprehensive variant filtering including GATK VQSR, hard filters, bcftools expressions, and quality metric interpret... |
| [bio-variant-calling-joint-calling](skills/bioskills/joint-calling/) | `bioskills` | Joint genotype calling across multiple samples using GATK CombineGVCFs and GenotypeGVCFs. Essential for cohort studie... |
| [bio-variant-calling-structural-variant-calling](skills/bioskills/structural-variant-calling/) | `bioskills` | Call structural variants (SVs) from sequencing data using Manta, Delly, GRIDSS, and LUMPY. Detects deletions, inserti... |
| [bio-variant-normalization](skills/bioskills/variant-normalization/) | `bioskills` | Normalize indel representation, decompose MNPs, and split multiallelic variants using bcftools norm. Use when compari... |
| [bio-vcf-basics](skills/bioskills/vcf-basics/) | `bioskills` | View, query, and understand VCF/BCF variant files using bcftools and cyvcf2. Use when inspecting variants, extracting... |
| [bio-vcf-manipulation](skills/bioskills/vcf-manipulation/) | `bioskills` | Merge, concatenate, sort, intersect, and subset VCF files using bcftools. Use when combining variant files, comparing... |
| [bio-vcf-statistics](skills/bioskills/vcf-statistics/) | `bioskills` | Generate variant statistics, sample concordance, and quality metrics using bcftools stats and gtcheck. Use when evalu... |
| [bio-workflows-atacseq-pipeline](skills/bioskills/atacseq-pipeline/) | `bioskills` | End-to-end ATAC-seq workflow from FASTQ files to differential accessibility and TF footprinting. Covers alignment, pe... |
| [bio-workflows-causal-genomics-pipeline](skills/bioskills/causal-genomics-pipeline/) | `bioskills` | End-to-end post-GWAS causal inference pipeline orchestrating heritability partitioning, genetic correlation, Mendelia... |
| [bio-workflows-chipseq-pipeline](skills/bioskills/chipseq-pipeline/) | `bioskills` | End-to-end ChIP-seq workflow from FASTQ files to annotated peaks. Covers QC, alignment, peak calling with MACS3 (or H... |
| [bio-workflows-clip-pipeline](skills/bioskills/clip-pipeline/) | `bioskills` | End-to-end CLIP-seq pipeline from FASTQ to ENCODE-compliant binding sites, single-nucleotide crosslink maps, annotati... |
| [bio-workflows-cnv-pipeline](skills/bioskills/cnv-pipeline/) | `bioskills` | End-to-end copy number variant detection workflow from BAM files. Covers CNVkit analysis for exome/targeted sequencin... |
| [bio-workflows-edna-pipeline](skills/bioskills/edna-pipeline/) | `bioskills` | End-to-end eDNA metabarcoding from raw amplicons to community ecology. Covers QC, primer removal, denoising with OBIT... |
| [bio-workflows-fastq-to-variants](skills/bioskills/fastq-to-variants/) | `bioskills` | End-to-end DNA sequencing workflow from FASTQ files to variant calls. Covers QC, alignment with BWA, BAM processing, ... |
| [bio-workflows-genome-annotation-pipeline](skills/bioskills/genome-annotation-pipeline/) | `bioskills` | End-to-end genome annotation pipeline from assembled contigs to functional annotation, covering repeat masking, gene ... |
| [bio-workflows-genome-assembly-pipeline](skills/bioskills/genome-assembly-pipeline/) | `bioskills` | End-to-end genome assembly workflow from reads to polished assembly with QC. Supports short reads (SPAdes), long read... |
| [bio-workflows-gwas-pipeline](skills/bioskills/gwas-pipeline/) | `bioskills` | End-to-end GWAS workflow from VCF to association results. Covers PLINK QC, population structure correction, and assoc... |
| [bio-workflows-longread-sv-pipeline](skills/bioskills/longread-sv-pipeline/) | `bioskills` | End-to-end workflow for detecting structural variants from long-read sequencing data. Covers ONT/PacBio alignment wit... |
| [bio-workflows-merip-pipeline](skills/bioskills/merip-pipeline/) | `bioskills` | End-to-end MeRIP-seq analysis from FASTQ to m6A peaks and differential methylation. Use when analyzing epitranscripto... |
| [bio-workflows-metabolic-modeling-pipeline](skills/bioskills/metabolic-modeling-pipeline/) | `bioskills` | End-to-end genome-scale metabolic modeling from genome sequence to flux predictions. Covers automated reconstruction ... |
| [bio-workflows-metabolomics-pipeline](skills/bioskills/metabolomics-pipeline/) | `bioskills` | End-to-end metabolomics workflow from raw MS data to pathway analysis. Orchestrates XCMS preprocessing, annotation, n... |
| [bio-workflows-metagenomics-pipeline](skills/bioskills/metagenomics-pipeline/) | `bioskills` | End-to-end metagenomics workflow from FASTQ to taxonomic and functional profiles. Covers Kraken2 classification, Brac... |
| [bio-workflows-methylation-pipeline](skills/bioskills/methylation-pipeline/) | `bioskills` | End-to-end bisulfite sequencing workflow from FASTQ to differentially methylated regions. Covers Bismark alignment, m... |
| [bio-workflows-microbiome-pipeline](skills/bioskills/microbiome-pipeline/) | `bioskills` | End-to-end 16S amplicon workflow from FASTQ reads to differential abundance. Orchestrates DADA2 ASV inference, taxono... |
| [bio-workflows-neoantigen-pipeline](skills/bioskills/neoantigen-pipeline/) | `bioskills` | End-to-end neoantigen discovery from somatic variants to ranked vaccine candidates. Integrates HLA typing, MHC bindin... |
| [bio-workflows-riboseq-pipeline](skills/bioskills/riboseq-pipeline/) | `bioskills` | End-to-end Ribo-seq analysis from FASTQ to translation efficiency and ORF detection. Use when analyzing ribosome prof... |
| [bio-workflows-rnaseq-to-de](skills/bioskills/rnaseq-to-de/) | `bioskills` | End-to-end RNA-seq workflow from FASTQ files to differential expression results. Covers QC, quantification (Salmon or... |
| [bio-workflows-smrna-pipeline](skills/bioskills/smrna-pipeline/) | `bioskills` | End-to-end small RNA-seq analysis from FASTQ to differential miRNA expression. Use when analyzing miRNA, piRNA, or ot... |
| [bio-workflows-somatic-variant-pipeline](skills/bioskills/somatic-variant-pipeline/) | `bioskills` | End-to-end somatic variant calling from tumor-normal paired samples using Mutect2 or Strelka2. Covers preprocessing, ... |
| [bio-write-sequences](skills/bioskills/write-sequences/) | `bioskills` | Write biological sequences to files (FASTA, FASTQ, GenBank, EMBL) using Biopython Bio.SeqIO. Use when saving sequence... |
| [biopython](skills/kdense/biopython/) | `kdense` | Comprehensive molecular biology toolkit. Use for sequence manipulation, file parsing (FASTA/GenBank/PDB), phylogeneti... |
| [biopython-molecular-biology](skills/sciagent/biopython-molecular-biology/) | `sciagent` | Molecular biology toolkit: sequence manipulation, FASTA/GenBank/PDB I/O, NCBI Entrez, BLAST automation, pairwise/MSA ... |
| [biopython-sequence-analysis](skills/sciagent/biopython-sequence-analysis/) | `sciagent` | Biopython sequence analysis: parse FASTA/FASTQ/GenBank/GFF (SeqIO), NCBI Entrez (esearch/efetch/elink), remote/local ... |
| [bioservices](skills/kdense/bioservices/) | `kdense` | Unified Python interface to 40+ bioinformatics services. Use when querying multiple databases (UniProt, KEGG, ChEMBL,... |
| [bioservices-multi-database](skills/sciagent/bioservices-multi-database/) | `sciagent` | > |
| [bulk-rna-expression](skills/bioclaw_hub/bulk-rna-expression/) | `bioclaw_hub` | Python-first workflow for bulk RNA-seq expression intake, normalization, sample QC, and downstream-ready matrices. |
| [bulk-rna-seq-deseq2-analysis-with-omicverse](skills/openclaw/bulk-deseq2-analysis/) | `openclaw` | Walk Claude through PyDESeq2-based differential expression, including ID mapping, DE testing, fold-change thresholdin... |
| [bulk-rna-seq-differential-expression-with-omicverse](skills/openclaw/bulk-deg-analysis/) | `openclaw` | Guide Claude through omicverse's bulk RNA-seq DEG pipeline, from gene ID mapping and DESeq2 normalization to statisti... |
| [busco-status-interpretation](skills/sciagent/busco-status-interpretation/) | `sciagent` | Guide to interpreting BUSCO completeness statuses: why Duplicated BUSCOs count as complete, parsing output files, com... |
| [bwa-mem2-dna-aligner](skills/sciagent/bwa-mem2-dna-aligner/) | `sciagent` | Fast short-read DNA aligner for WGS/WES/ChIP-seq. 2× faster BWA-MEM successor; outputs SAM/BAM with read group header... |
| [causal-genomics](skills/bioclaw_hub/causal-genomics/) | `bioclaw_hub` | Workflow for fine-mapping, colocalization, mediation, pleiotropy analysis, and Mendelian randomization. |
| [cbioportal-database](skills/sciagent/cbioportal-database/) | `sciagent` | Cancer genomics (TCGA et al.) via cBioPortal REST API. Retrieve somatic mutations, CNAs, expression, clinical data (s... |
| [cell-detection](skills/clawbio/cell-detection/) | `clawbio` | Cell segmentation in fluorescence microscopy images. Supports Cellpose/cpsam (Cellpose 4.0) with additional backends |
| [chip-clonal-hematopoiesis-agent](skills/openclaw/chip-clonal-hematopoiesis-agent/) | `openclaw` | AI-powered clonal hematopoiesis of indeterminate potential (CHIP) detection, risk stratification, and cardiovascular/... |
| [claw-ancestry-pca](skills/clawbio/claw-ancestry-pca/) | `clawbio` | Ancestry decomposition PCA against the Simons Genome Diversity Project |
| [claw-metagenomics](skills/clawbio/claw-metagenomics/) | `clawbio` | Shotgun metagenomics profiling — taxonomy, resistome, and functional pathways |
| [clinical-trial-finder](skills/clawbio/clinical-trial-finder/) | `clawbio` | Find clinical trials for a gene, variant, or condition from ClinicalTrials.gov + EUCTR, with FHIR R4 output |
| [clinical-variant-reporter](skills/clawbio/clinical-variant-reporter/) | `clawbio` | Classify germline variants from VCF/BCF files according to the ACMG/AMP 2015 28-criteria evidence framework and |
| [clinpgx](skills/clawbio/clinpgx/) | `clawbio` | Query the ClinPGx API for pharmacogenomic gene-drug data, clinical annotations, CPIC guidelines, and FDA drug |
| [clinpgx-database](skills/sciagent/clinpgx-database/) | `sciagent` | Query the ClinPGx (formerly PharmGKB) REST API plus the CPIC PostgREST companion API for pharmacogenomic clinical ann... |
| [clinvar-database](skills/sciagent/clinvar-database/) | `sciagent` | Query NCBI ClinVar via E-utilities for variant clinical significance, pathogenicity, disease associations. Search by ... |
| [cnv-caller-agent](skills/openclaw/cnv-caller-agent/) | `openclaw` | AI-enhanced copy number variation calling and analysis from sequencing data for cancer genomics, constitutional CNV d... |
| [cnvkit-copy-number](skills/sciagent/cnvkit-copy-number/) | `sciagent` | Detect somatic CNVs from WES/WGS/targeted BAMs (CNVkit v0.9.x). Bin coverage in target/antitarget regions, normalize ... |
| [cobrapy](skills/kdense/cobrapy/) | `kdense` | Constraint-based metabolic modeling (COBRA). FBA, FVA, gene knockouts, flux sampling, SBML models, for systems biolog... |
| [cobrapy-metabolic-modeling](skills/sciagent/cobrapy-metabolic-modeling/) | `sciagent` | Constraint-based (COBRA) analysis of genome-scale metabolic models: FBA, FVA, knockouts, flux sampling, production en... |
| [comparative-genomics](skills/bioclaw_hub/comparative-genomics/) | `bioclaw_hub` | Workflow for orthology, synteny, ancestral reconstruction, and evolutionary comparison across genomes. |
| [copy-number](skills/bioclaw_hub/copy-number/) | `bioclaw_hub` | Workflow for copy-number estimation, segmentation, annotation, and visualization in sequencing-based assays. |
| [cosmic-database](skills/sciagent/cosmic-database/) | `sciagent` | Query COSMIC for cancer somatic mutations, gene census, mutational signatures, drug resistance variants. REST API v3.... |
| [database-lookup](skills/kdense/database-lookup/) | `kdense` | Search 78 public scientific, biomedical, materials science, and economic databases via REST APIs. Covers physics/astr... |
| [dbsnp-database](skills/sciagent/dbsnp-database/) | `sciagent` | Query NCBI dbSNP for SNP records by rsID, gene, or region via E-utilities and Variation Services REST API. Retrieve a... |
| [ddinter-database](skills/sciagent/ddinter-database/) | `sciagent` | Query DDInter drug-drug interactions via REST API (1.7M+ interactions, 2,400+ drugs). Search by drug name/ID for seve... |
| [deeptools](skills/kdense/deeptools/) | `kdense` | NGS analysis toolkit. BAM to bigWig conversion, QC (correlation, PCA, fingerprints), heatmaps/profiles (TSS, peaks), ... |
| [deeptools-ngs-analysis](skills/sciagent/deeptools-ngs-analysis/) | `sciagent` | NGS CLI for ChIP/RNA/ATAC-seq. BAM→bigWig with RPGC/CPM/RPKM, sample correlation/PCA, heatmaps/profiles around featur... |
| [degenerate-input-filtering](skills/sciagent/degenerate-input-filtering/) | `sciagent` | Filter degenerate, uninformative inputs before statistical tests: single-sequence alignments, empty files, constant f... |
| [depmap-crispr-essentiality](skills/sciagent/depmap-crispr-essentiality/) | `sciagent` | DepMap CRISPR gene effect (Chronos) analysis: sign convention for essentiality, per-gene NaN-safe Spearman correlatio... |
| [deseq2-differential-expression](skills/sciagent/deseq2-differential-expression/) | `sciagent` | Bulk RNA-seq DE with R/Bioconductor DESeq2. Negative binomial GLM, empirical Bayes shrinkage, Wald/LRT tests, multi-f... |
| [dnanexus-integration](skills/kdense/dnanexus-integration/) | `kdense` | DNAnexus cloud genomics platform. Build apps/applets, manage data (upload/download), dxpy Python SDK, run workflows, ... |
| [emdb-database](skills/sciagent/emdb-database/) | `sciagent` | Look up EMDB cryo-EM density maps and fitted atomic models via the entry REST API + EBI Search WS. Fetch entry metada... |
| [ena-database](skills/sciagent/ena-database/) | `sciagent` | ENA REST API for sequences, reads, assemblies, and annotations. Portal API search, Browser API retrieval (XML/FASTA/E... |
| [ensembl-database](skills/sciagent/ensembl-database/) | `sciagent` | Ensembl REST API for gene/transcript/variant annotations in 300+ species. Gene info by symbol/ID, sequence, cross-ref... |
| [epigenomics-methylgpt-agent](skills/openclaw/epigenomics-methylgpt-agent/) | `openclaw` | AI-powered DNA methylation analysis using MethylGPT foundation models for epigenomic profiling, differential methylat... |
| [epitranscriptomics](skills/bioclaw_hub/epitranscriptomics/) | `bioclaw_hub` | Workflow for RNA modification analysis such as m6A peak calling, differential modification, and transcript-level visu... |
| [equity-scorer](skills/clawbio/equity-scorer/) | `clawbio` | Compute HEIM diversity and equity metrics from VCF or ancestry data. Generates heterozygosity, FST, PCA plots, |
| [etetoolkit](skills/kdense/etetoolkit/) | `kdense` | Phylogenetic tree toolkit (ETE). Tree manipulation (Newick/NHX), evolutionary event detection, orthology/paralogy, NC... |
| [fastp-fastq-preprocessing](skills/sciagent/fastp-fastq-preprocessing/) | `sciagent` | All-in-one FASTQ QC and adapter trimming. Auto-detects Illumina adapters, filters low-quality reads, corrects paired-... |
| [featurecounts-rna-counting](skills/sciagent/featurecounts-rna-counting/) | `sciagent` | Counts RNA-seq reads overlapping GTF gene features. Takes sorted STAR BAMs plus GTF; outputs a per-gene tab-delimited... |
| [fine-mapping](skills/clawbio/fine-mapping/) | `clawbio` | Statistical fine-mapping of GWAS loci using SuSiE, SuSiE-inf, and Approximate Bayes Factors to identify credible |
| [flow-bio](skills/clawbio/flow-bio/) | `clawbio` | Flow.bio API bridge — authenticate, browse pipelines/samples/projects, search, upload data, launch pipeline executions, |
| [gatk-variant-calling](skills/sciagent/gatk-variant-calling/) | `sciagent` | GATK Best Practices for germline SNP/indel calling from WGS/WES BAMs. Per-sample HaplotypeCaller GVCFs, GenomicsDBImp... |
| [gene-database](skills/sciagent/gene-database/) | `sciagent` | NCBI Gene via E-utilities: curated records across 1M+ taxa. Official symbols, aliases, RefSeq IDs, summaries, coordin... |
| [gene-panel-design-agent](skills/openclaw/gene-panel-design-agent/) | `openclaw` | AI-powered design of targeted gene panels for clinical and research applications including cancer diagnostics, pharma... |
| [gene-regulatory-networks](skills/bioclaw_hub/gene-regulatory-networks/) | `bioclaw_hub` | Workflow for regulatory network inference, regulon scoring, perturbation-aware comparison, and network visualization. |
| [genome-assembly](skills/bioclaw_hub/genome-assembly/) | `bioclaw_hub` | Workflow for de novo assembly, scaffolding, polishing, contamination review, and assembly QC. |
| [genome-compare](skills/clawbio/genome-compare/) | `clawbio` | Compare your genome to George Church (PGP-1) and estimate ancestry composition via IBS and EM admixture |
| [genome-match](skills/clawbio/genome-match/) | `clawbio` | Score genetic compatibility across all male-female pairings in a Genomebook generation |
| [geopandas](skills/kdense/geopandas/) | `kdense` | Python library for working with geospatial vector data including shapefiles, GeoJSON, and GeoPackage files. Use when ... |
| [gnomad-database](skills/sciagent/gnomad-database/) | `sciagent` | gnomAD v4 population variant frequencies via GraphQL API. Allele counts and frequencies stratified by ancestry (AFR, ... |
| [gseapy-gene-enrichment](skills/sciagent/gseapy-gene-enrichment/) | `sciagent` | GSEA and over-representation analysis (ORA) for RNA-seq and proteomics. Wraps Enrichr for ORA against MSigDB, KEGG, G... |
| [gtars](skills/kdense/gtars/) | `kdense` | High-performance toolkit for genomic interval analysis in Rust with Python bindings. Use when working with genomic re... |
| [gtex-database](skills/openclaw/gtex-database/) | `openclaw` | Query GTEx (Genotype-Tissue Expression) portal for tissue-specific gene expression, eQTLs (expression quantitative tr... |
| [gwas-catalog-region-fetch](skills/clawbio/gwas-catalog-region-fetch/) | `clawbio` | \| |
| [gwas-database](skills/sciagent/gwas-database/) | `sciagent` | NHGRI-EBI GWAS Catalog REST API for SNP-trait associations from published GWAS. Query studies, associations, variants... |
| [gwas-lookup](skills/clawbio/gwas-lookup/) | `clawbio` | Federated variant lookup across 9 genomic databases — GWAS Catalog, Open Targets, PheWeb (UKB, FinnGen, BBJ), |
| [gwas-pipeline](skills/clawbio/gwas-pipeline/) | `clawbio` | End-to-end GWAS automation wrapping PLINK2 for genotype QC and REGENIE for two-step whole-genome regression association |
| [gwas-prs](skills/clawbio/gwas-prs/) | `clawbio` | Calculate polygenic risk scores from DTC genetic data using the PGS Catalog |
| [hemoglobinopathy-analysis-agent](skills/openclaw/hemoglobinopathy-analysis-agent/) | `openclaw` | AI-powered analysis of hemoglobin disorders including sickle cell disease, thalassemias, and variant hemoglobins usin... |
| [hi-c-3d-genomics](skills/bioclaw_hub/hi-c-3d-genomics/) | `bioclaw_hub` | Workflow for Hi-C and related 3D genomics analyses including compartments, loops, TADs, differential contacts, and vi... |
| [hmdb-database](skills/sciagent/hmdb-database/) | `sciagent` | Parse HMDB (Human Metabolome Database) local XML for metabolite info, chemical properties, biological context, diseas... |
| [homer-motif-analysis](skills/sciagent/homer-motif-analysis/) | `sciagent` | De novo and known TF motif enrichment in ChIP-seq/ATAC-seq peaks via HOMER. findMotifsGenome.pl finds over-represente... |
| [hrd-analysis-agent](skills/openclaw/hrd-analysis-agent/) | `openclaw` | AI-powered homologous recombination deficiency (HRD) analysis for PARP inhibitor response prediction using genomic sc... |
| [jaspar-database](skills/sciagent/jaspar-database/) | `sciagent` | JASPAR 2024 TF binding profiles via REST API and pyJASPAR. Retrieve PFMs/PWMs by TF name, JASPAR ID, species, or stru... |
| [jgi-lakehouse](skills/omics/jgi-lakehouse/) | `omics` | Queries JGI Lakehouse (Dremio) for genomics metadata from GOLD, IMG, Mycocosm, Phytozome. Downloads genome files from... |
| [kegg-database](skills/sciagent/kegg-database/) | `sciagent` | KEGG REST API (academic only). Pathways, genes, compounds, enzymes, diseases, drugs via 7 ops (info/list/find/get/con... |
| [long-read-genomics](skills/bioclaw_hub/long-read-genomics/) | `bioclaw_hub` | Workflow for nanopore or PacBio long-read QC, alignment, polishing, methylation-aware analysis, and structural varian... |
| [long-read-sequencing-agent](skills/openclaw/long-read-sequencing-agent/) | `openclaw` | AI-powered analysis of long-read sequencing data (PacBio, ONT) for structural variant detection, isoform discovery, e... |
| [macs3-peak-calling](skills/sciagent/macs3-peak-calling/) | `sciagent` | Poisson-model peak caller for ChIP-seq/ATAC-seq BAMs. MACS3 callpeak finds enriched regions (TF sites or histone mark... |
| [market-research-reports](skills/kdense/market-research-reports/) | `kdense` | Generate comprehensive market research reports (50+ pages) in the style of top consulting firms (McKinsey, BCG, Gartn... |
| [mendelian-randomisation](skills/clawbio/mendelian-randomisation/) | `clawbio` | Two-sample Mendelian Randomisation from GWAS summary statistics with IVW, MR-Egger, weighted median/mode, and |
| [metabolomics](skills/bioclaw_hub/metabolomics/) | `bioclaw_hub` | Workflow for untargeted or targeted metabolomics including preprocessing, normalization, annotation, statistics, and ... |
| [metagenomics](skills/bioclaw/metagenomics/) | `bioclaw` | Shotgun metagenomics workflow with host-depletion-aware QC, taxonomic profiling, functional profiling, AMR follow-up,... |
| [methylation-analysis](skills/bioclaw_hub/methylation-analysis/) | `bioclaw_hub` | Workflow for methylation alignment or calling, DMR analysis, methylation QC, and locus-level interpretation. |
| [microbiome-amplicon](skills/bioclaw_hub/microbiome-amplicon/) | `bioclaw_hub` | Workflow for amplicon microbiome analysis including denoising, taxonomy assignment, diversity analysis, and different... |
| [monarch-database](skills/sciagent/monarch-database/) | `sciagent` | Monarch Initiative knowledge graph REST API for disease-gene-phenotype associations and cross-species orthology. MOND... |
| [mouse-phenome-database](skills/sciagent/mouse-phenome-database/) | `sciagent` | Retrieve mouse phenotype data from the Jackson Laboratory Mouse Phenome Database (MPD) via its REST API. Browse 520+ ... |
| [multimodal-radpath-fusion-agent](skills/openclaw/multimodal-radpath-fusion-agent/) | `openclaw` | AI-powered multimodal diagnostic fusion integrating radiology imaging (CT/MRI/PET), digital pathology (WSI), genomics... |
| [multiqc-qc-reports](skills/sciagent/multiqc-qc-reports/) | `sciagent` | Aggregates QC from 150+ bioinformatics tools into one interactive HTML report. Scans FastQC, samtools, STAR, HISAT2, ... |
| [multiqc-reporter](skills/clawbio/multiqc-reporter/) | `clawbio` | Aggregates QC reports from any bioinformatics tool outputs (FastQC, fastp, STAR, Picard, samtools, etc.) into |
| [nan-safe-correlation](skills/sciagent/nan-safe-correlation/) | `sciagent` | Per-feature NaN-safe Spearman/Pearson correlation across many features (genes, proteins, variants) with missing value... |
| [nextflow-development](skills/openclaw/nextflow-development/) | `openclaw` | Run nf-core bioinformatics pipelines (rnaseq, sarek, atacseq) on sequencing data. Use when analyzing RNA-seq, WGS/WES... |
| [nfcore-rnaseq-wrapper](skills/clawbio/nfcore-rnaseq-wrapper/) | `clawbio` | Wrapper skill for running nf-core/rnaseq bulk RNA-seq preprocessing from FASTQ or BAM inputs with strict preflight, r... |
| [nutrigx-advisor](skills/clawbio/nutrigx-advisor/) | `clawbio` | Personalised nutrition report from consumer genetic data (23andMe, AncestryDNA, VCF) — interrogates nutritionally-rel... |
| [openalex-database](skills/sciagent/openalex-database/) | `sciagent` | Query OpenAlex REST API for 250M+ scholarly works, authors, institutions, journals, concepts. Search by keyword, auth... |
| [pacsomatic](skills/kdense/pacsomatic/) | `kdense` | Operator toolkit for nf-core/pacsomatic matched tumor-normal workflows from BAM inputs. Use this skill when the user ... |
| [pan-cancer-multiomics-agent](skills/openclaw/pan-cancer-multiomics-agent/) | `openclaw` | AI-powered pan-cancer analysis integrating genomic, transcriptomic, proteomic, and epigenomic data for cancer subtypi... |
| [parameter-optimization](skills/openclaw/parameter-optimization/) | `openclaw` | Explore and optimize simulation parameters via design of experiments (DOE), sensitivity analysis, and optimizer selec... |
| [pathogen-epi-genomics](skills/bioclaw_hub/pathogen-epi-genomics/) | `bioclaw_hub` | Workflow for outbreak-style pathogen genomics, surveillance, lineage assignment, and transmission-oriented comparativ... |
| [pharmacogenomics-agent](skills/openclaw/pharmacogenomics-agent/) | `openclaw` | AI-driven pharmacogenomic analysis for precision dosing and adverse event prediction using multi-omics data. |
| [pharmgx-reporter](skills/clawbio/pharmgx-reporter/) | `clawbio` | Pharmacogenomic report from DTC genetic data (23andMe/AncestryDNA) — 12 genes, 31 SNPs, 51 drugs |
| [phasing-imputation](skills/bioclaw_hub/phasing-imputation/) | `bioclaw_hub` | Workflow for haplotype phasing, genotype imputation, reference-panel matching, and imputation QC. |
| [phylogenetics](skills/kdense/phylogenetics/) | `kdense` | Build and analyze phylogenetic trees using MAFFT (multiple alignment), IQ-TREE 2 (maximum likelihood), and FastTree (... |
| [plannotate-plasmid-annotation](skills/sciagent/plannotate-plasmid-annotation/) | `sciagent` | Auto-annotate plasmids with features (promoters, terminators, resistance, origins, tags, fluorescent proteins) via BL... |
| [plink2-gwas-analysis](skills/sciagent/plink2-gwas-analysis/) | `sciagent` | GWAS and population genetics tool. Processes PLINK (.bed/.bim/.fam), VCF, and BGEN; runs QC (MAF, HWE, missingness), ... |
| [polars-bio](skills/kdense/polars-bio/) | `kdense` | High-performance genomic interval operations and bioinformatics file I/O on Polars DataFrames. Overlap, nearest, merg... |
| [popeve-variant-predictor-agent](skills/openclaw/popeve-variant-predictor-agent/) | `openclaw` | AI-powered genetic variant pathogenicity prediction using PopEVE deep learning model for population-aware disease var... |
| [precision-oncology-agent](skills/openclaw/precision-oncology-agent/) | `openclaw` | Fuse genomic variants, pathology findings, and clinical context to draft evidence-linked therapy options for tumor bo... |
| [pride-database](skills/sciagent/pride-database/) | `sciagent` | Search the PRIDE Archive v3 REST API for proteomics datasets: discover projects by keyword + faceted filters (organis... |
| [profile-report](skills/clawbio/profile-report/) | `clawbio` | Unified personal genomic profile report — reads a PatientProfile JSON and synthesizes all skill results into |
| [prokka-genome-annotation](skills/sciagent/prokka-genome-annotation/) | `sciagent` | Annotate prokaryotic genomes (bacteria, archaea, viruses) via Prokka's BLAST/HMM pipeline. Identifies CDS, rRNA, tRNA... |
| [pubmed-database](skills/sciagent/pubmed-database/) | `sciagent` | >- |
| [pydeseq2-differential-expression](skills/sciagent/pydeseq2-differential-expression/) | `sciagent` | Bulk RNA-seq DE with PyDESeq2: load counts, normalize, fit negative binomial models, Wald test (BH-FDR), LFC shrinkag... |
| [pyhealth](skills/kdense/pyhealth/) | `kdense` | Build clinical/healthcare deep-learning pipelines with PyHealth — loading EHR/signal/imaging datasets (MIMIC-III/IV, ... |
| [pymc-bayesian-modeling](skills/sciagent/pymc-bayesian-modeling/) | `sciagent` | Bayesian modeling with PyMC 5: priors, likelihood, NUTS/ADVI sampling, diagnostics (R-hat, ESS), LOO/WAIC comparison,... |
| [pysam](skills/kdense/pysam/) | `kdense` | Genomic file toolkit. Read/write SAM/BAM/CRAM alignments, VCF/BCF variants, FASTA/FASTQ sequences, extract regions, c... |
| [pysam-genomic-files](skills/sciagent/pysam-genomic-files/) | `sciagent` | Read/write SAM/BAM/CRAM, VCF/BCF, FASTA/FASTQ. Region queries, pileup, variant filtering, read groups. Python htslib ... |
| [query-clinvar](skills/bioclaw/query-clinvar/) | `bioclaw` | Query ClinVar for clinical variant significance. Use when user asks about variant pathogenicity, genetic variants, cl... |
| [query-ensembl](skills/bioclaw/query-ensembl/) | `bioclaw` | Query Ensembl for genomic data. Use when user asks about gene coordinates, genomic sequences, variants, gene structur... |
| [quickgo-database](skills/sciagent/quickgo-database/) | `sciagent` | Query EBI QuickGO REST API for GO terms and protein annotations. Fetch term metadata by ID, search by keyword, walk a... |
| [radiomics-pathomics-fusion-agent](skills/openclaw/radiomics-pathomics-fusion-agent/) | `openclaw` | AI-powered multimodal fusion of radiology (CT/MRI/PET) and pathology (H&E/IHC) imaging with clinical and genomic data... |
| [read-qc](skills/bioclaw_hub/read-qc/) | `bioclaw_hub` | Workflow for sequencing read QC, trimming, contamination screening, and pre-alignment cleanup. |
| [recombinator](skills/clawbio/recombinator/) | `clawbio` | Produce offspring genomes from parent pairs via meiotic recombination, mutation, and clinical evaluation |
| [regulomedb-database](skills/sciagent/regulomedb-database/) | `sciagent` | Query RegulomeDB v2 GET REST API to score variants for regulatory function and retrieve overlapping evidence (TF bind... |
| [rna-quantification](skills/bioclaw_hub/rna-quantification/) | `bioclaw_hub` | Workflow for gene and transcript quantification from RNA-seq reads using alignment-based or alignment-free tools. |
| [roary-pangenome](skills/sciagent/roary-pangenome/) | `sciagent` | Compute the bacterial pan-genome from Prokka/Bakta GFF3 annotations with Roary's CD-HIT + BLAST + MCL clustering pipe... |
| [salmon-rna-quantification](skills/sciagent/salmon-rna-quantification/) | `sciagent` | Ultra-fast RNA-seq transcript/gene quantification via quasi-mapping (no BAM). Builds a k-mer index from transcriptome... |
| [samtools-bam-processing](skills/sciagent/samtools-bam-processing/) | `sciagent` | CLI toolkit for SAM/BAM/CRAM: sort, index, convert, filter, QC alignments. Core commands: view, sort, index, flagstat... |
| [scikit-bio](skills/kdense/scikit-bio/) | `kdense` | Biological data toolkit. Sequence analysis, alignments, phylogenetic trees, diversity metrics (alpha/beta, UniFrac), ... |
| [sec-report](skills/bioclaw/sec-report/) | `bioclaw` | SEC (size-exclusion chromatography) analysis with peak detection, oligomer classification, and publication-quality PD... |
| [seq-wrangler](skills/clawbio/seq-wrangler/) | `clawbio` | NGS read QC, alignment, and BAM processing pipeline. Wraps FastQC, BWA/Bowtie2/Minimap2, SAMtools, and MultiQC for au... |
| [simo-multiomics-integration-agent](skills/openclaw/simo-multiomics-integration-agent/) | `openclaw` | AI-powered spatial integration of multi-omics datasets using probabilistic alignment for comprehensive tissue atlas c... |
| [simpleitk-image-registration](skills/sciagent/simpleitk-image-registration/) | `sciagent` | Register, segment, filter, resample 3D medical images (MRI, CT, microscopy) via SimpleITK Python; DICOM, NIfTI, multi... |
| [snpeff-variant-annotation](skills/sciagent/snpeff-variant-annotation/) | `sciagent` | Annotate and filter VCF variants with SnpEff and SnpSift. SnpEff predicts functional effects (HIGH/MODERATE/LOW/MODIF... |
| [soul2dna](skills/clawbio/soul2dna/) | `clawbio` | Compile SOUL.md character profiles into synthetic diploid genomes (.genome.json) via trait-to-allele mapping |
| [spatial-epigenomics-agent](skills/openclaw/spatial-epigenomics-agent/) | `openclaw` | AI-powered spatial epigenomics analysis combining chromatin accessibility, histone modifications, and DNA methylation... |
| [star-rna-seq-aligner](skills/sciagent/star-rna-seq-aligner/) | `sciagent` | Splice-aware RNA-seq aligner producing sorted BAM and splice junction tables. Builds genome index, runs two-pass alig... |
| [tcga-bulk-data-preprocessing-with-omicverse](skills/openclaw/tcga-preprocessing/) | `openclaw` | Guide Claude through ingesting TCGA sample sheets, expression archives, and clinical carts into omicverse, initialisi... |
| [tiledbvcf](skills/kdense/tiledbvcf/) | `kdense` | Efficient storage and retrieval of genomic variant data using TileDB. Scalable VCF/BCF ingestion, incremental sample ... |
| [tooluniverse-cancer-variant-interpretation](skills/openclaw/tooluniverse-cancer-variant-interpretation/) | `openclaw` | Provide comprehensive clinical interpretation of somatic mutations in cancer. Given a gene symbol + variant (e.g., EG... |
| [tooluniverse-chemical-compound-retrieval](skills/openclaw/tooluniverse-chemical-compound-retrieval/) | `openclaw` | Retrieves chemical compound information from PubChem and ChEMBL with disambiguation, cross-referencing, and quality a... |
| [tooluniverse-chemical-safety](skills/openclaw/tooluniverse-chemical-safety/) | `openclaw` | Comprehensive chemical safety and toxicology assessment integrating ADMET-AI predictions, CTD toxicogenomics, FDA lab... |
| [tooluniverse-clinical-guidelines](skills/openclaw/tooluniverse-clinical-guidelines/) | `openclaw` | Search and retrieve clinical practice guidelines across 12+ authoritative sources including NICE, WHO, ADA, AHA/ACC, ... |
| [tooluniverse-clinical-trial-matching](skills/openclaw/tooluniverse-clinical-trial-matching/) | `openclaw` | AI-driven patient-to-trial matching for precision medicine and oncology. Given a patient profile (disease, molecular ... |
| [tooluniverse-crispr-screen-analysis](skills/openclaw/tooluniverse-crispr-screen-analysis/) | `openclaw` | Comprehensive CRISPR screen analysis for functional genomics. Analyze pooled or arrayed CRISPR screens (knockout, act... |
| [tooluniverse-drug-research](skills/openclaw/tooluniverse-drug-research/) | `openclaw` | Generates comprehensive drug research reports with compound disambiguation, evidence grading, and mandatory completen... |
| [tooluniverse-drug-target-validation](skills/openclaw/tooluniverse-drug-target-validation/) | `openclaw` | Comprehensive computational validation of drug targets for early-stage drug discovery. Evaluates targets across 10 di... |
| [tooluniverse-epigenomics](skills/openclaw/tooluniverse-epigenomics/) | `openclaw` | Production-ready genomics and epigenomics data processing for BixBench questions. Handles methylation array analysis ... |
| [tooluniverse-expression-data-retrieval](skills/openclaw/tooluniverse-expression-data-retrieval/) | `openclaw` | Retrieves gene expression and omics datasets from ArrayExpress and BioStudies with gene disambiguation, experiment qu... |
| [tooluniverse-gwas-drug-discovery](skills/openclaw/tooluniverse-gwas-drug-discovery/) | `openclaw` | Transform GWAS signals into actionable drug targets and repurposing opportunities. Performs locus-to-gene mapping, ta... |
| [tooluniverse-gwas-finemapping](skills/openclaw/tooluniverse-gwas-finemapping/) | `openclaw` | Identify and prioritize causal variants at GWAS loci using statistical fine-mapping and locus-to-gene predictions. Co... |
| [tooluniverse-gwas-snp-interpretation](skills/openclaw/tooluniverse-gwas-snp-interpretation/) | `openclaw` | Interpret genetic variants (SNPs) from GWAS studies by aggregating evidence from multiple databases (GWAS Catalog, Op... |
| [tooluniverse-gwas-study-explorer](skills/openclaw/tooluniverse-gwas-study-explorer/) | `openclaw` | Compare GWAS studies, perform meta-analyses, and assess replication across cohorts. Integrates NHGRI-EBI GWAS Catalog... |
| [tooluniverse-gwas-trait-to-gene](skills/openclaw/tooluniverse-gwas-trait-to-gene/) | `openclaw` | Discover genes associated with diseases and traits using GWAS data from the GWAS Catalog (500,000+ associations) and ... |
| [tooluniverse-literature-deep-research](skills/openclaw/tooluniverse-literature-deep-research/) | `openclaw` | Conduct comprehensive literature research with target disambiguation, evidence grading, and structured theme extracti... |
| [tooluniverse-multi-omics-integration](skills/openclaw/tooluniverse-multi-omics-integration/) | `openclaw` | Integrate and analyze multiple omics datasets (transcriptomics, proteomics, epigenomics, genomics, metabolomics) for ... |
| [tooluniverse-multiomic-disease-characterization](skills/openclaw/tooluniverse-multiomic-disease-characterization/) | `openclaw` | Comprehensive multi-omics disease characterization integrating genomics, transcriptomics, proteomics, pathway, and th... |
| [tooluniverse-pharmacovigilance](skills/openclaw/tooluniverse-pharmacovigilance/) | `openclaw` | Analyze drug safety signals from FDA adverse event reports, label warnings, and pharmacogenomic data. Calculates disp... |
| [tooluniverse-phylogenetics](skills/openclaw/tooluniverse-phylogenetics/) | `openclaw` | Production-ready phylogenetics and sequence analysis skill for alignment processing, tree analysis, and evolutionary ... |
| [tooluniverse-polygenic-risk-score](skills/openclaw/tooluniverse-polygenic-risk-score/) | `openclaw` | Build and interpret polygenic risk scores (PRS) for complex diseases using GWAS summary statistics. Calculates geneti... |
| [tooluniverse-precision-medicine-stratification](skills/openclaw/tooluniverse-precision-medicine-stratification/) | `openclaw` | Comprehensive patient stratification for precision medicine by integrating genomic, clinical, and therapeutic data. G... |
| [tooluniverse-protein-structure-retrieval](skills/openclaw/tooluniverse-protein-structure-retrieval/) | `openclaw` | Retrieves protein structure data from RCSB PDB, PDBe, and AlphaFold with protein disambiguation, quality assessment, ... |
| [tooluniverse-rare-disease-diagnosis](skills/openclaw/tooluniverse-rare-disease-diagnosis/) | `openclaw` | Provide differential diagnosis for patients with suspected rare diseases based on phenotype and genetic data. Matches... |
| [tooluniverse-sequence-retrieval](skills/openclaw/tooluniverse-sequence-retrieval/) | `openclaw` | Retrieves biological sequences (DNA, RNA, protein) from NCBI and ENA with gene disambiguation, accession type handlin... |
| [tooluniverse-spatial-omics-analysis](skills/openclaw/tooluniverse-spatial-omics-analysis/) | `openclaw` | Computational analysis framework for spatial multi-omics data integration. Given spatially variable genes (SVGs), spa... |
| [tooluniverse-structural-variant-analysis](skills/openclaw/tooluniverse-structural-variant-analysis/) | `openclaw` | Comprehensive structural variant (SV) analysis skill for clinical genomics. Classifies SVs (deletions, duplications, ... |
| [tooluniverse-systems-biology](skills/openclaw/tooluniverse-systems-biology/) | `openclaw` | Comprehensive systems biology and pathway analysis using multiple pathway databases (Reactome, KEGG, WikiPathways, Pa... |
| [tooluniverse-target-research](skills/openclaw/tooluniverse-target-research/) | `openclaw` | Gather comprehensive biological target intelligence from 9 parallel research paths covering protein info, structure, ... |
| [tooluniverse-variant-analysis](skills/openclaw/tooluniverse-variant-analysis/) | `openclaw` | Production-ready VCF processing, variant annotation, mutation analysis, and structural variant (SV/CNV) interpretatio... |
| [tooluniverse-variant-interpretation](skills/openclaw/tooluniverse-variant-interpretation/) | `openclaw` | Systematic clinical variant interpretation from raw variant calls to ACMG-classified recommendations with structural ... |
| [torch-geometric](skills/kdense/torch-geometric/) | `kdense` | Guide for building Graph Neural Networks with PyTorch Geometric (PyG). Use this skill whenever the user asks about gr... |
| [torch-geometric-graph-neural-networks](skills/sciagent/torch-geometric-graph-neural-networks/) | `sciagent` | PyTorch Geometric (PyG) for graph neural networks: node/graph classification, link prediction with GCN, GAT, GraphSAG... |
| [ucsc-genome-browser](skills/sciagent/ucsc-genome-browser/) | `sciagent` | Query UCSC Genome Browser REST API for DNA sequences, tracks, gene models, and conservation across 100+ assemblies. R... |
| [uniprot-database](skills/openclaw/uniprot-database/) | `openclaw` | Direct REST API access to UniProt. Protein searches, FASTA retrieval, ID mapping, Swiss-Prot/TrEMBL. For Python workf... |
| [uniprot-protein-database](skills/sciagent/uniprot-protein-database/) | `sciagent` | Query UniProt REST API: search by gene/protein name, fetch FASTA, map IDs (Ensembl, PDB, RefSeq), access Swiss-Prot a... |
| [varcadd-pathogenicity](skills/openclaw/varcadd-pathogenicity/) | `openclaw` | Variant Scorer |
| [variant-annotation](skills/clawbio/variant-annotation/) | `clawbio` | Annotate VCF variants with Ensembl VEP REST, ClinVar significance, gnomAD/population frequency context, and prioritized |
| [variant-calling](skills/bioclaw_hub/variant-calling/) | `bioclaw_hub` | Workflow for small-variant and structural-variant discovery, filtering, annotation, and interpretation from sequencin... |
| [variant-interpretation-acmg](skills/openclaw/variant-interpretation-acmg/) | `openclaw` | Classifies genetic variants according to ACMG (American College of Medical Genetics) guidelines. |
| [vcf-annotator](skills/clawbio/vcf-annotator/) | `clawbio` | Annotate VCF variants with Ensembl VEP, ClinVar, and gnomAD. Ranks variants by impact (HIGH/MODERATE/LOW/MODIFIER) an... |
| [vcf-variant-filtering](skills/sciagent/vcf-variant-filtering/) | `sciagent` | Guide to quality filtering raw VCF files before computing summary stats (Ts/Tv ratio, variant counts, AF distribution... |
| [wes-clinical-report-en](skills/clawbio/wes-clinical-report-en/) | `clawbio` | Generates professional clinical PDF reports in English from WES (Whole Exome Sequencing) data with clinical interpret... |
| [wes-clinical-report-es](skills/clawbio/wes-clinical-report-es/) | `clawbio` | Generates professional clinical PDF reports in Spanish from WES (Whole Exome Sequencing) data with clinical interpret... |

</details>

<br/>

## 🔬 Proteomics 蛋白质组学
<br/>

<details>
<summary><b>Click to expand · 点击展开 (146 skills)</b></summary>

| Skill | Source 来源 | Description 描述 |
|-------|-------------|------------------|
| [adaptyv](skills/kdense/adaptyv/) | `kdense` | How to use the Adaptyv Bio Foundry API and Python SDK for protein experiment design, submission, and results retrieva... |
| [adhd-daily-planner](skills/openclaw/adhd-daily-planner/) | `openclaw` | Time-blind friendly planning, executive function support, and daily structure for ADHD brains. Specializes in realist... |
| [affinity-proteomics](skills/clawbio/affinity-proteomics/) | `clawbio` | Unified analysis pipeline for affinity-based proteomics platforms — Olink (PEA, NPX) and SomaLogic SomaScan (SOMAmer, |
| [alphafold](skills/adaptyv/alphafold/) | `adaptyv` | > |
| [alphafold-database](skills/openclaw/alphafold-database/) | `openclaw` | Access AlphaFold's 200M+ AI-predicted protein structures. Retrieve structures by UniProt ID, download PDB/mmCIF files... |
| [alphafold-database-access](skills/sciagent/alphafold-database-access/) | `sciagent` | > |
| [alphafold2-multimer](skills/bioclaw_hub/alphafold2-multimer/) | `bioclaw_hub` | > |
| [antibody-design-agent](skills/openclaw/antibody-design-agent/) | `openclaw` | An advanced agent for de novo antibody design and optimization using state-of-the-art protein language models (MAGE, ... |
| [benchling-integration](skills/kdense/benchling-integration/) | `kdense` | Benchling R&D platform integration. Access registry (DNA, proteins), inventory, ELN entries, workflows via API, build... |
| [bgpt-mcp](skills/clawbio/bgpt-mcp/) | `clawbio` | Search scientific papers via the BGPT MCP server and retrieve structured experimental data — methods, results, |
| [binder-design-campaign-manager](skills/bioclaw_hub/binder-design-campaign-manager/) | `bioclaw_hub` | > |
| [binder-design-tool-selection](skills/bioclaw_hub/binder-design-tool-selection/) | `bioclaw_hub` | > |
| [bindingdb-database](skills/openclaw/bindingdb-database/) | `openclaw` | Query BindingDB for measured drug-target binding affinities (Ki, Kd, IC50, EC50). Search by target (UniProt ID), comp... |
| [bio-atac-seq-nucleosome-positioning](skills/bioskills/nucleosome-positioning/) | `bioskills` | Map nucleosome center positions, occupancy, and fuzziness from ATAC-seq fragment-size patterns using NucleoATAC, ATAC... |
| [bio-data-visualization-sequence-logos](skills/bioskills/sequence-logos/) | `bioskills` | Build sequence logos from aligned DNA, RNA, or protein motifs using ggseqlogo (R), Logomaker (Python), or WebLogo wit... |
| [bio-foundation-housekeeping](skills/omics/bio-foundation-housekeeping/) | `omics` | Initialize a bioinformatics project scaffold with reproducible environments, schemas, and data cataloging. Use for ne... |
| [bio-generative-design](skills/bioskills/generative-design/) | `bioskills` | Designs novel molecules using REINVENT 4 (de novo, scaffold decoration, linker design, R-group, molecular optimizatio... |
| [bio-hi-c-analysis-hic-differential](skills/bioskills/hic-differential/) | `bioskills` | Compare Hi-C contact matrices between conditions to identify differential chromatin interactions. Compute log2 fold c... |
| [bio-hi-c-analysis-tad-detection](skills/bioskills/tad-detection/) | `bioskills` | Call topologically associating domains (TADs) from Hi-C data using insulation score, HiCExplorer, and other methods. ... |
| [bio-immunoinformatics-mhc-binding-prediction](skills/bioskills/mhc-binding-prediction/) | `bioskills` | Predict peptide-MHC class I and II binding affinity using MHCflurry and NetMHCpan neural network models. Identify pot... |
| [bio-immunoinformatics-neoantigen-prediction](skills/bioskills/neoantigen-prediction/) | `bioskills` | Identify tumor neoantigens from somatic mutations using pVACtools for personalized cancer immunotherapy. Predict muta... |
| [bio-interaction-databases](skills/bioskills/interaction-databases/) | `bioskills` | Query protein-protein and gene interaction databases (STRING, BioGRID, IntAct, SIGNOR, Reactome, HuRI, HuMAP, OmniPat... |
| [bio-ml-docking-rescoring](skills/bioskills/ml-docking-rescoring/) | `bioskills` | Performs ML-based protein-ligand pose prediction and scoring using DiffDock-L (diffusion-based), Boltz-1 / Boltz-2 (f... |
| [bio-molecular-io](skills/bioskills/molecular-io/) | `bioskills` | Reads, writes, and converts molecular file formats (SMILES, InChI, SDF V2000/V3000, MOL2, PDB, MMTF) using RDKit and ... |
| [bio-molecular-standardization](skills/bioskills/molecular-standardization/) | `bioskills` | Standardizes molecular structures using ChEMBL chembl_structure_pipeline and RDKit rdMolStandardize covering sanitiza... |
| [bio-pdb-geometric-analysis](skills/bioskills/geometric-analysis/) | `bioskills` | Perform geometric calculations on protein structures using Biopython Bio.PDB. Use when measuring distances, angles, a... |
| [bio-pdb-structure-io](skills/bioskills/structure-io/) | `bioskills` | Parse and write protein structure files using Biopython Bio.PDB. Use when reading PDB, mmCIF, and MMTF files, downloa... |
| [bio-pdb-structure-modification](skills/bioskills/structure-modification/) | `bioskills` | Modify protein structures using Biopython Bio.PDB. Use when transforming coordinates, removing atoms or residues, add... |
| [bio-pdb-structure-navigation](skills/bioskills/structure-navigation/) | `bioskills` | Navigate protein structure hierarchy using Biopython Bio.PDB SMCRA model. Use when accessing models, chains, residues... |
| [bio-phylo-tree-manipulation](skills/bioskills/tree-manipulation/) | `bioskills` | Modify phylogenetic tree structure using Biopython Bio.Phylo. Use when rooting trees with outgroups, midpoint, or MAD... |
| [bio-population-genetics-population-structure](skills/bioskills/population-structure/) | `bioskills` | Analyze population structure using PCA and admixture analysis with PLINK and ADMIXTURE. Identify population clusters,... |
| [bio-pose-validation](skills/bioskills/pose-validation/) | `bioskills` | Validates docked / generated protein-ligand poses using PoseBusters physical-validity tests, strain energy quantifica... |
| [bio-prefect-dask-nextflow](skills/omics/bio-prefect-dask-nextflow/) | `omics` | Design and scaffold bioinformatics pipelines using Prefect+Dask for local/distributed execution or Nextflow for HPC s... |
| [bio-primer-design-primer-validation](skills/bioskills/primer-validation/) | `bioskills` | Validate PCR primers for specificity, dimers, hairpins, and secondary structures using primer3-py thermodynamic calcu... |
| [bio-protac-degraders](skills/bioskills/protac-degraders/) | `bioskills` | Designs PROTACs, molecular glues, and bivalent degraders with explicit handling of E3 ligase choice (VHL, CRBN, IAP, ... |
| [bio-proteomics-data-import](skills/bioskills/data-import/) | `bioskills` | Load and parse mass spectrometry data formats including mzML, mzXML, and quantification tool outputs like MaxQuant pr... |
| [bio-proteomics-dia-analysis](skills/bioskills/dia-analysis/) | `bioskills` | Data-independent acquisition (DIA) proteomics analysis with DIA-NN and other tools. Use when analyzing DIA mass spect... |
| [bio-proteomics-peptide-identification](skills/bioskills/peptide-identification/) | `bioskills` | Peptide-spectrum matching and protein identification from MS/MS data. Use when identifying peptides from tandem mass ... |
| [bio-proteomics-protein-inference](skills/bioskills/protein-inference/) | `bioskills` | Protein grouping and inference from peptide identifications. Use when resolving protein ambiguity from shared peptide... |
| [bio-proteomics-quantification](skills/bioskills/quantification/) | `bioskills` | Protein quantification from mass spectrometry data including label-free (LFQ, intensity-based), isobaric labeling (TM... |
| [bio-proteomics-spectral-libraries](skills/bioskills/spectral-libraries/) | `bioskills` | Build, manage, and search spectral libraries for proteomics. Use when creating or working with spectral libraries for... |
| [bio-qsar-modeling](skills/bioskills/qsar-modeling/) | `bioskills` | Builds QSAR / QSPR models using chemprop D-MPNN, MolFormer, Uni-Mol, ChemBERTa, random forest baselines, and Gaussian... |
| [bio-rna-structure-ncrna-search](skills/bioskills/ncrna-search/) | `bioskills` | Searches for non-coding RNA homologs and classifies RNA families using Infernal covariance model searches against the... |
| [bio-rna-structure-structure-probing](skills/bioskills/structure-probing/) | `bioskills` | Analyzes experimental RNA structure probing data from SHAPE-MaP and DMS-MaPseq experiments using ShapeMapper2. Conver... |
| [bio-scaffold-analysis](skills/bioskills/scaffold-analysis/) | `bioskills` | Analyzes chemical libraries by scaffold using Bemis-Murcko scaffolds, generic frameworks, cyclic skeletons, matched m... |
| [bio-sequence-similarity](skills/openclaw/bio-sequence-similarity/) | `openclaw` | Find homologous sequences using iterative BLAST (PSI-BLAST), profile HMMs (HMMER), and reciprocal best hit analysis. ... |
| [bio-similarity-searching](skills/bioskills/similarity-searching/) | `bioskills` | Performs molecular similarity searching using Tanimoto, Tversky, Dice, and cosine coefficients on bit/count fingerpri... |
| [bio-structural-biology-alphafold-predictions](skills/bioskills/alphafold-predictions/) | `bioskills` | Access and analyze AlphaFold protein structure predictions. Use when predicted structures are needed for proteins wit... |
| [bio-structural-biology-modern-structure-prediction](skills/bioskills/modern-structure-prediction/) | `bioskills` | Predict protein structures using modern ML models including AlphaFold3, ESMFold, Chai-1, and Boltz-1. Use when predic... |
| [bio-structure-annotation](skills/omics/bio-structure-annotation/) | `omics` | Structure prediction and structure-based annotation. |
| [bio-substructure-search](skills/bioskills/substructure-search/) | `bioskills` | Searches molecular libraries for substructure matches using SMARTS patterns with explicit handling of recursive SMART... |
| [bio-transcription-translation](skills/bioskills/transcription-translation/) | `bioskills` | Transcribe DNA to RNA and translate to protein using Biopython. Use when converting between DNA, RNA, and protein seq... |
| [bio-virtual-screening](skills/bioskills/virtual-screening/) | `bioskills` | Performs structure-based virtual screening using AutoDock Vina, SMINA, GNINA (CNN scoring), and DiffDock-L hybrid wor... |
| [blast-search](skills/bioclaw/blast-search/) | `bioclaw` | Run BLAST sequence similarity searches. Use when the user asks to BLAST a sequence, find similar sequences, identify ... |
| [boltz-structure-prediction](skills/bioclaw_hub/boltz-structure-prediction/) | `bioclaw_hub` | > |
| [chai1-structure-prediction](skills/bioclaw_hub/chai1-structure-prediction/) | `bioclaw_hub` | > |
| [chembl-database](skills/openclaw/chembl-database/) | `openclaw` | Query ChEMBL's bioactive molecules and drug discovery data. Search compounds by structure/properties, retrieve bioact... |
| [clinical-decision-support-documents](skills/sciagent/clinical-decision-support-documents/) | `sciagent` | Guidelines for clinical decision support (CDS) documents: biomarker-stratified cohort analyses and GRADE-graded treat... |
| [clinical-nlp-extractor](skills/openclaw/clinical-nlp-extractor/) | `openclaw` | Extracts medical entities (Diseases, Medications, Procedures) from unstructured clinical text using regex and simple ... |
| [clinical-note-summarization](skills/openclaw/clinical-note-summarization/) | `openclaw` | Structure raw clinical notes into SOAP-format summaries with explicit contradictions, missing data, and ICD-linked as... |
| [cryoem-ai-drug-design-agent](skills/openclaw/cryoem-ai-drug-design-agent/) | `openclaw` | AI-powered integration of cryo-EM structural data with generative AI and molecular dynamics for structure-based drug ... |
| [dailymed-database](skills/sciagent/dailymed-database/) | `sciagent` | Query FDA drug labels (DailyMed) via REST API. Search structured product labels (SPLs) by name, NDC, set ID, or RxCUI... |
| [diffdock](skills/kdense/diffdock/) | `kdense` | Diffusion-based molecular docking. Predict protein-ligand binding poses from PDB/SMILES, confidence scores, virtual s... |
| [doc-coauthoring](skills/openclaw/doc-coauthoring/) | `openclaw` | Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation,... |
| [drugbank-database](skills/openclaw/drugbank-database/) | `openclaw` | Access and analyze comprehensive drug information from the DrugBank database including drug properties, interactions,... |
| [end-to-end-protein-design-workflow](skills/bioclaw_hub/end-to-end-protein-design-workflow/) | `bioclaw_hub` | > |
| [esm-protein-language-model](skills/sciagent/esm-protein-language-model/) | `sciagent` | Protein language models (ESM3, ESM C) for sequence generation, structure prediction, inverse folding, and embeddings.... |
| [esm2-sequence-scoring](skills/bioclaw_hub/esm2-sequence-scoring/) | `bioclaw_hub` | > |
| [exploratory-data-analysis](skills/kdense/exploratory-data-analysis/) | `kdense` | Perform comprehensive exploratory data analysis on scientific data files across 200+ file formats. This skill should ... |
| [fda-database](skills/sciagent/fda-database/) | `sciagent` | Query openFDA REST API for adverse events (FAERS), labeling, product info, recalls, enforcement. Search by drug name,... |
| [finishing-a-development-branch](skills/openclaw/finishing-a-development-branch/) | `openclaw` | Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides comple... |
| [foldseek](skills/adaptyv/foldseek/) | `adaptyv` | > |
| [gget](skills/kdense/gget/) | `kdense` | Fast CLI/Python queries to 20+ bioinformatics databases. Use for quick lookups: gene info, BLAST searches, AlphaFold ... |
| [glycoengineering](skills/kdense/glycoengineering/) | `kdense` | Analyze and engineer protein glycosylation. Scan sequences for N-glycosylation sequons (N-X-S/T), predict O-glycosyla... |
| [gtopdb-database](skills/sciagent/gtopdb-database/) | `sciagent` | Query IUPHAR/BPS Guide to Pharmacology (GtoPdb) for receptor-ligand interactions, target/ligand metadata, families, a... |
| [histolab](skills/kdense/histolab/) | `kdense` | Lightweight WSI tile extraction and preprocessing. Use for basic slide processing tissue detection, tile extraction, ... |
| [hypothesis-generation](skills/kdense/hypothesis-generation/) | `kdense` | Structured hypothesis formulation from observations. Use when you have experimental observations or data and need to ... |
| [imaging-mass-cytometry](skills/bioclaw_hub/imaging-mass-cytometry/) | `bioclaw_hub` | Workflow for multiplexed imaging or IMC segmentation, phenotyping, and spatial summarization. |
| [interpro-database](skills/sciagent/interpro-database/) | `sciagent` | Query InterPro REST API for protein domain architecture, family classification, and member-DB integration. Search ent... |
| [lit-synthesizer](skills/clawbio/lit-synthesizer/) | `clawbio` | Search PubMed and bioRxiv for bioinformatics literature, synthesise results into a structured report, and build |
| [matchms](skills/kdense/matchms/) | `kdense` | Spectral similarity and compound identification for metabolomics. Use for comparing mass spectra, computing similarit... |
| [matchms-spectral-matching](skills/sciagent/matchms-spectral-matching/) | `sciagent` | MS spectral matching and metabolite ID with matchms. Import spectra (mzML, MGF, MSP, JSON), filter/normalize peaks, s... |
| [maxquant-proteomics](skills/sciagent/maxquant-proteomics/) | `sciagent` | MaxQuant + Perseus proteomics pipeline: run MaxQuant for LFQ and SILAC; parse proteinGroups.txt in Python; filter con... |
| [metabolomics-workbench-database](skills/sciagent/metabolomics-workbench-database/) | `sciagent` | Query Metabolomics Workbench REST API (4,200+ NIH studies) for metabolite ID, study discovery, RefMet standardization... |
| [modal](skills/kdense/modal/) | `kdense` | Cloud computing platform for running Python on GPUs and serverless infrastructure. Use when deploying AI/ML models, r... |
| [molecular-dynamics](skills/kdense/molecular-dynamics/) | `kdense` | Run and analyze molecular dynamics simulations with OpenMM and MDAnalysis. Set up protein/small molecule systems, def... |
| [molecular-glue-discovery-agent](skills/openclaw/molecular-glue-discovery-agent/) | `openclaw` | AI-powered molecular glue discovery for targeted protein degradation, enabling neo-substrate recruitment and undrugga... |
| [multi-omics-integration](skills/bioclaw_hub/multi-omics-integration/) | `bioclaw_hub` | Workflow for integrating matched or partially matched omics layers into shared latent structure and cross-modal inter... |
| [myeloma-mrd-agent](skills/openclaw/myeloma-mrd-agent/) | `openclaw` | AI-powered minimal residual disease (MRD) analysis for multiple myeloma using next-generation flow cytometry, NGS, an... |
| [networkx](skills/kdense/networkx/) | `kdense` | Comprehensive toolkit for creating, analyzing, and visualizing complex networks and graphs in Python. Use when workin... |
| [nnunet-segmentation](skills/sciagent/nnunet-segmentation/) | `sciagent` | Medical image segmentation with nnU-Net's self-configuring framework — auto-selects architecture, preprocessing, trai... |
| [pdb](skills/adaptyv/pdb/) | `adaptyv` | > |
| [pdb-database](skills/sciagent/pdb-database/) | `sciagent` | Query RCSB PDB (200K+ structures) via the public REST + GraphQL APIs with plain `requests` (no SDK). Search by text, ... |
| [peer-review](skills/kdense/peer-review/) | `kdense` | Structured manuscript/grant review with checklist-based evaluation. Use when writing formal peer reviews with specifi... |
| [peer-review-methodology](skills/sciagent/peer-review-methodology/) | `sciagent` | Structured peer review of manuscripts and grants. 7-stage evaluation: initial assessment, section review, statistical... |
| [polars-dovmed](skills/omics/polars-dovmed/) | `omics` | Search the PMC Open Access literature with polars-dovmed. Author structured JSON queries directly, then use the hoste... |
| [proposal-review](skills/omics/proposal-review/) | `omics` | Structured, decision-ready review framework for AI/ML, computational biology, and bioscience proposals. Use when eval... |
| [protac-design-agent](skills/openclaw/protac-design-agent/) | `openclaw` | AI-powered PROTAC (Proteolysis Targeting Chimera) design for targeted protein degradation, integrating ternary comple... |
| [protein-design-qc](skills/bioclaw_hub/protein-design-qc/) | `bioclaw_hub` | > |
| [protein-design-workflow](skills/adaptyv/protein-design-workflow/) | `adaptyv` | > |
| [protein-interaction-network-analysis](skills/openclaw/tooluniverse-protein-interactions/) | `openclaw` | Analyze protein-protein interaction networks using STRING, BioGRID, and SASBDB databases. Maps protein identifiers, r... |
| [protein-qc](skills/adaptyv/protein-qc/) | `adaptyv` | > |
| [protein-structure-prediction](skills/openclaw/protein-structure-prediction/) | `openclaw` | Predicts 3D protein structures from amino acid sequences using ESMFold or AlphaFold3 (mock). |
| [proteina-complexa](skills/bioclaw_hub/proteina-complexa/) | `bioclaw_hub` | > |
| [proteinmpnn](skills/adaptyv/proteinmpnn/) | `adaptyv` | > |
| [proteomics](skills/bioclaw/proteomics/) | `bioclaw` | Mass spectrometry proteomics QC, quantification, comparative analysis, and export for DDA, DIA, and protein-level res... |
| [proteomics-clock](skills/clawbio/proteomics-clock/) | `clawbio` | Compute organ-specific biological age from Olink proteomic data using Goeminne et al. (2025) elastic net aging |
| [pubchem-compound-search](skills/sciagent/pubchem-compound-search/) | `sciagent` | Query PubChem (110M+ compounds) directly via the PUG-REST/JSON API with plain `requests` — no SDK install required. S... |
| [pubchem-database](skills/openclaw/pubchem-database/) | `openclaw` | Query PubChem via PUG-REST API/PubChemPy (110M+ compounds). Search by name/CID/SMILES, retrieve properties, similarit... |
| [pubmed-summariser](skills/clawbio/pubmed-summariser/) | `clawbio` | Search PubMed for a gene name or disease term and generate a structured research briefing of the top recent English-l... |
| [pymatgen](skills/kdense/pymatgen/) | `kdense` | Materials science toolkit. Crystal structures (CIF, POSCAR), phase diagrams, band structure, DOS, Materials Project i... |
| [pyopenms](skills/kdense/pyopenms/) | `kdense` | Complete mass spectrometry analysis platform. Use for proteomics workflows feature detection, peptide identification,... |
| [pyopenms-mass-spectrometry](skills/sciagent/pyopenms-mass-spectrometry/) | `sciagent` | MS data processing with PyOpenMS for LC-MS/MS proteomics and metabolomics — mzML/mzXML I/O, signal processing (smooth... |
| [pytdc](skills/kdense/pytdc/) | `kdense` | Therapeutics Data Commons. AI-ready drug discovery datasets (ADME, toxicity, DTI), benchmarks, scaffold splits, molec... |
| [query-alphafold](skills/bioclaw/query-alphafold/) | `bioclaw` | Query AlphaFold protein structure predictions. Use when user asks about protein structure, 3D structure, protein fold... |
| [query-interpro](skills/bioclaw/query-interpro/) | `bioclaw` | Query InterPro for protein domains and families. Use when user asks about protein domains, functional sites, protein ... |
| [query-pdb](skills/bioclaw/query-pdb/) | `bioclaw` | Query RCSB PDB for experimental protein structures. Use when user asks about crystal structures, X-ray, cryo-EM, NMR ... |
| [query-stringdb](skills/bioclaw/query-stringdb/) | `bioclaw` | Query STRING for protein-protein interactions. Use when user asks about protein interactions, interaction networks, b... |
| [query-uniprot](skills/bioclaw/query-uniprot/) | `bioclaw` | Query UniProt protein database. Use when user asks about protein sequences, functions, annotations, domains, or prote... |
| [rdkit](skills/kdense/rdkit/) | `kdense` | Cheminformatics toolkit for fine-grained molecular control. SMILES/SDF parsing, descriptors (MW, LogP, TPSA), fingerp... |
| [rdkit-cheminformatics](skills/sciagent/rdkit-cheminformatics/) | `sciagent` | Cheminformatics toolkit for molecular analysis and virtual screening: SMILES/SDF parsing, descriptors (MW, LogP, TPSA... |
| [rowan](skills/kdense/rowan/) | `kdense` | Rowan is a cloud-native molecular modeling and medicinal-chemistry workflow platform with a Python API. Use for pKa a... |
| [sar-analysis](skills/sciagent/sar-analysis/) | `sciagent` | Structure-activity relationship (SAR) analysis guide for drug discovery including molecular descriptor analysis, scaf... |
| [scholar-evaluation](skills/kdense/scholar-evaluation/) | `kdense` | Systematically evaluate scholarly work using the ScholarEval framework, providing structured assessment across resear... |
| [scientific-slides](skills/kdense/scientific-slides/) | `kdense` | Build slide decks and presentations for research talks. Use this for making PowerPoint slides, conference presentatio... |
| [scientific-writing](skills/kdense/scientific-writing/) | `kdense` | Core skill for the deep research and writing tool. Write scientific manuscripts in full paragraphs (never bullet poin... |
| [sequence-analysis](skills/bioclaw/sequence-analysis/) | `bioclaw` | Analyze DNA/RNA/protein sequences. Use when the user provides a sequence and asks for analysis, translation, GC conte... |
| [skill-builder](skills/clawbio/skill-builder/) | `clawbio` | Scaffold a new ClawBio skill from a spec file (JSON/YAML) or interactively — generates SKILL.md, Python skeleton, tes... |
| [spr-bli-binding-characterization](skills/bioclaw_hub/spr-bli-binding-characterization/) | `bioclaw_hub` | > |
| [string-database](skills/openclaw/string-database/) | `openclaw` | Query STRING API for protein-protein interactions (59M proteins, 20B interactions). Network analysis, GO/KEGG enrichm... |
| [string-database-ppi](skills/sciagent/string-database-ppi/) | `sciagent` | Query STRING REST API for PPIs (59M proteins, 20B interactions, 5000+ species). Retrieve networks, run GO/KEGG enrich... |
| [string-protein-interaction-analysis-with-omicverse](skills/openclaw/bulk-stringdb-ppi/) | `openclaw` | Help Claude query STRING for protein interactions, build PPI graphs with pyPPI, and render styled network figures for... |
| [struct-predictor](skills/clawbio/struct-predictor/) | `clawbio` | Protein structure prediction with Boltz-2. Accepts YAML inputs (single protein or multi-chain complex), runs |
| [structural-biology](skills/bioclaw/structural-biology/) | `bioclaw` | Structure retrieval, confidence-aware AlphaFold DB usage, coordinate download, PAE and pLDDT interpretation, and stru... |
| [tcr-pmhc-prediction-agent](skills/openclaw/tcr-pmhc-prediction-agent/) | `openclaw` | AI-powered TCR-peptide-MHC interaction prediction using AlphaFold3 and deep learning for therapeutic TCR discovery, n... |
| [time-resolved-cryoem-agent](skills/openclaw/time-resolved-cryoem-agent/) | `openclaw` | AI-powered time-resolved cryo-EM analysis for capturing protein dynamics, drug-binding kinetics, and conformational t... |
| [tooluniverse-binder-discovery](skills/openclaw/tooluniverse-binder-discovery/) | `openclaw` | Discover novel small molecule binders for protein targets using structure-based and ligand-based approaches. Creates ... |
| [tooluniverse-infectious-disease](skills/openclaw/tooluniverse-infectious-disease/) | `openclaw` | Rapid pathogen characterization and drug repurposing analysis for infectious disease outbreaks. Identifies pathogen t... |
| [tooluniverse-protein-therapeutic-design](skills/openclaw/tooluniverse-protein-therapeutic-design/) | `openclaw` | Design novel protein therapeutics (binders, enzymes, scaffolds) using AI-guided de novo design. Uses RFdiffusion for ... |
| [torchdrug](skills/kdense/torchdrug/) | `kdense` | PyTorch-native graph neural networks for molecules and proteins. Use when building custom GNN architectures for drug ... |
| [tpd-ternary-complex-agent](skills/openclaw/tpd-ternary-complex-agent/) | `openclaw` | AI-powered ternary complex prediction for targeted protein degradation, modeling POI-degrader-E3 ligase assemblies to... |
| [umap-learn](skills/kdense/umap-learn/) | `kdense` | UMAP dimensionality reduction. Fast nonlinear manifold learning for 2D/3D visualization, clustering preprocessing (HD... |
| [unichem-database](skills/sciagent/unichem-database/) | `sciagent` | Cross-reference compound IDs across 20+ databases (ChEMBL, DrugBank, PubChem, ChEBI, PDB, SureChEMBL, HMDB, DrugCentr... |
| [viennarna-structure-prediction](skills/sciagent/viennarna-structure-prediction/) | `sciagent` | Predict RNA secondary structure, MFE folding, base-pair probabilities, RNA-RNA interactions via ViennaRNA Python bind... |
| [what-if-oracle](skills/kdense/what-if-oracle/) | `kdense` | Run structured What-If scenario analysis with multi-branch possibility exploration. Use this skill when the user asks... |
| [wikipedia-search](skills/openclaw/wikipedia-search/) | `openclaw` | Search and fetch structured content from Wikipedia using the MediaWiki API for reliable, encyclopedic information |

</details>

<br/>

## 🔵 Single-Cell 单细胞
<br/>

<details>
<summary><b>Click to expand · 点击展开 (117 skills)</b></summary>

| Skill | Source 来源 | Description 描述 |
|-------|-------------|------------------|
| [anndata](skills/kdense/anndata/) | `kdense` | Data structure for annotated matrices in single-cell analysis. Use when working with .h5ad files or integrating with ... |
| [anndata-data-structure](skills/sciagent/anndata-data-structure/) | `sciagent` | Annotated matrices for single-cell genomics. Stores X with obs/var metadata, layers, embeddings (obsm/varm), graphs (... |
| [arboreto](skills/kdense/arboreto/) | `kdense` | Infer gene regulatory networks (GRNs) from gene expression data using scalable algorithms (GRNBoost2, GENIE3). Use wh... |
| [arboreto-grn-inference](skills/sciagent/arboreto-grn-inference/) | `sciagent` | GRN inference from expression via GRNBoost2 (gradient boosting) or GENIE3 (Random Forest). Load matrix, filter by TFs... |
| [bio-atac-seq-co-accessibility](skills/bioskills/co-accessibility/) | `bioskills` | Infer cis-regulatory connections (peak-to-peak co-accessibility) from scATAC-seq using Cicero, ArchR getCoAccessibili... |
| [bio-atac-seq-deep-learning-atac](skills/bioskills/deep-learning-atac/) | `bioskills` | Sequence-based deep learning for ATAC-seq using chromBPNet, BPNet, scBasset, or EnFormer. Use when correcting Tn5 bia... |
| [bio-atac-seq-enhancer-gene-linking](skills/bioskills/enhancer-gene-linking/) | `bioskills` | Predict enhancer-gene regulatory connections from ATAC-seq using ABC, ENCODE-rE2G, HiChIP, or Cicero. Use when linkin... |
| [bio-atac-seq-motif-deviation](skills/bioskills/motif-deviation/) | `bioskills` | Analyze TF motif accessibility variability across samples or single cells using chromVAR. Use when identifying TF mot... |
| [bio-atac-seq-single-cell-atac](skills/bioskills/single-cell-atac/) | `bioskills` | Process and analyze single-cell ATAC-seq data with Signac, ArchR, SnapATAC2, or Cell Ranger ATAC. Use when handling 1... |
| [bio-causal-genomics-heritability-partitioning](skills/bioskills/heritability-partitioning/) | `bioskills` | Estimate SNP heritability and partition it across functional annotations, cell types, and loci from GWAS summary stat... |
| [bio-chipseq-chromatin-state-segmentation](skills/bioskills/chromatin-state-segmentation/) | `bioskills` | Segments the genome into chromatin states from combinatorial histone modification and chromatin factor ChIP-seq data.... |
| [bio-chipseq-peak-annotation](skills/bioskills/peak-annotation/) | `bioskills` | Annotates ChIP-seq peaks to genomic features, nearest genes, ENCODE candidate cis-regulatory elements (cCREs), and re... |
| [bio-clip-seq-stamp-antibody-free](skills/bioskills/stamp-antibody-free/) | `bioskills` | Profiles RNA-binding protein targets without antibody or UV crosslinking using STAMP (APOBEC1-RBP fusion, C-to-U edit... |
| [bio-crispr-screens-combinatorial-screens](skills/bioskills/combinatorial-screens/) | `bioskills` | Designs and analyzes combinatorial CRISPR screens covering paired-Cas9 (Big Papi, Najm 2018), enhanced AsCas12a multi... |
| [bio-crispr-screens-perturb-seq-analysis](skills/bioskills/perturb-seq-analysis/) | `bioskills` | Analyzes single-cell pooled CRISPR screens (Perturb-seq, CROP-seq, Perturb-CITE-seq, ECCITE-seq, multiome) where each... |
| [bio-data-visualization-dimensionality-reduction-plots](skills/bioskills/dimensionality-reduction-plots/) | `bioskills` | Produce and interpret PCA, t-SNE, UMAP, and PHATE plots for high-dimensional omics data with rigor about which method... |
| [bio-data-visualization-matplotlib-fundamentals](skills/bioskills/matplotlib-fundamentals/) | `bioskills` | Build publication-quality figures with matplotlib using the object-oriented Figure/Axes API, constrained_layout, rcPa... |
| [bio-expression-matrix-normalization](skills/bioskills/normalization/) | `bioskills` | Normalize and transform RNA-seq count matrices for differential expression, visualization, and clustering. Covers bet... |
| [bio-expression-matrix-sparse-handling](skills/bioskills/sparse-handling/) | `bioskills` | Work with sparse matrices for memory-efficient storage of count data. Use when dealing with single-cell data or large... |
| [bio-flow-cytometry-clustering-phenotyping](skills/bioskills/clustering-phenotyping/) | `bioskills` | Unsupervised clustering and cell type identification for flow/mass cytometry. Covers FlowSOM, Phenograph, and CATALYS... |
| [bio-gene-regulatory-networks-coexpression-networks](skills/bioskills/coexpression-networks/) | `bioskills` | Build weighted gene co-expression networks to identify modules of co-regulated genes and relate them to phenotypes us... |
| [bio-gene-regulatory-networks-multiomics-grn](skills/bioskills/multiomics-grn/) | `bioskills` | Build enhancer-driven gene regulatory networks by integrating single-cell RNA-seq and ATAC-seq data using SCENIC+ to ... |
| [bio-gene-regulatory-networks-scenic-regulons](skills/bioskills/scenic-regulons/) | `bioskills` | Infer gene regulatory networks and identify transcription factor regulons from single-cell RNA-seq data using pySCENI... |
| [bio-imaging-mass-cytometry-cell-segmentation](skills/bioskills/cell-segmentation/) | `bioskills` | Cell segmentation from multiplexed tissue images. Covers deep learning (Cellpose, Mesmer) and classical approaches fo... |
| [bio-imaging-mass-cytometry-interactive-annotation](skills/bioskills/interactive-annotation/) | `bioskills` | Interactive cell type annotation for IMC data. Covers napari-based annotation, marker-guided labeling, training data ... |
| [bio-imaging-mass-cytometry-phenotyping](skills/bioskills/phenotyping/) | `bioskills` | Cell type assignment from marker expression in IMC data. Covers manual gating, clustering, and automated classificati... |
| [bio-imaging-mass-cytometry-spatial-analysis](skills/bioskills/spatial-analysis/) | `bioskills` | Spatial analysis of cell neighborhoods and interactions in IMC data. Covers neighbor graphs, spatial statistics, and ... |
| [bio-machine-learning-atlas-mapping](skills/bioskills/atlas-mapping/) | `bioskills` | Maps query single-cell data to reference atlases using scArches transfer learning with scVI and scANVI models. Transf... |
| [bio-methylation-dmr-detection](skills/bioskills/dmr-detection/) | `bioskills` | Differentially methylated region (DMR) detection using methylKit tiles, bsseq BSmooth, and DMRcate. Use when identify... |
| [bio-read-qc-umi-processing](skills/bioskills/umi-processing/) | `bioskills` | Extract, process, and deduplicate reads using Unique Molecular Identifiers (UMIs) with umi_tools. Use when library pr... |
| [bio-single-cell-batch-integration](skills/bioskills/batch-integration/) | `bioskills` | Integrate multiple scRNA-seq samples/batches using Harmony, scVI, Seurat anchors, and fastMNN. Remove technical varia... |
| [bio-single-cell-cell-annotation](skills/bioskills/cell-annotation/) | `bioskills` | Automated cell type annotation using reference-based methods including CellTypist, scPred, SingleR, and Azimuth for c... |
| [bio-single-cell-cell-communication](skills/bioskills/cell-communication/) | `bioskills` | Infer cell-cell communication networks from scRNA-seq data using CellChat, NicheNet, and LIANA for ligand-receptor in... |
| [bio-single-cell-clustering](skills/bioskills/clustering/) | `bioskills` | Dimensionality reduction and clustering for single-cell RNA-seq using Seurat (R) and Scanpy (Python). Use for running... |
| [bio-single-cell-data-io](skills/bioskills/data-io/) | `bioskills` | Read, write, and create single-cell data objects using Seurat (R) and Scanpy (Python). Use for loading 10X Genomics d... |
| [bio-single-cell-doublet-detection](skills/bioskills/doublet-detection/) | `bioskills` | Detect and remove doublets (multiple cells captured in one droplet) from single-cell RNA-seq data. Uses Scrublet (Pyt... |
| [bio-single-cell-lineage-tracing](skills/bioskills/lineage-tracing/) | `bioskills` | Reconstruct cell lineage trees from CRISPR barcode tracing or mitochondrial mutations. Use when studying clonal dynam... |
| [bio-single-cell-markers-annotation](skills/bioskills/markers-annotation/) | `bioskills` | Find marker genes and annotate cell types in single-cell RNA-seq using Seurat (R) and Scanpy (Python). Use for differ... |
| [bio-single-cell-metabolite-communication](skills/bioskills/metabolite-communication/) | `bioskills` | Analyze metabolite-mediated cell-cell communication using MeboCost for metabolic signaling inference between cell typ... |
| [bio-single-cell-multimodal-integration](skills/bioskills/multimodal-integration/) | `bioskills` | Analyze multi-modal single-cell data (CITE-seq, Multiome, spatial). Use when working with data that measures multiple... |
| [bio-single-cell-perturb-seq](skills/bioskills/perturb-seq/) | `bioskills` | Analyze Perturb-seq and CROP-seq CRISPR screening data integrated with scRNA-seq. Use when identifying gene function ... |
| [bio-single-cell-preprocessing](skills/bioskills/preprocessing/) | `bioskills` | Quality control, filtering, and normalization for single-cell RNA-seq using Seurat (R) and Scanpy (Python). Use for c... |
| [bio-single-cell-scatac-analysis](skills/bioskills/scatac-analysis/) | `bioskills` | Single-cell ATAC-seq analysis with Signac (R/Seurat) and ArchR. Process 10X Genomics scATAC data, perform QC, dimensi... |
| [bio-single-cell-splicing](skills/bioskills/single-cell-splicing/) | `bioskills` | Analyzes alternative splicing at single-cell resolution. The first decision is library chemistry — 10X 3' is fundamen... |
| [bio-single-cell-trajectory-inference](skills/bioskills/trajectory-inference/) | `bioskills` | Infer developmental trajectories and pseudotime from single-cell RNA-seq data using Monocle3, Slingshot, and scVelo f... |
| [bio-spatial-transcriptomics-spatial-deconvolution](skills/bioskills/spatial-deconvolution/) | `bioskills` | Estimate cell type composition in spatial transcriptomics spots using reference-based deconvolution. Use cell2locatio... |
| [bio-spatial-transcriptomics-spatial-domains](skills/bioskills/spatial-domains/) | `bioskills` | Identify spatial domains and tissue regions in spatial transcriptomics data using Squidpy and Scanpy. Cluster spots c... |
| [bio-spatial-transcriptomics-spatial-visualization](skills/bioskills/spatial-visualization/) | `bioskills` | Visualize spatial transcriptomics data using Squidpy and Scanpy. Create tissue plots with gene expression, clusters, ... |
| [bio-sra-data](skills/bioskills/sra-data/) | `bioskills` | Download raw sequencing reads from NCBI SRA using sra-tools (prefetch, fasterq-dump, vdb-validate) or the ENA mirror.... |
| [bio-systems-biology-context-specific-models](skills/bioskills/context-specific-models/) | `bioskills` | Build tissue and condition-specific metabolic models using GIMME, iMAT, and INIT algorithms with expression data cons... |
| [bio-tcr-bcr-analysis-scirpy-analysis](skills/bioskills/scirpy-analysis/) | `bioskills` | Analyze single-cell TCR and BCR data integrated with gene expression using scirpy. Use when working with 10x Genomics... |
| [bio-temporal-genomics-trajectory-modeling](skills/bioskills/trajectory-modeling/) | `bioskills` | Models continuous temporal trajectories from bulk or time-resolved omics data using generalized additive models (mgcv... |
| [bio-workflows-crispr-screen-pipeline](skills/bioskills/crispr-screen-pipeline/) | `bioskills` | End-to-end pooled and single-cell CRISPR screen analysis from FASTQ to hit genes. Orchestrates library design QC, gui... |
| [bio-workflows-grn-pipeline](skills/bioskills/grn-pipeline/) | `bioskills` | End-to-end gene regulatory network inference pipeline from processed single-cell data to regulon discovery and pertur... |
| [bio-workflows-multiome-pipeline](skills/bioskills/multiome-pipeline/) | `bioskills` | End-to-end multiome workflow for joint scRNA-seq + scATAC-seq analysis. Covers data loading, separate modality proces... |
| [bio-workflows-scrnaseq-pipeline](skills/bioskills/scrnaseq-pipeline/) | `bioskills` | End-to-end single-cell RNA-seq workflow from 10X Genomics data to annotated cell types. Covers QC, normalization, clu... |
| [bio-workflows-tcr-pipeline](skills/bioskills/tcr-pipeline/) | `bioskills` | End-to-end TCR/BCR repertoire analysis from FASTQ to clonotype diversity metrics. Use when analyzing immune repertoir... |
| [bioinformatics-singlecell](skills/openclaw/bioinformatics-singlecell/) | `openclaw` | Advanced single-cell multi-omics analysis including scRNA-seq, scCITE-seq, scATAC-seq, and TARGET-seq. Use when analy... |
| [biomni](skills/openclaw/biomni/) | `openclaw` | Autonomous biomedical AI agent framework for executing complex research tasks across genomics, drug discovery, molecu... |
| [bioskills](skills/bioskills/bioskills-installer/) | `bioskills` | Installs 425 bioinformatics skills covering sequence analysis, RNA-seq, single-cell, variant calling, metagenomics, s... |
| [bulk-rna-seq-deconvolution-with-bulk2single](skills/openclaw/bulk-to-single-deconvolution/) | `openclaw` | Turn bulk RNA-seq cohorts into synthetic single-cell datasets using omicverse's Bulk2Single workflow for cell fractio... |
| [bulktrajblend-trajectory-interpolation](skills/openclaw/bulk-trajblend-interpolation/) | `openclaw` | Extend scRNA-seq developmental trajectories with BulkTrajBlend by generating intermediate cells from bulk RNA-seq, tr... |
| [cell-annotation](skills/bioclaw/cell-annotation/) | `bioclaw` | Automated and marker-guided single-cell cell type annotation using CellTypist, marker review, reference transfer, and... |
| [cell-communication](skills/bioclaw_hub/cell-communication/) | `bioclaw_hub` | Workflow for ligand-receptor communication inference in single-cell or spatial data with sender-receiver summaries an... |
| [cellchat-cell-communication](skills/sciagent/cellchat-cell-communication/) | `sciagent` | Infer and visualize intercellular communication from scRNA-seq with CellChat (R). Build CellChat from Seurat/counts →... |
| [celltypist-cell-annotation](skills/sciagent/celltypist-cell-annotation/) | `sciagent` | Automated scRNA-seq cell type annotation via pre-trained logistic regression. 45+ models: immune, gut, lung, brain, f... |
| [cellxgene-census](skills/kdense/cellxgene-census/) | `kdense` | Query the CELLxGENE Census (61M+ cells) programmatically. Use when you need expression data across tissues, diseases,... |
| [compbioagent-explorer](skills/openclaw/compbioagent-explorer/) | `openclaw` | scRNA-seq Explorer |
| [data-visualization-biomedical](skills/openclaw/data-visualization-biomedical/) | `openclaw` | Publication-quality visualizations for biomedical and genomics data. Use when creating volcano plots, heatmaps, UMAP ... |
| [deep-visual-proteomics-agent](skills/openclaw/deep-visual-proteomics-agent/) | `openclaw` | AI-driven integration of cellular imaging, laser microdissection, and ultra-sensitive mass spectrometry for spatially... |
| [diff-visualizer](skills/clawbio/diff-visualizer/) | `clawbio` | Rich downstream visualisation and reporting for bulk RNA-seq differential expression and scRNA marker/contrast |
| [encode-database](skills/sciagent/encode-database/) | `sciagent` | ENCODE Portal REST API for regulatory genomics: TF ChIP-seq, ATAC-seq/DNase-seq peaks, histone marks, and RNA-seq acr... |
| [fastq-analysis-pipeline](skills/openclaw/fastq-analysis/) | `openclaw` | Guide through omicverse's alignment module for SRA downloading, FASTQ quality control, STAR alignment, gene quantific... |
| [geniml](skills/kdense/geniml/) | `kdense` | This skill should be used when working with genomic interval data (BED files) for machine learning tasks. Use for tra... |
| [geo-database](skills/sciagent/geo-database/) | `sciagent` | NCBI GEO access via GEOparse and E-utilities. Search by keyword/organism/platform, download GSE series matrices, pars... |
| [gget-genomic-databases](skills/sciagent/gget-genomic-databases/) | `sciagent` | Unified CLI/Python interface to 20+ genomic databases. Gene lookups (Ensembl search/info/seq), BLAST/BLAT, AlphaFold,... |
| [harmony-batch-correction](skills/sciagent/harmony-batch-correction/) | `sciagent` | Harmony batch correction for scRNA-seq and other omics. Removes batch effects from PCA embeddings while preserving bi... |
| [hugging-science](skills/kdense/hugging-science/) | `kdense` | Use when the user is doing AI/ML work in a scientific domain — biology, chemistry, physics, astronomy, climate, genom... |
| [lamindb](skills/kdense/lamindb/) | `kdense` | This skill should be used when working with LaminDB, an open-source data framework for biology that makes data querya... |
| [lamindb-data-management](skills/sciagent/lamindb-data-management/) | `sciagent` | Open-source FAIR biology data framework. Version artifacts (AnnData, DataFrame, Zarr), track lineage, validate via on... |
| [lobster-bioinformatics](skills/openclaw/lobster-bioinformatics/) | `openclaw` | Run bioinformatics analyses using Lobster AI - single-cell RNA-seq, bulk RNA-seq, literature mining, dataset discover... |
| [mofaplus-multi-omics](skills/sciagent/mofaplus-multi-omics/) | `sciagent` | Multi-Omics Factor Analysis v2 (MOFA+) with mofapy2. Jointly decompose omics layers (scRNA, ATAC, proteomics, methyla... |
| [multiome-scatac](skills/bioclaw_hub/multiome-scatac/) | `bioclaw_hub` | Workflow for paired or integrated single-cell RNA and ATAC analysis with multimodal latent spaces and regulatory inte... |
| [muon-multiomics-singlecell](skills/sciagent/muon-multiomics-singlecell/) | `sciagent` | Multi-modal single-cell analysis with muon/MuData. Joint RNA+ATAC (10x Multiome), CITE-seq (RNA+protein), other multi... |
| [nfcore-scrnaseq-wrapper](skills/clawbio/nfcore-scrnaseq-wrapper/) | `clawbio` | Wrapper skill for running nf-core/scrnaseq upstream single-cell RNA-seq preprocessing from FASTQ with strict prefligh... |
| [ngs-analysis](skills/openclaw/ngs-analysis/) | `openclaw` | Next-generation sequencing data analysis pipelines including bulk RNA-seq, scRNA-seq preprocessing, variant calling, ... |
| [popv-cell-annotation](skills/sciagent/popv-cell-annotation/) | `sciagent` | Consensus cell type annotation: runs 10+ algorithms (KNN-Harmony/BBKNN/Scanorama/scVI, CellTypist, ONCLASS, Random Fo... |
| [remap-database](skills/sciagent/remap-database/) | `sciagent` | Query ReMap 2022 TF ChIP-seq peak database via REST API and BED downloads. Retrieve TF peaks overlapping a region (ch... |
| [rna-velocity-agent](skills/openclaw/rna-velocity-agent/) | `openclaw` | AI-powered RNA velocity analysis for predicting cellular state transitions, differentiation trajectories, and dynamic... |
| [scanpy](skills/kdense/scanpy/) | `kdense` | Standard single-cell RNA-seq analysis pipeline. Use for QC, normalization, dimensionality reduction (PCA/UMAP/t-SNE),... |
| [scanpy-scrna-seq](skills/sciagent/scanpy-scrna-seq/) | `sciagent` | scRNA-seq with Scanpy: QC, normalization, HVG selection, PCA, neighborhood graph, UMAP/t-SNE, Leiden clustering, mark... |
| [scfoundation-model-agent](skills/openclaw/scfoundation-model-agent/) | `openclaw` | Unified agent for leveraging single-cell foundation models (scGPT, scBERT, Geneformer, scFoundation) for cross-specie... |
| [scrna-embedding](skills/clawbio/scrna-embedding/) | `clawbio` | Local scVI/scANVI-based single-cell latent embedding and batch-aware integration from raw-count .h5ad or 10x |
| [scrna-orchestrator](skills/clawbio/scrna-orchestrator/) | `clawbio` | Local Scanpy pipeline for single-cell RNA-seq QC, optional doublet detection, clustering, marker discovery, optional |
| [scrna-preprocessing-clustering](skills/bioclaw/scrna-preprocessing-clustering/) | `bioclaw` | Standard scRNA-seq preprocessing and clustering with Scanpy. Use for QC, normalization, HVG selection, PCA, neighbor ... |
| [scrna-qc](skills/openclaw/scrna-qc/) | `openclaw` | Execute the MAD-based single-cell RNA-seq QC workflow (scripts + Python API) to filter low-quality cells and emit rep... |
| [scvelo](skills/kdense/scvelo/) | `kdense` | RNA velocity analysis with scVelo. Estimate cell state transitions from unspliced/spliced mRNA dynamics, infer trajec... |
| [scvi-tools](skills/kdense/scvi-tools/) | `kdense` | Deep generative models for single-cell omics. Use when you need probabilistic batch correction (scVI), transfer learn... |
| [scvi-tools-single-cell](skills/sciagent/scvi-tools-single-cell/) | `sciagent` | Deep generative models for single-cell omics: probabilistic batch correction (scVI), semi-supervised annotation (scAN... |
| [single-cell-annotation](skills/sciagent/single-cell-annotation/) | `sciagent` | Best practices for single-cell RNA-seq cell type annotation including marker-based, reference-based, and automated cl... |
| [single-cell-annotation-guide](skills/sciagent/single-cell-annotation-guide/) | `sciagent` | Decision framework for manual marker-based, automated (CellTypist), and reference-based (popV) cell type annotation i... |
| [single-cell-annotation-skills-with-omicverse](skills/openclaw/single-annotation/) | `openclaw` | Guide Claude through SCSA, MetaTiME, CellVote, CellMatch, GPTAnno, and weighted KNN transfer workflows for annotating... |
| [single-cell-atlas](skills/zamushwani/single-cell-atlas/) | `zamushwani` | — |
| [single-cell-cellphonedb-communication-mapping](skills/openclaw/single-cellphone-db/) | `openclaw` | Run omicverse's CellPhoneDB v5 wrapper on annotated single-cell data to infer ligand-receptor networks and produce Ce... |
| [single-cell-clustering-and-batch-correction-with-omicverse](skills/openclaw/single-clustering/) | `openclaw` | Guide Claude through omicverse's single-cell clustering workflow, covering preprocessing, QC, multimethod clustering,... |
| [single-cell-downstream-analysis](skills/openclaw/single-downstream-analysis/) | `openclaw` | Checklist-style reference for OmicVerse downstream tutorials covering AUCell scoring, metacell DEG, and related exports. |
| [single-cell-multi-omics-integration](skills/openclaw/single-multiomics/) | `openclaw` | Quick-reference sheet for OmicVerse tutorials spanning MOFA, GLUE pairing, SIMBA integration, TOSICA transfer, and St... |
| [single-cell-preprocessing-with-omicverse](skills/openclaw/single-preprocessing/) | `openclaw` | Walk through omicverse's single-cell preprocessing tutorials to QC PBMC3k data, normalise counts, detect HVGs, and ru... |
| [single-cell-rna-qc](skills/openclaw/single-cell-rna-qc/) | `openclaw` | Performs quality control on single-cell RNA-seq data (.h5ad or .h5 files) using scverse best practices with MAD-based... |
| [single2spatial-spatial-mapping](skills/openclaw/single-to-spatial-mapping/) | `openclaw` | Map scRNA-seq atlases onto spatial transcriptomics slides using omicverse's Single2Spatial workflow for deep-forest t... |
| [spatial-transcriptomics](skills/bioclaw_hub/spatial-transcriptomics/) | `bioclaw_hub` | Workflow for spatial transcriptomics preprocessing, domain detection, deconvolution, neighborhood analysis, and publi... |
| [tme-immune-profiling-agent](skills/openclaw/tme-immune-profiling-agent/) | `openclaw` | Comprehensive AI-powered tumor microenvironment immune profiling integrating bulk deconvolution, single-cell analysis... |
| [tooluniverse-immune-repertoire-analysis](skills/openclaw/tooluniverse-immune-repertoire-analysis/) | `openclaw` | Comprehensive immune repertoire analysis for T-cell and B-cell receptor sequencing data. Analyze TCR/BCR repertoires ... |
| [tooluniverse-single-cell](skills/openclaw/tooluniverse-single-cell/) | `openclaw` | Production-ready single-cell and expression matrix analysis using scanpy, anndata, and scipy. Performs scRNA-seq QC, ... |
| [tooluniverse-spatial-transcriptomics](skills/openclaw/tooluniverse-spatial-transcriptomics/) | `openclaw` | Analyze spatial transcriptomics data to map gene expression in tissue architecture. Supports 10x Visium, MERFISH, seq... |
| [trajectory-lineage](skills/bioclaw_hub/trajectory-lineage/) | `bioclaw_hub` | Workflow for pseudotime, lineage branching, and state-transition analysis in single-cell data. |
| [universal-single-cell-annotator](skills/openclaw/universal-single-cell-annotator/) | `openclaw` | Annotate scRNA-seq |

</details>

<br/>

## 🧫 Biology & AI 生物学与AI
<br/>

<details>
<summary><b>Click to expand · 点击展开 (117 skills)</b></summary>

| Skill | Source 来源 | Description 描述 |
|-------|-------------|------------------|
| [aav-vector-design-agent](skills/openclaw/aav-vector-design-agent/) | `openclaw` | AI-powered adeno-associated virus (AAV) vector design for gene therapy including capsid engineering, promoter selecti... |
| [agent-browser](skills/omics/agent-browser/) | `omics` | Browser automation via agent-browser CLI for web navigation, form filling, screenshots, scraping, login flows, and UI... |
| [ai-analyzer](skills/openclaw/ai-analyzer/) | `openclaw` | AI驱动的综合健康分析系统，整合多维度健康数据、识别异常模式、预测健康风险、提供个性化建议。支持智能问答和AI健康报告生成。 |
| [ai-scientist-evaluator](skills/omics/ai-scientist-evaluator/) | `omics` | >- |
| [bayesian-optimizer](skills/openclaw/bayesian-optimizer/) | `openclaw` | Bayesian Optimize |
| [bindcraft](skills/adaptyv/bindcraft/) | `adaptyv` | > |
| [binder-design](skills/adaptyv/binder-design/) | `adaptyv` | > |
| [binding-characterization](skills/adaptyv/binding-characterization/) | `adaptyv` | > |
| [bio-flow-cytometry-bead-normalization](skills/bioskills/bead-normalization/) | `bioskills` | Bead-based normalization for CyTOF and high-parameter flow cytometry. Covers EQ bead normalization, signal drift corr... |
| [bio-flow-cytometry-fcs-handling](skills/bioskills/fcs-handling/) | `bioskills` | Read and manipulate Flow Cytometry Standard (FCS) files. Covers loading data, accessing parameters, and basic data ex... |
| [bio-gene-calling](skills/omics/bio-gene-calling/) | `omics` | Call genes and annotate basic features for prokaryotes, viruses, and eukaryotes. |
| [bio-human-feedback](skills/bioclaw/bio-human-feedback/) | `bioclaw` | — |
| [bio-immunoinformatics-tcr-epitope-binding](skills/bioskills/tcr-epitope-binding/) | `bioskills` | Predict TCR-epitope specificity using ERGO-II and deep learning models for T-cell receptor antigen recognition. Match... |
| [bio-innovation-check](skills/bioclaw/bio-innovation-check/) | `bioclaw` | — |
| [bio-logic](skills/omics/bio-logic/) | `omics` | Evaluate scientific rigor, methods, biases, and evidence quality for claims, papers, and study designs. |
| [bio-manuscript-refine](skills/bioclaw/bio-manuscript-refine/) | `bioclaw` | — |
| [bio-manuscript-text](skills/bioclaw/bio-manuscript-text/) | `bioclaw` | — |
| [bio-metric-system](skills/bioclaw/bio-metric-system/) | `bioclaw` | — |
| [bio-molecular-descriptors](skills/bioskills/molecular-descriptors/) | `bioskills` | Calculates molecular fingerprints (ECFP/Morgan, FCFP, MACCS, RDKit, AtomPair, TopologicalTorsion, Avalon, MAP4, MHFP6... |
| [bio-phylo-divergence-dating](skills/bioskills/divergence-dating/) | `bioskills` | Estimate divergence times using molecular clock models with BEAST2, MCMCTree, and TreePL. Use when dating speciation ... |
| [bio-phylo-species-trees](skills/bioskills/species-trees/) | `bioskills` | Estimate species trees using coalescent methods including ASTRAL-III, wASTRAL, ASTRAL-Pro, SVDQuartets, and BPP. Use ... |
| [bio-phylo-tree-io](skills/bioskills/tree-io/) | `bioskills` | Read, write, and convert phylogenetic tree files using Biopython Bio.Phylo. Use when parsing Newick, Nexus, PhyloXML,... |
| [bio-ppt-generate](skills/bioclaw/bio-ppt-generate/) | `bioclaw` | — |
| [bio-reporting-quarto-reports](skills/bioskills/quarto-reports/) | `bioskills` | Build reproducible scientific documents, presentations, and websites with Quarto supporting R, Python, Julia, and Obs... |
| [bio-ribo-seq-ribosome-stalling](skills/bioskills/ribosome-stalling/) | `bioskills` | Detect ribosome pausing and stalling sites from Ribo-seq data at codon resolution. Use when studying translational re... |
| [bio-stats-ml-reporting](skills/omics/bio-stats-ml-reporting/) | `omics` | Aggregate results, train ML models, and produce reports with validated references. |
| [bio-task-system](skills/bioclaw/bio-task-system/) | `bioclaw` | — |
| [biokernel](skills/openclaw/biokernel/) | `openclaw` | Biomedical OS Core & MCP Server |
| [biologist-analyst](skills/openclaw/biologist-analyst/) | `openclaw` | \| |
| [biomcp-server](skills/openclaw/biomcp-server/) | `openclaw` | MCP bio bridge |
| [boltz](skills/adaptyv/boltz/) | `adaptyv` | > |
| [boltzgen](skills/adaptyv/boltzgen/) | `adaptyv` | > |
| [brainstorming](skills/openclaw/brainstorming/) | `openclaw` | You MUST use this before any creative work - creating features, building components, adding functionality, or modifyi... |
| [campaign-manager](skills/adaptyv/campaign-manager/) | `adaptyv` | > |
| [cellagent-annotation](skills/openclaw/cellagent-annotation/) | `openclaw` | Cell tagger |
| [cellpose-cell-segmentation](skills/sciagent/cellpose-cell-segmentation/) | `sciagent` | DL cell/nucleus segmentation for fluorescence and brightfield microscopy. Pre-trained models (cyto3, nuclei, tissuene... |
| [chai](skills/adaptyv/chai/) | `adaptyv` | > |
| [chemist-analyst](skills/openclaw/chemist-analyst/) | `openclaw` | \| |
| [cirq](skills/kdense/cirq/) | `kdense` | Google quantum computing framework. Use when targeting Google Quantum AI hardware, designing noise-aware circuits, or... |
| [computational-pathology-agent](skills/openclaw/computational-pathology-agent/) | `openclaw` | Analyze Whole Slide Images (WSI) for digital pathology, including tissue segmentation and feature extraction. |
| [crisis-response-protocol](skills/openclaw/crisis-response-protocol/) | `openclaw` | Handle mental health crisis situations in AI coaching safely. Use when implementing crisis detection, safety protocol... |
| [crispr-guide-design](skills/openclaw/crispr-guide-design/) | `openclaw` | Guide foundry |
| [crispr-screen-triage](skills/clawbio/crispr-screen-triage/) | `clawbio` | Deterministic CRISPR screen hit ranking from local guide-level count tables |
| [data-transform](skills/openclaw/data-transform/) | `openclaw` | Transform, clean, reshape, and preprocess data using pandas and numpy. Works with ANY LLM provider (GPT, Gemini, Clau... |
| [dhdna-profiler](skills/kdense/dhdna-profiler/) | `kdense` | Extract cognitive patterns and thinking fingerprints from any text. Use this skill when the user wants to analyze how... |
| [differentiation-schemes](skills/openclaw/differentiation-schemes/) | `openclaw` | Select and apply numerical differentiation schemes for PDE/ODE discretization. Use when choosing finite difference/vo... |
| [dispatching-parallel-agents](skills/openclaw/dispatching-parallel-agents/) | `openclaw` | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies |
| [dnasp](skills/clawbio/dnasp/) | `clawbio` | >- |
| [docx](skills/kdense/docx/) | `kdense` | Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers in... |
| [emergency-card](skills/openclaw/emergency-card/) | `openclaw` | 生成紧急情况下快速访问的医疗信息摘要卡片。当用户需要旅行、就诊准备、紧急情况或询问"紧急信息"、"医疗卡片"、"急救信息"时使用此技能。提取关键信息（过敏、用药、急症、植入物），支持多格式输出（JSON、文本、二维码），用于急救或快速就医。 |
| [epidemiologist-analyst](skills/openclaw/epidemiologist-analyst/) | `openclaw` | \| |
| [esm](skills/adaptyv/esm/) | `adaptyv` | > |
| [executing-plans](skills/openclaw/executing-plans/) | `openclaw` | Use when you have a written implementation plan to execute in a separate session with review checkpoints |
| [family-health-analyzer](skills/openclaw/family-health-analyzer/) | `openclaw` | 分析家族病史、评估遗传风险、识别家庭健康模式、提供个性化预防建议 |
| [fastreer](skills/clawbio/fastreer/) | `clawbio` | >- |
| [fhir-developer-skill](skills/openclaw/fhir-developer-skill/) | `openclaw` | > |
| [find-skills](skills/openclaw/find-skills/) | `openclaw` | Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is... |
| [fitness-analyzer](skills/openclaw/fitness-analyzer/) | `openclaw` | 分析运动数据、识别运动模式、评估健身进展，并提供个性化训练建议。支持与慢性病数据的关联分析。 |
| [flowio](skills/kdense/flowio/) | `kdense` | Parse FCS (Flow Cytometry Standard) files v2.0-3.1. Extract events as NumPy arrays, read metadata/channels, convert t... |
| [flowio-flow-cytometry](skills/sciagent/flowio-flow-cytometry/) | `sciagent` | Parse/write FCS (Flow Cytometry) files v2.0-3.1. Events as NumPy, channel metadata, multi-dataset files, CSV/FCS expo... |
| [get-available-resources](skills/kdense/get-available-resources/) | `kdense` | This skill should be used at the start of any computationally intensive scientific task to detect and report availabl... |
| [goal-analyzer](skills/openclaw/goal-analyzer/) | `openclaw` | 分析健康目标数据、识别目标模式、评估目标进度,并提供个性化目标管理建议。支持与营养、运动、睡眠等健康数据的关联分析。 |
| [grief-companion](skills/openclaw/grief-companion/) | `openclaw` | Compassionate bereavement support, memorial creation, grief education, and healing journey guidance. Specializes in u... |
| [health-trend-analyzer](skills/openclaw/health-trend-analyzer/) | `openclaw` | 分析一段时间内健康数据的趋势和模式。关联药物、症状、生命体征、化验结果和其他健康指标的变化。识别令人担忧的趋势、改善情况，并提供数据驱动的洞察。当用户询问健康趋势、模式、随时间的变化或"我的健康状况有什么变化？"时使用。支持多维度分析... |
| [hipaa-compliance](skills/openclaw/hipaa-compliance/) | `openclaw` | Ensure HIPAA compliance when handling PHI (Protected Health Information). Use when writing code that accesses user he... |
| [hypogenic-hypothesis-generation](skills/sciagent/hypogenic-hypothesis-generation/) | `sciagent` | LLM-driven hypothesis generation/testing on tabular data. Three methods: HypoGeniC (data-driven), HypoRefine (literat... |
| [immune-deconvolution](skills/zamushwani/immune-deconvolution/) | `zamushwani` | — |
| [ipsae](skills/adaptyv/ipsae/) | `adaptyv` | > |
| [kragen-knowledge-graph](skills/openclaw/kragen-knowledge-graph/) | `openclaw` | Graph-RAG Solver |
| [leads-literature-mining](skills/openclaw/leads-literature-mining/) | `openclaw` | Review Automator |
| [manuscript-review-council](skills/omics/manuscript-review-council/) | `omics` | Run a multi-agent scientific manuscript review with parallel specialist reviewers, disagreement checks, and an editor... |
| [markitdown](skills/kdense/markitdown/) | `kdense` | Convert files and office documents to Markdown. Supports PDF, DOCX, PPTX, XLSX, images (with OCR), audio (with transc... |
| [medical-imaging-review](skills/openclaw/medical-imaging-review/) | `openclaw` | > |
| [mental-health-analyzer](skills/openclaw/mental-health-analyzer/) | `openclaw` | 分析心理健康数据、识别心理模式、评估心理健康状况、提供个性化心理健康建议。支持与睡眠、运动、营养等其他健康数据的关联分析。 |
| [mesh-generation](skills/openclaw/mesh-generation/) | `openclaw` | Plan and evaluate mesh generation for numerical simulations. Use when choosing grid resolution, checking aspect ratio... |
| [molecule-evolution-agent](skills/openclaw/molecule-evolution-agent/) | `openclaw` | Evolve Molecules |
| [molfeat](skills/openclaw/molfeat/) | `openclaw` | Molecular featurization for ML (100+ featurizers). ECFP, MACCS, descriptors, pretrained models (ChemBERTa), convert S... |
| [multimodal-medical-imaging](skills/openclaw/multimodal-medical-imaging/) | `openclaw` | Analyzes medical images (X-ray, MRI, CT) using multimodal LLMs to identify anomalies and generate reports. |
| [nutrition-analyzer](skills/openclaw/nutrition-analyzer/) | `openclaw` | 分析营养数据、识别营养模式、评估营养状况，并提供个性化营养建议。支持与运动、睡眠、慢性病数据的关联分析。 |
| [occupational-health-analyzer](skills/openclaw/occupational-health-analyzer/) | `openclaw` | 分析职业健康数据、识别工作相关健康风险、评估职业健康状况、提供个性化职业健康建议。支持与睡眠、运动、心理健康等其他健康数据的关联分析。 |
| [opentrons-protocol-agent](skills/openclaw/opentrons-protocol-agent/) | `openclaw` | Generates executable Python protocols for Opentrons OT-2 and Flex robots from natural language descriptions. |
| [opentrons-protocol-api](skills/sciagent/opentrons-protocol-api/) | `sciagent` | Python API v2 for Opentrons OT-2/Flex liquid handlers: protocols as Python files with metadata and run(); control pip... |
| [paper-2-web](skills/openclaw/paper-2-web/) | `openclaw` | This skill should be used when converting academic papers into promotional and presentation formats including interac... |
| [pdf-processing](skills/openclaw/pdf-processing/) | `openclaw` | Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user... |
| [prior-auth-coworker](skills/openclaw/prior-auth-coworker/) | `openclaw` | Prior Auth Review |
| [psychologist-analyst](skills/openclaw/psychologist-analyst/) | `openclaw` | \| |
| [pydicom-medical-imaging](skills/sciagent/pydicom-medical-imaging/) | `sciagent` | Pure Python DICOM for medical imaging (CT, MRI, X-ray, ultrasound). Read/write DICOM, pixels as NumPy, edit tags, win... |
| [radgpt-radiology-reporter](skills/openclaw/radgpt-radiology-reporter/) | `openclaw` | Radiology Reporter |
| [receiving-code-review](skills/openclaw/receiving-code-review/) | `openclaw` | Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or tec... |
| [recovery-community-moderator](skills/openclaw/recovery-community-moderator/) | `openclaw` | Trauma-informed AI moderator for addiction recovery communities. Applies harm reduction principles, honors 12-step tr... |
| [regulatory-drafter](skills/openclaw/regulatory-drafter/) | `openclaw` | Automates the drafting of regulatory documents (e.g., FDA CTD sections) with citation management and audit trails. |
| [rehabilitation-analyzer](skills/openclaw/rehabilitation-analyzer/) | `openclaw` | 分析康复训练数据、识别康复模式、评估康复进展，并提供个性化康复建议 |
| [requesting-code-review](skills/openclaw/requesting-code-review/) | `openclaw` | Use when completing tasks, implementing major features, or before merging to verify work meets requirements |
| [scientific-impact-assessment](skills/omics/scientific-impact-assessment/) | `omics` | Assess paper and journal impact using OpenAlex citation counts, optional Altmetric data, and curated journal impact-f... |
| [setup](skills/adaptyv/setup/) | `adaptyv` | > |
| [shap-model-explainability](skills/sciagent/shap-model-explainability/) | `sciagent` | >- |
| [simpy](skills/openclaw/simpy/) | `openclaw` | Process-based discrete-event simulation framework in Python. Use this skill when building simulations of systems with... |
| [simpy-discrete-event-simulation](skills/sciagent/simpy-discrete-event-simulation/) | `sciagent` | Process-based discrete-event simulation. Model queues, shared resources, timed events: manufacturing, service ops, ne... |
| [simulation-validator](skills/openclaw/simulation-validator/) | `openclaw` | Validate simulations before, during, and after execution. Use for pre-flight checks, runtime monitoring, post-run val... |
| [sleep-analyzer](skills/openclaw/sleep-analyzer/) | `openclaw` | 分析睡眠数据、识别睡眠模式、评估睡眠质量，并提供个性化睡眠改善建议。支持与其他健康数据的关联分析。 |
| [slurm-job-script-generator](skills/openclaw/slurm-job-script-generator/) | `openclaw` | Generate SLURM `sbatch` job scripts and sanity-check HPC resource requests (nodes, tasks, CPUs, memory, GPUs) for sim... |
| [sragent](skills/sragent/claude-skill/) | `sragent` | \| |
| [subagent-driven-development](skills/openclaw/subagent-driven-development/) | `openclaw` | Use when executing implementation plans with independent tasks in the current session |
| [sympy-symbolic-math](skills/sciagent/sympy-symbolic-math/) | `sciagent` | Symbolic math in Python: exact algebra, calculus (derivatives, integrals, limits), equation solving, symbolic matrice... |
| [systematic-debugging](skills/openclaw/systematic-debugging/) | `openclaw` | Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes |
| [tcm-constitution-analyzer](skills/openclaw/tcm-constitution-analyzer/) | `openclaw` | 分析中医体质数据、识别体质类型、评估体质特征,并提供个性化养生建议。支持与营养、运动、睡眠等健康数据的关联分析。 |
| [test-driven-development](skills/openclaw/test-driven-development/) | `openclaw` | Use when implementing any feature or bugfix, before writing implementation code |
| [time-stepping](skills/openclaw/time-stepping/) | `openclaw` | Plan and control time-step policies for simulations. Use when coupling CFL/physics limits with adaptive stepping, ram... |
| [timesfm-forecasting](skills/openclaw/timesfm-forecasting/) | `openclaw` | Zero-shot time series forecasting with Google's TimesFM foundation model. Use for any univariate time series (sales, ... |
| [transformers](skills/kdense/transformers/) | `kdense` | This skill should be used when working with pre-trained transformer models for natural language processing, computer ... |
| [travel-health-analyzer](skills/openclaw/travel-health-analyzer/) | `openclaw` | 分析旅行健康数据、评估目的地健康风险、提供疫苗接种建议、生成多语言紧急医疗信息卡片。支持WHO/CDC数据集成的专业级旅行健康风险评估。 |
| [trialgpt-matching](skills/openclaw/trialgpt-matching/) | `openclaw` | Trial shortlist |
| [using-git-worktrees](skills/openclaw/using-git-worktrees/) | `openclaw` | Use when starting feature work that needs isolation from current workspace or before executing implementation plans -... |
| [verification-before-completion](skills/openclaw/verification-before-completion/) | `openclaw` | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running ver... |
| [weightloss-analyzer](skills/openclaw/weightloss-analyzer/) | `openclaw` | 分析减肥数据、计算代谢率、追踪能量缺口、管理减肥阶段 |
| [writing-plans](skills/openclaw/writing-plans/) | `openclaw` | Use when you have a spec or requirements for a multi-step task, before touching code |
| [writing-skills](skills/openclaw/writing-skills/) | `openclaw` | Use when creating new skills, editing existing skills, or verifying skills work before deployment |

</details>

<br/>

## 🏥 Clinical 临床医学
<br/>

<details>
<summary><b>Click to expand · 点击展开 (97 skills)</b></summary>

| Skill | Source 来源 | Description 描述 |
|-------|-------------|------------------|
| [agentd-drug-discovery](skills/openclaw/agentd-drug-discovery/) | `openclaw` | Use the AgentD workflow to mine evidence, design molecules, and rank candidates with SAR plus ADMET annotations for e... |
| [autodock-vina-docking](skills/sciagent/autodock-vina-docking/) | `sciagent` | Molecular docking with AutoDock Vina (Python API). Receptor/ligand prep (Meeko + RDKit), grid box, docking, pose and ... |
| [autonomous-oncology-agent](skills/openclaw/autonomous-oncology-agent/) | `openclaw` | Precision Oncology |
| [bio-admet-prediction](skills/bioskills/admet-prediction/) | `bioskills` | Predicts ADMET properties using ADMETlab 3.0 (119 endpoints with uncertainty), ADMET-AI, DeepChem MolNet, and chempro... |
| [bio-clinical-biostatistics-bayesian-trials](skills/bioskills/bayesian-trials/) | `bioskills` | Designs Bayesian clinical trials including Phase I dose-finding (BOIN, CRM, EWOC, mTPI-2), meta-analytic-predictive (... |
| [bio-clinical-biostatistics-cdisc-data](skills/bioskills/cdisc-data-handling/) | `bioskills` | Reads, validates, and prepares CDISC SDTM and ADaM clinical trial data for analysis. Covers SDTM domain joins (DM, AE... |
| [bio-clinical-biostatistics-effect-measures](skills/bioskills/effect-measures/) | `bioskills` | Computes and interprets treatment effect measures (OR, RR, RD, HR, NNT) with calibrated confidence intervals (Wilson,... |
| [bio-clinical-biostatistics-logistic-regression](skills/bioskills/logistic-regression/) | `bioskills` | Performs logistic regression for clinical trial outcomes (binary, ordinal, multinomial) with marginal-vs-conditional ... |
| [bio-clinical-biostatistics-missing-data](skills/bioskills/missing-data-sensitivity/) | `bioskills` | Implements missing-data sensitivity analyses for confirmatory clinical trials including MMRM under MAR (with Kenward-... |
| [bio-clinical-biostatistics-multiplicity-graphical](skills/bioskills/multiplicity-graphical/) | `bioskills` | Implements multiplicity control for confirmatory clinical trials using graphical procedures (Bretz-Maurer-Hommel), ga... |
| [bio-clinical-biostatistics-subgroup-analysis](skills/bioskills/subgroup-analysis/) | `bioskills` | Performs subgroup and heterogeneous treatment effect (HTE) analyses for clinical trials. Covers Mantel-Haenszel pooli... |
| [bio-clinical-biostatistics-survival-analysis](skills/bioskills/survival-analysis/) | `bioskills` | Performs time-to-event analysis for clinical trials including Cox proportional hazards regression with PH diagnostics... |
| [bio-clinical-biostatistics-trial-reporting](skills/bioskills/trial-reporting/) | `bioskills` | Prepares statistical reports for clinical trials following CONSORT 2025, SPIRIT 2025, ICH E9(R1) estimands, and FDA 2... |
| [bio-clinical-databases-polygenic-risk](skills/bioskills/polygenic-risk/) | `bioskills` | Constructs and validates polygenic risk scores using LDpred2-auto, SBayesRC, MegaPRS, PRS-CS, PROSPER, MUSSEL, Bridge... |
| [bio-covalent-design](skills/bioskills/covalent-design/) | `bioskills` | Designs covalent inhibitors and warheads targeting cysteine (most common, 98% of covalent drugs), lysine, serine, thr... |
| [bio-systems-biology-gene-essentiality](skills/bioskills/gene-essentiality/) | `bioskills` | Perform in silico gene knockout analysis and synthetic lethality screens using COBRApy single and double deletions. P... |
| [bio-workflows-clinical-trial-pipeline](skills/bioskills/clinical-trial-pipeline/) | `bioskills` | End-to-end clinical trial analysis workflow from CDISC SDTM/ADaM loading through ICH E9(R1) estimand-driven primary a... |
| [bio-workflows-outbreak-pipeline](skills/bioskills/outbreak-pipeline/) | `bioskills` | End-to-end outbreak investigation from pathogen isolates to transmission networks. Orchestrates MLST typing, AMR surv... |
| [biomedical-search](skills/openclaw/biomedical-search/) | `openclaw` | Complete biomedical information search combining PubMed, preprints, clinical trials, and FDA drug labels. Powered by ... |
| [cancer-metabolism-agent](skills/openclaw/cancer-metabolism-agent/) | `openclaw` | AI-powered analysis of cancer metabolic reprogramming including Warburg effect, glutamine addiction, lipid metabolism... |
| [cancer-research-figure-guide](skills/sciagent/cancer-research-figure-guide/) | `sciagent` | Cancer Research (AACR) figures: resolution (300-1200 DPI), formats (EPS/TIFF/AI), hierarchical panel labels (Ai, Aii,... |
| [cart-design-optimizer-agent](skills/openclaw/cart-design-optimizer-agent/) | `openclaw` | AI-guided CAR-T cell design for solid tumors using antigen prioritization, safety-by-design architectures, and exhaus... |
| [cellular-senescence-agent](skills/openclaw/cellular-senescence-agent/) | `openclaw` | AI-powered analysis of cellular senescence for aging research, cancer therapy response, and senolytic drug development. |
| [chatehr-clinician-assistant](skills/openclaw/chatehr-clinician-assistant/) | `openclaw` | EHR Chat Assistant |
| [chematagent-drug-discovery](skills/openclaw/chematagent-drug-discovery/) | `openclaw` | Chemical Lab Agent |
| [chembl-database-bioactivity](skills/sciagent/chembl-database-bioactivity/) | `sciagent` | Query ChEMBL (2M+ compounds, 19M+ bioactivity measurements, 13K+ targets) via the public REST/JSON API with plain `re... |
| [chemcrow-drug-discovery](skills/openclaw/chemcrow-drug-discovery/) | `openclaw` | An LLM chemistry agent with expert-designed tools for organic synthesis, drug discovery, and materials design. |
| [chemical-property-lookup](skills/openclaw/chemical-property-lookup/) | `openclaw` | Compute RDKit-driven molecular properties (MW, logP, TPSA, QED, Lipinski) for a SMILES string to support downstream d... |
| [chromosomal-instability-agent](skills/openclaw/chromosomal-instability-agent/) | `openclaw` | AI-powered analysis of chromosomal instability (CIN) signatures for cancer prognosis, immunotherapy response predicti... |
| [claw-semantic-sim](skills/clawbio/claw-semantic-sim/) | `clawbio` | Semantic Similarity Index for disease research literature using PubMedBERT embeddings |
| [clinical-diagnostic-reasoning](skills/openclaw/clinical-diagnostic-reasoning/) | `openclaw` | Identify and counteract cognitive biases in medical decision-making through systematic error analysis and contextual ... |
| [clinical-reports](skills/kdense/clinical-reports/) | `kdense` | Write comprehensive clinical reports including case reports (CARE guidelines), diagnostic reports (radiology/patholog... |
| [clinical-trial-protocol-skill](skills/openclaw/clinical-trial-protocol-skill/) | `openclaw` | Generate clinical trial protocols for medical devices or drugs. This skill should be used when users say "Create a cl... |
| [clinical-trials-search](skills/openclaw/clinical-trials-search/) | `openclaw` | Search ClinicalTrials.gov with natural language queries. Find clinical trials, enrollment, and outcomes using Valyu s... |
| [clinicaltrials-database](skills/openclaw/clinicaltrials-database/) | `openclaw` | Query ClinicalTrials.gov via API v2. Search trials by condition, drug, location, status, or phase. Retrieve trial det... |
| [clinicaltrials-database-search](skills/sciagent/clinicaltrials-database-search/) | `sciagent` | Query ClinicalTrials.gov API v2 for trial data. Search by condition, drug/intervention, location, sponsor, or phase; ... |
| [ctdna-dynamics-mrd-agent](skills/openclaw/ctdna-dynamics-mrd-agent/) | `openclaw` | AI-powered circulating tumor DNA dynamics analysis for molecular residual disease detection, treatment response monit... |
| [cytokine-storm-analysis-agent](skills/openclaw/cytokine-storm-analysis-agent/) | `openclaw` | AI-powered cytokine release syndrome (CRS) and cytokine storm analysis for prediction, monitoring, and management in ... |
| [datacommons-client](skills/openclaw/datacommons-client/) | `openclaw` | Work with Data Commons, a platform providing programmatic access to public statistical data from global sources. Use ... |
| [datamol](skills/kdense/datamol/) | `kdense` | Pythonic wrapper around RDKit with simplified interface and sensible defaults. Preferred for standard drug discovery ... |
| [datamol-cheminformatics](skills/sciagent/datamol-cheminformatics/) | `sciagent` | >- |
| [deepchem](skills/kdense/deepchem/) | `kdense` | Molecular ML with diverse featurizers and pre-built datasets. Use for property prediction (ADMET, toxicity) with trad... |
| [depmap](skills/kdense/depmap/) | `kdense` | Query the Cancer Dependency Map (DepMap) for cancer cell line gene dependency scores (CRISPR Chronos), drug sensitivi... |
| [drug-discovery-search](skills/openclaw/drug-discovery-search/) | `openclaw` | End-to-end drug discovery platform combining ChEMBL compounds, DrugBank, targets, and FDA labels. Natural language po... |
| [drug-interaction-checker](skills/openclaw/drug-interaction-checker/) | `openclaw` | Checks for potential drug-drug interactions (DDIs) between a list of medications. |
| [drug-labels-search](skills/openclaw/drug-labels-search/) | `openclaw` | Search FDA drug labels with natural language queries. Official drug information, indications, and safety data via Valyu. |
| [drug-photo](skills/clawbio/drug-photo/) | `clawbio` | Medication photo to personalised PGx dosage card via Claude vision — snap a pill, get genotype-informed guidance |
| [drugbank-database-access](skills/sciagent/drugbank-database-access/) | `sciagent` | Parse local DrugBank XML for drug info, interactions, targets, and properties. Search by ID/name/CAS, extract DDIs wi... |
| [drugbank-search](skills/openclaw/drugbank-search/) | `openclaw` | Search DrugBank comprehensive drug database with natural language queries. Drug mechanisms, interactions, and safety ... |
| [ehr-analysis](skills/bioclaw_hub/ehr-analysis/) | `bioclaw_hub` | End-to-end EHR predictive modeling pipeline with PyHealth, covering dataset loading, task definition, model training,... |
| [exosome-ev-analysis-agent](skills/openclaw/exosome-ev-analysis-agent/) | `openclaw` | AI-powered extracellular vesicle and exosome analysis for cancer biomarker discovery, liquid biopsy applications, and... |
| [imaging-data-commons](skills/kdense/imaging-data-commons/) | `kdense` | Query and download public cancer imaging data from NCI Imaging Data Commons using idc-index. Use for accessing large-... |
| [immune-checkpoint-combination-agent](skills/openclaw/immune-checkpoint-combination-agent/) | `openclaw` | AI-powered analysis for predicting optimal immune checkpoint inhibitor combinations based on tumor microenvironment, ... |
| [liquid-biopsy-analytics-agent](skills/openclaw/liquid-biopsy-analytics-agent/) | `openclaw` | Comprehensive analysis of liquid biopsy data (ctDNA, CTCs) for cancer detection, MRD monitoring, and response tracking. |
| [mdanalysis-trajectory](skills/sciagent/mdanalysis-trajectory/) | `sciagent` | Analyze MD trajectories from GROMACS, AMBER, NAMD, CHARMM, LAMMPS. Reads topology/trajectory into Universe objects; s... |
| [medchem](skills/kdense/medchem/) | `kdense` | Medicinal chemistry filters. Apply drug-likeness rules (Lipinski, Veber), PAINS filters, structural alerts, complexit... |
| [medical-entity-extractor](skills/openclaw/medical-entity-extractor/) | `openclaw` | Extract medical entities (symptoms, medications, lab values, diagnoses) from patient messages. |
| [medical-research-toolkit](skills/openclaw/medical-research-toolkit/) | `openclaw` | Query 14+ biomedical databases for drug repurposing, target discovery, clinical trials, and literature research. Acce... |
| [modern-drug-rehab-computer](skills/openclaw/modern-drug-rehab-computer/) | `openclaw` | Comprehensive knowledge system for addiction recovery environments, supporting both residential and outpatient (IOP/P... |
| [molfeat-molecular-featurization](skills/sciagent/molfeat-molecular-featurization/) | `sciagent` | Molecular featurization hub (100+ featurizers) for ML. SMILES to fingerprints (ECFP, MACCS, MAP4), descriptors (RDKit... |
| [mpn-progression-monitor-agent](skills/openclaw/mpn-progression-monitor-agent/) | `openclaw` | AI-powered myeloproliferative neoplasm monitoring for disease progression prediction, treatment response tracking, an... |
| [mpn-research-assistant](skills/openclaw/mpn-research-assistant/) | `openclaw` | Myeloproliferative neoplasm (MPN) research expertise including JAK2/CALR/MPL mutations, myelofibrosis, polycythemia v... |
| [mrd-edge-detection-agent](skills/openclaw/mrd-edge-detection-agent/) | `openclaw` | Ultra-sensitive AI-powered molecular residual disease detection using MRD-EDGE deep learning for sub-0.001% VAF ctDNA... |
| [multi-ancestry-prs-agent](skills/openclaw/multi-ancestry-prs-agent/) | `openclaw` | AI-powered multi-ancestry polygenic risk score calculation and optimization for equitable disease risk prediction acr... |
| [nk-cell-therapy-agent](skills/openclaw/nk-cell-therapy-agent/) | `openclaw` | AI-powered NK cell therapy design for cancer immunotherapy including CAR-NK engineering, memory-like NK generation, a... |
| [open-targets-search](skills/openclaw/open-targets-search/) | `openclaw` | Search Open Targets drug-disease associations with natural language queries. Target validation powered by Valyu seman... |
| [opentargets-database](skills/sciagent/opentargets-database/) | `sciagent` | Query Open Targets GraphQL API for target-disease associations, evidence, drug links, safety. Search targets by gene,... |
| [organoid-drug-response-agent](skills/openclaw/organoid-drug-response-agent/) | `openclaw` | AI-powered analysis of patient-derived organoid (PDO) drug screening for personalized oncology treatment selection an... |
| [patiently-ai](skills/openclaw/patiently-ai/) | `openclaw` | Patiently AI simplifies medical documents for patients. Takes doctor's letters, test results, prescriptions, discharg... |
| [pdx-model-analysis-agent](skills/openclaw/pdx-model-analysis-agent/) | `openclaw` | AI-powered analysis of patient-derived xenograft (PDX) models for drug response prediction, translational research, a... |
| [primekg](skills/kdense/primekg/) | `kdense` | Query the Precision Medicine Knowledge Graph (PrimeKG) for multiscale biological data including genes, drugs, disease... |
| [prior-auth-review-skill](skills/openclaw/prior-auth-review-skill/) | `openclaw` | Automate payer review of prior authorization (PA) requests. This skill should be used when users say "Review this PA ... |
| [prs-net-deep-learning-agent](skills/openclaw/prs-net-deep-learning-agent/) | `openclaw` | Geometric deep learning-based polygenic risk score prediction using PRS-Net for modeling gene interactions, enhanced ... |
| [pytdc-therapeutics-data-commons](skills/sciagent/pytdc-therapeutics-data-commons/) | `sciagent` | > |
| [query-opentarget](skills/bioclaw/query-opentarget/) | `bioclaw` | Query OpenTargets for drug targets, disease associations, and therapeutic evidence. Use when user asks about drug tar... |
| [scientific-critical-thinking](skills/sciagent/scientific-critical-thinking/) | `sciagent` | Evaluating scientific evidence and claims. Covers study design hierarchy (RCT to expert opinion), effect sizes (OR, R... |
| [scientific-literature-search](skills/sciagent/scientific-literature-search/) | `sciagent` | Systematic strategies for searching scientific literature across PubMed, arXiv, Google Scholar, and AI-assisted tools... |
| [scientific-manuscript](skills/openclaw/scientific-manuscript/) | `openclaw` | High-impact scientific manuscript preparation for journals like Nature, Blood, Cell. Use when writing abstracts, intr... |
| [target-validation-scorer](skills/clawbio/target-validation-scorer/) | `clawbio` | Evidence-grounded target validation scoring with GO/NO-GO decisions for drug discovery campaigns |
| [tcell-exhaustion-analysis-agent](skills/openclaw/tcell-exhaustion-analysis-agent/) | `openclaw` | AI-powered analysis of T-cell exhaustion states, epigenetic scarring, stem-like T-cell populations, and checkpoint bl... |
| [tcr-repertoire-analysis-agent](skills/openclaw/tcr-repertoire-analysis-agent/) | `openclaw` | AI-powered T-cell receptor repertoire analysis for cancer diagnosis, immunotherapy response prediction, and therapeut... |
| [tooluniverse-adverse-event-detection](skills/openclaw/tooluniverse-adverse-event-detection/) | `openclaw` | Detect and analyze adverse drug event signals using FDA FAERS data, drug labels, disproportionality analysis (PRR, RO... |
| [tooluniverse-antibody-engineering](skills/openclaw/tooluniverse-antibody-engineering/) | `openclaw` | Comprehensive antibody engineering and optimization for therapeutic development. Covers humanization, affinity matura... |
| [tooluniverse-clinical-trial-design](skills/openclaw/tooluniverse-clinical-trial-design/) | `openclaw` | Strategic clinical trial design feasibility assessment using ToolUniverse. Evaluates patient population sizing, bioma... |
| [tooluniverse-disease-research](skills/openclaw/tooluniverse-disease-research/) | `openclaw` | Generate comprehensive disease research reports using 100+ ToolUniverse tools. Creates a detailed markdown report fil... |
| [tooluniverse-drug-drug-interaction](skills/openclaw/tooluniverse-drug-drug-interaction/) | `openclaw` | Comprehensive drug-drug interaction (DDI) prediction and risk assessment. Analyzes interaction mechanisms (CYP450, tr... |
| [tooluniverse-drug-repurposing](skills/openclaw/tooluniverse-drug-repurposing/) | `openclaw` | Identify drug repurposing candidates using ToolUniverse for target-based, compound-based, and disease-driven strategi... |
| [tooluniverse-network-pharmacology](skills/openclaw/tooluniverse-network-pharmacology/) | `openclaw` | Construct and analyze compound-target-disease networks for drug repurposing, polypharmacology discovery, and systems ... |
| [tooluniverse-precision-oncology](skills/openclaw/tooluniverse-precision-oncology/) | `openclaw` | Provide actionable treatment recommendations for cancer patients based on molecular profile. Interprets tumor mutatio... |
| [tooluniverse-statistical-modeling](skills/openclaw/tooluniverse-statistical-modeling/) | `openclaw` | Perform statistical modeling and regression analysis on biomedical datasets. Supports linear regression, logistic reg... |
| [transformers-bio-nlp](skills/sciagent/transformers-bio-nlp/) | `sciagent` | HuggingFace Transformers with biomedical LMs (BioBERT, PubMedBERT, BioGPT, BioMedLM) for scientific NLP: NER (genes, ... |
| [treatment-plans](skills/kdense/treatment-plans/) | `kdense` | Generate concise (3-4 page), focused medical treatment plans in LaTeX/PDF format for all clinical specialties. Suppor... |
| [trial-eligibility-agent](skills/openclaw/trial-eligibility-agent/) | `openclaw` | Parse trial protocols and patient data to produce criterion-level MET/NOT/UNKNOWN determinations with evidence and ga... |
| [tumor-clonal-evolution-agent](skills/openclaw/tumor-clonal-evolution-agent/) | `openclaw` | AI-powered analysis of tumor clonal architecture, subclonal dynamics, and evolutionary trajectories from multi-region... |
| [tumor-heterogeneity-agent](skills/openclaw/tumor-heterogeneity-agent/) | `openclaw` | AI-powered intratumor heterogeneity analysis for clonal architecture reconstruction, subclonal evolution tracking, an... |
| [tumor-mutational-burden-agent](skills/openclaw/tumor-mutational-burden-agent/) | `openclaw` | Calculates and harmonizes Tumor Mutational Burden (TMB) across platforms to predict immunotherapy response. |
| [zinc-database](skills/sciagent/zinc-database/) | `sciagent` | Query ZINC15/ZINC22 virtual compound libraries (1.4B compounds, 750M purchasable). Search lead/fragment/drug-like com... |

</details>

<br/>

## 📊 Transcriptomics 转录组学
<br/>

<details>
<summary><b>Click to expand · 点击展开 (87 skills)</b></summary>

| Skill | Source 来源 | Description 描述 |
|-------|-------------|------------------|
| [adaptyv-bio](skills/sciagent/adaptyv-bio/) | `sciagent` | API + Python SDK for ordering cell-free protein expression and binding assays. Submit sequences for expression (10–10... |
| [alternative-splicing](skills/bioclaw_hub/alternative-splicing/) | `bioclaw_hub` | Workflow for event-level and isoform-level splicing analysis with sashimi-ready outputs and splice QC. |
| [armored-cart-design-agent](skills/openclaw/armored-cart-design-agent/) | `openclaw` | AI-powered design of armored CAR-T cells with cytokine/chemokine expression for enhanced solid tumor efficacy, includ... |
| [bio-atac-seq-differential-accessibility](skills/bioskills/differential-accessibility/) | `bioskills` | Identify differentially accessible chromatin regions across conditions using DiffBind, csaw, DESeq2, or edgeR. Use wh... |
| [bio-chipseq-differential-binding](skills/bioskills/differential-binding/) | `bioskills` | Identifies differentially bound ChIP-seq regions between conditions using DiffBind, csaw (sliding windows), DESeq2/ed... |
| [bio-chipseq-spike-in-normalization](skills/bioskills/spike-in-normalization/) | `bioskills` | Normalizes ChIP-seq data using exogenous spike-in (ChIP-Rx with Drosophila chromatin per Orlando 2014 / Egan 2016; E.... |
| [bio-clip-seq-ago-clip-mirna-targets](skills/bioskills/ago-clip-mirna-targets/) | `bioskills` | Identify direct miRNA-target interactions from AGO HITS-CLIP, AGO-CLEAR-CLIP (chimeric reads), HEAP (Halo-Ago2 mouse)... |
| [bio-clip-seq-binding-site-annotation](skills/bioskills/binding-site-annotation/) | `bioskills` | Annotate CLIP-seq peaks or crosslink sites to RNA features (5'UTR, CDS, 3'UTR, intron, splice junction, snoRNA, tRNA,... |
| [bio-clip-seq-differential-clip](skills/bioskills/differential-clip/) | `bioskills` | Identify differentially bound regions across CLIP-seq conditions (knockdown vs control, treatment vs vehicle, disease... |
| [bio-codon-usage](skills/bioskills/codon-usage/) | `bioskills` | Analyze codon usage, calculate CAI (Codon Adaptation Index), and examine synonymous codon bias using Biopython. Use w... |
| [bio-crispr-screens-batch-correction](skills/bioskills/batch-correction/) | `bioskills` | Batch effect correction for CRISPR screens covering ComBat empirical-Bayes, RUV, SVA, control-sgRNA normalization, an... |
| [bio-data-visualization-network-visualization](skills/bioskills/network-visualization/) | `bioskills` | Visualize biological networks (PPI, gene-regulatory, co-expression, pathway) with layout algorithm choice (ForceAtlas... |
| [bio-data-visualization-volcano-and-ma-plots](skills/bioskills/volcano-and-ma-plots/) | `bioskills` | Build volcano and MA plots from differential-expression / association results with LFC shrinkage, FDR-adjusted thresh... |
| [bio-data-visualization-volcano-customization](skills/openclaw/bio-data-visualization-volcano-customization/) | `openclaw` | Create publication-ready volcano plots with custom thresholds, gene labels, and highlighting using ggplot2, EnhancedV... |
| [bio-de-deseq2-basics](skills/bioskills/deseq2-basics/) | `bioskills` | Perform differential expression analysis using DESeq2 in R/Bioconductor. Use for analyzing RNA-seq count data, creati... |
| [bio-de-edger-basics](skills/bioskills/edger-basics/) | `bioskills` | Perform differential expression analysis using edgeR in R/Bioconductor. Use for analyzing RNA-seq count data with the... |
| [bio-de-results](skills/bioskills/de-results/) | `bioskills` | Extract, filter, annotate, and export differential expression results from DESeq2 or edgeR. Use for identifying signi... |
| [bio-differential-expression-batch-correction](skills/bioskills/batch-correction/) | `bioskills` | Remove batch effects from RNA-seq data using ComBat, ComBat-Seq, limma removeBatchEffect, and SVA for unknown batch v... |
| [bio-differential-expression-timeseries-de](skills/bioskills/timeseries-de/) | `bioskills` | Analyze time-series RNA-seq data using limma voom with splines, maSigPro, and ImpulseDE2. Identify genes with dynamic... |
| [bio-differential-splicing](skills/bioskills/differential-splicing/) | `bioskills` | Detects differential alternative splicing between conditions using rMATS-turbo (binomial LRT on junction counts), lea... |
| [bio-epitranscriptomics-m6a-differential](skills/bioskills/m6a-differential/) | `bioskills` | Identify differential m6A methylation between conditions from MeRIP-seq. Use when comparing epitranscriptomic changes... |
| [bio-epitranscriptomics-m6a-peak-calling](skills/bioskills/m6a-peak-calling/) | `bioskills` | Call m6A peaks from MeRIP-seq IP vs input comparisons. Use when identifying m6A modification sites from methylated RN... |
| [bio-epitranscriptomics-m6anet-analysis](skills/bioskills/m6anet-analysis/) | `bioskills` | Detect m6A modifications from Oxford Nanopore direct RNA sequencing using m6Anet. Use when analyzing epitranscriptomi... |
| [bio-expression-matrix-counts-ingest](skills/bioskills/counts-ingest/) | `bioskills` | Load gene expression count matrices from various formats including CSV, TSV, featureCounts, Salmon, kallisto, and 10X... |
| [bio-flow-cytometry-differential-analysis](skills/bioskills/differential-analysis/) | `bioskills` | Differential abundance and state analysis for cytometry data. Compare cell populations between conditions using stati... |
| [bio-gene-regulatory-networks-differential-networks](skills/bioskills/differential-networks/) | `bioskills` | Compare gene regulatory and co-expression networks between biological conditions to identify rewired regulatory relat... |
| [bio-gene-regulatory-networks-perturbation-simulation](skills/bioskills/perturbation-simulation/) | `bioskills` | Simulate transcription factor perturbation effects on cell state using CellOracle, which integrates GRN inference wit... |
| [bio-geo-data](skills/bioskills/geo-data/) | `bioskills` | Query and download from NCBI Gene Expression Omnibus (GEO) and EMBL-EBI's BioStudies/ArrayExpress mirror. Use when fi... |
| [bio-immunoinformatics-immunogenicity-scoring](skills/bioskills/immunogenicity-scoring/) | `bioskills` | Score and prioritize neoantigens and epitopes for immunogenicity using multi-factor models combining MHC binding, pro... |
| [bio-isoform-switching](skills/bioskills/isoform-switching/) | `bioskills` | Analyzes differential transcript usage (DTU) and isoform switches with functional consequence prediction (NMD via 50n... |
| [bio-metabolomics-statistical-analysis](skills/bioskills/statistical-analysis/) | `bioskills` | Statistical analysis for metabolomics data. Covers preprocessing (log2 transformation, normalization), limma moderate... |
| [bio-methylation-differential-cpg](skills/bioskills/differential-cpg-testing/) | `bioskills` | Per-CpG differential methylation testing from bisulfite sequencing count data or beta-value matrices. Covers beta and... |
| [bio-multi-omics-mofa-integration](skills/bioskills/mofa-integration/) | `bioskills` | Multi-Omics Factor Analysis (MOFA2) for unsupervised integration of multiple data modalities. Identifies shared and v... |
| [bio-pathway-go-enrichment](skills/bioskills/go-enrichment/) | `bioskills` | Gene Ontology over-representation analysis using clusterProfiler enrichGO. Use when identifying biological functions ... |
| [bio-pathway-gsea](skills/bioskills/gsea/) | `bioskills` | Gene Set Enrichment Analysis using clusterProfiler gseGO and gseKEGG. Use when analyzing ranked gene lists to find co... |
| [bio-proteomics-differential-abundance](skills/bioskills/differential-abundance/) | `bioskills` | Statistical testing for differentially abundant proteins between conditions. Covers preprocessing (log2 transformatio... |
| [bio-research-tools-biomarker-signature-studio](skills/openclaw/bio-research-tools-biomarker-signature-studio/) | `openclaw` | Multi-omic biomarker discovery studio that ingests expression + metadata, performs QC, multi-strategy feature selecti... |
| [bio-reverse-complement](skills/bioskills/reverse-complement/) | `bioskills` | Generate reverse complements and complements of DNA/RNA sequences using Biopython. Use when working with opposite str... |
| [bio-ribo-seq-translation-efficiency](skills/bioskills/translation-efficiency/) | `bioskills` | Calculate translation efficiency (TE) as the ratio of ribosome occupancy to mRNA abundance. Use when comparing transl... |
| [bio-rna-quantification-tximport-workflow](skills/bioskills/tximport-workflow/) | `bioskills` | Import transcript-level quantifications from Salmon/kallisto into R for gene-level analysis with DESeq2/edgeR using t... |
| [bio-rnaseq-qc](skills/bioskills/rnaseq-qc/) | `bioskills` | RNA-seq specific quality control including rRNA contamination detection, strandedness verification, gene body coverag... |
| [bio-small-rna-seq-differential-mirna](skills/bioskills/differential-mirna/) | `bioskills` | Perform differential expression analysis of miRNAs between conditions using DESeq2 or edgeR with small RNA-specific c... |
| [bio-small-rna-seq-mirdeep2-analysis](skills/bioskills/mirdeep2-analysis/) | `bioskills` | Discover novel miRNAs and quantify known miRNAs using miRDeep2 de novo prediction from small RNA-seq data. Use when i... |
| [bio-small-rna-seq-smrna-preprocessing](skills/bioskills/smrna-preprocessing/) | `bioskills` | Preprocess small RNA sequencing data with adapter trimming and size selection optimized for miRNA, piRNA, and other s... |
| [bio-small-rna-seq-target-prediction](skills/bioskills/target-prediction/) | `bioskills` | Predict miRNA target genes using sequence-based algorithms and database lookups. Use when identifying potential mRNA ... |
| [bio-spatial-transcriptomics-image-analysis](skills/bioskills/image-analysis/) | `bioskills` | Process and analyze tissue images from spatial transcriptomics data using Squidpy. Extract image features, segment ce... |
| [bio-spatial-transcriptomics-spatial-communication](skills/bioskills/spatial-communication/) | `bioskills` | Analyze cell-cell communication in spatial transcriptomics data using ligand-receptor analysis with Squidpy. Infer in... |
| [bio-spatial-transcriptomics-spatial-data-io](skills/bioskills/spatial-data-io/) | `bioskills` | Load spatial transcriptomics data from Visium, Xenium, MERFISH, Slide-seq, and other platforms using Squidpy and Spat... |
| [bio-spatial-transcriptomics-spatial-multiomics](skills/bioskills/spatial-multiomics/) | `bioskills` | Analyze high-resolution spatial platforms like Slide-seq, Stereo-seq, and Visium HD. Use when working with subcellula... |
| [bio-spatial-transcriptomics-spatial-neighbors](skills/bioskills/spatial-neighbors/) | `bioskills` | Build spatial neighbor graphs for spatial transcriptomics data using Squidpy. Compute k-nearest neighbors, Delaunay t... |
| [bio-spatial-transcriptomics-spatial-preprocessing](skills/bioskills/spatial-preprocessing/) | `bioskills` | Quality control, filtering, normalization, and feature selection for spatial transcriptomics data. Calculate QC metri... |
| [bio-spatial-transcriptomics-spatial-proteomics](skills/bioskills/spatial-proteomics/) | `bioskills` | Analyzes spatial proteomics data from CODEX, IMC, and MIBI platforms including cell segmentation and protein colocali... |
| [bio-spatial-transcriptomics-spatial-statistics](skills/bioskills/spatial-statistics/) | `bioskills` | Compute spatial statistics for spatial transcriptomics data using Squidpy. Calculate Moran's I, Geary's C, spatial au... |
| [bio-workflows-biomarker-pipeline](skills/bioskills/biomarker-pipeline/) | `bioskills` | End-to-end biomarker discovery workflow from expression data to validated biomarker panels. Covers feature selection ... |
| [bio-workflows-expression-to-pathways](skills/bioskills/expression-to-pathways/) | `bioskills` | Workflow from differential expression results to functional enrichment analysis. Covers GO, KEGG, Reactome enrichment... |
| [bio-workflows-multi-omics-pipeline](skills/bioskills/multi-omics-pipeline/) | `bioskills` | End-to-end multi-omics integration workflow. Orchestrates data harmonization, MOFA/mixOmics integration, factor inter... |
| [bio-workflows-proteomics-pipeline](skills/bioskills/proteomics-pipeline/) | `bioskills` | End-to-end proteomics workflow from MaxQuant output to differential protein abundance. Orchestrates data import, norm... |
| [bio-workflows-spatial-pipeline](skills/bioskills/spatial-pipeline/) | `bioskills` | End-to-end spatial transcriptomics workflow for Visium/Xenium data. Covers data loading, preprocessing, spatial analy... |
| [bio-workflows-timecourse-pipeline](skills/bioskills/timecourse-pipeline/) | `bioskills` | End-to-end time-course analysis from expression matrix to temporal patterns and enrichment. Covers temporal DE, Mfuzz... |
| [bulk-rna-seq-batch-correction-with-combat](skills/openclaw/bulk-combat-correction/) | `openclaw` | Use omicverse's pyComBat wrapper to remove batch effects from merged bulk RNA-seq or microarray cohorts, export corre... |
| [bulk-wgcna-analysis-with-omicverse](skills/openclaw/bulk-wgcna-analysis/) | `openclaw` | Assist Claude in running PyWGCNA through omicverse—preprocessing expression matrices, constructing co-expression modu... |
| [cell-free-expression](skills/adaptyv/cell-free-expression/) | `adaptyv` | > |
| [cell-free-protein-expression](skills/bioclaw_hub/cell-free-protein-expression/) | `bioclaw_hub` | > |
| [cellfree-rna-agent](skills/openclaw/cellfree-rna-agent/) | `openclaw` | AI-powered cell-free RNA analysis from liquid biopsy for cancer detection, tissue-of-origin identification, and non-i... |
| [crispr-offtarget-predictor](skills/openclaw/crispr-offtarget-predictor/) | `openclaw` | Predicts potential off-target sites for a given sgRNA sequence using mismatch analysis. |
| [de-summary](skills/clawbio/de-summary/) | `clawbio` | Summarise pre-computed differential expression results with ranked gene lists, biological themes, and publication-ready |
| [differential-expression](skills/bioclaw/differential-expression/) | `bioclaw` | Bulk transcriptomics differential expression with count-aware modeling, design validation, contrast handling, thresho... |
| [ginkgo-cloud-lab](skills/kdense/ginkgo-cloud-lab/) | `kdense` | Submit and manage protocols on Ginkgo Bioworks Cloud Lab (cloud.ginkgo.bio), a web-based interface for autonomous lab... |
| [nicheformer-spatial-agent](skills/openclaw/nicheformer-spatial-agent/) | `openclaw` | Foundation model-powered spatial transcriptomics analysis leveraging 53M+ spatially resolved cells for cellular archi... |
| [omics-analysis-guide](skills/sciagent/omics-analysis-guide/) | `sciagent` | Three-tiered approach to omics data analysis (transcriptomics, proteomics) covering validated pipelines, standard wor... |
| [plotly-interactive-plots](skills/sciagent/plotly-interactive-plots/) | `sciagent` | Interactive scientific visualization with Plotly. Two APIs: plotly.express (px) for one-liner DataFrame plots, plotly... |
| [proteomics-de](skills/clawbio/proteomics-de/) | `clawbio` | Differential expression analysis for label-free quantitative (LFQ) intensity data with standard MaxQuant and |
| [pydeseq2](skills/kdense/pydeseq2/) | `kdense` | Differential gene expression analysis (Python DESeq2). Identify DE genes from bulk RNA-seq counts, Wald tests, FDR co... |
| [query-geo](skills/bioclaw/query-geo/) | `bioclaw` | Query NCBI GEO for gene expression datasets. Use when user asks about RNA-seq datasets, microarray data, expression d... |
| [rare-disease-rnaseq](skills/clawbio/rare-disease-rnaseq/) | `clawbio` | Blood RNA-seq expression-outlier detection for rare-disease diagnostics. Cases scored against a control reference pan... |
| [ribo-seq](skills/bioclaw_hub/ribo-seq/) | `bioclaw_hub` | Workflow for ribosome profiling, P-site aware preprocessing, periodicity checks, ORF detection, and translation effic... |
| [rnaseq-de](skills/clawbio/rnaseq-de/) | `clawbio` | Differential expression analysis for bulk RNA-seq and pseudo-bulk count matrices with QC, PCA, and contrast testing. |
| [sds-gel-review](skills/bioclaw/sds-gel-review/) | `bioclaw` | Review SDS-PAGE or protein purification gel images using DNA sequence, protein sequence, base-pair length, expected p... |
| [small-rna-seq](skills/bioclaw_hub/small-rna-seq/) | `bioclaw_hub` | Workflow for small RNA and miRNA preprocessing, quantification, differential analysis, and target-oriented interpreta... |
| [spatial-agent](skills/openclaw/spatial-agent/) | `openclaw` | An agent that interprets spatial transcriptomics data to propose mechanistic hypotheses and analyze tissue organization. |
| [spatial-transcriptomics-agent](skills/openclaw/spatial-transcriptomics-agent/) | `openclaw` | Spatial analyst |
| [spatial-transcriptomics-analysis](skills/openclaw/spatial-transcriptomics-analysis/) | `openclaw` | Automated analysis pipeline for Spatial Transcriptomics (Visium, Xenium) integrating histology and gene expression. |
| [spatial-transcriptomics-tutorials-with-omicverse](skills/openclaw/spatial-tutorials/) | `openclaw` | Guide users through omicverse's spatial transcriptomics tutorials covering preprocessing, deconvolution, and downstre... |
| [sympy](skills/kdense/sympy/) | `kdense` | Use this skill when working with symbolic mathematics in Python. This skill should be used for symbolic computation t... |
| [tooluniverse-metabolomics-analysis](skills/openclaw/tooluniverse-metabolomics-analysis/) | `openclaw` | Analyze metabolomics data including metabolite identification, quantification, pathway analysis, and metabolic flux. ... |
| [tooluniverse-proteomics-analysis](skills/openclaw/tooluniverse-proteomics-analysis/) | `openclaw` | Analyze mass spectrometry proteomics data including protein quantification, differential expression, post-translation... |
| [tooluniverse-rnaseq-deseq2](skills/openclaw/tooluniverse-rnaseq-deseq2/) | `openclaw` | Production-ready RNA-seq differential expression analysis using PyDESeq2. Performs DESeq2 normalization, dispersion e... |

</details>

<br/>

## 🗄️ Databases 数据库查询
<br/>

<details>
<summary><b>Click to expand · 点击展开 (54 skills)</b></summary>

| Skill | Source 来源 | Description 描述 |
|-------|-------------|------------------|
| [aeon](skills/kdense/aeon/) | `kdense` | This skill should be used for time series machine learning tasks including classification, regression, clustering, fo... |
| [arxiv-search](skills/omics/arxiv-search/) | `omics` | Search arXiv preprints through the official arXiv API and turn arXiv IDs into local Markdown summaries. Use when you ... |
| [bio-batch-downloads](skills/bioskills/batch-downloads/) | `bioskills` | Download large datasets from NCBI efficiently using EPost, history server, batching, rate limiting, and retry logic. ... |
| [bio-data-visualization-ggplot2-fundamentals](skills/bioskills/ggplot2-fundamentals/) | `bioskills` | Build publication-quality figures in R with ggplot2 using the grammar of graphics (data + aesthetics + geometries + s... |
| [bio-dataset-search](skills/bioclaw/bio-dataset-search/) | `bioclaw` | — |
| [bio-motif-search](skills/bioskills/motif-search/) | `bioskills` | Find patterns, motifs, and subsequences in biological sequences using Biopython. Use when searching for transcription... |
| [bio-restriction-sites](skills/bioskills/restriction-sites/) | `bioskills` | Find restriction enzyme cut sites in DNA sequences using Biopython Bio.Restriction. Search with single enzymes, batch... |
| [bio-retrosynthesis](skills/bioskills/retrosynthesis/) | `bioskills` | Performs retrosynthetic planning using AiZynthFinder (MCTS, template-based), Chemformer (template-free transformer), ... |
| [bio-tools](skills/bioclaw/bio-tools/) | `bioclaw` | Biology research tools reference. Always available inside agent containers. |
| [biomni-general-agent](skills/openclaw/biomni-general-agent/) | `openclaw` | Use the local Biomni checkout to orchestrate its 150+ biomedical tools, databases, and know-how workflows for complex... |
| [biomni-research-agent](skills/openclaw/biomni-research-agent/) | `openclaw` | Bio-Research Generalist |
| [biorxiv-database](skills/sciagent/biorxiv-database/) | `sciagent` | Query bioRxiv/medRxiv preprints via REST API. Search by DOI, category, or date range; retrieve metadata (title, abstr... |
| [biorxiv-search](skills/omics/biorxiv-search/) | `omics` | Search bioRxiv preprints through the official bioRxiv API and locally filter titles, abstracts, and authors for keywo... |
| [chembl-search](skills/openclaw/chembl-search/) | `openclaw` | Search ChEMBL bioactive molecules database with natural language queries. Find compounds and assay data with Valyu se... |
| [citation-management](skills/kdense/citation-management/) | `kdense` | Comprehensive citation management for academic research. Search Google Scholar and PubMed for papers, extract accurat... |
| [crossref-lookup](skills/omics/crossref-lookup/) | `omics` | Query the Crossref REST API for DOI validation, title search, citation metadata, and bibliography audits. Use when yo... |
| [deep-research](skills/openclaw/deep-research/) | `openclaw` | Execute autonomous multi-step deep research on any topic. Use when the user asks for comprehensive research, literatu... |
| [deep-research-swarm](skills/openclaw/deep-research-swarm/) | `openclaw` | Multi-agent research literature analysis |
| [eqtl-catalogue-region-fetch](skills/clawbio/eqtl-catalogue-region-fetch/) | `clawbio` | \| |
| [exa-search](skills/kdense/exa-search/) | `kdense` | Web toolkit powered by Exa, tuned for scientific and technical content. Use this skill when the user needs to search ... |
| [fluidsim](skills/kdense/fluidsim/) | `kdense` | Framework for computational fluid dynamics simulations using Python. Use when running fluid dynamics simulations incl... |
| [geomaster](skills/kdense/geomaster/) | `kdense` | Comprehensive geospatial science skill covering remote sensing, GIS, spatial analysis, machine learning for earth obs... |
| [geopandas-geospatial](skills/sciagent/geopandas-geospatial/) | `sciagent` | >- |
| [get-api-docs](skills/omics/get-api-docs/) | `omics` | Fetch current API and SDK documentation with the chub CLI. Use when writing or reviewing code against fast-changing A... |
| [knowledge-synthesis](skills/openclaw/knowledge-synthesis/) | `openclaw` | Combines search results from multiple sources into coherent, deduplicated answers with source attribution. Handles co... |
| [labstep](skills/openclaw/labstep/) | `openclaw` | Interact with the Labstep electronic lab notebook API using labstepPy. Query experiments, protocols, resources, inven... |
| [literature-review](skills/kdense/literature-review/) | `kdense` | Conduct comprehensive, systematic literature reviews using multiple academic databases (PubMed, arXiv, bioRxiv, Seman... |
| [literature-search](skills/openclaw/literature-search/) | `openclaw` | Comprehensive scientific literature search across PubMed, arXiv, bioRxiv, medRxiv. Natural language queries powered b... |
| [mcpmed-bioinformatics-server](skills/openclaw/mcpmed-bioinformatics-server/) | `openclaw` | Model Context Protocol (MCP) server for bioinformatics web services like GEO, STRING, and UCSC Cell Browser. |
| [medrxiv-search](skills/openclaw/medrxiv-search/) | `openclaw` | Search medRxiv medical preprints with natural language queries. Powered by Valyu semantic search. |
| [ncbi-datasets](skills/clawbio/ncbi-datasets/) | `clawbio` | >- |
| [nonlinear-solvers](skills/openclaw/nonlinear-solvers/) | `openclaw` | Select and configure nonlinear solvers for f(x)=0 or min F(x). Use for Newton methods, quasi-Newton (BFGS, L-BFGS), B... |
| [optimize-for-gpu](skills/kdense/optimize-for-gpu/) | `kdense` | GPU-accelerate Python code using CuPy, Numba CUDA, Warp, cuDF, cuML, cuGraph, KvikIO, cuCIM, cuxfilter, cuVS, cuSpati... |
| [paper-lookup](skills/kdense/paper-lookup/) | `kdense` | Search 10 academic paper databases via REST APIs for research papers, preprints, and scholarly articles. Covers PubMe... |
| [patents-search](skills/openclaw/patents-search/) | `openclaw` | Search global patents with natural language queries. Prior art, patent landscapes, and innovation tracking via Valyu. |
| [perplexity-search](skills/openclaw/perplexity-search/) | `openclaw` | Perform AI-powered web searches with real-time information using Perplexity models via LiteLLM and OpenRouter. This s... |
| [plotly-interactive-visualization](skills/sciagent/plotly-interactive-visualization/) | `sciagent` | Interactive visualization with Plotly. 40+ chart types (scatter, line, heatmap, 3D, geographic) with hover, zoom, pan... |
| [pubmed-search](skills/openclaw/pubmed-search/) | `openclaw` | Search PubMed for scientific literature. Use when the user asks to find papers, search literature, look up research, ... |
| [pymoo](skills/sciagent/pymoo/) | `sciagent` | Python framework for single- and multi-objective optimization with evolutionary algorithms. Define vectorized objecti... |
| [research-grants](skills/openclaw/research-grants/) | `openclaw` | Write competitive research proposals for NSF, NIH, DOE, and DARPA. Agency-specific formatting, review criteria, budge... |
| [research-literature](skills/openclaw/research-literature/) | `openclaw` | Research Literature agent for healthcare workflows. |
| [research-lookup](skills/openclaw/research-lookup/) | `openclaw` | Look up current research information using Perplexity's Sonar Pro Search or Sonar Reasoning Pro models through OpenRo... |
| [scientific-brainstorming](skills/kdense/scientific-brainstorming/) | `kdense` | Creative research ideation and exploration. Use for open-ended brainstorming sessions, exploring interdisciplinary co... |
| [scientific-problem-selection](skills/openclaw/scientific-problem-selection/) | `openclaw` | This skill should be used when scientists need help with research problem selection, project ideation, troubleshootin... |
| [scikit-learn-machine-learning](skills/sciagent/scikit-learn-machine-learning/) | `sciagent` | Classical ML in Python: classification, regression, clustering, dim reduction, evaluation, tuning, preprocessing pipe... |
| [scikit-survival-analysis](skills/sciagent/scikit-survival-analysis/) | `sciagent` | Time-to-event modeling with scikit-survival: Cox PH (elastic net), Random Survival Forests, Boosting, SVMs for censor... |
| [search-strategy](skills/openclaw/search-strategy/) | `openclaw` | Query decomposition and multi-source search orchestration. Breaks natural language questions into targeted searches p... |
| [statistical-analysis](skills/kdense/statistical-analysis/) | `kdense` | Guided statistical analysis with test selection and reporting. Use when you need help choosing appropriate tests for ... |
| [turingdb-graph](skills/clawbio/turingdb-graph/) | `clawbio` | Build, query, and analyse biomedical knowledge graphs in TuringDB, a columnar graph database with git-like versioning. |
| [ukb-navigator](skills/clawbio/ukb-navigator/) | `clawbio` | Semantic search across UK Biobank's 12,000+ data fields and publications — find the right variables for your |
| [uniprot](skills/adaptyv/uniprot/) | `adaptyv` | > |
| [uspto-database](skills/sciagent/uspto-database/) | `sciagent` | Access USPTO patent data via PatentsView REST API and Google Patents Public Data (BigQuery). Search by inventor, assi... |
| [venue-templates](skills/kdense/venue-templates/) | `kdense` | Access comprehensive LaTeX templates, formatting requirements, and submission guidelines for major scientific publica... |
| [virtual-lab-agent](skills/openclaw/virtual-lab-agent/) | `openclaw` | AI-powered virtual laboratory orchestrating multi-agent scientific research teams for autonomous hypothesis generatio... |

</details>

<br/>

## 🔗 Multi-Omics 多组学整合
<br/>

<details>
<summary><b>Click to expand · 点击展开 (51 skills)</b></summary>

| Skill | Source 来源 | Description 描述 |
|-------|-------------|------------------|
| [bio-data-visualization-specialized-omics-plots](skills/openclaw/bio-data-visualization-specialized-omics-plots/) | `openclaw` | Reusable plotting functions for common omics visualizations. Custom ggplot2/matplotlib implementations of volcano, MA... |
| [bio-fragment-analysis](skills/bioskills/fragment-analysis/) | `bioskills` | Analyzes cfDNA fragment size distributions and fragmentomics features using FinaleToolkit or Griffin. Extracts nucleo... |
| [bio-machine-learning-biomarker-discovery](skills/bioskills/biomarker-discovery/) | `bioskills` | Selects informative features for biomarker discovery using Boruta all-relevant selection, mRMR minimum redundancy, an... |
| [bio-machine-learning-model-validation](skills/bioskills/model-validation/) | `bioskills` | Implements nested cross-validation and stratified splits for unbiased model evaluation on biomedical datasets. Preven... |
| [bio-machine-learning-prediction-explanation](skills/bioskills/prediction-explanation/) | `bioskills` | Explains machine learning predictions on omics data using SHAP values and LIME for feature attribution. Identifies wh... |
| [bio-machine-learning-survival-analysis](skills/bioskills/survival-analysis/) | `bioskills` | Analyzes time-to-event data using Kaplan-Meier curves, log-rank tests, and Cox proportional hazards regression with l... |
| [bio-metabolomics-lipidomics](skills/bioskills/lipidomics/) | `bioskills` | Specialized lipidomics analysis for lipid identification, quantification, and pathway interpretation. Covers LC-MS li... |
| [bio-metabolomics-metabolite-annotation](skills/bioskills/metabolite-annotation/) | `bioskills` | Metabolite identification from m/z and retention time. Covers database matching, MS/MS spectral matching, and confide... |
| [bio-metabolomics-normalization-qc](skills/bioskills/normalization-qc/) | `bioskills` | Quality control and normalization for metabolomics data. Covers QC-based correction, batch effect removal, and data t... |
| [bio-metabolomics-targeted-analysis](skills/bioskills/targeted-analysis/) | `bioskills` | Targeted metabolomics analysis using MRM/SRM with standard curves. Covers absolute quantification, method validation,... |
| [bio-multi-omics-mixomics-analysis](skills/bioskills/mixomics-analysis/) | `bioskills` | Supervised and unsupervised multi-omics integration with mixOmics. Includes sPLS for pairwise integration and DIABLO ... |
| [bio-multi-omics-similarity-network](skills/bioskills/similarity-network/) | `bioskills` | Similarity Network Fusion (SNF) for patient stratification using multi-omics data. Integrates multiple data types int... |
| [bio-viromics](skills/omics/bio-viromics/) | `omics` | Detect, classify, and QC viral contigs. |
| [biomedical-data-analysis](skills/openclaw/biomedical-data-analysis/) | `openclaw` | Omics data forge |
| [brenda-database](skills/sciagent/brenda-database/) | `sciagent` | BRENDA Enzyme DB SOAP/REST queries: kinetic parameters (Km, Vmax, kcat, Ki), EC classes, substrate specificity, inhib... |
| [cancer-multiomics](skills/zamushwani/cancer-multiomics/) | `zamushwani` | — |
| [clinical-decision-support](skills/kdense/clinical-decision-support/) | `kdense` | Generate professional clinical decision support (CDS) documents for pharmaceutical and clinical research settings, in... |
| [dask](skills/openclaw/dask/) | `openclaw` | Distributed computing for larger-than-RAM pandas/NumPy workflows. Use when you need to scale existing pandas/NumPy co... |
| [database-access](skills/bioclaw_hub/database-access/) | `bioclaw_hub` | Workflow for retrieving public omics datasets, sequences, annotations, and literature-linked biological resources. |
| [digital-twin-clinical-agent](skills/openclaw/digital-twin-clinical-agent/) | `openclaw` | AI-powered patient digital twin creation for clinical trial simulation, treatment outcome prediction, and personalize... |
| [ehr-fhir-integration](skills/openclaw/ehr-fhir-integration/) | `openclaw` | Provides comprehensive tools for working with Electronic Health Records (EHR) using the HL7 FHIR standard. |
| [infographics](skills/openclaw/infographics/) | `openclaw` | Create professional infographics using Nano Banana Pro AI with smart iterative refinement. Uses Gemini 3 Pro for qual... |
| [kegg-pathway-analysis](skills/sciagent/kegg-pathway-analysis/) | `sciagent` | Guide to KEGG pathway enrichment for DEG results. Covers ORA vs GSEA, mandatory directionality splitting, KEGG organi... |
| [labarchive-integration](skills/openclaw/labarchive-integration/) | `openclaw` | Electronic lab notebook API integration. Access notebooks, manage entries/attachments, backup notebooks, integrate wi... |
| [latchbio-integration](skills/kdense/latchbio-integration/) | `kdense` | Latch platform for bioinformatics workflows. Build pipelines with Latch SDK, @workflow/@task decorators, deploy serve... |
| [latex-posters](skills/openclaw/latex-posters/) | `openclaw` | Create professional research posters in LaTeX using beamerposter, tikzposter, or baposter. Support for conference pre... |
| [latex-research-posters](skills/sciagent/latex-research-posters/) | `sciagent` | Research posters in LaTeX using beamerposter, tikzposter, or baposter. Layout, typography, color schemes, figure inte... |
| [libsbml-network-modeling](skills/sciagent/libsbml-network-modeling/) | `sciagent` | Build, read, validate, modify SBML biological network models via the libSBML Python API. SBML Levels 1–3, reactions/k... |
| [machine-learning-for-omics](skills/bioclaw_hub/machine-learning-for-omics/) | `bioclaw_hub` | Workflow for predictive modeling, biomarker discovery, survival modeling, and explainability over omics-derived featu... |
| [matplotlib](skills/kdense/matplotlib/) | `kdense` | Low-level plotting library for full customization. Use when you need fine-grained control over every plot element, cr... |
| [medea-therapeutic-discovery](skills/openclaw/medea-therapeutic-discovery/) | `openclaw` | An AI agent for therapeutic discovery that executes transparent, multi-step omics analyses including research plannin... |
| [multi-search-engine](skills/openclaw/multi-search-engine/) | `openclaw` | Multi search engine integration with 17 engines (8 CN + 9 Global). Supports advanced search operators, time filters, ... |
| [neurokit2](skills/kdense/neurokit2/) | `kdense` | Comprehensive biosignal processing toolkit for analyzing physiological data including ECG, EEG, EDA, RSP, PPG, EMG, a... |
| [numerical-integration](skills/openclaw/numerical-integration/) | `openclaw` | Select and configure time integration methods for ODE/PDE simulations. Use when choosing explicit/implicit schemes, s... |
| [omero-integration](skills/kdense/omero-integration/) | `kdense` | Microscopy data management platform. Access images via Python, retrieve datasets, analyze pixels, manage ROIs/annotat... |
| [omics-target-evidence-mapper](skills/clawbio/omics-target-evidence-mapper/) | `clawbio` | Aggregate public target-level evidence across omics and translational sources for research triage. |
| [opentrons-integration](skills/openclaw/opentrons-integration/) | `openclaw` | Lab automation platform for Flex/OT-2 robots. Write Protocol API v2 protocols, liquid handling, hardware modules (hea... |
| [pathway-analysis](skills/bioclaw_hub/pathway-analysis/) | `bioclaw_hub` | Workflow for enrichment testing, ranked-gene analysis, pathway scoring, and pathway-focused visualization across omic... |
| [pennylane](skills/kdense/pennylane/) | `kdense` | Hardware-agnostic quantum ML framework with automatic differentiation. Use when training quantum circuits via gradien... |
| [pptx-posters](skills/openclaw/pptx-posters/) | `openclaw` | Create research posters using HTML/CSS that can be exported to PDF or PPTX. Use this skill ONLY when the user explici... |
| [protocolsio-integration](skills/sciagent/protocolsio-integration/) | `sciagent` | protocols.io REST API: search and fetch wet-lab, bioinformatics, and clinical protocols by keyword, DOI, or category,... |
| [pyzotero](skills/openclaw/pyzotero/) | `openclaw` | Interact with Zotero reference management libraries using the pyzotero Python client. Retrieve, create, update, and d... |
| [reactome-database](skills/sciagent/reactome-database/) | `sciagent` | Query Reactome pathways via REST: pathway queries, entity lookup, keyword search, gene list enrichment, hierarchy, cr... |
| [seaborn](skills/openclaw/seaborn/) | `openclaw` | Statistical visualization with pandas integration. Use for quick exploration of distributions, relationships, and cat... |
| [systems-biology](skills/bioclaw_hub/systems-biology/) | `bioclaw_hub` | Workflow for constraint-based metabolic modeling, context-specific models, gene essentiality, and systems-level inter... |
| [tooluniverse-immunotherapy-response-prediction](skills/openclaw/tooluniverse-immunotherapy-response-prediction/) | `openclaw` | Predict patient response to immune checkpoint inhibitors (ICIs) using multi-biomarker integration. Given a cancer typ... |
| [tooluniverse-metabolomics](skills/openclaw/tooluniverse-metabolomics/) | `openclaw` | Comprehensive metabolomics research skill for identifying metabolites, analyzing studies, and searching metabolomics ... |
| [wellally-tech](skills/openclaw/wellally-tech/) | `openclaw` | Integrate digital health data sources (Apple Health, Fitbit, Oura Ring) and connect to WellAlly.tech knowledge base. ... |
| [workflow-management](skills/bioclaw_hub/workflow-management/) | `bioclaw_hub` | Workflow for orchestrating reproducible omics pipelines with workflow engines and clear execution provenance. |
| [xlsx](skills/kdense/xlsx/) | `kdense` | Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants t... |
| [zarr-python](skills/openclaw/zarr-python/) | `openclaw` | Chunked N-D arrays for cloud storage. Compressed arrays, parallel I/O, S3/GCS integration, NumPy/Dask/Xarray compatib... |

</details>

<br/>

## 🧪 Bioinformatics 生信通用
<br/>

<details>
<summary><b>Click to expand · 点击展开 (50 skills)</b></summary>

| Skill | Source 来源 | Description 描述 |
|-------|-------------|------------------|
| [astropy](skills/kdense/astropy/) | `kdense` | Comprehensive Python library for astronomy and astrophysics. This skill should be used when working with astronomical... |
| [bio-analysis-system](skills/bioclaw/bio-analysis-system/) | `bioclaw` | — |
| [bio-batch-processing](skills/bioskills/batch-processing/) | `bioskills` | Process multiple sequence files in batch using Biopython. Use when working with many files, merging/splitting sequenc... |
| [bio-compressed-files](skills/bioskills/compressed-files/) | `bioskills` | Read and write compressed sequence files (gzip, bzip2, BGZF) using Biopython. Use when working with .gz or .bz2 seque... |
| [bio-filter-sequences](skills/bioskills/filter-sequences/) | `bioskills` | Filter and select sequences by criteria (length, ID, GC content, patterns) using Biopython. Use when subsetting seque... |
| [bio-flow-cytometry-compensation-transformation](skills/bioskills/compensation-transformation/) | `bioskills` | Spillover compensation and data transformation for flow cytometry. Covers compensation matrix calculation, applicatio... |
| [bio-flow-cytometry-doublet-detection](skills/bioskills/doublet-detection/) | `bioskills` | Detect and remove doublets from flow and mass cytometry data. Covers FSC/SSC gating and computational doublet detecti... |
| [bio-flow-cytometry-gating-analysis](skills/bioskills/gating-analysis/) | `bioskills` | Manual and automated gating for defining cell populations in flow cytometry. Covers rectangular, polygon, and data-dr... |
| [bio-hi-c-analysis-hic-data-io](skills/bioskills/hic-data-io/) | `bioskills` | Load, convert, and manipulate Hi-C contact matrices using cooler format. Read .cool/.mcool files, convert from .hic f... |
| [bio-hi-c-analysis-matrix-operations](skills/bioskills/matrix-operations/) | `bioskills` | Balance, normalize, and transform Hi-C contact matrices using cooler and cooltools. Apply iterative correction (ICE),... |
| [bio-imaging-mass-cytometry-data-preprocessing](skills/bioskills/data-preprocessing/) | `bioskills` | Load and preprocess imaging mass cytometry (IMC) and MIBI data. Covers MCD/TIFF handling, hot pixel removal, and imag... |
| [bio-imaging-mass-cytometry-quality-metrics](skills/bioskills/quality-metrics/) | `bioskills` | Quality metrics for IMC data including signal-to-noise, channel correlation, tissue integrity, and acquisition QC. Us... |
| [bio-orchestrator](skills/clawbio/bio-orchestrator/) | `clawbio` | Meta-agent that routes bioinformatics requests to specialised sub-skills. Handles file type detection, analysis |
| [bio-primer-design-primer-basics](skills/bioskills/primer-basics/) | `bioskills` | Design PCR primers for a target sequence using primer3-py. Specify target regions, product size, melting temperature,... |
| [bio-read-qc-quality-filtering](skills/bioskills/quality-filtering/) | `bioskills` | Filter reads by quality scores, length, and N content using Trimmomatic and fastp. Apply sliding window trimming, rem... |
| [bio-restriction-enzyme-selection](skills/bioskills/enzyme-selection/) | `bioskills` | Select restriction enzymes by criteria using Biopython Bio.Restriction. Find enzymes that cut once, don't cut, produc... |
| [bio-restriction-fragment-analysis](skills/bioskills/fragment-analysis/) | `bioskills` | Analyze restriction digest fragments using Biopython Bio.Restriction. Predict fragment sizes, get fragment sequences,... |
| [bio-ribo-seq-orf-detection](skills/bioskills/orf-detection/) | `bioskills` | Detect and quantify translated ORFs from Ribo-seq data including uORFs and novel ORFs using RiboCode and ORFquant. Us... |
| [bio-ribo-seq-ribosome-periodicity](skills/bioskills/ribosome-periodicity/) | `bioskills` | Validate Ribo-seq data quality by checking 3-nucleotide periodicity and calculating P-site offsets. Use when assessin... |
| [bio-seq-objects](skills/bioskills/seq-objects/) | `bioskills` | Create and manipulate Seq, MutableSeq, and SeqRecord objects using Biopython. Use when creating sequences from string... |
| [bio-sequence-properties](skills/bioskills/sequence-properties/) | `bioskills` | Calculate sequence properties like GC content, molecular weight, isoelectric point, and GC skew using Biopython. Use ... |
| [bio-sequence-slicing](skills/bioskills/sequence-slicing/) | `bioskills` | Slice, extract, and concatenate biological sequences using Biopython. Use when extracting subsequences, joining seque... |
| [bio-sequence-statistics](skills/bioskills/sequence-statistics/) | `bioskills` | Calculate sequence statistics (N50, length distribution, GC content, summary reports) using Biopython. Use when analy... |
| [bone-marrow-ai-agent](skills/openclaw/bone-marrow-ai-agent/) | `openclaw` | AI-powered bone marrow morphology analysis, cell classification, and hematologic disorder diagnosis using deep learni... |
| [chemistry-agent](skills/openclaw/chemistry-agent/) | `openclaw` | Autonomous chemical synthesis & analysis |
| [coagulation-thrombosis-agent](skills/openclaw/coagulation-thrombosis-agent/) | `openclaw` | AI-powered analysis of coagulation disorders, thrombosis risk prediction, anticoagulation management, and platelet fu... |
| [convergence-study](skills/openclaw/convergence-study/) | `openclaw` | Spatial and temporal convergence analysis with Richardson extrapolation and Grid Convergence Index (GCI) for solution... |
| [crisis-detection-intervention-ai](skills/openclaw/crisis-detection-intervention-ai/) | `openclaw` | Detect crisis signals in user content using NLP, mental health sentiment analysis, and safe intervention protocols. I... |
| [data-stats-analysis](skills/openclaw/data-stats-analysis/) | `openclaw` | Perform statistical tests, hypothesis testing, correlation analysis, and multiple testing corrections using scipy and... |
| [galaxy-bridge](skills/clawbio/galaxy-bridge/) | `clawbio` | Galaxy tool discovery, intelligent recommendation, and execution — 8,000+ bioinformatics tools from usegalaxy.org |
| [hrv-alexithymia-expert](skills/openclaw/hrv-alexithymia-expert/) | `openclaw` | Heart rate variability biometrics and emotional awareness training. Expert in HRV analysis, interoception training, b... |
| [hypogenic](skills/kdense/hypogenic/) | `kdense` | Automated LLM-driven hypothesis generation and testing on tabular datasets. Use when you want to systematically explo... |
| [illumina-bridge](skills/clawbio/illumina-bridge/) | `clawbio` | Import DRAGEN-exported Illumina result bundles into ClawBio for local tertiary analysis and downstream routing. |
| [iso-13485-certification](skills/kdense/iso-13485-certification/) | `kdense` | Comprehensive toolkit for preparing ISO 13485 certification documentation for medical device Quality Management Syste... |
| [jungian-psychologist](skills/openclaw/jungian-psychologist/) | `openclaw` | Expert in Jungian analytical psychology, depth psychology, shadow work, archetypal analysis, dream interpretation, ac... |
| [numerical-stability](skills/openclaw/numerical-stability/) | `openclaw` | Analyze and enforce numerical stability for time-dependent PDE simulations. Use when selecting time steps, choosing e... |
| [opencv-bioimage-analysis](skills/sciagent/opencv-bioimage-analysis/) | `sciagent` | Computer vision for bio-image preprocessing, feature detection, real-time microscopy. Color conversion, morphology, c... |
| [pathml](skills/kdense/pathml/) | `kdense` | Full-featured computational pathology toolkit. Use for advanced WSI analysis including multiplexed immunofluorescence... |
| [pdf](skills/openclaw/pdf-anthropic/) | `openclaw` | Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents... |
| [performance-profiling](skills/openclaw/performance-profiling/) | `openclaw` | Identify computational bottlenecks, analyze scaling behavior, estimate memory requirements, and receive optimization ... |
| [repro-enforcer](skills/clawbio/repro-enforcer/) | `clawbio` | Export any bioinformatics analysis as a reproducible bundle with Conda environment, Singularity container definition, |
| [sgrna-design-guide](skills/sciagent/sgrna-design-guide/) | `sciagent` | Three-tiered sgRNA design guide using validated Addgene sequences, CRISPick pre-computed datasets, or de novo design ... |
| [statsmodels](skills/kdense/statsmodels/) | `kdense` | Statistical models library for Python. Use when you need specific model classes (OLS, GLM, mixed models, ARIMA) with ... |
| [statsmodels-statistical-modeling](skills/sciagent/statsmodels-statistical-modeling/) | `sciagent` | Python statistical modeling: regression (OLS, WLS, GLM), discrete (Logit, Poisson, NegBin), time series (ARIMA, SARIM... |
| [survival-analysis](skills/zamushwani/survival-analysis/) | `zamushwani` | — |
| [tooluniverse-image-analysis](skills/openclaw/tooluniverse-image-analysis/) | `openclaw` | Production-ready microscopy image analysis and quantitative imaging data skill for colony morphometry, cell counting,... |
| [trackpy-particle-tracking](skills/sciagent/trackpy-particle-tracking/) | `sciagent` | Python library for single-particle tracking (SPT) in video microscopy via the Crocker-Grier algorithm. Locate particl... |
| [using-superpowers](skills/openclaw/using-superpowers/) | `openclaw` | Use when starting any conversation - establishes how to find and use skills, requiring Skill tool invocation before A... |
| [usmle](skills/openclaw/usmle/) | `openclaw` | Prepare for US medical licensing exams with progress tracking, weak area analysis, question bank management, and resi... |
| [wearable-analysis-agent](skills/openclaw/wearable-analysis-agent/) | `openclaw` | Analyzes longitudinal wearable sensor data (heart rate, activity, sleep) to detect anomalies and provide personalized... |

</details>

<br/>

## 📈 Visualization 可视化
<br/>

<details>
<summary><b>Click to expand · 点击展开 (38 skills)</b></summary>

| Skill | Source 来源 | Description 描述 |
|-------|-------------|------------------|
| [beautiful-data-viz](skills/omics/beautiful-data-viz/) | `omics` | Create publication-quality matplotlib/seaborn charts with readable axes, tight layout, and curated palettes. |
| [bio-copy-number-copy-ratio-segmentation](skills/bioskills/copy-ratio-segmentation/) | `bioskills` | Normalize read-depth copy-ratio profiles and segment them into copy-number regions using circular binary segmentation... |
| [bio-data-visualization-color-palettes](skills/bioskills/color-palettes/) | `bioskills` | Select colormaps and qualitative palettes for scientific figures using perceptual-uniformity, color-vision-deficiency... |
| [bio-data-visualization-forest-funnel-plots](skills/bioskills/forest-funnel-plots/) | `bioskills` | Build forest plots (HR, OR, RR, beta-coefficient summaries with CIs) and funnel plots (meta-analysis publication-bias... |
| [bio-data-visualization-interactive-visualization](skills/bioskills/interactive-visualization/) | `bioskills` | Build interactive HTML/web visualizations with plotly (Python/R), bokeh (Python), and gganimate/plotly frames for ani... |
| [bio-data-visualization-multipanel-figures](skills/bioskills/multipanel-figures/) | `bioskills` | Compose multi-panel publication figures with patchwork, cowplot, gridExtra (R), or matplotlib GridSpec/subfigures (Py... |
| [bio-data-visualization-statistical-annotation](skills/bioskills/statistical-annotation/) | `bioskills` | Add p-value brackets, significance asterisks, and effect-size annotations to distribution plots using ggpubr, ggsigni... |
| [bio-figure-design](skills/bioclaw/bio-figure-design/) | `bioclaw` | — |
| [bio-phylo-tree-visualization](skills/bioskills/tree-visualization/) | `bioskills` | Draw and export phylogenetic trees using Biopython Bio.Phylo with matplotlib and modern alternatives. Use when creati... |
| [bio-primer-design-qpcr-primers](skills/bioskills/qpcr-primers/) | `bioskills` | Design qPCR primers and TaqMan/molecular beacon probes using primer3-py. Configure probe Tm, primer-probe spacing, an... |
| [bio-reporting-figure-export](skills/bioskills/figure-export/) | `bioskills` | Exports publication-ready figures in various formats with proper resolution, sizing, and typography. Use when prepari... |
| [bio-reporting-rmarkdown-reports](skills/bioskills/rmarkdown-reports/) | `bioskills` | Create reproducible bioinformatics analysis reports with R Markdown including code, results, and visualizations in HT... |
| [bio-tcr-bcr-analysis-repertoire-visualization](skills/bioskills/repertoire-visualization/) | `bioskills` | Create publication-quality visualizations of immune repertoire data including circos plots, clone tracking, diversity... |
| [bio-workflows-hic-pipeline](skills/bioskills/hic-pipeline/) | `bioskills` | End-to-end Hi-C analysis workflow from contact pairs to compartments, TADs, and loops. Covers cooler matrices, coolto... |
| [cell-figure-guide](skills/sciagent/cell-figure-guide/) | `sciagent` | Cell (Cell Press) figure preparation: resolution (300-1000 DPI), formats (TIFF/PDF), RGB color, Avenir/Arial fonts, u... |
| [data-visualization-expert](skills/openclaw/data-visualization-expert/) | `openclaw` | Generate insightful, publication-quality visualizations from complex datasets. |
| [data-viz-plots](skills/openclaw/data-viz-plots/) | `openclaw` | Create publication-quality plots and visualizations using matplotlib and seaborn. Works with ANY LLM provider (GPT, G... |
| [general-figure-guide](skills/sciagent/general-figure-guide/) | `sciagent` | Universal QA checklist for generated scientific plots: overlapping labels, clipped text, missing axes/legends, overcr... |
| [linear-solvers](skills/openclaw/linear-solvers/) | `openclaw` | Select and configure linear solvers for systems Ax=b in dense and sparse problems. Use when choosing direct vs iterat... |
| [markdown-mermaid-writing](skills/openclaw/markdown-mermaid-writing/) | `openclaw` | Comprehensive markdown and Mermaid diagram writing skill. Use when creating any scientific document, report, analysis... |
| [matplotlib-scientific-plotting](skills/sciagent/matplotlib-scientific-plotting/) | `sciagent` | Low-level Python plotting for scientific figures: publication-quality line, scatter, bar, heatmap, contour, 3D; multi... |
| [napari-image-viewer](skills/sciagent/napari-image-viewer/) | `sciagent` | Interactive viewer for microscopy. Displays 2D/3D/4D arrays as Image, Labels, Points, Shapes, Tracks layers; supports... |
| [networkx-graph-analysis](skills/sciagent/networkx-graph-analysis/) | `sciagent` | Graph and network analysis toolkit. Four graph types (directed, undirected, multi-edge), centrality, shortest paths, ... |
| [neuropixels-analysis](skills/kdense/neuropixels-analysis/) | `kdense` | Neuropixels neural recording analysis. Load SpikeGLX/OpenEphys data, preprocess, motion correction, Kilosort4 spike s... |
| [notebooks](skills/omics/notebooks/) | `omics` | Author, execute, and deliver reproducible analysis notebooks in marimo (default) or Jupyter, with all cells run end-t... |
| [plotly](skills/openclaw/plotly/) | `openclaw` | Interactive visualization library. Use when you need hover info, zoom, pan, or web-embeddable charts. Best for dashbo... |
| [plotly-dashboard-skill](skills/omics/plotly-dashboard-skill/) | `omics` | Build production-ready Plotly Dash dashboards with consistent theming, clear layouts, and performant callbacks. |
| [post-processing](skills/openclaw/post-processing/) | `openclaw` | Extract, analyze, and visualize simulation output data. Use for field extraction, time series analysis, line profiles... |
| [pyimagej-fiji-bridge](skills/sciagent/pyimagej-fiji-bridge/) | `sciagent` | Python bridge to ImageJ2/Fiji for macros, plugins (Bio-Formats, TrackMate, Analyze Particles), NumPy↔ImagePlus/ImgLib... |
| [pytorch-lightning](skills/openclaw/pytorch-lightning/) | `openclaw` | Deep learning framework (PyTorch Lightning). Organize PyTorch code into LightningModules, configure Trainers for mult... |
| [report-template](skills/bioclaw/report-template/) | `bioclaw` | Publication-quality PDF report generation using Typst templates. Produces professional scientific reports with colore... |
| [reporting-and-figure-export](skills/bioclaw_hub/reporting-and-figure-export/) | `bioclaw_hub` | Workflow for packaging analysis outputs into reproducible reports, clean tables, and publication-ready figure exports. |
| [scientific-visualization](skills/kdense/scientific-visualization/) | `kdense` | Meta-skill for publication-ready figures. Use when creating journal submission figures requiring multi-panel layouts,... |
| [scikit-image-processing](skills/sciagent/scikit-image-processing/) | `sciagent` | Python image processing for microscopy and bioimage analysis. Read/write images, filter (Gaussian, median, LoG), segm... |
| [shap](skills/kdense/shap/) | `kdense` | Model interpretability and explainability using SHAP (SHapley Additive exPlanations). Use this skill when explaining ... |
| [speech-pathology-ai](skills/openclaw/speech-pathology-ai/) | `openclaw` | Expert speech-language pathologist specializing in AI-powered speech therapy, phoneme analysis, articulation visualiz... |
| [statistical-significance-annotation](skills/sciagent/statistical-significance-annotation/) | `sciagent` | Guide for annotating statistical significance (p-value asterisks) on comparison plots. Covers standard notation (ns, ... |
| [vaex](skills/openclaw/vaex/) | `openclaw` | Use this skill for processing and analyzing large tabular datasets (billions of rows) that exceed available RAM. Vaex... |

</details>

<br/>

## ⚙️ Workflow 流程编排
<br/>

<details>
<summary><b>Click to expand · 点击展开 (31 skills)</b></summary>

| Skill | Source 来源 | Description 描述 |
|-------|-------------|------------------|
| [bio-manuscript-pipeline](skills/bioclaw/bio-manuscript-pipeline/) | `bioclaw` | — |
| [bio-reporting-jupyter-reports](skills/bioskills/jupyter-reports/) | `bioskills` | Creates reproducible Jupyter notebooks for bioinformatics analysis with parameterization using papermill. Use when ge... |
| [bio-workflow-management-cwl-workflows](skills/bioskills/cwl-workflows/) | `bioskills` | Create portable, standards-based bioinformatics pipelines with Common Workflow Language (CWL). Use when building work... |
| [bio-workflow-management-nextflow-pipelines](skills/bioskills/nextflow-pipelines/) | `bioskills` | Create scalable, containerized bioinformatics pipelines with Nextflow DSL2 supporting Docker, Singularity, and cloud ... |
| [bio-workflow-management-snakemake-workflows](skills/bioskills/snakemake-workflows/) | `bioskills` | Build reproducible bioinformatics pipelines with Snakemake using rules, wildcards, and automatic dependency resolutio... |
| [bio-workflow-management-wdl-workflows](skills/bioskills/wdl-workflows/) | `bioskills` | Create portable bioinformatics pipelines with Workflow Description Language (WDL) using Cromwell or miniwdl execution... |
| [bio-workflow-methods-docwriter](skills/omics/bio-workflow-methods-docwriter/) | `omics` | Generate reproducible Methods documentation from workflow run artifacts (Nextflow/Snakemake/CWL), including exact com... |
| [bio-workflows-crispr-editing-pipeline](skills/bioskills/crispr-editing-pipeline/) | `bioskills` | End-to-end CRISPR experiment design from target selection to delivery-ready constructs. Covers guide RNA design, off-... |
| [bio-workflows-cytometry-pipeline](skills/bioskills/cytometry-pipeline/) | `bioskills` | End-to-end flow cytometry workflow from FCS files to differential analysis. Orchestrates compensation, transformation... |
| [bio-workflows-imc-pipeline](skills/bioskills/imc-pipeline/) | `bioskills` | End-to-end imaging mass cytometry workflow from raw acquisitions to spatial cell analysis. Orchestrates image preproc... |
| [bioconductor-bridge](skills/clawbio/bioconductor-bridge/) | `clawbio` | Bioconductor package discovery, workflow recommendation, setup inspection, and starter code generation grounded |
| [biomaster-workflows](skills/openclaw/biomaster-workflows/) | `openclaw` | Pipeline maestro |
| [care-coordination](skills/openclaw/care-coordination/) | `openclaw` | Care Coordination agent for healthcare workflows. |
| [claims-appeals](skills/openclaw/claims-appeals/) | `openclaw` | Claims Appeals agent for healthcare workflows. |
| [fhir-development](skills/openclaw/fhir-development/) | `openclaw` | FHIR Development agent for healthcare workflows. |
| [histolab-wsi-processing](skills/sciagent/histolab-wsi-processing/) | `sciagent` | WSI processing for digital pathology. Tissue detection, tile extraction (random, grid, score-based), filter pipelines... |
| [instrument-data-to-allotrope](skills/openclaw/instrument-data-to-allotrope/) | `openclaw` | Convert laboratory instrument output files (PDF, CSV, Excel, TXT) to Allotrope Simple Model (ASM) JSON format or flat... |
| [lab-results](skills/openclaw/lab-results/) | `openclaw` | Lab Results agent for healthcare workflows. |
| [nextflow-workflow-engine](skills/sciagent/nextflow-workflow-engine/) | `sciagent` | Dataflow workflow engine for scalable bioinformatics pipelines. Defines processes (containerized tasks) connected by ... |
| [pdf-processing-pro](skills/openclaw/pdf-processing-pro/) | `openclaw` | Production-ready PDF processing with forms, tables, OCR, validation, and batch operations. Use when working with comp... |
| [polars](skills/kdense/polars/) | `kdense` | Fast in-memory DataFrame library for datasets that fit in RAM. Use when pandas is too slow but data still fits in mem... |
| [pydicom](skills/kdense/pydicom/) | `kdense` | Python library for working with DICOM (Digital Imaging and Communications in Medicine) files. Use this skill when rea... |
| [pylabrobot](skills/sciagent/pylabrobot/) | `sciagent` | Hardware-agnostic Python liquid-handler library: portable scripts run on Hamilton STAR, Tecan Freedom EVO, Opentrons ... |
| [regulatory-drafting](skills/openclaw/regulatory-drafting/) | `openclaw` | Regulatory Drafting agent for healthcare workflows. |
| [scikit-learn](skills/openclaw/scikit-learn/) | `openclaw` | Machine learning in Python with scikit-learn. Use when working with supervised learning (classification, regression),... |
| [scikit-survival](skills/kdense/scikit-survival/) | `kdense` | Comprehensive toolkit for survival analysis and time-to-event modeling in Python using scikit-survival. Use this skil... |
| [sequence-and-format-io](skills/bioclaw_hub/sequence-and-format-io/) | `bioclaw_hub` | Workflow for foundational sequence parsing, conversion, compression handling, and interval-aware file validation. |
| [simulation-orchestrator](skills/openclaw/simulation-orchestrator/) | `openclaw` | Orchestrate multi-simulation campaigns including parameter sweeps, batch jobs, and result aggregation. Use for runnin... |
| [single-trajectory-analysis](skills/openclaw/single-trajectory/) | `openclaw` | Guide to reproducing OmicVerse trajectory workflows spanning PAGA, Palantir, VIA, velocity coupling, and fate scoring... |
| [skills-hub](skills/bioclaw/skills-hub/) | `bioclaw` | Browse and install community skills from the BioClaw Skills Hub. Use when a user's task is not covered by built-in sk... |
| [spikeinterface-electrophysiology](skills/sciagent/spikeinterface-electrophysiology/) | `sciagent` | Unified Python framework for extracellular electrophysiology. Load 20+ formats (SpikeGLX, OpenEphys, NWB, Intan, Maxw... |

</details>

<br/>

## 🧫 Epigenomics 表观组学
<br/>

<details>
<summary><b>Click to expand · 点击展开 (19 skills)</b></summary>

| Skill | Source 来源 | Description 描述 |
|-------|-------------|------------------|
| [atac-seq](skills/bioclaw/atac-seq/) | `bioclaw` | ATAC-seq processing with assay QC, MACS3 peak calling, consensus peak matrices, differential accessibility, and motif... |
| [bio-atac-seq-atac-qc](skills/bioskills/atac-qc/) | `bioskills` | ATAC-seq library quality control -- TSS enrichment, FRiP, fragment-size periodicity, library complexity (NRF/PBC1/PBC... |
| [bio-atac-seq-footprinting](skills/bioskills/footprinting/) | `bioskills` | Detect transcription factor binding footprints in ATAC-seq using TOBIAS, HINT-ATAC, Wellington, or scprinter. Use whe... |
| [bio-chipseq-cut-and-run-tag](skills/bioskills/cut-and-run-tag/) | `bioskills` | Analyzes CUT&RUN (Skene Henikoff 2017) and CUT&Tag (Kaya-Okur 2019) chromatin profiling data. Handles SEACR vs MACS2 ... |
| [bio-chipseq-motif-analysis](skills/bioskills/motif-analysis/) | `bioskills` | Discovers de novo motifs and tests known motif enrichment in ChIP-seq, ATAC-seq, or other peak sequences using HOMER,... |
| [bio-chipseq-qc](skills/bioskills/chipseq-qc/) | `bioskills` | Assesses ChIP-seq quality across antibody specificity, fragmentation, enrichment, replicate concordance, and library ... |
| [bio-chipseq-super-enhancers](skills/bioskills/super-enhancers/) | `bioskills` | Identifies super-enhancers from H3K27ac, MED1, or BRD4 ChIP-seq using ROSE, ROSE2, LILY, HOMER -style super, and ENCO... |
| [bio-clip-seq-clip-motif-analysis](skills/bioskills/clip-motif-analysis/) | `bioskills` | Discover RBP binding motifs from CLIP-seq peaks or single-nucleotide crosslink sites using HOMER, MEME/STREME, kpLogo... |
| [bio-clip-seq-clip-qc](skills/bioskills/clip-qc/) | `bioskills` | Comprehensive quality control for CLIP-seq libraries (eCLIP, iCLIP, iCLIP2, PAR-CLIP) covering library complexity (pr... |
| [bio-copy-number-recurrent-cnv](skills/bioskills/recurrent-cnv/) | `bioskills` | Identify recurrent and driver copy number alterations across a tumor cohort with GISTIC2 (G-score, Ziggurat deconstru... |
| [bio-hi-c-analysis-compartment-analysis](skills/bioskills/compartment-analysis/) | `bioskills` | Detect A/B compartments from Hi-C data using cooltools and eigenvector decomposition. Identify active (A) and inactiv... |
| [bio-hi-c-analysis-loop-calling](skills/bioskills/loop-calling/) | `bioskills` | Detect chromatin loops and point interactions from Hi-C data using cooltools, chromosight, and HiCCUPS-like methods. ... |
| [bio-long-read-sequencing-nanopore-methylation](skills/bioskills/nanopore-methylation/) | `bioskills` | Calls DNA methylation from Oxford Nanopore sequencing data using signal-level analysis. Use when detecting 5mC or 6mA... |
| [bio-methylation-based-detection](skills/bioskills/methylation-based-detection/) | `bioskills` | Analyzes cfDNA methylation patterns for cancer detection using cfMeDIP-seq or bisulfite sequencing with MethylDackel.... |
| [chip-seq](skills/bioclaw/chip-seq/) | `bioclaw` | ChIP-seq peak calling and downstream interpretation with MACS3, signal track export, annotation, motif analysis, and ... |
| [methylation-clock](skills/clawbio/methylation-clock/) | `clawbio` | Compute epigenetic age from DNA methylation arrays using PyAging clocks from GEO accessions or local files. |
| [methylation-cycle](skills/clawbio/claw-methylation-cycle/) | `clawbio` | — |
| [open-notebook](skills/kdense/open-notebook/) | `kdense` | Self-hosted, open-source alternative to Google NotebookLM for AI-powered research and document analysis. Use when org... |
| [pptx](skills/openclaw/pptx-official/) | `openclaw` | Presentation creation, editing, and analysis. When Claude needs to work with presentations (.pptx files) for: (1) Cre... |

</details>

<br/>

## 🌿 Pathway 通路分析
<br/>

<details>
<summary><b>Click to expand · 点击展开 (13 skills)</b></summary>

| Skill | Source 来源 | Description 描述 |
|-------|-------------|------------------|
| [bio-pathway-enrichment-visualization](skills/bioskills/enrichment-visualization/) | `bioskills` | Visualize enrichment results using enrichplot package functions. Use when creating publication-quality figures from c... |
| [bio-pathway-kegg-pathways](skills/bioskills/kegg-pathways/) | `bioskills` | KEGG pathway and module enrichment analysis using clusterProfiler enrichKEGG and enrichMKEGG. Use when identifying me... |
| [bio-pathway-reactome](skills/bioskills/reactome-pathways/) | `bioskills` | Reactome pathway enrichment using ReactomePA package. Use when analyzing gene lists against Reactome's curated peer-r... |
| [bio-pathway-wikipathways](skills/bioskills/wikipathways/) | `bioskills` | WikiPathways enrichment using clusterProfiler and rWikiPathways. Use when analyzing gene lists against community-cura... |
| [generate-image](skills/kdense/generate-image/) | `kdense` | Generate or edit images using AI models (FLUX, Nano Banana 2). Use for general-purpose image generation including pho... |
| [gsea-enrichment-analysis](skills/openclaw/gsea-enrichment/) | `openclaw` | Gene set enrichment analysis with correct geneset format handling. Critical guidance for loading pathway databases an... |
| [ontology-explorer](skills/openclaw/ontology-explorer/) | `openclaw` | > |
| [ontology-mapper](skills/openclaw/ontology-mapper/) | `openclaw` | > |
| [ontology-validator](skills/openclaw/ontology-validator/) | `openclaw` | > |
| [query-kegg](skills/bioclaw/query-kegg/) | `bioclaw` | Query KEGG for biological pathways and gene info. Use when user asks about metabolic pathways, signaling pathways, pa... |
| [query-reactome](skills/bioclaw/query-reactome/) | `bioclaw` | Query Reactome for biological pathways and reactions. Use when user asks about signaling cascades, biological process... |
| [scientific-schematics](skills/kdense/scientific-schematics/) | `kdense` | Create publication-quality scientific diagrams using Nano Banana 2 AI with smart iterative refinement. Uses Gemini 3.... |
| [tooluniverse-gene-enrichment](skills/openclaw/tooluniverse-gene-enrichment/) | `openclaw` | Perform comprehensive gene enrichment and pathway analysis using gseapy (ORA and GSEA), PANTHER, STRING, Reactome, an... |

</details>

<br/>

## 🦠 Metagenomics 宏基因组
<br/>

<details>
<summary><b>Click to expand · 点击展开 (8 skills)</b></summary>

| Skill | Source 来源 | Description 描述 |
|-------|-------------|------------------|
| [bio-annotation](skills/omics/bio-annotation/) | `omics` | Functional annotation and taxonomy inference from sequence homology. |
| [bio-blast-searches](skills/bioskills/blast-searches/) | `bioskills` | Run remote BLAST searches against NCBI servers using Biopython Bio.Blast.NCBIWWW. Use when identifying unknown sequen... |
| [bio-crispr-screens-screen-qc](skills/bioskills/screen-qc/) | `bioskills` | Quality control for pooled CRISPR screens covering library representation, Gini index, log-skew, replicate Pearson an... |
| [bio-microbiome-differential-abundance](skills/bioskills/differential-abundance/) | `bioskills` | Differential abundance testing for microbiome data using compositionally-aware methods like ALDEx2, ANCOM-BC2, and Ma... |
| [bio-microbiome-qiime2-workflow](skills/bioskills/qiime2-workflow/) | `bioskills` | QIIME2 command-line workflow for 16S/ITS amplicon analysis. Alternative to DADA2/phyloseq R workflow with built-in pr... |
| [bio-microbiome-taxonomy-assignment](skills/bioskills/taxonomy-assignment/) | `bioskills` | Taxonomic classification of ASVs using reference databases like SILVA, GTDB, or UNITE. Covers naive Bayes classifiers... |
| [microbiome-cancer-agent](skills/openclaw/microbiome-cancer-agent/) | `openclaw` | AI-powered analysis of microbiome-cancer interactions including tumor microbiome profiling, immunotherapy response pr... |
| [tracking-taxonomy-updates](skills/omics/tracking-taxonomy-updates/) | `omics` | Track and reconcile taxonomy updates across NCBI, GTDB, ICTV, and community eukaryote frameworks with versioned prove... |

</details>

<br/>

## 🧩 Protein Design 蛋白质设计
<br/>

<details>
<summary><b>Click to expand · 点击展开 (6 skills)</b></summary>

| Skill | Source 来源 | Description 描述 |
|-------|-------------|------------------|
| [bio-clip-seq-m6a-clip](skills/bioskills/m6a-clip/) | `bioskills` | Map N6-methyladenosine (m6A) RNA modifications at single-nucleotide resolution using miCLIP (Linder 2015), miCLIP2 + ... |
| [bio-tcr-bcr-analysis-immcantation-analysis](skills/bioskills/immcantation-analysis/) | `bioskills` | Analyze BCR repertoires for somatic hypermutation, clonal lineages, and B cell phylogenetics using the Immcantation f... |
| [ligandmpnn](skills/adaptyv/ligandmpnn/) | `adaptyv` | > |
| [mage-antibody-generator](skills/openclaw/MAGE/) | `openclaw` | Ab seq forge |
| [rfdiffusion](skills/adaptyv/rfdiffusion/) | `adaptyv` | > |
| [solublempnn](skills/adaptyv/solublempnn/) | `adaptyv` | > |

</details>

<br/>

---

<div align="center">

**1306 Skills · 11 Sources · 15 Categories**

*Aggregated with ❤️ for the biomedical AI community · 为生物医学 AI 社区整合*

</div>
