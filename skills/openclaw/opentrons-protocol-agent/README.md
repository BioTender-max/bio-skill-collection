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

# Opentrons Protocol Agent

**ID:** `biomedical.lab_automation.opentrons_agent`
**Version:** 1.0.0
**Status:** Experimental
**Category:** Lab Automation / Robotics

---

## Overview

The **Opentrons Protocol Agent** is an LLM-driven tool designed to bridge the gap between experimental design and physical execution. It translates natural language experimental descriptions (e.g., "Serial dilution of samples A-H") into valid, executable Python protocols for Opentrons OT-2 and Flex robots.

This agent empowers "wet lab" automation by allowing researchers to control liquid handling robots via chat interfaces, reducing the barrier to entry for coding complex automation scripts.

---

## Key Capabilities

### 1. Protocol Generation
- Converts text instructions into `opentrons.protocol_api` Python scripts.
- Supports common workflows: PCR prep, ELISA, serial dilutions, aliquoting.
- Automatically calculates volumes and well positions.

### 2. Labware Verification
- Validates that requested labware (plates, tipracks) are compatible and available in the standard library.
- Suggests appropriate pipettes (P20, P300, P1000) based on transfer volumes.

### 3. Safety & Validation
- Performs "virtual run" simulations to check for errors (e.g., running out of tips, aspirating air).
- Includes safety comments and deck setup instructions in the generated code.

---

## Usage

### Example Prompt

```text
Create an Opentrons protocol for a serial dilution.
- Source: Column 1 of a 96-well plate (Corning 3635) containing 200uL stock.
- Destination: Columns 2-12 of the same plate.
- Dilution factor: 1:2 (transfer 100uL, mix 3 times).
- Pipette: P300 Single-Channel Gen2.
- Tips: Opentrons 300uL tiprack on slot 1.
```

### LLM Agent Integration

```python
@tool
def generate_opentrons_protocol(
    experiment_type: str,
    source_labware: str,
    dest_labware: str,
    transfer_volume: float,
    replicates: int = 1
) -> str:
    """
    Generates a Python script for an Opentrons robot.
    
    Args:
        experiment_type: 'serial_dilution', 'pcr_prep', 'reformatting'
        source_labware: API name of source plate
        dest_labware: API name of destination plate
        transfer_volume: Volume in uL
    """
    # Logic to construct the protocol string
    pass
```

---

## Dependencies

- `opentrons>=7.0.0`
- `pandas` (for sample mapping)

## References
- Opentrons Python API V2 Documentation
- "Self-driving laboratories" (Gomes et al., Nature 2023)

---

## Author
**MD BABU MIA**
*Artificial Intelligence Group*
*Icahn School of Medicine at Mount Sinai*
md.babu.mia@mssm.edu


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->