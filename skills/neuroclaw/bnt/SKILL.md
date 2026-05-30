---
name: bnt
description: "Use this model doc whenever the user wants to run BrainNetworkTransformer for fMRI phenotype prediction, including data loading, training, and evaluation. BNT uses dense FC matrices (no PyG dependency) with DEC pooling + interpretable transformer encoder."
license: MIT License (NeuroClaw custom skill - freely modifiable within the project)
layer: base
skill_type: model
dependencies:
  - fmri-skill
  - run_models
---
# BrainNetworkTransformer (BNT) Model Doc

## Overview
BrainNetworkTransformer 是一种基于 Transformer 的脑网络分析模型，使用 DEC (Deep Embedded Clustering) 池化实现可解释的节点聚类。

- Paper: Kan et al., 2022, BrainNetworkTransformer
- Official code: https://github.com/Wayfear/BrainNetworkTransformer
- NeuroClaw reimplementation: `models/bnt/` (无 hydra/omegaconf 依赖，纯 argparse)
- Primary input: ROI-level FC 矩阵（dense [N, N]，非 PyG 图格式）
- Primary output: phenotype prediction (classification/regression) + attention weights + DEC assignments

**Research use only.**

---

## NeuroClaw 实现要点

NeuroClaw 版本对原始 BNT 做了以下关键改动：

1. **去除 hydra/omegaconf 依赖**：原始代码使用 hydra 配置系统，NeuroClaw 改为纯 argparse，降低依赖复杂度。
2. **纯 PyTorch Dataset**：不依赖 PyG，使用标准 `torch.utils.data.Dataset` + `DataLoader`，输入为 dense FC matrix [B, N, N]。
3. **Fisher-z 反变换**：与 BrainGNN 一致，存储的 fc_matrix 是 Fisher-z，加载时用 `torch.tanh()` 还原为 Pearson r，对角线置零。
4. **nhead 自动适配**：当 forward_dim (N + pos_embed_dim) 不能被 nhead 整除时，自动降低 nhead 到最大兼容值。
5. **支持 classification + regression 双任务**：regression 时 nclass=1，输出 raw scalar，用 MSELoss。
6. **可选 T1 GM volume 融合**：`--include-t1` 将 z-scored GM volume 作为额外 1 维拼接到 FC 行末尾（node feature dim 从 N 变为 N+1）。
7. **DEC loss 集成**：训练时自动累加各 pooling 层的 KL 散度 loss，权重可调。
8. **Learnable positional embedding**：默认启用 identity positional encoding (dim=8)，拼接到 node feature 后。

---

## Quick Start (NeuroClaw 内部)

### 前置条件
- conda env: `neuroclaw` (Python 3.11)
- 已有 `data/braingnn_input/<atlas>/sub-*.pt` 文件（由 fmri-skill 生成，BNT 复用同一数据源）
- 可选：`data/t1_volume/<atlas>/sub-*.npz`（GM volume）

### 训练（分类）
```bash
python models/bnt/scripts/train.py \
    --atlas schaefer_100_7net \
    --labels-csv data/hcp_gender_labels.csv \
    --subjects-file data/ready_subjects.txt \
    --fold 0 --kfold 5 \
    --n-epochs 50 --batch-size 32 --lr 0.001 \
    --include-t1
```

### 训练（回归）
```bash
python models/bnt/scripts/train.py \
    --atlas aal_116 \
    --labels-csv data/hcp_age_labels.csv \
    --subject-col subject_id --label-col age \
    --task regression --label-scaling standardization \
    --fold 0 --n-epochs 50
```

### Dry Run（验证数据加载）
```bash
python models/bnt/scripts/train.py --atlas aal_116 --dry-run
```

---

## 核心文件

| 文件 | 作用 |
|---|---|
| `models/bnt/net/bnt.py` | 模型定义：InterpretableTransformerEncoder + DEC pooling + FC head |
| `models/bnt/scripts/data_adapter.py` | 数据加载：NeuroClaw .pt -> PyTorch Dataset (dense FC) |
| `models/bnt/scripts/train.py` | 训练入口：K-fold CV, classification/regression (待创建) |

---

## 数据格式约定

