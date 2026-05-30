---
id: pooled-crispr-screens
name: Pooled CRISPR Screen Analysis
category: transcriptomics
short-description: "Analyze pooled CRISPR screens with single-cell RNA-seq readout (Perturb-seq/CROP-seq)."
detailed-description: "Process 10X feature-barcode matrices for pooled CRISPR screens with scRNA-seq readout (Perturb-seq, CROP-seq, CRISPRi/a). Maps sgRNAs to cells, performs QC, runs tiered analysis (fast t-test screening, target validation, batch-corrected DE with glmGamPoi), and identifies perturbations with significant transcriptional effects. Handles multi-library experiments with batch correction."
starting-prompt: Analyze my pooled CRISPR screen data with single-cell RNA-seq readout . .
---

# Pooled CRISPR Screen Analysis

Analyze pooled CRISPR screens with single-cell RNA-seq readout using a tiered workflow: fast screening → target validation → rigorous differential expression.

## When to Use This Skill

Use this skill when you have:
- ✅ **Pooled CRISPR screens with scRNA-seq** (Perturb-seq, CROP-seq, CRISPRi/a)
- ✅ **10X Feature Barcoding data** (sgRNA captured as feature barcodes)
- ✅ **Multi-library experiments** with biological replicates
- ✅ **sgRNA-to-cell mapping files** (already assigned)

**Don't use this skill for:**
- ❌ Arrayed CRISPR screens (separate wells per perturbation) → use bulk RNA-seq DE skills
- ❌ Non-transcriptional readouts (e.g., protein, flow cytometry)
- ❌ Data without sgRNA assignments → use CellRanger or CROP-seq pipeline first

## Quick Start (Example Data)

**Test this skill with a real CRISPRi Perturb-seq dataset (~10 minutes):**

```python
from load_example_data import load_example_data
data = load_example_data()  # Downloads Papalexi 2021 (~140MB, cached after first run)

adata_list = data['adata_list']  # List of AnnData objects (one per batch)
mapping_files = data['mapping_files']  # sgRNA mapping files
```

**What you get:**
- **Dataset:** Papalexi & Satija 2021 ECCITE-seq CRISPRi screen (THP-1 cells)
- **Size:** ~20,700 cells x 18,649 genes across 4 batches
- **Perturbations:** 25 target genes (~4 guides each) targeting immune checkpoint regulators + non-targeting controls
- **Screen type:** CRISPRi (expected knockdown direction: down)
- **Reference:** Papalexi et al. (2021) *Nature Genetics* 53:322-331

**For offline testing:** Use `load_example_data(dataset='demo')` for a small synthetic dataset.

