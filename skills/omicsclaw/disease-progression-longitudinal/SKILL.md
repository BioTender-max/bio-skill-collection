---
id: disease-progression-longitudinal
name: Disease Progression Trajectory Analysis
category: multi_omics
short-description: Reconstruct disease progression trajectories from longitudinal patient omics data.
detailed-description: Analyze time-series patient data (RNA-seq, proteomics, metabolomics) to reconstruct consensus disease trajectories using TimeAx multiple alignment. Orders samples by disease pseudotime, identifies trajectory-associated features, and validates against clinical outcomes. Handles irregular sampling patterns and works with cross-sectional or longitudinal cohorts.
starting-prompt: Analyze disease progression trajectories from longitudinal patient omics data
---

# Disease Progression Trajectory Analysis

## When to Use This Skill

Use this skill when you have **longitudinal patient omics data** and want to:
- ✅ Reconstruct disease progression trajectories from time-series data
- ✅ Order samples by disease stage (pseudotime) with irregular sampling
- ✅ Identify biomarkers changing along disease trajectory
- ✅ Stratify patients as fast vs. slow progressors
- ✅ Predict clinical outcomes from trajectory position
- ✅ Validate computational staging against clinical measures

**Required data:**
- Minimum 10 patients with 3+ timepoints each
- Omics data: RNA-seq, proteomics, metabolomics, or clinical biomarkers
- Metadata: Patient IDs, timepoints (days/months/years), optional outcomes

**Primary method:** TimeAx multiple trajectory alignment (handles irregular sampling)

**Feature identification:** Polynomial regression (linear/quadratic/cubic) per the TimeAx paper (Frishberg et al., Nat Commun 2023), with FDR-corrected Q-value filtering. Captures both monotonic and non-monotonic dynamics.

**Alternative methods:** Linear Mixed Models (regular sampling), Hidden Markov Models (discrete stages)

## Installation

**R ≥ 4.0** with the TimeAx package (primary trajectory method):

```r
# Install TimeAx from GitHub
install.packages("remotes")
remotes::install_github("amitfrish/TimeAx")

# Required for plotting
install.packages(c("ggplot2", "ggprism"))

# Required for demo dataset (GSE128959 batch correction)
BiocManager::install("sva")
```

**Python ≥ 3.9** for the workflow wrapper and analysis pipeline:

```bash
# Core analysis packages
pip install numpy pandas scipy scikit-learn statsmodels lifelines

# Visualization packages
pip install seaborn matplotlib

# PDF report generation (optional)
pip install reportlab

# Optional
pip install hmmlearn        # Hidden Markov Models alternative
```

**For Linear Mixed Models alternative:** R packages `lme4`, `lmerTest`

**License compliance:** All packages use permissive licenses (MIT, BSD, Apache 2.0) - commercial AI agent use permitted.

For detailed installation and troubleshooting, see [troubleshooting_guide.md](references/troubleshooting_guide.md)

## Inputs

**Required files:**

1. **Data matrix** (features × samples)
   - CSV/TSV format with features as rows, samples as columns
   - Feature types: genes, proteins, metabolites, or clinical biomarkers
   - Normalized counts or continuous measurements
   - ⚠️ **TimeAx requires all-positive values** (e.g., log2-normalized, RMA). Do NOT Z-score normalize before TimeAx — it creates negative values that disable the `ratio` mechanism.

2. **Sample metadata** (CSV/TSV)
   - Required columns: `sample_id`, `patient_id`, `timepoint`
   - Optional: `outcome`, `treatment`, `batch`, clinical covariates
   - Timepoints: numeric values (days, months, years from baseline)

**Data requirements:**
- ≥10 patients minimum (20+ recommended)
- ≥3 timepoints per patient minimum
- Handles irregular sampling (different timepoints per patient)
- Works with cross-sectional + longitudinal cohorts

## Outputs

**Primary results:**
- `pseudotime_assignments.csv` - Disease pseudotime for each sample
- `trajectory_features.csv` - Features changing along trajectory, with polynomial degree, R², and direction
- `patient_summaries.csv` - Per-patient progression statistics
- `all_feature_statistics.csv` - Statistics for all tested features

**Analysis objects (for downstream use):**
- `timeax_model.pkl` - Complete TimeAx model object
  - Load with: `model = pickle.load(open('timeax_model.pkl', 'rb'))`
  - Required for: Projecting new samples, downstream trajectory analysis

**Reports:**
- `analysis_report.pdf` - Publication-quality PDF with Introduction, Methods, Results, Conclusions
  - Requires: `pip install reportlab` (optional — markdown report generated regardless)
