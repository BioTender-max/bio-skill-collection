---
name: hand-tracking-toolkit
description: Facebook Research Hand Tracking Challenge Toolkit - evaluation and visualization tools for 3D hand tracking. Supports loading HOT3D data, computing metrics (PA-MPJPE, AUC, etc.), visualizing 3D pose projections, and generating tracking evaluation reports. Essential for benchmarking hand tracking algorithms.
license: Apache 2.0
metadata:
    skill-author: K-Dense Inc.
    original-repo: https://github.com/facebookresearch/hand_tracking_toolkit
    organization: Meta Facebook Research
    skill-category: Computer Vision / Evaluation
    tags: [hand-tracking, evaluation, metrics, visualization, benchmarking, hot3d]
---

# Hand Tracking Toolkit - Evaluation & Visualization

## Overview

Comprehensive toolkit from Meta Facebook Research for evaluating and visualizing 3D hand tracking systems. Provides standardized metrics, visualization tools, and data loaders for the HOT3D dataset. Essential for researchers developing and benchmarking hand tracking algorithms on multi-view egocentric data.

**Use this for**: Evaluating hand tracking performance, generating evaluation reports, visualizing 3D predictions vs ground truth.

## When to Use This Skill

Use when you need to:
- **Evaluate** hand tracking algorithms with standard metrics
- **Visualize** 3D hand pose predictions and ground truth
- **Benchmark** on HOT3D dataset
- **Generate** evaluation reports and leaderboards
- **Compare** different tracking methods
- **Debug** hand tracking predictions

## Core Capabilities

### 1. Standard Metrics

Compute widely-used hand tracking metrics:
- **PA-MPJPE**: Per-vertex Mean Per Joint Position Error (aligned)
- **MPJPE**: Mean Per Joint Position Error
- **AUC**: Area Under Curve for error thresholds
- **PCK**: Percentage of Correct Keypoints
- **Mesh error**: Surface-to-surface distance

### 2. Visualization Tools

Rich visualization options:
- 3D skeleton plots
- Multi-view projections
- Error heatmaps
- Trajectory visualizations
- Side-by-side comparisons

### 3. Data Loaders

Easy data loading:
- HOT3D dataset sequences
- Ground truth annotations
- Prediction format standardization
- Batch processing support

## Quick Start

```bash
# Clone repository
git clone https://github.com/facebookresearch/hand_tracking_toolkit.git
cd hand_tracking_toolkit

# Install
pip install -r requirements.txt

# Run evaluation
python evaluate.py \
    --predictions path/to/predictions.pkl \
    --ground_truth path/to/hot3d/sequence \
    --output_dir ./results

# Generate visualizations
python visualize.py \
    --predictions path/to/predictions.pkl \
    --ground_truth path/to/hot3d/sequence \
    --output visualizations.png
```

## Usage Examples

### Example 1: Evaluate Predictions

```python
from toolkit import Evaluator
import pickle

# Load predictions
with open('predictions.pkl', 'rb') as f:
    predictions = pickle.load(f)

# Load ground truth
evaluator = Evaluator()
evaluator.load_ground_truth('path/to/hot3d_sequence')

# Compute metrics
metrics = evaluator.evaluate(predictions)

print(f"PA-MPJPE: {metrics['pa_mpjpe']:.2f} mm")
print(f"AUC: {metrics['auc']:.3f}")
print(f"PCK@0.1: {metrics['pck_01']*100:.1f}%")
```

### Example 2: Visualize Results

```python
from toolkit import Visualizer

viz = Visualizer()

# Load data
viz.load_predictions('predictions.pkl')
viz.load_ground_truth('ground_truth_path')

# Create visualization
fig = viz.plot_3d_skeleton(
    frame_id=100,
    show_pred=True,
    show_gt=True,
    show_errors=True
)

fig.savefig('comparison_3d.png')
```

### Example 3: Generate Report

```python
from toolkit import ReportGenerator

report = ReportGenerator()
report.load_evaluation_results('results.json')

# Generate PDF report
report.generate_pdf(
    output_path='evaluation_report.pdf',
    include_plots=True,
    include_per_joint_errors=True
)
```

## Supported Formats

**Prediction format**:
```python
predictions = {
    'sequence_id': 'seq001',
    'frames': [
        {
            'frame_id': 0,
            'left_hand': np.array((21, 3)),  # 21 joints x 3 coords
            'right_hand': np.array((21, 3)),
            'confidence': np.array(21),
        },
        # ... more frames
    ]
}
```

## Metrics Reference

| Metric | Description | Lower is Better |
|--------|-------------|-----------------|
| MPJPE | Mean per-joint position error (mm) | ✓ |
| PA-MPJPE | Aligned MPJPE (procrustes) | ✓ |
| AUC | Area under error threshold curve | ✗ |
| PCK | % keypoints within threshold | ✗ |

## Integration

Works with:
- **hot3d**: Primary dataset
- **Custom trackers**: Convert predictions to supported format
- **Visualization tools**: Matplotlib, Plotly, Open3D

## Best Practices

1. **Standardize** predictions to required format
2. **Use multiple metrics** for comprehensive evaluation
3. **Visualize** errors to understand failure modes
4. **Report** per-joint errors for detailed analysis
5. **Cross-validate** on multiple sequences

## Requirements

- Python 3.8+
- NumPy, SciPy
- Matplotlib (for plotting)
- Open3D (for 3D visualization)
- PyTorch (optional, for loading models)

## References

- GitHub: https://github.com/facebookresearch/hand_tracking_toolkit
- HOT3D: https://facebookresearch.github.io/hot3d
- Challenge: https://eval.ai/web/challenges/challenge-page/...

## License

Apache 2.0
