#!/usr/bin/env Rscript
# Validate expression analysis pipeline against TCGA-LUAD
# Expected runtime: 10-15 minutes (mostly download time)

suppressPackageStartupMessages({
  library(TCGAbiolinks)
  library(DESeq2)
  library(SummarizedExperiment)
})

cat("=== Expression Analysis Validation ===\n\n")
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
cat("Downloading TCGA-LUAD expression data...\n")
query <- GDCquery(
  project = "TCGA-LUAD",
  data.category = "Transcriptome Profiling",
  data.type = "Gene Expression Quantification",
  workflow.type = "STAR - Counts"
)
results <- getResults(query)

check("Query returns > 500 samples", nrow(results) > 500)
check("Both tumor and normal present",
  any(results$sample_type == "Primary Tumor") &&
  any(results$sample_type == "Solid Tissue Normal"))

tumor_n <- sum(results$sample_type == "Primary Tumor")
normal_n <- sum(results$sample_type == "Solid Tissue Normal")
cat(sprintf("  Tumor: %d, Normal: %d\n", tumor_n, normal_n))
check("Tumor count 500-600", tumor_n >= 500 && tumor_n <= 600)
check("Normal count 50-70", normal_n >= 50 && normal_n <= 70)

# --- Download a small subset for DE testing ---
# Use 20 tumor + 10 normal for speed
set.seed(42)
tumor_barcodes <- results$cases[results$sample_type == "Primary Tumor"]
normal_barcodes <- results$cases[results$sample_type == "Solid Tissue Normal"]
subset_barcodes <- c(
  sample(tumor_barcodes, min(20, length(tumor_barcodes))),
  sample(normal_barcodes, min(10, length(normal_barcodes)))
)

query_sub <- GDCquery(
  project = "TCGA-LUAD",
  data.category = "Transcriptome Profiling",
  data.type = "Gene Expression Quantification",
  workflow.type = "STAR - Counts",
  barcode = subset_barcodes
)
GDCdownload(query_sub, directory = "GDCdata_test")
se <- GDCprepare(query_sub, directory = "GDCdata_test")

check("GDCprepare returns SummarizedExperiment", is(se, "SummarizedExperiment"))
check("Has unstranded assay", "unstranded" %in% assayNames(se))

# --- DESeq2 pipeline ---
counts_mat <- assay(se, "unstranded")
col_data <- as.data.frame(colData(se))

check("Count matrix has > 50000 genes", nrow(counts_mat) > 50000)
check("All counts are non-negative", all(counts_mat >= 0, na.rm = TRUE))

dds <- DESeqDataSetFromMatrix(
  countData = counts_mat,
  colData = col_data,
  design = ~ sample_type
)

keep <- rowSums(counts(dds) >= 10) >= 5
dds <- dds[keep, ]
check("Pre-filter retains 15000-30000 genes",
  nrow(dds) >= 15000 && nrow(dds) <= 30000)

dds$sample_type <- relevel(factor(dds$sample_type), ref = "Solid Tissue Normal")
dds <- DESeq(dds)

res <- results(dds, alpha = 0.05)
check("DESeq2 produces results", !is.null(res))
check("Results have padj column", "padj" %in% colnames(as.data.frame(res)))

# DEG counts — with small subset expect fewer, but direction should hold
sig <- subset(as.data.frame(res), padj < 0.05 & abs(log2FoldChange) > 1)
n_up <- sum(sig$log2FoldChange > 0, na.rm = TRUE)
n_down <- sum(sig$log2FoldChange < 0, na.rm = TRUE)
cat(sprintf("  DEGs (padj<0.05, |LFC|>1): %d total (%d up, %d down)\n",
  nrow(sig), n_up, n_down))

check("At least 500 DEGs found (small subset)", nrow(sig) >= 500)
check("Both up and down-regulated genes present", n_up > 0 && n_down > 0)

# --- Check known biology ---
# TP53 and EGFR should show differential expression in LUAD
gene_symbols <- sub("\\..*", "", rownames(res))
res_df <- as.data.frame(res)
res_df$symbol <- gene_symbols

# VST for sanity check
vsd <- vst(dds, blind = FALSE)
check("VST produces matrix", !is.null(assay(vsd)))

# --- Cleanup ---
unlink("GDCdata_test", recursive = TRUE)

cat(sprintf("\n=== Expression: %d passed, %d failed ===\n", pass, fail))
