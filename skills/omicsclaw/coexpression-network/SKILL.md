---
id: coexpression-network
name: Weighted Gene Co-expression Network Analysis (WGCNA)
category: transcriptomics
short-description: Build gene co-expression networks to identify modules and hub genes from RNA-seq data.
detailed-description: |
  Performs weighted gene co-expression network analysis (WGCNA) to identify modules of coordinately
  expressed genes and hub genes within those modules. Takes normalized RNA-seq count matrices,
  constructs scale-free co-expression networks, detects modules using hierarchical clustering,
  correlates modules with sample traits, and identifies hub genes. Best for: finding gene regulatory
  networks, identifying key genes driving biological processes, relating gene groups to phenotypes.
  Requires ≥15 samples (20+ recommended) and 5,000-15,000 most variable genes.
starting-prompt: Build a co-expression network to identify gene modules and hub genes from my RNA-seq data . .
---

# Weighted Gene Co-expression Network Analysis (WGCNA)

## Overview

Build weighted gene co-expression networks to identify modules of coordinately expressed genes and discover hub genes that may be key regulators. This workflow uses WGCNA (Weighted Gene Co-expression Network Analysis) to group genes into modules based on their expression patterns across samples, then correlates these modules with experimental conditions or traits.

**Key Concept:** Unlike single-gene analysis, WGCNA identifies groups of genes that behave similarly across samples, revealing biological pathways and potential regulatory relationships.

**Use Cases:**
- Identify gene modules associated with experimental conditions
- Discover hub genes (highly connected genes within modules)
- Find genes with similar expression patterns to known genes of interest
- Reduce dimensionality of gene expression data for downstream analysis
- Generate hypotheses about gene function based on co-expression

**Default Prompt:** "Build a co-expression network to identify gene modules and hub genes from my RNA-seq data"

## When to Use This Skill

Use WGCNA when you want to:

- **Identify gene modules** associated with experimental conditions or phenotypes
- **Discover hub genes** that are highly connected within modules and may be key regulators
- **Find co-expressed genes** with similar expression patterns to known genes of interest
- **Reduce dimensionality** of large gene expression datasets for downstream analysis
- **Generate hypotheses** about gene function based on co-expression patterns

**Requirements:**
- ≥15 samples (20+ recommended for robust results)
- Normalized expression data (VST, rlog, TPM, or FPKM - NOT raw counts)
- 5,000-15,000 most variable genes
- Batch effects removed or corrected

**Not suitable for:**
- Small sample sizes (<15 samples) - consider alternative approaches
- Raw count data - normalize first using DESeq2 or similar
- Data with uncorrected batch effects - correct before WGCNA

---

## Installation

**Core WGCNA packages:**
```r
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install("WGCNA")
```

**Visualization packages:**
```r
install.packages(c("ggplot2", "ggprism"))
BiocManager::install("ComplexHeatmap")
```

**Enrichment analysis (optional):**
```r
BiocManager::install(c("clusterProfiler", "org.Hs.eg.db"))  # Human
# BiocManager::install("org.Mm.eg.db")  # Mouse
# BiocManager::install("org.Rn.eg.db")  # Rat
```

| Software | Version | License | Commercial Use | Installation |
|----------|---------|---------|----------------|--------------|
| WGCNA | ≥1.70 | GPL-2+ | ✅ Permitted | `BiocManager::install('WGCNA')` |
| ggplot2 | ≥3.3.0 | MIT | ✅ Permitted | `install.packages('ggplot2')` |
| ComplexHeatmap | ≥2.10.0 | MIT | ✅ Permitted | `BiocManager::install('ComplexHeatmap')` |
| clusterProfiler | ≥4.0.0 | Artistic-2.0 | ✅ Permitted | `BiocManager::install('clusterProfiler')` |

---

## Inputs

**Required:**
1. **Normalized expression matrix** (CSV/TSV):
   - Rows: Genes, Columns: Samples
   - Values: VST, rlog, TPM, or FPKM (NOT raw counts)
   - 5,000-15,000 most variable genes recommended

