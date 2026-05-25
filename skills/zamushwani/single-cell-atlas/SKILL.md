# Single-Cell Atlas Construction

Full single-cell RNA-seq pipeline from raw counts to biological interpretation. Covers QC, normalization, batch integration, clustering, annotation, pseudobulk DE, trajectory inference, cell-cell communication, and TF activity. Dual-language: Seurat v5 (R) and scanpy (Python).

## When to Use This Skill

Activate when the user requests:
- Single-cell RNA-seq quality control and preprocessing
- 10x Chromium data processing (Cell Ranger output)
- Doublet detection and removal
- Normalization of UMI count matrices
- Feature selection for dimensionality reduction
- Processing scRNA-seq data before integration, clustering, or annotation
- Batch integration across samples or experiments
- Clustering and resolution selection
- Automated or marker-based cell type annotation
- UMAP visualization
- Differential expression between conditions (pseudobulk)
- Trajectory inference and RNA velocity
- Cell-cell communication analysis
- Transcription factor activity and gene regulatory networks

## Inputs

| Data Type | Format | Source |
|-----------|--------|--------|
| Count matrix | 10x HDF5 (`.h5`), MEX (matrix.mtx + barcodes + features) | Cell Ranger, STARsolo |
| Count matrix | AnnData (`.h5ad`) for scanpy, Seurat object (`.rds`) for R | Processed datasets |
| Reference | PBMC 3k, Tabula Muris, HCA datasets | 10x Genomics, HCA |

---

## Loading Data

### Seurat v5 (R)

```r
library(Seurat)  # v5.4+

# From Cell Ranger output (filtered_feature_bc_matrix/)
obj <- Read10X("path/to/filtered_feature_bc_matrix/") |>
  CreateSeuratObject(project = "sample1", min.cells = 3, min.features = 200)

# From HDF5
obj <- Read10X_h5("path/to/filtered_feature_bc_matrix.h5") |>
  CreateSeuratObject(project = "sample1", min.cells = 3, min.features = 200)

# Seurat v5 uses Assay5 (layers: counts, data, scale.data)
# Access counts: obj[["RNA"]]$counts or LayerData(obj, layer = "counts")
```

### scanpy (Python)

```python
import scanpy as sc  # v1.12+

# From Cell Ranger output
adata = sc.read_10x_mtx("path/to/filtered_feature_bc_matrix/", var_names="gene_symbols")

# From HDF5
adata = sc.read_10x_h5("path/to/filtered_feature_bc_matrix.h5")

# Store raw counts for later
adata.raw = adata.copy()
```

---

## Quality Control

### Computing QC Metrics

#### Seurat

```r
obj[["percent.mt"]] <- PercentageFeatureSet(obj, pattern = "^MT-")
# Mouse: pattern = "^mt-"
# Ribosomal: pattern = "^RP[SL]" (optional, rarely used for filtering)

# QC stats are in obj@meta.data:
#   nCount_RNA = total UMI per cell
#   nFeature_RNA = genes detected per cell
#   percent.mt = mitochondrial fraction
```

#### scanpy

```python
adata.var["mt"] = adata.var_names.str.startswith("MT-")
sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], percent_top=None, log1p=True, inplace=True)

# Adds to adata.obs:
#   total_counts, n_genes_by_counts, pct_counts_mt
#   log1p_total_counts, log1p_n_genes_by_counts
```

### MAD-Based Filtering

```
Why MAD over fixed thresholds:
  Fixed thresholds (>200 genes, <5% MT) are arbitrary and dataset-specific.
  A threshold that works for PBMCs fails for tumor tissues (higher MT baseline)
  or deep-sequenced datasets (more genes detected per cell).

  MAD (median absolute deviation) adapts to the actual data distribution.
  Flag cells that deviate > N MADs from the median in the problematic direction.
  Default: 3 MADs (~99% of values under normality).
  Permissive: 5 MADs (for heterogeneous tissues).
```

#### Seurat (manual MAD implementation)

```r
# Compute MAD thresholds per metric
mad_outlier <- function(x, nmads = 3, direction = "both") {
  med <- median(x, na.rm = TRUE)
  mad_val <- mad(x, na.rm = TRUE)
  if (direction == "lower") return(x < med - nmads * mad_val)
  if (direction == "higher") return(x > med + nmads * mad_val)
  (x < med - nmads * mad_val) | (x > med + nmads * mad_val)
}

obj$outlier_mt <- mad_outlier(obj$percent.mt, nmads = 3, direction = "higher")
obj$outlier_ncount <- mad_outlier(log1p(obj$nCount_RNA), nmads = 3, direction = "both")
obj$outlier_nfeat <- mad_outlier(log1p(obj$nFeature_RNA), nmads = 3, direction = "lower")

obj$discard <- obj$outlier_mt | obj$outlier_ncount | obj$outlier_nfeat

cat(sprintf("Cells flagged: %d / %d (%.1f%%)\n",
  sum(obj$discard), ncol(obj), 100 * mean(obj$discard)))

obj <- subset(obj, subset = discard == FALSE)
```

#### scanpy (MAD filtering)

