---
name: paper-reproduce
description: >
  Systematic methodology for reproducing published academic papers using provided data.
  Use when the user asks to reproduce, replicate, or verify results from a published paper,
  including sample selection, descriptive statistics, regression analyses, and generating
  reproduction reports (Markdown + LaTeX PDF). Covers the full pipeline: data exploration,
  variable identification/mapping, sample filtering, variable construction, statistical
  analysis, result comparison, and documentation. Applicable to any observational study,
  clinical cohort, or survey-based research paper.
---

# Paper Reproduce — 论文复现方法论

## 核心原则

1. **先探索后建模** — 永远不要假设变量名和编码，必须从数据中验证
2. **逐步筛选逐步核对** — 每一步样本量都要和论文对比
3. **容忍偏差但记录偏差** — harmonized 数据集和原始数据必然有差异，关键是记录和解释
4. **边干边说** — 每完成一步立即输出中间结果，不要等全部跑完才汇报

## 复现流程（6 阶段）

### Phase 1: 任务理解 + 数据探索

```
输入: 论文 PDF/任务文档 + 数据文件
输出: 变量映射表 (variable_mapping.json)
```

1. 精读任务文档，提取：
   - 样本筛选流程（每步的 n 和排除条件）
   - 因变量、自变量、协变量的定义和编码
   - 统计方法（回归类型、标准误类型、标准化方式）
   - 期望的表格数值（用于验证）

2. 探索数据结构：
   ```python
   df = pd.read_stata('data.dta')  # 或 read_csv/read_sas
   print(f"维度: {df.shape}")
   print(f"变量: {df.columns.tolist()}")
   # 按前缀分组查看变量
   # 检查是否有 wave/time/year 标识
   ```

3. **变量识别四步法**（最关键的步骤）：
   - **精确匹配**: 搜索论文提到的变量名（如 `dc009s1`）
   - **语义搜索**: 搜索关键词（如 `mem`, `recall`, `orient`）
   - **范围验证**: 检查候选变量的值域是否匹配论文描述（如 0-10）
   - **交叉验证**: 用已知关系验证（如 `total = sub1 + sub2 + sub3`）

> **经验教训**: harmonized 数据集的变量名与原始问卷变量名通常完全不同。
> 不要假设 `dc009s1` 存在，要搜索语义等价的变量。

### Phase 2: 变量构建 + 验证

```
输入: variable_mapping.json
输出: 构建好变量的 DataFrame
```

1. 逐个构建变量，**每个变量构建后立即验证**：
   - 值域是否在期望范围内
   - 缺失率是否合理
   - 均值/比例是否接近论文报告值

2. **组合变量的验证技巧**：
   ```python
   # 验证 total = sub1 + sub2 + ... + subN
   calc = df['sub1'] + df['sub2'] + df['sub3']
   diff = (df['total'] - calc).abs()
   match_rate = (diff < 0.01).mean()
   print(f"吻合率: {match_rate:.1%}")
   ```

3. **分类变量编码注意事项**：
   - Stata/SPSS 导入的 category 变量通常是中文标签
   - 用 `value_counts()` 检查所有可能值
   - 论文说的"未婚"可能包含离异、丧偶、分居等多种状态
   - 论文说的"低于初中"教育，在 harmonized 数据中可能对应不同的分类变量

> **经验教训**: 当变量均值与论文偏差大时（如 MS 均值 7.11 vs 论文 5.73），
> 优先怀疑变量构成定义有误，而非数据问题。尝试不同的子变量组合。

### Phase 3: 样本筛选

```
输入: 构建好变量的 DataFrame
输出: 分析用的最终样本
```

1. 严格按论文的顺序逐步排除
2. **每一步都输出并对比**：
   ```
   Step N: 描述 → 保留 XXXX [论文: YYYY, 差 ZZZ]
   ```
3. 如果某步偏差大（>10%），**停下来排查**：
   - 检查变量缺失率：哪个变量贡献了最多缺失？
   - 如果是认知/生理测量变量缺失率高，考虑放宽定义
   - 对比论文的排除人数确定偏差来源

> **经验教训**: 要求多个变量同时不缺失会导致排除量远超预期。
> 如果论文未说明如何处理缺失，尝试：(a) 只要求核心变量不缺失，
> (b) 分步排除而非一次性 `dropna(subset=all_vars)`。

### Phase 4: 统计分析

```
输入: 最终样本
输出: Table 1, Table 2, Table 3 等
```

