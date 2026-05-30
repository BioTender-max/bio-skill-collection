---
name: harness-core
description: "Core harness library providing standardized self-verification, checkpoint management, drift detection, and audit logging utilities for all NeuroClaw skills. This is NOT directly called by users; instead, it is imported as a Python module by other skills for harness-compliant execution, validation, and reproducibility. Use this as a foundation/plugin SDK when building or enhancing other skills. Triggers: none (library import only). This skill provides: HarnessController class, VerificationRunner, CheckpointManager, DriftDetector, AuditLogger, DependencyManifest, and related utilities."
license: MIT License (NeuroClaw custom skill – freely modifiable within the project)
layer: base
skill_type: tool
dependencies: []
---
# Harness Core Library

## Overview

`harness-core` is the **base SDK / plugin library** for implementing NeuroClaw harness engineering standards across all skills.

Instead of reimplementing validation, checkpointing, logging, and drift detection in every skill, `harness-core` provides reusable, well-tested Python classes and utilities that all other skills can import and extend.

**Key design principle**: Harness-awareness is **not optional** — every data-processing, model-execution, and experiment-running skill should import from this library to achieve:
- Standardized self-verification across all skills
- Reproducible, hash-verified experiment logs
- Automatic checkpoint/resume capability
- Drift detection and anomaly alerts
- Privacy-preserving audit trails

### When to Use This Skill

**Directly**: Rarely — this is a library, not a user-facing skill.

**Indirectly (as a dependency)**: 
- When developing or modifying skills like `experiment-controller`, `run_models`, `fmri-skill`, `smri-skill`, etc.
- When using skills that have been enhanced to support harness engineering
- When integrating external tools or models into NeuroClaw (inherit harness patterns)

## Core Components

### 1. HarnessController (Main Orchestrator)

**Purpose**: Manages the full lifecycle of harness-compliant execution.

**Usage**:
```python
from skills.harness_core import HarnessController

controller = HarnessController(
    task_name="fmri_preprocessing",
    session_id="exp_20260405_143000",
    checkpoint_dir="./checkpoints",
    log_dir="./logs"
)

# Automatic environment snapshot capture
controller.initialize()

# Define task phases
controller.add_phase("quality_check", description="Verify input BIDS compliance")
controller.add_phase("preprocessing", description="Apply fMRI preprocessing")
controller.add_phase("feature_extraction", description="Extract ROI time series")

# Execute with auto-checkpointing
for phase_name in ["quality_check", "preprocessing", "feature_extraction"]:
    try:
        phase = controller.get_phase(phase_name)
        result = execute_phase(phase.name)  # User-defined function
        controller.record_phase_success(phase_name, result)
        controller.save_checkpoint(f"after_{phase_name}")
    except Exception as e:
        controller.record_phase_failure(phase_name, str(e))
        controller.save_checkpoint(f"failed_{phase_name}")
        raise

# Auto-generates: audit_report.md, environment_manifest.json, checkpoints/
```

### 2. VerificationRunner

**Purpose**: Automated validation module with pluggable check functions.

**Usage**:
```python
from skills.harness_core import VerificationRunner

verifier = VerificationRunner(task_type="fmri_preprocessing")

# Built-in checks
verifier.add_check("bids_compliance", 
    checker=lambda data: check_bids_format(data),
    severity="error"  # or "warning"
)

verifier.add_check("data_integrity",
    checker=lambda data: check_nan_inf(data),
    severity="error"
)

verifier.add_check("statistical_bounds",
    checker=lambda data: check_intensity_range(data, min=-10, max=10),
    severity="warning"
)

# Run all checks; returns VerificationReport
report = verifier.run(output_data)

if report.failed:
    print(f"Verification FAILED: {report.summary}")
else:
    print(f"All checks passed. Confidence: {report.confidence_score}")
```

### 3. CheckpointManager

**Purpose**: Handles saving/loading of execution state with compression and integrity verification.