- `SUMMARY.txt` - Plain-text summary report

**TimeAx R plots (PNG + SVG, generated in Step 2):**
- `timeax_pseudotime_vs_time.png/.svg` - Per-patient pseudotime vs actual time trajectories
- `timeax_progression_rates.png/.svg` - Patient progression rate comparison (fast vs slow)
- `timeax_seed_dynamics.png/.svg` - Seed feature expression trends along pseudotime
- `timeax_uncertainty.png/.svg` - Pseudotime uncertainty distribution

**Python plots (PNG + SVG, generated in Step 3):**
- `patient_trajectories_pca.png/.svg` - PCA with pseudotime coloring and patient trajectory lines
- `patient_trajectories_umap.png/.svg` - UMAP nonlinear projection
- `trajectory_heatmap.png/.svg` - Feature expression clustermap
- `trajectory_trends.png/.svg` - Polynomial fit trends for top features
- `pseudotime_vs_stage.png/.svg` - Pseudotime vs clinical tumor stage (biological validation)
- `patient_progression.png/.svg` - Per-patient pseudotime spaghetti plot
- `seed_feature_heatmap.png/.svg` - TimeAx seed feature dynamics heatmap

**Metadata:**
- `model_metadata.json` - Analysis parameters, quality metrics (monotonicity, robustness)

## Clarification Questions

🚨 **ALWAYS ask Question 1 FIRST. Do not ask about data type, study design, or analysis parameters before the user has answered Question 1.**

### 1. Input Files (ASK THIS FIRST)
   - **Do you have longitudinal patient omics data to analyze?**
     - If uploaded: Are these your data matrix and sample metadata files?
     - Expected: Data matrix (features × samples) + metadata (sample_id, patient_id, timepoint)
   - **Or use example/demo data?**
     - **GSE128959 bladder cancer recurrence** (18 patients, 84 samples, 17K genes) — from the TimeAx paper (Frishberg et al. 2023). Requires R + `sva` package. Downloads ~5MB on first run.

> 🚨 **IF EXAMPLE DATA SELECTED:** All parameters are pre-defined (bladder cancer microarray, 18 patients, 4-6 timepoints, tumor recurrence, TimeAx method with ComBat batch correction). **DO NOT ask questions 2-6.** Proceed directly to Step 1.

**Questions 2-6 are ONLY for users providing their own data:**

### 2. **Data Type**: Bulk RNA-seq, proteomics, metabolomics, clinical biomarkers, or multi-omics?
### 3. **Study Design**: Number of patients (min 10, recommend 20+)? Timepoints per patient (min 3)? Sampling pattern (regular/irregular)? Time units and range?
### 4. **Disease Context**: Disease type? Treatment status? Available clinical outcomes (survival, relapse, response)? Known clinical staging?
### 5. **Analysis Goals**: Pseudotime ordering, patient stratification, biomarker discovery, outcome prediction, or trajectory comparison?
### 6. **Method Preference**: TimeAx (recommended), Linear Mixed Models, Hidden Markov Models, or not sure?

## Standard Workflow

> **Note:** Run from the OmicsClaw root directory and add the workflow scripts to `sys.path`:
> ```python
> import sys; import os; sys.path.insert(0, os.path.abspath('knowledge_base/scripts/disease-progression-longitudinal'))
> ```

🚨 **MANDATORY: USE SCRIPTS EXACTLY AS SHOWN - DO NOT WRITE INLINE CODE** 🚨

**Step 1 - Load and preprocess data:**

**For example/demo data (GSE128959 bladder cancer):**
```python
from load_and_preprocess import load_example_data, load_and_preprocess_data

# Load GSE128959 (downloads and preprocesses via R on first run)
data, metadata = load_example_data()

# Save to files for the standard pipeline
data.to_csv('gse128959_expression.csv')
metadata.to_csv('gse128959_metadata.csv', index=False)

# Run through standard preprocessing
data, metadata, preprocessing_stats = load_and_preprocess_data(
    data_file='gse128959_expression.csv',
    metadata_file='gse128959_metadata.csv',
    data_type='rnaseq',
    min_patients=10,
    min_timepoints=3
)
```

**For your own data:**
```python
from load_and_preprocess import load_and_preprocess_data

data, metadata, preprocessing_stats = load_and_preprocess_data(
    data_file="patient_expression.csv",
    metadata_file="sample_metadata.csv",
    data_type='rnaseq',  # 'rnaseq', 'proteomics', 'metabolomics', 'clinical'
    min_patients=10,
    min_timepoints=3
)
```
**DO NOT write inline data loading or preprocessing code. Just use the script.**

