---
id: lasso-biomarker-panel
name: LASSO Biomarker Panel Discovery & Validation
category: multi_omics
short-description: "Select minimal biomarker panels using LASSO regularization with nested cross-validation, stability selection, and independent cohort validation."
detailed-description: "Build parsimonious biomarker panels (5-15 features) from high-dimensional omics data using penalized logistic regression (elastic net) with nested cross-validation and stability selection. Produces ROC/AUC curves, calibration plots, and feature importance visualizations suitable for clinical exploratory endpoint submissions. Supports discovery/validation cohort design following Ali et al. (Nat Med 2025) methodology. Works with RNA-seq, proteomics, or any quantitative feature matrix with binary outcomes."
starting-prompt: Build a LASSO biomarker panel to predict treatment response from gene expression data.
---

# LASSO Biomarker Panel Discovery & Validation

Select minimal, interpretable biomarker panels from high-dimensional omics data using penalized logistic regression (LASSO/elastic net) with nested cross-validation and stability selection.

## When to Use This Skill

Use this skill when you need to:
- **Select a minimal biomarker panel** (5-15 features) from thousands of candidates
- **Build a predictive model** for a binary clinical outcome (responder/non-responder, disease/control)
- **Validate across cohorts** — discovery + independent validation design
- **Generate regulatory-grade outputs** — ROC/AUC, calibration, decision curves
- **Design clinical exploratory endpoints** from omics biomarker signatures

**Don't use this skill for:**
- Unsupervised clustering (use `bulk-omics-clustering`)
- Differential expression only (use `bulk-rnaseq-counts-to-de-deseq2`)
- Multi-omics integration/factor discovery (use `multiomics-patient-stratification`)
- Continuous outcomes — this skill is for binary classification

## Installation

```r
options(repos = c(CRAN = "https://cloud.r-project.org"))
if (!require('BiocManager', quietly = TRUE)) install.packages('BiocManager')

# Core (required)
install.packages(c('glmnet', 'pROC', 'ggplot2', 'ggprism', 'ggrepel'))

# Heatmap (required for feature heatmap)
BiocManager::install(c('ComplexHeatmap'))
install.packages('circlize')

# Example data — Sepsis MARS consortium (recommended demo) + breast cancer/UNIFI
BiocManager::install(c('GEOquery', 'Biobase'))

# Example data — IMvigor210 bladder cancer IO (alternative demo)
install.packages('remotes')
remotes::install_github('SiYangming/DESeq', upgrade = 'never')
remotes::install_github('SiYangming/IMvigor210CoreBiologies', upgrade = 'never')
BiocManager::install('DESeq2')

# Optional: DE pre-filtering
BiocManager::install('limma')

# Optional: Biological interpretation (pathway enrichment, cell-type context)
BiocManager::install(c('clusterProfiler', 'org.Hs.eg.db', 'fgsea'))
install.packages('msigdbr')
```

| Software | Version | License | Commercial Use | Installation |
|----------|---------|---------|----------------|-------------|
| glmnet | >=4.1 | GPL-2 | Permitted | `install.packages('glmnet')` |
| pROC | >=1.18 | GPL (>=3) | Permitted | `install.packages('pROC')` |
| ggplot2 | >=3.4 | MIT | Permitted | `install.packages('ggplot2')` |
| ggprism | >=1.0.3 | GPL (>=3) | Permitted | `install.packages('ggprism')` |
| ggrepel | >=0.9 | GPL-3 | Permitted | `install.packages('ggrepel')` |
| ComplexHeatmap | >=2.10 | MIT | Permitted | `BiocManager::install('ComplexHeatmap')` |
| circlize | >=0.4.15 | MIT | Permitted | `install.packages('circlize')` |

## Inputs

**Required:**
- **Expression matrix** (genes x samples): TPM, FPKM, normalized counts, or protein abundance
- **Sample metadata**: Data frame with a **binary outcome column** (0/1 or two-level factor)
  - Rownames must match expression column names
  - Minimum 20 samples per group (40+ recommended)

**Optional:**
- **Validation cohort**: Independent expression matrix + metadata with same outcome
- **Pre-filtered feature list**: From DE analysis or WGCNA hub genes (see Related Skills)

## Outputs

**Primary results:**
- `biomarker_panel.csv` — Final panel features with LASSO coefficients and selection frequencies
- `all_feature_stability.csv` — All features ranked by selection frequency
- `discovery_performance.csv` — Per-fold AUC, sensitivity, specificity
- `validation_performance.csv` — External validation metrics (if validation cohort provided)

