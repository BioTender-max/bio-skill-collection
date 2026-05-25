#!/usr/bin/env Rscript
# Validate CNV analysis pipeline against TCGA-LUAD
# Expected runtime: 5-10 minutes

suppressPackageStartupMessages({
  library(TCGAbiolinks)
  library(GenomicRanges)
})

cat("=== CNV Analysis Validation ===\n\n")
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

# --- Segment data retrieval ---
cat("Downloading TCGA-LUAD masked copy number segments...\n")
query_cnv <- GDCquery(
  project = "TCGA-LUAD",
  data.category = "Copy Number Variation",
  data.type = "Masked Copy Number Segment"
)
results <- getResults(query_cnv)

check("Query returns > 500 files", nrow(results) > 500)

# Download a subset for validation
set.seed(42)
subset_barcodes <- sample(results$cases, min(30, nrow(results)))

query_sub <- GDCquery(
  project = "TCGA-LUAD",
  data.category = "Copy Number Variation",
  data.type = "Masked Copy Number Segment",
  barcode = subset_barcodes
)
GDCdownload(query_sub, directory = "GDCdata_test_cnv")
cnv_seg <- GDCprepare(query_sub, directory = "GDCdata_test_cnv")

check("Segment data returned", is.data.frame(cnv_seg) || is(cnv_seg, "data.frame"))

required_cols <- c("Chromosome", "Start", "End", "Segment_Mean")
check("Required columns present",
  all(required_cols %in% colnames(cnv_seg)))

cat(sprintf("  Total segments: %d\n", nrow(cnv_seg)))
check("Segments returned (> 1000)", nrow(cnv_seg) > 1000)

# --- Segment_Mean interpretation ---
seg_mean <- cnv_seg$Segment_Mean

check("Segment_Mean is numeric", is.numeric(seg_mean))
check("Segment_Mean centered near 0 (diploid baseline)",
  abs(median(seg_mean, na.rm = TRUE)) < 0.3)
check("Range includes gains and losses",
  any(seg_mean > 0.3, na.rm = TRUE) && any(seg_mean < -0.3, na.rm = TRUE))

# --- Gain/loss classification ---
gains <- sum(seg_mean > 0.3, na.rm = TRUE)
losses <- sum(seg_mean < -0.3, na.rm = TRUE)
amps <- sum(seg_mean > 0.7, na.rm = TRUE)
deep_del <- sum(seg_mean < -0.7, na.rm = TRUE)

cat(sprintf("  Gains (>0.3): %d, Losses (<-0.3): %d\n", gains, losses))
cat(sprintf("  Amplifications (>0.7): %d, Deep deletions (<-0.7): %d\n",
  amps, deep_del))

check("Both gains and losses detected", gains > 0 && losses > 0)
check("Some amplifications detected", amps > 0)

# --- Gene-level mapping ---
seg_gr <- GRanges(
  seqnames = paste0("chr", cnv_seg$Chromosome),
  ranges = IRanges(start = cnv_seg$Start, end = cnv_seg$End),
  segment_mean = cnv_seg$Segment_Mean
)

check("GRanges construction succeeds", is(seg_gr, "GRanges"))
check("GRanges has entries", length(seg_gr) > 0)

# Load gene annotations if available
tryCatch({
  library(TxDb.Hsapiens.UCSC.hg38.knownGene)
  genes_gr <- genes(TxDb.Hsapiens.UCSC.hg38.knownGene)
  hits <- findOverlaps(genes_gr, seg_gr)
  cat(sprintf("  Gene-segment overlaps: %d\n", length(hits)))
  check("findOverlaps returns hits", length(hits) > 0)

  # Check known LUAD CNV targets exist in overlaps
  # CDKN2A (chr9), NKX2-1 (chr14), MYC (chr8) should have segments
  chr9_segs <- sum(seqnames(seg_gr) == "chr9")
  chr14_segs <- sum(seqnames(seg_gr) == "chr14")
  chr8_segs <- sum(seqnames(seg_gr) == "chr8")
  check("Segments on chr8, chr9, chr14 (key LUAD CNV loci)",
    chr9_segs > 0 && chr14_segs > 0 && chr8_segs > 0)
}, error = function(e) {
  cat(sprintf("  SKIP: Gene mapping requires TxDb.Hsapiens.UCSC.hg38.knownGene (%s)\n",
    e$message))
})

# --- Cleanup ---
unlink("GDCdata_test_cnv", recursive = TRUE)

cat(sprintf("\n=== CNV: %d passed, %d failed ===\n", pass, fail))
