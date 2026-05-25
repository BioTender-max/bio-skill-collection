---
name: ehr-analysis
description: End-to-end EHR predictive modeling pipeline with PyHealth, covering dataset loading, task definition, model training, evaluation, calibration, and clinical interpretation.
tool_type: python
primary_tool: pyhealth
---

# EHR Analysis

## Version Compatibility

Reference examples assume:

- `pyhealth` 1.1.6+ (stable) or 2.0+ (latest, requires Python ≥ 3.12)
- `torch` 2.0+
- `pandas` 2.0+

Verify the runtime first:

- Python: `python -c "import pyhealth; print(pyhealth.__version__)"`
- CLI: `pip show pyhealth`
- If APIs differ between 1.x and 2.x, consult the installed docs and adapt the pattern accordingly.


## Overview

Use this skill when the user needs to:

- load and structure EHR data from MIMIC-III, MIMIC-IV, eICU, OMOP-CDM, or a custom dataset
- define clinical prediction tasks such as mortality, readmission, length of stay, or drug recommendation
- train and evaluate deep learning or ML models on patient visit sequences
- apply medical code normalization, ontology mapping, or tokenization
- calibrate model outputs or generate post-hoc interpretability artifacts

## When To Use This Skill

- the data source is a structured EHR database or tabular patient record export
- the task requires longitudinal patient visit sequences as model input
- the user needs benchmark-compatible evaluation metrics for clinical AI
- medical code systems (ICD, ATC, NDC, CPT, CCS) must be normalized or mapped before modeling

## Quick Route

- Known EHR source (MIMIC, eICU, OMOP): load with a `pyhealth.datasets` class, then `set_task`.
- Custom tabular data: wrap in `SampleBaseDataset`, then follow the same pipeline.
- Code mapping only: use `pyhealth.medcode` independently without the full pipeline.
- Evaluation only: use `pyhealth.metrics` independently on existing predictions.

## Progressive Disclosure

- Read `references/technical_reference.md` for dataset branching rules, task schema details, model selection guidance, and calibration caveats.
- Read `references/commands_and_thresholds.md` for concrete PyHealth code patterns, recommended thresholds, and output file conventions.
- Keep `SKILL.md` as the main execution path and load reference files only when the task or failure mode needs the extra detail.

## Default Rules

- Always use raw integer counts or visit-level code lists as model inputs; do not pre-aggregate before loading.
- Keep dataset loading, task definition, model training, and evaluation as separate, inspectable stages.
- Record dataset name, table selections, code mapping applied, task function, model class, and PyHealth version in every experiment.
- Favor reproducible train/val/test splits via `split_by_patient` over random splits that can leak patient data.

## Expected Inputs

- EHR source files or database dumps (MIMIC-III, MIMIC-IV, eICU, OMOP-CDM, or custom CSV/Parquet)
- table names to load (e.g., `diagnoses_icd`, `procedures_icd`, `prescriptions`)
- optional medical code mapping specifications
- task definition (predefined or custom)
- model architecture choice and training hyperparameters

## Expected Outputs

- `results/model_checkpoint.pth`
- `results/test_metrics.json`
- `results/predictions.tsv`
- `qc/dataset_stats.tsv`
- `figures/calibration_curve.pdf`
- `figures/feature_importance.pdf`

## Preferred Tools

- `pyhealth.datasets` — MIMIC3Dataset, MIMIC4Dataset, eICUDataset, OMOPDataset, SampleBaseDataset
- `pyhealth.tasks` — MortalityPrediction, ReadmissionPrediction, DrugRecommendation, LengthOfStayPrediction, and custom task functions
- `pyhealth.models` — RNN, LSTM, GRU, Transformer, RETAIN, SafeDrug, GAMENet, AdaCare, ConCare, StageNet
- `pyhealth.trainer` — Trainer
- `pyhealth.metrics` — binary, multiclass, multilabel, fairness, interpretability metrics
- `pyhealth.medcode` — InnerMap, CrossMap for ontology lookup and code mapping
- `pyhealth.tokenizer` — Tokenizer for code-to-index transformations
- `pyhealth.calib` — calibration and prediction set construction

## Starter Pattern

