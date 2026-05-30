---
id: multi-omics-integration
name: Multi-Omics Integration (MOFA+)
category: multi_omics
short-description: "Integrate 2+ omics layers using MOFA+ to identify latent factors explaining cross-omics variation, with variance decomposition and factor interpretation."
detailed-description: "Performs multi-omics factor analysis using MOFA2 to decompose multi-omics datasets into interpretable latent factors. Handles missing data across views, identifies shared and view-specific sources of variation, associates factors with clinical covariates, and exports factor scores for downstream patient stratification. Supports any combination of omics layers (RNA-seq, proteomics, methylation, drug response, mutations). Includes the CLL blood cancer dataset (200 patients, 4 omics) as a pharma-relevant demonstration."
starting-prompt: Integrate my multi-omics data using MOFA+ to identify latent factors driving cross-omics variation . .
---

# Multi-Omics Integration (MOFA+)

Identify **latent factors** driving variation across 2+ omics layers using **MOFA+** (Multi-Omics Factor Analysis). Decomposes multi-omics data into interpretable factors, each capturing shared or view-specific biological signal. Handles **missing data** across views natively.

## When to Use This Skill

**Use when you:**
- ✅ Have 2+ omics layers measured on overlapping samples (RNA-seq + proteomics, methylation + mutations, etc.)
- ✅ Want to find shared sources of variation across omics (not just per-omics analysis)
- ✅ Need to identify which omics layers contribute to each source of variation
- ✅ Have incomplete data (not all samples measured in all views) — MOFA handles this
- ✅ Want factor scores for downstream patient stratification or survival analysis

**Don't use for:**
- ❌ Single omics data (use `bulk-rnaseq-counts-to-de-deseq2` or `bulk-omics-clustering`)
- ❌ Supervised prediction (use `lasso-biomarker-panel` instead)
- ❌ Single-cell multi-modal (MOFA2 supports it, but consider `scrna-trajectory-inference`)
- ❌ Fewer than 10 samples per view

**Runtime:** ~5-8 minutes total (CLL example). First run adds ~1-3 min for Python environment setup.

## Installation

```r
# Bioconductor packages
if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")
BiocManager::install(c("MOFA2", "MOFAdata", "ComplexHeatmap"))

# CRAN packages
install.packages(c("ggprism", "circlize", "reshape2", "RColorBrewer"))
```

| Package | Version | License | Commercial Use | Installation |
|---------|---------|---------|----------------|--------------|
| MOFA2 | ≥1.12.0 | LGPL (≥3) | ✅ Permitted | `BiocManager::install("MOFA2")` |
| MOFAdata | ≥1.8.0 | Artistic-2.0 | ✅ Permitted | `BiocManager::install("MOFAdata")` (example data) |
| ComplexHeatmap | ≥2.18.0 | MIT | ✅ Permitted | `BiocManager::install("ComplexHeatmap")` |
| ggprism | ≥1.0.3 | GPL (≥3) | ✅ Permitted | `install.packages("ggprism")` |
| circlize | ≥0.4.15 | MIT | ✅ Permitted | `install.packages("circlize")` |
| reshape2 | ≥1.4.4 | MIT | ✅ Permitted | `install.packages("reshape2")` |
| RColorBrewer | ≥1.1 | Apache-2.0 | ✅ Permitted | `install.packages("RColorBrewer")` |
| rmarkdown | ≥2.25 | GPL-3 | ✅ Permitted | `install.packages("rmarkdown")` (optional, PDF) |

## Inputs

- **Multi-omics data:** Named list of matrices (features × samples), one per omics view
  - Minimum 2 views, any combination of omics types
  - Samples as columns, features as rows
  - Missing samples across views OK (MOFA handles incomplete overlap)
- **Sample metadata** (optional): CSV/TSV with sample IDs + clinical variables (for factor-trait associations)
- **Supported formats:** R matrices, CSV/TSV files, or MultiAssayExperiment

## Outputs

**Analysis objects (RDS):**
- `mofa_model.rds` — Complete trained MOFA model for downstream use
  - Load with: `model <- readRDS('mofa_results/mofa_model.rds')`
  - Required for: `bulk-omics-clustering` (factor-based clustering), `lasso-biomarker-panel` (feature selection)

