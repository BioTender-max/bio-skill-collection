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
<summary><b>🧬 RNA-seq 差异表达分析 · Bulk RNA-seq DE</b></summary>

| 步骤 | Skill | 来源 | 说明 |
|------|-------|------|------|
| 1️⃣ 质控 QC | [`fastq-quality`](./skills/bioskills/fastq-quality) | `bioskills` | FastQC/fastp 原始数据质控 |
| 2️⃣ 比对 Alignment | [`hisat2-alignment`](./skills/bioskills/hisat2-alignment) | `bioskills` | HISAT2 剪接感知比对 |
| 3️⃣ 计数 Counting | [`featurecounts-counting`](./skills/bioskills/featurecounts-counting) | `bioskills` | featureCounts 生成计数矩阵 |
| 4️⃣ 差异分析 DE | [`deseq2-basics`](./skills/bioskills/deseq2-basics) | `bioskills` | DESeq2（推荐） |
| 4️⃣ 差异分析 alt | [`edger-basics`](./skills/bioskills/edger-basics) | `bioskills` | edgeR（小样本量） |
| 5️⃣ 可视化 Viz | [`de-visualization`](./skills/bioskills/de-visualization) | `bioskills` | 火山图、热图、PCA |
| 6️⃣ 富集 Enrichment | [`gsea`](./skills/bioskills/gsea) | `bioskills` | GSEA 基因集富集 |
| 6️⃣ GO 富集 alt | [`go-enrichment`](./skills/bioskills/go-enrichment) | `bioskills` | GO/KEGG ORA |

> 💡 DESeq2 适合大多数场景；样本量 < 5 时考虑 edgeR。比对前确认基因组版本与 GTF 一致。

</details>

<details>
<summary><b>🔵 单细胞 RNA-seq 分析 · scRNA-seq</b></summary>

| 步骤 | Skill | 来源 | 说明 |
|------|-------|------|------|
| 1️⃣ 数据加载 | [`data-io`](./skills/bioskills/data-io) | `bioskills` | 加载 10x/h5ad，Scanpy/Seurat |
| 2️⃣ 双细胞过滤 | [`doublet-detection`](./skills/bioskills/doublet-detection) | `bioskills` | Scrublet/DoubletFinder |
| 3️⃣ 批次整合 | [`batch-integration`](./skills/bioskills/batch-integration) | `bioskills` | Harmony 批次校正 |
| 4️⃣ 聚类 | [`clustering`](./skills/bioskills/clustering) | `bioskills` | Leiden 聚类 |
| 5️⃣ 细胞注释 | [`cell-annotation`](./skills/bioskills/cell-annotation) | `bioskills` | CellTypist/SingleR |
| 6️⃣ 细胞通讯 | [`cell-communication`](./skills/bioskills/cell-communication) | `bioskills` | CellChat/LIANA |
| 7️⃣ 轨迹推断 | [`trajectory-inference`](./skills/bioskills/trajectory-inference) | `bioskills` | Monocle3/scVelo |
| 8️⃣ 空间组学 | [`tooluniverse-spatial-omics-analysis`](./skills/openclaw/tooluniverse-spatial-omics-analysis) | `openclaw` | Visium/Xenium |

> 💡 先用 Scanpy（Python）探索，再用 Seurat（R）出图。批次整合放在聚类之前。

</details>

<details>
<summary><b>🧬 WGS 变异分析 · Whole Genome Variant Analysis</b></summary>

| 步骤 | Skill | 来源 | 说明 |
|------|-------|------|------|
| 1️⃣ 比对 | [`bwa-alignment`](./skills/bioskills/bwa-alignment) | `bioskills` | BWA-MEM2 |
| 2️⃣ 变异检测 | [`gatk-variant-calling`](./skills/bioskills/gatk-variant-calling) | `bioskills` | GATK HaplotypeCaller |
| 2️⃣ 深度学习 alt | [`deepvariant`](./skills/bioskills/deepvariant) | `bioskills` | DeepVariant（长读长） |
| 3️⃣ 频率过滤 | [`gnomad-frequencies`](./skills/bioskills/gnomad-frequencies) | `bioskills` | gnomAD 人群频率 |
| 4️⃣ 致病性注释 | [`clinvar-lookup`](./skills/bioskills/clinvar-lookup) | `bioskills` | ClinVar 临床意义 |
| 5️⃣ GWAS | [`gwas-pipeline`](./skills/bioskills/gwas-pipeline) | `bioskills` | PLINK2 全基因组关联 |
| 6️⃣ 精细定位 | [`fine-mapping`](./skills/bioskills/fine-mapping) | `bioskills` | SuSiE 因果变异定位 |

> 💡 短读长用 BWA-MEM2 + GATK；长读长用 minimap2 + DeepVariant。GWAS 前做 PCA 人群分层校正。

</details>

<details>
<summary><b>🧩 蛋白质设计 · Protein Design</b></summary>