2. **Sample metadata** (CSV/TSV):
   - Sample IDs matching expression matrix columns
   - Traits/conditions for module-trait correlation

**Optional:**
- Differential expression results (to highlight DEGs)
- Gene annotations for enrichment analysis

**Data Requirements:**
- ≥15 samples (20+ recommended)
- Batch effects removed or corrected
- No missing values in expression matrix

---

## Outputs

**CSV Files:**
1. **`wgcna_gene_modules.csv`** - Gene-module assignments with connectivity metrics
2. **`wgcna_hub_genes.csv`** - Top hub genes per module
3. **`wgcna_module_trait_cor.csv`** - Module-trait correlations with p-values
4. **`wgcna_eigengenes.csv`** - Module eigengene values per sample
5. **`wgcna_report.md`** - Summary report with interpretation

**Plots (PNG + SVG):**
6. **`soft_power_selection.png/.svg`** - Power selection diagnostic plot
7. **`module_dendrogram.png/.svg`** - Gene dendrogram with module colors
8. **`module_trait_correlation.png/.svg`** - Module-trait heatmap
9. **`eigengene_heatmap.png/.svg`** - Module eigengene expression patterns
10. **`hub_genes_barplot.png/.svg`** - Hub genes by connectivity

**Analysis Objects (RDS):**
11. **`wgcna_network.rds`** - Complete network object from blockwiseModules
    - Load with: `net <- readRDS('wgcna_network.rds')`
    - Required for: module preservation analysis, advanced network visualization
12. **`wgcna_module_colors.rds`** - Module color assignments per gene
    - Load with: `colors <- readRDS('wgcna_module_colors.rds')`
    - Required for: downstream module-specific analyses
13. **`wgcna_expression_matrix.rds`** - Filtered expression matrix used for analysis
    - Load with: `expr <- readRDS('wgcna_expression_matrix.rds')`
    - Required for: reanalysis, module preservation testing
14. **`wgcna_full_results.rds`** - Complete results object with all components
    - Load with: `results <- readRDS('wgcna_full_results.rds')`
    - Required for: replotting, additional analyses

**Key Metrics:**
- `module`: Module color assignment (grey = unassigned)
- `kWithin`: Intramodular connectivity (higher = more connected)
- `MM`: Module membership (correlation with eigengene)
- `hub_score`: Combined connectivity metric (MM × kWithin)

---

## Clarification Questions

1. **Input Files** (ASK THIS FIRST):
   - Do you have specific normalized expression data and sample metadata files to analyze?
   - If uploaded: Are these the expression matrix and metadata you'd like to analyze?
   - Expected formats: CSV or TSV with genes as rows, samples as columns
   - **Or use example data?** Female mouse liver dataset (135 samples, liver tissue, multiple traits)

2. **What is your normalized expression data format?**
   - VST (variance stabilizing transformation) from DESeq2
   - rlog (regularized log) from DESeq2
   - TPM (transcripts per million)
   - FPKM/RPKM
   - If unsure or raw counts: normalize first using DESeq2

3. **How many samples do you have?**
   - 15-30 samples (minimum for WGCNA, results may be less robust)
   - 30-50 samples (good power for network detection)
   - 50+ samples (excellent power, most reliable results)

4. **What traits/conditions do you want to correlate with modules?**
   - Treatment vs control (binary)
   - Disease status or phenotype
   - Continuous variables (age, dose, time, weight)
   - Multiple traits (all will be tested)

5. **Gene filtering strategy?**
   - Top 5,000 most variable genes (default, recommended)
   - Top 10,000-15,000 genes (for larger datasets)
   - All genes passing expression threshold
   - Pre-filtered gene list (e.g., from DE analysis)

---

## Standard Workflow

> **Note:** Run from the OmicsClaw root directory and add the workflow scripts to `sys.path`:
> ```python
> import sys; import os; sys.path.insert(0, os.path.abspath('knowledge_base/scripts/coexpression-network'))
> ```

🚨 **MANDATORY: USE SCRIPTS EXACTLY AS SHOWN - DO NOT WRITE INLINE CODE** 🚨

