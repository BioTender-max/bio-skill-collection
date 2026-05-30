---
id: mendelian-randomization-twosamplemr
name: "Two-Sample Mendelian Randomization"
category: genomics_genetics
short-description: "Assess causal relationships between traits using GWAS summary statistics and genetic instruments."
detailed-description: "Performs two-sample Mendelian Randomization (MR) analysis using genetic variants as instrumental variables to test causal effects of an exposure on an outcome. Supports OpenGWAS database access and user-provided GWAS summary statistics. Applies IVW, MR-Egger, weighted median, and weighted mode methods with comprehensive sensitivity analyses."
starting-prompt: "I want to test whether LDL cholesterol has a causal effect on coronary heart disease using Mendelian Randomization."
---

# Two-Sample Mendelian Randomization

## When to Use This Skill

- You have **GWAS summary statistics** for an exposure and outcome trait
- You want to test **causal direction** between two traits (not just correlation)
- You need to assess whether an observed association is likely causal or confounded
- You want to use **genetic variants as instrumental variables** (natural experiment)
- You have OpenGWAS trait IDs **or** your own GWAS summary statistics files

**Not suitable for:** One-sample MR (individual-level data), non-linear MR, multivariable MR with >2 exposures

## Installation

```r
install.packages(c("remotes", "ggplot2", "ggprism", "dplyr", "rmarkdown"))
remotes::install_github("MRCIEU/TwoSampleMR")
# For PDF report generation (optional but recommended):
# install.packages("tinytex"); tinytex::install_tinytex()
# For MR-PRESSO outlier detection (optional but recommended):
# remotes::install_github("rondolab/MR-PRESSO")
```

| Software | Version | License | Commercial Use |
|----------|---------|---------|----------------|
| TwoSampleMR | ≥0.5.6 | GPL-3 | ✅ Permitted |
| ieugwasr | ≥0.2.1 | MIT | ✅ Permitted |
| ggplot2 | ≥3.4.0 | MIT | ✅ Permitted |
| ggprism | ≥1.0.3 | GPL (≥3) | ✅ Permitted |
| dplyr | ≥1.1.0 | MIT | ✅ Permitted |
| rmarkdown | ≥2.20 | GPL-3 | ✅ Permitted |

## Inputs

**Option A — OpenGWAS IDs (recommended):**
- Exposure ID (e.g., `"ieu-a-300"` for LDL cholesterol)
- Outcome ID (e.g., `"ieu-a-7"` for coronary heart disease)
- Browse available traits at: https://gwas.mrcieu.ac.uk/

**Option B — User-provided files (CSV/TSV):**
- Exposure GWAS summary statistics
- Outcome GWAS summary statistics

| Required Column | Description | Example |
|----------------|-------------|---------|
| SNP | rsID | rs1234567 |
| beta | Effect estimate | 0.05 |
| se | Standard error | 0.01 |
| pval | P-value | 5e-10 |
| effect_allele | Effect allele | A |
| other_allele | Other allele | G |
| eaf | Effect allele frequency (optional) | 0.3 |

## Outputs

**Results (CSV):**
- `mr_results.csv` — MR estimates from all 4 methods (beta, SE, p-value, nSNP, F-statistics)
- `heterogeneity_results.csv` — Cochran's Q test for instrument heterogeneity
- `pleiotropy_results.csv` — MR-Egger intercept test for directional pleiotropy
- `directionality_results.csv` — Steiger test confirming causal direction
- `harmonized_data.csv` — SNP-level harmonized exposure-outcome data
- `single_snp_results.csv` — Per-SNP Wald ratio estimates
- `leaveoneout_results.csv` — Leave-one-out robustness estimates
- MR-PRESSO outlier results (if heterogeneity significant and MRPRESSO installed)

