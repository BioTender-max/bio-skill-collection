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

# TrialGPT: Clinical Trial Matching

**Source:** [ncbi-nlp/TrialGPT](https://github.com/ncbi-nlp/TrialGPT)
**Local Repository:** `./repo`
**Status:** Integrated & Downloaded

---

## Overview

TrialGPT is an NIH-developed framework for matching patients to clinical trials using LLMs. It provides a structured pipeline for trial retrieval, eligibility parsing, and ranking with evidence-based explanations.

---

## Capabilities

1. **Trial Retrieval** - Identify candidate trials from ClinicalTrials.gov.
2. **Criteria Parsing** - Convert eligibility text into structured criteria.
3. **Patient Profiling** - Summarize patient records into matchable features.
4. **Ranking + Explanation** - Score trial relevance and provide justifications.

---

## Recommended Usage

1. **Install dependencies**
   ```bash
   cd repo
   pip install -r requirements.txt
   ```
2. **Run retrieval** - identify candidate trials for a condition.
3. **Run matching** - evaluate eligibility with structured criteria.
4. **Review outputs** - validate by clinician or trial coordinator.

---

## Input and Output Expectations

**Input:**
- Patient summary (structured or narrative)
- Condition keywords or diagnosis codes

**Output:**
- Ranked trials with relevance scores
- Criteria-level match explanations
- Missing data checklist

---

## Integration Notes

- Use TrialGPT for retrieval and initial ranking, then hand off to the **Clinical Trial Eligibility Agent** for deeper criterion-by-criterion analysis.
- Cache trial metadata (NCT ID, protocol version) to ensure reproducibility.

---

## Limitations

- Requires up-to-date trial metadata; outdated data can misclassify eligibility.
- LLM reasoning should be audited by clinical staff before enrollment decisions.



<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->