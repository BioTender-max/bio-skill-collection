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
name: 'opentrons-protocol-agent'
description: 'Generates executable Python protocols for Opentrons OT-2 and Flex robots from natural language descriptions.'
measurable_outcome: Execute skill workflow successfully with valid output within 15 minutes.
allowed-tools:
  - read_file
  - run_shell_command
---


# Opentrons Protocol Agent

The **Opentrons Protocol Agent** bridges the gap between experimental design and physical execution by translating instructions into Opentrons Python API scripts.

## When to Use This Skill

*   When you need to automate a liquid handling task (PCR prep, ELISA, serial dilution).
*   When you have a text description of a lab protocol and need code for the robot.
*   To validate if a requested protocol is feasible with available labware.

## Core Capabilities

1.  **Protocol Generation**: Creates valid `.py` files for OT-2/Flex.
2.  **Labware Validation**: Checks compatibility of plates and tipracks.
3.  **Volume Calculation**: Automates liquid transfer math (e.g., dilution factors).

## Workflow

1.  **Describe**: Provide the experiment details (source, destination, volumes).
2.  **Generate**: The agent uses the `opentrons_protocol_template.py` or internal logic to draft the script.
3.  **Review**: The user (or a simulator agent) reviews the code for safety.

## Example Usage

**User**: "Create a protocol for 1:2 serial dilution in a 96-well plate."

**Agent Action**:
(Uses an LLM to fill in the template or generate code)
```bash
# Agent writes the file to disk
python3 -m opentrons.simulate generated_protocol.py
```


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->