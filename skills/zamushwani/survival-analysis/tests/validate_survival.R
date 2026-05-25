#!/usr/bin/env Rscript
# Validate Kaplan-Meier survival analysis against TCGA-GBM
# Uses the full GBM clinical cohort (no expression download needed).
# Checks median OS, 2-year survival, and KM curve construction.
# Expected runtime: 2-5 minutes (clinical data only)

suppressPackageStartupMessages({
  library(TCGAbiolinks)
  library(survival)
})

cat("=== Survival Analysis Validation ===\n\n")
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

# --- Get full GBM clinical data ---
cat("Downloading TCGA-GBM clinical data...\n")
clinical <- GDCquery_clinic("TCGA-GBM")

check("Clinical data retrieved", !is.null(clinical) && nrow(clinical) > 0)
cat(sprintf("  Total patients: %d\n", nrow(clinical)))
check("More than 500 GBM patients", nrow(clinical) > 500)

# --- Construct survival endpoint ---
clinical$os_time <- ifelse(!is.na(clinical$days_to_death),
  as.numeric(clinical$days_to_death),
  as.numeric(clinical$days_to_last_follow_up))
clinical$os_event <- ifelse(clinical$vital_status == "Dead", 1, 0)
clinical$os_months <- clinical$os_time / 30.44

# Drop missing or invalid
clinical <- clinical[!is.na(clinical$os_months) & clinical$os_months > 0, ]
cat(sprintf("  Patients with valid survival data: %d\n", nrow(clinical)))
check("At least 400 patients with survival data", nrow(clinical) >= 400)

n_events <- sum(clinical$os_event == 1)
cat(sprintf("  Deaths (events): %d\n", n_events))
check("At least 300 events (deaths)", n_events >= 300)

# --- Kaplan-Meier overall ---
cat("\nOverall survival...\n")
km_all <- survfit(Surv(os_months, os_event) ~ 1, data = clinical)

med_os <- summary(km_all)$table["median"]
cat(sprintf("  Median OS: %.1f months\n", med_os))
check("Median OS between 12 and 18 months", med_os >= 12 && med_os <= 18)

# 2-year survival rate
surv_2yr <- summary(km_all, times = 24)$surv
cat(sprintf("  2-year survival: %.1f%%\n", surv_2yr * 100))
check("2-year survival between 15%% and 35%%", surv_2yr >= 0.15 && surv_2yr <= 0.35)

# --- Median follow-up (reverse KM) ---
km_fu <- survfit(Surv(os_months, 1 - os_event) ~ 1, data = clinical)
med_fu <- summary(km_fu)$table["median"]
cat(sprintf("  Median follow-up (reverse KM): %.1f months\n", med_fu))
check("Median follow-up > 6 months", med_fu > 6)

# --- KM by gender ---
cat("\nKaplan-Meier by gender...\n")
km_gender <- survfit(Surv(os_months, os_event) ~ gender, data = clinical)
check("KM by gender runs without error", !is.null(km_gender))

# Log-rank test
lr <- survdiff(Surv(os_months, os_event) ~ gender, data = clinical)
lr_p <- 1 - pchisq(lr$chisq, df = length(lr$n) - 1)
cat(sprintf("  Log-rank p-value (gender): %.4f\n", lr_p))
# Gender is NOT a strong prognostic factor in GBM — p may or may not be significant
# We just check the test runs and returns a valid p-value
check("Log-rank returns valid p-value", !is.na(lr_p) && lr_p >= 0 && lr_p <= 1)

# --- Age distribution ---
if ("age_at_index" %in% colnames(clinical)) {
  clinical$age <- as.numeric(clinical$age_at_index)
} else if ("age_at_diagnosis" %in% colnames(clinical)) {
  clinical$age <- as.numeric(clinical$age_at_diagnosis)
} else {
  clinical$age <- NA
}

if (any(!is.na(clinical$age))) {
  med_age <- median(clinical$age, na.rm = TRUE)
  cat(sprintf("\n  Median age at diagnosis: %.0f years\n", med_age))
  check("Median age 55-65 years (typical for GBM)", med_age >= 55 && med_age <= 65)
}

cat(sprintf("\n=== Survival: %d passed, %d failed ===\n", pass, fail))
