# 🧬 Bio Skill 大全 v2

**全网最大生物医学 AI Agent 技能合集，共收录 1306 个经过去重的 bio skills，来自 GitHub 上 11 个顶级开源仓库，覆盖从基础生信分析到前沿蛋白质设计的完整生物医学研究链条。**

## 整合来源

整合的来源包括：专注纯生信流程的 **GPTomics/bioSkills**（524 个），收录了从序列比对、变异分析、差异表达到单细胞和表观组学的系统性工具集；聚合了 12 个子仓库的医学 AI 技能库 **OpenClaw-Medical-Skills**（326 个），涵盖临床报告、药物安全、癌症基因组和医疗设备等方向；面向科研 Agent 的 **SciAgent-Skills**（153 个）；通用科学计算技能库 **K-Dense-AI**（102 个）；专注生信流程编排的 **ClawBio**（63 个）；纯生物十大类的 **Bioclaw Skills Hub**（46 个）和 **BioClaw** 内置技能（37 个）；单细胞与空间组学专项的 **omics-skills**（29 个）；蛋白质设计全套工具 **adaptyvbio/protein-design-skills**（21 个），包含 RFDiffusion、ProteinMPNN、Boltz 等前沿方法；以及癌症多组学 R 分析技能和 SRA/GEO 数据检索技能各若干。

## 能力覆盖

从能力覆盖来看，基因组学方向最为丰富，共 472 个技能，涵盖 WGS/WES 分析、变异注释、GWAS、CNV、结构变异等全流程；蛋白质组学 146 个，包括质谱分析、结构预测与蛋白质设计；单细胞分析 117 个，从预处理、聚类、细胞类型注释到轨迹推断一应俱全；临床与医学方向 97 个，覆盖 EHR 分析、临床试验、药物相互作用和精准医学；转录组学 87 个；多组学整合 51 个；数据库直连查询 54 个，可直接访问 UniProt、PDB、KEGG、Reactome、GEO、ClinVar、Ensembl 等主流数据库。

## 技术规格

- **总技能数**：1306（去重后）
- **原始收录**：1926（跨仓库去重 620 个重复）
- **覆盖类别**：基因组学(472)、蛋白质组学(146)、单细胞(117)、临床(97)、转录组(87)、多组学(51)等 15 大类
- **兼容框架**：OpenClaw、NanoClaw、BioClaw 及所有支持 SKILL.md 格式的 Claude Agent 框架

## 文件说明

- `bioskill_collection_v2.zip` — 完整技能包，解压后即可上传 SkillHub
- `bioskill_index_v2.csv` — 1306 行索引表，含 skill_name / source_repo / category / description / archive_path

所有技能均采用标准 SKILL.md 格式，可直接上传 SkillHub 使用。
