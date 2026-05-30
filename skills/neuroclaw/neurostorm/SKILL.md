---
name: neurostorm
description: "Use this skill whenever the user wants to run the NeuroSTORM multi-model fMRI platform: preprocessing, pretraining (MAE or contrastive), fine-tuning, inference, or benchmarking. It covers 8 built-in models — NeuroSTORM, SwiFT, BrainGNN, BrainNetworkTransformer (BNT), LG-GNN, Com-BrainTF, IBGNN, BrainNetCNN — across 3 input modalities (voxel 4D, ROI time series 2D, functional connectivity 2D). Triggers include: 'fMRI', 'NeuroSTORM', 'SwiFT', 'BrainGNN', 'BNT', 'BrainNetCNN', 'LG-GNN', 'Com-BrainTF', 'IBGNN', 'fMRI preprocessing', 'fMRI foundation model', 'ROI time series', 'functional connectivity', 'brain graph', 'HCP', 'ABCD', 'UKB', 'ADHD200', 'COBRE', 'UCLA', 'NSD', 'BOLD5000', 'disease diagnosis from fMRI', 'pretrain fMRI model', 'fine-tune fMRI', or any request involving .nii/.nii.gz fMRI volume files."
license: MIT
layer: base
skill_type: model
dependencies:
  - fmri-skill
  - smri-skill
  - run_models
---
# NeuroSTORM Skill

## Overview

`neurostorm-skill` wraps the unified **NeuroSTORM fMRI platform** (CUHK-AIM-Group), which, as of the 2026-05-08 release, ships **8 model implementations** under a single training/fine-tuning entry point. Use this skill for the full lifecycle: data download, preprocessing, pretraining, fine-tuning, and inference.

**Supported models (8)**

| Model | Input type | Graph? | Backbone |
|-------|-----------|--------|----------|
| `neurostorm` | voxel (4D) | No | Mamba-SSM |
| `swift` | voxel (4D) | No | Swin 4D Transformer |
| `braingnn` | FC graph (2D) | Yes | GNN |
| `bnt` | FC matrix (2D) | No | Transformer |
| `lggnn` | ROI + FC | Yes | Learnable GNN |
| `combraintf` | FC matrix (2D) | No | Community-aware Transformer |
| `ibgnn` | FC graph (2D) | Yes | Interpretable GNN |
| `brainnetcnn` | FC matrix (2D) | No | CNN |

**Supported tasks**

| ID | Task |
|----|------|
| 1 | Age & Gender Prediction |
| 2 | Phenotype Prediction |
| 3 | Disease Diagnosis |
| 4 | fMRI Retrieval |
| 5 | Task fMRI State Classification |

**Supported datasets:** HCP1200, ABCD, UKB, Cobre, ADHD200, HCPA, HCPD, UCLA, HCPEP, HCPTASK, GOD, NSD, BOLD5000.

**Dual data formats:** `PT` (faster random access, larger disk) and `H5` (compact, scales to large cohorts). Choose at preprocessing and at training via `--output_format` / `--data_format`.

---

## Installation

Use the upstream `requirements.txt` + `set_env.sh` flow (Python 3.11, CUDA 12.8, PyTorch 2.7.1).

```bash
# 1. Clone and enter
git clone https://github.com/CUHK-AIM-Group/NeuroSTORM.git
cd NeuroSTORM

# 2. Create and activate env
conda create -n neurostorm python=3.11
conda activate neurostorm

# 3. Auto-detect conda + CUDA paths, set TORCH_CUDA_ARCH_LIST
source ./set_env.sh

# 4. Core dependencies
pip install -r requirements.txt
pip install "setuptools<81"               # pytorch-lightning 1.9.4 compat
pip install "transformers<=4.39.3"        # mamba-ssm compat

# 5. Graph-based models (BrainGNN / LG-GNN / IBGNN)
pip install torch-geometric
pip install torch-scatter torch-sparse -f https://data.pyg.org/whl/torch-2.7.0+cu128.html

# 6. FC-based models (BNT / BrainNetCNN / Com-BrainTF)
pip install scikit-learn pandas h5py deepdish

# 7. Mamba-SSM (NeuroSTORM only)
bash scripts/install_mamba.sh
#   or manually: causal-conv1d v1.5.0.post8, mamba v2.2.2
#   both built with TORCH_CUDA_ARCH_LIST matching your GPU (12.0 Blackwell,
#   9.0 H100, 8.9 4090, 8.6 3090, 8.0 A100)
```

**Docker alternative:**

```bash
docker build -t neurostorm:latest .
docker run --gpus all -it --rm -v $(pwd):/workspace --shm-size=8g neurostorm:latest
```

**Verify:**

```bash
python -c "import torch; print(torch.cuda.is_available())"
python -c "import torch_geometric; print('PyG OK')"
python -c "from mamba_ssm import Mamba; print('Mamba OK')"
python -c "from models.neurostorm import NeuroSTORM; print('NeuroSTORM OK')"
```