```python
import numpy as np

def mad_outlier(adata, metric, nmads=3, direction="higher"):
    """Flag outliers beyond N MADs from median."""
    vals = adata.obs[metric].values
    med = np.median(vals)
    mad = np.median(np.abs(vals - med)) * 1.4826  # scale to match SD
    if direction == "higher":
        return vals > med + nmads * mad
    elif direction == "lower":
        return vals < med - nmads * mad
    else:
        return (vals < med - nmads * mad) | (vals > med + nmads * mad)

adata.obs["outlier_mt"] = mad_outlier(adata, "pct_counts_mt", nmads=3, direction="higher")
adata.obs["outlier_counts"] = mad_outlier(adata, "log1p_total_counts", nmads=3, direction="both")
adata.obs["outlier_genes"] = mad_outlier(adata, "log1p_n_genes_by_counts", nmads=3, direction="lower")

adata.obs["discard"] = adata.obs["outlier_mt"] | adata.obs["outlier_counts"] | adata.obs["outlier_genes"]

print(f"Cells flagged: {adata.obs['discard'].sum()} / {adata.n_obs} "
      f"({100 * adata.obs['discard'].mean():.1f}%)")

adata = adata[~adata.obs["discard"]].copy()
```

#### Bioconductor (scater — dedicated function)

```r
library(scater)  # Bioconductor
sce <- as.SingleCellExperiment(obj)
sce <- addPerCellQCMetrics(sce, subsets = list(mt = grep("^MT-", rownames(sce))))

# isOutlier handles log-transformation and batch-aware thresholds
discard <- isOutlier(sce$subsets_mt_percent, nmads = 3, type = "higher") |
  isOutlier(sce$detected, nmads = 3, type = "lower", log = TRUE) |
  isOutlier(sce$sum, nmads = 3, type = "both", log = TRUE)

sce <- sce[, !discard]
```

### Gene Filtering

```r
# Remove genes detected in very few cells
# min.cells = 3 in CreateSeuratObject handles this for Seurat

# For scanpy:
# sc.pp.filter_genes(adata, min_cells=3)

# Also consider removing:
#   Mitochondrial genes (after using them for QC)
#   Ribosomal genes (optional, sometimes informative)
#   Sex-linked genes (if confounding — XIST, DDX3Y, etc.)
```

---

## Doublet Detection

### scDblFinder (R — top performer in benchmarks)

```r
library(scDblFinder)  # Bioconductor

sce <- as.SingleCellExperiment(obj)
sce <- scDblFinder(sce)

# Results in colData(sce)$scDblFinder.class: "singlet" or "doublet"
# Also: scDblFinder.score (continuous), scDblFinder.cxds_score
table(sce$scDblFinder.class)

# Expected doublet rate for 10x Chromium: ~0.8% per 1000 cells captured
# 5000 cells -> ~4% doublets, 10000 cells -> ~8% doublets

# Transfer back to Seurat
obj$doublet_class <- sce$scDblFinder.class
obj$doublet_score <- sce$scDblFinder.score
obj <- subset(obj, subset = doublet_class == "singlet")
```

### Scrublet (Python — integrated in scanpy)

```python
# Scrublet is now in the core scanpy API (not external)
sc.pp.scrublet(adata, expected_doublet_rate=0.06)

# Adds to adata.obs:
#   predicted_doublet (bool), doublet_score (float)
print(f"Detected doublets: {adata.obs['predicted_doublet'].sum()}")

adata = adata[~adata.obs["predicted_doublet"]].copy()
```

```
Doublet detection order:
  Run BEFORE normalization and feature selection.
  Doublets with mixed transcriptomes distort HVG selection
  and normalization size factors.

  For multi-sample experiments:
    Run doublet detection PER SAMPLE, not on merged data.
    Cross-sample doublets don't exist in droplet-based protocols.
```

---

## Normalization

### Decision Tree

```
Which normalization method?

  Seurat v5 workflow, plan to integrate multiple samples?
    -> SCTransform(obj) — v2 is default in Seurat v5
    -> Replaces NormalizeData + FindVariableFeatures + ScaleData in one call
    -> Returns 3000 variable features by default
    -> Requires glmGamPoi package for speed

  Seurat v5, single sample or exploratory analysis?
    -> NormalizeData(obj) + FindVariableFeatures(obj) + ScaleData(obj)
    -> Log-normalization: counts / total * 10000 -> log1p
    -> Fast, simple, adequate for most single-sample analyses

  scanpy workflow?
    -> sc.pp.normalize_total(adata, target_sum=1e4) + sc.pp.log1p(adata)
    -> Standard log-normalization, analogous to Seurat's LogNormalize

  Need principled size factor estimation (composition bias)?
    -> scran::computeSumFactors() on a SingleCellExperiment
    -> Requires pre-clustering with scran::quickCluster()
    -> Slowest method but handles composition bias best

  Dealing with very large datasets (>500k cells)?
    -> SCTransform with BPCells on-disk storage (Seurat v5)
    -> Or scanpy with backed mode: sc.read_h5ad("data.h5ad", backed="r")
```

### SCTransform v2 (Seurat)

```r
# SCTransform v2 is the default in Seurat v5
# Uses glmGamPoi for fast regularized negative binomial regression
# install.packages("glmGamPoi")  # or BiocManager::install("glmGamPoi")

obj <- SCTransform(obj, verbose = FALSE)
# Replaces NormalizeData + FindVariableFeatures + ScaleData
# Sets default assay to "SCT"
# Variable features stored in VariableFeatures(obj)

# For multiple samples, run SCTransform on each before integration
# Then use IntegrateLayers() or SelectIntegrationFeatures()
```

### Log-Normalization (Seurat)

