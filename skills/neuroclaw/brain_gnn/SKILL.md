---
name: braingnn
description: "Use this model doc whenever the user wants to run BrainGNN for fMRI phenotype prediction, including graph construction, training, and evaluation. This document focuses on model-level usage and delegates upstream preprocessing to fmri-skill (and optionally hcpya-skill for HCP data)."
license: MIT License (NeuroClaw custom skill - freely modifiable within the project)
layer: base
skill_type: model
dependencies:
  - fmri-skill
  - run_models
---
# BrainGNN Model Doc

## Overview
BrainGNN is an interpretable graph neural network for fMRI analysis and phenotype prediction.

- Paper: Li et al., 2020, BrainGNN
- Official code: https://github.com/xxlya/BrainGNN_Pytorch/tree/main
- NeuroClaw reimplementation: `models/braingnn/` (Windows-compatible, 无需 torch_sparse)
- Primary input: ROI-level fMRI connectivity matrices (per-subject .pt files)
- Primary output: phenotype prediction (classification/regression) + interpretable pooling scores

**Research use only.**

---

## NeuroClaw 实现要点

NeuroClaw 版本对原始 BrainGNN 做了以下关键改动：

1. **去除 torch_sparse 依赖**：`augment_adj` 不再使用 `spspmm` 做邻接矩阵平方，改用 `add_self_loops + remove_self_loops`，在 Windows 上可直接运行。
2. **全连接输入图**：data_adapter 构建 FULL graph（所有 i!=j 对），edge_attr = |Pearson r|。TopKPooling 负责选择，不在输入端做稀疏化。
3. **Fisher-z 反变换**：存储的 fc_matrix 是 Fisher-z，加载时用 `torch.tanh()` 还原为 Pearson r，对角线置零。
4. **支持 classification + regression 双任务**：通过 `--task` 参数切换，regression 时 nclass=1，输出 raw scalar，用 MSELoss。
5. **PyG >=2.3 兼容**：TopKPooling.weight 可能在 `pool.select.weight`，forward 中做了兼容处理。
6. **可选 T1 GM volume 融合**：`--include-t1` 将 z-scored GM volume 作为额外 1 维 node feature 拼接。

---

## Quick Start (NeuroClaw 内部)

### 前置条件
- conda env: `neuroclaw` (Python 3.11)
- 已有 `data/braingnn_input/<atlas>/sub-*.pt` 文件（由 fmri-skill 生成）
- 可选：`data/t1_volume/<atlas>/sub-*.npz`（GM volume）

### 训练（分类）
```bash
python models/braingnn/scripts/train.py \
    --atlas schaefer_100_7net \
    --labels-csv data/hcp_gender_labels.csv \
    --subjects-file data/ready_subjects.txt \
    --fold 0 --kfold 5 \
    --n-epochs 50 --batch-size 16 --lr 0.005 \
    --include-t1
```

### 训练（回归）
```bash
python models/braingnn/scripts/train.py \
    --atlas aal_116 \
    --labels-csv data/hcp_age_labels.csv \
    --subject-col subject_id --label-col age \
    --task regression --label-scaling standardization \
    --fold 0 --n-epochs 50
```

### Atlas Sweep（快速对比）
```bash
python models/braingnn/scripts/sweep_atlases.py
```
对所有可用 atlas 跑 fold 0，输出 CSV 对比表。

### Dry Run（验证数据加载）
```bash
python models/braingnn/scripts/train.py --atlas aal_116 --dry-run
```

---

## 核心文件

| 文件 | 作用 |
|---|---|
| `models/braingnn/net/braingnn.py` | 模型定义：MyNNConv + TopKPooling + FC head + loss functions |
| `models/braingnn/scripts/data_adapter.py` | 数据加载：NeuroClaw .pt -> PyG InMemoryDataset |
| `models/braingnn/scripts/train.py` | 训练入口：K-fold CV, classification/regression |
| `models/braingnn/scripts/sweep_atlases.py` | Atlas 对比扫描脚本 |