**Usage**:
```python
from skills.harness_core import CheckpointManager

checkpoint_mgr = CheckpointManager(
    checkpoint_dir="./checkpoints",
    compression="lz4",  # or "gzip", "zstd"
    hash_algorithm="sha256"
)

# Save state after each task
checkpoint_mgr.save(
    checkpoint_name="after_task_001",
    data={
        "model_state": model.state_dict(),
        "data_cache": processed_data,
        "metadata": {"task": "training", "epoch": 50}
    },
    overwrite=False  # Prevent accidental overwrites
)

# Resume from checkpoint
state = checkpoint_mgr.load("after_task_001")
model.load_state_dict(state["model_state"])
```

### 4. DriftDetector

**Purpose**: Monitor data and model behavior for distribution shifts.

**Usage**:
```python
from skills.harness_core import DriftDetector

detector = DriftDetector(
    reference_data=training_data,
    detector_type="kl_divergence"  # or "ks_test", "wasserstein"
)

# Run detection on new/inference data
drift_report = detector.detect(new_data)

if drift_report.drift_detected:
    print(f"⚠️  Drift detected: KL divergence = {drift_report.divergence}")
    if drift_report.severity == "critical":
        trigger_retraining_alert()
```

### 5. AuditLogger

**Purpose**: Structured, privacy-preserving logging for reproducibility and compliance.

**Usage**:
```python
from skills.harness_core import AuditLogger

logger = AuditLogger(
    log_file="./logs/experiment_audit.jsonl",
    pii_scrubber=True  # Auto-redact sensitive info
)

logger.log_event(
    event_type="skill_execution",
    skill_name="fmri_preprocessing",
    status="started",
    timestamp="2026-04-05T14:22:00Z",
    metadata={"input_file": "sub-001_task-rest_bold.nii.gz", "subjects": 100}
)

logger.log_validation(
    task_name="preprocessing",
    checks_passed=45,
    checks_failed=0,
    warnings=2,
    artifacts_hash={"output_data_sha256": "abc123..."}
)
```

### 6. DependencyManifest

**Purpose**: Generate and verify reproducible dependency specifications.

**Usage**:
```python
from skills.harness_core import DependencyManifest

manifest = DependencyManifest(environment_name="neuroclaw-dl")

# Auto-capture current environment
manifest.capture_current_environment()

# Export to multiple formats
manifest.export_to_conda_yml("environment-lock.yml")
manifest.export_to_pip_txt("requirements-pinned.txt")
manifest.export_to_json("DEPENDENCY_MANIFEST.json")

# Verify environment matches manifest
verified = manifest.verify_current_environment(strict=True)
print(f"Environment verified: {verified.status}")
if not verified.matched:
    print(f"Mismatches: {verified.mismatches}")
```

## Python API Reference

### HarnessController

```python
class HarnessController:
    def __init__(self, task_name, session_id, checkpoint_dir, log_dir):
        """Initialize harness controller."""
    
    def initialize(self):
        """Capture environment snapshot and setup logging."""
    
    def add_phase(self, phase_name, description=""):
        """Register a task phase."""
    
    def execute_phase(self, phase_name, func, *args, **kwargs):
        """Execute function and record result."""
    
    def record_phase_success(self, phase_name, result):
        """Log successful phase completion."""
    
    def record_phase_failure(self, phase_name, error_msg):
        """Log phase failure with error details."""
    
    def save_checkpoint(self, checkpoint_name):
        """Save execution state checkpoint."""
    
    def load_checkpoint(self, checkpoint_name):
        """Restore execution state from checkpoint."""
    
    def finalize(self):
        """Generate final audit report and cleanup."""
```

### VerificationRunner

```python
class VerificationRunner:
    def __init__(self, task_type):
        """Initialize verification runner."""
    
    def add_check(self, check_name, checker, severity="error"):
        """Register a validation check function."""
    
    def run(self, data):
        """Execute all checks; return VerificationReport."""
```

### DriftDetector