#### 描述统计 (Table 1)
```python
# 连续变量: M(SD) + t 检验
t_stat, p_val = stats.ttest_ind(group1[var], group2[var])

# 分类变量: % + 卡方检验
ct = pd.crosstab(grouping_var, category_var)
chi2, p_val, dof, expected = stats.chi2_contingency(ct)
```

#### 回归分析 (Table 2/3)
```python
# 标准化所有变量（因变量和自变量都标准化 → 得到标准化 beta）
from sklearn.preprocessing import StandardScaler
df_std = df[all_vars].copy()
for col in df_std.columns:
    df_std[col] = (df_std[col] - df_std[col].mean()) / df_std[col].std()

# OLS + 稳健标准误 (HC3)
model = smf.ols('y ~ x1 + x2 + ...', data=df_std).fit(cov_type='HC3')
```

#### 交互项处理
```python
# 标准化后再构建交互项
df_std['interaction'] = df_std['var1'] * df_std['var2']
```

#### 分层分析
```python
# 对每个子群体分别标准化后回归（不要用全样本的标准化参数）
for subset_name, subset in subsets.items():
    sub_std = subset[vars].copy()
    for col in sub_std.columns:
        sub_std[col] = (sub_std[col] - sub_std[col].mean()) / sub_std[col].std()
    model = smf.ols(formula, data=sub_std).fit(cov_type='HC3')
```

> **经验教训**: 
> - 标准化beta要求因变量和自变量都标准化
> - HC3 是最常用的稳健标准误，但不同软件默认不同（SPSS 用 HC0）
> - 分层分析时去掉分层变量（如按性别分层时不控制性别）
> - 分层分析对每个子群体独立标准化

### Phase 5: 结果对比 + 偏差分析

逐项核对论文报告值，使用三级标记：

| 标记 | 含义 | 标准 |
|------|------|------|
| ✅ | 验证 | 数值接近（允许末位四舍五入差异），显著性一致 |
| ⚠️ | 趋势一致 | 方向相同，但显著性不同（通常因样本量差异） |
| ❌ | 未复现 | 方向相反或差距太大 |

对每个 ❌ 和 ⚠️ 给出可能原因。

### Phase 6: 输出文档

同时生成两种格式：

1. **Markdown 文档**: 完整的复现报告，包含方法、结果、对比表、偏差讨论
2. **LaTeX → PDF**: 专业排版的 PDF 报告

LaTeX 编译注意事项：
- 中文用 `ctex` 包 + `xelatex` 编译
- 流程图用 `tikz`
- 表格用 `booktabs`（三线表）
- `\checkmark` 需要 `amssymb` 包

```bash
xelatex -interaction=nonstopmode report.tex  # 第一遍
xelatex -interaction=nonstopmode report.tex  # 第二遍（交叉引用）
```

## 输出目录结构

```
reproduce_<study>/
├── scripts/
│   └── full_analysis.py      # 主分析脚本（可独立运行）
├── figure1.json               # 筛选流程数据
├── table1.csv                 # 描述统计
├── table2.csv                 # 回归结果
├── table3.csv                 # 分层/补充分析
├── analysis_output.txt        # 完整控制台输出
├── 复现报告.md                # Markdown 报告
├── 复现报告.tex               # LaTeX 源文件
├── 复现报告.pdf               # PDF 报告
└── data files...              # 原始数据（不修改）
```

## 常见陷阱

| 陷阱 | 表现 | 解决 |
|------|------|------|
| **harmonized vs 原始数据** | 变量名不同、缺失模式不同、编码不同 | 基于语义+范围搜索变量，不要硬编码变量名 |
| **组合变量定义错误** | 均值偏差大（>1SD） | 用 total = sum(parts) 验证；尝试不同的子变量组合 |
| **缺失值级联** | 多变量同时要求非缺失 → 排除量远超论文 | 分步排除；先排核心变量缺失，再排协变量缺失 |
| **分类变量编码** | 中文标签多义（"未婚"的范围） | `value_counts()` 全部列出，逐一确认 |
| **标准化方式** | β系数方向对但数值偏大/偏小 | 确认是全变量标准化还是只标准化连续变量 |
| **稳健标准误类型** | p 值略有差异 | HC0/HC1/HC3 选择；SPSS 默认 HC0 |
| **Docker 文件同步** | 脚本修改后容器内仍是旧版 | 每次修改后 `docker cp` 同步 |

## 参考

详细的调查数据库特定操作，参见对应的数据库 skill（如 `charls-reproduce`）。