**For your own data:** Replace with your 10X feature-barcode matrices and sgRNA mapping files (see [Inputs](#inputs)).

## Installation

**Core packages (required):**
```bash
# Create conda environment
conda create -n crispr-screen python=3.8
conda activate crispr-screen

# Install packages
pip install scanpy==1.9+ anndata==0.8+ pandas numpy scipy
pip install scikit-learn  # For outlier detection
pip install diffxpy  # For differential expression
```

**Visualization packages (required):**
```bash
pip install matplotlib seaborn
```

**Optional packages:**
```bash
# For glmGamPoi (requires R ≥4.0)
# Install R, then:
# install.packages("BiocManager")
# BiocManager::install("glmGamPoi")
pip install rpy2  # Python-R interface

# For PDF report generation (optional, recommended)
pip install reportlab
```

**Version requirements:**

| Software | Version | License | Commercial Use | Install |
|----------|---------|---------|----------------|---------|
| scanpy | ≥1.9 | BSD-3 | ✅ Permitted | `pip install scanpy` |
| anndata | ≥0.8 | BSD-3 | ✅ Permitted | `pip install anndata` |
| matplotlib | ≥3.5 | PSF | ✅ Permitted | `pip install matplotlib` |
| seaborn | ≥0.12 | BSD-3 | ✅ Permitted | `pip install seaborn` |
| scikit-learn | ≥1.0 | BSD-3 | ✅ Permitted | `pip install scikit-learn` |
| diffxpy | ≥0.7 | BSD-3 | ✅ Permitted | `pip install diffxpy` |
| reportlab | ≥3.6 | BSD | ✅ Permitted | `pip install reportlab` (optional) |
| rpy2 | ≥3.5 | GPL-2 | ✅ Permitted | `pip install rpy2` (optional) |

## Inputs

**Required:**
- **10X Feature-Barcode matrices** (.h5 format, one per library)
  - Contains gene expression + sgRNA counts
  - From CellRanger with Feature Barcoding
- **sgRNA mapping files** (TSV with cell-sgRNA assignments)
  - Format: `cell_barcode\tsgRNA_id`
  - One file per library
  - Should filter to single sgRNA assignments (doublets removed)

**sgRNA naming conventions:**
- With gene names: `GENE_sgRNA1`, `GENE_sgRNA2` (delimiter: `_`)
- Without gene names: Requires separate gene lookup table

**Alternative inputs:** CROP-seq pipeline output, custom sgRNA assignment files

**See [references/crispr_screen_best_practices.md](references/crispr_screen_best_practices.md) for data format details.**

## Outputs

**Primary results:**
- `screening_summary.txt` - Per-perturbation DE statistics from t-test
- `validation_results.csv` - Target gene knockdown/activation validation
- `glmgampoi/` - Batch-corrected DE results (top hits)
- `hit_list.csv` - Final validated hits with DE gene counts

**Processed data:**
- `adata_normalized.h5ad` - Normalized AnnData object for downstream analysis
  - Load with: `adata = sc.read_h5ad('adata_normalized.h5ad')`
  - Required for: Clustering, pseudotime, trajectory analysis
- `adata_processed.h5ad` - Final processed data with all annotations

**Analysis objects (pickle):**
- `analysis_objects.pkl` - Analysis results for downstream skills
  - Load with: `import pickle; objs = pickle.load(open('analysis_objects.pkl', 'rb'))`
  - Contains: perturbation_summary, de_results, outlier_cells
  - Required for: functional-enrichment-from-degs, coexpression-network

**Report:**
- `crispr_screen_report.pdf` - Publication-quality PDF with Introduction, Methods, Results, Conclusions
  - Requires: `pip install reportlab` (optional — text report generated regardless)

**QC plots (PNG + SVG format):**
- `qc_metrics/` - Cell counts, mapping rates, doublet rates per library
- `volcano_plots/` - Per-perturbation volcano plots (top hits)
- `target_validation/` - Target gene expression heatmaps

**DE results (per perturbation):**
- `initial_screening/` - Fast t-test results (CSV per perturbation)
- `glmgampoi/` - Rigorous DE with batch correction (top 50-100 hits)

## Clarification Questions

🚨 **ALWAYS ask Question 1 FIRST. Do not ask about screen type, library details, or analysis goals before the user has answered Question 1.**

### 1. **Input Files** (ASK THIS FIRST):
   - **Do you have 10X Feature-Barcode matrix files (.h5) to analyze?**
     - If uploaded: How many libraries/replicates?
     - Expected format: `raw_feature_bc_matrix.h5` from CellRanger
   - **Do you have sgRNA-to-cell mapping files?**
     - If yes: Format? (TSV with barcode-sgRNA pairs). Doublets already filtered?
   - **Or use example data for testing?** (Papalexi 2021 CRISPRi dataset — real data, ~140MB download)

> 🚨 **IF EXAMPLE DATA SELECTED:** All parameters are pre-defined (CRISPRi, THP-1 immune cells, 25 target genes). **DO NOT ask questions 2-6.** Proceed directly to Step 1.

**Questions 2-6 are ONLY for users providing their own data:**

### 2. **Screen Type**: CRISPRi (knockdown), CRISPRa (activation), CRISPRko (knockout), or other?
### 3. **Library Information**: How many biological replicates? Non-targeting controls present? Approximate perturbations (10-100, 100-1000, 1000+)? sgRNAs per gene (1-2, 3-5, 5+)?
### 4. **Cell Type**: Primary neurons, iPSC-derived, immune cells, cancer cell lines, other? Expected phenotype (cell death, differentiation, activation, subtle)?
### 5. **sgRNA Naming**: Do sgRNA IDs include gene names (e.g., "GENE_sgRNA1")? If not, need gene lookup table?
### 6. **Analysis Goals** *(skip for example data)*:
   - Primary goal?
     - a) Identify all hits with transcriptional phenotypes (standard)
     - b) Compare specific perturbations against each other
     - c) Focus on a known gene set
   - Run downstream pathway enrichment?
     - a) Yes (recommended)
     - b) No, just hit identification

## Typical Complete Workflow

This skill performs **core Perturb-seq analysis: screening, validation, and hit identification**. For a complete CRISPR screen workflow:

1. **This skill**: Screen analysis → validated hits with transcriptional phenotypes (H5AD + hit lists)
2. **functional-enrichment-from-degs**: Pathway enrichment on hit perturbations → biological interpretation
3. **coexpression-network**: Network analysis from perturbed cells → regulatory relationships
4. **bulk-omics-clustering**: Cluster perturbations by signature → functional groups

**Quick start:** *"Analyze my pooled CRISPR screen and identify hits with pathway enrichment"*

