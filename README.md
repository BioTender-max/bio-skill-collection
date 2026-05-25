<div align="center">

<img src="https://raw.githubusercontent.com/BioTender-max/bio-skill-collection/main/assets/banner.png" alt="Bio Skill Collection" width="100%"/>

<br/>

[![Skills](https://img.shields.io/badge/Skills-1306-00d4aa?style=for-the-badge&logo=databricks&logoColor=white)](https://github.com/BioTender-max/bio-skill-collection/tree/main/skills)
[![Sources](https://img.shields.io/badge/Sources-11_Repos-0079d3?style=for-the-badge&logo=github&logoColor=white)](https://github.com/BioTender-max/bio-skill-collection#整合来源)
[![Categories](https://img.shields.io/badge/Categories-15-7c3aed?style=for-the-badge&logo=buffer&logoColor=white)](https://github.com/BioTender-max/bio-skill-collection#能力覆盖)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

<h3>全网最大生物医学 AI Agent 技能合集</h3>
<p><em>The largest open-source biomedical AI agent skill collection — 1306 curated skills from 11 top repositories</em></p>

</div>

---

## 🧬 关于本仓库 · About

本仓库系统性地整合了 GitHub 上所有主流生物医学 AI Agent 技能仓库，经过去重与质量筛选，形成覆盖**基因组学、蛋白质组学、单细胞、临床医学、蛋白质设计**等 15 大类的完整技能集合。每个 skill 是一个独立文件夹，包含 `SKILL.md` 技能定义及附属示例代码与参考文档，可直接加载到支持 SKILL.md 格式的 Claude Agent 框架中使用。

> This repository aggregates and deduplicates biomedical AI agent skills from 11 open-source repositories across GitHub, covering the full spectrum of bioinformatics, clinical research, and protein design. Each skill is a self-contained folder with a `SKILL.md` definition, ready to load into any Claude-based agent framework.

---

## ⚡ 能力覆盖 · Coverage

| 类别 | Skills | 涵盖方向 |
|------|:------:|---------|
| 🧬 **基因组学 Genomics** | 472 | WGS/WES · 变异注释 · GWAS · CNV · 结构变异 · 基因组组装 |
| 🔬 **蛋白质组学 Proteomics** | 146 | 质谱分析 · 结构预测 · 蛋白质从头设计 · 结合亲和力优化 |
| 🔵 **单细胞 Single-Cell** | 117 | 预处理 · 聚类 · 细胞类型注释 · 轨迹推断 · 细胞通讯 |
| 🏥 **临床医学 Clinical** | 97 | EHR 分析 · 临床试验 · 药物相互作用 · 精准医学 |
| 📊 **转录组学 Transcriptomics** | 87 | RNA-seq · 差异表达 · 可变剪接 · lncRNA · 小 RNA |
| 🗄️ **数据库查询 Database** | 54 | UniProt · PDB · KEGG · Reactome · GEO · ClinVar · Ensembl |
| 🔗 **多组学整合 Multi-Omics** | 51 | MOFA · DIABLO · 单细胞多模态 · 空间转录组 |
| 🧪 **生信通用 Bioinformatics** | 50 | 序列分析 · BLAST · 工具链 · 流程管理 |
| 📈 **可视化 Visualization** | 38 | 火山图 · 热图 · PCA/UMAP · 交互式图表 |
| ⚙️ **流程编排 Workflow** | 31 | Snakemake · Nextflow · CWL · WDL |
| 🧫 **表观组学 Epigenomics** | 19 | ChIP-seq · ATAC-seq · DNA 甲基化 · Hi-C |
| 🌿 **通路分析 Pathway** | 13 | KEGG · Reactome · GO · GSEA |
| 🦠 **宏基因组学 Metagenomics** | 8 | 16S/ITS · Kraken2 · MetaPhlAn · QIIME2 |
| 🧩 **蛋白质设计 Protein Design** | 6 | RFDiffusion · ProteinMPNN · Boltz · Chai · LigandMPNN |

---

## 📦 仓库结构 · Structure

```
bio-skill-collection/
├── assets/
│   └── banner.png
├── skills/
│   ├── adaptyv/        # 21 skills — 蛋白质设计（RFDiffusion · ProteinMPNN · Boltz · Chai）
│   ├── bioclaw/        # 37 skills — 生信核心工具与数据库查询
│   ├── bioclaw_hub/    # 46 skills — 转录组 · 表观组 · 蛋白质设计 · EHR 等十大类
│   ├── bioskills/      # 524 skills — 最系统的纯生信套件，覆盖全流程
│   ├── clawbio/        # 60 skills — 生信流程编排（GWAS · 单细胞 · 结构生物学）
│   ├── kdense/         # 91 skills — 科学计算通用技能
│   ├── omics/          # 29 skills — 单细胞与空间组学专项
│   ├── openclaw/       # 332 skills — 医学 AI 技能库，聚合 12 个子仓库
│   ├── sciagent/       # 151 skills — 科研 Agent（统计 · 数据库 · 临床决策）
│   ├── sragent/        #   1 skill  — SRA/GEO 数据检索
│   └── zamushwani/     #   4 skills — 癌症多组学 R 分析
├── bioskill_index_v2.csv   # 完整索引表 · Full index (1306 rows)
└── README.md
```

---

## 🌐 整合来源 · Sources

| 仓库 · Repository | Skills | 特色 · Highlights |
|-------------------|:------:|-------------------|
| [GPTomics/bioSkills](https://github.com/GPTomics/bioSkills) | **524** | 最系统纯生信套件，QC → 多组学全流程 |
| [FreedomIntelligence/OpenClaw-Medical-Skills](https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills) | **326** | 最大医学 AI 技能库，聚合 12+ 子仓库 |
| [jaechang-hits/SciAgent-Skills](https://github.com/jaechang-hits/SciAgent-Skills) | **151** | 科研 Agent，统计 · 数据库 · 临床决策 |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | **91** | 科学计算通用技能库 |
| [ClawBio/ClawBio](https://github.com/ClawBio/ClawBio) | **60** | 生信流程编排与协调 |
| [zongtingwei/Bioclaw_Skills_Hub](https://github.com/zongtingwei/Bioclaw_Skills_Hub) | **46** | 社区贡献纯生物十大类 |
| [Runchuan-BU/BioClaw](https://github.com/Runchuan-BU/BioClaw) | **37** | 生信核心工具与数据库查询 |
| [fmschulz/omics-skills](https://github.com/fmschulz/omics-skills) | **29** | 单细胞与空间组学专项 |
| [adaptyvbio/protein-design-skills](https://github.com/adaptyvbio/protein-design-skills) | **21** | 蛋白质设计全套（RFDiffusion · Boltz · Chai） |
| [zamushwani2/biomedical-ai-skills](https://github.com/zamushwani2/biomedical-ai-skills) | **4** | 癌症多组学 R 分析 |
| [ArcInstitute/SRAgent](https://github.com/ArcInstitute/SRAgent) | **1** | SRA/GEO 智能检索 |

> 原始发现 **1926** 个，跨仓库去重后保留 **1306** 个，同名技能优先保留质量更高的来源版本。
> *1926 skills discovered across all sources; 1306 retained after cross-repository deduplication.*

---

## 📋 索引文件 · Index

`bioskill_index_v2.csv` 包含所有 1306 个 skill 的完整索引：

| 字段 | 说明 · Description |
|------|--------------------|
| `skill_name` | 技能名称 · Skill name |
| `folder_name` | 文件夹名 · Folder name |
| `source_repo` | 来源仓库 · Source repository |
| `category` | 类别 · Category |
| `description` | 描述 · Description |
| `file_count` | 文件数 · File count |
| `archive_path` | 仓库内路径 · Path in repo |
---

## 🗺️ 分析场景路线图 · Analysis Roadmap

> 按任务选择路线，每条路线列出推荐 skill 顺序与关键 Tips。
> *Pick a scenario — each roadmap lists recommended skills in order with key tips.*

<details>
<summary><b>🧬 RNA-seq 差异表达分析 · Bulk RNA-seq Differential Expression</b></summary>

| 步骤 Step | Skill | 来源 Source | 说明 Description |
|-----------|-------|-------------|-----------------|
| 1️⃣ 质控 QC | [`fastq-quality`](./skills/bioskills/fastq-quality) | `bioskills` | FastQC/fastp 原始数据质控 · Raw data quality control |
| 2️⃣ 比对 Alignment | [`hisat2-alignment`](./skills/bioskills/hisat2-alignment) | `bioskills` | HISAT2 剪接感知比对 · Splice-aware alignment |
| 3️⃣ 计数 Counting | [`featurecounts-counting`](./skills/bioskills/featurecounts-counting) | `bioskills` | featureCounts 生成计数矩阵 · Gene count matrix |
| 4️⃣ 差异分析 DE | [`deseq2-basics`](./skills/bioskills/deseq2-basics) | `bioskills` | DESeq2 差异表达（推荐）· Differential expression (recommended) |
| 4️⃣ 差异分析 alt | [`edger-basics`](./skills/bioskills/edger-basics) | `bioskills` | edgeR 小样本量替代 · Alternative for small n |
| 5️⃣ 可视化 Viz | [`de-visualization`](./skills/bioskills/de-visualization) | `bioskills` | 火山图、热图、PCA · Volcano, heatmap, PCA |
| 6️⃣ 富集 Enrichment | [`gsea`](./skills/bioskills/gsea) | `bioskills` | GSEA 基因集富集 · Gene set enrichment analysis |
| 6️⃣ GO 富集 alt | [`go-enrichment`](./skills/bioskills/go-enrichment) | `bioskills` | GO/KEGG ORA 富集 · Over-representation analysis |

> 💡 DESeq2 适合大多数场景；样本量 < 5 时考虑 edgeR。比对前确认基因组版本与 GTF 一致。
> *DESeq2 suits most cases; consider edgeR for n < 5. Always match genome version with GTF annotation.*

</details>

<details>
<summary><b>🔵 单细胞 RNA-seq 分析 · Single-Cell RNA-seq Analysis</b></summary>

| 步骤 Step | Skill | 来源 Source | 说明 Description |
|-----------|-------|-------------|-----------------|
| 1️⃣ 数据加载 Load | [`data-io`](./skills/bioskills/data-io) | `bioskills` | 加载 10x/h5ad · Load 10x/h5ad, Scanpy/Seurat |
| 2️⃣ 双细胞过滤 Doublet | [`doublet-detection`](./skills/bioskills/doublet-detection) | `bioskills` | Scrublet/DoubletFinder 去除双细胞 · Remove doublets |
| 3️⃣ 批次整合 Batch | [`batch-integration`](./skills/bioskills/batch-integration) | `bioskills` | Harmony 批次校正 · Batch effect correction |
| 4️⃣ 聚类 Clustering | [`clustering`](./skills/bioskills/clustering) | `bioskills` | Leiden 聚类 · Leiden clustering |
| 5️⃣ 细胞注释 Annotation | [`cell-annotation`](./skills/bioskills/cell-annotation) | `bioskills` | CellTypist/SingleR 自动注释 · Automated annotation |
| 6️⃣ 细胞通讯 Communication | [`cell-communication`](./skills/bioskills/cell-communication) | `bioskills` | CellChat/LIANA 配体受体 · Ligand-receptor analysis |
| 7️⃣ 轨迹推断 Trajectory | [`trajectory-inference`](./skills/bioskills/trajectory-inference) | `bioskills` | Monocle3/scVelo 发育轨迹 · Developmental trajectory |
| 8️⃣ 空间组学 Spatial | [`tooluniverse-spatial-omics-analysis`](./skills/openclaw/tooluniverse-spatial-omics-analysis) | `openclaw` | Visium/Xenium 空间转录组 · Spatial transcriptomics |

> 💡 先用 Scanpy（Python）探索，再用 Seurat（R）出图。批次整合放在聚类之前。
> *Explore with Scanpy (Python), finalize figures with Seurat (R). Always batch-correct before clustering.*

</details>

<details>
<summary><b>🧬 WGS 变异分析 · Whole Genome Variant Analysis</b></summary>

| 步骤 Step | Skill | 来源 Source | 说明 Description |
|-----------|-------|-------------|-----------------|
| 1️⃣ 比对 Alignment | [`bwa-alignment`](./skills/bioskills/bwa-alignment) | `bioskills` | BWA-MEM2 比对 · Reference alignment |
| 2️⃣ 变异检测 Calling | [`gatk-variant-calling`](./skills/bioskills/gatk-variant-calling) | `bioskills` | GATK HaplotypeCaller 变异检测 · Variant calling |
| 2️⃣ 深度学习 alt | [`deepvariant`](./skills/bioskills/deepvariant) | `bioskills` | DeepVariant 长读长/高精度 · Long-read / high-accuracy |
| 3️⃣ 频率过滤 Filter | [`gnomad-frequencies`](./skills/bioskills/gnomad-frequencies) | `bioskills` | gnomAD 人群频率过滤 · Population frequency filter |
| 4️⃣ 致病性注释 Pathogenicity | [`clinvar-lookup`](./skills/bioskills/clinvar-lookup) | `bioskills` | ClinVar 临床意义 · Clinical significance |
| 5️⃣ GWAS 关联 | [`gwas-pipeline`](./skills/bioskills/gwas-pipeline) | `bioskills` | PLINK2 全基因组关联 · Genome-wide association |
| 6️⃣ 精细定位 Fine-mapping | [`fine-mapping`](./skills/bioskills/fine-mapping) | `bioskills` | SuSiE 因果变异定位 · Causal variant fine-mapping |

> 💡 短读长用 BWA-MEM2 + GATK；长读长用 minimap2 + DeepVariant。GWAS 前做 PCA 人群分层校正。
> *Short reads: BWA-MEM2 + GATK; long reads: minimap2 + DeepVariant. Always correct for population stratification (PCA) before GWAS.*

</details>

<details>
<summary><b>🧩 蛋白质设计 · Protein Design & Engineering</b></summary>

| 步骤 Step | Skill | 来源 Source | 说明 Description |
|-----------|-------|-------------|-----------------|
| 1️⃣ 结构预测 Structure | [`alphafold`](./skills/adaptyv/alphafold) | `adaptyv` | AlphaFold2 结构预测 · Structure prediction |
| 1️⃣ 结构预测 alt | [`boltz`](./skills/adaptyv/boltz) | `adaptyv` | Boltz-1 开源替代更快 · Faster open-source alternative |
| 2️⃣ 骨架生成 Backbone | [`rfdiffusion`](./skills/adaptyv/rfdiffusion) | `adaptyv` | RFDiffusion 从头生成骨架 · De novo backbone generation |
| 3️⃣ 序列设计 Sequence | [`proteinmpnn`](./skills/adaptyv/proteinmpnn) | `adaptyv` | ProteinMPNN 序列设计 · Sequence design on backbone |
| 4️⃣ Binder 设计 | [`binder-design`](./skills/adaptyv/binder-design) | `adaptyv` | Binder 工具链选择 · Binder design toolkit |
| 5️⃣ 质量评估 QC | [`protein-qc`](./skills/adaptyv/protein-qc) | `adaptyv` | 结构/表达/亲和力评分 · Structure / expression / affinity QC |

> 💡 标准流程：AlphaFold 预测靶点 → RFDiffusion 生成骨架 → ProteinMPNN 设计序列 → AlphaFold 验证复合物。
> *Standard pipeline: AlphaFold (target) → RFDiffusion (backbone) → ProteinMPNN (sequence) → AlphaFold (complex validation).*

</details>

<details>
<summary><b>🦠 宏基因组分析 · Metagenomics Analysis</b></summary>

| 步骤 Step | Skill | 来源 Source | 说明 Description |
|-----------|-------|-------------|-----------------|
| 1️⃣ 物种分类 Taxonomy | [`kraken-classification`](./skills/bioskills/kraken-classification) | `bioskills` | Kraken2 物种分类 · Taxonomic classification |
| 2️⃣ 丰度估计 Abundance | [`metaphlan-profiling`](./skills/bioskills/metaphlan-profiling) | `bioskills` | MetaPhlAn4 相对丰度 · Relative abundance profiling |
| 3️⃣ 16S 扩增子 Amplicon | [`amplicon-processing`](./skills/bioskills/amplicon-processing) | `bioskills` | DADA2 16S/ITS ASV · Amplicon sequence variants |
| 4️⃣ 多样性 Diversity | [`diversity-analysis`](./skills/bioskills/diversity-analysis) | `bioskills` | Alpha/Beta 多样性 · Alpha/Beta diversity, phyloseq |
| 5️⃣ 组装 Assembly | [`metagenome-assembly`](./skills/bioskills/metagenome-assembly) | `bioskills` | MEGAHIT/metaSPAdes 组装 · Metagenomic assembly |

> 💡 鸟枪法用 Kraken2 + MetaPhlAn；16S 扩增子用 DADA2。多样性分析前做 rarefaction 标准化。
> *Shotgun: Kraken2 + MetaPhlAn; 16S amplicon: DADA2. Rarefy before diversity analysis.*

</details>

<details>
<summary><b>💊 药物发现 · Drug Discovery</b></summary>

| 步骤 Step | Skill | 来源 Source | 说明 Description |
|-----------|-------|-------------|-----------------|
| 1️⃣ 靶点发现 Target ID | [`tooluniverse-target-research`](./skills/openclaw/tooluniverse-target-research) | `openclaw` | OpenTargets + 文献证据 · Evidence-based target ID |
| 2️⃣ 药物研究 Drug Profile | [`tooluniverse-drug-research`](./skills/openclaw/tooluniverse-drug-research) | `openclaw` | 药理/靶点/临床全景 · Pharmacology / target / clinical |
| 3️⃣ 分子描述符 Descriptors | [`molecular-descriptors`](./skills/bioskills/molecular-descriptors) | `bioskills` | RDKit 虚拟筛选特征 · Molecular features for screening |
| 4️⃣ 分子生成 Generation | [`generative-design`](./skills/bioskills/generative-design) | `bioskills` | REINVENT 生成式设计 · Generative molecular design |
| 5️⃣ ADMET 预测 | [`admet-prediction`](./skills/bioskills/admet-prediction) | `bioskills` | 成药性预测 · Druglikeness & ADMET prediction |
| 6️⃣ 安全性 Safety | [`tooluniverse-adverse-event-detection`](./skills/openclaw/tooluniverse-adverse-event-detection) | `openclaw` | FDA FAERS 信号检测 · Adverse event signal detection |

> 💡 靶点发现后先做 druggability 评估，再进入分子设计。ADMET 在虚拟筛选后、合成前完成。
> *Assess druggability before molecular design. Run ADMET after virtual screening, before synthesis.*

</details>

<details>
<summary><b>🏥 临床/EHR 分析 · Clinical & EHR Analysis</b></summary>

| 步骤 Step | Skill | 来源 Source | 说明 Description |
|-----------|-------|-------------|-----------------|
| 1️⃣ 临床试验检索 Search | [`clinicaltrials-database`](./skills/openclaw/clinicaltrials-database) | `openclaw` | ClinicalTrials.gov API 检索 · Trial search & export |
| 2️⃣ 患者匹配 Matching | [`tooluniverse-clinical-trial-matching`](./skills/openclaw/tooluniverse-clinical-trial-matching) | `openclaw` | 多维度患者-试验匹配 · Multi-criteria patient matching |
| 3️⃣ 生存分析 Survival | [`survival-analysis`](./skills/bioskills/survival-analysis) | `bioskills` | KM + Cox 回归 · Kaplan-Meier + Cox regression |
| 4️⃣ 生物标志物 Biomarker | [`biomarker-discovery`](./skills/bioskills/biomarker-discovery) | `bioskills` | LASSO/Boruta 特征筛选 · Feature selection |
| 5️⃣ 罕见病诊断 Rare Disease | [`tooluniverse-rare-disease-diagnosis`](./skills/openclaw/tooluniverse-rare-disease-diagnosis) | `openclaw` | HPO 表型匹配 · Phenotype-driven diagnosis |
| 6️⃣ 精准医学 Precision | [`tooluniverse-precision-medicine-stratification`](./skills/openclaw/tooluniverse-precision-medicine-stratification) | `openclaw` | 生物标志物患者分层 · Biomarker-driven stratification |

> 💡 EHR 预处理是关键：ICD 编码标准化、缺失值处理、时序特征提取。生存分析前检验 PH 假设。
> *EHR preprocessing is critical: standardize ICD codes, handle missingness, extract temporal features. Test PH assumption before Cox regression.*

</details>


<div align="center">

**1306 Skills · 11 Sources · 15 Categories · 6772 Files**

*Aggregated with ❤️ for the biomedical AI community*

</div>
