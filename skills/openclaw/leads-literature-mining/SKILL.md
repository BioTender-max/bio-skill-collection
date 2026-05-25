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
name: leads-literature-mining
description: Review Automator
keywords:
  - literature-mining
  - systematic-review
  - meta-analysis
  - pubmed
  - evidence-synthesis
measurable_outcome: Complete a systematic review screen of 100+ papers with >90% inclusion/exclusion accuracy compared to human baseline.
license: CC-BY-4.0
metadata:
  author: Nature Communications 2025
  version: "1.0.0"
compatibility:
  - system: Python 3.9+
allowed-tools:
  - run_shell_command
  - web_fetch
---

# LEADS (Literature Mining Agent)

A specialized LLM agent for automating systematic reviews and meta-analyses, capable of high-accuracy study selection and data extraction.

## When to Use

*   **Systematic Reviews**: Screening thousands of abstracts for inclusion criteria.
*   **Data Extraction**: Pulling specific metrics (e.g., hazard ratios, sample sizes) from full-text PDFs.
*   **Evidence Synthesis**: Aggregating findings across multiple studies.

## Core Capabilities

1.  **Study Selection**: Automated screening based on PICO criteria.
2.  **Data Extraction**: Structured extraction of study characteristics and results.
3.  **Quality Assessment**: Risk of bias evaluation.

## Workflow

1.  **Search**: Query PubMed/Embase.
2.  **Screen**: Apply inclusion/exclusion criteria to abstracts.
3.  **Extract**: Parse full text for data points.
4.  **Report**: Generate PRISMA flow diagram and evidence table.

## Example Usage

**User**: "Perform a systematic review on the efficacy of CAR-T in solid tumors."

**Agent Action**:
```bash
python -m leads.review --topic "CAR-T solid tumors" --criteria ./criteria.json
```


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->