```python
class DriftDetector:
    def __init__(self, reference_data, detector_type="kl_divergence"):
        """Initialize drift detector."""
    
    def detect(self, new_data):
        """Run drift detection; return DriftReport."""
```

### AuditLogger

```python
class AuditLogger:
    def __init__(self, log_file, pii_scrubber=True):
        """Initialize audit logger."""
    
    def log_event(self, event_type, **kwargs):
        """Log a structured event."""
    
    def log_validation(self, task_name, **kwargs):
        """Log validation results."""
```

## Integration Best Practices

### For Skill Developers

When creating a new skill or enhancing an existing one:

**1. Import harness-core utilities:**
```python
from skills.harness_core import (
    HarnessController,
    VerificationRunner,
    CheckpointManager,
    AuditLogger
)
```

**2. Wrap main execution in HarnessController:**
```python
def run_skill(input_data, config):
    controller = HarnessController(
        task_name="my_skill",
        session_id=generate_session_id(),
        checkpoint_dir="./checkpoints",
        log_dir="./logs"
    )
    
    controller.initialize()
    
    try:
        result = process_data(input_data)  # Your skill logic
        controller.record_phase_success("processing", result)
        return result
    finally:
        controller.finalize()
```

**3. Add self-verification:**
```python
verifier = VerificationRunner("my_skill_output")
verifier.add_check("output_shape", lambda r: r.shape == expected_shape)
verifier.add_check("no_nan", lambda r: not np.isnan(r).any())

report = verifier.run(result)
if not report.passed:
    raise ValueError(f"Verification failed: {report.summary}")
```

**4. Enable checkpointing for long tasks:**
```python
checkpoint_mgr = CheckpointManager("./checkpoints")

for epoch in range(max_epochs):
    train_one_epoch()
    if epoch % checkpoint_frequency == 0:
        checkpoint_mgr.save(f"epoch_{epoch}", {"model": model, "epoch": epoch})
```

### For Users / Experiment Runners

When executing a skill enhanced with harness-core:

1. **Audit logs are automatically generated** in `./logs/`
2. **Checkpoints are auto-saved** in `./checkpoints/`
3. **Environment manifests** (conda/pip specs) are captured in `experiment_metadata/`
4. **Reproducibility is guaranteed**: Re-run with same input data + environment → identical results

## Output Files Generated

Every harness-compliant skill execution generates:

```
experiment_20260405_143000/
├── audit_report.md                 # Human-readable summary
├── environment_manifest.json        # Dependencies snapshot
├── DEPENDENCY_MANIFEST.json         # Full version specs
├── requirements-pinned.txt          # Pip format
├── environment-lock.yml             # Conda format
├── task_manifest.json               # Task DAG + success/failure status
├── checkpoints/
│   ├── after_phase_001.pkl
│   ├── after_phase_002.pkl
│   └── checkpoint_metadata.json
├── logs/
│   ├── audit.jsonl                  # Structured event log
│   └── verification_report.json     # All validation checks
├── outputs/
│   ├── result_data.pkl
│   └── result_hash_verification.json
└── drift_detection_log.jsonl        # (if applicable)
```

## Installation & Integration

**This skill is provided as a Python package.** Integration steps:

1. **Already included in workspace**: `skills/harness-core/` folder
2. **For other skills to import**:
   ```python
   import sys
   sys.path.insert(0, '{workspace_root}/skills/harness-core')
   from harness_core import HarnessController, VerificationRunner, ...
   ```

3. **Or use relative imports within skills**:
   ```python
   from ..harness_core import HarnessController
   ```

## Extending Harness Core

To add custom checks, verifiers, or detectors:

```python
from skills.harness_core import VerificationRunner

class CustomVerifier(VerificationRunner):
    def add_domain_specific_check(self, data):
        """Add domain-specific validation."""
        self.add_check(
            "my_domain_constraint",
            checker=lambda d: validate_domain(d),
            severity="error"
        )
```

---

Created At: 2026-04-05 01:48 HKT  
Last Updated At: 2026-04-05 02:01 HKT
Author: chengwang96