# Bio Skill Collection

全网最大的生物医学 AI Agent 技能合集，共收录 **1306 个经过去重的 bio skills**，来自 GitHub 上 11 个顶级开源仓库，覆盖从基础生信分析到前沿蛋白质设计的完整生物医学研究链条。

## 仓库结构

```
skills/
├── adaptyv/        # 21 skills — 蛋白质设计（RFDiffusion、ProteinMPNN、Boltz、Chai）
├── bioclaw/        # 37 skills — 生信核心工具与数据库查询
├── bioclaw_hub/    # 46 skills — 转录组、表观组、蛋白质设计、EHR 等十大类
├── bioskills/      # 524 skills — 最系统的纯生信套件，覆盖全流程
├── clawbio/        # 60 skills — 生信流程编排（GWAS、单细胞、结构生物学）
├── kdense/         # 91 skills — 科学计算通用技能
├── omics/          # 29 skills — 单细胞与空间组学专项
├── openclaw/       # 332 skills — 医学 AI 技能库，聚合 12 个子仓库
├── sciagent/       # 151 skills — 科研 Agent 技能（统计、数据库、临床）
├── sragent/        #  1 skill  — SRA/GEO 数据检索
└── zamushwani/     #  4 skills — 癌症多组学 R 分析
```

每个 skill 是一个独立文件夹，包含 `SKILL.md`（技能定义）及附属的示例代码、参考文档等。

## 整合来源

| 仓库 | Skills | 特色 |
|------|--------|------|
| [GPTomics/bioSkills](https://github.com/GPTomics/bioSkills) | 524 | 纯生信套件，从 QC 到多组学全流程 |
| [FreedomIntelligence/OpenClaw-Medical-Skills](https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills) | 326 | 医学 AI 技能库，聚合 12+ 子仓库 |
| [jaechang-hits/SciAgent-Skills](https://github.com/jaechang-hits/SciAgent-Skills) | 151 | 科研 Agent，含统计、数据库、临床决策 |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 91 | 科学计算通用技能 |
| [ClawBio/ClawBio](https://github.com/ClawBio/ClawBio) | 60 | 生信流程编排 |
| [zongtingwei/Bioclaw_Skills_Hub](https://github.com/zongtingwei/Bioclaw_Skills_Hub) | 46 | 纯生物十大类技能 |
| [Runchuan-BU/BioClaw](https://github.com/Runchuan-BU/BioClaw) | 37 | 生信核心工具与数据库查询 |
| [fmschulz/omics-skills](https://github.com/fmschulz/omics-skills) | 29 | 单细胞与空间组学 |
| [adaptyvbio/protein-design-skills](https://github.com/adaptyvbio/protein-design-skills) | 21 | 蛋白质设计全套 |
| [zamushwani2/biomedical-ai-skills](https://github.com/zamushwani2/biomedical-ai-skills) | 4 | 癌症多组学 R 分析 |
| [ArcInstitute/SRAgent](https://github.com/ArcInstitute/SRAgent) | 1 | SRA/GEO 数据检索 |

原始发现 1926 个，跨仓库去重后保留 1306 个，同名技能优先保留质量更高的来源版本。

## 能力覆盖

**基因组学**（472）：WGS/WES 分析、变异注释、GWAS、CNV、结构变异、单倍型分型、基因组组装

**蛋白质组学**（146）：质谱分析、结构预测、蛋白质从头设计、结合亲和力优化

**单细胞分析**（117）：预处理、聚类、细胞类型注释、轨迹推断、细胞通讯、多模态整合

**临床与医学**（97）：EHR 分析、临床试验设计、药物相互作用、精准医学、不良事件检测

**转录组学**（87）：RNA-seq 全流程、差异表达、可变剪接、lncRNA、小 RNA

**数据库查询**（54）：UniProt、PDB、KEGG、Reactome、GEO、ClinVar、Ensembl、STRING

**多组学整合**（51）：MOFA、DIABLO、单细胞多模态、空间转录组

**表观组学**（19）：ChIP-seq、ATAC-seq、DNA 甲基化、Hi-C、染色质状态

**宏基因组学**（8）：16S/ITS 扩增子、Kraken2、MetaPhlAn、QIIME2

**蛋白质设计**（6）：RFDiffusion、ProteinMPNN、Boltz、Chai、LigandMPNN

## 索引文件

`bioskill_index_v2.csv` 包含所有 1306 个 skill 的索引，字段：

| 字段 | 说明 |
|------|------|
| `skill_name` | 技能名称 |
| `folder_name` | 文件夹名 |
| `source_repo` | 来源仓库 |
| `category` | 类别 |
| `description` | 描述 |
| `file_count` | 文件数 |
| `archive_path` | 仓库内路径 |

## 统计

- **总技能数**：1306（去重后）
- **原始收录**：1926
- **总文件数**：6772
- **来源仓库**：11 个
- **覆盖类别**：15 大类