**Step 1 - Load data:**
```r
library(WGCNA)
allowWGCNAThreads()

source("scripts/load_example_data.R")
wgcna_data <- load_example_wgcna_data()
datExpr <- wgcna_data$datExpr
meta <- wgcna_data$meta

# For your own data:
# source("scripts/prepare_wgcna_data.R")
# data <- prepare_wgcna_data("expression.csv", "metadata.csv", top_n_genes = 5000)
# datExpr <- data$datExpr
# meta <- data$meta
```

**Step 2 - Run WGCNA analysis:**
```r
source("scripts/wgcna_workflow.R")
results <- run_wgcna_analysis(
  datExpr,
  meta,
  traits = c("weight_g", "Glucose_mg_dl"),  # Adjust to your traits
  organism = "mouse"  # or "human", "rat", or NULL to skip enrichment
)
```
**DO NOT write inline WGCNA code. Just source the script.**

**Step 3 - Generate visualizations:**
```r
source("scripts/plot_all_wgcna.R")
plot_all_wgcna(results, output_dir = "wgcna_results")
```
🚨 **DO NOT write inline plotting code (png, svg, plotDendroAndColors, etc.). Just use the script.** 🚨

**The script handles PNG + SVG export with graceful fallback for SVG dependencies.**

**Step 4 - Export results:**
```r
source("scripts/export_wgcna_results.R")
export_all(results, output_dir = "wgcna_results")
```
**DO NOT write custom export code. Use export_all().**

**✅ VERIFICATION - You should see:**
- After Step 1: `"✓ Successfully loaded female mouse liver dataset"`
- After Step 2: `"✓ WGCNA analysis completed successfully!"`
- After Step 3: `"✓ All WGCNA plots generated successfully!"`
- After Step 4: `"=== Export Complete ==="`

⚠️ **CRITICAL - DO NOT:**
- ❌ **Write inline WGCNA code** → **STOP: Use `source("scripts/wgcna_workflow.R")`**
- ❌ **Write inline plotting code (png, svg, plotDendroAndColors, etc.)** → **STOP: Use `plot_all_wgcna()`**
- ❌ **Write custom export code** → **STOP: Use `export_all()`**
- ❌ **Try to install svglite** → script handles SVG fallback automatically
- ❌ Use absolute paths like `/mnt/knowhow/` → use relative paths `scripts/`
- ❌ Skip soft power selection → required for scale-free topology
- ❌ Use raw counts → normalize first with DESeq2 VST or rlog

**⚠️ IF SCRIPTS FAIL - Script Failure Hierarchy:**
1. **Fix and Retry (90%)** - Install missing package, re-run script
2. **Modify Script (5%)** - Edit the script file itself, document changes
3. **Use as Reference (4%)** - Read script, adapt approach, cite source
4. **Write from Scratch (1%)** - Only if genuinely impossible, explain why

**NEVER skip directly to writing inline code without trying the script first.**

**What the scripts provide:**
- [scripts/load_example_data.R](knowledge_base/scripts/coexpression-network/load_example_data.R) - Auto-fetch tutorial data (~135 samples)
- [scripts/prepare_wgcna_data.R](knowledge_base/scripts/coexpression-network/prepare_wgcna_data.R) - Load and filter your data
- [scripts/wgcna_workflow.R](knowledge_base/scripts/coexpression-network/wgcna_workflow.R) - Complete WGCNA analysis (power selection, network building, module-trait correlation, hub genes, enrichment)
- [scripts/plot_all_wgcna.R](knowledge_base/scripts/coexpression-network/plot_all_wgcna.R) - All publication-quality plots (PNG + SVG)
- [scripts/plotting_helpers.R](knowledge_base/scripts/coexpression-network/plotting_helpers.R) - Plot saving functions **with automatic SVG fallback handling**
- [scripts/export_wgcna_results.R](knowledge_base/scripts/coexpression-network/export_wgcna_results.R) - Export results and analysis objects

---

## Parameter Customization

