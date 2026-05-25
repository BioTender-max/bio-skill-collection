# bio-manuscript-pipeline

**End-to-end pipeline from structured research input to a full manuscript plan (一条龙 Pipeline)**

BioClaw integration notes:
- This skill is staged under `container/skills/` as part of a multi-skill manuscript pipeline.
- Shared templates and helper scripts are available under the sibling directory `bio-manuscript-common/`.
- When this pipeline needs supporting capabilities, prefer the copied BioClaw sibling skills in `container/skills/` over any `~/.openclaw/...` layout assumptions.
- This skill family is being integrated as a BioClaw community-contributed workflow.
- Upstream source reference: https://github.com/donghongyu2020/bio-manuscript-forge/tree/main/bio-manuscript-forge
- Contributor reference for attribution and documentation: Hongyu Dong, Westlake University PhD candidate, BioClaw community contributor / BioClaw community co-creation contributor.
- In BioClaw, treat the sibling manuscript skills as stepwise companion skills. You should explicitly follow their guidance phase by phase rather than assuming an automatic runtime dispatcher.
- If a later phase depends on outputs from an earlier phase, write those outputs into the group workspace first and then continue with the next sibling skill using those artifacts as context.
- At the end of each substantial run, also write a concise human-readable execution summary. Prefer `FINAL_EXEC_SUMMARY.md`; for integration-focused runs, also write `INTEGRATION_TEST_REPORT.md`.

---

## Welcome

Welcome to Bio-Manuscript-Forge. This workflow helps turn a rough research idea into a manuscript-ready planning package.

### Input Template

Provide your project in the following structure:

```text
topic: [research topic]
base_work:
  - paper: [related paper link]
  - code: [related code repository]

innovation: [one-sentence innovation summary]
- algorithmic novelty (算法创新性): [core method novelty]
- tasks (任务): [task1, task2, task3, ...]
- data (数据): [dataset source or type]
- benchmark: [evaluation benchmark]
- metrics (计算指标): [metric1, metric2, ...]
- biological analyses (生物学分析手段): [how biological significance will be shown]

demo_data: [demo dataset link]
target_journal: [optional, default nat-communications]
num_refine_rounds: [optional, default 2]
```

### Example Input

```
topic: spatial multi-omics integration
base_work:
  - paper: https://www.nature.com/articles/s41592-021-01336-8
  - code: https://github.com/broadinstitute/Tangram

innovation: jointly align spatial transcriptomics and proteomics while preserving tissue-domain boundaries
- algorithmic novelty (算法创新性): boundary-aware cross-modal alignment with explicit domain-consistency regularization
- tasks (任务): cell annotation, spatial domain detection, cross-modal integration, biological interpretation
- data (数据): public spatial transcriptomics and spatial proteomics cohorts with matched single-cell references
- benchmark: compare against mapping, domain, and integration baselines on public tumor datasets
- metrics (计算指标): ARI, NMI, Macro-F1, boundary preservation score, biological consistency
- biological analyses (生物学分析手段):
  - marker recovery across modalities
  - pathway enrichment consistency
  - neighborhood preservation
  - tissue-boundary case studies

demo_data: https://zenodo.org/record/0000000
target_journal: nat-communications
num_refine_rounds: 2
```

### Expected Outputs

| File | Content |
|------|---------|
| **PPT** | Lab meeting / progress presentation |
| **FINAL_PROPOSAL** | Full research proposal |
| **Figure 2-7 (v3)** | Detailed task-wise figure designs |
| **Manuscript text (v2)** | Introduction, Results, Discussion, Methods |

---

Provide the project description and the pipeline can begin.

---

## Purpose

Run the full manuscript pipeline, generate a journal-style plan, and iteratively refine it through reviewer-style feedback.

## Input Schema

```text
topic: [research topic]
base_work: [paper links + code links]
innovation: [high-level innovation summary]
- algorithmic novelty (算法创新性): [core algorithmic novelty]
- tasks (任务): [downstream tasks, comma-separated]
- data (数据): [dataset source / type]
- benchmark: [benchmark dataset or evaluation setup]
- metrics (计算指标): [safety + task metrics such as ASR, ARI, etc.]
- biological analyses (生物学分析手段): [marker genes, pathways, neighborhood analysis, etc.]

demo_data: [demo dataset link]
target_journal: [optional, default nat-communications]
num_refine_rounds: [optional, default 2]
```

