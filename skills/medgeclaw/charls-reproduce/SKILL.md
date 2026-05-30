---
name: charls-reproduce
description: >
  CHARLS (China Health and Retirement Longitudinal Study) database-specific knowledge
  for reproducing published papers. Use when reproducing or analyzing papers that use
  CHARLS data, including variable mapping from harmonized to raw questionnaire items,
  cognitive function scoring (episodic memory, mental status, TICS), CESD-10 depression
  screening, social isolation index construction, and chronic disease coding.
  Also use for any CHARLS data cleaning, variable construction, or cohort selection task.
---

# CHARLS Reproduce — CHARLS 数据库复现指南

## CHARLS 概览

| 项目 | 说明 |
|------|------|
| 全称 | China Health and Retirement Longitudinal Study (中国健康与养老追踪调查) |
| 官网 | https://charls.pku.edu.cn/ |
| 覆盖 | 全国 150 县级单位、450 社区，45 岁以上居民 |
| 波次 | wave1(2011), wave2(2013), wave3(2015), wave4(2018), wave5(2020) |
| 格式 | Stata (.dta), 也有 harmonized 版本 |

## Harmonized 数据集 vs 原始数据

大多数 CHARLS 论文使用**原始问卷模块数据**，变量名以 CHARLS 问卷编号命名（如 `dc009s1`）。但很多用户拿到的是 **harmonized 数据集**（合并所有波次，变量已清洗重命名）。

**识别方法**:
- 如果有 `wave` 列且包含 `wave1`-`wave5` → harmonized 数据
- 如果有 `dc009s1`, `be001`, `sc004_s1` 等原始变量名 → 原始数据
- harmonized 数据通常 ~10 万行（所有波次堆叠），原始数据每波 ~2 万行

**关键差异**: 变量名完全不同，缺失模式不同，编码方式不同。

## 核心变量映射表

### 认知功能

| 论文常用名 | 原始变量 | Harmonized 变量 | 范围 | 说明 |
|-----------|---------|----------------|------|------|
| 即时回忆 | `dc009s1`–`dc009s10` | `imrc` | 0-10 | 10 个词即时回忆正确数 |
| 延迟回忆 | `dc012s1`–`dc012s10` | `dlrc` | 0-10 | 延迟回忆正确数 |
| 情景记忆 (EM) | 自行计算 | `recall` 或 `(imrc+dlrc)/2` | 0-10 | **注意**: `recall` = `(imrc+dlrc)/2` |
| Serial 7 | `dc024` (5 次减法) | `ser7` | 0-5 | 100 连续减 7，正确次数 |
| 日期定向 | `dc003`-`dc006` | `orient` | 0-4 | = dw + dy + mo + yr（4 个二分项之和） |
| 画图 | `dc014` | `draw` | 0-1 | 重画展示图形是否正确 |
| 心理状态 (MS) | 自行计算 | `ser7 + orient + draw` | 0-10 | **重要**: 见下方详解 |
| 总认知分 | 自行计算 | `total_cognition` | 0-21 | 但 ≠ imrc+dlrc+ser7+orient+draw |

#### 心理状态 (Mental Status) 构建详解

论文中 MS 通常定义为 TICS 题目总分 = Serial 7 + 日期定向 + 画图 = 0-10。

但**注意**：
- `orient` = `dw + dy + mo + yr`（4 项，0-4），**不含** `ds`（day of season）
- 验证方法: `orient == dw + dy + mo + yr` 应 100% 吻合
- **如果论文 MS 均值 ~5-7**: 使用 `ser7 + orient + draw`（0-10）
- **如果论文 MS 均值 ~3-4**: 可能只用了 `orient + draw`（0-5），不含 ser7
- **`ser7` 缺失率高**（Wave1 约 19%），如果样本量偏差大，考虑排除 ser7

> **关键经验**: `ser7` 是 MS 定义中缺失率最高的子项。
> 如果筛选后样本量比论文少很多，先检查是否因 `ser7` 缺失。
> 尝试 `ms = orient + draw` 看样本量是否更接近论文。

### 抑郁 (CESD-10)

| 论文常用名 | 原始变量 | Harmonized 变量 | 范围 |
|-----------|---------|----------------|------|
| CESD-10 总分 | `dc002` 系列 (10 题) | `cesd10` | 0-30 |
| 抑郁分级 | CESD ≥ 10 | `cesd10 >= 10` | 二分 |

