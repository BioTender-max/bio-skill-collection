---
id: survival-analysis-clinical
name: Clinical Survival & Outcome Analysis
category: multi_omics
short-description: "Perform Kaplan-Meier estimation, Cox proportional hazards regression, and risk stratification from clinical time-to-event data."
detailed-description: "Analyze clinical survival outcomes using Kaplan-Meier estimation with log-rank tests, Cox proportional hazards regression with automatic covariate selection, proportional hazards assumption testing (Schoenfeld residuals), and risk stratification (median/tertile/quartile split). Produces publication-quality survival curves with risk tables, forest plots of hazard ratios, and diagnostic plots. Supports TCGA, clinical trial, and real-world evidence datasets. Exports risk scores and analysis objects (RDS) for downstream integration with biomarker panel discovery and multi-omics stratification."
starting-prompt: Run a survival analysis on breast cancer clinical data to identify prognostic factors and stratify patients by risk. Generate a PDF report with an intro, methods, results, conclusions and figures from all of the analyses you perform.
---

# Clinical Survival & Outcome Analysis

Kaplan-Meier survival estimation, Cox proportional hazards regression, and risk stratification for clinical and real-world evidence (RWE) datasets.

## When to Use This Skill

Use this skill when you need to:
- **Estimate survival curves** (Kaplan-Meier) with confidence intervals and risk tables
- **Identify prognostic factors** via Cox proportional hazards regression
- **Stratify patients by risk** using Cox model linear predictor
- **Test proportional hazards assumption** with Schoenfeld residuals
- **Compare survival between groups** (molecular subtypes, treatment arms, biomarker levels)
- **Generate forest plots** of hazard ratios for multi-covariate models

**Don't use this skill for:**
- ❌ Biomarker panel selection from omics → use `lasso-biomarker-panel`
- ❌ Differential expression analysis → use `bulk-rnaseq-counts-to-de-deseq2`
- ❌ Disease trajectory / longitudinal modeling → use `disease-progression-longitudinal`
- ❌ Genetic association / Mendelian randomization → use `mendelian-randomization-twosamplemr`

## Installation

```r
options(repos = c(CRAN = "https://cloud.r-project.org"))
if (!require('BiocManager', quietly = TRUE)) install.packages('BiocManager')

# Core (required)
install.packages(c('survival', 'ggplot2', 'ggprism', 'scales'))

# Enhanced KM curves with risk tables (recommended)
install.packages('survminer')

# Example data: TCGA BRCA (optional, needed for tcga_brca demo)
BiocManager::install('RTCGA.clinical')

```

| Software | Version | License | Commercial Use | Installation |
|----------|---------|---------|----------------|-------------|
| survival | >=3.5 | LGPL (>=2) | ✅ Permitted | `install.packages('survival')` |
| ggplot2 | >=3.4 | MIT | ✅ Permitted | `install.packages('ggplot2')` |
| ggprism | >=1.0.3 | GPL (>=3) | ✅ Permitted | `install.packages('ggprism')` |
| scales | >=1.2 | MIT | ✅ Permitted | `install.packages('scales')` |
| survminer | >=0.4.9 | GPL (>=2) | ✅ Permitted | `install.packages('survminer')` |

## Inputs

**Required:**
- **Clinical data** with columns for:
  - **Time-to-event** (numeric: days, months, or years)
  - **Event indicator** (binary: 0 = censored, 1 = event)
- Minimum 50 patients recommended (20+ events for reliable Cox estimates)

**Optional:**
- **Stratification variable** (e.g., molecular subtype, treatment arm, biomarker group)
- **Covariates** for Cox model (age, stage, receptor status, etc.)
- **Pre-computed risk scores** from upstream skills (e.g., `lasso-biomarker-panel`)

**Formats:** CSV/TSV with headers, or R data frame

## Outputs

**Primary results:**
- `cox_coefficients.csv` — Hazard ratios with 95% CI and p-values for all covariates
- `risk_scores.csv` — Patient-level risk scores and risk group assignments
- `clinical_annotated.csv` — Full clinical data with added risk group column
- `survival_summary.csv` — Summary statistics per risk group (N, events, event rate, median survival)
- `ph_assumption_test.csv` — Schoenfeld residual test results (chi-sq, p-value per covariate)

**Analysis objects (RDS):**
- `survival_model.rds` — Complete analysis object for downstream use
  - Load with: `model <- readRDS('results/survival_model.rds')`
  - Contains: KM fits, Cox model, PH test, risk groups, clinical data, metadata
  - Access risk scores: `model$cox$risk_scores`
  - Access Cox model: `model$cox$model`
  - Required for: `lasso-biomarker-panel` (risk scores as features), downstream integration