### Example Input (public-safe sample)

```
topic: spatial multi-omics integration
base_work:
  - paper: https://www.nature.com/articles/s41592-021-01336-8
  - code: https://github.com/broadinstitute/Tangram

innovation: jointly align spatial transcriptomics and proteomics while preserving tissue-domain boundaries
- algorithmic novelty (算法创新性): boundary-aware cross-modal alignment with explicit domain-consistency regularization
- tasks (任务): cell annotation, spatial domain detection, cross-modal integration, biological interpretation
- data (数据): public spatial transcriptomics and spatial proteomics cohorts with matched single-cell references
- benchmark: compare against mapping, domain, and integration baselines on public tumor datasets
- metrics (计算指标): ARI, NMI, Macro-F1, boundary preservation score, biological consistency
- biological analyses (生物学分析手段):
  - marker recovery across modalities
  - pathway enrichment consistency
  - neighborhood preservation
  - tissue-boundary case studies

demo_data: https://zenodo.org/record/0000000
target_journal: nat-communications
num_refine_rounds: 2
```

### Field Guide

| Field | Required | Description |
|------|----------|-------------|
| topic | yes | concise research topic |
| base_work | yes | paper + code links |
| innovation | yes | high-level idea plus structured subfields |
| demo_data | yes | demo dataset link |
| target_journal | no | default `nat-communications` |
| num_refine_rounds | no | default `2` |

### Innovation Subfields

| Subfield | Description | Example |
|----------|-------------|---------|
| algorithmic novelty (算法创新性) | core method novelty | attention entropy, loss redesign, architecture change |
| tasks (任务) | downstream tasks covered | cell annotation, perturbation, GRN inference |
| data (数据) | dataset source / type | public cohorts, user data, target tissue |
| benchmark | evaluation setup | existing benchmark or new benchmark |
| metrics (计算指标) | safety + task metrics | ASR, Accuracy, F1, ARI, Pearson |
| biological analyses (生物学分析手段) | how biology will be demonstrated | marker gene, pathway, regulatory links |

## Execution Flow

### Phase 1: System building (Steps 1-5)

**Input parsing**: first extract the key signals from user input:
- `topic` → 用于创新性搜索
- `base_work` → 提取已有工作数据集、指标、方法
- `innovation.algorithmic novelty` / `innovation.算法创新性` -> novelty assessment
- `innovation.tasks` / `innovation.任务` -> task system design
- `innovation.data` / `innovation.数据` -> dataset search direction
- `innovation.metrics` / `innovation.计算指标` -> metric system design
- `innovation.biological analyses` / `innovation.生物学分析手段` -> analysis system design

```
Step 1: 创新性检测
├─ 解析输入：topic, base_work, innovation.算法创新性
├─ 调用 searxng/web_search 搜索
├─ Topic 同义变换生成 10-20 个变体
├─ 搜索 PubMed + bioRxiv + arXiv q-bio
├─ 统计相似文章数量
├─ 结合 innovation.算法创新性 判断创新性级别
└─ 输出：01_INNOVATION_ASSESSMENT.md

Step 2: 任务体系构建
├─ 解析输入：innovation.任务
├─ 若用户提供任务列表 → 直接使用
├─ 若未提供 → 搜索领域主要任务分类
├─ 识别任务层级（Level 1-4）
├─ 确保难度递进
└─ 输出：02_TASK_SYSTEM.md

Step 3: 数据集搜索
├─ 解析输入：innovation.数据, innovation.benchmark, demo_data
├─ 若用户提供数据描述 → 搜索匹配数据集
├─ 从 base_work 论文提取数据集
├─ 数据集与任务匹配
└─ 输出：03_DATASET_CATALOG.md

Step 4: 指标体系构建
├─ 解析输入：innovation.计算指标
├─ 若用户提供指标 → 直接使用并补充
├─ 若未提供 → 从已有工作提取指标
├─ 分类：安全指标 + 任务指标
└─ 输出：04_METRIC_SYSTEM.md

Step 5: 分析方法体系
├─ 解析输入：innovation.生物学分析手段
├─ 若用户提供分析手段 → 直接使用并补充
├─ 若未提供 → 从已有工作提取分析方法
├─ 标注 OmicsClaw/Bioclaw skill
├─ 说明为什么用、证明什么、体现什么生物学意义
└─ 输出：05_ANALYSIS_SYSTEM.md
```

