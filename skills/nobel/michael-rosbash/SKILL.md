# SKILL.md — Michael Rosbash 蒸馏知识引擎

> 2017年诺贝尔生理学或医学奖得主 · 昼夜节律分子机制 · TTFL 转录-翻译负反馈回路

---

## 身份速查

| 字段 | 内容 |
|------|------|
| **姓名** | Michael Morris Rosbash |
| **生卒** | 1944.3.7– ，美国堪萨斯城 |
| **机构** | Brandeis University / HHMI |
| **诺奖** | 2017（与 Jeffrey Hall、Michael Young 共享） |
| **获奖理由** | 发现控制昼夜节律的分子机制 |
| **关键概念** | TTFL（转录-翻译负反馈回路）、period 基因、PER 蛋白振荡 |

## 一句话总结

Rosbash 证明了生物钟的核心是一个**自调控的转录-翻译负反馈回路**——*period* 基因产生的 PER 蛋白累积到阈值后反馈抑制自身转录，蛋白降解后循环重启，产生约24小时的自主振荡。这一范式从果蝇到人类高度保守。

## 核心知识图谱

### 1. 发现主线
```
Konopka & Benzer (1971): period 基因（第一个钟基因）
    ↓
Hall & Rosbash (1984): 克隆 period
    ↓
Hardin, Hall & Rosbash (1990): 提出 TTFL 负反馈模型 ← 里程碑
    ↓
Young (1995): timeless 基因，TIM-PER 异二聚体
    ↓
Rosbash Lab (1998): cycle、clock、cryptochrome
    ↓
哺乳动物保守性验证 → 人 → 医学应用
```

### 2. TTFL 核心机制
- **CLK-CYC** 激活 *per/tim* 转录 → mRNA 累积 → 翻译为 PER/TIM
- PER-TIM 异二聚体入核 → 抑制 CLK-CYC 活性 → *per/tim* 转录下降
- PER/TIM 磷酸化（DBT 激酶）→ 降解 → 解除抑制 → 循环重启
- **光**通过 CRY → TIM 降解 → 相位重置

### 3. 关键实验证据
- PER 蛋白丰度呈24h振荡，夜间峰值
- *per* mRNA 峰先于蛋白峰 → 提示转录后调控
- 无义突变消除 mRNA 振荡，野生型 PER 可拯救
- PER 核穿梭的时序调控

### 4. 方法论标志
- **正向遗传学**：突变 → 表型 → 基因
- **果蝇行为监测**：DAM 系统 + χ² 周期图分析
- **分子生物学**：抗体、Co-IP、ChIP-seq
- **Rosbash 特色**：RNA 后转录调控

## 六维研究索引

| 维度 | 文件 | 核心内容 |
|------|------|----------|
| 生平传记 | `research/01-biography.md` | 教育轨迹、学术合作、荣誉、个人特质 |
| 核心发现 | `research/02-core-discovery.md` | TTFL 的时间线、关键实验、回路模型 |
| 研究方法 | `research/03-methodology.md` | 正向遗传学、分子工具、行为监测、ChIP-seq |
| 理论框架 | `research/04-theoretical-framework.md` | 负反馈理论、温度补偿、授时机制、跨物种保守性 |
| 影响应用 | `research/05-impact-applications.md` | 睡眠障碍、代谢病、癌症时间治疗、公共卫生 |
| 哲学智慧 | `research/06-philosophy-wisdom.md` | 基础研究信念、科学三要素、时间哲学、人文关怀 |

## 核心引用

- Hardin PE, Hall JC, Rosbash M. (1990). *Feedback of the *Drosophila* period gene product on circadian cycling of its messenger RNA levels*. Nature 343: 536–540. **（TTFL 模型的奠基论文）**
- Konopka RJ, Benzer S. (1971). *Clock mutants of *Drosophila melanogaster*. Proc Natl Acad Sci USA 68: 2112–2116.
- Siwicki KK et al. (1988). *Circadian oscillations in the protein product of the period gene*. Science 241: 1279–1282.

## 经典语录

> "We are changing this successful formula [of immigration and openness] at our peril."
> "Scientific careers rely on inheritance, environment and random events like all biological phenomena."
> "One should never discount the importance of 'blind, dumb luck'."

## 触发场景

当用户涉及以下话题时，自动激活本知识库：
- 昼夜节律 / 生物钟 / circadian rhythm
- 睡眠障碍 / 轮班工作健康影响
- 转录-翻译反馈回路 / TTFL
- 果蝇遗传学 / 模式生物学
- 时间生物学 / chronobiology
- Michael Rosbash / 2017诺贝尔医学奖

---
*蒸馏引擎：女娲 · 蒸馏时间：2026-04-06 · 信息源：诺贝尔官网、PubMed/PMC、HHMI、Britannica*
