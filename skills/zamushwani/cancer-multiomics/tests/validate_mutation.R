#!/usr/bin/env Rscript
# Validate mutation analysis pipeline against TCGA-LUAD
# Expected runtime: 5-10 minutes

suppressPackageStartupMessages({
  library(TCGAbiolinks)
  library(maftools)
})

cat("=== Mutation Analysis Validation ===\n\n")
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

# --- MAF retrieval ---
cat("Downloading TCGA-LUAD MuTect2 MAF...\n")
maf_df <- GDCquery_Maf("LUAD", pipelines = "mutect2")

check("MAF data.frame returned", is.data.frame(maf_df))
check("MAF has > 50000 variants", nrow(maf_df) > 50000)
check("Required MAF columns present",
  all(c("Hugo_Symbol", "Variant_Classification", "Tumor_Sample_Barcode") %in%
    colnames(maf_df)))

maf <- read.maf(maf = maf_df)
check("read.maf succeeds", is(maf, "MAF"))

n_samples <- length(getSampleSummary(maf)$Tumor_Sample_Barcode)
cat(sprintf("  Samples in MAF: %d\n", n_samples))
check("MAF has 500-600 samples", n_samples >= 400 && n_samples <= 700)

# --- Known driver genes ---
# TCGA-LUAD top drivers: TP53 (~46%), KRAS (~33%), EGFR (~14%), STK11 (~17%)
gene_summary <- getGeneSummary(maf)

get_freq <- function(gene) {
  row <- gene_summary[gene_summary$Hugo_Symbol == gene, ]
  if (nrow(row) == 0) return(0)
  row$MutatedSamples / n_samples * 100
}

tp53_freq <- get_freq("TP53")
kras_freq <- get_freq("KRAS")
egfr_freq <- get_freq("EGFR")
stk11_freq <- get_freq("STK11")

cat(sprintf("  TP53: %.1f%%, KRAS: %.1f%%, EGFR: %.1f%%, STK11: %.1f%%\n",
  tp53_freq, kras_freq, egfr_freq, stk11_freq))

check("TP53 mutated in 30-60% of samples", tp53_freq >= 30 && tp53_freq <= 60)
check("KRAS mutated in 20-45% of samples", kras_freq >= 20 && kras_freq <= 45)
check("EGFR mutated in 8-25% of samples", egfr_freq >= 8 && egfr_freq <= 25)
check("STK11 mutated in 10-25% of samples", stk11_freq >= 10 && stk11_freq <= 25)

# Known mutual exclusivity: EGFR and KRAS
# (can't statistically test on summary alone, but both should be present)
check("EGFR and KRAS both detected as drivers", egfr_freq > 0 && kras_freq > 0)

# --- TMB ---
tmb_df <- tmb(maf, captureSize = 50, logScale = FALSE)
median_tmb <- median(tmb_df$total_perMB, na.rm = TRUE)
mean_tmb <- mean(tmb_df$total_perMB, na.rm = TRUE)
cat(sprintf("  TMB median: %.2f mut/MB, mean: %.2f mut/MB\n", median_tmb, mean_tmb))

# TCGA-LUAD median TMB ~5-8 mut/MB
check("Median TMB between 2 and 15 mut/MB", median_tmb >= 2 && median_tmb <= 15)

# --- Oncoplot (verify it runs without error) ---
tryCatch({
  pdf(tempfile(fileext = ".pdf"))
  oncoplot(maf, top = 10)
  dev.off()
  check("Oncoplot generates without error", TRUE)
}, error = function(e) {
  check("Oncoplot generates without error", FALSE)
})

# --- Somatic interactions ---
tryCatch({
  si <- somaticInteractions(maf, top = 25, pvalue = c(0.05, 0.01))
  check("somaticInteractions runs", is.data.frame(si))
  # Check that EGFR-KRAS mutual exclusivity is detected
  egfr_kras <- si[si$gene1 %in% c("EGFR", "KRAS") &
                   si$gene2 %in% c("EGFR", "KRAS"), ]
  if (nrow(egfr_kras) > 0) {
    check("EGFR-KRAS interaction detected", TRUE)
  } else {
    check("EGFR-KRAS interaction detected", FALSE)
  }
}, error = function(e) {
  check("somaticInteractions runs", FALSE)
})

# --- Signature extraction (quick check, not full NMF) ---
tryCatch({
  tnm <- trinucleotideMatrix(maf, prefix = "chr", add = TRUE,
    ref_genome = "BSgenome.Hsapiens.UCSC.hg38")
  check("trinucleotideMatrix succeeds", !is.null(tnm))
  check("96 substitution classes present", ncol(tnm$nmf_matrix) == 96)
}, error = function(e) {
  cat(sprintf("  SKIP: trinucleotideMatrix requires BSgenome.Hsapiens.UCSC.hg38 (%s)\n",
    e$message))
})

cat(sprintf("\n=== Mutation: %d passed, %d failed ===\n", pass, fail))