**CSV results:**
- `factor_values.csv` — Sample factor scores (samples × factors)
- `weights_*.csv` — Feature weights per view (features × factors)
- `variance_explained_per_factor.csv` — R² per factor per view
- `variance_explained_total.csv` — Total R² per view
- `top_features_per_factor.csv` — Top 20 features per factor per view

**Visualizations (PNG + SVG):**
- `mofa_variance_per_factor` — Heatmap: R² per factor per view (signature MOFA plot)
- `mofa_total_variance` — Bar chart: total R² per view
- `mofa_factor_scatter` — Scatter: Factor 1 vs 2 colored by clinical variable
- `mofa_factor_correlation` — Tile: factor-factor correlations
- `mofa_top_weights` — Faceted bar: top feature weights per factor
- `mofa_factor_heatmap` — ComplexHeatmap: factors × samples with annotations
- `mofa_factor_clinical` — Box plots: factor values by clinical groups

**Reports:**
- `analysis_report.md` — Markdown summary with methods, results, references
- `analysis_report.pdf` — PDF report with embedded figures (requires rmarkdown + LaTeX)

## Clarification Questions

1. **Input Files** (ASK THIS FIRST):
   - Do you have multi-omics data matrices to integrate?
   - Expected: Named list of matrices (features × samples), or CSV files per omics view
   - **Or use example data?** CLL blood cancer dataset (200 patients: mRNA, methylation, mutations, drug response)

> 🚨 **IF EXAMPLE DATA SELECTED:** Skip questions 3-4. Proceed directly to Step 1.

2. **Analysis Options:**
   - *(If using example data)* Number of factors:
     - a) 15 factors — standard analysis (recommended)
     - b) 5 factors — quick demo (~2 min faster)
   - *(If using own data)* Number of factors:
     - a) 15 (recommended starting point)
     - b) Custom number

3. *(Own data only)* **Data types per view:**
   - Which omics types? (RNA-seq, proteomics, methylation, mutations, metabolomics, drug response, other)
   - Are any views binary (0/1)? MOFA uses Bernoulli likelihood for binary data.

4. *(Own data only)* **Sample metadata:**
   - Do you have a sample metadata file (CSV/TSV) with clinical variables?
   - Variables for factor-trait associations (e.g., disease status, treatment, subtype)?

## Standard Workflow

> **Note:** Run from the OmicsClaw root directory and add the workflow scripts to `sys.path`:
> ```python
> import sys; import os; sys.path.insert(0, os.path.abspath('knowledge_base/scripts/multi-omics-integration'))
> ```

🚨 **MANDATORY: USE SCRIPTS EXACTLY AS SHOWN - DO NOT WRITE INLINE CODE** 🚨

**Step 1 - Load data:**
```r
# For CLL example data:
source("scripts/load_example_data.R")
cll <- load_cll_data()

# For user data:
# source("scripts/load_example_data.R")
# cll <- load_user_data(
#   file_paths = list(RNA = "rna.csv", Protein = "protein.csv"),
#   metadata_path = "metadata.csv"
# )
```
**✅ VERIFICATION:** `"✓ Data loaded successfully!"` with per-view dimensions

---

**Step 2 - Run MOFA analysis:**
```r
source("scripts/mofa_workflow.R")
model <- run_mofa_analysis(
    data_list = cll$data,
    metadata = cll$metadata,
    n_factors = 15,
    output_dir = "mofa_results"
)
```
**DO NOT write inline MOFA code. Just call `run_mofa_analysis()`.**

⏱️ **Takes ~2-5 min** (+ ~1-3 min extra on first run for Python environment setup via basilisk).

**✅ VERIFICATION:** `"✓ MOFA model trained successfully!"` with variance explained summary

---

**Step 3 - Generate visualizations:**
```r
source("scripts/mofa_plots.R")
generate_all_plots(model, output_dir = "mofa_results")
```
🚨 **DO NOT write inline plotting code (ggsave, ggplot, Heatmap, etc.). Just use the script.** 🚨

**The script handles PNG + SVG export with graceful fallback for SVG dependencies.**

**✅ VERIFICATION:** `"✓ All plots generated successfully!"` with file count

---

**Step 4 - Export results:**
```r
source("scripts/export_results.R")
export_all(model, output_dir = "mofa_results")
```
**DO NOT write custom export code. Use `export_all()`.**