```r
obj <- NormalizeData(obj)  # LogNormalize, scale.factor = 10000
obj <- FindVariableFeatures(obj, selection.method = "vst", nfeatures = 2000)
obj <- ScaleData(obj)      # centers and scales, optionally regress out variables
# ScaleData(obj, vars.to.regress = "percent.mt")  # regress out MT% if needed
```

### scanpy Normalization

```python
# Store raw counts first
adata.layers["counts"] = adata.X.copy()

sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
# adata.X now contains log-normalized data
# adata.layers["counts"] retains raw counts for DE analysis later
```

### scran Deconvolution (Bioconductor)

```r
library(scran)
sce <- as.SingleCellExperiment(obj)

# Pre-cluster to avoid violating the non-DE majority assumption
clusters <- quickCluster(sce)
sce <- computeSumFactors(sce, clusters = clusters)
# Size factors in sizeFactors(sce), centered around 1

sce <- logNormCounts(sce)
# logcounts(sce) now contains normalized, log-transformed values
```

---

## Feature Selection

### Seurat (VST)

```r
# After NormalizeData:
obj <- FindVariableFeatures(obj, selection.method = "vst", nfeatures = 2000)
# After SCTransform: already done (default 3000 features)

# Inspect top variable genes
head(VariableFeatures(obj), 20)

# Visualize variance-mean relationship
VariableFeaturePlot(obj)
```

### scanpy

```python
# Flavor depends on input: seurat_v3 needs raw counts, seurat needs log-normalized
sc.pp.highly_variable_genes(adata, flavor="seurat_v3", n_top_genes=2000)
# Adds adata.var["highly_variable"], adata.var["means"], adata.var["variances"]

# Subset to HVGs for PCA (keep all genes in adata.raw)
adata = adata[:, adata.var["highly_variable"]].copy()
```

### Deviance-Based (scry — more principled alternative)

```r
library(scry)  # Bioconductor
sce <- as.SingleCellExperiment(obj)

# Compute binomial deviance per gene on raw counts
sce <- devianceFeatureSelection(sce, assay = "counts", sorted = TRUE)
# Top genes by deviance are most informative
# Select top 2000-4000 genes
hvgs <- head(rownames(sce), 2000)

# Pairs with GLM-PCA instead of standard PCA
# glmpca <- GLMPCA(counts(sce[hvgs, ]), L = 30, fam = "poi")
```

```
Feature selection guidelines:
  2000-3000 HVGs works for most datasets.
  More HVGs (4000-5000) can help for heterogeneous tissues or rare cell types.
  No single method consistently outperforms others (2025 Nature Methods benchmark).
  Deviance-based selection (scry) is more principled than variance-based
  but less widely adopted.
```

---

---

## Dimensionality Reduction

### PCA

#### Seurat

```r
obj <- RunPCA(obj, npcs = 50, verbose = FALSE)
# Determine how many PCs to use downstream
ElbowPlot(obj, ndims = 50)
# Pick the elbow — typically 15-30 PCs for most datasets
# Alternatively: use JackStraw (slow) or molecular cross-validation
```

#### scanpy

```python
sc.tl.pca(adata, n_comps=50, svd_solver="arpack")
sc.pl.pca_variance_ratio(adata, n_pcs=50, log=True)
# Pick PCs where variance ratio flattens — typically 15-30
```

### UMAP

```
UMAP is for visualization only. Never cluster on UMAP coordinates.
Distances between clusters in UMAP do NOT reflect biological similarity.
Cluster size does not reflect heterogeneity.

Parameters that matter:
  n_neighbors: 10-30 (default 15). Lower = more local detail, higher = broader topology.
  min_dist: 0.1-0.5 (default 0.1). Lower = tighter clusters, higher = more spread.
  For cell type identification: min_dist = 0.1-0.3
  For trajectory visualization: min_dist = 0.3-0.5
```

#### Seurat

```r
obj <- FindNeighbors(obj, dims = 1:30)
obj <- RunUMAP(obj, dims = 1:30, min.dist = 0.3, n.neighbors = 30)
DimPlot(obj, reduction = "umap", group.by = "cell_type")
```

#### scanpy

```python
sc.pp.neighbors(adata, n_neighbors=15, n_pcs=30)
sc.tl.umap(adata, min_dist=0.3)
sc.pl.umap(adata, color=["cell_type", "batch"])
```

---

## Batch Integration

### Method Selection

```
Which integration method?

  Few batches (2-5), similar cell compositions?
    -> Harmony: fast, works in PCA space, no GPU needed.
    -> RPCA (Seurat): conservative, preserves biology well.

  Many batches (>5), different cell compositions across batches?
    -> scVI: deep generative model, handles complex batch effects.
    -> CCA (Seurat): finds shared correlation structure across batches.

  Have partial cell type labels?
    -> scANVI: semi-supervised, uses labels for better integration.
    -> Best overall performer when labels are available (scIB benchmark).

  Very large dataset (>500k cells)?
    -> Harmony: scales linearly, runs in seconds on PCA.
    -> Seurat v5 sketch-based: subsamples, integrates sketch, projects back.

  Simple/fast first pass?
    -> Harmony. Works well for most cases and takes < 1 minute.

  Evaluate integration quality?
    -> scib-metrics: batch ASW, graph iLISI (mixing), cell type ASW, NMI (conservation).
    -> Scoring: 40% batch removal + 60% biological conservation.
```

### Harmony (R)

