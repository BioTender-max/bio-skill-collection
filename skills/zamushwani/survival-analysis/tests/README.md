# Validation Tests

Tests run survival analysis methods against TCGA-GBM clinical data and verify output against published benchmarks.

## Running

```bash
Rscript run_all.R              # all tests (~10-20 min)
Rscript run_all.R survival     # KM curves, median OS, 2-year survival
Rscript run_all.R cox          # Cox PH, age HR, Schoenfeld, C-index
Rscript run_all.R prognostic   # IDH-mutant vs wildtype survival
```

## What each test checks

**survival**: Runs Kaplan-Meier on the full GBM cohort. Checks median OS is 12-18 months, 2-year survival is 15-35%, and median follow-up via reverse KM.

**cox**: Fits Cox PH with age and gender. Checks age HR is 1.01-1.06 per year, runs cox.zph for PH assumption, verifies C-index > 0.5, and validates EPV >= 10.

**prognostic**: Fetches molecular subtypes via TCGAquery_subtype. If IDH status is available, compares IDH-mutant vs IDH-wildtype survival (expect mutant >> wildtype OS). Skips gracefully if subtype data is unavailable.

## Requirements

```r
BiocManager::install("TCGAbiolinks")
install.packages("survival")
```

## Expected values (TCGA-GBM)

| Check | Expected | Source |
|-------|----------|--------|
| Median overall survival | 12-18 months | Ostrom et al. 2014, TCGA 2008 |
| 2-year survival | 15-35% | TCGA pan-glioma studies |
| Median age at diagnosis | 55-65 years | CBTRUS Statistical Report |
| Age HR (per year) | 1.01-1.06 | Multiple TCGA Cox analyses |
| IDH-mutant frequency | < 15% of GBM | Yan et al. 2009, TCGA 2008 |
| IDH-mutant vs wildtype OS | ~31 vs ~15 months | Parsons et al. 2008 |
| IDH log-rank p | < 0.05 | Consistent across studies |