**✅ VERIFICATION:** `"=== Export Complete ==="` with file list

---

⚠️ **CRITICAL - DO NOT:**
- ❌ **Write inline MOFA code** → **STOP: Use `run_mofa_analysis()`**
- ❌ **Write inline plotting code (ggsave, ggplot, Heatmap, etc.)** → **STOP: Use `generate_all_plots()`**
- ❌ **Write custom export code** → **STOP: Use `export_all()`**
- ❌ **Try to install basilisk/reticulate manually** → MOFA2 handles Python automatically

**⚠️ IF SCRIPTS FAIL - Script Failure Hierarchy:**
1. **Fix and Retry (90%)** — Install missing package, re-run script
2. **Modify Script (5%)** — Edit the script file itself, document changes
3. **Use as Reference (4%)** — Read script, adapt approach, cite source
4. **Write from Scratch (1%)** — Only if genuinely impossible, explain why

**NEVER skip directly to writing inline code without trying the script first.**

## Common Issues

| Error | Cause | Solution |
|-------|-------|----------|
| **basilisk Python env setup slow** | First-time setup of Python backend | **Normal — wait 1-3 minutes.** Only happens once per R installation. |
| **`run_mofa` hangs at "Training model..."** | Model training in progress | **Normal — wait 2-5 min.** Training is compute-intensive. |
| **`Error in py_call_impl`: Python error** | basilisk environment issue | Restart R session, retry. If persistent: `BiocManager::install("MOFA2", force = TRUE)` |
| **Metadata download failed** | EBI FTP blocked or offline | **Normal fallback.** Analysis runs without trait plots. Metadata is optional. |
| **"No convergence"** | Too many factors or too few samples | Reduce `n_factors` (try 5-10). Ensure ≥10 samples. |
| **SVG export failed** | Missing svglite/cairo | **Normal.** PNG always generated. `generate_all_plots()` handles fallback automatically. |
| **Memory error** | Dataset too large | Filter features to top 5,000 most variable per view before MOFA. |

## Interpretation Guide

### Variance Decomposition (Key MOFA Output)
- **High R² in one view:** Factor captures view-specific variation
- **High R² across views:** Factor captures **shared** cross-omics signal (most interesting)
- **Low total R²:** MOFA explains little variation in that view — consider adding features or views

### Factor Interpretation
| Pattern | Meaning |
|---------|---------|
| Factor active in mRNA + methylation | Epigenetic regulation of transcription |
| Factor active in mutations + drug response | Genetic determinants of drug sensitivity |
| Factor correlates with clinical subtype | Biologically meaningful patient stratification |
| Factor active in only one view | View-specific technical or biological variation |

**See:** `references/mofa-interpretation-guide.md` for detailed downstream analysis.

## Suggested Next Steps

After running MOFA:
- **Patient stratification:** Use `bulk-omics-clustering` on factor scores to define molecular subtypes
- **Biomarker discovery:** Use `lasso-biomarker-panel` on top-weighted features per factor
- **Pathway enrichment:** Use `functional-enrichment-from-degs` on top mRNA features per factor
- **Network analysis:** Use `coexpression-network` on factor-associated genes
- **Survival analysis:** Use `survival-analysis-clinical` with factor scores as covariates

## Related Skills

| Skill | Relationship |
|-------|-------------|
| `bulk-omics-clustering` | Downstream: cluster on MOFA factor scores |
| `lasso-biomarker-panel` | Downstream: select biomarkers from top factor features |
| `disease-progression-longitudinal` | Complementary: trajectory analysis on factor scores |
| `coexpression-network` | Downstream: network analysis on factor-associated genes |
| `functional-enrichment-from-degs` | Downstream: pathway enrichment on top factor features |
| `bulk-rnaseq-counts-to-de-deseq2` | Upstream: generate DE results as one omics view |

## References

- Argelaguet R, et al. (2020) MOFA+: a statistical framework for comprehensive integration of multi-modal single-cell data. *Genome Biology* 21:111.
- Argelaguet R, et al. (2018) Multi-Omics Factor Analysis—a framework for unsupervised integration of multi-omics data sets. *Molecular Systems Biology* 14:e8124.
- Dietrich S, et al. (2018) Drug-perturbation-based stratification of blood cancer. *Journal of Clinical Investigation* 128(1):427-445.
