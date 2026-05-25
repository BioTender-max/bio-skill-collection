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
name: chatehr-clinician-assistant
description: EHR Chat Assistant
keywords:
  - EHR
  - clinical
  - summarization
  - patient-records
  - FHIR
measurable_outcome: Answer 5 clinical queries and generate a discharge summary from a patient record with <10s latency.
license: Apache-2.0
metadata:
  author: Stanford Medicine
  version: "1.0.0"
compatibility:
  - system: Python 3.10+
allowed-tools:
  - run_shell_command
  - read_file
---

# ChatEHR

AI software for clinicians to interact with patient medical records via natural language queries and automatic chart summarization.

## When to Use

*   **Rapid Review**: "Summarize the patient's cardiology history."
*   **Data Extraction**: "What was the last creatinine level?"
*   **Documentation**: Generating draft notes or discharge summaries.

## Core Capabilities

1.  **Chart Summarization**: Condense complex history into readable notes.
2.  **QA**: Answer specific questions about the patient's data.
3.  **FHIR Integration**: Works with standard FHIR resources.

## Workflow

1.  **Connect**: Authenticate with the EHR system (sandbox or secure instance).
2.  **Select Patient**: Load patient context.
3.  **Query**: Submit natural language questions.

## Example Usage

**User**: "Summarize the last 3 oncology visits."

**Agent Action**:
```bash
python -m chatehr.query --patient_id 12345 --prompt "Summarize last 3 oncology visits"
```


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->