```python
from pyhealth.datasets import MIMIC3Dataset
from pyhealth.tasks import drug_recommendation_mimic3_fn
from pyhealth.datasets import split_by_patient, get_dataloader
from pyhealth.models import Transformer
from pyhealth.trainer import Trainer

# Step 1: load dataset
dataset = MIMIC3Dataset(
    root="/path/to/mimic3/",
    tables=["DIAGNOSES_ICD", "PROCEDURES_ICD", "PRESCRIPTIONS"],
    code_mapping={"NDC": ("ATC", {"target_kwargs": {"level": 3}})},
)

# Step 2: define task
samples = dataset.set_task(task_fn=drug_recommendation_mimic3_fn)

# Step 3: split and build dataloaders
train_ds, val_ds, test_ds = split_by_patient(samples, [0.8, 0.1, 0.1])
train_loader = get_dataloader(train_ds, batch_size=32, shuffle=True)
val_loader   = get_dataloader(val_ds,   batch_size=32, shuffle=False)
test_loader  = get_dataloader(test_ds,  batch_size=32, shuffle=False)

# Step 4: initialize model
model = Transformer(
    dataset=samples,
    feature_keys=["conditions", "procedures"],
    label_key="drugs",
    mode="multilabel",
)

# Step 5: train
trainer = Trainer(model=model)
trainer.train(
    train_dataloader=train_loader,
    val_dataloader=val_loader,
    epochs=50,
    monitor="pr_auc_samples",
)

# Step 6: evaluate
metrics = trainer.evaluate(test_loader)
print(metrics)
```

## Workflow

### 1. Validate dataset access and structure

Confirm the EHR source is accessible and the required tables are present. Inspect patient counts, visit counts, and code distributions before building tasks.

### 2. Load data with `pyhealth.datasets`

Use the appropriate dataset class. Apply code mappings at load time so downstream tasks and models operate on a consistent vocabulary. Record which tables and mappings were used.

### 3. Define the clinical task

Choose a predefined task function or write a custom one. Confirm the input schema (feature keys and types) and output schema (label key and mode: binary, multiclass, or multilabel) match the clinical question.

### 4. Split patients and build dataloaders

Always split by patient, not by visit or row, to prevent patient-level data leakage. Use `split_by_patient` and `get_dataloader` from `pyhealth.datasets`.

### 5. Initialize and train the model

Select an architecture matched to the task and data size. Configure `feature_keys`, `label_key`, and `mode` explicitly. Use `Trainer` for training, validation monitoring, and checkpoint saving.

### 6. Evaluate and report

Compute task-appropriate metrics using `pyhealth.metrics`. For binary tasks report AUROC and AUPRC. For multilabel tasks report Jaccard and PR-AUC. Export a metrics JSON and a predictions TSV alongside the model checkpoint.

### 7. Calibrate and interpret where needed

Apply calibration from `pyhealth.calib` when predicted probabilities will be used for clinical decision support. Use `pyhealth.interpret` for feature-level or visit-level attribution when the use case requires explainability.


## Output Artifacts

```text
results/
├── model_checkpoint.pth
├── test_metrics.json
└── predictions.tsv
qc/
├── dataset_stats.tsv
└── split_summary.tsv
figures/
├── calibration_curve.pdf
└── feature_importance.pdf
```


## Key Parameters

| Parameter | Typical value | Notes |
|---|---|---|
| `batch_size` | `32` | reduce for large visit sequences or memory-constrained environments |
| `epochs` | `50` | use early stopping via `monitor` metric |
| `monitor` | `"pr_auc_samples"` for multilabel; `"roc_auc"` for binary | task-dependent |
| `split_by_patient` ratios | `[0.8, 0.1, 0.1]` | always split by patient not by visit |
| code mapping level | ATC level 3 for drug codes | balance specificity and sparsity |
| `n_top_genes` (HVG analog) | N/A for EHR; use vocabulary filtering | filter rare codes with `min_count` |


## Quality Review

- Confirm patient count, visit count, and code vocabulary size before training.
- Verify that train, validation, and test sets have no overlapping patient IDs.
- Check class balance for binary and multiclass tasks before reporting metrics.
- Review calibration curves if predicted probabilities feed downstream clinical logic.
- Do not report only AUROC; include AUPRC especially for imbalanced clinical outcomes.
- Record dataset version, table selection, code mapping, task function, and model class for every experiment.

## Anti-Patterns

- splitting by visit or row instead of by patient, causing data leakage
- using AUROC as the sole metric for rare clinical events
- applying code mappings inconsistently across train and test sets
- mixing raw codes and mapped codes in the same feature without documenting it
- reporting model results without checking data coverage for the target cohort
- treating predicted probabilities as calibrated without verification

## Related Skills

- `Machine Learning For Omics`
- `Multi-Omics Integration`
- `Pathway Analysis`
- `Reporting And Figure Export`

## Optional Supplements

- `pyhealth.medcode` for standalone code mapping
- `pyhealth.calib` for post-hoc calibration
- `pyhealth.interpret` for interpretability
