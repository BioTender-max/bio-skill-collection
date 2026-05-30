---
name: combraintf
description: "Use this model doc whenever the user wants to run Com-BrainTF (Community-aware Brain Transformer) for fMRI phenotype prediction. Com-BrainTF uses dense FC matrices with a two-level Transformer (per-community local + global) and DEC pooling. NeuroClaw auto-derives community partitions from atlas naming conventions (Yeo 7-net for Schaefer, lobe-based for AAL)."
license: MIT License (NeuroClaw custom skill - freely modifiable within the project)
layer: base
skill_type: model
dependencies:
  - fmri-skill
  - run_models
---
# Com-BrainTF Model Doc

## Overview
Com-BrainTF (Community-aware Brain Transformer) 是一种针对 fMRI 连接组的两级 Transformer。第一级对每个脑功能社区（如 Yeo 7-network）内的 ROI 独立做 self-attention，并为每个社区维护一个可学习的 CLS token；第二级把所有社区的 CLS + 全部 ROI 节点拼接，再过一个带 DEC 池化的 Transformer，最后展平进 FC head。

- Paper: Bannadabhavi et al., 2023, "Community-Aware Transformer for Autism Prediction in fMRI Connectome"，MICCAI
- Official code: https://github.com/ubc-tea/Com-BrainTF
- NeuroClaw reimplementation: `models/combraintf/`（去除 hydra/omegaconf 与硬编码 node_clus_map，改为运行时从 atlas 推导）
- Primary input: dense FC 矩阵 [B, N, N]
- Primary output: phenotype prediction + DEC assignment + per-level attention

**Research use only.**

---

## NeuroClaw 实现要点

1. **去除 hydra/omegaconf**：原版用 hydra 配置 + DictConfig，NeuroClaw 改为纯 Python 构造函数，所有参数显式传入。
2. **动态 community partition**：原版从 `node_clus_map.pickle` 加载 Schaefer-400 的固定社区映射；NeuroClaw 在 `data_adapter.py::build_community_ids(atlas)` 里根据 ROI 名自动推导：
   - `schaefer_*_7net` → Yeo 7-network（Vis/SomMot/DorsAttn/SalVentAttn/Limbic/Cont/Default）+ Unknown 兜底，共 8 组
   - `aal_*` / `destrieux` / `dk_*` / `harvard_oxford_*` → 7 lobe + Other = 8 组
   - 其他无语义命名的 atlas（cc200/glasser/basc/power/msdl）→ MD5 hash round-robin 8 组兜底
3. **支持任意 atlas**：上层只需传 `community_ids: list[int]`（长度 = n_roi），模型自动按社区分组、独立 local transformer。
4. **每社区独立 CLS token**：与原版一致，每个社区一个 `nn.Parameter([1, d_model])`，由 `local_transformers[k]` 持有。
5. **任务统一接口**：classification (`nclass=N`) 与 regression (`nclass=1, task='regression'`)。
6. **数据复用**：直接复用 BNT 的 `BNTDataset` + `bnt_collate`，无需额外预处理。

---

## Quick Start (NeuroClaw 内部)

### 前置条件
- conda env: `neuroclaw` (Python 3.11)
- 已有 `data/braingnn_input/<atlas>/sub-*.pt` 文件（与 BNT/BrainGNN 共享）

### 训练（分类，单 fold 冒烟测试）
```bash
python skills/combraintf/scripts/train_reference.py \
    --atlas schaefer_200_7net \
    --labels-csv data/hcp_gender_labels.csv \
    --fold 0 --n-epochs 10 --batch-size 8
```

### 训练（回归，HCP age）
```bash
python skills/combraintf/scripts/train_reference.py \
    --atlas aal_116 \
    --labels-csv data/hcp_age_labels.csv \
    --task regression --fold 0 --n-epochs 50
```

### 推荐 atlas
- **最优**：`schaefer_200_7net` 或 `schaefer_400_7net`（原生 Yeo 7-net 命名，社区分组最干净）
- **可用**：`aal_116`、`aal3_166`（lobe-based 8 组，可解释性好）
- **兜底**：其他 atlas 用 MD5 hash 分组，效果可能不如有语义的 atlas

---

