# Survival Analysis

Time-to-event analysis for cancer clinical data. Covers Kaplan-Meier, Cox proportional hazards, competing risks, restricted mean survival time, and optimal cutpoint selection using the survival, ggsurvfit, tidycmprsk, and survRM2 packages.

## When to Use This Skill

Activate when the user requests:
- Kaplan-Meier survival curves with risk tables
- Log-rank or stratified log-rank tests between groups
- Cox proportional hazards modeling (univariable or multivariable)
- Proportional hazards assumption checking
- Competing risks analysis (cause-specific or Fine-Gray)
- Restricted mean survival time (RMST) comparisons
- Optimal biomarker cutpoint selection for survival
- Forest plots for multivariate Cox models

## Inputs

| Data Type | Format | Source |
|-----------|--------|--------|
| Clinical | Tabular (time, event, covariates) | TCGA GDC via TCGAbiolinks, cBioPortal |
| Time variable | Days/months to event or last follow-up | `days_to_death`, `days_to_last_follow_up` |
| Event indicator | Binary (0 = censored, 1 = event) | Derived from `vital_status` |
| Covariates | Categorical or continuous | Age, stage, gene expression, mutations |

---

## Preparing TCGA Survival Data

```r
library(TCGAbiolinks)
library(SummarizedExperiment)

query <- GDCquery(
  project = "TCGA-GBM",
  data.category = "Transcriptome Profiling",
  data.type = "Gene Expression Quantification",
  workflow.type = "STAR - Counts"
)
GDCdownload(query, directory = "GDCdata")
se <- GDCprepare(query, directory = "GDCdata")
clinical <- as.data.frame(colData(se))

# Construct survival endpoint from TCGA clinical fields
# TCGA stores time in days. Convert to months for readability.
clinical$os_time <- ifelse(!is.na(clinical$days_to_death),
  as.numeric(clinical$days_to_death),
  as.numeric(clinical$days_to_last_follow_up))
clinical$os_event <- ifelse(clinical$vital_status == "Dead", 1, 0)
clinical$os_months <- clinical$os_time / 30.44

# Drop samples with missing survival data
clinical <- clinical[!is.na(clinical$os_months) & clinical$os_months > 0, ]
```

## Kaplan-Meier Estimation

```r
library(survival)    # v3.8+
library(ggsurvfit)   # v1.2+, pharmaverse — modern replacement for survminer

# survfit2() tracks the calling environment for cleaner legend labels
# Use survfit2() with ggsurvfit; use survfit() with base R plotting
km_fit <- survfit2(Surv(os_months, os_event) ~ gender, data = clinical)

ggsurvfit(km_fit) +
  add_confidence_interval() +
  add_risktable() +
  add_pvalue(location = "annotation") +
  scale_x_continuous(breaks = seq(0, 60, 12)) +
  labs(x = "Months", y = "Overall survival probability") +
  theme_classic(base_size = 12)

# Median survival per group
summary(km_fit)$table[, "median"]

# Median follow-up: reverse KM method (censor events, event the censored)
km_fu <- survfit(Surv(os_months, 1 - os_event) ~ 1, data = clinical)
summary(km_fu)$table["median"]
# Always report median follow-up alongside survival estimates
```

## Log-Rank Test

```r
# Two-group comparison
survdiff(Surv(os_months, os_event) ~ idh1_status, data = clinical)
# Returns chi-square and p-value. Tests H0: survival curves are identical.

# Stratified log-rank — adjust for a confounder without estimating its effect
survdiff(Surv(os_months, os_event) ~ treatment + strata(age_group), data = clinical)
```

```
When log-rank is appropriate:
  Groups have proportional hazards (non-crossing curves)
    -> log-rank is most powerful
  Curves cross or separate late (common in immunotherapy)
    -> log-rank has low power. Use RMST or weighted log-rank.
  > 2 groups
    -> log-rank gives a global test. Follow up with pairwise comparisons
       using p.adjust() for multiple testing correction.
```

## Cox Proportional Hazards

### Univariable

```r
# Continuous covariate
cox_age <- coxph(Surv(os_months, os_event) ~ age_at_diagnosis, data = clinical)
summary(cox_age)
# HR per 1-year increase. exp(coef) = HR, lower/upper .95 = CI

# Categorical covariate — set reference level explicitly
clinical$stage <- relevel(factor(clinical$stage), ref = "Stage I")
cox_stage <- coxph(Surv(os_months, os_event) ~ stage, data = clinical)
```

### Multivariable