**Analysis objects (RDS):**
- `lasso_model.rds` — Complete model result for downstream use
  - Load with: `model <- readRDS('results/lasso_model.rds')`
  - Predict with: `source("scripts/lasso_workflow.R"); predict_biomarker_panel(model, new_X)`
  - Required for: `multiomics-patient-stratification`, downstream prediction

**Plots (PNG + SVG at 300 DPI):**
- `roc_curve.png/.svg` — ROC curve (discovery + validation overlay)
- `stability_barplot.png/.svg` — Feature selection frequency across CV folds
- `coefficient_forest.png/.svg` — LASSO coefficients with 95% CIs
- `calibration_curve.png/.svg` — Predicted vs observed probability
- `auc_distribution.png/.svg` — AUC distribution across CV folds
- `feature_heatmap.png/.svg` — Clustered heatmap of panel features

**Reports:**
- `summary_report.md` — Comprehensive analysis report (goals, context, datasets, methods, results)
- `summary_report.pdf` — PDF report (only if tinytex installed; falls back to HTML automatically — this is expected in most environments)
- `summary_report.Rmd` — R Markdown source (customizable)

## Clarification Questions

**ALWAYS ask Question 1 FIRST.**

### 1. **Example or Own Data?** (ASK THIS FIRST):
   - **a) Run example dataset to showcase the workflow** (recommended)
     - Runs a sepsis blood transcriptomics demo (MARS Consortium, ICU patients) that derives a ~15–25 gene panel for identifying immunosuppressed sepsis patients — CV AUC ~0.986 (discovery cohort estimate; panel size varies across runs)
     - **No further questions needed.** Proceed directly to Step 1 with all defaults.
   - **b) I have my own expression data and patient outcomes to analyze**
     - Continue to Questions 2-4 below

> **IF EXAMPLE SELECTED (option a):** Skip all remaining questions. Run Step 1 with: `data <- load_sepsis_data(outcome = "endotype")`, then Steps 2-4 with defaults (`top_n_variable = 2000`, `alpha = 0.5`, `disease = "sepsis"`).

**Questions 2-4 are ONLY asked if the user selected option (b) — own data:**

### 2. **Input Files** *(own data only)*:
   - What expression data file(s) do you have? (CSV, TSV, RDS, or Bioconductor object)
     - Expected: Gene/protein × sample matrix (rows = features, columns = samples)
   - What metadata/clinical file do you have?
     - Must include a **binary outcome column** (0/1 or two-level factor)
     - Rownames must match expression column names

### 3. **Outcome & Organism** *(own data only)*:
   - What is the binary outcome column name in your metadata?
   - What do the two levels represent? (e.g., responder/non-responder, disease/control)
   - What organism? (human/mouse/rat — for pathway enrichment)

### 4. **Analysis Options** *(own data only — structured)*:
   - **LASSO regularization:**
     - a) Pure LASSO, alpha=1.0 (sparsest panel)
     - b) Elastic net, alpha=0.5 (recommended — retains correlated features)
   - **Feature pre-filtering:**
     - a) Top 2000 most variable features (recommended for >5000 features)
     - b) Top 500 most variable (for smaller datasets or faster runs)
     - c) Use all features (no filtering)

## Standard Workflow

> **Note:** Run from the OmicsClaw root directory and add the workflow scripts to `sys.path`:
> ```python
> import sys; import os; sys.path.insert(0, os.path.abspath('knowledge_base/scripts/lasso-biomarker-panel'))
> ```

**MANDATORY: USE SCRIPTS EXACTLY AS SHOWN - DO NOT WRITE INLINE CODE**

**Step 1 - Load data:**
```r
source("scripts/load_example_data.R")
data <- load_sepsis_data(outcome = "endotype")  # 479 ICU patients, Mars1 endotype classification
# OR: data <- load_sepsis_data(outcome = "mortality")  # 479 patients, 28-day mortality
# OR: data <- load_breast_cancer_pcr_data(outcome = "subtype")  # 218 tumors, Basal vs LumA
# OR: data <- load_imvigor210_data()   # 190 bladder cancer patients, atezolizumab
# OR: data <- load_unifi_data()        # 542 UC patients, UNIFI ustekinumab trial
```
**DO NOT write custom data loading code. Use the loader functions.**

**VERIFICATION:** You MUST see: `"✓ Sepsis endotype data loaded successfully!"` (or similar per dataset)