CESD-10 的 10 个题目中第 5 题（充满希望）和第 8 题（感到快乐）为**反向计分**。
harmonized 数据的 `cesd10` 已经处理好反向计分。

### 社会隔离

社会隔离指数通常由 4 个二分维度加总（0-4）：

| 维度 | 原始变量 | Harmonized 变量 | 得 1 分条件 |
|------|---------|----------------|-----------|
| 婚姻 | `be001` | `marry` | 非"已婚"状态 |
| 子女联系 | `sc004_s1` 等 | `kcntf`(面对面) + `kcntpm`(电话邮件) | 面对面和电话都无 |
| 居住地区 | `resid` / `rsuburb` | `hrural` 或 `rural2` | 农村 |
| 社会活动 | `dc045_s1` 等 | `socwk` 或 `act_1`-`act_8` | 不参加 |

#### 婚姻变量编码

`marry` 的可能值（harmonized 中文标签）:
```
已婚          → 0（有伴侣同居）
已婚但不住在一起 → 视论文定义（通常算 0 或 1）
丧偶          → 1
离异          → 1
分居          → 1
从未结婚       → 1
同居          → 0
```

**关键**: "已婚但不住在一起"的编码需要根据论文定义判断。
如果论文说"unmarried or not living with a partner"，则算 1。

#### 子女联系频率

harmonized 数据中**没有直接的联系频率变量**，只有：
- `kcntf`: 是否与子女面对面联系（是/否）
- `kcntpm`: 是否与子女电话/邮件联系（是/否）
- `kcnt`: 是否与子女有任何联系（是/否）
- `hchild`: 子女数量

原始数据有具体频率（每周/每月/每年），harmonized 只保留了二分变量。

> **经验**: 如果论文用"每周少于一次"作为阈值，用 harmonized 数据只能近似。
> `kcntf != '是' and kcntpm != '是'` 是合理的近似。

#### 农村/城市

- `hrural`: 户籍所在地（农村/城市），**每个人在所有波次都一样**
- `rural2`: 实际居住地（农村/城市），可能与户籍不同

> `hrural` 和 `rural2` 有交叉不一致的情况。论文通常用 `hrural`。

### 人口学与健康变量

| 论文变量 | Harmonized 变量 | 编码说明 |
|---------|----------------|---------|
| 年龄 | `age` | 连续；140 个缺失值（Wave1） |
| 性别 | `ragender` | 中文标签"男性"/"女性"；2 个缺失 |
| 教育 | `raeducl` | 3 类: "低于初中学历"/"高中和职业培训"/"高等教育" |
| 教育（细分） | `raeduc_c` | 4 类: "未完成小学"/"小学"/"中学"/"高中及以上" |
| BMI | `bmi` | 连续；有异常值（>100），需过滤 10-60 范围 |
| 高血压 | `hibpe` | "是"/"否"；基于"医生曾告知" |
| 糖尿病 | `diabe` | "是"/"否" |
| 心脏病 | `hearte` | "是"/"否"；含冠心病、心肌梗死等 |
| 脑卒中 | `stroke` | "是"/"否" |
| 当前吸烟 | `smoken` | "是"/"否"（当前是否吸烟） |
| 曾经吸烟 | `smokev` | "是"/"否"（是否曾经吸过烟） |
| 过去一年饮酒 | `drinkl` | "是"/"否" |
| 曾经饮酒 | `drinkev` | "是"/"否" |

### 社会活动变量

| Harmonized 变量 | 含义 | 频率变量 |
|----------------|------|---------|
| `act_1` / `social1` | 与朋友互动 | `freq_act_1`: 1=几乎每天, 2=每周, 3=不经常, 4=从不 |
| `act_2` / `social2` | 打牌/麻将/下棋 | `freq_act_2` |
| `act_3` / `social3` | 参加社区组织 | `freq_act_3` |
| `act_4` / `social4` | 志愿/慈善活动 | `freq_act_4` |
| `act_5` / `social5` | 上课/教育培训 | `freq_act_5` |
| `act_6` / `social6` | 炒股 | `freq_act_6` |
| `act_7` / `social7` | 上网 | `freq_act_7` |
| `act_8` / `social8` | 其他 | `freq_act_8` |
| `socwk` | 是否参加任何社会活动（汇总） | — |

## 日期定向子变量