```r
cox_multi <- coxph(
  Surv(os_months, os_event) ~ age_at_diagnosis + gender + idh1_status + mgmt_methylation,
  data = clinical
)
summary(cox_multi)

# Concordance index (C-statistic): 0.5 = random, 1.0 = perfect discrimination
# TCGA-GBM with IDH + MGMT: expect C-index ~0.65-0.75
concordance(cox_multi)
```

### Design Considerations

```
Variable selection:
  Include variables that are clinically established prognostic factors.
  Do NOT use stepwise selection (AIC/BIC) for final models in clinical contexts —
  it inflates Type I error and produces unstable models.
  Stepwise is acceptable for exploratory analysis with clear disclosure.

Events per variable (EPV):
  Classic rule: >= 10 events per predictor in the model.
  With 50 events, fit at most 5 covariates.
  More recent work (Riley 2019) recommends >= 20 EPV for adequate precision.
  Too many covariates relative to events = overfitting and unstable HRs.

Continuous vs categorical:
  Keep continuous variables continuous in Cox models. Dichotomizing age at
  median discards information and reduces power.
  If a cutpoint is needed for clinical communication, derive it separately
  (see Optimal Cutpoints below) and validate externally.
```

## Proportional Hazards Assumption

```r
# Schoenfeld residual test
zph <- cox.zph(cox_multi, transform = "km")
print(zph)
# Per-covariate p-values + global test
# p > 0.05: PH assumption not rejected (but doesn't prove PH holds)
# p < 0.05: evidence of non-proportionality for that covariate

# Visual check — more informative than the p-value alone
# Horizontal band of residuals -> PH holds
# Systematic trend (slope) -> PH violated, effect changes over time
plot(zph)
# Or with survminer: survminer::ggcoxzph(zph)
```

```
Interpreting Schoenfeld residuals:
  Positive slope: effect increases over time (HR drifts upward)
  Negative slope: effect weakens over time (early benefit that fades)
  U-shape or crossing zero: complex time-varying effect

  The p-value is sample-size dependent: large datasets reject PH
  for clinically negligible departures. Always look at the plot.
```

### Handling PH Violations

```r
# Option 1: Time-varying coefficient with tt()
# Preferred when a specific covariate violates PH
cox_tv <- coxph(
  Surv(os_months, os_event) ~ age_at_diagnosis + tt(treatment),
  data = clinical,
  tt = function(x, t, ...) x * log(t + 1)
)
# Tests whether treatment effect changes with log(time)
# Significant tt() term confirms time-varying effect

# Option 2: Stratification — for nuisance variables
# Each stratum gets its own baseline hazard; no HR estimated for that variable
cox_strat <- coxph(
  Surv(os_months, os_event) ~ age_at_diagnosis + mgmt_methylation + strata(center),
  data = clinical
)
# Re-run cox.zph() after stratification to confirm remaining covariates satisfy PH

# Option 3: Time-splitting with tmerge() — for time-varying covariates
# When a covariate value changes during follow-up (e.g., treatment switch)
library(survival)
td_data <- tmerge(
  data1 = clinical, data2 = clinical,
  id = patient_id,
  os_event = event(os_months, os_event),
  treatment_switch = tdc(switch_time, new_treatment)
)
cox_td <- coxph(Surv(tstart, tstop, os_event) ~ treatment_switch + age_at_diagnosis,
  data = td_data)
```

## Competing Risks

```
Two hazard models — they answer different questions:

Cause-specific hazard (CSH):
  "Does treatment affect the rate of cancer death among patients still alive?"
  Standard coxph() treating competing events as censored.
  Use for: etiological questions, causal inference.

Fine-Gray subdistribution hazard (SDH):
  "Does treatment affect the cumulative probability of dying from cancer
   when competing events are accounted for?"
  Use for: prediction, prognostic models, clinical decision-making.

Run both and report side-by-side.
A covariate can have a significant CSH but non-significant SDH (or vice versa)
because they measure different things.
```

```r
library(tidycmprsk)  # v1.1+, wraps cmprsk with tidy interface
library(ggsurvfit)

# Event coding for competing risks:
# 0 = censored, 1 = event of interest, 2 = competing event
# Example: 1 = cancer death, 2 = death from other cause
clinical$event_type <- factor(
  ifelse(clinical$os_event == 0, "censored",
    ifelse(clinical$cause_of_death == "cancer", "cancer_death", "other_death")),
  levels = c("censored", "cancer_death", "other_death")
)

# Cumulative incidence function (CIF)
cif <- cuminc(Surv(os_months, event_type) ~ treatment, data = clinical)

ggcuminc(cif, outcome = "cancer_death") +
  add_risktable() +
  labs(x = "Months", y = "Cumulative incidence of cancer death") +
  theme_classic(base_size = 12)

# Fine-Gray regression (subdistribution hazard)
fg <- crr(Surv(os_months, event_type) ~ age + treatment + stage,
  data = clinical, failcode = "cancer_death")
summary(fg)

# Cause-specific Cox (standard Cox, treating competing events as censored)
clinical$cancer_event <- ifelse(clinical$event_type == "cancer_death", 1, 0)
cs <- coxph(Surv(os_months, cancer_event) ~ age + treatment + stage, data = clinical)
summary(cs)
```

