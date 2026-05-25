# EHR Analysis Technical Reference

## Purpose

This reference file provides deeper implementation notes for `ehr-analysis`.

## When To Read This File

- use when the dataset source or format requires non-standard loading
- use when task schema design, model selection, or metric choice is ambiguous
- use when calibration, fairness, or interpretability is part of the deliverable

---

## Dataset Branching

### MIMIC-III

- Use `MIMIC3Dataset`.
- Commonly loaded tables: `DIAGNOSES_ICD`, `PROCEDURES_ICD`, `PRESCRIPTIONS`, `LABEVENTS`.
- ICD-9 codes are the default diagnosis vocabulary; map to CCS or CCSR for coarser groupings.

### MIMIC-IV

- Use `MIMIC4Dataset`.
- Supports a richer schema with ICD-10 codes and additional clinical tables.
- Use when the study requires more recent coding standards or note linkage.

### eICU

- Use `eICUDataset`.
- Focused on ICU patients across multiple sites; useful for severity and mortality modeling.
- Check site-level batch effects before pooling all sites.

### OMOP-CDM

- Use `OMOPDataset`.
- Any database conforming to the OMOP common data model (CPRD, All of Us, institutional EHRs).
- Vocabulary is standardized; verify concept IDs map cleanly to the task.

### Custom data

- Wrap preprocessed patient data in `SampleBaseDataset`.
- Structure: each sample is a dict with feature keys and a label key matching the task schema.
- Use `pyhealth.tokenizer.Tokenizer` independently to encode code sequences before passing to models.

---

## Task Schema Design

Tasks in PyHealth define:

- `input_schema`: dict mapping feature key → data type (`"sequence"`, `"binary"`, `"multiclass"`, `"multilabel"`, `"numeric"`)
- `output_schema`: dict mapping label key → data type

Processors are applied automatically based on the schema:
- `"sequence"` → `SequenceProcessor` (code tokenization)
- `"binary"` → `BinaryLabelProcessor`
- `"multiclass"` → `MulticlassLabelProcessor`
- `"multilabel"` → `MultilabelLabelProcessor`

### Custom task function pattern

```python
def my_task_fn(patient):
    samples = []
    for i in range(1, len(patient)):
        visits = patient[:i]
        conditions = [v.get_code_list(table="DIAGNOSES_ICD") for v in visits]
        label = int(patient[i].discharge_status == "expired")
        samples.append({
            "visit_id": patient[i].visit_id,
            "patient_id": patient.patient_id,
            "conditions": conditions,
            "label": label,
        })
    return samples
```

---

## Model Selection

| Model | Best for | Notes |
|---|---|---|
| `RNN`, `LSTM`, `GRU` | general sequential EHR tasks | good baseline; fast to train |
| `Transformer` | large datasets, complex temporal patterns | strong default for MIMIC-scale data |
| `RETAIN` | tasks where interpretability is required | produces visit- and feature-level attention weights |
| `SafeDrug` | drug recommendation with safety constraints | encodes drug molecular graphs; requires drug SMILES |
| `GAMENet` | drug recommendation with DDI graph | incorporates drug-drug interaction knowledge |
| `AdaCare` | tasks with irregular time intervals | adaptive recalibration of clinical features |
| `ConCare` | multi-task clinical prediction | context-aware feature integration |
| `StageNet` | disease staging and progression | models disease trajectory through disease stages |

---

## Medical Code Systems

| System | Covers | PyHealth vocabulary key |
|---|---|---|
| ICD-9-CM | diagnoses (US, legacy) | `"ICD9CM"` |
| ICD-10-CM | diagnoses (US, current) | `"ICD10CM"` |
| ICD-9-Proc | procedures (legacy) | `"ICD9PROC"` |
| ICD-10-PCS | procedures (current) | `"ICD10PCS"` |
| NDC | drug products | `"NDC"` |
| ATC | drug classes (WHO) | `"ATC"` |
| RxNorm | drug concepts | `"RxNorm"` |
| CPT4 | procedures (billing) | `"CPT4"` |
| CCS / CCSCM | coarsened diagnosis groupings | `"CCSCM"` |

### Code mapping pattern

```python
from pyhealth.medcode import CrossMap, InnerMap

# Cross-system: NDC → ATC level 3
ndc_to_atc = CrossMap.load("NDC", "ATC")
atc_codes = ndc_to_atc.map("00527051210", target_kwargs={"level": 3})

# Within-system: ICD-9 hierarchy
icd9cm = InnerMap.load("ICD9CM")
icd9cm.lookup("428.0")          # 'Congestive heart failure, unspecified'
icd9cm.get_ancestors("428.0")   # ['428', '420-429.99', ...]
```

---

## Evaluation Metrics by Task Mode

| Task mode | Primary metrics | Secondary metrics |
|---|---|---|
| `binary` | AUROC, AUPRC | F1, accuracy, ECE (calibration) |
| `multiclass` | macro-F1, accuracy | per-class AUROC |
| `multilabel` | Jaccard, PR-AUC-samples | F1-samples, AUROC-samples |
| drug recommendation | Jaccard, DDI rate, F1 | coverage, novelty |

Always report AUPRC alongside AUROC for imbalanced outcomes. Clinical mortality and readmission datasets are often heavily imbalanced.

---

## Calibration

Post-hoc calibration is important when model outputs feed clinical decision thresholds.

```python
from pyhealth.calib.calibration import TemperatureScaling

calibrator = TemperatureScaling()
calibrator.fit(val_loader, model)
calibrated_probs = calibrator.calibrate(test_loader, model)
```

Available calibration methods: `TemperatureScaling`, `HistogramBinning`, `DirichletCalibration`, `KCal`.

Available prediction set methods (conformal inference): `LABEL`, `SCRIB`, `FavMac`, `CovariateLabel`, `ClusterLabel`.

---

## Fairness

Fairness metrics require protected attribute columns in the patient metadata.

```python
from pyhealth.metrics.fairness import evaluate_fairness

fairness_report = evaluate_fairness(
    y_true=y_true,
    y_pred=y_pred,
    sensitive_attr=sensitive_attr,
)
```

Check for disparities in AUROC, calibration, and error rates across demographic subgroups before reporting aggregate performance.

---

## Validation Priorities

- Confirm identifiers and metadata join correctly before modeling.
- Verify no patient-level data leakage across train, val, and test splits.
- Inspect class and label distributions before selecting the evaluation metric.
- Check code coverage: fraction of codes in test that appeared in train.
- Review calibration before deploying probability thresholds in clinical settings.
- Document dataset version, access date, and all preprocessing decisions.

---

## Common Failure Modes

- splitting by visit instead of by patient, inflating performance metrics
- evaluating on an AUROC alone for rare events where AUPRC is more informative
- applying different code mappings at train time versus test time
- loading only diagnosis codes when the task also requires procedure or drug history
- ignoring class imbalance in loss function configuration
- treating uncalibrated softmax outputs as clinically meaningful probabilities

---

## Optional Supplements

- `pyhealth.medcode` — standalone code lookup and mapping without the full pipeline
- `pyhealth.calib` — post-hoc calibration and conformal prediction sets
- `pyhealth.interpret` — RETAIN-style attention extraction and feature attribution

## Conceptual Provenance

- EHR predictive modeling pipelines (PyHealth, KDD 2023)
- clinical task definition and patient cohort construction patterns
- medical code normalization and cross-system mapping patterns