| 步骤 | Skill | 来源 | 说明 |
|------|-------|------|------|
| 1️⃣ 结构预测 | [`alphafold`](./skills/adaptyv/alphafold) | `adaptyv` | AlphaFold2 |
| 1️⃣ 结构预测 alt | [`boltz`](./skills/adaptyv/boltz) | `adaptyv` | Boltz-1（更快） |
| 2️⃣ 骨架生成 | [`rfdiffusion`](./skills/adaptyv/rfdiffusion) | `adaptyv` | RFDiffusion |
| 3️⃣ 序列设计 | [`proteinmpnn`](./skills/adaptyv/proteinmpnn) | `adaptyv` | ProteinMPNN |
| 4️⃣ Binder 设计 | [`binder-design`](./skills/adaptyv/binder-design) | `adaptyv` | Binder 工具链 |
| 5️⃣ 质量评估 | [`protein-qc`](./skills/adaptyv/protein-qc) | `adaptyv` | 结构/表达/亲和力评分 |

> 💡 标准流程：AlphaFold 预测靶点 → RFDiffusion 生成骨架 → ProteinMPNN 设计序列 → AlphaFold 验证复合物。

</details>

<details>
<summary><b>🦠 宏基因组分析 · Metagenomics</b></summary>

| 步骤 | Skill | 来源 | 说明 |
|------|-------|------|------|
| 1️⃣ 物种分类 | [`kraken-classification`](./skills/bioskills/kraken-classification) | `bioskills` | Kraken2 |
| 2️⃣ 丰度估计 | [`metaphlan-profiling`](./skills/bioskills/metaphlan-profiling) | `bioskills` | MetaPhlAn4 |
| 3️⃣ 16S 扩增子 | [`amplicon-processing`](./skills/bioskills/amplicon-processing) | `bioskills` | DADA2 |
| 4️⃣ 多样性分析 | [`diversity-analysis`](./skills/bioskills/diversity-analysis) | `bioskills` | Alpha/Beta 多样性 |
| 5️⃣ 组装 | [`metagenome-assembly`](./skills/bioskills/metagenome-assembly) | `bioskills` | MEGAHIT/metaSPAdes |

> 💡 鸟枪法用 Kraken2 + MetaPhlAn；16S 扩增子用 DADA2。多样性分析前做 rarefaction 标准化。

</details>

<details>
<summary><b>💊 药物发现 · Drug Discovery</b></summary>

| 步骤 | Skill | 来源 | 说明 |
|------|-------|------|------|
| 1️⃣ 靶点发现 | [`tooluniverse-target-research`](./skills/openclaw/tooluniverse-target-research) | `openclaw` | OpenTargets + 文献证据 |
| 2️⃣ 药物研究 | [`tooluniverse-drug-research`](./skills/openclaw/tooluniverse-drug-research) | `openclaw` | 药理/靶点/临床全景 |
| 3️⃣ 分子描述符 | [`molecular-descriptors`](./skills/bioskills/molecular-descriptors) | `bioskills` | RDKit 虚拟筛选特征 |
| 4️⃣ 分子生成 | [`generative-design`](./skills/bioskills/generative-design) | `bioskills` | REINVENT 生成式设计 |
| 5️⃣ ADMET | [`admet-prediction`](./skills/bioskills/admet-prediction) | `bioskills` | 成药性预测 |
| 6️⃣ 安全性 | [`tooluniverse-adverse-event-detection`](./skills/openclaw/tooluniverse-adverse-event-detection) | `openclaw` | FDA FAERS 信号检测 |

> 💡 靶点发现后先做 druggability 评估，再进入分子设计。ADMET 在虚拟筛选后、合成前完成。

</details>

<details>
<summary><b>🏥 临床/EHR 分析 · Clinical & EHR</b></summary>

| 步骤 | Skill | 来源 | 说明 |
|------|-------|------|------|
| 1️⃣ 临床试验检索 | [`clinicaltrials-database`](./skills/openclaw/clinicaltrials-database) | `openclaw` | ClinicalTrials.gov API |
| 2️⃣ 患者匹配 | [`tooluniverse-clinical-trial-matching`](./skills/openclaw/tooluniverse-clinical-trial-matching) | `openclaw` | 多维度患者-试验匹配 |
| 3️⃣ 生存分析 | [`survival-analysis`](./skills/bioskills/survival-analysis) | `bioskills` | KM + Cox 回归 |
| 4️⃣ 生物标志物 | [`biomarker-discovery`](./skills/bioskills/biomarker-discovery) | `bioskills` | LASSO/Boruta |
| 5️⃣ 罕见病诊断 | [`tooluniverse-rare-disease-diagnosis`](./skills/openclaw/tooluniverse-rare-disease-diagnosis) | `openclaw` | HPO 表型匹配 |
| 6️⃣ 精准医学 | [`tooluniverse-precision-medicine-stratification`](./skills/openclaw/tooluniverse-precision-medicine-stratification) | `openclaw` | 患者分层 |

> 💡 EHR 预处理是关键：ICD 编码标准化、缺失值处理、时序特征提取。生存分析前检验 PH 假设。

</details>


<div align="center">

**1306 Skills · 11 Sources · 15 Categories · 6772 Files**

*Aggregated with ❤️ for the biomedical AI community*

</div>