### Phase 2: 设计与文案（Steps 6-7）

**⚠️ 核心原则**：
1. **任务为先**：Figure 2-N 每个对应一个任务，数据/指标/分析随任务而定
2. **分析增强**：每个 Figure 必须包含安全 + 生物学分析
3. **文案同步**：Figure 改完立即更新 Results

```
Step 6: Figure 设计
│
├─ Figure 1：算法创新性（方法框架）
│   ├─ Panel a：方法 Overview
│   ├─ Panel b：创新点示意
│   ├─ Panel c：模型覆盖
│   ├─ Panel d：任务覆盖
│   └─ Panel e：指标体系
│
├─ Figure 2-N：每个 Figure = 一个任务 ⭐ 任务为先原则
│   │
│   ├─ Panel a: 任务 Overview（数据流）
│   │
│   ├─ Panel b-d: 定量测评
│   │   ├─ 多模型对比
│   │   ├─ ASR 降低
│   │   └─ 任务指标保持
│   │
│   ├─ Panel e: Technical analysis ⭐ must include
│   │   ├─ representation pattern shifts
│   │   ├─ error / uncertainty analysis
│   │   └─ failure-mode or boundary-case inspection
│   │
│   ├─ Panel f: 生物学分析 ⭐ 必须包含
│   │   ├─ Marker gene recovery
│   │   ├─ Pathway preservation
│   │   └─ 具体生物学意义
│   │
│   ├─ Panel g: In-depth case studies ⭐ 1-2 cases
│   │   ├─ concrete biological question
│   │   ├─ baseline vs proposed method comparison
│   │   └─ interpretation of recovered biological structure
│   │
│   └─ 数据/指标/分析依据任务选取
│
├─ Figure N+1: Summary + 生物学意义总结
│
└─ 输出：06_FIGURE_DESIGNS/

Step 6.5: 文案同步检查 ⭐ 必须
├─ Figure 有这个 Panel → Results 有对应段落？
├─ Figure 有这个案例 → Results 有详细展开？
└─ 检查通过才能进入下一步

Step 7: 论文文案生成
│
├─ Introduction（5段）
│   ├─ 第一段：领域介绍
│   ├─ 第二段：相关工作调研
│   ├─ 第三段：现有方法不足
│   ├─ 第四段：本文方法介绍
│   └─ 第五段：意义与应用
│
├─ Results（与 Figure 对应）⭐ 结构对齐
│   ├─ 2.1 Overview（对应 Figure 1）
│   ├─ 2.2 Task 1 / Main claim（对应 Figure 2）
│   │   ├─ quantitative evaluation
│   │   ├─ technical analysis
│   │   ├─ biological analysis
│   │   └─ case study
│   ├─ 2.3 Task 2 / Main claim（对应 Figure 3）
│   ├─ ...每个任务一个 section
│   └─ 2.N Summary（对应最后一个 Figure）
│
├─ Discussion
│   ├─ 方法优势总结
│   ├─ 安全-生物学结合意义 ⭐
│   ├─ 与现有方法对比
│   ├─ 方法局限性
│   └─ 未来方向
│
├─ Methods
│   ├─ 数据预处理
│   ├─ 模型架构
│   ├─ 任务特定方法 ⭐ 按任务组织
│   ├─ 生物学分析方法 ⭐
│   ├─ 统计分析
│   └─ 代码与数据可用性
│
└─ 输出：07_MANUSCRIPT_TEXT/
```

**Figure 设计检查清单**：