**Plots (PNG + SVG at 300 DPI):**
- `km_overall.png/.svg` — Overall Kaplan-Meier curve with confidence interval
- `km_stratified.png/.svg` — Stratified survival curves with log-rank p-value
- `forest_plot.png/.svg` — Forest plot of hazard ratios with significance markers
- `km_risk_groups.png/.svg` — Risk group survival curves with log-rank test
- `schoenfeld_diagnostics.png/.svg` — PH assumption diagnostic plots
- `cumulative_hazard.png/.svg` — Cumulative hazard function

**Reports:**
- `survival_report.md` — Comprehensive markdown report
- `survival_report.pdf` — Agent-generated PDF report with Introduction, Methods, Results, Conclusions, and embedded figures

**⚠️ PDF style rules:**
- **US Letter page size (8.5 × 11 in)** — always set page dimensions explicitly; do not rely on library defaults
- **No Unicode superscripts** — use `3.36e-06` or `3.36 × 10^(-6)`, not Unicode superscript chars (they render as ■ in PDF fonts)
- **No half-empty pages** — group headings with their content; only page-break before major sections (Results, Conclusions)
- **Figures ≥80% page width** — multi-panel figures must be large enough to read; never embed below 50% width

## Clarification Questions

🚨 **ALWAYS ask Question 1 FIRST.**

### 1. **Example or Own Data?** (ASK THIS FIRST):
   - **a) TCGA Breast Cancer** (recommended for demo)
     - 1,100+ patients with overall survival, molecular subtypes (HR+/HER2-, HR+/HER2+, HER2+, Triple Negative), stage, age, ER/PR/HER2 status
     - **Requires download** (~50MB via RTCGA.clinical, cached after first run)
   - **b) NCCTG Lung Cancer** (quick demo, no download)
     - 228 advanced lung cancer patients, sex stratification, ECOG performance status
     - Built-in R dataset — runs instantly
   - **c) I have my own clinical data to analyze**
     - Continue to Questions 2-3 below

> **IF EXAMPLE SELECTED (option a or b):** Proceed to Question 2 for analysis options. Skip Question 3.

### 2. **Analysis Options** *(structured — for all datasets)*:
   - **Stratification variable?**
     - a) Default for dataset (mol_subtype for TCGA BRCA, sex for Lung)
     - b) Stage
     - c) Age group
   - **Risk stratification method?**
     - a) Median split — 2 groups (recommended)
     - b) Tertiles — 3 groups
     - c) Quartiles — 4 groups

### 3. **Data Details** *(own data only — free-text OK)*:
   - What is the time column name? Units (days/months/years)?
   - What is the event column name? What does 1 represent (death/relapse/progression)?
   - What stratification variable? What covariates for the Cox model?

## Standard Workflow

> **Note:** Run from the OmicsClaw root directory and add the workflow scripts to `sys.path`:
> ```python
> import sys; import os; sys.path.insert(0, os.path.abspath('knowledge_base/scripts/survival-analysis-clinical'))
> ```

🚨 **MANDATORY: USE SCRIPTS EXACTLY AS SHOWN - DO NOT WRITE INLINE CODE** 🚨

**Step 1 - Load data:**
```r
source("scripts/load_example_data.R")
data <- load_example_data(dataset = "tcga_brca")
# OR: data <- load_example_data(dataset = "lung")
# OR: data <- load_user_data("path/to/clinical.csv", time_col = "time", event_col = "status")
```
**DO NOT write custom data loading code. Use the loader functions.**

**✅ VERIFICATION:** You MUST see: `"✓ TCGA BRCA data loaded successfully!"` (or similar)

**Step 2 - Run survival analysis:**
```r
source("scripts/basic_workflow.R")
result <- run_survival_analysis(data)
# Optional: result <- run_survival_analysis(data, risk_strata_method = "tertiles")
# Optional: result <- run_survival_analysis(data, covariates = c("age", "stage"))
```
**DO NOT write inline Cox/KM code (coxph, survfit, etc.). Just source and call.**

**✅ VERIFICATION:** You MUST see: `"✓ Survival analysis completed successfully!"`

**❌ IF YOU DON'T SEE THIS:** You wrote inline code. Stop and use `source()`.

