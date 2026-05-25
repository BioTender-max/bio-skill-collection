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

# BioMCP Server

**ID:** `biomedical.mcp.biomcp`
**Version:** 1.0.0
**Status:** Production
**Category:** Infrastructure / MCP

---

## Overview

**BioMCP** is a dedicated Model Context Protocol (MCP) server for biomedical data. It exposes standard biomedical APIs (PubMed, ClinicalTrials.gov, PubChem) to any MCP-compliant LLM client (Claude Desktop, Cursor, etc.).

## Tools Provided

1.  `search_pubmed(query, max_results)`
2.  `get_drug_info(drug_name)` (via RxNorm/FDA)
3.  `search_clinical_trials(condition, location)`
4.  `get_gene_summary(gene_symbol)` (via NCBI Gene)

## Usage

Add to your `claude_desktop_config.json`:

```json
"biomcp": {
  "command": "uvx",
  "args": ["biomcp"]
}
```

## References
- [LobeHub BioMCP](https://lobehub.com/mcp/genomoncology-biomcp)


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->