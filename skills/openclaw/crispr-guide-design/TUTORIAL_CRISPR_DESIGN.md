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

# Tutorial: CRISPR gRNA Design with Python

**Domain:** Genomics / Synthetic Biology
**Level:** Beginner
**Estimated Time:** 15 Minutes

## Introduction

CRISPR-Cas9 is a "gene editing scissors". To cut a specific gene, you need a "Guide RNA" (gRNA) that matches the DNA sequence.

But you can't just pick *any* sequence. It must:
1.  Be 20 base pairs long.
2.  End with a **PAM sequence** (NGG) so Cas9 can bind.
3.  Have the right "GC Content" (too strong/weak binding is bad).
4.  Avoid "Poly-T" runs (which stop transcription).

## The Code Logic

The `CRISPRDesigner` class automates this:

1.  **Scanner:** Slides through the DNA string looking for `GG`.
2.  **Extractor:** Whenever it finds `GG`, it looks 21 steps backward to grab the "Spacer".
3.  **Scorer:** It calculates math on the spacer (Count Gs and Cs) to predict how well it will work.

## Running the Tool

```python
from crispr_designer import CRISPRDesigner

designer = CRISPRDesigner()
sequence = "ATGGAGGAGCCGCAGTCAGATCCTAGCGTCGAGCCCCCTCTGAGTCAGGAAACATTTTCAGACCTATGGAAACTGTGAGTGGATCCATTGGAAGGGC"

results = designer.find_targets(sequence)

# The results are already sorted by "Efficiency Score"
best_guide = results[0]
print(f"Best Guide: {best_guide['spacer']} (Score: {best_guide['efficiency_score']})")
```

## Assignments

1.  **Search:** Find the DNA sequence for the *CFTR* gene (associated with Cystic Fibrosis). Paste a snippet into the variable `sequence`.
2.  **Modify:** Edit `crispr_designer.py` to support **Cas12a**. Cas12a looks for a different PAM (`TTTV`) instead of `NGG`.
    *   *Hint:* Change the loop to look for `TTT` and grab sequence *after* it, not before.


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->