**Plots (PNG + SVG):**
- `mr_scatter_plot` — SNP-exposure vs SNP-outcome with method regression lines
- `mr_forest_plot` — Individual + combined SNP effect estimates
- `mr_funnel_plot` — Precision vs effect size (asymmetry = pleiotropy)
- `mr_leaveoneout_plot` — Effect stability when removing each SNP

**Report:**
- `mr_report.pdf` — Structured analysis report (Introduction, Methods, Results, Figures, Conclusions)

**Analysis objects (RDS):**
- `mr_object.rds` — Complete analysis (results, sensitivity, harmonized data)
  - Load with: `mr_obj <- readRDS("mr_results/mr_object.rds")`

## Clarification Questions

1. **Input Data** (ASK THIS FIRST):
   - Do you have specific **GWAS summary statistics** or **OpenGWAS trait IDs**?
   - If files uploaded: Are these the exposure and outcome GWAS files?
   - Expected formats: CSV/TSV with SNP, beta, se, pval, effect_allele, other_allele
   - **Or use example data?** LDL Cholesterol → Coronary Heart Disease demo (drug-target validation example)

2. **Exposure and Outcome**:
   - *(If using example data)* Pre-set: Exposure = LDL Cholesterol, Outcome = Coronary Heart Disease — no need to specify
   - *(If using your own data)* What is the **exposure** (potential cause)? What is the **outcome** (potential effect)?

3. **Parameters** (defaults usually fine):
   - P-value threshold for instruments? (default: 5×10⁻⁸)
   - LD clumping r²? (default: 0.001)

## Standard Workflow

> **Note:** Run from the OmicsClaw root directory and add the workflow scripts to `sys.path`:
> ```python
> import sys; import os; sys.path.insert(0, os.path.abspath('knowledge_base/scripts/mendelian-randomization-twosamplemr'))
> ```

🚨 **MANDATORY: USE SCRIPTS EXACTLY AS SHOWN — DO NOT WRITE INLINE CODE** 🚨

**Step 1 — Load and harmonize data:**
```r
source("scripts/load_data.R")
dat <- load_example_data()
# OR: dat <- load_from_opengwas("ieu-a-300", "ieu-a-7")
# OR: dat <- load_from_files("exposure.csv", "outcome.csv")
```
**DO NOT write inline data loading or harmonization code. Use the functions above.**

✅ **VERIFICATION:** You MUST see `"✓ Data loaded and harmonized successfully!"`

**Step 2 — Run MR analysis:**
```r
source("scripts/run_mr_analysis.R")
mr_results <- run_mr(dat)
sensitivity <- run_sensitivity(dat, mr_results)
```
**DO NOT write inline MR code. Just source the script and call the functions.**

✅ **VERIFICATION:** You MUST see `"✓ MR analysis completed successfully!"` AND `"✓ Sensitivity analyses completed successfully!"`

**Step 3 — Generate visualizations:**
```r
source("scripts/mr_plots.R")
generate_all_plots(mr_results, dat, sensitivity$singlesnp, sensitivity$leaveoneout, output_dir = "mr_results")
```
🚨 **DO NOT write inline plotting code (ggsave, ggplot, etc.). Just use the function.** 🚨

✅ **VERIFICATION:** You MUST see `"✓ All MR plots generated successfully!"`

**Step 4 — Export results and generate report:**
```r
source("scripts/export_results.R")
export_all(mr_results, sensitivity, dat, output_dir = "mr_results")
```
**DO NOT write custom export code. Use export_all(). It automatically generates the PDF report.**

✅ **VERIFICATION:** You MUST see `"✓ Report generated successfully!"` AND `"=== Export Complete ==="`

❌ **IF YOU DON'T SEE VERIFICATION MESSAGES:** You wrote inline code. Stop and use the scripts.

⚠️ **CRITICAL — DO NOT:**
- ❌ **Write inline MR analysis code** → **STOP: Use `run_mr()` and `run_sensitivity()`**
- ❌ **Write inline plotting code** → **STOP: Use `generate_all_plots()`**
- ❌ **Write custom export code** → **STOP: Use `export_all()`**
- ❌ **Write custom report code** → **STOP: Use `generate_report()`**
- ❌ **Try to install system dependencies** → Scripts handle package installation

