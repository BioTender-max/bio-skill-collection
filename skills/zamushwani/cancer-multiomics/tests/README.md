# Validation Tests

Tests that verify the cancer-multiomics SKILL.md code against TCGA-LUAD public data.

## Running

```bash
cd skills/cancer-multiomics/tests/

# All tests (~30-45 min, downloads from GDC)
Rscript run_all.R

# Single test
Rscript run_all.R expression
Rscript run_all.R mutation
Rscript run_all.R cnv
Rscript run_all.R methylation
```

## What gets tested

| Test | What it checks |
|------|---------------|
| `validate_expression.R` | GDC query, DESeq2 pipeline, DEG counts, sample counts |
| `validate_mutation.R` | MAF retrieval, driver gene frequencies (TP53, KRAS, EGFR, STK11), TMB range, oncoplot, somatic interactions |
| `validate_cnv.R` | Segment download, Segment_Mean interpretation, gain/loss detection, gene-level mapping |
| `validate_methylation.R` | 450K data retrieval, beta-value range, M-value conversion, limma DMP analysis, delta-beta direction |

## Expected values (TCGA-LUAD benchmarks)

Based on the TCGA-LUAD landmark paper (Nature 2014, PMID 25079552) and GDC current data:

| Metric | Expected |
|--------|----------|
| Expression samples | ~540 tumor, ~59 normal |
| DEGs (padj<0.05, \|LFC\|>1) | 3,000-5,000 (full cohort) |
| TP53 mutation frequency | 40-50% |
| KRAS mutation frequency | 28-38% |
| Median TMB | 4-8 mut/MB |
| Methylation samples | ~485 tumor, ~32 normal |
| 450K probes after filtering | ~420,000-440,000 |

## Requirements

```r
# Core (required)
install.packages("BiocManager")
BiocManager::install(c(
  "TCGAbiolinks", "DESeq2", "maftools",
  "SummarizedExperiment", "limma"
))

# For CNV gene mapping
BiocManager::install(c(
  "GenomicRanges", "TxDb.Hsapiens.UCSC.hg38.knownGene"
))

# For signature analysis
BiocManager::install("BSgenome.Hsapiens.UCSC.hg38")

# For DMR and pathway analysis
BiocManager::install(c("DMRcate", "missMethyl"))
```

## Notes

- Tests download data from GDC. First run is slow; cached data speeds up reruns.
- Small subsets are used (10-30 samples) for speed. Some checks use wider bounds to accommodate reduced power.
- Tests that require optional packages (BSgenome, TxDb, DMRcate) are skipped if the package is not installed.
