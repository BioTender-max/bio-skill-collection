# Immune Deconvolution

Estimate immune and stromal cell composition from bulk RNA-seq using multiple algorithms. Wraps CIBERSORT, quanTIseq, EPIC, xCell, MCP-counter, TIMER, and ESTIMATE through the immunedeconv unified interface.

## When to Use This Skill

Activate when the user requests:
- Immune cell type estimation from bulk RNA-seq or microarray
- Tumor microenvironment characterization
- Immune subtype classification across a cancer cohort
- Tumor purity estimation from expression data
- Comparison of immune infiltration between conditions or subtypes
- Multi-method deconvolution benchmarking

## Inputs

| Data Type | Format | Source |
|-----------|--------|--------|
| Expression | TPM matrix (genes x samples), **not log-transformed** | TCGA via TCGAbiolinks, GEO |
| Clinical | Tabular (subtype, stage, outcome) | TCGA GDC, cBioPortal |
| Signature matrix | LM22.txt (for CIBERSORT only) | cibersortx.stanford.edu (registration required) |

All methods except TIMER and ESTIMATE need TPM with HGNC gene symbols as rownames. Raw counts and Ensembl IDs will produce wrong results silently.

---

## Preparing Input from TCGA

```r
library(TCGAbiolinks)
library(SummarizedExperiment)

query <- GDCquery(
  project = "TCGA-BRCA",
  data.category = "Transcriptome Profiling",
  data.type = "Gene Expression Quantification",
  workflow.type = "STAR - Counts"
)
GDCdownload(query, directory = "GDCdata")
se <- GDCprepare(query, directory = "GDCdata")

# Extract TPM — immunedeconv needs TPM, not counts
tpm <- assay(se, "tpm_unstrand")

# Convert Ensembl IDs to gene symbols
library(org.Hs.eg.db)
symbols <- mapIds(org.Hs.eg.db,
  keys = sub("\\..*", "", rownames(tpm)),
  keytype = "ENSEMBL", column = "SYMBOL", multiVals = "first")

# Drop unmapped genes, resolve duplicates by keeping highest mean expression
tpm <- tpm[!is.na(symbols), ]
rownames(tpm) <- symbols[!is.na(symbols)]

# Deduplicate: quanTIseq crashes on duplicate rownames
dups <- duplicated(rownames(tpm))
if (any(dups)) {
  means <- rowMeans(tpm)
  keep <- !duplicated(rownames(tpm)) |
    (duplicated(rownames(tpm)) & means == ave(means, rownames(tpm), FUN = max))
  tpm <- tpm[keep, ]
  tpm <- tpm[!duplicated(rownames(tpm)), ]  # safety net
}

# Keep only tumor samples for deconvolution
tumor_barcodes <- colData(se)$sample_type == "Primary Tumor"
tpm_tumor <- tpm[, tumor_barcodes]
```

## Method Selection

```
What do you need from the deconvolution?

Absolute cell fractions (values sum to 1, interpretable as proportions)?
  -> quanTIseq: 10 immune types + "Other". Validated against flow cytometry and IHC.
  -> EPIC: 6 immune types + cancer cells. Built for solid tumors.
  -> CIBERSORT absolute mode: 22 immune subtypes. Requires registration.

Relative proportions (which immune cells dominate, not how much)?
  -> CIBERSORT relative: 22 types. Gold standard, widely published.
  -> quanTIseq also works (ignore "Other", compare immune fractions).

Enrichment scores (rank samples by infiltration, not quantify)?
  -> xCell: 64 cell types. Broadest coverage, good for discovery.
  -> MCP-counter: 8 immune + 2 stromal. Fewest assumptions, works well with noisy data.

Immune vs stromal vs tumor purity?
  -> ESTIMATE: immune score, stromal score, purity estimate.
  -> Or use "Other" fraction from quanTIseq/EPIC as purity proxy.

Cancer-type-specific correction?
  -> TIMER: 6 immune types, pre-built models per TCGA cancer type.
  -> ConsensusTME: cancer-specific gene sets, uses ssGSEA.

Don't know which to pick?
  -> Run quanTIseq + MCP-counter + EPIC. If all three agree on a trend,
     the signal is real. Disagreement means the effect is method-dependent.
```

## Score Interpretation

This matters more than method choice. Getting it wrong leads to wrong biological conclusions.