**✅ VERIFICATION:** You MUST see: `"✓ Data loaded and preprocessed successfully!"`

**Step 2 - Run trajectory analysis:**
```python
from run_trajectory_analysis import run_trajectory_analysis

# Run TimeAx alignment and identify trajectory features
results = run_trajectory_analysis(
    data,
    metadata,
    method='timeax',  # 'timeax', 'lmm', 'hmm'
    patient_column='patient_id',
    time_column='timepoint'
)
# Extract: pseudotime, trajectory_features, model, robustness_score
```
**DO NOT write inline TimeAx or trajectory code. Just use the script.**

**✅ VERIFICATION:** You MUST see: `"✓ Trajectory analysis completed successfully!"`

**Step 3 - Generate visualizations:**
```python
from generate_all_plots import generate_all_plots

# Generate all plots (PNG + SVG with graceful fallback)
generate_all_plots(
    data,
    metadata,
    results,
    output_dir='trajectory_results'
)
```
🚨 **DO NOT write inline plotting code (plt.savefig, seaborn, etc.). Just use the script.** 🚨

**The script handles PNG + SVG export with graceful fallback for SVG dependencies.**

**✅ VERIFICATION:** You MUST see: `"✓ All visualizations generated successfully!"`

**Step 4 - Export results:**
```python
from export_results import export_all

# Export all results, model object, and metadata
export_all(
    data=data,
    metadata=metadata,
    results=results,
    output_dir='trajectory_results'
)
```
**DO NOT write custom export code. Use export_all().**

**✅ VERIFICATION:** You MUST see: `"=== Export Complete ==="`

---

⚠️ **CRITICAL - DO NOT:**
- ❌ **Write inline data loading code** → **STOP: Use `load_and_preprocess_data()`**
- ❌ **Write inline TimeAx/trajectory code** → **STOP: Use `run_trajectory_analysis()`**
- ❌ **Write inline plotting code** → **STOP: Use `generate_all_plots()`**
- ❌ **Write custom export code** → **STOP: Use `export_all()`**

**⚠️ IF SCRIPTS FAIL - Script Failure Hierarchy:**
1. **Fix and Retry (90%)** - Install missing package, re-run script
2. **Modify Script (5%)** - Edit the script file itself, document changes
3. **Use as Reference (4%)** - Read script, adapt approach, cite source
4. **Write from Scratch (1%)** - Only if genuinely impossible, explain why

**NEVER skip directly to writing inline code without trying the script first.**

---

## Detailed Methodology

For comprehensive details on algorithms, parameters, and methods:

- **TimeAx algorithm:** [timeax_methodology.md](references/timeax_methodology.md)
- **Alternative methods (LMM, HMM):** [lmm_hmm_alternatives.md](references/lmm_hmm_alternatives.md)
- **Method comparison and selection:** [method_comparison.md](references/method_comparison.md)
- **Data preprocessing by type:** [data_preprocessing_guide.md](references/data_preprocessing_guide.md)
- **Validation framework:** [validation_framework.md](references/validation_framework.md)

## Quality Control

**Quick checklist:**
- ✅ ≥10 patients with ≥3 timepoints each
- ✅ Within-patient monotonicity >0.5 (good) or 0.3-0.5 (moderate)
- ✅ Pseudotime correlates with clinical measures (r >0.2, p <0.05)
- ✅ Trajectory features identified (seed feature fallback if FDR <0.05 yields 0)
- ✅ Samples don't cluster by batch (check PCA)

**Note on robustness:** The TimeAx `robustness()` function (v0.1.1) can produce misleading negative values even on valid data. Use **within-patient monotonicity** as the primary quality metric instead.

For comprehensive QC guidelines, see [validation_framework.md](references/validation_framework.md)

## Common Issues

