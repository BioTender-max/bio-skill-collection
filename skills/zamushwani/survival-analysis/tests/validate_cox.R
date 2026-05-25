#!/usr/bin/env Rscript
# Validate Cox proportional hazards against TCGA-GBM
# Tests Cox with age, PH assumption checking, and C-index.
# Expected runtime: 2-5 minutes (clinical data only)

suppressPackageStartupMessages({
  library(TCGAbiolinks)
  library(survival)
})

cat("=== Cox Regression Validation ===\n\n")
pass <- 0; fail <- 0

check <- function(name, condition) {
  if (isTRUE(condition)) {
    cat(sprintf("  PASS: %s\n", name))
    pass <<- pass + 1
  } else {
    cat(sprintf("  FAIL: %s\n", name))
    fail <<- fail + 1
  }
}

# --- Prepare clinical data ---
cat("Downloading TCGA-GBM clinical data...\n")
clinical <- GDCquery_clinic("TCGA-GBM")

clinical$os_time <- ifelse(!is.na(clinical$days_to_death),
  as.numeric(clinical$days_to_death),
  as.numeric(clinical$days_to_last_follow_up))
clinical$os_event <- ifelse(clinical$vital_status == "Dead", 1, 0)
clinical$os_months <- clinical$os_time / 30.44
clinical <- clinical[!is.na(clinical$os_months) & clinical$os_months > 0, ]

# Age variable
if ("age_at_index" %in% colnames(clinical)) {
  clinical$age <- as.numeric(clinical$age_at_index)
} else if ("age_at_diagnosis" %in% colnames(clinical)) {
  clinical$age <- as.numeric(clinical$age_at_diagnosis)
}
clinical <- clinical[!is.na(clinical$age), ]
cat(sprintf("  Patients with age + survival: %d\n", nrow(clinical)))

# --- Univariable Cox: Age ---
cat("\nCox regression with age...\n")
cox_age <- coxph(Surv(os_months, os_event) ~ age, data = clinical)
s <- summary(cox_age)

hr_age <- s$conf.int[1, "exp(coef)"]
hr_lo <- s$conf.int[1, "lower .95"]
hr_hi <- s$conf.int[1, "upper .95"]
p_age <- s$coefficients[1, "Pr(>|z|)"]

cat(sprintf("  Age HR per year: %.3f (95%% CI: %.3f-%.3f)\n", hr_age, hr_lo, hr_hi))
cat(sprintf("  Age p-value: %.4f\n", p_age))

# Published: HR ~1.02-1.05 per year in GBM (Ostrom 2014, various TCGA analyses)
check("Age HR between 1.01 and 1.06 per year", hr_age >= 1.01 && hr_age <= 1.06)
check("Age is significant (p < 0.05)", p_age < 0.05)

# --- PH assumption ---
cat("\nProportional hazards check (Schoenfeld residuals)...\n")
zph <- cox.zph(cox_age)
check("cox.zph() runs without error", !is.null(zph))

zph_p <- zph$table[1, "p"]
cat(sprintf("  cox.zph p-value for age: %.4f\n", zph_p))
# Age may or may not satisfy PH in GBM — just check the test runs
check("cox.zph returns valid p-value", !is.na(zph_p) && zph_p >= 0 && zph_p <= 1)

# --- Multivariable Cox: Age + Gender ---
cat("\nMultivariable Cox (age + gender)...\n")
clinical$gender <- factor(clinical$gender)
cox_multi <- coxph(Surv(os_months, os_event) ~ age + gender, data = clinical)
s_multi <- summary(cox_multi)

check("Multivariable model converges", !is.null(s_multi))

n_coef <- nrow(s_multi$coefficients)
cat(sprintf("  Number of coefficients: %d\n", n_coef))
check("Model has 2 coefficients (age + gender)", n_coef == 2)

# --- C-index ---
c_idx <- concordance(cox_multi)$concordance
cat(sprintf("  C-index: %.3f\n", c_idx))
check("C-index > 0.5 (better than random)", c_idx > 0.5)
# Age alone gives modest discrimination in GBM (~0.55-0.65)
check("C-index < 0.85 (not suspiciously high)", c_idx < 0.85)

# --- EPV check ---
n_events <- sum(clinical$os_event == 1)
n_vars <- n_coef
epv <- n_events / n_vars
cat(sprintf("  Events per variable: %.0f\n", epv))
check("EPV >= 10 (adequate model stability)", epv >= 10)

# --- PH check on multivariable model ---
cat("\ncox.zph on multivariable model...\n")
zph_multi <- cox.zph(cox_multi)
global_p <- zph_multi$table["GLOBAL", "p"]
cat(sprintf("  Global PH test p-value: %.4f\n", global_p))
check("Global cox.zph returns valid p-value",
  !is.na(global_p) && global_p >= 0 && global_p <= 1)

cat(sprintf("\n=== Cox: %d passed, %d failed ===\n", pass, fail))
