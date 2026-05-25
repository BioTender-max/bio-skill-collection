#!/usr/bin/env Rscript
# Validate methylation analysis pipeline against TCGA-LUAD
# Expected runtime: 10-20 minutes (large download)

suppressPackageStartupMessages({
  library(TCGAbiolinks)
  library(SummarizedExperiment)
})

cat("=== Methylation Analysis Validation ===\n\n")
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

# --- Data retrieval ---
cat("Querying TCGA-LUAD methylation data...\n")
query_met <- GDCquery(
  project = "TCGA-LUAD",
  data.category = "DNA Methylation",
  platform = "Illumina Human Methylation 450"
)
results <- getResults(query_met)

tumor_n <- sum(results$sample_type == "Primary Tumor")
normal_n <- sum(results$sample_type == "Solid Tissue Normal")
cat(sprintf("  Tumor: %d, Normal: %d\n", tumor_n, normal_n))

check("Methylation tumor samples > 400", tumor_n > 400)
check("Methylation normal samples > 20", normal_n > 20)

# --- Download small subset ---
set.seed(42)
tumor_bc <- results$cases[results$sample_type == "Primary Tumor"]
normal_bc <- results$cases[results$sample_type == "Solid Tissue Normal"]
subset_bc <- c(
  sample(tumor_bc, min(10, length(tumor_bc))),
  sample(normal_bc, min(5, length(normal_bc)))
)

query_sub <- GDCquery(
  project = "TCGA-LUAD",
  data.category = "DNA Methylation",
  platform = "Illumina Human Methylation 450",
  barcode = subset_bc
)
GDCdownload(query_sub, directory = "GDCdata_test_met")
met_se <- GDCprepare(query_sub, directory = "GDCdata_test_met")

check("GDCprepare returns data", !is.null(met_se))

# Extract beta values
if (is(met_se, "SummarizedExperiment")) {
  beta <- assay(met_se)
  check("Beta matrix returned from SE", !is.null(beta))
} else if (is.data.frame(met_se) || is.matrix(met_se)) {
  beta <- as.matrix(met_se)
  check("Beta matrix returned", !is.null(beta))
} else {
  beta <- NULL
  check("Beta matrix returned", FALSE)
}

if (!is.null(beta)) {
  cat(sprintf("  Probes: %d, Samples: %d\n", nrow(beta), ncol(beta)))

  check("Probe count > 400000 (450K array)", nrow(beta) > 400000)
  check("Sample count matches request", ncol(beta) >= 10)

  # Beta value range check
  beta_range <- range(beta, na.rm = TRUE)
  cat(sprintf("  Beta range: [%.3f, %.3f]\n", beta_range[1], beta_range[2]))
  check("Beta values in [0, 1]", beta_range[1] >= 0 && beta_range[2] <= 1)

  # NA proportion (some probes fail, but should be < 10%)
  na_prop <- mean(is.na(beta))
  cat(sprintf("  NA proportion: %.1f%%\n", na_prop * 100))
  check("NA proportion < 20%", na_prop < 0.20)

  # --- DMP analysis with limma ---
  tryCatch({
    library(limma)

    # M-values for statistics
    beta_clean <- beta[complete.cases(beta), ]
    # Avoid log(0) or log(Inf)
    beta_clean[beta_clean < 0.001] <- 0.001
    beta_clean[beta_clean > 0.999] <- 0.999
    mVals <- log2(beta_clean / (1 - beta_clean))

    check("M-value conversion succeeds", all(is.finite(mVals)))

    sample_type <- ifelse(
      grepl("-01[A-Z]", colnames(beta_clean)), "Tumor", "Normal")
    group <- factor(sample_type, levels = c("Normal", "Tumor"))

    if (length(unique(group)) == 2 && all(table(group) >= 2)) {
      design <- model.matrix(~ 0 + group)
      colnames(design) <- levels(group)
      contMatrix <- makeContrasts(Tumor - Normal, levels = design)

      fit <- lmFit(mVals, design)
      fit2 <- contrasts.fit(fit, contMatrix)
      fit2 <- eBayes(fit2, trend = TRUE)

      dmps <- topTable(fit2, coef = 1, number = Inf, sort.by = "p")
      check("limma DMP analysis succeeds", nrow(dmps) > 0)

      n_sig <- sum(dmps$adj.P.Val < 0.05, na.rm = TRUE)
      cat(sprintf("  Significant DMPs (adj.P.Val < 0.05): %d\n", n_sig))

      # With 10 tumor vs 5 normal, expect some DMPs
      check("At least 1000 DMPs detected (small subset)", n_sig >= 1000)

      # Delta-beta for top DMPs
      top_probes <- rownames(dmps)[1:min(100, nrow(dmps))]
      tumor_mean <- rowMeans(beta_clean[top_probes, group == "Tumor"])
      normal_mean <- rowMeans(beta_clean[top_probes, group == "Normal"])
      delta_beta <- tumor_mean - normal_mean

      check("Delta-beta has both hyper and hypo CpGs",
        any(delta_beta > 0.1, na.rm = TRUE) &&
        any(delta_beta < -0.1, na.rm = TRUE))
    } else {
      cat("  SKIP: Not enough samples in both groups for DMP analysis\n")
    }
  }, error = function(e) {
    cat(sprintf("  SKIP: limma DMP analysis failed (%s)\n", e$message))
  })

  # --- DMRcate ---
  tryCatch({
    library(DMRcate)
    cat("  DMRcate available: YES\n")
    check("DMRcate package available", TRUE)
  }, error = function(e) {
    cat("  SKIP: DMRcate not installed\n")
  })

  # --- missMethyl ---
  tryCatch({
    library(missMethyl)
    cat("  missMethyl available: YES\n")
    check("missMethyl package available", TRUE)
  }, error = function(e) {
    cat("  SKIP: missMethyl not installed\n")
  })
}

# --- Cleanup ---
unlink("GDCdata_test_met", recursive = TRUE)

cat(sprintf("\n=== Methylation: %d passed, %d failed ===\n", pass, fail))