| Comparison | Valid methods | Invalid methods |
|------------|-------------|-----------------|
| **Between samples** (sample A has more CD8 T cells than B) | All methods | - |
| **Between cell types** (more B cells than T cells in sample A) | quanTIseq, EPIC, CIBERSORT | xCell, MCP-counter, TIMER |
| **Absolute quantification** (15% of cells are CD8 T cells) | quanTIseq, EPIC, CIBERSORT-abs | Everything else |

xCell and MCP-counter scores are arbitrary units. A CD8 score of 0.4 from xCell and 3.7 from MCP-counter cannot be compared to each other, and neither means "40% CD8 T cells."

---

## immunedeconv Setup

```r
# Install: wraps 9 methods in one API
# remotes::install_github("omnideconv/immunedeconv")
library(immunedeconv)  # v2.1.0+

# For CIBERSORT (optional, requires registration at cibersortx.stanford.edu):
# Download CIBERSORT.R and LM22.txt, then:
# set_cibersort_binary("/path/to/CIBERSORT.R")
# set_cibersort_mat("/path/to/LM22.txt")
```

## quanTIseq

```r
qt <- deconvolute(tpm_tumor, method = "quantiseq")
# Returns tibble: cell_type column + one column per sample
# Cell types: B cell, Macrophage M1, Macrophage M2, Monocyte, Neutrophil,
#   NK cell, T cell CD4+ (non-regulatory), T cell CD8+,
#   T cell regulatory (Tregs), Myeloid dendritic cell,
#   uncharacterized cell

# Fractions sum to 1 per sample. "uncharacterized cell" = tumor + stroma.
# In solid tumors, "uncharacterized cell" should be 0.5-0.9.
# If < 0.3, check if sample is actually a lymphoma or immune-rich tissue.
```

## EPIC

```r
epic <- deconvolute(tpm_tumor, method = "epic")
# Cell types: B cell, CAFs, CD4+ T cell, CD8+ T cell,
#   Endothelial, Macrophage, NK cell, otherCells

# otherCells = uncharacterized (mostly tumor in solid cancers)
# EPIC was specifically built for solid tumors — preferred over
# quanTIseq when you need a cancer cell fraction estimate
```

## CIBERSORT

```r
# Requires setup (see above). LM22 has 22 immune subtypes:
# naive/memory B cells, plasma, CD8/CD4 subtypes, gamma-delta T,
# NK resting/activated, monocytes, M0/M1/M2 macrophages,
# DC resting/activated, mast resting/activated, eosinophils, neutrophils

cib <- deconvolute(tpm_tumor, method = "cibersort")
# Relative fractions (sum to 1 across 22 types)

cib_abs <- deconvolute(tpm_tumor, method = "cibersort_abs")
# Absolute mode: scales by total immune content

# CIBERSORT reports a p-value per sample from permutation testing.
# p > 0.05 means the deconvolution fit is unreliable — flag or exclude.
# Access via running CIBERSORT directly (not through immunedeconv wrapper).
```

## xCell

```r
xc <- deconvolute(tpm_tumor, method = "xcell")
# 64 cell types including fine subtypes:
#   T cell subtypes (Th1, Th2, Th17, Treg, CD8 naive, CD8 effector, etc.)
#   B cell subtypes (naive, memory, plasma)
#   Myeloid (M1, M2, DC subsets)
#   Stromal (fibroblasts, endothelial, pericytes)
# Plus composite: ImmuneScore, StromalScore, MicroenvironmentScore

# xCell uses ssGSEA followed by spillover correction.
# Scores are enrichment-based — only compare within a cell type across samples.
# All-zero scores for a cell type = not enough gene signature overlap.
# Check that your gene symbols are standard HGNC.
```

## MCP-counter

```r
mcp <- deconvolute(tpm_tumor, method = "mcp_counter")
# 10 populations: T cells, CD8+ T cells, Cytotoxic lymphocytes,
#   B lineage, NK cells, Monocytic lineage, Myeloid dendritic cells,
#   Neutrophils, Endothelial cells, Fibroblasts

# Scores are arbitrary units based on marker gene expression.
# Uses manually curated transcriptomic markers with minimal cell-type overlap
# with minimal overlap between cell types.
# Works well even with noisy or poorly normalized data.
```

## TIMER

