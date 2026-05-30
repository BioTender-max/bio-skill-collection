---
name: ibgnn
description: "Use this model doc whenever the user wants to run IBGNN (Interpretable Brain Graph Neural Network) for fMRI phenotype prediction. IBGNN is a PyG-based GNN with a learnable MLP message function over [x_i, x_j, edge_attr], designed for connectome-based brain disorder analysis with post-hoc edge-mask explainer support."
license: MIT License (NeuroClaw custom skill - freely modifiable within the project)
layer: base
skill_type: model
dependencies:
  - fmri-skill
  - run_models
---
# IBGNN Model Doc

## Overview
IBGNN (Interpretable Brain Graph Neural Network) 是面向脑连接组分析的可解释 GNN。核心组件是 MPConv —— 在 GCN 归一化基础上，将消息计算从简单加权聚合改为 `MLP([x_i, x_j, edge_attr])` 学习消息函数。模型与 post-hoc 边遮罩 explainer 配合使用，可提取对预测重要的边子图。

- Paper: Cui et al., 2022, "Interpretable Graph Neural Networks for Connectome-Based Brain Disorder Analysis"，MICCAI
- Official code: https://github.com/HennyJie/IBGNN
- NeuroClaw reimplementation: `models/ibgnn/`（移除 explainer 用的 edge_flag 机制，仅保留 encoder）
- Primary input: PyG Data graph（与 BrainGNN 共享数据格式）
- Primary output: phenotype prediction（可选 attention/重要边解释）

**Research use only.**

---

## NeuroClaw 实现要点

1. **MPConv 核心**：每条边的消息 = `Linear([x_i, x_j, edge_attr])`，比 GCN 多一层非线性表达。
2. **GCN 归一化**：边权 |corr| 经过对称归一化（与 GCN 相同），再注入 self-loop。
3. **去除 edge_flag**：原版用于 explainer 屏蔽边，普通 forward 中 edge_flag 是全 1 tensor，NeuroClaw 直接砍掉以简化代码。
4. **正边权约束**：`edge_attr.abs()` 后传入，与 BrainGNN 同样做法（softmax 类操作需要非负）。
5. **任务统一接口**：classification (`nclass=N`) 与 regression (`nclass=1, task='regression'`) 一套代码。
6. **PyG 2.7 兼容**：`torch_scatter.scatter_add` 已被 `torch_geometric.utils.scatter(reduce='sum')` 替代。
7. **数据复用**：直接复用 BrainGNN 的 `NeuroClawFCDataset`，无需额外预处理。

---

## Quick Start (NeuroClaw 内部)

### 前置条件
- conda env: `neuroclaw` (Python 3.11)
- 已有 `data/braingnn_input/<atlas>/sub-*.pt` 文件（与 BrainGNN 共享）

### 训练（分类，单 fold 冒烟测试）
```bash
python skills/ibgnn/scripts/train_reference.py \
    --atlas aal_116 \
    --labels-csv data/hcp_gender_labels.csv \
    --fold 0 --n-epochs 10 --batch-size 16
```

### 训练（回归，HCP age）
```bash
python skills/ibgnn/scripts/train_reference.py \
    --atlas schaefer_100_7net \
    --labels-csv data/hcp_age_labels.csv \
    --task regression --fold 0 --n-epochs 50
```

---

## 核心文件

| 文件 | 作用 |
|---|---|
| `models/ibgnn/net/ibgnn.py` | 模型定义：MPConv + IBGConv stack + MLP head |
| `models/ibgnn/scripts/data_adapter.py` | 数据适配（薄封装复用 `models.braingnn`） |
| `skills/ibgnn/scripts/train_reference.py` | K-fold CV 训练参考实现 |

---

## 模型架构

```
Input PyG Data (x=[N,N], edge_index, edge_attr, batch)
  -> abs(edge_attr) -> gcn_norm with self-loops
  -> MPConv(N, hidden) + ReLU + Dropout
  -> MPConv(hidden, hidden)  (n_gnn_layers 层)
  -> global_mean_pool (或 sum)
  -> MLP head: Linear(hidden, hidden) + ReLU + shortcut + Linear(hidden, nclass)
Output: logits
```

每条边的消息：`msg(i,j) = Linear([h_i; h_j; edge_weight])`

---

## 关键训练参数

| 参数 | 论文默认 | NeuroClaw 默认 | 说明 |
|---|---|---|---|
| `--lr` | 1e-4 | 1e-3 | 论文 1e-4，对齐其他模型用 1e-3 |
| `--wd` | 1e-5 | 5e-4 | 权重衰减 |
| `--hidden-dim` | 128 | 128 | GNN/MLP 隐藏维度 |
| `--n-gnn-layers` | 2-3 | 2 | MPConv 堆叠层数 |
| `--n-mlp-layers` | 1 | 1 | MLP head 深度 |
| `--pooling` | mean | mean | 'mean' 或 'sum' |
| `--n-epochs` | 100 | 50 | 与其他模型对齐 |
| `--batch-size` | 16 | 16 | |

---

## 调试经验与注意事项

1. **`edge_attr.abs()` 必须**：FC 矩阵带负相关，但 GCN 归一化和消息聚合假设非负权重，否则归一化得到 NaN。
2. **MPConv 参数量**：消息 MLP `Linear(2*hidden+1, hidden)`，每层约 `(2H+1)*H` 参数，比 GCN 重 ~2 倍。
3. **n_gnn_layers 选择**：论文 2-3 层最优；超过 3 层会过平滑。
4. **shortcut connection**：MLP head 内 `h = net(x) + shortcut(x)`，避免深网络梯度衰减。
5. **PyG 2.7 兼容**：使用 `torch_geometric.utils.scatter` 替代已废弃的 `torch_scatter.scatter_add`。
6. **数据复用**：与 BrainGNN 共享 `NeuroClawFCDataset`，无需重复加载/缓存。
7. **Explainer 未移植**：原 repo 的 `main_explainer.py`（GNNExplainer 后处理）暂未移植，若需可补充。

---

## NeuroClaw 委托规则

- ROI 生成和预处理：委托 `fmri-skill`
- HCP 数据下载/编排：委托 `hcpya-skill` / `hcpa-skill` / `hcpd-skill` / `hcpep-skill`
- 依赖检查：`dependency-planner` + `conda-env-manager`
- 执行路由：`claw-shell`

执行前需明确计划确认。

---

## Reference

- Cui H, Dai W, Zhu Y, Li X, He L, Yang C. 2022. Interpretable Graph Neural Networks for Connectome-Based Brain Disorder Analysis. MICCAI.
- Official repository: https://github.com/HennyJie/IBGNN
- BrainGB benchmark by same author: https://github.com/HennyJie/BrainGB
- NeuroClaw BrainGNN skill (共享数据格式): `skills/brain_gnn/SKILL.md`

Created At: 2026-05-19 01:30 HKT
Last Updated At: 2026-05-19 01:30 HKT
Author: chengwang96
