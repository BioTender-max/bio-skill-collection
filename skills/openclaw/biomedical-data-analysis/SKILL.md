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
name: biomedical-data-analysis
description: Omics data forge
keywords:
  - pandas
  - R-tidyverse
  - SQL
  - visualization
  - reproducible
measurable_outcome: Deliver a cleaned dataset + statistical summary + at least one visualization or dashboard spec for each request within 1 working session (≤30 minutes).
license: MIT
metadata:
  author: BioSkills Team
  version: "1.0.0"
compatibility:
  - system: Python 3.9+ / R 4.0+
allowed-tools:
  - run_shell_command
  - read_file
  - python_repl
---

# Biomedical Data Analysis

Run the cross-language data analysis workflows (Python, R, SQL, Tableau/Power BI) described in this module to clean, analyze, and visualize biomedical datasets end-to-end.

## Workflow
1. **Scope request:** Identify analysis_type (`exploratory`, `statistical`, `predictive`, `visualization`) and required language/tooling.
2. **Acquire data:** Load from CSV/Parquet/SQL using pandas, tidyverse, or connectors described in `README.md`.
3. **Process:** Apply wrangling, descriptive stats, modeling, or SQL aggregations as listed in the capability tables.
4. **Visualize:** Choose Matplotlib/Seaborn/Plotly for inline plots or emit Tableau/Power BI specs per need.
5. **Document:** Provide code snippets + outputs, noting package versions and any assumptions.

## Guardrails
- Use reproducible scripts or notebooks—avoid manual spreadsheet edits.
- Keep PHI secure; when touching EHR-level SQL list filters minimizing data exposure.
- Clearly separate exploratory findings from validated statistical conclusions.

## References
- Capability tables, code samples, and parameter definitions live in `README.md` (plus `tutorials/README.md` for step-by-step lessons).


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->