Full details: upstream `INSTALLATION.md`.

---

## Workflows

### 1. Data Preprocessing

Assume raw fMRI is in MNI152 space (apply FSL / fMRIPrep / HCP pipelines first).

```bash
# 1a. Brain extraction (optional, FSL BET)
bash datasets/brain_extraction.sh /path/to/raw /path/to/extracted

# 1b. Volume preprocessing — 4D voxel tensors for NeuroSTORM / SwiFT
python datasets/preprocessing_volume.py \
    --dataset_name hcp \
    --load_root ./data/hcp \
    --save_root ./processed_data/hcp \
    --output_format pt \                  # or h5 for large cohorts
    --num_processes 8

# 1c. Extract ROI time series — for all graph / FC models
python datasets/generate_roi_data_from_nii.py \
    --atlas_names cc200 \
    --dataset_names hcp \
    --output_dir ./processed_data \
    --num_processes 32

# 1d. Compute functional connectivity — for BrainGNN / BNT / Com-BrainTF / IBGNN / BrainNetCNN
python datasets/compute_fc.py \
    --roi_dir ./processed_data/roi/cc200 \
    --output_dir ./processed_data/fc/cc200 \
    --atlas_name cc200 \
    --fc_types correlation partial_correlation \
    --num_processes 8
```

Auxiliary scripts: `datasets/compute_stats_and_mask.py`, `datasets/compute_atlas_map.py`.

---

### 2. Pretraining

NeuroSTORM supports two pretraining strategies via `main.py`.

**MAE pretraining (NeuroSTORM):**

```bash
python main.py \
    --dataset_name HCP1200 \
    --image_path ./data/HCP1200_MNI_to_TRs_minmax \
    --model neurostorm \
    --pretraining \
    --use_mae \
    --mask_ratio 0.75 \
    --batch_size 16 \
    --learning_rate 1e-4 \
    --max_epochs 100 \
    --loggername tensorboard \
    --project_name pt_neurostorm_mae
```

**Contrastive pretraining (SwiFT-style):**

```bash
python main.py \
    --dataset_name HCP1200 \
    --image_path ./data/HCP1200_MNI_to_TRs_minmax \
    --model swift \
    --pretraining \
    --use_contrastive \
    --contrastive_type 3 \
    --batch_size 16 \
    --learning_rate 1e-4 \
    --max_epochs 100
```

Ready-made scripts in `scripts/hcp_pretrain/`.

---

### 3. Fine-tuning

The same `main.py` handles every model; switch with `--model` and (for graph/FC models) `--data_type` / `--atlas_name` / `--fc_type` / `--num_rois`.

**NeuroSTORM — gender classification:**

```bash
python main.py \
    --dataset_name HCP1200 \
    --image_path ./data/HCP1200_MNI_to_TRs_minmax \
    --model neurostorm \
    --load_model_path ./pretrained_models/neurostorm_mae.pth \
    --downstream_task_type classification \
    --task_name sex \
    --num_classes 2 \
    --batch_size 32 \
    --learning_rate 5e-5 \
    --max_epochs 50
```

**NeuroSTORM — age regression (with label standardization):**

```bash
python main.py \
    --model neurostorm \
    --downstream_task_type regression \
    --task_name age \
    --num_classes 1 \
    --label_scaling_method standardization \
    --dataset_name HCP1200 --image_path ./data/HCP1200_MNI_to_TRs_minmax \
    --batch_size 32 --learning_rate 1e-3 --max_epochs 50
```

**BrainGNN (FC graph input):**

```bash
python main.py \
    --model braingnn \
    --data_type fc_graph \
    --atlas_name cc200 \
    --fc_type partial_correlation \
    --num_rois 200 \
    --dataset_name HCP1200 --image_path ./data/HCP1200_MNI_to_TRs_minmax \
    --downstream_task_type classification --task_name sex --num_classes 2 \
    --batch_size 32
```

**BrainNetworkTransformer (BNT, hierarchical pooling):**

```bash
python main.py \
    --model bnt \
    --data_type fc_bnt \
    --atlas_name cc200 \
    --num_rois 200 \
    --pooling_sizes 100 50 25 \
    --do_pooling True True False \
    --dataset_name HCP1200 --image_path ./data/HCP1200_MNI_to_TRs_minmax \
    --downstream_task_type classification --task_name sex --num_classes 2
```

**BrainNetCNN:**

```bash
python main.py \
    --model brainnetcnn \
    --data_type fc_bnt \
    --atlas_name cc200 --num_rois 200 \
    --dataset_name HCP1200 --image_path ./data/HCP1200_MNI_to_TRs_minmax \
    --downstream_task_type classification --task_name sex --num_classes 2
```