## Restricted Mean Survival Time

```r
library(survRM2)  # v1.0-4

# RMST: area under the survival curve up to time tau
# Avoids the PH assumption entirely — compares mean survival time between groups

rmst <- rmst2(
  time = clinical$os_months,
  status = clinical$os_event,
  arm = as.numeric(clinical$treatment == "experimental"),
  tau = 24  # restrict to 24 months — must be pre-specified
)
print(rmst)
# Returns:
#   RMST difference (treatment - control), CI, p-value
#   RMST ratio
#   RMTL ratio (restricted mean time lost)

# tau must be less than the minimum of the largest observed time in each group.
# Pre-specify tau based on clinical context (e.g., 12, 24, 36 months).
# Run sensitivity analysis across multiple tau values.
```

```
When to use RMST vs HR:
  Proportional hazards hold?
    -> HR is more efficient. Report both HR and RMST.
  Curves cross or separate late (immunotherapy, delayed effect)?
    -> RMST captures the difference that HR misses.
  Need a clinically interpretable number?
    -> RMST: "Treatment gives 3.2 extra months of survival on average"
       HR: "Treatment reduces the hazard by 30%" (less intuitive)
```

## Optimal Cutpoint Selection

```r
library(survminer)  # v0.5+, provides surv_cutpoint

# maxstat approach: maximally selected log-rank statistic
# Finds the cutpoint that maximally separates high/low groups
cp <- surv_cutpoint(clinical, time = "os_months", event = "os_event",
  variables = "biomarker_score")
summary(cp)
cat(sprintf("Optimal cutpoint: %.2f (corrected p = %.4f)\n",
  cp$cutpoint$cutpoint, cp$cutpoint$statistic))

# Categorize samples at the cutpoint
clinical$biomarker_group <- surv_categorize(cp)$biomarker_score

# Plot with survminer (surv_cutpoint is survminer-specific, not ggsurvfit)
fit_cp <- survfit(Surv(os_months, os_event) ~ biomarker_group, data = clinical)
ggsurvplot(fit_cp, data = clinical, pval = TRUE, risk.table = TRUE)
```

```
Cutpoint pitfalls — read before using:
  1. Inflated significance: searching all cutpoints maximizes the test statistic.
     The p-value from maxstat is corrected for this, but the effect size (HR)
     is still biased upward. A random variable can appear highly prognostic.

  2. Non-reproducibility: data-driven cutpoints rarely replicate.
     Any cutpoint found this way MUST be validated in an independent cohort
     or via cross-validation. Without validation, it is a hypothesis, not a finding.

  3. Information loss: dichotomizing a continuous biomarker at any cutpoint
     discards information. A continuous covariate in Cox regression is almost
     always more powerful than a dichotomized one.

  4. When cutpoints are justified:
     - Clinical decision-making (treat/don't treat needs a threshold)
     - An established cutpoint exists (Ki-67 > 14%, PSA > 4 ng/mL)
     - Communication to non-statistical audiences

  Use continuous modeling for primary analysis, cutpoints for clinical translation.
```

## Forest Plots

```r
library(forestmodel)  # v0.6+

# Directly from a coxph object — one function call
forest_model(cox_multi)
# Produces a ggplot2-based forest plot with HRs, 95% CIs, p-values

# Customize
forest_model(cox_multi,
  factor_separate_line = TRUE,       # categorical levels on separate lines
  format_options = forest_model_format_options(
    text_size = 3.5, point_size = 3
  )
)

# Alternative: survminer::ggforest() for quick plots
# Limitation: does not handle interactions or spline terms properly
survminer::ggforest(cox_multi, data = clinical)
```

## Output Specification

| Output | Format | Description |
|--------|--------|-------------|
| `km_curves.pdf` | PDF | Kaplan-Meier curves with risk table and p-value |
| `cox_summary.csv` | CSV | HR, 95% CI, p-value for each covariate |
| `cox_zph.pdf` | PDF | Schoenfeld residual plots for PH assumption |
| `forest_plot.pdf` | PDF | Multivariate Cox forest plot |
| `cif_curves.pdf` | PDF | Cumulative incidence curves for competing risks |
| `rmst_results.csv` | CSV | RMST difference, ratio, CI, p-value |
| `cutpoint_analysis.csv` | CSV | Optimal cutpoint, corrected p-value, HR at cutpoint |