```r
library(harmony)  # v1.2+

# Run on PCA embeddings — fast, no GPU needed
obj <- RunHarmony(obj, group.by.vars = "batch", dims.use = 1:30)
# theta = 2 (default): diversity penalty. Increase to 3-4 for stubborn batch effects.
# lambda = 1 (default): ridge regression penalty. Decrease for stronger correction.

# Use harmony reduction for downstream steps
obj <- FindNeighbors(obj, reduction = "harmony", dims = 1:30)
obj <- RunUMAP(obj, reduction = "harmony", dims = 1:30)
obj <- FindClusters(obj, resolution = 0.5)
```

### Harmony (scanpy)

```python
import scanpy.external as sce

sce.pp.harmony_integrate(adata, key="batch", basis="X_pca", adjusted_basis="X_pca_harmony")
# Use the corrected embedding for neighbors/UMAP
sc.pp.neighbors(adata, use_rep="X_pca_harmony", n_pcs=30)
sc.tl.umap(adata)
```

### Seurat v5 IntegrateLayers

```r
# Split layers by batch (if not already split after merge)
obj[["RNA"]] <- split(obj[["RNA"]], f = obj$batch)

# Standard workflow: normalize, HVGs, scale, PCA, then integrate
obj <- NormalizeData(obj)
obj <- FindVariableFeatures(obj)
obj <- ScaleData(obj)
obj <- RunPCA(obj)

# Integration — pick one method:
obj <- IntegrateLayers(obj, method = HarmonyIntegration,
  orig.reduction = "pca", new.reduction = "harmony")

# Or CCA/RPCA:
# obj <- IntegrateLayers(obj, method = CCAIntegration,
#   orig.reduction = "pca", new.reduction = "integrated.cca")

# Rejoin layers before DE analysis
obj <- JoinLayers(obj)
```

### scVI (Python)

```python
import scvi  # v1.4+

# Setup — requires raw counts in a specific layer
scvi.model.SCVI.setup_anndata(adata, batch_key="batch", layer="counts")

model = scvi.model.SCVI(adata, n_latent=30, n_layers=2, gene_likelihood="nb")
model.train(max_epochs=400, accelerator="auto")
# GPU speeds training ~10x but CPU works for < 100k cells

# Get latent representation
adata.obsm["X_scVI"] = model.get_latent_representation()

# Use for neighbors/UMAP
sc.pp.neighbors(adata, use_rep="X_scVI")
sc.tl.umap(adata)
```

### scANVI (semi-supervised, when partial labels available)

```python
# Start from a trained scVI model
scvi.model.SCANVI.setup_anndata(adata, batch_key="batch",
  labels_key="cell_type", unlabeled_category="Unknown")

scanvi_model = scvi.model.SCANVI.from_scvi_model(model,
  labels_key="cell_type", unlabeled_category="Unknown")
scanvi_model.train(max_epochs=20)

adata.obsm["X_scANVI"] = scanvi_model.get_latent_representation()
adata.obs["predicted_label"] = scanvi_model.predict()
```

---

## Clustering

### Leiden (preferred over Louvain)

```
Why Leiden over Louvain:
  Louvain can produce badly connected communities (internal disconnections).
  Leiden guarantees well-connected communities.
  Louvain is no longer maintained. Leiden is the default in Seurat and scanpy.
```

#### Seurat

```r
obj <- FindNeighbors(obj, reduction = "harmony", dims = 1:30)
obj <- FindClusters(obj, algorithm = 4, resolution = 0.5)
# algorithm = 4 is Leiden. algorithm = 1 is Louvain (legacy).
# resolution: 0.3-0.5 = coarse, 0.8-1.0 = fine, 1.2+ = very fine
```

#### scanpy

```python
sc.tl.leiden(adata, resolution=0.5)
# Requires leidenalg package
# sc.tl.louvain() is deprecated as of scanpy 1.12
```

### Resolution Selection

```
Picking resolution is one of the hardest choices in scRNA-seq analysis.
Too low: biologically distinct cell types merged.
Too high: single cell types split into meaningless subclusters.

Approaches:
  1. Clustree (R): visualize cluster stability across resolutions 0.1-1.5
     library(clustree)
     clustree(obj, prefix = "RNA_snn_res.")
     Pick the resolution where clusters stabilize (no excessive splitting).

  2. Known biology: if you expect ~9 cell types (PBMCs), resolution 0.4-0.6
     gives ~8-12 clusters. If you expect ~20 (complex tissue), go higher.

  3. Marker gene validation: run FindAllMarkers at each resolution.
     Clusters that lack distinct markers at high resolution were over-split.

  4. Silhouette scores: compute per-cluster silhouette on PCA embedding.
     Low silhouette = poorly separated cluster = likely over-split.
```

```r
# Clustree: test multiple resolutions
library(clustree)
obj <- FindClusters(obj, algorithm = 4, resolution = seq(0.1, 1.5, 0.1))
clustree(obj, prefix = "RNA_snn_res.")
# Pick the highest resolution with stable cluster assignments
```

---

## Cell Type Annotation

### Decision Tree

```
Which annotation method?

  Have a reference atlas for the same tissue?
    -> CellTypist (Python): pre-trained models for immune, lung, gut, brain, etc.
    -> scANVI: transfer labels from reference during integration.

  Working in Seurat (R) with known tissue type?
    -> scType: marker-gene database, scores clusters directly.
    -> Fast, customizable, works on Seurat scale.data.

  No reference, no database matches your tissue?
    -> Manual annotation with FindAllMarkers + known canonical markers.
    -> Still the gold standard for novel tissues or rare cell types.

  Want a quick first pass?
    -> CellTypist with majority_voting=True. Then validate with markers.
```

