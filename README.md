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

<div align="center">

**1306 Skills · 11 Sources · 15 Categories · 6772 Files**

*Aggregated with ❤️ for the biomedical AI community*

</div>