**Step 3 - Generate visualizations:**
```r
source("scripts/survival_plots.R")
generate_all_plots(result, output_dir = "results")
```
🚨 **DO NOT write inline plotting code (ggsave, ggplot, ggsurvplot, etc.). Just use `generate_all_plots()`.** 🚨

**The script handles PNG + SVG export with graceful fallback for SVG dependencies.**

**✅ VERIFICATION:** You MUST see: `"✓ All survival plots generated successfully!"`

**Step 4 - Export results:**
```r
source("scripts/export_results.R")
export_all(result, output_dir = "results")
```
**DO NOT write custom export code. Use `export_all()` to save all outputs including RDS.**

**✅ VERIFICATION:** You MUST see:
- `"=== Export Complete ==="`

⚠️ **CRITICAL - DO NOT:**
- ❌ **Write inline Cox/KM code (coxph, survfit)** → **STOP: Use `source("scripts/basic_workflow.R")`**
- ❌ **Write inline plotting code (ggsave, ggplot, ggsurvplot)** → **STOP: Use `generate_all_plots()`**
- ❌ **Write custom export code** → **STOP: Use `export_all()`**
- ❌ **Try to install svglite** → script handles SVG fallback automatically

**⚠️ IF SCRIPTS FAIL - Script Failure Hierarchy:**
1. **Fix and Retry (90%)** - Install missing package, re-run script
2. **Modify Script (5%)** - Edit the script file itself, document changes
3. **Use as Reference (4%)** - Read script, adapt approach, cite source
4. **Write from Scratch (1%)** - Only if genuinely impossible, explain why

**NEVER skip directly to writing inline code without trying the script first.**

## Common Issues

| Error | Cause | Fix |
|-------|-------|-----|
| **"No valid covariates found"** | All columns have >20% missing or single value | Provide covariates explicitly: `run_survival_analysis(data, covariates = c("age", "stage"))` |
| **"Cox model failed with all covariates"** | Collinear or non-convergent covariates | Script auto-falls back to stepwise. Inspect individual p-values. |
| **PH assumption violated (global p < 0.05)** | Time-varying effects | Note in report. Consider stratified analysis. See `references/cox-regression-guide.md`. |
| **"Event column must be binary (0/1)"** | Non-standard event coding | Recode: e.g., `survival::lung` uses 1=censored, 2=dead → script handles this. |
| **RTCGA.clinical download fails** | Network/firewall issue | Use `dataset = "lung"` as fallback (no download needed). |
| **SVG export failed** | Missing optional dependency | Normal — `generate_all_plots()` falls back automatically. PNG always generated. |
| **KM curve drops steeply despite low event rate** | **Heavy censoring (correct behavior)** | **NOT A BUG.** With heavy censoring (e.g., 90% censored), the at-risk set shrinks so each late event causes a large survival drop. The KM tail (N at risk < 30) is unreliable. Report **landmark survival rates** instead. |
| **Subtype medians have upper CI = NA** | **KM never crosses 50% for that group** | The median is an unreliable extrapolation. The script flags this — use landmark rates instead. Do NOT report these medians as reliable point estimates. |

## Agent Summary Guidelines

When presenting final results to the user, the agent MUST:
1. **Report the C-index** (concordance) from the Cox model — but see EPV rule below
2. **Check `result$median_reliable`** — if FALSE, report "Median survival: Not reached" and use **landmark survival rates** (from `result$landmark_survival`) instead
3. **Report landmark survival rates** (1-year, 3-year, 5-year OS with 95% CI) — these are always more robust than median, especially for low-event datasets
4. **State PH assumption result** (satisfied or violated, with global p-value)
5. **List significant covariates** with HR, 95% CI, and p-value
6. **Report EPV** (events per variable) — if `result$epv < 10`, warn that model may be overfitted
7. **Report excluded patients** — if `result$n_excluded > 0`, note how many were excluded from Cox model
8. **Report risk group separation** (log-rank chi-sq and p-value)
9. **Report PDF status** — if PDF generation failed, say so and note markdown report is available
10. **Never fabricate survival curve descriptions** — reference the actual generated plots
11. **Never report unreliable medians as if they are reliable** — when upper CI = NA, the KM curve did not cross 50% and the median is an unreliable extrapolation
12. **Methods section MUST match actual model** — list only covariates from `names(coef(result$cox$model))`. Check `result$dropped_covariates` and report what was excluded and why. NEVER list covariates from memory; always verify against the fitted model.
13. **Report dropped covariates** — if `result$dropped_covariates` is non-empty, list each dropped variable and reason (rare levels, collinearity) in the Methods section
14. **Report reference groups** — for each categorical covariate, state the reference level and its N (from `result$reference_levels`). If N < 50, flag the HR as "unstable due to small reference group (N=X)"
15. **Report informative missingness** — if any entry in `result$diagnostics$missing_assessment` has `informative = TRUE`, report the event rate comparison prominently and note selection bias risk
16. **Report follow-up anomalies** — if `result$diagnostics$followup_anomaly` is TRUE, investigate and explain prominently. Do NOT dismiss as "expected" without evidence.