---

## 数据格式约定

### 输入文件 (`data/braingnn_input/<atlas>/sub-<id>.pt`)
```python
{
    "subject_id": str,
    "atlas": str,
    "n_rois": int,
    "time_series": Tensor[T, n_roi],
    "fc_matrix": Tensor[n_roi, n_roi],   # Fisher-z transformed
    "node_features": Tensor[n_roi, n_roi],
    "edge_index": Tensor[2, n_edge],
    "edge_attr": Tensor[n_edge, 1],
    "roi_names": list[str],
}
```

### 可选 T1 文件 (`data/t1_volume/<atlas>/sub-<id>.npz`)
```python
{
    "subject_id": str,
    "atlas": str,
    "n_rois": int,
    "roi_names": list[str],
    "gm_volume_mm3": ndarray[n_roi],
    "gm_fraction": ndarray[n_roi],
}
```

### 输出 checkpoint (`models/braingnn/checkpoints/<atlas>/fold<N>.pt`)
```python
{
    "state_dict": OrderedDict,
    "args": dict,
    "best_val_acc": float,  # classification
    "test_acc": float,
    "n_roi": int,
    "indim": int,
}
```

---

## 关键训练参数

| 参数 | 默认值 | 说明 |
|---|---|---|
| `--atlas` | (必填) | atlas 名，需匹配 data/braingnn_input/ 下子目录 |
| `--fold` | 0 | CV fold index |
| `--kfold` | 5 | 总 fold 数（自动根据最小类别数调整） |
| `--n-epochs` | 50 | 训练轮数 |
| `--batch-size` | 16 | batch size |
| `--lr` | 0.01 | 学习率 |
| `--ratio` | 0.5 | TopKPooling 保留比例 |
| `--n-communities` | 8 | MyNNConv 中间层 community 数 |
| `--include-t1` | False | 是否融合 T1 GM volume |
| `--task` | classification | classification / regression |
| `--lamb3/4/5` | 0.1 | topk_loss 和 consist_loss 权重 |

---

## 调试经验与注意事项

1. **indim/nroi 自动推断**：train.py 从第一个样本自动获取 `n_roi` 和 `indim`，无需手动指定。
2. **PyG cache 问题**：修改数据后需删除 `data/braingnn_cache/<atlas>/` 目录，否则会加载旧缓存。sweep_atlases.py 已自动处理。
3. **edge_attr 维度**：augment_adj 后 edge_attr 可能变为 1D，pool 层需要 squeeze 处理（已在 forward 中处理）。
4. **小样本 kfold 自动调整**：当最小类别样本数 < kfold 时，自动降低 kfold 避免 StratifiedKFold 报错。
5. **regression 标签标准化**：默认对 y 做 z-score（基于训练集统计），评估时反变换回原始尺度。
6. **softmax 在 message 中**：MyNNConv 对 edge_weight 做 softmax attention，因此输入 edge_attr 必须为非负值（|Pearson r|）。
7. **ROI mask 支持**：data_adapter 支持 `roi_mask` 参数做子图选择，用于消融实验。

---

## NeuroClaw 委托规则

- ROI 生成和预处理：委托 `fmri-skill`
- HCP 数据下载/编排：委托 `hcpya-skill` / `hcpa-skill` / `hcpd-skill` / `hcpep-skill`
- 依赖检查：`dependency-planner` + `conda-env-manager`
- 执行路由：`claw-shell`

执行前需明确计划确认。

---

## Reference

- Li X, Zhou Y, Dvornek N, Zhang M, Gao S, Zhuang J, Scheinost D, Staib L, Ventola P, Duncan J. 2020. BrainGNN.
- Official repository: https://github.com/xxlya/BrainGNN_Pytorch/tree/main
- PyG installation notes: https://pytorch-geometric.readthedocs.io/en/latest/notes/installation.html

Created At: 2026-03-28 19:53 HKT
Last Updated At: 2026-05-15 22:50 HKT
Author: chengwang96