### 输入文件 (`data/braingnn_input/<atlas>/sub-<id>.pt`)
与 BrainGNN 共享同一数据源：
```python
{
    "subject_id": str,
    "atlas": str,
    "n_rois": int,
    "fc_matrix": Tensor[n_roi, n_roi],   # Fisher-z transformed
    "node_features": Tensor[n_roi, n_roi],
    "roi_names": list[str],
}
```

### BNT 内部表示
- 输入 tensor: `[B, N, N]` dense Pearson correlation matrix (tanh 反变换后)
- 若 include_t1: `[B, N, N+1]`（最后一列为 z-scored GM volume）
- 若 pos_encoding="identity": 模型内部拼接为 `[B, N, N+P]`

---

## 模型架构

```
Input FC [B, N, N]
  -> (optional) concat positional embedding -> [B, N, N+P]
  -> TransPoolingEncoder_1 (Transformer + DEC pool: N -> K1)
  -> TransPoolingEncoder_2 (Transformer + DEC pool: K1 -> K2)
  -> dim_reduction: Linear(N+P -> 8) + LeakyReLU
  -> Flatten -> FC head (256 -> 32 -> nclass)
```

默认 sizes: `[N//2, N//10]`（根据 ROI 数自动缩放）

---

## 关键训练参数

| 参数 | 默认值 | 说明 |
|---|---|---|
| `--atlas` | (必填) | atlas 名，需匹配 data/braingnn_input/ 下子目录 |
| `--fold` | 0 | CV fold index |
| `--kfold` | 5 | 总 fold 数 |
| `--n-epochs` | 50 | 训练轮数 |
| `--batch-size` | 32 | batch size（BNT 比 BrainGNN 更轻量，可用更大 batch） |
| `--lr` | 0.001 | 学习率 |
| `--sizes` | auto | DEC pooling 各层节点数，默认 [N//2, N//10] |
| `--pos-embed-dim` | 8 | positional embedding 维度 |
| `--nhead` | 4 | Transformer attention heads（自动适配） |
| `--dec-weight` | 0.1 | DEC KL loss 权重 |
| `--include-t1` | False | 是否融合 T1 GM volume |
| `--task` | classification | classification / regression |

---

## 调试经验与注意事项

1. **nhead 整除问题**：forward_dim = N + pos_embed_dim，必须能被 nhead 整除。模型已自动处理，但若手动指定 nhead 需注意。
2. **DEC encoder 维度**：DEC 内部 encoder 输入为 `input_feature_size * input_node_num`，ROI 数较大时参数量会爆炸。建议 encoder_hidden 保持 32。
3. **数据复用**：BNT 和 BrainGNN 共享 `data/braingnn_input/` 数据源，无需重复预处理。
4. **无 PyG 依赖**：BNT 完全基于标准 PyTorch，不需要 torch_geometric、torch_sparse 等。
5. **Attention 可解释性**：每层 TransPoolingEncoder 存储 attention weights，可用于 ROI 重要性分析。
6. **DEC assignment 可视化**：DEC pooling 的 soft assignment matrix 可映射回 ROI，展示聚类结构。
7. **collate 函数**：使用自定义 `bnt_collate` 返回 (fc_batch, y_batch, sid_list)，不要用默认 collate。
8. **regression 标签标准化**：与 BrainGNN 一致，对 y 做 z-score（基于训练集统计），评估时反变换。

---

## NeuroClaw 委托规则

- ROI 生成和预处理：委托 `fmri-skill`
- HCP 数据下载/编排：委托 `hcpya-skill` / `hcpa-skill` / `hcpd-skill` / `hcpep-skill`
- 依赖检查：`dependency-planner` + `conda-env-manager`
- 执行路由：`claw-shell`

执行前需明确计划确认。

---

## Reference

- Kan X, Dai W, Cui H, Zhang Z, Guo Y, He L. 2022. BrainNetworkTransformer. NeurIPS.
- Official repository: https://github.com/Wayfear/BrainNetworkTransformer
- NeuroClaw BrainGNN skill (共享数据格式): `skills/brain_gnn/SKILL.md`

Created At: 2026-05-15 23:00 HKT
Last Updated At: 2026-05-15 23:00 HKT
Author: chengwang96
