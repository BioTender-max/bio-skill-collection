---
id: spatial-transcriptomics
name: Spatial Transcriptomics Visium Analysis
category: transcriptomics
short-description: "Analyze 10x Visium spatial transcriptomics data from QC through spatial domain analysis with clustering, spatially variable genes, and neighborhood enrichment."
detailed-description: "Complete spatial transcriptomics analysis for 10x Visium data using Squidpy and Scanpy. Performs quality control, normalization, Leiden clustering, spatial neighbor graph construction, spatially variable gene identification via Moran's I, neighborhood enrichment analysis, and co-occurrence scoring. Produces publication-ready spatial tissue overlays, UMAP plots, enrichment heatmaps, and SVG bar charts. Supports Space Ranger output, H5AD files, or built-in 10x Genomics example datasets including V1_Human_Heart for cardiometabolic research."
starting-prompt: Analyze spatial transcriptomics data from a 10x Visium experiment to identify spatially variable genes and tissue domains.
---

# Spatial Transcriptomics Visium Analysis

## When to Use This Skill

- You have **10x Visium** spatial gene expression data (with or without H&E image)
- You want to identify **spatially variable genes** across a tissue section
- You want to discover **spatial tissue domains** via clustering
- You want to quantify **neighborhood enrichment** between cell clusters
- You want to analyze **co-occurrence** patterns of cell types across distances
- Input is Space Ranger output, `.h5ad`, or `.h5` file

**Not for:** Single-molecule FISH (MERFISH/Xenium), Slide-seq, or single-cell RNA-seq without spatial coordinates. For scRNA-seq, use `scrnaseq-scanpy-core-analysis`.

## Installation

```bash
pip install squidpy scanpy anndata scikit-misc plotnine plotnine-prism seaborn matplotlib numpy pandas scikit-learn
```

| Package | Version | License | Commercial Use | Installation |
|---------|---------|---------|----------------|--------------|
| squidpy | ≥1.4 | BSD-3-Clause | ✅ Permitted | `pip install squidpy` |
| scanpy | ≥1.9 | BSD-3-Clause | ✅ Permitted | `pip install scanpy` |
| anndata | ≥0.8 | BSD-3-Clause | ✅ Permitted | `pip install anndata` |
| plotnine | ≥0.12 | MIT | ✅ Permitted | `pip install plotnine` |
| plotnine-prism | ≥0.2 | MIT | ✅ Permitted | `pip install plotnine-prism` |
| seaborn | ≥0.11 | BSD-3-Clause | ✅ Permitted | `pip install seaborn` |
| matplotlib | ≥3.5 | PSF | ✅ Permitted | `pip install matplotlib` |
| scikit-learn | ≥1.0 | BSD-3-Clause | ✅ Permitted | `pip install scikit-learn` |
| scikit-misc | ≥0.1 | BSD-3-Clause | ✅ Permitted | `pip install scikit-misc` |
| numpy | ≥1.21 | BSD-3-Clause | ✅ Permitted | `pip install numpy` |
| pandas | ≥1.3 | BSD-3-Clause | ✅ Permitted | `pip install pandas` |

**License Compliance:** All packages use permissive licenses (BSD, MIT, PSF) that permit commercial use in AI agent applications.

## Inputs

| Input | Format | Description |
|-------|--------|-------------|
| Visium data | `.h5ad`, `.h5`, or Space Ranger directory | Gene expression + spatial coordinates |
| H&E image | Embedded in above | Tissue histology (optional, enhances spatial plots) |

**Built-in example:** V1_Human_Heart from 10x Genomics (~4,247 spots, ~33,538 genes, includes H&E image).

## Outputs

**Analysis objects:**
- `adata_processed.h5ad` — Complete processed AnnData for downstream use
  - Load with: `adata = sc.read_h5ad('adata_processed.h5ad')`
  - Contains: clusters, embeddings, SVG results, spatial graph

**Tables (CSV):**
- `spatially_variable_genes.csv` — SVGs ranked by Moran's I with FDR
- `cluster_assignments.csv` — Spot barcodes + Leiden cluster + spatial coordinates
- `neighborhood_enrichment.csv` — Cluster-cluster enrichment z-scores
- `spot_metadata.csv` — All spot-level QC and annotation metadata
- `analysis_summary.txt` — Human-readable report

