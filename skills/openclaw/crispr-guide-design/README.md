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

# CRISPR Guide Design Agent

**ID:** `biomedical.genomics.crispr_design`
**Version:** 1.1.0
**Status:** Production
**Category:** Genomics / Gene Editing

---

## Overview

The **CRISPR Guide Design Agent** automates sgRNA design for gene editing experiments. It selects target loci, scores guide efficiency, evaluates off-target risk, and generates cloning-ready oligos and protocols.

---

## Inputs

| Field | Type | Notes |
|------|------|------|
| `gene_symbol` | str | Official gene symbol (HGNC or MGI) |
| `organism` | str | `human` or `mouse` (hg38/mm10) |
| `cas_variant` | str | `SpCas9`, `SaCas9`, `Cas12a`, etc. |
| `target_region` | str | `first_exon`, `all_exons`, or domain name |
| `num_guides` | int | Number of guides to return |
| `avoid_variants` | bool | Exclude guides overlapping common SNPs |

---

## Outputs

- Ranked sgRNA list with efficiency and off-target scores
- Genomic coordinates (chromosome, start, strand)
- Cloning oligos with overhangs
- Protocol steps and validation primers (optional)

### Output Schema (Recommended)

```json
{
  "guide_id": "TP53_exon2_guide1",
  "sequence": "GACTG...",
  "pam": "NGG",
  "locus": "chr17:7577120-7577139:+",
  "scores": {"doench": 0.62, "cfd": 0.78, "gc_content": 0.55},
  "off_target_hits": ["chr1:... (2mm)"]
}
```

---

## Workflow

1. **Resolve target** - map gene symbol to canonical transcript and exon coordinates.
2. **Enumerate guides** - scan for PAM-compatible sites in target region.
3. **Score guides** - apply Doench/DeepCRISPR/CFD scoring.
4. **Off-target search** - find genome-wide near matches (<= 3 mismatches).
5. **Rank + filter** - remove low-efficiency or high-risk guides.
6. **Generate protocols** - cloning oligos and validation primers.

---

## Guardrails

- Always report the reference genome build.
- Avoid guides overlapping common variants (dbSNP/gnomAD) when possible.
- Flag guides with high off-target density in coding regions.
- Output is **experimental design support**, not a guarantee of efficacy.

---

## Dependencies

```
biopython>=1.80
requests>=2.28
pandas>=1.5
```

---

## References

- Doench et al. (2016) optimized sgRNA design
- Hsu et al. (2013) specificity of Cas9 nucleases
- CRISPOR, Cas-OFFinder

---

## Author

**MD BABU MIA**
*Artificial Intelligence Group*
*Icahn School of Medicine at Mount Sinai*
md.babu.mia@mssm.edu


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->