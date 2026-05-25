#!/usr/bin/env Rscript
# Validate known prognostic markers in TCGA-GBM
# Attempts to compare IDH-mutant vs IDH-wildtype survival using
# molecular subtype data from TCGAbiolinks.
# If subtype data is unavailable, tests skip gracefully.
# Expected runtime: 5-10 minutes

suppressPackageStartupMessages({
  library(TCGAbiolinks)
  library(survival)
})

cat("=== Prognostic Markers Validation ===\n\n")
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

# --- Get clinical data ---
cat("Downloading TCGA-GBM clinical data...\n")
clinical <- GDCquery_clinic("TCGA-GBM")

clinical$os_time <- ifelse(!is.na(clinical$days_to_death),
  as.numeric(clinical$days_to_death),
  as.numeric(clinical$days_to_last_follow_up))
clinical$os_event <- ifelse(clinical$vital_status == "Dead", 1, 0)
clinical$os_months <- clinical$os_time / 30.44
clinical <- clinical[!is.na(clinical$os_months) & clinical$os_months > 0, ]

# --- Try to get molecular subtypes (IDH status) ---
cat("Fetching GBM molecular subtype data...\n")
subtypes <- tryCatch(
  TCGAquery_subtype("GBM"),
  error = function(e) NULL
)

if (is.null(subtypes)) {
  cat("  SKIP: TCGAquery_subtype('GBM') failed.\n")
  cat("  Cannot validate IDH prognostic markers without subtype data.\n")
  cat(sprintf("\n=== Prognostic: %d passed, %d failed (subtype tests skipped) ===\n",
    pass, fail))
  quit(save = "no")
}

cat(sprintf("  Subtype data rows: %d\n", nrow(subtypes)))
cat(sprintf("  Subtype columns: %s\n",
  paste(head(colnames(subtypes), 15), collapse = ", ")))

# --- Find IDH column ---
idh_col <- grep("IDH|idh", colnames(subtypes), value = TRUE)
cat(sprintf("  IDH-related columns: %s\n",
  ifelse(length(idh_col) > 0, paste(idh_col, collapse = ", "), "none found")))

if (length(idh_col) == 0) {
  cat("  SKIP: No IDH column found in subtype data.\n")
  cat(sprintf("\n=== Prognostic: %d passed, %d failed (IDH tests skipped) ===\n",
    pass, fail))
  quit(save = "no")
}

idh_col <- idh_col[1]
subtypes$idh_status <- subtypes[[idh_col]]
cat(sprintf("  Using column: %s\n", idh_col))
cat("  IDH status distribution:\n")
print(table(subtypes$idh_status, useNA = "ifany"))

# --- Merge with clinical data ---
# Match on patient barcode (first 12 characters)
subtypes$patient <- substr(subtypes$patient, 1, 12)
clinical$patient <- substr(clinical$submitter_id, 1, 12)

merged <- merge(clinical, subtypes[, c("patient", "idh_status")],
  by = "patient", all.x = FALSE)
merged <- merged[!is.na(merged$idh_status), ]
cat(sprintf("\n  Merged samples with IDH status: %d\n", nrow(merged)))

if (nrow(merged) < 20) {
  cat("  SKIP: Too few samples with IDH status for comparison.\n")
  cat(sprintf("\n=== Prognostic: %d passed, %d failed ===\n", pass, fail))
  quit(save = "no")
}

# --- Standardize IDH status ---
# Different versions may label differently (Mutant/WT, mut/wt, etc.)
merged$idh_binary <- ifelse(
  grepl("Mut|mut|mutant|Mutant|YES|yes|IDH1|R132", merged$idh_status,
    ignore.case = TRUE),
  "Mutant", "Wildtype")

n_mut <- sum(merged$idh_binary == "Mutant")
n_wt <- sum(merged$idh_binary == "Wildtype")
cat(sprintf("  IDH-Mutant: %d, IDH-Wildtype: %d\n", n_mut, n_wt))

# IDH mutations are rare in primary GBM (~5-10%)
check("IDH-mutant frequency < 15%% of GBM",
  n_mut / (n_mut + n_wt) < 0.15)

if (n_mut < 3 || n_wt < 20) {
  cat("  SKIP: Not enough samples per IDH group.\n")
  cat(sprintf("\n=== Prognostic: %d passed, %d failed ===\n", pass, fail))
  quit(save = "no")
}

# --- KM by IDH status ---
cat("\nKaplan-Meier by IDH status...\n")
km_idh <- survfit(Surv(os_months, os_event) ~ idh_binary, data = merged)

med_mut <- summary(km_idh)$table[1, "median"]
med_wt <- summary(km_idh)$table[2, "median"]
cat(sprintf("  IDH-Mutant median OS: %.1f months\n", med_mut))
cat(sprintf("  IDH-Wildtype median OS: %.1f months\n", med_wt))

# IDH-mutant GBM has dramatically better prognosis
check("IDH-Mutant median OS > IDH-Wildtype", med_mut > med_wt)

# --- Log-rank test ---
lr <- survdiff(Surv(os_months, os_event) ~ idh_binary, data = merged)
lr_p <- 1 - pchisq(lr$chisq, df = 1)
cat(sprintf("  Log-rank p-value: %.6f\n", lr_p))
check("IDH log-rank p < 0.05", lr_p < 0.05)

# --- Cox HR for IDH ---
cox_idh <- coxph(Surv(os_months, os_event) ~ idh_binary, data = merged)
hr_idh <- summary(cox_idh)$conf.int["idh_binaryWildtype", "exp(coef)"]
cat(sprintf("  HR (Wildtype vs Mutant): %.2f\n", hr_idh))
# Wildtype vs Mutant HR should be > 1 (wildtype is worse)
check("IDH-Wildtype HR > 1.5 vs Mutant (worse prognosis)", hr_idh > 1.5)

cat(sprintf("\n=== Prognostic: %d passed, %d failed ===\n", pass, fail))