**Step 2 - Run LASSO analysis:**
```r
source("scripts/prepare_features.R")
features <- prepare_feature_matrix(data$expression, data$metadata, data$outcome_col, top_n_variable = 2000)

source("scripts/lasso_workflow.R")
model <- run_lasso_panel(features$X, features$y, alpha = 0.5)
```
**DO NOT write inline LASSO code (glmnet, cv.glmnet, etc.). Just use the scripts.**

**VERIFICATION:** You MUST see: `"✓ LASSO panel selection completed successfully!"`

**IF YOU DON'T SEE THIS:** You wrote inline code. Stop and use `source()`.

**Step 3 - Generate visualizations:**
```r
source("scripts/biomarker_plots.R")
generate_all_plots(model, X = features$X, y = features$y, output_dir = "results")
```
**DO NOT write inline plotting code (ggsave, ggplot, etc.). Just use `generate_all_plots()`.**

**The script handles PNG + SVG export with graceful fallback for SVG dependencies.**

**VERIFICATION:** You MUST see: `"✓ All biomarker plots generated successfully!"`

**Step 4 - Export results:**
```r
source("scripts/export_results.R")
export_all(model, output_dir = "results", data = data, features = features)
```
**DO NOT write custom export code. Use `export_all()`.**

**Pass `data` and `features` for a comprehensive report with disease context and methods.**

**VERIFICATION:** You MUST see: `"=== Export Complete ==="`

**NOTE on PDF:** If `export_all()` reports "PDF rendering failed", this is expected in environments without LaTeX. Inform the user that `summary_report.html` and `summary_report.md` are available instead. Do NOT silently omit this from the summary.

⚠️ **CRITICAL: Do NOT interpret panel biology without running enrichment**

After identifying the panel, do NOT describe gene functions or pathway membership from gene names alone. This is a hallucination risk. Instead:
- State the panel genes and their coefficients/stability scores
- Direct the user to run pathway enrichment as a next step
- Only describe biology if `functional-enrichment-from-degs` has been run in this session

✅ Acceptable: "ACSL6 was selected in 100% of folds with a positive coefficient."
❌ NOT acceptable: "ACSL6 is involved in mitochondrial fatty acid metabolism, consistent with..."

**Step 5 (Strongly Recommended) — External Validation:**

> **Without this step, all performance metrics are discovery-cohort estimates only and are expected to be optimistic. Do not present results as a validated panel without completing this step.**
```r
source("scripts/load_example_data.R")
val_data <- load_breast_cancer_validation_data("GSE32646")  # or load_pursuit_data()
source("scripts/validate_external.R")
source("scripts/prepare_features.R")
val_features <- prepare_validation_features(val_data$expression, features$feature_names)
val_result <- validate_panel(model, val_features$X, val_data$metadata[[val_data$outcome_col]],
                              cohort_name = "GSE32646")
export_all(model, validation_result = val_result, output_dir = "results",
           data = data, features = features)
```

**CRITICAL - DO NOT:**
- **Write inline LASSO code** -> **STOP: Use `source("scripts/lasso_workflow.R")`**
- **Write inline plotting code** -> **STOP: Use `generate_all_plots()`**
- **Write custom export code** -> **STOP: Use `export_all()`**
- **Try to install svglite** -> script handles SVG fallback automatically

**IF SCRIPTS FAIL - Script Failure Hierarchy:**
1. **Fix and Retry (90%)** - Install missing package, re-run script
2. **Modify Script (5%)** - Edit the script file itself, document changes
3. **Use as Reference (4%)** - Read script, adapt approach, cite source
4. **Write from Scratch (1%)** - Only if genuinely impossible, explain why

**NEVER skip directly to writing inline code without trying the script first.**

## Common Issues

| Error | Cause | Fix |
|-------|-------|-----|
| **"No shared samples"** | Column names don't match rownames | Check `colnames(expression)` match `rownames(metadata)` |
| **"Outcome must be binary"** | Non-binary outcome column | Ensure 2 unique values in outcome. Recode if multi-level. |
| **cv.glmnet convergence warning** | Too few samples for 10-fold CV | Reduce `n_inner_folds` to 5 or increase sample size |
| **"No features passed stability"** | Very noisy data or small effect | Script auto-relaxes to top 10 features. Consider alpha=0.5 (elastic net). |
| **Low validation AUC** | Cross-platform gene loss | Check `val_features$n_matched`. If <50% matched, use same-platform validation. |
| **SVG export error** | Missing optional dependency | Normal - `generate_all_plots()` falls back to base R svg() automatically. |
| **GEOquery download fails** | Network/firewall issue | Retry or download manually from NCBI GEO website |
| **PDF report not generated** | tinytex/LaTeX not installed | Normal fallback — use `summary_report.html` or `summary_report.md` instead. Do NOT silently omit this from the summary. |