⚠️ **CRITICAL REPORTING RULES:**
- **EPV < 10 + C-index:** If `result$epv < 10`, you MUST describe the C-index as "potentially overfitted" or "unreliable". NEVER use "good" or "moderate discrimination" without this caveat. The C-index is optimistically biased when EPV is low.
- **PH violation + forest plot/Cox table:** If global PH test p < 0.05, you MUST include a prominent warning on the forest plot caption AND any Cox results table: "PH assumption violated (p=X) — HRs represent time-averaged effects and may be misleading." Do NOT present HRs as primary findings without this warning.
- **Small reference groups:** If a key finding involves a categorical covariate whose reference group has N < 50, flag the estimate as unstable. State the reference group N explicitly.
- **Never fabricate group sizes or statistics.** All Ns, HRs, CIs, and p-values in the report text MUST be copied from the script console output or exported CSV files. Do NOT estimate, round from memory, or recalculate group sizes. If a number is not in the output, re-run the relevant step or read the exported file.

## Interpretation Guidelines

- **C-index > 0.7:** Good model discrimination — **ONLY if EPV >= 10**. If EPV < 10, say "potentially overfitted (EPV = X)"
- **C-index 0.6-0.7:** Moderate — useful combined with clinical factors
- **C-index ~ 0.5:** No better than chance
- **HR > 1:** Higher hazard (worse prognosis) per unit increase
- **HR < 1:** Lower hazard (protective effect)
- **HR 95% CI includes 1.0:** Not statistically significant
- **PH global p < 0.05:** Proportional hazards assumption violated — HRs are time-averaged and may be misleading. Must be stated prominently on forest plots and Cox tables, not buried in a later section.
- **EPV < 10:** Model underpowered — C-index likely optimistically biased; consider fewer covariates. NEVER call the C-index "good" when EPV < 10.
- **Median survival "Not reached":** KM curve never crosses 50% — use landmark survival rates instead
- **Low event rate (<15%):** KM curves may drop steeply in the tail due to small at-risk set (heavy censoring), not because most patients die. Always check N at risk at each timepoint.
- **Median follow-up < 2 yr with max obs > 5 yr:** Likely a data quality artifact — investigate completeness of follow-up times for censored patients before interpreting results.

## Suggested Next Steps

1. **Biomarker panel discovery** — Use risk scores as features → `lasso-biomarker-panel`
2. **Pathway enrichment** — If molecular subtypes differ → `functional-enrichment-from-degs`
3. **Multi-omics integration** — Combine clinical + omics → `multi-omics-integration-mofa`
4. **Disease trajectory** — Map temporal progression → `disease-progression-longitudinal`
5. **Clinical trial landscape** — Search related interventional trials → `clinicaltrials-landscape`

## Related Skills

| Skill | Relationship |
|-------|-------------|
| `lasso-biomarker-panel` | **Downstream** — Use risk scores as features for biomarker selection |
| `disease-progression-longitudinal` | **Complementary** — Trajectory analysis on same clinical data |
| `multi-omics-integration-mofa` | **Upstream** — Factor scores as Cox covariates |
| `bulk-rnaseq-counts-to-de-deseq2` | **Upstream** — DE results inform covariate selection |
| `coexpression-network` | **Upstream** — Module eigengenes as survival predictors |

## References

- Cox DR. Regression Models and Life-Tables. J R Stat Soc B. 1972;34(2):187-220.
- Kaplan EL, Meier P. Nonparametric Estimation from Incomplete Observations. JASA. 1958;53(282):457-481.
- Cancer Genome Atlas Network. Comprehensive molecular portraits of human breast tumours. Nature. 2012;490:61-70.
- Loprinzi CL, et al. Prospective evaluation of prognostic variables from patient-completed questionnaires. J Clin Oncol. 1994;12:601-607.
- Therneau TM. A Package for Survival Analysis in R. R package survival.
- See [references/cox-regression-guide.md](references/cox-regression-guide.md) for detailed Cox PH interpretation
- See [references/risk-stratification-guide.md](references/risk-stratification-guide.md) for risk group methodology
