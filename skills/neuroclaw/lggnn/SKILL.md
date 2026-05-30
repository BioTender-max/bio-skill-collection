---
name: lggnn
description: "Use this model doc whenever the user wants to run LG-GNN (Local-to-Global GNN) for fMRI phenotype prediction. LG-GNN is a PyG-based GNN with SABP (Self-Attention Brain Pooling) and mutual-information regularization. NeuroClaw adapts the original population-graph version to single-subject brain graphs."
license: MIT License (NeuroClaw custom skill - freely modifiable within the project)
layer: base
skill_type: model
dependencies:
  - fmri-skill
  - run_models
---
# LG-GNN Model Doc

## Overview
LG-GNN (Local-to-Global GNN) 是一种针对脑疾病诊断的两阶段图神经网络。原始论文使用 Local_GNN 提取每个被试的脑图嵌入，再通过基于人口学信息构建的 Global_GNN 进行人群图分类。NeuroClaw 改造为单被试任务：保留 Local_GNN（含 SABP + 互信息正则化的创新组件），用 MLP head 替代人口图。

- Paper: Zhang et al., 2022, "Local to Global Hierarchical Graph Neural Network for Brain Disorder Diagnosis"，MICCAI
- Official code: https://github.com/cnuzh/LG-GNN
- NeuroClaw reimplementation: `models/lggnn/`（去除人口图依赖，单被试 PyG 流程）
- Primary input: PyG Data graph（与 BrainGNN 共享数据格式）
- Primary output: phenotype prediction + ROI 重要性（SABP perm）+ MI loss 辅助监督

**Research use only.**

---

## NeuroClaw 实现要点

1. **单被试改造**：原版需要非影像表型数据构建人口图，NeuroClaw 仅保留 Local_GNN，用 MLP head 输出。
2. **SABP 池化**：Self-Attention Brain Pooling，topk 选择 ROI + tanh(score) 加权，并产生互信息估计 `mi` 作为辅助 loss（论文权重 0.1，loss 取 `loss - 0.1 * mi` 鼓励高互信息）。
3. **PyG 2.7 兼容**：原 `torch_geometric.nn.pool.topk_pool` 已重构，NeuroClaw 用 `pool.select.topk` + 内联 `filter_adj`。
4. **任务统一接口**：classification (`nclass=N`) 与 regression (`nclass=1, task='regression'`) 一套代码。
5. **数据复用**：直接复用 BrainGNN 的 `NeuroClawFCDataset`，无需额外预处理。

---

## Quick Start (NeuroClaw 内部)

### 前置条件
- conda env: `neuroclaw` (Python 3.11)
- 已有 `data/braingnn_input/<atlas>/sub-*.pt` 文件（与 BrainGNN 共享）

### 训练（分类，单 fold 冒烟测试）
```bash
python skills/lggnn/scripts/train_reference.py \
    --atlas aal_116 \
    --labels-csv data/hcp_gender_labels.csv \
    --fold 0 --n-epochs 10 --batch-size 16
```

### 训练（回归，HCP age）
```bash
python skills/lggnn/scripts/train_reference.py \
    --atlas schaefer_100_7net \
    --labels-csv data/hcp_age_labels.csv \
    --task regression --fold 0 --n-epochs 50
```

---

## 核心文件

| 文件 | 作用 |
|---|---|
| `models/lggnn/net/lggnn.py` | 模型定义：LocalGNN (GCN×2 + SABP + GCN) + MLP head |
| `models/lggnn/scripts/data_adapter.py` | 数据适配（薄封装复用 `models.braingnn`） |
| `skills/lggnn/scripts/train_reference.py` | K-fold CV 训练参考实现 |

---

## 模型架构

```
Input PyG Data (x=[N,N], edge_index, edge_attr, batch)
  -> GCNConv(N, 64) + ReLU
  -> GCNConv(64, 20) + ReLU
  -> SABP pool (ratio=0.5): topk_score + tanh weighted; 产生 mi_estimate
  -> GCNConv(20, 20) + ReLU
  -> 残差: pooled + conv3
  -> global_mean_pool
  -> MLP head: Linear(20 -> 64) + ReLU + Dropout + Linear(64 -> nclass)
Output: (logits, mi_loss)
```

---

## 关键训练参数

| 参数 | 论文默认 | NeuroClaw 默认 | 说明 |
|---|---|---|---|
| `--lr` | 0.01 | 0.001 | 论文用 0.01，NeuroClaw 与其他模型对齐用 0.001 |
| `--wd` | 5e-5 | 5e-4 | 权重衰减 |
| `--hidden-dim` | 64 | 64 | GCN 隐藏维度 |
| `--embed-dim` | 20 | 20 | SABP 后嵌入维度 |
| `--ratio` | 0.9 | 0.5 | SABP keep ratio，论文 0.9，对齐 BrainGNN 用 0.5 |
| `--dropout` | 0.2 | 0.3 | MLP head dropout |
| `--mi-weight` | 0.1 | 0.1 | MI loss 权重（注意：从 loss 中减去） |
| `--n-epochs` | 400 | 50 | 论文 400 ep，NeuroClaw 50 ep 与其他模型对齐 |

---

## 调试经验与注意事项

1. **MI loss 符号**：原论文 `loss = loss_cla - 0.1 * mi_loss`（最大化 MI），NeuroClaw 保持相同符号约定。
2. **SABP 输出形状**：池化后节点数变为 `floor(ratio * N)`，注意 batch 后的 graph_emb 是 `[B, embed_dim]`。
3. **ratio 调参**：论文 ratio=0.9（仅丢 10% ROI）需要 hgc=16；NeuroClaw 用 hgc=64 时 ratio=0.5 更稳定。
4. **PyG 2.7 兼容**：旧版 `topk_pool.topk/filter_adj` 已移除，使用 `pool.select.topk.topk` 与内联 `_filter_adj`。
5. **MI 初始为 0**：训练开始时 mi_estimate ≈ 0（因 joint 和 margin 分布相近），训练过程中应逐步变正。
6. **数据复用**：与 BrainGNN 共享 `NeuroClawFCDataset`，无需重复加载/缓存。

---

## NeuroClaw 委托规则

- ROI 生成和预处理：委托 `fmri-skill`
- HCP 数据下载/编排：委托 `hcpya-skill` / `hcpa-skill` / `hcpd-skill` / `hcpep-skill`
- 依赖检查：`dependency-planner` + `conda-env-manager`
- 执行路由：`claw-shell`

执行前需明确计划确认。

---

## Reference

- Zhang Y, Zhan L, Cai W, Thompson P, Huang H. 2022. Local to Global Hierarchical Graph Neural Network for Brain Disorder Diagnosis. MICCAI.
- Official repository: https://github.com/cnuzh/LG-GNN
- NeuroClaw BrainGNN skill (共享数据格式): `skills/brain_gnn/SKILL.md`

Created At: 2026-05-19 01:30 HKT
Last Updated At: 2026-05-19 01:30 HKT
Author: chengwang96
