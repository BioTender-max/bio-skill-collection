# EHR Analysis Commands And Thresholds

## Five-Stage Pipeline (Canonical Pattern)

```python
# ── Stage 1: Load dataset ──────────────────────────────────────────────────
from pyhealth.datasets import MIMIC3Dataset

dataset = MIMIC3Dataset(
    root="/path/to/mimic3/",
    tables=["DIAGNOSES_ICD", "PROCEDURES_ICD", "PRESCRIPTIONS"],
    code_mapping={"NDC": ("ATC", {"target_kwargs": {"level": 3}})},
)

# ── Stage 2: Define task ───────────────────────────────────────────────────
from pyhealth.tasks import drug_recommendation_mimic3_fn

samples = dataset.set_task(task_fn=drug_recommendation_mimic3_fn)

# ── Stage 3: Split and dataload ────────────────────────────────────────────
from pyhealth.datasets import split_by_patient, get_dataloader

train_ds, val_ds, test_ds = split_by_patient(samples, [0.8, 0.1, 0.1])
train_loader = get_dataloader(train_ds, batch_size=32, shuffle=True)
val_loader   = get_dataloader(val_ds,   batch_size=32, shuffle=False)
test_loader  = get_dataloader(test_ds,  batch_size=32, shuffle=False)

# ── Stage 4: Model ────────────────────────────────────────────────────────
from pyhealth.models import Transformer

model = Transformer(
    dataset=samples,
    feature_keys=["conditions", "procedures"],
    label_key="drugs",
    mode="multilabel",
)

# ── Stage 5: Train and evaluate ───────────────────────────────────────────
from pyhealth.trainer import Trainer

trainer = Trainer(model=model)
trainer.train(
    train_dataloader=train_loader,
    val_dataloader=val_loader,
    epochs=50,
    monitor="pr_auc_samples",
)
metrics = trainer.evaluate(test_loader)
print(metrics)
```

---

## Mortality Prediction Example (Binary)

```python
from pyhealth.datasets import MIMIC4Dataset
from pyhealth.tasks import MortalityPredictionMIMIC4
from pyhealth.models import RETAIN
from pyhealth.trainer import Trainer
from pyhealth.datasets import split_by_patient, get_dataloader

dataset = MIMIC4Dataset(
    root="/path/to/mimic4/",
    tables=["diagnoses_icd", "procedures_icd"],
    code_mapping={"ICD10CM": "CCSCM"},
)

samples = dataset.set_task(MortalityPredictionMIMIC4())
train_ds, val_ds, test_ds = split_by_patient(samples, [0.8, 0.1, 0.1])

model = RETAIN(
    dataset=samples,
    feature_keys=["conditions"],
    label_key="label",
    mode="binary",
)

trainer = Trainer(model=model)
trainer.train(
    train_dataloader=get_dataloader(train_ds, batch_size=32, shuffle=True),
    val_dataloader=get_dataloader(val_ds, batch_size=32, shuffle=False),
    epochs=50,
    monitor="roc_auc",
)
print(trainer.evaluate(get_dataloader(test_ds, batch_size=32, shuffle=False)))
```

---

## Medical Code Mapping

```python
from pyhealth.medcode import CrossMap, InnerMap

# ICD-9 → CCS (coarser grouping)
icd9_to_ccs = CrossMap.load("ICD9CM", "CCSCM")
icd9_to_ccs.map("428.0")             # ['108']

# NDC → ATC level 3
ndc_to_atc = CrossMap.load("NDC", "ATC")
ndc_to_atc.map("00527051210", target_kwargs={"level": 3})  # ['A11C']

# Within-system lookup
icd9cm = InnerMap.load("ICD9CM")
icd9cm.lookup("428.0")               # 'Congestive heart failure, unspecified'
icd9cm.get_ancestors("428.0")        # ['428', '420-429.99', ...]
```

---

## Tokenizer (Standalone)

```python
from pyhealth.tokenizer import Tokenizer

token_space = ["A01A", "A02A", "A02B", "A03C", "A04A"]
tokenizer = Tokenizer(tokens=token_space, special_tokens=["<pad>", "<unk>"])

# Encode visit sequences (3D: patient × visit × code)
tokens = [[["A03C", "A04A"], ["A02B"]], [["A01A", "A02A"]]]
indices = tokenizer.batch_encode_3d(tokens)
decoded = tokenizer.batch_decode_3d(indices)
```

---

## Custom Task Function

```python
def mortality_task_fn(patient):
    samples = []
    for i in range(1, len(patient)):
        conditions = [v.get_code_list(table="DIAGNOSES_ICD") for v in patient[:i]]
        label = int(patient[i].discharge_status == "expired")
        samples.append({
            "visit_id": patient[i].visit_id,
            "patient_id": patient.patient_id,
            "conditions": conditions,
            "label": label,
        })
    return samples

samples = dataset.set_task(task_fn=mortality_task_fn)
```

---

## Calibration

```python
from pyhealth.calib.calibration import TemperatureScaling

calibrator = TemperatureScaling()
calibrator.fit(val_loader, model)
cal_probs = calibrator.calibrate(test_loader, model)
```

---

## Recommended Thresholds and Defaults

| Setting | Default | Notes |
|---|---|---|
| `batch_size` | `32` | reduce if OOM on long sequences |
| `epochs` | `50` | use `monitor` for early stopping |
| `split_by_patient` | `[0.8, 0.1, 0.1]` | never split by visit |
| binary monitor metric | `"roc_auc"` | also track `"pr_auc"` for rare events |
| multilabel monitor metric | `"pr_auc_samples"` | or `"jaccard_samples"` |
| ATC mapping level | `3` | balance drug specificity and sparsity |
| minimum code frequency | filter codes appearing in `< 10` patients | reduce vocabulary noise |

---

## Output Convention

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
