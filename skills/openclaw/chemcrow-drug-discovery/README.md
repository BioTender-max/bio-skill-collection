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

# ChemCrow Lite: Drug Discovery Tools

## Overview
This skill provides a lightweight implementation of the **ChemCrow** agent concept. It exposes a set of tools for chemical analysis, safety checks, and property calculation. It is designed to work with `rdkit` if available, but gracefully degrades to a "Mock Mode" for demonstration purposes if libraries are missing.

## Features
- **Molecular Weight Calculator:** Uses `rdkit.Chem.Descriptors` (or estimates in mock mode).
- **Safety Checker:** Heuristic detection of common structural alerts (Nitro groups, Heavy metals).
- **Validity Checker:** Verifies SMILES string format.
- **Extensible Tool Interface:** Designed to be easily wrapped by an LLM (LangChain/AutoGPT).

## Usage

### Prerequisites
For full functionality:
```bash
pip install rdkit
```

### Running the Agent

**1. Demo Mode (Runs through test cases):**
```bash
python chem_tools.py
```

**2. CLI Mode:**
```bash
# Calculate Molecular Weight
python chem_tools.py MolWeight "CC(=O)Nc1ccc(O)cc1"

# Check Safety
python chem_tools.py Safety "Cc1c(N(=O)=O)cc(N(=O)=O)cc1N(=O)=O"
```

## Integration
To use this with an LLM:
1. Import `ChemCrowAgent`.
2. Expose `agent.tools` to your LLM's function calling capabilities.
3. The LLM can then request "MolWeight" for a generated molecule to verify its properties.


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->