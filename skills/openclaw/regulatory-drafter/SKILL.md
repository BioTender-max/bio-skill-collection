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
name: 'regulatory-drafter'
description: 'Automates the drafting of regulatory documents (e.g., FDA CTD sections) with citation management and audit trails.'
measurable_outcome: Execute skill workflow successfully with valid output within 15 minutes.
allowed-tools:
  - read_file
  - run_shell_command
---


# Regulatory Drafter Skill

This skill assists regulatory affairs professionals by automatically generating sections of the Common Technical Document (CTD) from raw data and literature. It focuses on accuracy, traceability, and adherence to FDA/EMA guidelines.

## When to Use This Skill

*   **Drafting CTD Sections**: Automatically generate Module 2.4 (Nonclinical Overview) or Module 2.5 (Clinical Overview).
*   **Citation Management**: When you need to synthesize multiple PDFs into a coherent narrative with inline citations.
*   **Audit Trails**: When every claim must be traceable back to a source document.

## Core Capabilities

1.  **Document Synthesis**: Ingests clinical study reports (CSRs) and literature to write narrative text.
2.  **Citation Linking**: Inserts hyperlinks or references to the source material.
3.  **Style Compliance**: Adheres to eCTD formatting standards.

## Workflow

1.  **Ingest Data**: Point the agent to a folder of source PDFs/Data.
2.  **Draft**: Run the drafter with a specific section target (e.g., "Nonclinical Overview").
3.  **Review**: The agent outputs a Markdown/Word draft with annotations.

## Example Usage

**User**: "Draft the Nonclinical Overview based on the toxicology reports in ./data/tox."

**Agent Action**:
```bash
python3 Skills/Anthropic_Health_Stack/regulatory_drafter.py --input "./data/tox" --section "2.4"
```


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->