### CellTypist (Python)

```python
import celltypist
from celltypist import models

# Download models (run once)
models.download_models(force_update=True)

# Input must be log-normalized to 10,000 counts per cell
# If adata.X is already log-normalized, proceed directly
predictions = celltypist.annotate(
  adata,
  model="Immune_All_Low.pkl",   # 90 immune subtypes across 20 tissues
  majority_voting=True           # refines via local subcluster consensus
)

adata = predictions.to_adata()
# Adds: adata.obs["predicted_labels"], adata.obs["over_clustering"],
#   adata.obs["majority_voting"], adata.obs["conf_score"]
```

### scType (R)

```r
# Source scType functions from GitHub
source("https://raw.githubusercontent.com/IanevskiAleksandr/sc-type/master/R/gene_sets_prepare.R")
source("https://raw.githubusercontent.com/IanevskiAleksandr/sc-type/master/R/sctype_score_.R")

# Prepare marker gene database
db <- "https://raw.githubusercontent.com/IanevskiAleksandr/sc-type/master/ScTypeDB_full.xlsx"
gs_list <- gene_sets_prepare(db, "Immune system")

# Score each cell against all cell types
es <- sctype_score(
  scRNAseqData = obj[["RNA"]]$scale.data,  # Seurat v5 layer access
  gs = gs_list$gs_positive,
  gs2 = gs_list$gs_negative
)

# Assign cell types to clusters
cl_results <- do.call("rbind", lapply(unique(obj$seurat_clusters), function(cl) {
  es_cl <- sort(rowSums(es[, rownames(obj@meta.data[obj$seurat_clusters == cl, ])]),
    decreasing = TRUE)
  data.frame(cluster = cl, type = names(es_cl[1]), score = es_cl[1])
}))

obj$sctype_annotation <- cl_results$type[match(obj$seurat_clusters, cl_results$cluster)]
```

### Manual Annotation with Markers

```r
# Find markers for each cluster
markers <- FindAllMarkers(obj, only.pos = TRUE, min.pct = 0.25, logfc.threshold = 0.5)

# Top 5 markers per cluster
top5 <- markers |> group_by(cluster) |> top_n(5, wt = avg_log2FC)

# Known PBMC markers for reference:
#   CD4+ T: IL7R, CCR7 (naive), S100A4 (memory)
#   CD8+ T: CD8A, CD8B
#   B cells: MS4A1 (CD20), CD79A
#   NK: GNLY, NKG7, KLRD1
#   CD14 Mono: CD14, LYZ
#   FCGR3A Mono: FCGR3A, MS4A7
#   DC: FCER1A, CST3
#   Platelets: PPBP

# Dot plot of markers across clusters
DotPlot(obj, features = c("IL7R", "CD8A", "MS4A1", "GNLY", "CD14",
  "FCGR3A", "FCER1A", "PPBP"), group.by = "seurat_clusters") +
  RotatedAxis()
```

---

## Differential Expression (Pseudobulk)

```
Why pseudobulk and not Wilcoxon/t-test on single cells:
  Cells from the same donor are not independent.
  Cell-level tests treat 5000 cells from 3 donors as n=5000, not n=3.
  This inflates significance: thousands of false positives.
  Squair et al. 2021, Zimmerman et al. 2021 both showed pseudobulk methods
  outperform cell-level tests for cross-condition comparisons.

  When cell-level tests are OK:
    Marker gene discovery within a single sample (no cross-sample comparison).
    FindAllMarkers for cluster markers is fine — it's within-sample.

  When pseudobulk is required:
    Any comparison across conditions, treatments, or donors.
```

### Pseudobulk with DESeq2 (R)

```r
library(DESeq2)

# Aggregate raw counts: sum per gene, grouped by sample + cell_type
# Seurat v5: JoinLayers first, then extract counts
obj <- JoinLayers(obj)
counts <- obj[["RNA"]]$counts

pb <- aggregate(t(as.matrix(counts)),
  by = list(sample = obj$sample_id, cell_type = obj$cell_type),
  FUN = sum)
# Reshape to genes x pseudobulk_samples matrix
# Or use scuttle::aggregateAcrossCells (cleaner)

# With scuttle (recommended)
library(scuttle)
sce <- as.SingleCellExperiment(obj)
pb_sce <- aggregateAcrossCells(sce,
  ids = DataFrame(sample = sce$sample_id, cell_type = sce$cell_type))

# Run DESeq2 on one cell type
ct <- "CD8+ T"
pb_ct <- pb_sce[, pb_sce$cell_type == ct]

dds <- DESeqDataSetFromMatrix(
  countData = counts(pb_ct),
  colData = colData(pb_ct),
  design = ~ condition  # e.g., treatment vs control
)
dds <- DESeq(dds)
res <- results(dds, alpha = 0.05)
```

### Pseudobulk with decoupleR (Python)

```python
import decoupler as dc

# Aggregate counts by sample + cell_type
pdata = dc.get_pseudobulk(
    adata, sample_col="sample_id", groups_col="cell_type",
    layer="counts", min_cells=10, min_counts=1000
)

# Run DESeq2 via decoupler's wrapper
dc.deseq2(pdata, design="~condition")
# Results in pdata.uns with log2FC, padj per gene per cell type
```

---

## Trajectory Inference

### Method Selection