⚠️ **IF SCRIPTS FAIL — Script Failure Hierarchy:**
1. **Fix and Retry (90%)** — Install missing R package, re-run script
2. **Modify Script (5%)** — Edit the script file, document changes
3. **Use as Reference (4%)** — Read script, adapt approach, cite source
4. **Write from Scratch (1%)** — Only if genuinely impossible, explain why

## Common Issues

| Issue | Cause | Solution |
|-------|-------|---------|
| **"No instruments found"** | No SNPs below p-value threshold | Try a less stringent threshold or check trait ID |
| **LD clumping API fails** | OpenGWAS/IEU API temporarily down | Script falls back to no clumping with warning; results may be affected by LD |
| **"Only N SNPs retained"** | Allele harmonization removed most SNPs | Check if exposure/outcome are from same genome build |
| **Steiger test fails** | Sample sizes unavailable in metadata | Normal for some datasets; other sensitivity tests still valid |
| **SVG export error** | Missing optional dependency | Normal — `generate_all_plots()` falls back to base R svg() automatically |
| **OpenGWAS rate limiting** | Too many API requests | Wait a few minutes and retry |
| **PDF report fails** | LaTeX/tinytex not installed | Install with `tinytex::install_tinytex()` — report auto-falls back to HTML or base R PDF |
| **Steiger R² warning for binary outcome** | Outcome is case-control, not quantitative | Use `get_r_from_lor()` with prevalence to compute liability-scale R² before directionality test |
| **MR-PRESSO not available** | MRPRESSO package not installed | `remotes::install_github('rondolab/MR-PRESSO')` — optional but recommended when heterogeneity is significant |
| **"Cannot find function"** | Script not sourced | Run `source("scripts/load_data.R")` before calling functions |

## Interpreting Results

See [references/interpretation-guide.md](references/interpretation-guide.md) for detailed guidance.

**Quick interpretation:**
- **Concordant methods** (IVW, Egger, WM, WMode agree on direction + significance) → stronger evidence
- **Any method non-significant or discordant** → must be discussed explicitly, not dismissed
- **IVW significant + no heterogeneity + no pleiotropy** → strongest evidence
- **Egger intercept p < 0.05** → directional pleiotropy may bias IVW
- **High heterogeneity (Q p < 0.05)** → run MR-PRESSO, flag outlier instruments
- **Steiger direction incorrect** → reverse causation concern (check binary outcome R² correction)
- **F-statistic < 10** → weak instrument bias toward the null

## Suggested Next Steps

- **Multiple exposures?** → Run bidirectional MR (swap exposure/outcome)
- **Pleiotropy detected?** → Consider MR-PRESSO or multivariable MR
- **Significant result?** → Replicate with independent GWAS datasets
- **Drug target validation?** → Use cis-MR with variants near gene of interest
- **Pathway analysis?** → Combine with functional enrichment skills

## Related Skills

- `polygenic-risk-score` — Polygenic risk score computation (LDpred2)
- `polygenic-risk-score-prs-catalog` — PRS from pre-computed PGS Catalog weights
- `eqtl-colocalization-coloc` — eQTL colocalization analysis (MR follow-up)

## References

- Sanderson E, et al. (2022). Mendelian randomization. *Nat Rev Methods Primers*. [PMC7384151](https://pmc.ncbi.nlm.nih.gov/articles/PMC7384151/)
- Hemani G, et al. (2018). The MR-Base platform supports systematic causal inference across the human phenome. *eLife*. DOI: 10.7554/eLife.34408
- TwoSampleMR package: https://github.com/MRCIEU/TwoSampleMR
- OpenGWAS database: https://gwas.mrcieu.ac.uk/
- STROBE-MR guidelines: https://doi.org/10.1001/jama.2023.1788
