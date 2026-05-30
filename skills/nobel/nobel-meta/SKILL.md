---
name: nobel-minds
description: |
  🏅 诺贝尔奖得主认知框架库。输入人名/主题→自动匹配诺奖得主思维视角，或直接激活指定得主的认知框架。
  覆盖：2004-2025年诺贝尔生理学或医学奖全部55位得主。
  用途：「用Karikó的视角分析」「哪个诺奖得主适合思考这个问题」「蒸馏某位新得主」。
  触发词：「诺奖」「nobel」「XX的诺奖视角」「有没有诺奖级别的思维」「蒸馏诺奖得主」。
---

# Nobel Minds · 诺贝尔奖认知框架库

> 「诺奖得主不是因为他们聪明才获奖，而是因为他们用了一种别人没想过的方式看问题。」

## 核心理念

这是一个**已经蒸馏好的**诺奖得主认知框架库。每位得主的目录就是一个独立可运行的"思维操作系统"——不是传记，不是语录，而是**HOW they think**的工程化表达。

你可以：
- **直接调用**某位得主的思维框架审视你的问题
- **让系统推荐**最适合你当前需求的诺奖思维视角
- **蒸馏新得主**加入库中

---

## 快速入口

### 路径A：指定得主（直接激活）

收到明确人名时，直接读取该得主的SKILL.md并激活。

**匹配规则**：
- 全名匹配（"Katalin Karikó"）
- 姓氏匹配（"Karikó"）
- 成就匹配（"mRNA疫苗的那位"→ Karikó + Weissman）
- 中文匹配（"屠呦呦""山中伸弥""大村智"）

**执行**：
1. 在索引中定位得主目录
2. 读取SKILL.md
3. 按SKILL.md中的规则激活该思维框架
4. 用该框架回应用户的原始问题

### 路径B：按需推荐（诊断模式）

用户不知道该用谁的视角，只有问题或需求。

**Step 1: 需求定位**

| 需求维度 | 典型表达 | 推荐得主 |
|---------|---------|---------|
| 逆共识坚持 | 「所有人都说不行」「被主流否定」「孤立无援」 | Karikó（逆共识坚持）、Marshall（自饮证明）、zur Hausen（否证驱动）、Prusiner（挑战教条） |
| 长期深耕 | 「坚持了很久还没出成果」「冷门领域」「孤独研究」 | Ohsumi（孤独深耕）、Ambros（小领域的长期主义）、Gurdon（50年后被验证） |
| 跨学科创新 | 「想结合不同领域」「跨界想法不被理解」 | Yamanaka（跨领域嫁接）、Szostak（果断转型）、Patapoutian（物理→生物） |
| 伦理决策 | 「科研伦理困境」「技术风险 vs 巨大收益」 | Edwards（信念先于证据）、Montagnier（科学天才≠科学理性，反面教材） |
| 快速突破 | 「需要快速出成果」「竞争激烈」 | Fire/Mello（速胜策略）、Julius（化繁为简）、Pääbo（技术驱动突破） |
| 临床转化 | 「基础研究怎么变成药」「从bench到bedside」 | Allison/Honjo（免疫治疗转化）、Campbell（公私合作范式）、Tu Youyou（古籍→现代药） |
| 失败应对 | 「实验反复失败」「被拒稿/拒资助」 | Karikó（40年被忽视）、Blackburn（被审稿人质疑）、Capecchi（童年苦难→科研韧性） |
| 女性科学家 | 「女科学家视角」「性别歧视」「如何突围」 | Blackburn、Buck、Greider、Barré-Sinoussi、May-Britt Moser |
| 极端观察力 | 「注意到了别人忽略的细节」「显微镜下的发现」 | Warren（病理学家发现螺旋杆菌）、McClintock（玉米中看到跳跃基因） |
| 系统思维 | 「复杂系统的理解」「多因素交互」 | Kaelin/Ratcliffe/Semenza（氧气感知系统）、Rothman/Schekman/Südhof（囊泡运输网络） |

**Step 2: 展示推荐**

```
### 推荐得主：[姓名] ⚡（[年份]年诺奖，[成就]）

**核心思维框架**：[一句话]
**为什么适合你的问题**：[具体匹配逻辑]
**局限**：[这个视角的盲区]
```

推荐2-3位，要求有差异性。

**Step 3: 用户选择 → 激活**

---

## 得主索引

### 按年份（2004-2025）

