#!/usr/bin/env Rscript
# Master validation script for cancer-multiomics skill
#
# Runs all validation tests against TCGA-LUAD public data.
# Tests verify that the code in SKILL.md produces expected results
# when run against real data.
#
# Usage:
#   Rscript run_all.R           # run all tests
#   Rscript run_all.R expression # run one test
#
# Expected runtime: 30-45 minutes (mostly TCGA downloads)
#
# Requirements:
#   Core: TCGAbiolinks, DESeq2, maftools, SummarizedExperiment, limma
#   Recommended: GenomicRanges, TxDb.Hsapiens.UCSC.hg38.knownGene,
#                BSgenome.Hsapiens.UCSC.hg38, DMRcate, missMethyl

args <- commandArgs(trailingOnly = TRUE)

tests <- c("expression", "mutation", "cnv", "methylation")
if (length(args) > 0) {
  tests <- match.arg(args[1], tests)
}

cat("Cancer Multi-Omics Skill Validation\n")
cat("====================================\n")
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

cat("\n====================================\n")
cat("Validation complete.\n")