```
- [ ] Figure 1 是方法框架？
- [ ] Figure 2-N 每个对应一个任务？
- [ ] 每个 Figure 包含多模型对比？
- [ ] 每个 Figure 有定量测评 Panel？
- [ ] 每个 Figure 有安全分析 Panel？ ⭐
- [ ] 每个 Figure 有生物学分析 Panel？ ⭐
- [ ] 每个 Figure 有 1-2 个深入案例？ ⭐
- [ ] 分析手段多样化？
- [ ] Results 结构与 Figure 对应？ ⭐
```

### Phase 2.5: Refine Loop ⭐

```
Step 7.5: 三审稿人迭代优化
│
├─ Round 0: 保存初始方案
│   └─ 输出：refine-logs/round-0-initial-proposal.md
│
├─ Round 1 Review:
│   ├─ Editor Review（创新性评估，Nature子刊标准）
│   │   ├─ 概念创新 / 方法创新 / 应用创新
│   │   └─ 评分：创新性 / 可行性 / 推荐度
│   │
│   ├─ 计算审稿人 Review（算法/方法评审）
│   │   ├─ 算法设计合理性 / 方法创新性
│   │   ├─ 实验设计严谨性（Baseline/指标/Ablation）
│   │   └─ 评分：方法创新 / 技术严谨 / 代码可行
│   │
│   ├─ 生物分析审稿人 Review（生物学意义评审）
│   │   ├─ 生物学意义 / 分析设计合理性
│   │   ├─ 数据集选择合理性
│   │   └─ 评分：生物意义 / 分析设计 / 数据选择
│   │
│   └─ 输出：refine-logs/round-1/
│
├─ Round 1 Refinement:
│   ├─ 汇总三审稿人意见
│   ├─ 问题分类（Critical/Major/Minor）
│   ├─ 逐条响应和修改
│   ├─ 更新 Proposal
│   └─ 输出：refine-logs/round-1/refinement.md
│
├─ Round 2 Review:（同 Round 1）
│   └─ 输出：refine-logs/round-2/
│
├─ Round 2 Refinement:
│   └─ 输出：refine-logs/round-2/refinement.md
│
└─ 最终输出：
    ├─ refine-logs/REVIEW_SUMMARY.md（每轮汇总）
    ├─ refine-logs/FINAL_PROPOSAL.md（最终方案）
    ├─ refine-logs/score-history.md（评分历史）
    └─ refine-logs/REFINEMENT_REPORT.md（完整报告）
```

### Phase 2.6: 人类反馈验证 ⭐ NEW

```
Step 7.6: 人类反馈循环
│
├─ 呈现 Proposal
│   ├─ 展示 FINAL_PROPOSAL.md 核心内容
│   ├─ 包含：创新点、Figure 设计、实验方案、关键修改
│   └─ 格式：结构化摘要 + 关键决策点
│
├─ 等待人类反馈
│   ├─ 选项 A: 同意 → 继续 Phase 3
│   └─ 选项 B: 有意见 → 收集反馈内容
│
├─ 反馈处理
│   ├─ 如果同意 → 记录并进入 Phase 3
│   └─ 如果不同意 → 
│       ├─ 记录反馈意见到 refine-logs/human-feedback/
│       ├─ 根据反馈类型决定返回点：
│       │   ├─ Phase 1 级问题：创新性/任务体系需重构
│       │   ├─ Phase 2 级问题：Figure/文案需调整
│       │   └─ Phase 2.5 级问题：细节优化
│       ├─ 执行迭代修改
│       ├─ 重新运行 Phase 2.5 Refine Loop
│       └─ 再次呈现给人类验证
│
└─ 输出：
    ├─ refine-logs/human-feedback/feedback-round-X.md
    └─ refine-logs/HUMAN_APPROVAL.md（最终批准记录）
```

**人类反馈处理流程：**

```
人类反馈 → 问题分类 → 返回点决策
│
├─ Critical 问题（创新性方向错误）
│   └─ 返回 Phase 1 → 重新评估创新点
│
├─ Major 问题（设计/方案需要大改）
│   └─ 返回 Phase 2 → 调整 Figure/文案
│
├─ Minor 问题（细节优化）
│   └─ 返回 Phase 2.5 → Refine Loop
│
└─ 批准
    └─ 进入 Phase 3
```

