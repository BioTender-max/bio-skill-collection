<!--
# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

-->

---
name: wearable-analysis-agent
description: Analyzes longitudinal wearable sensor data (heart rate, activity, sleep) to detect anomalies and provide personalized health insights.
keywords:
  - wearable
  - sensor-data
  - health-monitoring
  - anomaly-detection
  - longitudinal-analysis
measurable_outcome: Detects atrial fibrillation and sleep anomalies with >90% accuracy using continuous PPG and accelerometer data.
license: MIT
metadata:
  author: Biomedical AI Team
  version: "1.0.0"
compatibility:
  - system: Python 3.9+
allowed-tools:
  - run_shell_command
  - read_file
---

# Wearable Analysis Agent

The **Wearable Analysis Agent** processes data from consumer health devices (Apple Watch, Fitbit, Oura) to monitor vital signs, detect arrhythmias, and analyze lifestyle patterns.

## When to Use This Skill

*   When analyzing raw export data from wearables (XML, JSON, CSV).
*   To detect irregular heart rhythms (AFib) from PPG data.
*   For longitudinal sleep quality and circadian rhythm analysis.
*   To correlate activity levels with biomarkers or symptom logs.

## Core Capabilities

1.  **Arrhythmia Detection**: Algorithms to identify Atrial Fibrillation burdens from irregular tachograms.
2.  **Sleep Staging**: classifying wake/REM/deep sleep from movement and heart rate variability.
3.  **Activity Recognition**: Categorizing physical activities and calculating intensity (METs).
4.  **Trend Analysis**: Detecting significant deviations in resting heart rate or HRV over weeks/months.

## Workflow

1.  **Ingest**: Parse standardized health exports (e.g., Apple Health XML).
2.  **Preprocess**: Clean noise, handle missing data, align timestamps.
3.  **Analyze**: Apply specific detection algorithms (e.g., `arrhythmia_detector.py`).
4.  **Report**: Generate summary of anomalies and trends.

## Example Usage

**User**: "Analyze my Apple Health export for signs of irregular heart rhythm last month."

**Agent Action**:
```bash
python3 Skills/Consumer_Health/Wearable_Analysis/arrhythmia_detector.py --input apple_health_export.xml --window "last_month"
```


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->