**Why separate skills?** Modular design works across screen types (CRISPRi/a/ko) and readouts (scRNA-seq, bulk). See [Suggested Next Steps](#suggested-next-steps) for details.

## Standard Workflow

> **Note:** Run from the OmicsClaw root directory and add the workflow scripts to `sys.path`:
> ```python
> import sys; import os; sys.path.insert(0, os.path.abspath('knowledge_base/scripts/pooled-crispr-screens'))
> ```

🚨 **MANDATORY: USE SCRIPTS EXACTLY AS SHOWN - DO NOT WRITE INLINE CODE** 🚨

**This skill uses low-freedom script execution.** Pooled CRISPR screen analysis requires careful multi-step processing with QC checkpoints. Scripts handle:
- Multi-library loading and concatenation
- sgRNA doublet filtering
- Cell-type specific QC thresholds
- Batch effect handling
- Target validation checks

**Step 1 - Load data and map sgRNAs:**

**For example data:**
```python
from load_example_data import load_example_data
data = load_example_data()  # Papalexi 2021 CRISPRi (~140MB, cached)
adata_list = data['adata_list']
mapping_files = data['mapping_files']
```

**For your own data:**
```python
from load_10x_libraries import load_multiple_libraries
from map_sgrna_to_cells import map_sgrna_to_adata
from qc_filtering import apply_qc_filters
from concatenate_libraries import concatenate_libraries

# Load, map, filter, concatenate
adata_list = load_multiple_libraries(["lib1.h5", "lib2.h5"])
adata_mapped = [map_sgrna_to_adata(ad, mf, sgrna_delimiter="_")
                for ad, mf in zip(adata_list, mapping_files)]
adata_filtered = [apply_qc_filters(ad, min_genes=2000, min_counts=8000, max_mito_pct=0.15)
                  for ad in adata_mapped]
adata = concatenate_libraries(adata_filtered, batch_labels=["lib1", "lib2"])
```
**DO NOT write inline loading/QC code. Use the functions above.**

**✅ VERIFICATION:** You should see `"✓ sgRNA mapping complete: [N] cells retained"` for each library, then `"✓ Libraries concatenated: [N] total cells"`

**Step 2 - Preprocess and normalize:**
```python
from gene_name_corrections import correct_gene_names
from expression_filtering import filter_by_expression
from normalize_and_scale import normalize_only

# Preprocessing pipeline
adata = correct_gene_names(adata, corrections={}, gene_col='gene')
adata = filter_by_expression(adata, group_key='sgRNA', min_mean_expression=0.5)
adata = normalize_only(adata, target_sum=1e6, exclude_highly_expressed=True)
```
**DO NOT write inline preprocessing code. Use the functions above.**

**✅ VERIFICATION:** You should see `"✓ Gene name corrections applied"`, then `"✓ Expression filtering: [N] genes retained"`, then `"✓ Normalization complete"`

**Step 3 - Run tiered analysis:**
```python
from screen_all_perturbations import screen_all_perturbations, call_hits
from validate_perturbations import validate_target_effect
from differential_expression_glmgampoi import run_glmgampoi_batch

# Fast screening → preliminary hits → validation
de_results = screen_all_perturbations(adata, control_group='non-targeting',
                                       gene_col='gene', test_method='t-test',
                                       output_dir='results/initial_screening/')
preliminary_hits = call_hits(de_results, min_de_genes=10)
validation = validate_target_effect(de_results, expected_direction='down',  # 'up' for CRISPRa
                                     min_log2fc=-0.5)
validated_hits = preliminary_hits[
    preliminary_hits['perturbation'].isin(
        validation[validation['target_affected']]['perturbation']
    )
]

# Rigorous DE for top hits (optional, requires R + glmGamPoi)
top_hits = validated_hits.head(50)
glmgampoi_results = run_glmgampoi_batch(adata, perturbations=top_hits['perturbation'].tolist(),
                                         donor_col='batch', output_dir='results/glmgampoi/')
```
**DO NOT write inline DE code. Use the functions above.**

**✅ VERIFICATION:** You should see `"✓ Screening complete: [N] perturbations tested"`, then `"Validated hits: [N]/[M]"`, then (if glmGamPoi runs) `"✓ glmGamPoi complete"`

**Step 4 - Visualize and export:**
```python
from visualize_perturbations import create_volcano_plots
from export_results import export_all_results

# Volcano plots for top hits
for gene in top_hits['perturbation'].head(10):
    create_volcano_plots(de_results[gene], perturbation=gene, output_dir='figures/')

# Export all results (CSV, H5AD, pickle, PDF report, hit lists)
export_all_results(adata=adata, perturbation_summary=validated_hits,
                   de_results=de_results, output_dir='results/')
```
**DO NOT write custom export code. Use export_all_results().**

**✅ VERIFICATION:** You should see `"✓ Volcano plots generated: [N] perturbations"`, then `"=== Export Complete ==="` with list of files saved

**❌ IF YOU DON'T SEE VERIFICATION MESSAGES:** You wrote inline code instead of using the functions. Stop and use the provided functions.

⚠️ **CRITICAL - DO NOT:**
- ❌ **Write inline data loading code** → **STOP: Use load_multiple_libraries() and map_sgrna_to_adata()**
- ❌ **Write inline QC/filtering code** → **STOP: Use apply_qc_filters() and filter_by_expression()**
- ❌ **Write inline DE screening code** → **STOP: Use screen_all_perturbations() and validate_target_effect()**
- ❌ **Write custom export code** → **STOP: Use export_all_results()**

**⚠️ IF SCRIPTS FAIL - Script Failure Hierarchy:**
1. **Fix and Retry (90%)** - Install missing package, re-run script
2. **Modify Script (5%)** - Edit the script file itself, document changes
3. **Use as Reference (4%)** - Read script, adapt approach, cite source
4. **Write from Scratch (1%)** - Only if genuinely impossible, explain why

**NEVER skip directly to writing inline code without trying the script first.**

**📁 QC Thresholds by Cell Type:**

| Cell Type | min_genes | min_counts | max_mito_pct |
|-----------|-----------|------------|--------------|
| Primary neurons | 2000-3000 | 8000-10000 | 0.10-0.15 |
| iPSC-derived | 1500-2500 | 5000-8000 | 0.15-0.20 |
| Immune cells | 1000-1500 | 3000-5000 | 0.15-0.20 |
| Macrophages | 1000 | 3000-5000 | 0.18-0.20 |
| Cancer cell lines | 1500-2500 | 5000-8000 | 0.15-0.25 |

**See [references/qc_guidelines.md](references/qc_guidelines.md) for detailed thresholds.**

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| **Low sgRNA mapping rate (<30%)** | Poor capture efficiency, wrong mapping file | Check feature barcode library prep, verify sgRNA reference matches |
| **High doublet rate (>10%)** | High MOI, barcode collisions | Lower viral MOI in future screens, filter doublets computationally |
| **Target gene not DE** | Incomplete knockdown, ineffective sgRNA, compensation | Check sgRNA design, validate with protein, check for paralogs |
| **Low validation rate (<50%)** | Weak perturbations, wrong expected direction | Check CRISPRi vs CRISPRa, adjust log2fc threshold, check positive controls |
| **Memory errors** | Large dataset (>100k cells) | Process libraries separately, use backed mode (`adata = sc.read_h5ad('file.h5ad', backed='r')`) |
| **Inconsistent replicates** | Batch effects, population drift | Check batch balance, perform batch correction, analyze replicates separately first |
| **glmGamPoi fails** | R not installed, missing package | Install R ≥4.0 and glmGamPoi, or skip and use t-test results |
| **SVG export failed** | Missing SVG backend | **Normal — script falls back automatically. Both PNG and SVG attempted.** |

**See [references/troubleshooting_guide.md](references/troubleshooting_guide.md) for detailed solutions.**

## Suggested Next Steps

**After running this skill:**
1. **functional-enrichment-from-degs** - Pathway enrichment on hit perturbations
2. **coexpression-network** - Build gene regulatory networks from perturbed cells
3. **bulk-omics-clustering** - Cluster perturbations by transcriptional signature

**Related analyses:**
- Compare hit genes to GWAS loci (genetic-variant-annotation)
- Investigate heterogeneous responses (use Step 12 optional heterogeneity analysis in [references/statistical_methods.md](references/statistical_methods.md))

## Related Skills

- **functional-enrichment-from-degs** - Pathway enrichment on DE genes
- **de-results-to-plots** - Advanced visualization (heatmaps, custom plots)
- **coexpression-network** - Gene regulatory network inference
- **bulk-omics-clustering** - Cluster samples/perturbations by expression

## References

**Key Papers:**
- Dixit et al. (2016) "Perturb-Seq" *Cell* 167:1853-1866
- Datlinger et al. (2017) "Pooled CRISPR screening with single-cell readout" *Nature Methods* 14:297-301
- Papalexi et al. (2021) "Characterizing the molecular regulation of inhibitory immune checkpoints" *Nature Genetics* 53:322-331 *(example dataset)*
- Replogle et al. (2020) "Direct guide RNA capture" *Nature Biotechnology* 38:954-961
- Peidli et al. (2024) "scPerturb: harmonized single-cell perturbation data" *Nature Methods* 21:531-540 *(data source)*

**Online Resources:**
- 10X Feature Barcoding: https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/algorithms/crispr
- CROP-seq pipeline: https://github.com/argschwind/CROP-seq-pipeline
- Alector Perturb-seq analysis: https://github.com/Alector-BIO/CRISPR_PerturbSeq_pHM_publication

**See [references/crispr_screen_best_practices.md](references/crispr_screen_best_practices.md) for comprehensive guidelines.**