**When customization is needed:**

- **Soft power selection:** Read [references/parameter-tuning-guide.md](references/parameter-tuning-guide.md) to understand how to choose appropriate power values for your data
- **Module detection parameters:** See [references/parameter-tuning-guide.md#module-detection](references/parameter-tuning-guide.md) for guidance on min_module_size and merge_cut_height
- **Complete custom workflow:** Read [references/wgcna-reference.md](references/wgcna-reference.md) for detailed code examples with explanations (only if you need full control)

---

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Too few samples error | <15 samples | WGCNA requires ≥15 samples; combine replicates or use alternative methods |
| Scale-free R² never exceeds 0.75 | Batch effects or poor data quality | Check for batch effects; try different normalization; inspect PCA |
| All genes assigned to grey module | minModuleSize too large or poor gene filtering | Lower minModuleSize to 20-30; increase top_n_genes to 10,000-15,000 |
| No significant module-trait correlations | Weak biological signal or incorrect traits | Check trait coding (numeric for continuous, 0/1 for binary); try more samples |
| Soft power recommended is very high (>20) | Data not suitable for scale-free network | Check normalization; consider signed vs unsigned network |
| Hub gene identification fails | Module colors not provided correctly | Ensure module_colors matches gene order in datExpr |
| Enrichment analysis returns no results | Wrong organism or gene ID format | Verify organism parameter matches data; convert gene IDs if needed |
| Memory errors during network construction | Too many genes | Reduce to 5,000-10,000 most variable genes; increase RAM |

---

## Interpretation Guidelines

**Module colors:**
- Each color = distinct co-expression module
- **Grey** = genes not assigned to any module
- Larger modules may represent broader biological processes

**Hub genes:**
- High `kWithin` = highly connected within module
- High `MM` = strong correlation with module eigengene
- Hub genes are candidates for experimental validation

**Module-trait correlations:**
- **|r| > 0.5 and p < 0.05** = significant association
- Positive correlation = module genes increase with trait
- Negative correlation = module genes decrease with trait
- Focus on modules with strongest associations

---

## Suggested Next Steps

After identifying modules and hub genes:

1. **Functional validation** - Validate hub genes experimentally (qPCR, knockdown, overexpression)
2. **Enrichment analysis** - Test modules for GO/KEGG enrichment to understand biological processes
3. **Compare with DE results** - Overlay DE genes on network to see which modules are enriched
4. **Network visualization** - Export to Cytoscape for detailed network visualization
5. **Cross-dataset validation** - Test module preservation in independent datasets

---

## Related Skills

- **[bulk-rnaseq-counts-to-de-deseq2](../bulk-rnaseq-counts-to-de-deseq2/)** - Normalize counts and perform differential expression analysis (run before WGCNA)
- **[de-results-to-gene-lists](../de-results-to-gene-lists/)** - Extract gene lists from DE results to overlay on network
- **[functional-enrichment-from-degs](../functional-enrichment-from-degs/)** - Perform GO/KEGG enrichment on modules

---

## References

**Documentation:**
- [WGCNA Best Practices Guide](references/wgcna-best-practices.md) - Comprehensive guide on data preparation, QC, and troubleshooting
- [Parameter Tuning Guide](references/parameter-tuning-guide.md) - Detailed parameter selection guidance
- [WGCNA Reference](references/wgcna-reference.md) - Complete code examples with explanations
- [Troubleshooting Guide](references/troubleshooting.md) - Common errors and solutions

**Example Data:**
- [Example Datasets](assets/eval/datasets/example_datasets.md) - Public datasets for WGCNA analysis

**Key Papers:**
- [Key WGCNA Papers](assets/eval/papers/key_papers.md) - Essential publications
- Langfelder & Horvath (2008). WGCNA: an R package for weighted correlation network analysis. *BMC Bioinformatics*. doi:10.1186/1471-2105-9-559
- Zhang & Horvath (2005). A general framework for weighted gene co-expression network analysis. *Statistical Applications in Genetics and Molecular Biology*. doi:10.2202/1544-6115.1128
