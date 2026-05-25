#!/usr/bin/env Rscript
# Validate immune deconvolution methods against TCGA-BRCA
# Runs quanTIseq, EPIC, MCP-counter on a 30-sample subset.
# Checks output format, fraction ranges, and cross-method CD8 concordance.
# Expected runtime: 15-25 minutes (mostly download time)

suppressPackageStartupMessages({
  library(TCGAbiolinks)
  library(SummarizedExperiment)
  library(org.Hs.eg.db)
  library(immunedeconv)
})

cat("=== Deconvolution Methods Validation ===\n\n")
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
cat("Querying TCGA-BRCA expression data...\n")
query <- GDCquery(
  project = "TCGA-BRCA",
  data.category = "Transcriptome Profiling",
  data.type = "Gene Expression Quantification",
  workflow.type = "STAR - Counts"
)
results <- getResults(query)
tumor_results <- results[results$sample_type == "Primary Tumor", ]

check("TCGA-BRCA has > 1000 tumor samples", nrow(tumor_results) > 1000)

cat("Downloading 30-sample subset...\n")
set.seed(42)
subset_barcodes <- sample(tumor_results$cases, 30)

query_sub <- GDCquery(
  project = "TCGA-BRCA",
  data.category = "Transcriptome Profiling",
  data.type = "Gene Expression Quantification",
  workflow.type = "STAR - Counts",
  barcode = subset_barcodes
)
GDCdownload(query_sub, directory = "GDCdata_deconv")
se <- GDCprepare(query_sub, directory = "GDCdata_deconv")

# --- Prepare TPM matrix ---
tpm <- assay(se, "tpm_unstrand")

symbols <- mapIds(org.Hs.eg.db,
  keys = sub("\\..*", "", rownames(tpm)),
  keytype = "ENSEMBL", column = "SYMBOL", multiVals = "first")
tpm <- tpm[!is.na(symbols), ]
rownames(tpm) <- symbols[!is.na(symbols)]

# Deduplicate — quanTIseq crashes on duplicate rownames
if (any(duplicated(rownames(tpm)))) {
  means <- rowMeans(tpm)
  keep_idx <- ave(means, rownames(tpm), FUN = function(x) x == max(x)) == 1
  tpm <- tpm[keep_idx, ]
  tpm <- tpm[!duplicated(rownames(tpm)), ]
}

check("TPM has > 15000 mapped genes", nrow(tpm) > 15000)
check("30 samples in matrix", ncol(tpm) == 30)
check("No duplicate rownames", !any(duplicated(rownames(tpm))))
check("Not log-transformed (max TPM > 100)", max(tpm, na.rm = TRUE) > 100)

# --- quanTIseq ---
cat("\nRunning quanTIseq...\n")
qt <- deconvolute(tpm, method = "quantiseq")

check("quanTIseq returns data.frame", is.data.frame(qt))
check("Has cell_type column", "cell_type" %in% colnames(qt))
check("Returns 11 cell types", nrow(qt) == 11)
check("Includes uncharacterized cell", "uncharacterized cell" %in% qt$cell_type)

# Fractions sum to 1
qt_mat <- as.matrix(qt[, -1])
col_sums <- colSums(qt_mat, na.rm = TRUE)
check("Fractions sum to ~1 per sample", all(abs(col_sums - 1) < 0.01))

# Uncharacterized cell = mostly tumor in solid cancers
unchar <- as.numeric(qt[qt$cell_type == "uncharacterized cell", -1])
med_unchar <- median(unchar, na.rm = TRUE)
cat(sprintf("  Median uncharacterized fraction: %.3f\n", med_unchar))
check("Uncharacterized fraction 0.4-0.95", med_unchar >= 0.4 && med_unchar <= 0.95)

# M2 > M1 in most solid tumors
m1 <- median(as.numeric(qt[qt$cell_type == "Macrophage M1", -1]), na.rm = TRUE)
m2 <- median(as.numeric(qt[qt$cell_type == "Macrophage M2", -1]), na.rm = TRUE)
cat(sprintf("  Median M1: %.4f, M2: %.4f\n", m1, m2))
check("Macrophage M2 >= M1 (typical for solid tumors)", m2 >= m1)

# CD8 not all zero
cd8_qt <- as.numeric(qt[qt$cell_type == "T cell CD8+", -1])
check("CD8+ T cell fractions not all zero", any(cd8_qt > 0))

# --- EPIC ---
cat("\nRunning EPIC...\n")
epic <- deconvolute(tpm, method = "epic")

check("EPIC returns data.frame", is.data.frame(epic))
check("EPIC includes otherCells", "otherCells" %in% epic$cell_type)

other_cells <- as.numeric(epic[epic$cell_type == "otherCells", -1])
med_other <- median(other_cells, na.rm = TRUE)
cat(sprintf("  Median otherCells fraction: %.3f\n", med_other))
check("EPIC otherCells > 0.5 (solid tumor)", med_other > 0.5)

cd8_epic <- as.numeric(epic[epic$cell_type == "T cell CD8+", -1])
check("EPIC CD8+ not all zero", any(cd8_epic > 0))

# --- MCP-counter ---
cat("\nRunning MCP-counter...\n")
mcp <- deconvolute(tpm, method = "mcp_counter")

check("MCP-counter returns data.frame", is.data.frame(mcp))
check("MCP-counter has 10 populations", nrow(mcp) == 10)
check("Includes CD8+ T cells", any(grepl("CD8", mcp$cell_type)))
check("Includes Fibroblasts", any(grepl("Fibroblast", mcp$cell_type)))

cd8_mcp <- as.numeric(mcp[grepl("CD8", mcp$cell_type), -1])
check("MCP CD8+ scores not all zero", any(cd8_mcp > 0))

# --- Cross-method CD8+ T cell concordance ---
cat("\nCross-method concordance (CD8+ T cells)...\n")

rho_qt_epic <- cor(cd8_qt, cd8_epic, method = "spearman",
  use = "pairwise.complete.obs")
rho_qt_mcp <- cor(cd8_qt, cd8_mcp, method = "spearman",
  use = "pairwise.complete.obs")
rho_epic_mcp <- cor(cd8_epic, cd8_mcp, method = "spearman",
  use = "pairwise.complete.obs")

cat(sprintf("  quanTIseq vs EPIC:  rho = %.3f\n", rho_qt_epic))
cat(sprintf("  quanTIseq vs MCP:   rho = %.3f\n", rho_qt_mcp))
cat(sprintf("  EPIC vs MCP:        rho = %.3f\n", rho_epic_mcp))

check("quanTIseq-EPIC CD8 rho > 0.3", rho_qt_epic > 0.3)
check("quanTIseq-MCP CD8 rho > 0.3", rho_qt_mcp > 0.3)
check("EPIC-MCP CD8 rho > 0.3", rho_epic_mcp > 0.3)

# --- Cleanup ---
unlink("GDCdata_deconv", recursive = TRUE)

cat(sprintf("\n=== Deconvolution: %d passed, %d failed ===\n", pass, fail))