| 变量 | 含义 | 纳入 orient |
|------|------|-----------|
| `dw` | 星期几 (day of week) | ✅ |
| `dy` | 日 (day) | ✅ |
| `mo` | 月 (month) | ✅ |
| `yr` | 年 (year) | ✅ |
| `ds` | 季节 (day of season) | ❌ 不在 orient 中 |

验证: `orient == dw + dy + mo + yr` 应 100% 吻合。

## 常见缺失率（Wave1 参考）

| 变量 | 缺失数 | 缺失率 | 影响 |
|------|-------|--------|------|
| `age` | 140 | 0.8% | 低 |
| `ragender` | 2 | <0.1% | 低 |
| `imrc` | 3,505 | 19.8% | **高** |
| `dlrc` | 3,626 | 20.5% | **高** |
| `ser7` | 3,425 | 19.3% | **高** — 认知筛选的主要杀手 |
| `orient` | 2,571 | 14.5% | 中 |
| `draw` | 1,880 | 10.6% | 中 |
| `cesd10` | 1,671 | 9.4% | 中 |
| `bmi` | 4,077 | 23.0% | **高** |
| `socwk` | 1,484 | 8.4% | 中 |

> **关键**: `imrc`、`dlrc`、`ser7` 的缺失率都在 ~20%。
> 如果论文要求所有认知变量同时不缺失，实际排除量会远超直觉。
> 有些论文可能只用了 EM（不含 MS）或只用了部分 MS 子项来降低缺失。

## 样本筛选经验

### 标准流程

```python
w1 = df[df['wave'] == 'wave1'].copy()

# Step 1: 年龄筛选
step1 = w1[w1['age'] >= 50]

# Step 2: 认知完整 — 分开检查，找出缺失的主要来源
for v in ['imrc', 'dlrc', 'ser7', 'orient', 'draw']:
    na_count = step1[v].isna().sum()
    print(f"  {v} 缺失: {na_count} ({na_count/len(step1)*100:.1f}%)")

# 先排核心因变量缺失（EM），再排 MS
step2a = step1.dropna(subset=['imrc', 'dlrc'])  # EM 核心
step2b = step2a.dropna(subset=['orient', 'draw'])  # MS 基础项
step2c = step2b.dropna(subset=['ser7'])  # 可选: 如果 MS 含 ser7

# Step 3-5: 后续筛选...
```

### 样本量调试策略

如果样本量与论文偏差 >10%:

1. **检查各变量缺失贡献**: 哪个变量排除了最多人？
2. **尝试不同的 MS 定义**:
   - `ms = ser7 + orient + draw`（标准，但 ser7 缺失率高）
   - `ms = orient + draw`（不含 ser7，缺失率低）
   - 只要求 EM 不缺失，不要求 MS 不缺失
3. **检查婚姻编码**: "已婚但不住在一起"算已婚还是未婚？
4. **检查 BMI 异常值**: 原始 BMI 有 >100 的值，是否被论文保留？

## Wave 间数据合并

```python
# 提取 Wave1 基线
w1 = df[df['wave'] == 'wave1'].copy()

# 提取 Wave3 结局
w3 = df[df['wave'] == 'wave3'].copy()
w3_outcome = w3[['ID', 'target_var']].rename(columns={'target_var': 'target_var_w3'})

# 合并
merged = w1.merge(w3_outcome, on='ID', how='left')
# 随访缺失 = merge 后 target_var_w3 为 NaN
```

## 标准化 OLS 回归模板

```python
import statsmodels.formula.api as smf
from sklearn.preprocessing import StandardScaler

# 标准化所有变量（因变量 + 自变量 → 得到标准化 beta）
all_vars = [dv] + ivs
df_std = df[all_vars].copy()
for col in df_std.columns:
    df_std[col] = (df_std[col] - df_std[col].mean()) / df_std[col].std()

# 交互项在标准化后构建
df_std['interaction'] = df_std['var1'] * df_std['var2']

# OLS + HC3
formula = f'{dv} ~ ' + ' + '.join(ivs)
model = smf.ols(formula, data=df_std).fit(cov_type='HC3')
```

## 环境注意事项

- 数据文件可能在 Docker 容器内，注意路径映射
- Stata .dta 读取: `pd.read_stata()`，category 变量会自动转为中文标签
- 大文件（>50MB）读取较慢，首次加载后考虑缓存为 parquet