**LG-GNN, Com-BrainTF, IBGNN**: same pattern — set `--model` and choose the matching `--data_type` (`fc_graph` for GNNs, `fc_bnt` for transformer/CNN FC inputs). See `scripts/run_braingnn.sh`, `scripts/run_bnt.sh`, and other `scripts/*_downstream/` folders for templates.

**Useful fine-tuning flags**

| Flag | Purpose |
|------|---------|
| `--data_format {auto,pt,h5}` | select preprocessed file format |
| `--load_model_path` | load pretrained backbone weights |
| `--freeze_feature_extractor` | freeze backbone, train head only |
| `--resume_ckpt_path` | resume from Lightning checkpoint |
| `--use_scheduler --milestones 50 100` | multi-step LR |
| `--optimizer AdamW --weight_decay 0.01` | switch optimizer |
| `--augment_during_training` + `--augment_only_affine` / `--augment_only_intensity` | data augmentation |
| `--gpu_ids 0,1,2` / `--num_gpus 4` | GPU selection (DDP auto when >1) |
| `--loggername tensorboard --project_name NAME` | logging |

---

### 4. Inference / Demo

**Single subject:**

```bash
python demo.py \
    --mode single \
    --ckpt_path ./pretrained_models/gender.ckpt \
    --fmri_path ./data/HCP1200_MNI_to_TRs_minmax/img/100206 \
    --task gender
```

Task options include `age`, `gender`, `phenotype` (with `--phenotype_name` + `--phenotype_type`).

**Batch inference on a test split:**

```bash
python demo.py \
    --mode dataset \
    --ckpt_path /path/to/model.ckpt \
    --task age \
    --image_path /path/to/preprocessed/data
```

Or run the bundled script: `sh scripts/run_demo.sh`.

---

## Input / Output Summary

| Stage | Input | Output |
|-------|-------|--------|
| Preprocessing (volume) | `.nii` / `.nii.gz` in MNI152 | `.pt` or `.h5` 4D tensors |
| Preprocessing (ROI) | `.nii` + atlas | ROI time series `.pt`/`.h5` |
| Preprocessing (FC) | ROI time series | FC matrices (correlation / partial) |
| Pretraining | Preprocessed voxel tensors | `.pth` / `.ckpt` |
| Fine-tuning | Preprocessed data + pretrained `.pth` | Fine-tuned `.ckpt` + TensorBoard logs |
| Inference | Preprocessed data + `.ckpt` | Predictions (stdout / file) |

---

## Testing

Upstream ships a full `pytest` suite and GitHub Actions CI.

```bash
make test           # full suite
make test-cov       # with coverage
make test-unit      # unit tests only
make ci             # local CI dry-run
```

Key test modules: `test_model_loading.py`, `test_dual_format.py`, `test_atlas_masking.py`.

---

## Directory Reference (upstream)

```
NeuroSTORM/
├── main.py                 entry point for pretraining + fine-tuning
├── demo.py                 unified single-file and dataset inference
├── set_env.sh              auto-detect conda/CUDA paths
├── Makefile                test / dev commands
├── requirements.txt
├── INSTALLATION.md         detailed install
├── USER_GUIDE.md           full usage guide
├── datasets/
│   ├── preprocessing_volume.py
│   ├── generate_roi_data_from_nii.py
│   ├── compute_fc.py
│   ├── fmri_datasets.py    voxel dataset loaders
│   └── roi_datasets.py     ROI + FC loaders
├── models/
│   ├── neurostorm.py  swift.py  braingnn.py  bnt.py
│   ├── lggnn.py  combraintf.py  ibgnn.py  brainnetcnn.py
│   ├── heads/{cls,reg,emb}_head.py
│   ├── load_model.py
│   └── lightning_model.py
├── scripts/
│   ├── hcp_pretrain/  hcp_downstream/
│   ├── install_mamba.sh  run_demo.sh
│   ├── run_braingnn.sh  run_bnt.sh
│   └── dataset_download/
└── tests/                   pytest suite, runs in GitHub Actions CI
```

---

## Reference

- Paper: *Towards a General-Purpose Foundation Model for fMRI Analysis*, Wang et al., Nature Biomedical Engineering, 2026. https://www.nature.com/articles/s41551-026-01666-y
- Project: https://cuhk-aim-group.github.io/NeuroSTORM/
- GitHub: https://github.com/CUHK-AIM-Group/NeuroSTORM
- Upstream docs: `INSTALLATION.md`, `USER_GUIDE.md`

Model attributions: SwiFT (Transconnectome), BrainGNN (LifangHe), BNT (Wayfear), LG-GNN (cnuzh), Com-BrainTF (ubc-tea), IBGNN (HennyJie), BrainNetCNN (nicofarr).

---

Created At: 2026-04-02 00:23 HKT
Last Updated At: 2026-05-11 20:45 HKT  (synced to upstream 2026-05-08 release: +7 models, dual PT/H5, FC pipeline, pytest suite)
Author: chengwang96