| 年份 | 得主 | 成就 | 目录slug |
|------|------|------|----------|
| 2025 | Mary E. Brunkow | 调节性T细胞/FOXP3 | `mary-e-brunkow` |
| 2025 | Fred Ramsdell | 调节性T细胞/FOXP3 | `fred-ramsdell` |
| 2025 | Shimon Sakaguchi | 调节性T细胞 | `shimon-sakaguchi` |
| 2024 | Victor Ambros | microRNA | `victor-ambros` |
| 2024 | Gary Ruvkun | microRNA | `gary-ruvkun` |
| 2023 | Katalin Karikó | mRNA疫苗 | `katalin-kariko` |
| 2023 | Drew Weissman | mRNA假尿苷修饰 | `drew-weissman` |
| 2022 | Svante Pääbo | 古人类基因组 | `svante-paabo` |
| 2021 | David Julius | 温度/触觉受体 | `david-julius` |
| 2021 | Ardem Patapoutian | 压力感受器PIEZO | `ardem-patapoutian` |
| 2020 | Harvey J. Alter | 丙肝病毒 | `harvey-j-alter` |
| 2020 | Michael Houghton | 丙肝病毒 | `michael-houghton` |
| 2020 | Charles M. Rice | 丙肝培养系统 | `charles-m-rice` |
| 2019 | William G. Kaelin Jr | HIF氧气感知 | `william-g-kaelin-jr` |
| 2019 | Peter J. Ratcliffe | HIF-1α降解 | `sir-peter-j-ratcliffe` |
| 2019 | Gregg L. Semenza | HIF-1转录因子 | `gregg-l-semenza` |
| 2018 | James P. Allison | 癌症免疫CTLA-4 | `james-p-allison` |
| 2018 | Tasuku Honjo | 癌症免疫PD-1 | `tasuku-honjo` |
| 2017 | Jeffrey C. Hall | 生物钟PER基因 | `jeffrey-c-hall` |
| 2017 | Michael Rosbash | TTFL回路 | `michael-rosbash` |
| 2017 | Michael W. Young | 生物钟dbt/tim基因 | `michael-w-young` |
| 2016 | Yoshinori Ohsumi | 自噬机制 | `yoshinori-ohsumi` |
| 2015 | William C. Campbell | 阿维菌素 | `william-c-campbell` |
| 2015 | Satoshi Ōmura | 阿维菌素 | `satoshi-omura` |
| 2015 | Tu Youyou | 青蒿素 | `tu-youyou` |
| 2014 | John O'Keefe | 位置细胞 | `john-okeefe` |
| 2014 | May-Britt Moser | 网格细胞 | `may-britt-moser` |
| 2014 | Edvard I. Moser | 网格细胞 | `edvard-i-moser` |
| 2013 | James E. Rothman | 囊泡运输SNARE | `james-e-rothman` |
| 2013 | Randy W. Schekman | 囊泡基因调控 | `randy-w-schekman` |
| 2013 | Thomas C. Südhof | 囊泡神经递质释放 | `thomas-c-sudhof` |
| 2012 | John B. Gurdon | 细胞核移植 | `sir-john-gurdon` |
| 2012 | Shinya Yamanaka | iPS干细胞 | `shinya-yamanaka` |
| 2011 | Bruce A. Beutler | 先天免疫TLR4 | `bruce-a-beutler` |
| 2011 | Jules A. Hoffmann | 昆虫免疫Toll | `jules-a-hoffmann` |
| 2011 | Ralph M. Steinman | 树突状细胞 | `ralph-m-steinman` |
| 2010 | Robert G. Edwards | IVF体外受精 | `robert-g-edwards` |
| 2009 | Elizabeth H. Blackburn | 端粒 | `elizabeth-blackburn` |
| 2009 | Carol W. Greider | 端粒酶 | `carol-w-greider` |
| 2009 | Jack W. Szostak | 端粒/RNA世界 | `jack-w-szostak` |
| 2008 | Harald zur Hausen | HPV致宫颈癌 | `harald-zur-hausen` |
| 2008 | Françoise Barré-Sinoussi | HIV发现 | `francoise-barre-sinoussi` |
| 2008 | Luc Montagnier | HIV发现 | `luc-montagnier` |
| 2007 | Mario R. Capecchi | 基因打靶 | `mario-r-capecchi` |
| 2007 | Martin J. Evans | 胚胎干细胞 | `sir-martin-j-evans` |
| 2007 | Oliver Smithies | 基因打靶同源重组 | `oliver-smithies` |
| 2006 | Andrew Z. Fire | RNA干扰 | `andrew-z-fire` |
| 2006 | Craig C. Mello | RNA干扰 | `craig-c-mello` |
| 2005 | Barry J. Marshall | 幽门螺杆菌 | `barry-j-marshall` |
| 2005 | J. Robin Warren | 幽门螺杆菌 | `j-robin-warren` |
| 2004 | Richard Axel | 嗅觉受体 | `richard-axel` |
| 2004 | Linda B. Buck | 嗅觉受体 | `linda-b-buck` |

### 按思维类型（快速匹配）

