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

# Biomni: General-Purpose Biomedical Agent

**Source:** [snap-stanford/Biomni](https://github.com/snap-stanford/Biomni)
**Local Repository:** `./repo`
**Status:** Integrated & Downloaded

## Overview
Biomni is a state-of-the-art biomedical AI agent capable of solving a wide array of research problems by orchestrating a massive library of tools and databases.

## Resources
- **150+ Tools:** Specialized functions for cloning, CRISPR design, docking, etc.
- **105 Software Packages:** Wrappers for standard bio-software.
- **59 Databases:** APIs for PubMed, UniProt, ClinVar, PDB, etc.

## The "Know-How" Library
Biomni features a unique **Know-How Library**, a retrieval system containing:
- Experimental protocols.
- Troubleshooting guides.
- "Golden path" analysis strategies.
- Authoritative metadata for citation.

## Quick Start
1.  **Installation:**
    Biomni uses `pyproject.toml`.
    ```bash
    cd repo
    pip install .
    ```
    Or see `repo/tutorials` for Jupyter notebook examples.
2.  **Running Tutorials:**
    Explore `repo/tutorials/` to see Biomni in action.
    ```bash
    jupyter notebook repo/tutorials/
    ```

## Usage Modes
1.  **Standard Mode:** Uses full datalake and all tools.
2.  **Light Mode:** Uses only API-based tools (no heavy local data).
3.  **Commercial Mode:** Filters out non-commercial license tools/data.

<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->