```r
# TIMER uses tumor-type-specific regression — requires specifying cancer type
timer <- deconvolute(tpm_tumor, method = "timer",
  indications = rep("brca", ncol(tpm_tumor)))
# Valid indications: lowercase TCGA codes (brca, luad, coad, gbm, skcm, etc.)

# Returns 6 types: B cell, CD4+ T cell, CD8+ T cell,
#   Neutrophil, Macrophage, Dendritic cell

# If your cancer type is not in TIMER's pre-built models, use another method.
# TIMER needs at least 2 samples — single-sample deconvolution will fail.
```

## ESTIMATE

```r
# ESTIMATE: stromal score, immune score, tumor purity
# Oldest method (2013) but still the standard for purity estimation

est <- deconvolute_estimate(tpm_tumor)
# Returns: StromalScore, ImmuneScore, ESTIMATEScore, TumorPurity

# TumorPurity is derived from: cos(0.6049872018 + 0.0001467884 * ESTIMATEScore)
# This conversion was calibrated on Agilent microarrays.
# For RNA-seq, treat purity as approximate — the rank ordering is reliable,
# the absolute values less so.
```

## Tumor Purity Correction

```
Why purity matters:
  Low purity sample = fewer tumor cells = immune cells are a larger fraction
  High purity sample = more tumor cells = immune signal is compressed

  If group A has lower purity than group B on average, deconvolution
  will show group A as "more immune" even if the actual immune
  infiltration per unit tissue is identical.

When to correct:
  Comparing immune infiltration between groups
    -> Include ESTIMATE purity as covariate in linear model
  Correlating deconvolution scores with mutations or expression
    -> Partial correlation controlling for purity
  Filtering bad samples
    -> Remove samples with ESTIMATE purity < 0.2 (likely failed or lymphomas)

When NOT to correct:
  Reporting absolute immune fractions from quanTIseq/EPIC
    -> These already account for non-immune content via "Other"/"otherCells"
  Comparing within the same tumor type with similar purity distributions
    -> Correction adds noise without removing bias
```

```r
# Purity as covariate
est_scores <- deconvolute_estimate(tpm_tumor)
purity <- as.numeric(est_scores["TumorPurity", ])
sample_info$purity <- purity

# Linear model with purity adjustment
cd8_scores <- as.numeric(mcp[mcp$cell_type == "T cell CD8+", -1])
fit <- lm(cd8_scores ~ subtype + purity, data = sample_info)
summary(fit)
# Subtype coefficients are now purity-adjusted

# Partial correlation
library(ppcor)
pcor_result <- pcor.test(
  x = cd8_scores,
  y = sample_info$mutation_load,
  z = purity,
  method = "spearman"
)
```

## Cross-Method Comparison

```r
# Run multiple methods and compare CD8+ T cell estimates
methods_to_run <- c("quantiseq", "epic", "mcp_counter", "xcell")
all_res <- lapply(methods_to_run, function(m) {
  deconvolute(tpm_tumor, method = m)
})
names(all_res) <- methods_to_run

# Extract CD8 scores — each method uses slightly different cell type names
cd8_names <- c(
  quantiseq  = "T cell CD8+",
  epic       = "T cell CD8+",
  mcp_counter = "T cell CD8+",
  xcell      = "T cell CD8+"
)

cd8_mat <- sapply(methods_to_run, function(m) {
  res <- all_res[[m]]
  as.numeric(res[res$cell_type == cd8_names[m], -1])
})
rownames(cd8_mat) <- colnames(tpm_tumor)

# Cross-method Spearman correlation
cor(cd8_mat, method = "spearman", use = "pairwise.complete.obs")
# Expect rho > 0.5 between most pairs for CD8+ T cells
# rho < 0.3 for most pairs: check input format (log-transformed? wrong gene IDs?)
```

## Visualization