**Plots (PNG + SVG):**
- `qc_violins` — QC metric distributions
- `spatial_clusters` — Leiden clusters overlaid on tissue
- `spatial_markers` — Selected marker gene expression on tissue
- `umap_clusters` — UMAP embedding colored by cluster
- `neighborhood_enrichment` — Cluster enrichment heatmap
- `co_occurrence` — Co-occurrence probability vs distance
- `top_svgs` — Bar chart of top spatially variable genes
- `spatial_svg_[GENE]` — Spatial expression of top SVG

## Clarification Questions

**ALWAYS ask Question 1 FIRST:**

### 1. Input Files (ASK THIS FIRST):
- Do you have Visium data files to analyze?
  - **Supported formats:** `.h5ad`, `.h5`, or Space Ranger output directory
- **Or use example data?** V1_Human_Heart from 10x Genomics (human cardiac tissue, ~4K spots)

> 🚨 **IF EXAMPLE DATA SELECTED:** All parameters are pre-configured. **Skip remaining questions.** Proceed directly to Step 1.

### 2. Analysis Parameters (ONLY if user provides own data):
- **Clustering resolution?**
  - a) 0.5 (fewer, broader clusters)
  - b) 0.8 (standard — recommended)
  - c) 1.2 (more, finer clusters)
- **Mitochondrial threshold?**
  - a) 50% (recommended for cardiac/muscle tissue — high MT is normal)
  - b) 20% (standard for most tissues)
  - c) 30% (moderate)

### 3. Marker Genes (ONLY if user provides own data):
- Which marker genes to highlight in spatial plots?
  - Provide a list or use tissue-appropriate defaults

## Standard Workflow

🚨 **MANDATORY: USE SCRIPTS EXACTLY AS SHOWN — DO NOT WRITE INLINE CODE** 🚨

> **Note:** Run from the OmicsClaw root directory and add the workflow scripts to `sys.path`:
> ```python
> import sys; import os; sys.path.insert(0, os.path.abspath('knowledge_base/scripts/spatial-transcriptomics'))
> ```

**Step 1 — Load data:**
```python
from load_example_data import load_visium_heart
adata = load_visium_heart()
```
**DO NOT write inline data loading code. Just use the script.**

**✅ VERIFICATION:** You MUST see: `"✓ Data loaded successfully!"`

---

**Step 2 — Run analysis:**
```python
from spatial_workflow import run_spatial_analysis
adata = run_spatial_analysis(adata, output_dir="visium_results")
```
**DO NOT write inline analysis code. Just use the script.**

**✅ VERIFICATION:** You MUST see: `"✓ Spatial analysis completed successfully!"`

**❌ IF YOU DON'T SEE THIS:** You wrote inline code. Stop and use the script.

---

**Step 3 — Generate visualizations:**
```python
from generate_all_plots import generate_all_plots
generate_all_plots(adata, output_dir="visium_results")
# For non-cardiac tissue, pass tissue-appropriate markers:
# generate_all_plots(adata, output_dir="visium_results", marker_genes=["GENE1", "GENE2"])
```
🚨 **DO NOT write inline plotting code (plt.savefig, ggplot, clustermap, etc.). Just use the script.** 🚨

**The script handles PNG + SVG export with graceful fallback for SVG.**

**✅ VERIFICATION:** You MUST see: `"✓ All visualizations generated successfully!"`

---

**Step 4 — Export results:**
```python
from export_results import export_all
export_all(adata, output_dir="visium_results")
```
**DO NOT write custom export code. Use export_all().**

**✅ VERIFICATION:** You MUST see:
```
==================================================
=== Export Complete ===
==================================================
```

---

⚠️ **CRITICAL — DO NOT:**
- ❌ **Write inline analysis code** → **STOP: Use `run_spatial_analysis()`**
- ❌ **Write inline plotting code** → **STOP: Use `generate_all_plots()`**
- ❌ **Write custom export code** → **STOP: Use `export_all()`**
- ❌ **Try to install system libraries** → scripts handle optional deps gracefully

**⚠️ IF SCRIPTS FAIL — Script Failure Hierarchy:**
1. **Fix and Retry (90%)** — Install missing package, re-run script
2. **Modify Script (5%)** — Edit the script file itself, document changes
3. **Use as Reference (4%)** — Read script, adapt approach, cite source
4. **Write from Scratch (1%)** — Only if genuinely impossible, explain why

**NEVER skip directly to writing inline code without trying the script first.**

## Common Issues