```
Which trajectory method?

  Want cluster-level connectivity (which cell types connect)?
    -> PAGA (scanpy, fast, no assumptions about topology)
    -> Run first to understand the coarse structure.

  Want continuous pseudotime along a lineage?
    -> Diffusion pseudotime (scanpy sc.tl.dpt) — needs a root cell
    -> Monocle3 order_cells() — learns a graph, picks root interactively

  Want RNA velocity (transcriptional dynamics)?
    -> scVelo dynamical mode — requires spliced/unspliced counts from velocyto/STARsolo
    -> Caveat: assumes active transcription. Fails for stable/mature populations.
    -> Validate with CellRank 2 for fate probabilities.

  Branching trajectories?
    -> Monocle3: learns principal graph with automatic branch point detection.
    -> PAGA + DPT: use PAGA for topology, DPT for pseudotime per branch.
```

### PAGA + Diffusion Pseudotime (scanpy)

```python
# PAGA: cluster-level trajectory graph
sc.tl.paga(adata, groups="leiden")
sc.pl.paga(adata, threshold=0.03, show=True)
# Edges = statistically supported connections between clusters
# threshold: remove weak edges (default 0.03)

# Initialize UMAP with PAGA for better trajectory layout
sc.tl.umap(adata, init_pos="paga")

# Diffusion pseudotime (requires a root cell)
adata.uns["iroot"] = int(np.where(adata.obs["cell_type"] == "HSC")[0][0])
sc.tl.diffmap(adata)
sc.tl.dpt(adata)
sc.pl.umap(adata, color=["dpt_pseudotime", "cell_type"])
```

### Monocle3 (R)

```r
library(monocle3)

# Convert from Seurat
cds <- as.cell_data_set(obj)  # requires SeuratWrappers
cds <- preprocess_cds(cds, num_dim = 30)
cds <- reduce_dimension(cds)
cds <- cluster_cells(cds)

# Learn trajectory graph
cds <- learn_graph(cds)

# Order cells (select root interactively or programmatically)
cds <- order_cells(cds, root_cells = root_cell_ids)
# root_cell_ids: barcodes of cells at the trajectory start (e.g., stem cells)

plot_cells(cds, color_cells_by = "pseudotime", cell_size = 0.5)

# Find genes that change along the trajectory
trajectory_genes <- graph_test(cds, neighbor_graph = "principal_graph")
sig_genes <- trajectory_genes[trajectory_genes$q_value < 0.05, ]
```

### RNA Velocity (scVelo)

```python
import scvelo as scv  # v0.3+

# Requires spliced/unspliced counts (from velocyto or STARsolo)
scv.pp.filter_and_normalize(adata, min_shared_counts=20, n_top_genes=2000)
scv.pp.moments(adata, n_pcs=30, n_neighbors=30)

# Dynamical mode — fits full kinetic ODE per gene
scv.tl.recover_dynamics(adata)
scv.tl.velocity(adata, mode="dynamical")
scv.tl.velocity_graph(adata)

scv.pl.velocity_embedding_stream(adata, basis="umap", color="cell_type")

# Velocity confidence: low confidence = unreliable direction
scv.tl.velocity_confidence(adata)
# adata.obs["velocity_confidence"] — filter genes/cells with low values
```

```
RNA velocity caveats:
  Requires active transcription dynamics (splicing timescale ~ hours).
  Fails for: PBMCs (mature, stable), slow diseases, steady-state populations.
  Contradictory results reported on some datasets (opposite directions).
  Always validate with known biology before interpreting velocity arrows.
  Consider CellRank 2 for fate analysis — it works with or without velocity.
```

---

## Cell-Cell Communication

### CellChat v2 (R)

```r
library(CellChat)  # v2.1+, from jinworks/CellChat

# Create CellChat object from Seurat
cellchat <- createCellChat(obj, group.by = "cell_type")

# Set ligand-receptor database
CellChatDB <- CellChatDB.human  # or CellChatDB.mouse
cellchat@DB <- CellChatDB

# Inference pipeline
cellchat <- subsetData(cellchat)
cellchat <- identifyOverExpressedGenes(cellchat)
cellchat <- identifyOverExpressedInteractions(cellchat)
cellchat <- computeCommunProb(cellchat)
cellchat <- computeCommunProbPathway(cellchat)
cellchat <- aggregateNet(cellchat)

# Visualization
netVisual_aggregate(cellchat, signaling = "CXCL")
netVisual_bubble(cellchat, sources.use = c("CD8+ T"), targets.use = c("Macrophage"))
netAnalysis_computeCentrality(cellchat, slot.name = "netP")
```

### LIANA+ (Python — consensus across methods)

```python
import liana as li

# LIANA wraps 7 methods and computes consensus rankings
li.mt.rank_aggregate(
    adata,
    groupby="cell_type",
    resource_name="consensus",  # OmniPath consensus resource
    verbose=True
)

# Results in adata.uns["liana_res"]
liana_res = adata.uns["liana_res"]
# Columns: source, target, ligand_complex, receptor_complex,
#   magnitude_rank, specificity_rank (consensus scores)

# Filter top interactions
top = liana_res[(liana_res["magnitude_rank"] < 0.01)]

# Visualization
li.pl.dotplot(adata, colour="magnitude_rank", size="specificity_rank",
  source_labels=["CD8+ T"], target_labels=["Macrophage"])
```