```r
library(ggplot2)

# --- Stacked bar plot (quanTIseq fractions) ---
qt_long <- tidyr::pivot_longer(qt, -cell_type,
  names_to = "sample", values_to = "fraction")

ggplot(qt_long, aes(x = sample, y = fraction, fill = cell_type)) +
  geom_bar(stat = "identity", position = "stack") +
  theme_classic(base_size = 12) +
  theme(axis.text.x = element_blank(), axis.ticks.x = element_blank()) +
  labs(y = "Cell fraction", x = "Samples", fill = "Cell type")

# --- Boxplot by molecular subtype ---
score_df <- data.frame(
  sample = colnames(tpm_tumor),
  CD8 = as.numeric(mcp[mcp$cell_type == "T cell CD8+", -1]),
  subtype = sample_info$subtype
)

ggplot(score_df, aes(x = reorder(subtype, CD8, FUN = median), y = CD8, fill = subtype)) +
  geom_boxplot(outlier.size = 0.5) +
  geom_jitter(width = 0.15, alpha = 0.3, size = 0.5) +
  theme_classic(base_size = 12) +
  labs(y = "MCP-counter CD8+ T cell score", x = NULL) +
  theme(legend.position = "none")

# --- Cross-method correlation heatmap ---
library(ComplexHeatmap); library(circlize)
cor_mat <- cor(cd8_mat, method = "spearman", use = "pairwise.complete.obs")
col_fun <- colorRamp2(c(0, 0.5, 1), c("#2166AC", "white", "#B2182B"))

Heatmap(cor_mat, name = "Spearman\nrho", col = col_fun,
  cell_fun = function(j, i, x, y, w, h, fill) {
    grid.text(sprintf("%.2f", cor_mat[i, j]), x, y, gp = gpar(fontsize = 10))
  },
  column_title = "Cross-method concordance: CD8+ T cells")

# --- ESTIMATE purity vs immune score scatter ---
est_df <- data.frame(
  purity = as.numeric(est_scores["TumorPurity", ]),
  immune = as.numeric(est_scores["ImmuneScore", ]),
  subtype = sample_info$subtype
)
ggplot(est_df, aes(purity, immune, color = subtype)) +
  geom_point(alpha = 0.5, size = 1.5) +
  theme_classic(base_size = 12) +
  labs(x = "ESTIMATE tumor purity", y = "ESTIMATE immune score")
```

## Output Specification

| Output | Format | Description |
|--------|--------|-------------|
| `quantiseq_fractions.csv` | CSV | Absolute cell fractions per sample (sum to 1) |
| `epic_fractions.csv` | CSV | Absolute fractions including cancer cell estimate |
| `cibersort_fractions.csv` | CSV | 22-type relative or absolute fractions |
| `xcell_scores.csv` | CSV | 64 cell type enrichment scores |
| `mcp_scores.csv` | CSV | 10 population scores (arbitrary units) |
| `estimate_scores.csv` | CSV | Immune score, stromal score, purity per sample |
| `method_correlation.csv` | CSV | Cross-method Spearman rho per cell type |
| `immune_boxplot.pdf` | PDF | Cell scores by molecular subtype |
| `stacked_barplot.pdf` | PDF | Per-sample immune composition |

## Validation Checks

```
After running deconvolution on TCGA-BRCA, verify:

Subtype ordering (consistent across methods):
  Basal-like should have highest CD8+ T cell scores
  Luminal A should have lowest overall immune infiltration
  HER2-enriched sits between Basal and Luminal B
  If Luminal A ranks highest for immune infiltration, something is wrong.

quanTIseq sanity:
  "uncharacterized cell" in solid tumors should be 0.5-0.9
  Sum of all fractions = 1.0 per sample (within floating point tolerance)
  Macrophage M2 typically > M1 in most solid tumors
  If all CD8 fractions are 0: gene symbols may not match quanTIseq signature

ESTIMATE sanity:
  TCGA-BRCA median purity: ~0.75
  Basal: lower purity (0.55-0.70), Luminal A: higher purity (0.80-0.90)
  If all purities cluster near 1.0 or near 0: wrong platform setting or wrong input scale

Cross-method concordance:
  CD8+ T cell Spearman rho > 0.5 between quanTIseq, EPIC, MCP-counter
  rho < 0.3 across most pairs: input is likely log-transformed or has wrong gene IDs

Red flags:
  CIBERSORT p > 0.05 for > 30% of samples: signature doesn't fit this cohort
  xCell returns all zeros for many cell types: gene overlap too low
  TIMER returns NA: cancer type not in the pre-built model set
  quanTIseq crashes: duplicate gene symbols in rownames (must deduplicate)
  Only 1 sample: TIMER and ConsensusTME need >= 2 samples per cancer type
```

## Common Pitfalls