## Validation Checks

```
After running survival analysis on TCGA-GBM, verify:

Overall survival:
  Median OS for all GBM: ~14-16 months
  If median OS > 24 months: likely includes IDH-mutant cases (not true GBM under WHO 2021)
  2-year survival: ~20-25%

IDH1 mutation (strongest single prognostic factor in glioma):
  IDH-mutant median OS: ~31 months
  IDH-wildtype median OS: ~14-16 months
  Log-rank p-value: should be < 0.001
  Cox HR for IDH-mutant vs wildtype: ~0.3-0.4 (strong protective effect)
  IDH1 R132H mutation frequency: ~6% of original TCGA-GBM cohort

MGMT promoter methylation:
  MGMT methylated: ~42% of IDH-wildtype GBMs
  Methylated vs unmethylated: HR ~0.5-0.6
  This is both prognostic (survival) and predictive (TMZ response)

Cox model quality:
  C-index with IDH + MGMT + age: ~0.65-0.75
  EPV check: with ~400 events and 3-5 covariates, EPV is adequate (> 80)

Proportional hazards:
  Age typically satisfies PH in GBM (chronic risk factor)
  Treatment effect may violate PH (delayed separation with TMZ)
  If global cox.zph p < 0.05, identify the violating covariate

WHO 2021 note:
  "Glioblastoma" is now restricted to IDH-wildtype tumors.
  IDH-mutant grade 4 gliomas are reclassified as "Astrocytoma, IDH-mutant, Grade 4."
  When using TCGA-GBM data, reclassify or note this in your analysis.
```

## Common Pitfalls

### Kaplan-Meier
1. **Median follow-up from the KM estimate**: The median of the KM curve is median survival time, not median follow-up. Calculate median follow-up using the reverse KM method: `survfit(Surv(time, 1-event) ~ 1)`. Short follow-up with few events makes survival estimates unreliable beyond the last observed event.
2. **Interpreting the tail**: KM curves at the right end are based on very few patients. Wide confidence intervals there mean the curve is unreliable. Truncate plots at the time when < 10% of patients remain at risk.

### Cox Regression
3. **Ignoring the PH assumption**: Running `coxph()` and reporting HRs without checking `cox.zph()` first. If PH is violated, the reported HR is an average over time and may be misleading for both early and late effects.
4. **Overfitting**: Including too many covariates relative to events. With 50 events and 10 covariates, the model is unstable. Follow the EPV >= 10 rule (preferably >= 20).
5. **Stepwise selection for final models**: Forward/backward stepwise selection inflates Type I error and produces non-reproducible models. Pre-specify covariates based on clinical knowledge.
6. **Ignoring collinearity**: Stage and tumor size are correlated. Including both in a Cox model inflates standard errors and produces unstable HRs. Check VIF or pairwise correlations before fitting.

### Competing Risks
7. **Standard KM for competing risks endpoints**: KM treats competing events as censored, which inflates cumulative incidence of the event of interest. Use cumulative incidence functions (CIF) via `tidycmprsk::cuminc()` when competing events are present.
8. **Interpreting Fine-Gray as causal**: Fine-Gray SDH measures the effect on cumulative incidence, not on the rate among those at risk. A covariate that increases competing event risk will artificially appear to decrease the subdistribution hazard for the primary event.

### RMST and Cutpoints
9. **Post-hoc tau selection**: Choosing tau after seeing the data invalidates the RMST test. Pre-specify tau based on clinical context (standard follow-up duration, planned analysis timepoint).
10. **Cutpoint without validation**: An optimal cutpoint found by maxstat will appear highly significant in the discovery cohort even for a non-prognostic biomarker. Without independent validation, the cutpoint is a hypothesis, not a result.

## Related Skills

- [`cancer-multiomics`](../cancer-multiomics/SKILL.md): TCGA data retrieval, mutation status and gene expression for Cox covariates
- [`immune-deconvolution`](../immune-deconvolution/SKILL.md): Immune cell fraction estimates as continuous survival predictors

## Public Datasets for Testing

| Dataset | Samples | Use Case |
|---------|---------|----------|
| TCGA-GBM | 611 | Glioblastoma, strong IDH1/MGMT prognostic markers, poor prognosis |
| TCGA-BRCA | 1098 | Breast cancer, molecular subtype-specific survival differences |
| TCGA-LUAD | 585 | Lung adenocarcinoma, EGFR/KRAS mutation-driven survival |
| TCGA-OV | 608 | Ovarian cancer, classic for competing risks (progression vs death) |