```
CellChat vs LIANA:
  CellChat: single method, rich curated database (1000+ interactions), R only,
    built-in spatial support (v2), best visualization.
  LIANA: consensus across 7 methods, flexible databases (OmniPath, CellPhoneDB, etc.),
    Python + R, higher confidence (cross-method agreement).
  For publication: run both and report concordant interactions.
```

---

## Transcription Factor Activity

```
For TF activity scoring, decoupleR + CollecTRI is now preferred over pySCENIC
for most use cases. It is faster, less prone to overfitting (uses pre-defined
regulons rather than inferring from the same data), and benchmarks favorably.

Use pySCENIC only when you need to discover novel TF-target relationships
specific to your dataset.
```

### decoupleR (Python — recommended for TF activity)

```python
import decoupler as dc

# Get CollecTRI regulons (curated TF-target interactions)
net = dc.get_collectri(organism="human", split_complexes=False)

# Score TF activities per cell
dc.run_ulm(adata, net=net, source="source", target="target", weight="weight")
# Results in adata.obsm["ulm_estimate"] (activity scores)
# and adata.obsm["ulm_pvals"]

# Visualize TF activities on UMAP
acts = dc.get_acts(adata, obsm_key="ulm_estimate")
sc.pl.umap(acts, color=["PAX5", "SPI1", "GATA1"], vcenter=0, cmap="RdBu_r")
# PAX5 high in B cells, SPI1 in myeloid, GATA1 in erythroid
```

### decoupleR (R)

```r
library(decoupleR)

net <- get_collectri(organism = "human", split_complexes = FALSE)
# Run ULM (univariate linear model) on the expression matrix
acts <- run_ulm(mat = obj[["RNA"]]$data, net = net, .source = "source",
  .target = "target", .mor = "mor", minsize = 5)
```

### pySCENIC (for novel GRN discovery)

```python
# Only use when discovering dataset-specific regulatory networks
# Requires: pyscenic, arboreto, ctxcore

from pyscenic.utils import modules_from_adjacencies
from pyscenic.prune import prune2df, df2regulons
from pyscenic.aucell import aucell
from arboreto.algo import grnboost2

# Step 1: infer co-expression modules (slow — hours for large datasets)
adjacencies = grnboost2(expression_data, tf_names=tf_list, seed=42)

# Step 2: prune with cis-regulatory motif analysis
modules = modules_from_adjacencies(adjacencies, expression_data)
# Requires ranking databases (hg38 feather files from cisTarget)
df = prune2df(dbs, modules, "motifs-v10-nr.hgnc-m0.001-o0.0.tbl")
regulons = df2regulons(df)

# Step 3: score regulon activity per cell
auc_mtx = aucell(expression_data, regulons)
```

## Output Specification

| Output | Format | Description |
|--------|--------|-------------|
| `qc_metrics.csv` | CSV | Per-cell QC: total counts, genes detected, MT%, outlier flags |
| `doublet_scores.csv` | CSV | Doublet probability per cell, singlet/doublet classification |
| `filtered_object.rds` | RDS | Seurat object after QC, doublet removal, normalization |
| `filtered_adata.h5ad` | H5AD | AnnData after QC, doublet removal, normalization |
| `hvg_list.csv` | CSV | Selected highly variable genes |
| `integrated_object.rds` | RDS | Seurat object after batch integration |
| `integrated_adata.h5ad` | H5AD | AnnData after integration with latent embedding |
| `cluster_markers.csv` | CSV | Top markers per cluster from FindAllMarkers |
| `cell_annotations.csv` | CSV | Per-cell type assignments (automated + manual) |
| `umap_plot.pdf` | PDF | UMAP colored by cluster, batch, cell type |
| `pseudobulk_de.csv` | CSV | DESeq2 results per cell type (log2FC, padj) |
| `trajectory_pseudotime.csv` | CSV | Per-cell pseudotime values |
| `velocity_embedding.pdf` | PDF | RNA velocity stream plot on UMAP |
| `cellchat_network.rds` | RDS | CellChat object with communication probabilities |
| `liana_results.csv` | CSV | Consensus L-R interaction rankings |
| `tf_activities.csv` | CSV | decoupleR TF activity scores per cell/cluster |
| `qc_violin.pdf` | PDF | Violin plots of nCount, nFeature, percent.mt |

## Validation Checks

```
After preprocessing PBMC 3k (10x reference dataset), verify:

Cell counts:
  Starting cells: ~2,700
  After QC (MAD 3): ~2,500-2,650 (lose ~2-7%)
  After doublet removal: ~2,400-2,600 (lose ~2-5%)

QC distributions:
  Median genes/cell: 800-1200
  Median UMI/cell: 2000-4000
  Median MT%: 2-5%
  Cells with > 10% MT: < 5% of total (PBMCs have low MT content)

Normalization:
  After log-normalization, expression values should be 0-8 range (log scale)
  SCTransform residuals centered near 0 with SD ~1

Feature selection:
  2000 HVGs should include known markers: IL7R, CD14, MS4A1, CD8A, GNLY, NKG7
  Housekeeping genes (ACTB, GAPDH) should NOT be in top HVGs

Doublet detection:
  Expected doublets for 3k cells: 20-60 (~1-2%)
  If > 10% flagged: check threshold or consider the data has quality issues

Integration (multi-sample):
  After Harmony/scVI, UMAP should show batches interleaved, not separated
  Cell types should remain distinct (batch correction ≠ biological erasure)
  If all cell types collapse into one blob: over-correction (reduce theta or lambda)

Clustering (PBMC 3k at resolution 0.5):
  Expect 8-12 clusters
  CD4 T, CD8 T, B cells, NK, CD14 Mono, FCGR3A Mono, DC, Platelets should separate
  If only 3-4 clusters: resolution too low
  If >20 clusters: resolution too high, check with clustree

Annotation:
  CellTypist with Immune_All_Low on PBMCs should identify all major types
  scType with "Immune system" database should score CD14 Mono, B cells, NK correctly
  Manual markers: IL7R for CD4 T, CD8A for CD8 T, MS4A1 for B, CD14 for Mono, GNLY for NK
```

