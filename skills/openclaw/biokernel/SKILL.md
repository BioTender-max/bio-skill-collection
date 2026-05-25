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
name: biokernel
description: Biomedical OS Core & MCP Server
keywords:
  - kernel
  - os
  - mcp
  - api
  - system
measurable_outcome: Routes 100% of API requests to correct sub-agent with <200ms latency.
license: MIT
metadata:
  author: Biomedical OS Team
  version: "1.0.0"
compatibility:
  - system: Python 3.10+
allowed-tools:
  - run_shell_command
  - read_file
---

# BioKernel

The BioKernel is the central orchestration layer of the Biomedical OS, managing context, routing tasks to specialized agents via MCP (Model Context Protocol), and handling system resources.

## When to Use This Skill

*   **System Internal**: This is primarily a background skill for routing.
*   When initializing the Biomedical OS environment.
*   When managing state across multiple agent interactions.

## Core Capabilities

1.  **Task Routing**: Dispatches user queries to the correct specialist agent.
2.  **Context Management**: Maintains long-term memory and session state.
3.  **MCP Server**: Exposes tools and resources via standard protocol.

## Example Usage

**User**: "Start the BioKernel server."

**Agent Action**:
```bash
python3 platform/biokernel/server.py --port 8000
```


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->