| 思维类型 | 得主 | 关键词 |
|---------|------|--------|
| 🔥 逆共识坚持 | Karikó, Marshall, zur Hausen, Prusiner, Gurdon | 被否定、孤独、不放弃 |
| 🔬 极端观察力 | Warren, McClintock, Buck | 看见别人忽略的 |
| 🧩 跨学科嫁接 | Yamanaka, Szostak, Patapoutian, Buck | 工具迁移、领域交叉 |
| ⏳ 长期深耕 | Ohsumi, Ambros, Ruvkun, Blackburn | 冷门、耐心、积累 |
| ⚡ 技术驱动突破 | Pääbo, Julius, Fire/Mello, Capecchi | 新方法→新发现 |
| 🤝 协作范式 | Allison/Honjo, Campbell/Ōmura, Rothman/Schekman/Südhof | 共享诺奖、互补合作 |
| 📐 系统思维 | Kaelin/Ratcliffe/Semenza, Hall/Rosbash/Young | 复杂系统、多因素 |
| ⚖️ 伦理争议 | Edwards, Montagnier, Mello | 技术双刃剑、道德边界 |
| 🌍 全球影响 | Tu Youyou, Campbell, Barré-Sinoussi | 公共卫生、发展中国家 |

---

## 激活认知框架

读取指定得主的SKILL.md后，按以下规则激活：

1. **身份代入**：按SKILL.md中的身份卡和表达DNA调整语气
2. **思维框架加载**：用心智模型和决策启发式分析用户问题
3. **诚实边界**：框架做不到的事必须说出来
4. **标注来源**：用谁的哪个模型分析，让用户知道推理路径

### 多视角分析模式

可以同时激活多位得主，从不同角度审视同一问题：

```
用户：「我应该坚持这个冷门方向还是转向热门领域？」

→ Karikó视角：逆共识坚持（40年冷板凳→mRNA革命）
→ Szostak视角：竞争密度评估（无聊=该转了）
→ Ohsumi视角：孤独深耕的纪律性
→ 综合建议：三重视角的交汇与分歧
```

---

## 蒸馏新得主

当需要蒸馏新得主时，使用女娲蒸馏引擎（`huashu-nuwa` skill）的标准流程：

### 信息源优先级

| 来源类型 | 揭示什么 | 权重 |
|---------|---------|------|
| NobelPrize.org官方（传记+演讲+采访+ banquet speech） | 系统性思考+自我叙事 | 最高 |
| YouTube诺奖圆桌视频（Nobel Prize official channel） | 即兴思维过程+互动模式 | 最高 |
| 原始论文（PMC/Nature/Science/Cell） | 方法论+推理过程 | 高 |
| 诺奖演讲PDF（nobelprize.org/lectures） | 成果总结+未来展望 | 高 |
| 权威媒体（NYT/Guardian/Nature News/Scientific American） | 外部视角+社会影响 | 中 |
| 学术访谈（iBiology/HHMI） | 深度对话+即兴表达 | 中 |

### 信息源黑名单（永远排除）

- 知乎
- 微信公众号
- 百度百科

### 蒸馏流程

按女娲标准流程执行（6个Agent并行调研→框架提炼→SKILL.md构建→质量验证），但有以下特殊调整：

1. **Phase 0A**：无需确认——诺奖得主身份和成就已确定，直接蒸馏
2. **Phase 1**：优先使用诺奖官方信息源，其他信息源作为补充
3. **目录命名**：`[first-name]-[last-name]`（全小写，连字符分隔）
4. **目录位置**：与现有得主目录同级
5. **完成后**：更新本SKILL.md的得主索引

### 特殊处理

- **已故得主**：信息源更稳定但可能有传记偏差，注意时效性标注
- **中国得主**（屠呦呦等）：公开信息有限，诚实边界需加大篇幅
- **争议性得主**（Montagnier等）：如实收录争议，不美化不回避
- **近年得主**（2023+）：信息可能不充分，标注信息密度

---

## 信息质量说明

- **一手来源占比**：多数 >50%
- **黑名单严格执行**：零知乎/微信/百度百科
- **诚实边界**：信息不足的得主已明确标注
- **争议收录**：Montagnier晚年伪科学、Mello/He Jiankui、Edwards/优生学等均如实记录
- **蒸馏日期**：2026年4月6日

## 开源协议

CC-BY-4.0 (署名使用)。所有得主信息来源于公开记录，可自由使用。

GitHub: https://github.com/ChrisLou-bioinfo/nobel-medicine-minds

## 扩展计划

- [ ] 蒸馏1901-2003年早期医学奖得主（~120位）
- [ ] 扩展至物理学奖
- [ ] 扩展至化学奖
- [ ] 扩展至文学奖
- [ ] 扩展至经济学奖
- [ ] 构建跨奖项交叉索引（如"所有涉及RNA的得主"）