## Common Pitfalls

### QC
1. **Fixed MT% threshold on all datasets**: A 5% cutoff works for PBMCs but removes real cardiomyocytes (30-40% MT) or hepatocytes (15-20% MT). Use MAD-based filtering or at least check the distribution before setting a threshold.
2. **Not filtering genes**: Removing cells but keeping genes detected in 0-2 cells. These contribute noise to normalization and feature selection. Filter with `min.cells = 3` or `sc.pp.filter_genes(adata, min_cells=3)`.
3. **QC on merged data without batch awareness**: MAD thresholds should ideally be computed per sample/batch. A sample with lower quality shifts the median and hides outliers in better samples. Use `scater::isOutlier(..., batch = sample_id)` or compute MAD per sample.

### Doublets
4. **Doublet detection on merged multi-sample data**: Droplet-based doublets only form within a sample. Running scDblFinder or Scrublet on merged data creates false doublets between cell types that were never in the same droplet.
5. **Trusting doublet scores blindly for rare populations**: Rare cell types with intermediate profiles can be flagged as doublets. Cross-check flagged cells against known markers before removal.

### Normalization
6. **Using TPM/FPKM normalization for scRNA-seq**: Single-cell UMI counts are not length-biased. Standard bulk normalization (TPM, FPKM) is wrong for UMI data. Use library-size normalization or SCTransform.
7. **Running SCTransform without glmGamPoi**: SCTransform v2 requires glmGamPoi for the fast GLM fitting. Without it, the function falls back to a much slower implementation. Install it from Bioconductor.
8. **ScaleData on all genes**: `ScaleData()` only needs to run on variable features for PCA. Scaling all genes wastes memory and time. `ScaleData(obj, features = VariableFeatures(obj))`.

### Feature Selection
9. **Running HVG selection on normalized data with seurat_v3 flavor**: The `seurat_v3` flavor in scanpy expects raw counts, not log-normalized data. Using the wrong flavor silently produces bad HVG rankings.

### Integration
10. **Integrating before QC and doublet removal**: Batch integration amplifies artifacts from low-quality cells and doublets. Always QC and remove doublets per sample first, then merge and integrate.
11. **Over-correction erasing biology**: If cell types that should be distinct merge after integration, the method is too aggressive. Reduce Harmony `theta`, increase scVI `n_latent`, or try a more conservative method (RPCA).
12. **Not joining layers before DE in Seurat v5**: After `IntegrateLayers()`, each sample's counts are still in separate layers. Call `JoinLayers()` before `FindAllMarkers()` or DE analysis will fail or use only one sample's data.

### Clustering and Annotation
13. **Clustering on UMAP coordinates**: UMAP distorts distances and densities. Always cluster on PCA or integrated embeddings (Harmony, scVI latent space), never on UMAP dimensions.
14. **Single resolution without validation**: Picking resolution = 0.5 without checking is arbitrary. Use clustree, silhouette scores, or marker gene validation to support the choice.
15. **Automated annotation without marker validation**: CellTypist and scType provide a starting point, not ground truth. Always check top markers per cluster against known biology for the tissue. Automated tools can mislabel rare or novel cell types.

### Differential Expression
16. **Wilcoxon/t-test for cross-condition DE**: Treating cells as independent replicates inflates significance massively. Use pseudobulk (aggregate by sample + cell type, then DESeq2). Cell-level tests are only appropriate for marker discovery within a single sample.
17. **Pseudobulk on normalized data**: Aggregate raw counts, not normalized values. DESeq2 needs integers and handles normalization internally.

### Trajectory and Communication
18. **RNA velocity on stable populations**: Velocity requires active transcription dynamics. PBMCs, terminally differentiated cells, and chronic disease states produce meaningless velocity arrows. Check velocity confidence scores and validate against known biology.
19. **Over-interpreting cell communication rankings**: Both CellChat and LIANA rank L-R pairs by statistical enrichment, not by biological activity. High-ranked interactions are hypotheses for validation, not confirmed communication events.
20. **pySCENIC for TF activity scoring**: pySCENIC infers GRNs from the same data it scores, creating overfitting risk. For TF activity scoring alone (not GRN discovery), decoupleR with CollecTRI regulons is faster and more reproducible.

## Related Skills

- `cancer-multiomics`: Bulk RNA-seq analysis, TCGA data retrieval
- `immune-deconvolution`: Bulk-level immune estimation (compare with single-cell ground truth)

## Public Datasets for Testing

| Dataset | Cells | Use Case |
|---------|-------|----------|
| PBMC 3k (10x) | 2,700 | Standard tutorial dataset, 9 cell types, fast processing |
| PBMC 10k (10x) | 10,000 | Larger PBMC, tests scalability |
| Tabula Muris | 100k+ | Multi-organ mouse atlas, tests batch integration |
| Human Cell Atlas (HCA) | varies | Reference atlases for annotation |