## 核心文件

| 文件 | 作用 |
|---|---|
| `models/combraintf/net/combraintf.py` | 模型定义：Local TransPoolingEncoder ×K + Global TransPoolingEncoder + DEC pool + FC head |
| `models/combraintf/scripts/data_adapter.py` | 数据适配（薄封装 `models.bnt`）+ `build_community_ids(atlas)` + `get_community_ids(atlas)` |
| `skills/combraintf/scripts/train_reference.py` | K-fold CV 训练参考实现 |

---

## 模型架构

```
Input FC [B, N, N]
  -> 按 community_ids 重排 row & col（保持对称）
  -> 第一级：每个社区 k 一个 TransPoolingEncoder (local_transformer=True)
       - 拼 CLS token -> Transformer -> 输出 (节点特征, CLS)
  -> 收集 K 个 CLS token -> Linear -> 全局 CLS
  -> 拼回 [B, N+1, d_model]
  -> 第二级：TransPoolingEncoder (DEC pool: N+1 -> n_clusters)
  -> dim_reduce(d_model -> 8) + LeakyReLU
  -> flatten -> FC head (256 -> 32 -> nclass)
Output: (logits, assignment)
```

---

## 关键训练参数

| 参数 | 论文默认 | NeuroClaw 默认 | 说明 |
|---|---|---|---|
| `--lr` | 1e-4 | 1e-3 | 论文 1e-4，对齐其他模型用 1e-3 |
| `--wd` | 1e-4 | 5e-4 | 权重衰减 |
| `--hidden-size` | 1024 | 512 | Transformer FFN 维度 |
| `--nhead` | 8 | 4 | 多头注意力数（必须能整除 d_model = n_roi） |
| `--n-clusters` | 8 | 8 | DEC pool 输出聚类数 |
| `--dec-weight` | 0.1 | 0.1 | DEC KL loss 权重 |
| `--n-epochs` | 200 | 50 | 与其他模型对齐 |
| `--batch-size` | 16 | 8 | 比 BNT 重，参数量更大 |

---

## 调试经验与注意事项

1. **nhead 整除 d_model**：d_model = n_roi，必须能被 nhead 整除。Schaefer_200/4/8 都 OK，AAL_116/4 也 OK，但奇数 ROI 数（如 cc200 实际 190）需调 nhead。
2. **每社区 CLS 独立**：每个社区一个 `local_transformer`（含独立 CLS 参数），但 Transformer 层本身可共享或独立。NeuroClaw 实现为完全独立（每社区 1 个 TransformerEncoderLayer），略多参数但更易调试。
3. **community 边界顺序**：模型按 community_ids 排序，每个 community 的 ROI 必须连续。`get_community_ids` 返回的 list 内部数字未必连续，模型构造时会重排索引。
4. **n_communities 推导**：默认从 `set(community_ids)` 大小取，无需显式传。
5. **memory 占用**：local transformer 数 × hidden_size × d_model^2 量级，glasser_360 + hidden=1024 容易爆显存，建议 hidden=512 + batch=4。
6. **DEC orthogonal init**：保持论文默认 `orthogonal=True, freeze_center=True, project_assignment=True`，否则训练不稳定。
7. **assignment 可视化**：DEC 输出 [B, N+1, n_clusters] soft assignment，可用于社区→功能子网络映射的可视化。

---

## NeuroClaw 委托规则

- ROI 生成和预处理：委托 `fmri-skill`
- HCP 数据下载/编排：委托 `hcpya-skill` / `hcpa-skill` / `hcpd-skill` / `hcpep-skill`
- 依赖检查：`dependency-planner` + `conda-env-manager`
- 执行路由：`claw-shell`

执行前需明确计划确认。

---

## Reference

- Bannadabhavi A, Lee S, Deng W, Ying R, Li X. 2023. Community-Aware Transformer for Autism Prediction in fMRI Connectome. MICCAI.
- Official repository: https://github.com/ubc-tea/Com-BrainTF
- NeuroClaw BNT skill (共享数据格式): `skills/bnt/SKILL.md`

Created At: 2026-05-19 01:30 HKT
Last Updated At: 2026-05-19 01:30 HKT
Author: chengwang96
