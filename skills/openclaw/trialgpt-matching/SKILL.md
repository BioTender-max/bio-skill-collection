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
name: trialgpt-matching
description: Trial shortlist
keywords:
  - retrieval
  - ranking
  - ClinicalTrials
  - patient-profile
measurable_outcome: Produce ≥5 ranked trials (when available) with rationale + missing-data notes within 3 minutes of receiving a patient query.
license: MIT
metadata:
  author: TrialGPT Team
  version: "1.0.0"
compatibility:
  - system: Python 3.9+
allowed-tools:
  - run_shell_command
  - read_file
---

# TrialGPT Matching

Run the locally checked-out TrialGPT pipeline to retrieve, rank, and explain candidate trials for a patient before deeper eligibility review.

## Inputs
- Patient summary (structured JSON or free text) with condition keywords.
- Optional filters: geography, phase, intervention, biomarker.
- Up-to-date ClinicalTrials.gov dump or API access.

## Outputs
- Ranked trial table with NCT ID, title, score, and short justification.
- Parsed inclusion/exclusion text ready for downstream eligibility agents.
- Missing data checklist (e.g., "ECOG not provided").

## Workflow
1. **Setup:** `cd repo && pip install -r requirements.txt` (or reuse env).
2. **Trial retrieval:** Run TrialGPT retriever to pull candidate trials for the indication.
3. **Criteria parsing:** Convert eligibility blocks to structured criteria JSON.
4. **Patient profiling:** Summarize patient facts (labs, prior therapies, biomarkers).
5. **Ranking:** Execute TrialGPT ranking script to score each trial and emit explanations.
6. **Handoff:** Export ranked list + structured criteria for `trial-eligibility-agent`.

## Guardrails
- Refresh ClinicalTrials.gov metadata regularly to avoid stale trials.
- Label scores as AI-generated suggestions pending clinician validation.
- Retain prompt/config metadata for audit trails.

## References
- Detailed usage instructions and repo layout live in `README.md`.
- Coordinate with `Skills/Clinical/Trial_Eligibility_Agent` for criterion-level review.


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->