## Agent Summary Guidelines

When presenting final results to the user, the agent MUST:

1. **Always cite the CV AUC** (from `discovery_performance.csv`), never the final model AUC from the ROC plot
2. **Always state whether external validation was performed.** If not, include this sentence verbatim:
   > "These results are from the discovery cohort only. No external validation was performed. AUC estimates are expected to be optimistic."
3. **Never describe panel gene biology** unless `functional-enrichment-from-degs` was run in this session
4. **Always report PDF status** — if PDF generation failed, say so explicitly and note that .html/.md reports are available
5. **Never use the word "validated"** to describe a panel that has only been tested in the discovery cohort

## Interpretation Guidelines

- **AUC > 0.8**: Strong discriminative ability (clinically useful)
- **AUC 0.7-0.8**: Moderate — useful with other clinical factors
- **AUC 0.6-0.7**: Weak but above chance — typical for baseline transcriptomic prediction of treatment response
- **Stability >= 80%**: Feature is robustly selected (high confidence in panel)
- **Positive coefficient**: Higher expression -> higher probability of positive outcome
- **Negative coefficient**: Higher expression -> lower probability of positive outcome
- **Calibration**: Points near diagonal = well-calibrated model

### AUC Values — Which Number to Use

Two AUC figures are produced by this workflow:

| Figure | Value | What it means | Use this? |
|--------|-------|---------------|-----------|
| Mean CV AUC (`discovery_performance.csv`) | e.g. 0.986 | Average AUC across held-out test sets | **YES — cite this** |
| Final model AUC (ROC curve plot annotation) | e.g. 0.996 | Model applied back to its own training data | **NO — in-sample, optimistic** |

**Always report the mean CV AUC as the performance estimate.** The final model AUC is only shown for reference and will always be higher.

### Interpreting CV AUC: Known Optimism Bias

The reported CV AUC from this workflow is an **estimate within the discovery cohort**, not a true out-of-sample performance figure. It is subject to optimism bias because:

- Feature stability is computed across the same samples used for AUC estimation
- The final model is re-fit on all samples after feature selection

**Expected magnitude of bias:** Typically 0.02–0.05 AUC units for datasets of this size. A discovery AUC of 0.986 should be interpreted as "likely >0.93 in an independent cohort if the signal is real" — not as a guaranteed performance floor.

**The only way to get an unbiased estimate is external validation.**

## Suggested Next Steps

After building a biomarker panel:
1. **[REQUIRED before biological interpretation] Pathway enrichment** of panel genes -> `functional-enrichment-from-degs`
2. **Co-expression context** — which WGCNA modules contain panel genes -> `coexpression-network`
3. **Patient stratification** using panel as input -> `multiomics-patient-stratification`
4. **Literature validation** — are panel genes known disease/therapy markers?
5. **Independent cohort replication** on external validation datasets

## Related Skills

| Skill | Relationship |
|-------|-------------|
| `bulk-rnaseq-counts-to-de-deseq2` | **Upstream** — DE results can pre-filter features for LASSO |
| `coexpression-network` | **Upstream** — WGCNA hub genes as LASSO candidates (Paper 1 cascade) |
| `functional-enrichment-from-degs` | **Downstream** — Pathway enrichment of panel genes |
| `bulk-omics-clustering` | **Alternative** — Unsupervised patient stratification |
| `multiomics-patient-stratification` | **Downstream** — Multi-omics integration + subtyping |

## References

- **Ali et al., Nature Medicine 2025** — Cross-disease LASSO proteomics panels (AUC 0.81-0.88). Code: [github.com/NeuroGenomicsAndInformatics/NatMed_2025_GNPC](https://github.com/NeuroGenomicsAndInformatics/NatMed_2025_GNPC)
- **Shen et al., Cell 2024** — WGCNA -> LASSO 6-protein panel (AUC 0.911)
- **Sands et al., NEJM 2019** — UNIFI Trial (GSE206285 source)
- **Sandborn et al., Gastro 2014** — PURSUIT Trial (GSE92415 source)
- [glmnet vignette](https://glmnet.stanford.edu/articles/glmnet.html) — Friedman, Hastie, Tibshirani
- [pROC package](https://web.expasy.org/pROC/) — Robin et al., BMC Bioinformatics 2011
- See [references/lasso-reference.md](references/lasso-reference.md) for parameter tuning guide
- See [references/validation-guide.md](references/validation-guide.md) for multi-cohort design
