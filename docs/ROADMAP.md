# 🗺️ 分析场景路线图 · Analysis Scenario Roadmap

> 按分析任务选择对应路线，每条路线列出推荐的 skill 使用顺序与关键注意事项。
> *Choose a scenario below — each roadmap lists recommended skills in order with key tips.*

---

## 场景列表 · Scenarios

1. [🧬 RNA-seq 差异表达分析](#-rna-seq-差异表达分析)
2. [🔵 单细胞 RNA-seq 分析](#-单细胞-rna-seq-分析)
3. [🧬 WGS 变异分析](#-wgs-变异分析)
4. [🧩 蛋白质设计](#-蛋白质设计)
5. [🦠 宏基因组分析](#-宏基因组分析)
6. [💊 药物发现](#-药物发现)
7. [🏥 临床/EHR 分析](#-临床ehr-分析)

---

## 🧬 RNA-seq 差异表达分析
*Bulk RNA-seq Differential Expression*

**目标 Goal:** 从原始 FASTQ 到差异基因列表、通路富集结果  
*From raw FASTQ to differential gene list and pathway enrichment*

| 步骤 | Skill | 来源 | 说明 |
|------|-------|------|------|
| 1️⃣ 质控 QC | [`fastq-quality`](../skills/bioskills/fastq-quality) | `bioskills` | FastQC/fastp 原始数据质控 |
| 2️⃣ 比对 Alignment | [`hisat2-alignment`](../skills/bioskills/hisat2-alignment) | `bioskills` | HISAT2 剪接感知比对到参考基因组 |
| 3️⃣ 计数 Counting | [`featurecounts-counting`](../skills/bioskills/featurecounts-counting) | `bioskills` | featureCounts 生成基因计数矩阵 |
| 4️⃣ 差异分析 DE | [`deseq2-basics`](../skills/bioskills/deseq2-basics) | `bioskills` | DESeq2 差异表达分析（推荐） |
| 4️⃣ 差异分析 DE (alt) | [`edger-basics`](../skills/bioskills/edger-basics) | `bioskills` | edgeR 差异表达（小样本量替代方案） |
| 5️⃣ 可视化 Viz | [`de-visualization`](../skills/bioskills/de-visualization) | `bioskills` | 火山图、热图、PCA 可视化 |
| 6️⃣ 通路富集 Enrichment | [`gsea`](../skills/bioskills/gsea) | `bioskills` | GSEA 基因集富集分析 |
| 6️⃣ GO 富集 (alt) | [`go-enrichment`](../skills/bioskills/go-enrichment) | `bioskills` | GO/KEGG ORA 富集分析 |

> 💡 **Tips:** DESeq2 适合大多数场景；样本量 < 5 时考虑 edgeR。比对前务必确认参考基因组版本与 GTF 注释版本一致。

---

## 🔵 单细胞 RNA-seq 分析
*Single-Cell RNA-seq Analysis*

**目标 Goal:** 从 10x Genomics 数据到细胞类型注释、轨迹推断  
*From 10x Genomics data to cell type annotation and trajectory inference*

| 步骤 | Skill | 来源 | 说明 |
|------|-------|------|------|
| 1️⃣ 数据加载 Load | [`data-io`](../skills/bioskills/data-io) | `bioskills` | 加载 10x/h5ad 数据，Scanpy/Seurat 双语言 |
| 2️⃣ 双细胞过滤 Doublet | [`doublet-detection`](../skills/bioskills/doublet-detection) | `bioskills` | Scrublet/DoubletFinder 去除双细胞 |
| 3️⃣ 批次整合 Batch | [`batch-integration`](../skills/bioskills/batch-integration) | `bioskills` | Harmony 批次效应校正 |
| 4️⃣ 聚类 Clustering | [`clustering`](../skills/bioskills/clustering) | `bioskills` | Leiden 聚类，分辨率参数调优 |
| 5️⃣ 细胞注释 Annotation | [`cell-annotation`](../skills/bioskills/cell-annotation) | `bioskills` | CellTypist/SingleR 自动注释 |
| 6️⃣ 细胞通讯 Communication | [`cell-communication`](../skills/bioskills/cell-communication) | `bioskills` | CellChat/LIANA 配体受体分析 |
| 7️⃣ 轨迹推断 Trajectory | [`trajectory-inference`](../skills/bioskills/trajectory-inference) | `bioskills` | Monocle3/scVelo 发育轨迹 |
| 8️⃣ 空间组学 Spatial | [`tooluniverse-spatial-omics-analysis`](../skills/openclaw/tooluniverse-spatial-omics-analysis) | `openclaw` | Visium/Xenium 空间转录组分析 |

> 💡 **Tips:** 建议先用 Scanpy（Python）做探索性分析，再用 Seurat（R）做发表级图表。批次整合放在聚类之前。

---

## 🧬 WGS 变异分析
*Whole Genome Sequencing Variant Analysis*

**目标 Goal:** 从 FASTQ 到变异注释、GWAS 关联分析  
*From FASTQ to variant annotation and GWAS association*

| 步骤 | Skill | 来源 | 说明 |
|------|-------|------|------|
| 1️⃣ 比对 Alignment | [`bwa-alignment`](../skills/bioskills/bwa-alignment) | `bioskills` | BWA-MEM2 比对到参考基因组 |
| 2️⃣ 变异检测 Calling | [`gatk-variant-calling`](../skills/bioskills/gatk-variant-calling) | `bioskills` | GATK HaplotypeCaller 变异检测 |
| 2️⃣ 深度学习 (alt) | [`deepvariant`](../skills/bioskills/deepvariant) | `bioskills` | DeepVariant（长读长/高精度场景） |
| 3️⃣ 频率过滤 Filter | [`gnomad-frequencies`](../skills/bioskills/gnomad-frequencies) | `bioskills` | gnomAD 人群频率查询与过滤 |
| 4️⃣ 致病性注释 Pathogenicity | [`clinvar-lookup`](../skills/bioskills/clinvar-lookup) | `bioskills` | ClinVar 临床意义查询 |
| 5️⃣ GWAS 关联 | [`gwas-pipeline`](../skills/bioskills/gwas-pipeline) | `bioskills` | PLINK2 全基因组关联分析 |
| 6️⃣ 精细定位 Fine-mapping | [`fine-mapping`](../skills/bioskills/fine-mapping) | `bioskills` | SuSiE 因果变异精细定位 |

> 💡 **Tips:** 短读长用 BWA-MEM2 + GATK；长读长（ONT/PacBio）用 minimap2 + DeepVariant。GWAS 前务必做人群分层校正（PCA）。

---

## 🧩 蛋白质设计
*Protein Design & Engineering*

**目标 Goal:** 从靶点结构到设计序列、质量评估  
*From target structure to designed sequences and quality assessment*

| 步骤 | Skill | 来源 | 说明 |
|------|-------|------|------|
| 1️⃣ 结构预测 Structure | [`alphafold`](../skills/adaptyv/alphafold) | `adaptyv` | AlphaFold2 结构预测（无实验结构时） |
| 1️⃣ 结构预测 (alt) | [`boltz`](../skills/adaptyv/boltz) | `adaptyv` | Boltz-1 开源替代，速度更快 |
| 2️⃣ 骨架生成 Backbone | [`rfdiffusion`](../skills/adaptyv/rfdiffusion) | `adaptyv` | RFDiffusion 从头生成蛋白质骨架 |
| 3️⃣ 序列设计 Sequence | [`proteinmpnn`](../skills/adaptyv/proteinmpnn) | `adaptyv` | ProteinMPNN 在骨架上设计序列 |
| 4️⃣ Binder 设计 | [`binder-design`](../skills/adaptyv/binder-design) | `adaptyv` | Binder 设计工具链选择指南 |
| 5️⃣ 质量评估 QC | [`protein-qc`](../skills/adaptyv/protein-qc) | `adaptyv` | 结构/表达/结合亲和力综合评分 |

> 💡 **Tips:** 标准流程：AlphaFold 预测靶点结构 → RFDiffusion 生成 binder 骨架 → ProteinMPNN 设计序列 → AlphaFold 验证复合物结构。

---

## 🦠 宏基因组分析
*Metagenomics Analysis*

**目标 Goal:** 从测序数据到物种组成、功能注释、多样性分析  
*From sequencing data to taxonomic composition, functional annotation, and diversity*

| 步骤 | Skill | 来源 | 说明 |
|------|-------|------|------|
| 1️⃣ 物种分类 Taxonomy | [`kraken-classification`](../skills/bioskills/kraken-classification) | `bioskills` | Kraken2 宏基因组物种分类 |
| 2️⃣ 丰度估计 Abundance | [`metaphlan-profiling`](../skills/bioskills/metaphlan-profiling) | `bioskills` | MetaPhlAn4 物种相对丰度谱 |
| 3️⃣ 16S 扩增子 | [`amplicon-processing`](../skills/bioskills/amplicon-processing) | `bioskills` | DADA2 16S/ITS ASV 分析 |
| 4️⃣ 多样性分析 Diversity | [`diversity-analysis`](../skills/bioskills/diversity-analysis) | `bioskills` | Alpha/Beta 多样性，phyloseq |
| 5️⃣ 组装 Assembly | [`metagenome-assembly`](../skills/bioskills/metagenome-assembly) | `bioskills` | MEGAHIT/metaSPAdes 宏基因组组装 |

> 💡 **Tips:** 鸟枪法宏基因组用 Kraken2 + MetaPhlAn；16S 扩增子用 DADA2。多样性分析前注意样本深度标准化（rarefaction）。

---

## 💊 药物发现
*Drug Discovery*

**目标 Goal:** 从靶点发现到候选分子筛选、安全性评估  
*From target identification to candidate molecule screening and safety assessment*

| 步骤 | Skill | 来源 | 说明 |
|------|-------|------|------|
| 1️⃣ 靶点发现 Target ID | [`tooluniverse-target-research`](../skills/openclaw/tooluniverse-target-research) | `openclaw` | OpenTargets + 文献证据靶点发现 |
| 2️⃣ 药物研究 Drug Profile | [`tooluniverse-drug-research`](../skills/openclaw/tooluniverse-drug-research) | `openclaw` | 全面药物研究报告：药理/靶点/临床 |
| 3️⃣ 分子描述符 Descriptors | [`molecular-descriptors`](../skills/bioskills/molecular-descriptors) | `bioskills` | RDKit 分子描述符，虚拟筛选特征 |
| 4️⃣ 分子生成 Generation | [`generative-design`](../skills/bioskills/generative-design) | `bioskills` | REINVENT 生成式分子设计 |
| 5️⃣ ADMET 预测 | [`admet-prediction`](../skills/bioskills/admet-prediction) | `bioskills` | ADMET 性质预测，成药性评估 |
| 6️⃣ 安全性 Safety | [`tooluniverse-adverse-event-detection`](../skills/openclaw/tooluniverse-adverse-event-detection) | `openclaw` | FDA FAERS 不良事件信号检测 |

> 💡 **Tips:** 靶点发现后先做 druggability 评估（结合口袋分析），再进入分子设计。ADMET 预测应在虚拟筛选后、合成前完成。

---

## 🏥 临床/EHR 分析
*Clinical & EHR Analysis*

**目标 Goal:** 从电子病历到临床预测模型、精准医学方案  
*From EHR data to clinical prediction models and precision medicine*

| 步骤 | Skill | 来源 | 说明 |
|------|-------|------|------|
| 1️⃣ 临床试验检索 | [`clinicaltrials-database`](../skills/openclaw/clinicaltrials-database) | `openclaw` | ClinicalTrials.gov API 检索与导出 |
| 2️⃣ 患者匹配 Matching | [`tooluniverse-clinical-trial-matching`](../skills/openclaw/tooluniverse-clinical-trial-matching) | `openclaw` | 患者-试验多维度匹配 |
| 3️⃣ 生存分析 Survival | [`survival-analysis`](../skills/bioskills/survival-analysis) | `bioskills` | Kaplan-Meier + Cox 回归生存分析 |
| 4️⃣ 生物标志物 Biomarker | [`biomarker-discovery`](../skills/bioskills/biomarker-discovery) | `bioskills` | LASSO/Boruta 生物标志物发现 |
| 5️⃣ 罕见病诊断 | [`tooluniverse-rare-disease-diagnosis`](../skills/openclaw/tooluniverse-rare-disease-diagnosis) | `openclaw` | HPO 表型匹配 + 基因组变异解读 |
| 6️⃣ 精准医学 Precision | [`tooluniverse-precision-medicine-stratification`](../skills/openclaw/tooluniverse-precision-medicine-stratification) | `openclaw` | 精准医学患者分层：生物标志物整合 |

> 💡 **Tips:** EHR 数据预处理是关键：ICD 编码标准化、缺失值处理、时序特征提取。生存分析前检验 PH 假设（Schoenfeld 残差）。

---

<div align="center">

*7 scenarios · 50+ skill recommendations · Start from any step*

[← Back to main README](../README.md)

</div>
