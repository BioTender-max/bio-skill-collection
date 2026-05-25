# Validation Tests

Tests run immune deconvolution methods against TCGA-BRCA and verify output against known biological expectations.

## Running

```bash
Rscript run_all.R                # all tests (~45-60 min)
Rscript run_all.R deconvolution  # methods + cross-method concordance
Rscript run_all.R purity         # ESTIMATE purity checks
Rscript run_all.R subtypes       # Basal vs Luminal A ordering
```

## What each test checks

**deconvolution**: Runs quanTIseq, EPIC, MCP-counter on 30 BRCA tumors. Checks output format, fraction ranges, and cross-method Spearman correlation for CD8+ T cells (expect rho > 0.3).

**purity**: Runs ESTIMATE on the same 30 samples. Checks purity is 0-1, median is 0.50-0.95, and purity anticorrelates with ImmuneScore. Cross-validates against quanTIseq uncharacterized fraction.

**subtypes**: Downloads 10 Basal + 10 Luminal A samples (stratified by PAM50). Checks that Basal has higher CD8+ T cell scores and lower purity than Luminal A across methods.

## Requirements

```r
# Core
install.packages("remotes")
remotes::install_github("omnideconv/immunedeconv")
BiocManager::install(c("TCGAbiolinks", "SummarizedExperiment", "org.Hs.eg.db"))
```

## Expected values (TCGA-BRCA)

| Check | Expected |
|-------|----------|
| quanTIseq uncharacterized fraction | 0.4-0.95 |
| EPIC otherCells fraction | > 0.5 |
| Cross-method CD8 Spearman rho | > 0.3 |
| ESTIMATE median purity | 0.50-0.95 |
| Purity vs ImmuneScore correlation | rho < -0.3 |
| Basal CD8 vs LumA CD8 | Basal > LumA |
| Basal purity vs LumA purity | Basal < LumA |