| Error | Cause | Solution |
|-------|-------|----------|
| **Negative robustness score** | Known TimeAx v0.1.1 bug | **Normal.** The `robustness()` function is unreliable. Use **within-patient monotonicity** (>0.5 = good) as the primary quality metric instead. |
| **0 trajectory features (FDR <0.05)** | FDR too stringent for genome-wide test | **Normal with real data.** The script automatically falls back to testing TimeAx seed features (reduced FDR burden) and nominal p < 0.05. |
| **Memory error during alignment** | Too many features (>20,000) | Reduce to 5000-10000 most variable features before TimeAx. Script does this automatically. |
| **SVG export failed** | Missing cairo system library | **Normal - PNG still generated.** Script handles fallback automatically. DO NOT try to install cairo manually. |
| **Samples cluster by batch not time** | Uncorrected batch effects | Run ComBat batch correction before trajectory analysis. Set `batch_correction=True` in preprocessing. |
| **Negative values disable `ratio` mode** | Z-score or log-fold-change normalization | TimeAx `ratio=TRUE` requires positive values. Use log2 counts, RMA, or TPM — NOT Z-scores. |
| **"R TimeAx not available"** | R or TimeAx R package not installed | **STOP: Install R, then run:** `Rscript -e 'remotes::install_github("amitfrish/TimeAx")'`. See Installation section. |
| **PDF report not generated** | reportlab not installed | **Normal.** Install with `pip install reportlab`. SUMMARY.txt is always generated as fallback. |

For complete troubleshooting, see [troubleshooting_guide.md](references/troubleshooting_guide.md)

## Suggested Next Steps

After trajectory analysis, consider these downstream analyses:

1. **Functional enrichment** → Use `functional-enrichment-gprofiler` skill
   - Input: `trajectory_features.csv` (top up/down-regulated features)
   - Find pathways changing along disease trajectory

2. **Tissue expression analysis** → Use `tissue-expression-from-degs` skill
   - Input: `trajectory_features.csv`
   - Identify tissue-specific trajectory markers

3. **Transcription factor activity** → Use `tf-activity-dorothea` skill
   - Input: `pseudotime_assignments.csv` + original expression data
   - Find TFs driving disease progression

4. **Survival analysis** → Built into clinical validation
   - Input: `pseudotime_assignments.csv` + survival data
   - Stratify patients by pseudotime tertiles/quartiles

5. **Project new samples** → Use `scripts/timeax_inference.py`
   - Load: `timeax_model.pkl`
   - Stage new patients on trained trajectory

## Related Skills

**Upstream (data generation):**
- `bulk-rnaseq-counts-to-de-deseq2` - Generate expression data
- `proteomics-differential-expression` - Proteomics quantification
- `metabolomics-preprocessing` - Metabolite data

**Downstream (interpretation):**
- `functional-enrichment-gprofiler` - Pathway analysis of trajectory features
- `tissue-expression-from-degs` - Tissue-specific markers
- `tf-activity-dorothea` - Transcription factor drivers
- `grn-pyscenic` - Gene regulatory networks along trajectory

**Alternative trajectory methods:**
- `pseudotime-monocle` - For single-cell RNA-seq trajectories
- `trajectory-inference-slingshot` - Branching trajectories

## References

### Primary Citations

1. **TimeAx:** Frishberg A, van den Munckhof ICL, Ter Horst R, et al. Reconstructing disease dynamics for mechanistic insights and clinical benefit. *Nat Commun*. 2023;14(1):6940. [https://doi.org/10.1038/s41467-023-42354-8](https://doi.org/10.1038/s41467-023-42354-8)

2. **Linear Mixed Models:** Bates D, Mächler M, Bolker B, Walker S. Fitting Linear Mixed-Effects Models Using lme4. *J Stat Softw*. 2015;67(1):1-48.

3. **Disease Trajectories Review:** Schmidt AF, Heerspink HJL, Denig P, et al. Disease trajectory browser for exploring temporal, population-wide disease progression patterns. *Nat Commun*. 2020;11:4952.

### Software

| Software | Version | License | Commercial Use |
|----------|---------|---------|----------------|
| TimeAx | ≥0.1.0 | MIT | ✅ Permitted |
| NumPy | ≥1.21 | BSD | ✅ Permitted |
| Pandas | ≥1.3 | BSD | ✅ Permitted |
| scikit-learn | ≥1.0 | BSD | ✅ Permitted |
| seaborn | ≥0.11 | BSD | ✅ Permitted |
| matplotlib | ≥3.5 | BSD | ✅ Permitted |
| ggprism (R) | ≥1.0.3 | GPL (≥3) | ✅ Permitted |
| sva (R) | ≥3.40 | Artistic-2.0 | ✅ Permitted |
| reportlab | ≥3.6 | BSD | ✅ Permitted |

### Online Resources

- TimeAx GitHub: [https://github.com/amitfrish/TimeAx](https://github.com/amitfrish/TimeAx)
- TimeAx Documentation: [https://timeax.readthedocs.io/](https://timeax.readthedocs.io/)
- Disease Progression Modeling Review: [https://www.annualreviews.org/content/journals/10.1146/annurev-biodatasci-110123-041001](https://www.annualreviews.org/content/journals/10.1146/annurev-biodatasci-110123-041001)