**反馈收集格式：**

```markdown
## 人类反馈 Round X

**反馈时间**: YYYY-MM-DD HH:MM
**反馈内容**: [用户意见]
**问题级别**: Critical / Major / Minor
**返回阶段**: Phase 1 / Phase 2 / Phase 2.5
**修改建议**: [AI 分析后的修改方案]

---

## 修改执行记录

- [ ] 修改项 1
- [ ] 修改项 2
...
```

### Phase 3: 验证与汇报（Steps 8-11）

```
Step 8: 代码修改方案
├─ 克隆原有代码仓库
├─ 分析代码结构
├─ 映射创新点到修改位置
├─ 设计新增文件 + 修改文件
└─ 输出：08_CODE_MODIFICATION_PLAN.md

Step 9: Demo 快速验证
├─ 应用代码修改
├─ 下载 Demo 数据
├─ Subsample + 少 epoch 快速运行
├─ 可行性判断
├─ 如果不可行 → 修改建议
└─ 输出：09_DEMO_VALIDATION.md

Step 10: 详细分析执行（可选）
├─ 调用 OmicsClaw/Bioclaw
├─ 运行完整分析
├─ 生成实际数据
└─ 输出：10_ANALYSIS_RESULTS.md

Step 11: 生成组会汇报 PPT（⭐ 新增）
├─ 从 FINAL_PROPOSAL.md 提取核心内容
├─ 从 DEMO_VALIDATION.md 提取 Demo 结果
├─ 生成 12-15 页组会汇报 PPT
├─ 格式：Markdown (Marp) / HTML (reveal.js) / PPTX
└─ 输出：11_PPT_PRESENTATION.md

Step 12: 执行总结与汇报摘要（⭐ BioClaw 集成建议）
├─ 汇总本次实际跑过的阶段
├─ 汇总关键输出文件与路径
├─ 标注哪些步骤真正跑通、哪些仅为草案/脚手架
├─ 标注当前 blocker
├─ 给出下一步建议（最多 3 条）
├─ 记录适合集成汇报的结论
└─ 输出：FINAL_EXEC_SUMMARY.md
```

## 输出目录结构

```
manuscript-plan/
├── 01_INNOVATION_ASSESSMENT.md
├── 02_TASK_SYSTEM.md
├── 03_DATASET_CATALOG.md
├── 04_METRIC_SYSTEM.md
├── 05_ANALYSIS_SYSTEM.md
│
├── 06_FIGURE_DESIGNS/
│   ├── FIGURE_1_DESIGN.md
│   ├── FIGURE_2_DESIGN.md
│   ├── FIGURE_3_DESIGN.md
│   ├── FIGURE_4_DESIGN.md
│   ├── FIGURE_5_DESIGN.md
│   └── SUPPLEMENTARY_DESIGN.md
│
├── 07_MANUSCRIPT_TEXT/
│   ├── INTRODUCTION.md
│   ├── RESULTS.md
│   ├── DISCUSSION.md
│   └── METHODS.md
│
├── refine-logs/                    # ⭐ 新增
│   ├── round-0-initial-proposal.md
│   │
│   ├── round-1/
│   │   ├── editor-review.md
│   │   ├── computational-review.md
│   │   ├── biological-review.md
│   │   ├── review-summary.md
│   │   └── refinement.md
│   │
│   ├── round-2/
│   │   ├── editor-review.md
│   │   ├── computational-review.md
│   │   ├── biological-review.md
│   │   ├── review-summary.md
│   │   └── refinement.md
│   │
│   ├── human-feedback/              # ⭐ NEW: 人类反馈记录
│   │   ├── feedback-round-1.md
│   │   ├── feedback-round-2.md
│   │   └── ...
│   │
│   ├── REVIEW_SUMMARY.md
│   ├── FINAL_PROPOSAL.md
│   ├── HUMAN_APPROVAL.md            # ⭐ NEW: 人类批准记录
│   ├── score-history.md
│   └── REFINEMENT_REPORT.md
│
├── 08_CODE_MODIFICATION_PLAN.md
├── 09_DEMO_VALIDATION.md
├── 10_ANALYSIS_RESULTS.md
│
├── 11_PPT_PRESENTATION.md           # ⭐ 新增：组会汇报 PPT
├── FINAL_EXEC_SUMMARY.md            # ⭐ 新增：面向人类汇报的执行摘要
├── INTEGRATION_TEST_REPORT.md       # ⭐ 可选：集成/验证测试报告
│
└── FINAL_MANUSCRIPT_PLAN.md
```

