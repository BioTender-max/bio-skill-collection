#!/usr/bin/env Rscript
# Master validation script for immune-deconvolution skill
#
# Runs validation tests against TCGA-BRCA public data.
# Tests verify that deconvolution methods produce expected results
# on a well-characterized breast cancer cohort.
#
# Usage:
#   Rscript run_all.R                # run all tests
#   Rscript run_all.R deconvolution  # run one test
#
# Expected runtime: 45-60 minutes (mostly TCGA downloads)
#
# Requirements:
#   Core: TCGAbiolinks, SummarizedExperiment, immunedeconv, org.Hs.eg.db
#   immunedeconv wraps: quanTIseq, EPIC, MCP-counter, xCell, ESTIMATE

args <- commandArgs(trailingOnly = TRUE)

tests <- c("deconvolution", "purity", "subtypes")
if (length(args) > 0) {
  tests <- match.arg(args[1], tests)
}

cat("Immune Deconvolution Skill Validation\n")
cat("======================================\n")
cat(sprintf("Date: %s\n", Sys.time()))
cat(sprintf("R version: %s\n", R.version.string))
cat(sprintf("Tests to run: %s\n\n", paste(tests, collapse = ", ")))

script_dir <- dirname(sys.frame(1)$ofile)
if (is.null(script_dir) || script_dir == "") script_dir <- "."

for (test in tests) {
  script <- file.path(script_dir, sprintf("validate_%s.R", test))
  if (file.exists(script)) {
    cat(sprintf("\n--- Running %s validation ---\n\n", test))
    tryCatch(
      source(script, local = new.env()),
      error = function(e) {
        cat(sprintf("\nERROR in %s validation: %s\n", test, e$message))
      }
    )
  } else {
    cat(sprintf("Script not found: %s\n", script))
  }
}

cat("\n======================================\n")
cat("Validation complete.\n")