### Input
1. **Raw counts instead of TPM**: quanTIseq, EPIC, xCell, MCP-counter, and CIBERSORT expect TPM. Feeding raw counts compresses low-expression signatures and inflates high-expression ones. Convert first: `tpm <- counts / gene_lengths * 1e6 / colSums(counts / gene_lengths)`.
2. **Log-transformed input**: Most methods expect linear-scale TPM. Passing log2(TPM+1) flattens the dynamic range and produces wrong fractions. The immunedeconv docs say explicitly: "data must be on non-log scale."
3. **Ensembl IDs as rownames**: Every signature matrix uses HGNC gene symbols. Ensembl IDs will match nothing, and most methods fail silently with near-zero results rather than throwing an error.
4. **Duplicate gene symbols**: quanTIseq crashes on duplicate rownames. Deduplicate before calling any method — keep the row with highest mean expression.

### Interpretation
5. **Treating scores as fractions**: xCell and MCP-counter output enrichment scores, not proportions. Saying "20% CD8 T cells" from an MCP-counter score of 3.7 is meaningless. Only quanTIseq, EPIC, and CIBERSORT return interpretable fractions.
6. **Comparing values across methods**: A CD8 estimate of 0.12 from quanTIseq and 4.8 from MCP-counter are on completely different scales. Compare ranks or standardized scores, never raw values.
7. **Ignoring tumor purity**: A low-purity sample will show high immune fractions simply because the denominator (total cells) contains fewer tumor cells. Control for purity when comparing groups with different purity distributions.
8. **Treating deconvolution as ground truth**: These are estimates. Cross-method concordance increases confidence; single-method results are hypotheses. For publication, validate key findings with IHC, flow cytometry, or spatial transcriptomics.

### Method-specific
9. **CIBERSORT without checking fit p-values**: Samples with p > 0.05 have unreliable estimates. Excluding these is standard practice but often forgotten.
10. **TIMER on unsupported cancer types**: TIMER's regression models are pre-built for specific TCGA indications. Running it on a cancer type not in the training set gives uninterpretable results.
11. **Single-sample runs with TIMER or ConsensusTME**: These methods need at least 2 samples of the same cancer type. A single sample will either error or return NAs.
12. **Mixing microarray and RNA-seq without batch correction**: Deconvolution signatures are sensitive to platform effects. Don't pool microarray and RNA-seq samples without explicit normalization.

## Advanced: Single-Cell Reference-Based Deconvolution

When matched scRNA-seq data is available for the same tissue type, second-generation methods outperform signature-based approaches.

```r
# BayesPrism: top performer in 2024-2025 benchmarks
# install.packages("BayesPrism")  # or InstaPrism for faster runtime
library(BayesPrism)

# Requires: scRNA-seq reference (genes x cells) + cell type labels
# bulk: genes x samples matrix (counts, not TPM)
bp <- new.prism(
  reference = sc_counts,        # raw counts from scRNA-seq reference
  mixture = bulk_counts,         # raw counts from bulk samples
  input.type = "count.matrix",
  cell.type.labels = cell_labels,
  cell.state.labels = cell_states  # finer subtypes, optional
)
result <- run.prism(bp, n.cores = 4)
theta <- get.fraction(result, which = "final")  # samples x cell_types
# BayesPrism returns posterior mean fractions that sum to 1
```

```
When to use scRNA-seq-based methods vs signature-based:
  Have matched scRNA-seq reference for the same tissue type?
    -> BayesPrism or DWLS. Better accuracy than fixed signatures.
  No scRNA-seq reference, just bulk RNA-seq?
    -> quanTIseq + EPIC + MCP-counter (signature-based).
  Public scRNA-seq atlas exists for the tissue?
    -> Consider BayesPrism with the atlas as reference, but be aware
       of batch effects between your bulk data and the atlas.
```

## Related Skills

- [`cancer-multiomics`](../cancer-multiomics/SKILL.md): TCGA data retrieval and expression matrix preparation (input for deconvolution)
- [`survival-analysis`](../survival-analysis/SKILL.md): Use deconvolution scores as covariates in Cox models or KM stratification

## Public Datasets for Testing

| Dataset | Samples | Use Case |
|---------|---------|----------|
| TCGA-BRCA | 1098 | Breast cancer, strong immune subtype differences (Basal vs Luminal) |
| TCGA-SKCM | 472 | Melanoma, high immune infiltration, immunotherapy response data |
| TCGA-LUAD | 585 | Lung adenocarcinoma, mixed immune landscape |
| TCGA-COAD | 521 | Colorectal, MSI-H tumors are immune-hot vs MSS cold |