| Error | Cause | Fix |
|-------|-------|-----|
| **`ModuleNotFoundError: squidpy`** | Missing package | `pip install squidpy` |
| **`ModuleNotFoundError: plotnine_prism`** | Missing theme package | `pip install plotnine-prism` |
| **SVG export failed** | Missing SVG backend | Normal — PNG always generated. SVG is best-effort. |
| **`ValueError: coord_type='grid'`** | Non-grid spatial data | Use `coord_type='generic'` for non-Visium data |
| **0 SVGs found (FDR < 0.05)** | Low signal or few permutations | Increase `svgs_n_perms=1000` or relax FDR threshold |
| **Memory error on large dataset** | Too many spots/genes | Filter more aggressively or use `sc.pp.subsample()` |
| **`KeyError: 'spatial'`** | Missing spatial coordinates | Ensure data was loaded with `sc.read_visium()` or has `.obsm['spatial']` |
| **NaN in co-occurrence** | Known squidpy issue with `n_splits` | Use default `n_splits` parameter (do not override) |

## Interpreting Results

**Spatially Variable Genes (SVGs):**
- **Moran's I close to +1** → Gene expression is spatially clustered (strong spatial pattern)
- **Moran's I close to 0** → No spatial structure (random distribution)
- **Moran's I close to -1** → Dispersed pattern (checkerboard; rare in practice)
- **FDR < 0.05** is the standard significance threshold; use < 0.01 for stringent filtering
- Top SVGs typically include tissue-specific markers and boundary genes

**Neighborhood Enrichment Z-scores:**
- **Z > 2** → Clusters are significantly co-localized (tend to be spatially adjacent)
- **Z < -2** → Clusters are significantly segregated (avoid each other spatially)
- **-2 to 2** → No significant spatial preference
- Diagonal values (self-enrichment) indicate how spatially cohesive each cluster is

**Co-occurrence Curves:**
- Probability above expected → Clusters co-occur more than random at that distance
- Distance-dependent changes reveal spatial organization (e.g., border zone cell types co-occur at short range)

**Cluster-to-Tissue Mapping:**
- Compare spatial cluster plots with H&E histology to validate biological relevance
- Well-defined spatial clusters that match visible tissue structures (e.g., myocardium, fibrotic region) indicate meaningful tissue domains

## Agent Summary Guidelines

When presenting results to the user, the agent should:

- **Report key numbers:** spots analyzed, clusters found, number of significant SVGs
- **Highlight top 5-10 SVGs** with Moran's I values and known biological roles
- **Describe spatial patterns:** which clusters are co-localized vs segregated
- **Connect to biology:** relate spatial patterns to tissue architecture visible in H&E
- **Note limitations:** permutation count affects SVG p-values; low `n_perms` may miss weak signals
- **DO NOT** hallucinate gene functions — only report known annotations or suggest looking up unknown genes
- **DO NOT** over-interpret co-occurrence curves from small datasets or few clusters

**Mitochondrial content note:** Cardiac/muscle tissue has naturally high MT% (~30-40%) due to mitochondria-rich cells. The default `max_pct_mito=50%` is appropriate for heart tissue. For other tissues (brain, liver, immune), use 20% or lower.

## Suggested Next Steps

- **Functional enrichment** on SVG gene sets → `functional-enrichment-from-degs`
- **Cell type deconvolution** with cell2location or RCTD (specialized workflow)
- **Cell-cell communication** with CellChat or COMMOT on spatial data
- **Multi-sample integration** for comparing conditions (e.g., MI vs healthy)
- **Gene regulatory networks** on spatial clusters → `grn-pyscenic`

## Related Skills

| Skill | Relationship |
|-------|-------------|
| `scrnaseq-scanpy-core-analysis` | Companion scRNA-seq analysis (non-spatial) |
| `functional-enrichment-from-degs` | Downstream: enrichment on SVG gene lists |
| `de-results-to-gene-lists` | Downstream: gene list preparation from SVGs |
| `grn-pyscenic` | Downstream: regulatory networks from spatial clusters |
| `coexpression-network` | Downstream: co-expression on spatial domains |

## References

- **Squidpy:** Palla G, et al. "Squidpy: a scalable framework for spatial omics analysis." *Nature Methods* (2022). doi:10.1038/s41592-021-01358-2
- **Scanpy:** Wolf FA, et al. "SCANPY: large-scale single-cell gene expression data analysis." *Genome Biology* (2018). doi:10.1186/s13059-017-1382-0
- **Moran's I:** Moran PAP. "Notes on continuous stochastic phenomena." *Biometrika* (1950). doi:10.2307/2332142
- **10x Visium:** 10x Genomics. "Visium Spatial Gene Expression." https://www.10xgenomics.com/platforms/visium

**Detailed parameter guidance:** See `references/spatial-analysis-guide.md`
