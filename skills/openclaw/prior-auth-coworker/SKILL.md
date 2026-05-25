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
name: 'prior-auth-coworker'
description: 'Prior Auth Review'
measurable_outcome: Execute skill workflow successfully with valid output within 15 minutes.
allowed-tools:
  - read_file
  - run_shell_command
---


# Prior Authorization Coworker

This skill acts as an automated utilization management reviewer. It takes unstructured clinical notes and a procedure code, compares them against internal policy criteria (e.g., conservative therapy failure), and renders a decision.

## When to Use This Skill

*   When a user asks to "review a prior auth request".
*   When checking if a patient qualifies for a specific procedure (e.g., MRI).
*   When you need to generate a structured approval/denial letter justification.

## Core Capabilities

1.  **Policy Matching**: Checks against specific criteria (e.g., "Pain > 6 weeks").
2.  **Trace Generation**: Produces an "Anthropic-style" `<thinking>` trace for auditability.
3.  **Structured Output**: Returns a JSON object with decision, reasoning, and timestamps.

## Workflow

1.  **Extract Data**: Parse the clinical note and procedure code from the user's input.
2.  **Execute Review**: Run the coworker script.
3.  **Present Decision**: Output the JSON decision and the reasoning trace.

## Example Usage

**User**: "Check if this patient qualifies for an MRI of the Lumbar Spine: Patient has had back pain for 2 months, tried PT but it didn't work."

**Agent Action**:
```bash
python3 Skills/Clinical/Prior_Authorization/anthropic_coworker.py --code "MRI-L-SPINE" --note "Patient has back pain > 2 months. Failed PT."
```

## Supported Policies

*   `MRI-L-SPINE` (Lumbar Spine MRI)


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->