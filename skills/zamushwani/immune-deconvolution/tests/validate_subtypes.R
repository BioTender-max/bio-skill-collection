#!/usr/bin/env Rscript
# Validate deconvolution results against TCGA-BRCA molecular subtypes
# Downloads a stratified subset (Basal + Luminal A) to test the expected
# ordering: Basal-like should have higher immune infiltration than Luminal A.
# Expected runtime: 20-30 minutes

suppressPackageStartupMessages({
  library(TCGAbiolinks)
  library(SummarizedExperiment)
  library(org.Hs.eg.db)
  library(immunedeconv)
})

cat("=== Subtype Validation ===\n\n")
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

# --- Get BRCA molecular subtypes ---
cat("Fetching BRCA PAM50 subtypes...\n")
subtypes <- tryCatch(
  TCGAquery_subtype("BRCA"),
  error = function(e) NULL
)

if (is.null(subtypes)) {
  cat("  SKIP: TCGAquery_subtype failed. Cannot run subtype validation.\n")
  cat("\n=== Subtypes: skipped ===\n")
  quit(save = "no")
}

# Find the PAM50 column — name varies across TCGAbiolinks versions
pam50_col <- grep("PAM50|Subtype_mRNA|pam50", colnames(subtypes), value = TRUE)
if (length(pam50_col) == 0) {
  cat("  SKIP: No PAM50 column found in subtype data.\n")
  cat(sprintf("  Available columns: %s\n",
    paste(head(colnames(subtypes), 20), collapse = ", ")))
  cat("\n=== Subtypes: skipped ===\n")
  quit(save = "no")
}
pam50_col <- pam50_col[1]
cat(sprintf("  Using subtype column: %s\n", pam50_col))

subtype_table <- table(subtypes[[pam50_col]])
cat("  Subtype distribution:\n")
print(subtype_table)

# Identify Basal and Luminal A patients
basal_patients <- subtypes$patient[subtypes[[pam50_col]] == "Basal"]
luma_patients <- subtypes$patient[subtypes[[pam50_col]] == "LumA"]

check("At least 50 Basal patients available", length(basal_patients) >= 50)
check("At least 200 Luminal A patients available", length(luma_patients) >= 200)

# --- Stratified download: 10 Basal + 10 Luminal A ---
set.seed(123)
sel_basal <- sample(basal_patients, min(10, length(basal_patients)))
sel_luma <- sample(luma_patients, min(10, length(luma_patients)))

cat(sprintf("\nDownloading %d Basal + %d Luminal A samples...\n",
  length(sel_basal), length(sel_luma)))

query <- GDCquery(
  project = "TCGA-BRCA",
  data.category = "Transcriptome Profiling",
  data.type = "Gene Expression Quantification",
  workflow.type = "STAR - Counts",
  barcode = c(sel_basal, sel_luma)
)
GDCdownload(query, directory = "GDCdata_subtypes")
se <- GDCprepare(query, directory = "GDCdata_subtypes")

# Keep only Primary Tumor samples
tumor_idx <- se$sample_type == "Primary Tumor"
se <- se[, tumor_idx]

# --- Prepare TPM ---
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

# Assign subtypes to samples (match on patient barcode prefix)
sample_patient <- substr(colnames(tpm), 1, 12)
sample_subtype <- ifelse(sample_patient %in% sel_basal, "Basal",
  ifelse(sample_patient %in% sel_luma, "LumA", "Other"))

n_basal <- sum(sample_subtype == "Basal")
n_luma <- sum(sample_subtype == "LumA")
cat(sprintf("  Matched samples — Basal: %d, LumA: %d\n", n_basal, n_luma))

if (n_basal < 3 || n_luma < 3) {
  cat("  SKIP: Too few samples per subtype for comparison.\n")
  unlink("GDCdata_subtypes", recursive = TRUE)
  cat(sprintf("\n=== Subtypes: %d passed, %d failed ===\n", pass, fail))
  quit(save = "no")
}

# --- Run deconvolution ---
cat("\nRunning quanTIseq...\n")
qt <- deconvolute(tpm, method = "quantiseq")

cat("Running MCP-counter...\n")
mcp <- deconvolute(tpm, method = "mcp_counter")

# --- Compare Basal vs Luminal A ---
cat("\nComparing Basal vs Luminal A...\n")

# quanTIseq CD8
cd8_qt <- as.numeric(qt[qt$cell_type == "T cell CD8+", -1])
cd8_basal_qt <- cd8_qt[sample_subtype == "Basal"]
cd8_luma_qt <- cd8_qt[sample_subtype == "LumA"]
cat(sprintf("  quanTIseq CD8 — Basal median: %.4f, LumA median: %.4f\n",
  median(cd8_basal_qt), median(cd8_luma_qt)))
check("quanTIseq: Basal CD8 > LumA CD8",
  median(cd8_basal_qt) > median(cd8_luma_qt))

# MCP-counter CD8
cd8_mcp <- as.numeric(mcp[grepl("CD8", mcp$cell_type), -1])
cd8_basal_mcp <- cd8_mcp[sample_subtype == "Basal"]
cd8_luma_mcp <- cd8_mcp[sample_subtype == "LumA"]
cat(sprintf("  MCP CD8 — Basal median: %.2f, LumA median: %.2f\n",
  median(cd8_basal_mcp), median(cd8_luma_mcp)))
check("MCP-counter: Basal CD8 > LumA CD8",
  median(cd8_basal_mcp) > median(cd8_luma_mcp))

# quanTIseq uncharacterized (proxy for purity)
# Basal should have lower uncharacterized (= more immune = lower purity)
unchar <- as.numeric(qt[qt$cell_type == "uncharacterized cell", -1])
unchar_basal <- unchar[sample_subtype == "Basal"]
unchar_luma <- unchar[sample_subtype == "LumA"]
cat(sprintf("  Uncharacterized — Basal median: %.3f, LumA median: %.3f\n",
  median(unchar_basal), median(unchar_luma)))
check("Basal has lower uncharacterized fraction (more immune)",
  median(unchar_basal) < median(unchar_luma))

# ESTIMATE purity should be lower in Basal
cat("\nRunning ESTIMATE...\n")
est <- deconvolute_estimate(tpm)
purity <- as.numeric(est["TumorPurity", ])
pur_basal <- purity[sample_subtype == "Basal"]
pur_luma <- purity[sample_subtype == "LumA"]
cat(sprintf("  Purity — Basal median: %.3f, LumA median: %.3f\n",
  median(pur_basal), median(pur_luma)))
check("ESTIMATE: Basal purity < LumA purity",
  median(pur_basal) < median(pur_luma))

# Wilcoxon test for CD8 difference
wt <- wilcox.test(cd8_mcp[sample_subtype == "Basal"],
  cd8_mcp[sample_subtype == "LumA"], alternative = "greater")
cat(sprintf("  MCP CD8 Wilcoxon p-value: %.4f\n", wt$p.value))
check("CD8 Basal > LumA is significant (p < 0.1)", wt$p.value < 0.1)

# --- Cleanup ---
unlink("GDCdata_subtypes", recursive = TRUE)

cat(sprintf("\n=== Subtypes: %d passed, %d failed ===\n", pass, fail))