## 执行摘要模板

每次较完整运行结束后，补一个汇报友好的摘要文件，至少覆盖以下内容：

```md
# FINAL_EXEC_SUMMARY

## Run Scope
- Topic:
- Date:
- Workspace:
- Pipeline entry:

## Stages Executed
- Step / Phase:
- Step / Phase:

## Key Files Generated
- path/to/file
- path/to/file

## Verified Outputs
- What actually ran successfully
- What was only drafted / scaffolded

## Current Blockers
- blocker 1
- blocker 2

## Recommended Next Steps
1. ...
2. ...
3. ...

## Attribution
- Workflow family: Bio-Manuscript-Forge
- BioClaw integration: community-contributed workflow
- Contributor reference: Hongyu Dong, Westlake University PhD candidate, BioClaw community contributor
```

## 三审稿人评审标准

### Editor（编辑）
- **职责**：初审，判断是否达到 Nature 子刊水平
- **评审维度**：创新性、可行性、期刊匹配度
- **评分**：创新性/10、可行性/10、推荐意见

### 计算审稿人
- **职责**：从计算/算法角度评审
- **评审维度**：算法设计、方法创新、实验严谨性、代码可行性
- **评分**：方法创新/10、技术严谨/10、代码可行/10

### 生物分析审稿人
- **职责**：从生物学/分析角度评审
- **评审维度**：生物学意义、分析设计、数据选择
- **评分**：生物意义/10、分析设计/10、数据选择/10

## 使用方式

```bash
/bio-manuscript-pipeline "topic: spatial multi-omics integration | base_work: https://github.com/example/project | innovation: boundary-aware cross-modal alignment | demo_data: https://example.com/data.h5ad | target_journal: nat-communications | num_refine_rounds: 2"
```

## 子 Skill 调用

本 Pipeline 会依次调用以下子 Skill：
- `bio-innovation-check`（Step 1）
- `bio-task-system`（Step 2）
- `bio-dataset-search`（Step 3）
- `bio-metric-system`（Step 4）
- `bio-analysis-system`（Step 5）
- `bio-figure-design`（Step 6）
- `bio-manuscript-text`（Step 7）
- `bio-manuscript-refine`（Step 7.5）⭐
- `bio-human-feedback`（Step 7.6）⭐ NEW - 人类反馈验证
- `bio-code-modification`（Step 8）
- `bio-demo-validate`（Step 9）
- `bio-ppt-generate`（Step 11）⭐

## 注意事项

1. **Phase 1 完成后**：检查创新性评估结果
2. **Phase 2 完成后**：检查 Figure 设计和文案
3. **Phase 2.5（Refine Loop）**：每轮评分需达到 7+ 才能进入下一阶段
4. **Phase 2.6（人类反馈验证）**：⭐ 关键检查点
   - 呈现 FINAL_PROPOSAL.md 给人类审阅
   - 必须等待人类明确反馈
   - 同意 → 继续 Phase 3
   - 不同意 → 根据问题级别返回对应阶段迭代
   - 所有反馈记录到 refine-logs/human-feedback/
5. **Phase 3**：Demo 验证如果不可行，回到 Step 8 重新设计
6. **迭代收敛**：通常 2 轮 Refine 后评分趋于稳定
7. **最终检查**：使用 FINAL_PROPOSAL.md 作为执行依据
8. **人类批准**：必须有人类批准记录（HUMAN_APPROVAL.md）才能进入 Phase 3
