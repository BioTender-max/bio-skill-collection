#!/usr/bin/env Rscript
# Validate ESTIMATE purity estimation against TCGA-BRCA
# Checks immune/stromal scores, purity range, and purity-immune anticorrelation.
# Expected runtime: 15-20 minutes (mostly download time)

suppressPackageStartupMessages({
  library(TCGAbiolinks)
  library(SummarizedExperiment)
  library(org.Hs.eg.db)
  library(immunedeconv)
})

cat("=== Purity Estimation Validation ===\n\n")
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

# --- Prepare TPM (same 30-sample subset as deconvolution test) ---
cat("Downloading TCGA-BRCA expression subset (30 tumors)...\n")
query <- GDCquery(
  project = "TCGA-BRCA",
  data.category = "Transcriptome Profiling",
  data.type = "Gene Expression Quantification",
  workflow.type = "STAR - Counts"
)
results <- getResults(query)
tumor_results <- results[results$sample_type == "Primary Tumor", ]

set.seed(42)
subset_barcodes <- sample(tumor_results$cases, 30)

query_sub <- GDCquery(
  project = "TCGA-BRCA",
  data.category = "Transcriptome Profiling",
  data.type = "Gene Expression Quantification",
  workflow.type = "STAR - Counts",
  barcode = subset_barcodes
)
GDCdownload(query_sub, directory = "GDCdata_purity")
se <- GDCprepare(query_sub, directory = "GDCdata_purity")

tpm <- assay(se, "tpm_unstrand")
symbols <- mapIds(org.Hs.eg.db,
  keys = sub("\\..*", "", rownames(tpm)),
  keytype = "ENSEMBL", column = "SYMBOL", multiVals = "first")
tpm <- tpm[!is.na(symbols), ]
rownames(tpm) <- symbols[!is.na(symbols)]
if (any(duplicated(rownames(tpm)))) {
  means <- rowMeans(tpm)
  keep_idx <- ave(means, rownames(tpm), FUN = function(x) x == max(x)) == 1
  tpm <- tpm[keep_idx, ]
  tpm <- tpm[!duplicated(rownames(tpm)), ]
}

# --- Run ESTIMATE ---
cat("Running ESTIMATE...\n")
est <- deconvolute_estimate(tpm)

check("ESTIMATE returns result", !is.null(est))

rows <- rownames(est)
cat(sprintf("  Output rows: %s\n", paste(rows, collapse = ", ")))

check("Has StromalScore row", "StromalScore" %in% rows)
check("Has ImmuneScore row", "ImmuneScore" %in% rows)
check("Has ESTIMATEScore row", "ESTIMATEScore" %in% rows)
check("Has TumorPurity row", "TumorPurity" %in% rows)

# --- Purity range ---
purity <- as.numeric(est["TumorPurity", ])
check("All purity values are finite", all(is.finite(purity)))
check("All purity between 0 and 1", all(purity >= 0 & purity <= 1))

med_purity <- median(purity)
cat(sprintf("  Purity range: %.3f - %.3f\n", min(purity), max(purity)))
cat(sprintf("  Median purity: %.3f\n", med_purity))
check("Median purity 0.50-0.95 (BRCA)", med_purity >= 0.50 && med_purity <= 0.95)

# Purity should vary across samples (not constant)
purity_sd <- sd(purity)
cat(sprintf("  Purity SD: %.3f\n", purity_sd))
check("Purity SD > 0.05 (not constant)", purity_sd > 0.05)

# --- Score sanity ---
immune <- as.numeric(est["ImmuneScore", ])
stromal <- as.numeric(est["StromalScore", ])

check("ImmuneScore values are finite", all(is.finite(immune)))
check("StromalScore values are finite", all(is.finite(stromal)))

# Immune and stromal scores vary
check("ImmuneScore has variance", sd(immune) > 0)
check("StromalScore has variance", sd(stromal) > 0)

# --- Purity-immune anticorrelation ---
# Higher immune infiltration = lower purity (fundamental relationship)
rho <- cor(purity, immune, method = "spearman")
cat(sprintf("  Purity vs ImmuneScore rho: %.3f\n", rho))
check("Purity negatively correlated with ImmuneScore (rho < -0.3)", rho < -0.3)

# Purity-stromal anticorrelation (stromal content reduces purity too)
rho_stro <- cor(purity, stromal, method = "spearman")
cat(sprintf("  Purity vs StromalScore rho: %.3f\n", rho_stro))
check("Purity negatively correlated with StromalScore (rho < -0.3)", rho_stro < -0.3)

# --- Cross-validate with quanTIseq uncharacterized fraction ---
cat("\nCross-validating purity against quanTIseq...\n")
qt <- deconvolute(tpm, method = "quantiseq")
unchar <- as.numeric(qt[qt$cell_type == "uncharacterized cell", -1])

# ESTIMATE purity and quanTIseq "uncharacterized" both estimate non-immune content
rho_cross <- cor(purity, unchar, method = "spearman", use = "pairwise.complete.obs")
cat(sprintf("  ESTIMATE purity vs quanTIseq uncharacterized: rho = %.3f\n", rho_cross))
check("ESTIMATE purity correlates with quanTIseq uncharacterized (rho > 0.3)",
  rho_cross > 0.3)

# --- Cleanup ---
unlink("GDCdata_purity", recursive = TRUE)

cat(sprintf("\n=== Purity: %d passed, %d failed ===\n", pass, fail))
