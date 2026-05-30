---
id: functional-enrichment-from-degs
name: Functional Enrichment Analysis (GSEA + ORA)
category: functional_analysis
short-description: Perform functional enrichment analysis using clusterProfiler on differential expression results with GSEA and ORA.
detailed-description: Perform functional enrichment analysis using clusterProfiler on differential expression results with GSEA and ORA. Use when you have DE results with log2 fold changes and want to identify enriched biological pathways, GO terms, or gene sets. Supports MSigDB (Hallmark, KEGG, Reactome, GO), human and mouse data. GSEA (default, uses all ranked genes) detects coordinated pathway changes without arbitrary cutoffs. ORA (optional, uses significant gene lists) provides intuitive validation. Best for exploratory pathway analysis after DE testing.
starting-prompt: Perform functional enrichment analysis on my differential expression results . . 
---

# Functional Enrichment Analysis

Translate differential expression results into biological insights using GSEA and ORA.

## When to Use This Skill

Use this skill **after completing differential expression analysis** to identify enriched pathways and biological processes.

**Use when:**
- ✅ You have DE results with fold changes and p-values
- ✅ Want to answer: "What pathways or processes are affected?"
- ✅ Need to interpret gene lists in biological context
- ✅ Preparing results for publication or validation

**Two complementary methods:** GSEA (primary, uses all ranked genes, detects coordinated changes) and ORA (secondary, uses significant gene list, validates GSEA). **Default recommendation:** Run GSEA unless user specifically requests ORA or has only a gene list (no fold changes).

**See [references/gsea_ora_comparison.md](references/gsea_ora_comparison.md) for detailed method comparison.**

## Quick Start (Example Data)

**Test this skill with real DE results in ~2 minutes:**

```r
# Load example DE results from airway dataset (dexamethasone treatment)
source("scripts/load_example_data.R")
de_results <- load_airway_de_results()  # Auto-installs packages (~1-2 min, ~40MB)

# Load required packages and scripts
library(clusterProfiler)
library(msigdbr)
source("scripts/prepare_gene_lists.R")
source("scripts/get_msigdb_genesets.R")
source("scripts/run_gsea.R")
source("scripts/generate_plots.R")
source("scripts/export_results.R")

# Run GSEA workflow
ranked_genes <- create_ranked_list(de_results)
term2gene <- get_msigdb_genesets("human", c("H"))  # Hallmark pathways only for speed
gsea_result <- run_gsea(ranked_genes, term2gene, n_perm = 1000)
generate_all_plots(gsea_result)
export_all(gsea_result, ranked_genes, output_prefix = "quick_test")
```

**What you get:**
- **Dataset:** Human airway smooth muscle cells, dexamethasone treatment vs untreated
- **Expected results:** ~5-10 significant Hallmark pathways (Inflammatory Response, TNF-alpha signaling, Interferon response)
- **Outputs:** CSV results, SVG/PNG plots, RDS objects, markdown summary

**For your own data:** Replace example data loading with your DE results file (see [Inputs](#inputs) section).

## Installation

```r
# Install Bioconductor packages
if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install(c("clusterProfiler", "enrichplot", "org.Hs.eg.db"))

# Install CRAN packages
install.packages(c("msigdbr", "ggplot2", "ggrepel", "dplyr"))
```

### Software Requirements

| Package | Version | License | Commercial Use | Installation |
|---------|---------|---------|----------------|--------------|
| clusterProfiler | ≥4.0 | Artistic-2.0 | ✅ Permitted | `BiocManager::install("clusterProfiler")` |
| enrichplot | ≥1.12 | Artistic-2.0 | ✅ Permitted | `BiocManager::install("enrichplot")` |
| msigdbr | ≥7.4 | MIT | ✅ Permitted | `install.packages("msigdbr")` |
| org.Hs.eg.db | Latest | Artistic-2.0 | ✅ Permitted | `BiocManager::install("org.Hs.eg.db")` |
| org.Mm.eg.db | Latest | Artistic-2.0 | ✅ Permitted | `BiocManager::install("org.Mm.eg.db")` |
| ggplot2 | ≥3.3 | MIT | ✅ Permitted | `install.packages("ggplot2")` |
| ggrepel | ≥0.9 | GPL-3 | ✅ Permitted | `install.packages("ggrepel")` |
| dplyr | ≥1.0 | MIT | ✅ Permitted | `install.packages("dplyr")` |

### Database Licenses

**⚠️ KEGG requires commercial license for commercial use.** MSigDB and GO use CC-BY 4.0 (commercial use permitted with attribution). For commercial applications, use Hallmark, Reactome, or GO databases, or obtain appropriate KEGG license.

## Inputs

**Required:**
- **Differential expression results** with:
  - Gene identifiers (HGNC symbols preferred)
  - Log2 fold change values (for GSEA ranking)
  - Adjusted p-values (for ORA filtering)
  - Optional: Test statistics for optimal GSEA ranking

**Supported DE methods:**
- DESeq2 results (padj, log2FoldChange, stat)
- edgeR results (FDR, logFC, logCPM)
- limma results (adj.P.Val, logFC, t)

**File formats:**
- CSV/TSV files with DE results
- R data frames or result objects

**Species support:**
- Human (default)
- Mouse
- Other species via custom gene sets

## Outputs

**Primary results (CSV):**
- `enrichment_gsea_results.csv` - All GSEA results (NES, p-value, FDR, leading edge genes)
- `enrichment_ora_up_results.csv` - Enriched pathways in upregulated genes (if ORA run)
- `enrichment_ora_down_results.csv` - Enriched pathways in downregulated genes (if ORA run)

**Visualizations (PNG + SVG):**
- `gsea_dotplot.png` / `.svg` - Activated/suppressed pathways visualization
- `gsea_running_score.png` / `.svg` - Running enrichment score plots for top pathways
- `ora_up_barplot.png` / `.svg` - Bar plot for upregulated pathways (if ORA run)
- `ora_down_barplot.png` / `.svg` - Bar plot for downregulated pathways (if ORA run)

**Analysis objects (RDS):**
- `enrichment_gsea_result.rds` - Complete GSEA enrichResult object for downstream use
  - Load with: `gsea_result <- readRDS('enrichment_gsea_result.rds')`
  - Required for: pathway visualization tools, network analysis, downstream enrichment
- `enrichment_ora_up_result.rds` - ORA enrichResult for upregulated genes (if run)
- `enrichment_ora_down_result.rds` - ORA enrichResult for downregulated genes (if run)
- `enrichment_ranked_genes.rds` - Ranked gene list used for GSEA
  - Load with: `ranked_genes <- readRDS('enrichment_ranked_genes.rds')`

**Summary:**
- `enrichment_summary.md` - Text summary of top findings with interpretation

## Clarification Questions

**Default settings (use unless user specifies otherwise):**
- Method: GSEA
- Databases: Hallmark + KEGG
- Species: Human
- ORA thresholds: padj ≤ 0.05, |log2FC| ≥ 1 (only if running ORA)

**⚠️ CRITICAL: Always ask question #1 first to check if user has provided input files before proceeding with analysis.**

**Questions to ask only if ambiguous:**
1. **Input Files** (ASK THIS FIRST):
   - **Do you have specific differential expression results file(s) to analyze?**
     - If uploaded: Is this the DE results file (with log2 fold changes and p-values) you'd like to use?
     - Expected formats: CSV/TSV with gene, log2FoldChange, padj/FDR columns
   - **Or use example data for testing?**
     - Use `source("scripts/load_example_data.R"); de_results <- load_airway_de_results()`
     - Human airway dataset: dexamethasone treatment (~60k genes, ~1-2 min to generate)

2. **Method:** GSEA (default with full DE results), ORA (gene list only), or Both (validation)
3. **Databases:** Hallmark + KEGG (default exploratory), GO:BP (detailed processes), Reactome (alternative to KEGG), C6/C7 (cancer/immunology)
4. **Species:** Human (default) or Mouse

**See [references/decision-guide.md](references/decision-guide.md) for detailed decision guidance.**

## Standard Workflow

> **Note:** Run from the OmicsClaw root directory and add the workflow scripts to `sys.path`:
> ```python
> import sys; import os; sys.path.insert(0, os.path.abspath('knowledge_base/scripts/functional-enrichment-from-degs'))
> ```

🚨 **MANDATORY: USE SCRIPTS EXACTLY AS SHOWN - DO NOT WRITE INLINE CODE** 🚨

**CRITICAL: Use relative paths (knowledge_base/scripts/functional-enrichment-from-degs/). DO NOT construct absolute paths.**

These scripts provide robust, validated enrichment analysis. Use them as-is for standard GSEA workflows.

**Step 1 - Load data:**
```r
# Load all required scripts
source("scripts/load_de_results.R")
source("scripts/prepare_gene_lists.R")
source("scripts/get_msigdb_genesets.R")
source("scripts/run_gsea.R")
source("scripts/generate_plots.R")
source("scripts/export_results.R")

# Load your DE results
de_results <- load_de_results("your_de_results.csv")  # Replace with your file path

# Prepare inputs
ranked_genes <- create_ranked_list(de_results)
term2gene <- get_msigdb_genesets("human", c("H", "C2:CP:KEGG"))
```
**DO NOT write inline data loading code. Just use the scripts.**

**Step 2 - Run analysis:**
```r
gsea_result <- run_gsea(ranked_genes, term2gene)
```
**DO NOT write inline GSEA code. Just use run_gsea().**

**Step 3 - Generate visualizations:**
```r
generate_all_plots(gsea_result)
```
🚨 **DO NOT write inline plotting code (ggsave, dotplot, etc.). Just use generate_all_plots().** 🚨

**The script handles PNG + SVG export with graceful fallback for SVG dependencies.**

**Step 4 - Export results:**
```r
export_all(gsea_result, ranked_genes, output_prefix = "enrichment")
```
**DO NOT write custom export code. Use export_all().**

**✅ VERIFICATION - You should see:**
- After Step 1: `"✓ Data loaded successfully"`
- After Step 2: `"✓ Analysis completed successfully!"`
- After Step 3: `"✓ All plots generated successfully!"`
- After Step 4: `"=== Export Complete ==="`

**❌ IF YOU DON'T SEE THESE:** You wrote inline code. Stop and use the scripts.

⚠️ **CRITICAL - DO NOT:**
- ❌ **Write inline enrichment code** → **STOP: Use `run_gsea()`**
- ❌ **Write inline plotting code (ggsave, dotplot, gseaplot2, etc.)** → **STOP: Use `generate_all_plots()`**
- ❌ **Write custom export code** → **STOP: Use `export_all()`**
- ❌ **Use absolute paths** like `/mnt/knowhow/` → use relative paths `scripts/`
- ❌ **Skip the background parameter in ORA** → causes inflated p-values
- ❌ **Try to install svglite** → script handles SVG fallback automatically

**⚠️ IF SCRIPTS FAIL - Script Failure Hierarchy:**
1. **Fix and Retry (90%)** - Install missing package, re-run script
2. **Modify Script (5%)** - Edit the script file itself, document changes
3. **Use as Reference (4%)** - Read script, adapt approach, cite source
4. **Write from Scratch (1%)** - Only if genuinely impossible, explain why

**NEVER skip directly to writing inline code without trying the script first.**

**When customization is needed:**
- **Databases, ranking metrics, thresholds:** Read [references/decision-guide.md](references/decision-guide.md) to understand options and adapt to your specific analysis goals
- **Complete custom workflow:** See [references/method-reference.md](references/method-reference.md) for step-by-step inline examples (only if user explicitly requests full customization)
- **Adding ORA validation:** See Pattern 2 in [Common Patterns](#common-patterns) section below

**What the scripts provide:**
- [scripts/load_de_results.R](knowledge_base/scripts/functional-enrichment-from-degs/load_de_results.R) - Standardizes DE results from DESeq2/edgeR/limma
- [scripts/load_example_data.R](knowledge_base/scripts/functional-enrichment-from-degs/load_example_data.R) - Loads example datasets for testing
- [scripts/prepare_gene_lists.R](knowledge_base/scripts/functional-enrichment-from-degs/prepare_gene_lists.R) - Creates ranked lists (GSEA) and filtered lists (ORA)
- [scripts/get_msigdb_genesets.R](knowledge_base/scripts/functional-enrichment-from-degs/get_msigdb_genesets.R) - Retrieves MSigDB gene sets (Hallmark, KEGG, Reactome, GO)
- [scripts/run_gsea.R](knowledge_base/scripts/functional-enrichment-from-degs/run_gsea.R) - Runs GSEA with sensible defaults
- [scripts/run_ora.R](knowledge_base/scripts/functional-enrichment-from-degs/run_ora.R) - Runs ORA for up/downregulated genes
- [scripts/generate_plots.R](knowledge_base/scripts/functional-enrichment-from-degs/generate_plots.R) - Creates publication-quality PNG + SVG plots **with automatic SVG fallback handling**
- [scripts/export_results.R](knowledge_base/scripts/functional-enrichment-from-degs/export_results.R) - Exports CSV results, RDS objects, and markdown summaries

## Decision Guide

**Key decisions during analysis:**

1. **Method selection (before analysis):** GSEA only (default, full DE results), ORA only (gene list without fold changes), or Both (validation)

2. **Database selection (Step 3):** Hallmark + KEGG (default exploratory), GO:BP (detailed processes), Reactome (KEGG alternative, commercial-friendly), or C6/C7 (cancer/immunology)

3. **Ranking metric (Step 2):** Test statistic (best, balances effect + significance), signed -log10(pvalue) (good alternative), or log2FC only (not recommended)

**For detailed decision guidance with options and recommendations, see [references/decision-guide.md](references/decision-guide.md).**

## Common Patterns

**For all patterns and advanced examples, see [references/method-reference.md](references/method-reference.md).**

### Pattern 1: Quick GSEA with Default Settings

```r
# Load required scripts
source("scripts/load_de_results.R")
source("scripts/prepare_gene_lists.R")
source("scripts/get_msigdb_genesets.R")
source("scripts/run_gsea.R")
source("scripts/generate_plots.R")
source("scripts/export_results.R")

# Load, prepare, and run GSEA
de_results <- load_de_results("de_results.csv")
ranked_genes <- create_ranked_list(de_results)
term2gene <- get_msigdb_genesets("human", c("H", "C2:CP:KEGG"))
gsea_result <- run_gsea(ranked_genes, term2gene)
generate_all_plots(gsea_result)
export_all(gsea_result, ranked_genes, output_prefix = "enrichment")
```

### Pattern 2: GSEA + ORA for Validation

```r
# Load required scripts
source("scripts/load_de_results.R")
source("scripts/prepare_gene_lists.R")
source("scripts/get_msigdb_genesets.R")
source("scripts/run_gsea.R")
source("scripts/run_ora.R")
source("scripts/generate_plots.R")
source("scripts/export_results.R")

# Prepare inputs and run both methods
de_results <- load_de_results("de_results.csv")
ranked_genes <- create_ranked_list(de_results)
sig_genes <- filter_significant_genes(de_results)
term2gene <- get_msigdb_genesets("human", c("H", "C2:CP:KEGG"))
gsea_result <- run_gsea(ranked_genes, term2gene)
ora_up <- run_ora(sig_genes$up, term2gene, sig_genes$background, direction = "upregulated")
ora_down <- run_ora(sig_genes$down, term2gene, sig_genes$background, direction = "downregulated")
generate_all_plots(gsea_result)
generate_ora_barplot(ora_up, "Upregulated")
generate_ora_barplot(ora_down, "Downregulated")
export_all(gsea_result, ora_up, ora_down, ranked_genes, output_prefix = "enrichment")
```

**For results interpretation guidance, see [references/interpretation_guidelines.md](references/interpretation_guidelines.md).**

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| No significant GSEA results | Weak signal, wrong ranking, small gene sets | Try larger databases (GO:BP), verify ranking metric, check DE results quality |
| No significant ORA results | Thresholds too stringent, wrong gene symbols | Relax thresholds (padj < 0.1), verify gene symbols match database |
| Gene symbols not recognized | Wrong species, non-standard IDs | Ensure using official HGNC/MGI symbols, verify species matches database |
| Memory issues with large gene sets | Too many gene sets (e.g., all GO terms) | Reduce `max_size` parameter, use fewer databases, filter gene sets |
| Slow GSEA execution | High permutations, many gene sets | Reduce `n_perm` to 1000 for testing, use fewer gene sets |
| Different results between GSEA and ORA | Methods use different information | Normal - GSEA uses all genes, ORA uses cutoff. Check for agreement in top pathways |
| **SVG export error "svglite required"** | **Missing optional dependency** | **Use `generate_all_plots()` - it handles fallback automatically. DO NOT try to install svglite manually.** |
| **svglite dependency conflict** | **System library version mismatch** | **Normal - `generate_all_plots()` falls back to base R svg() device automatically. Both PNG and SVG will be created.** |

## Suggested Next Steps

After completing functional enrichment analysis:

### 1. Interpret and Validate Results
Check if enriched pathways align with experimental hypothesis and are biologically coherent. Examine leading edge genes and compare with literature. **See [references/interpretation_guidelines.md](references/interpretation_guidelines.md) for detailed guidance.**

### 2. Create Additional Visualizations
Generate optional advanced plots: enrichment maps (pathway networks), concept networks (gene-pathway connections), or ridge plots (expression distributions). **Use [scripts/generate_plots.R](knowledge_base/scripts/functional-enrichment-from-degs/generate_plots.R).**

### 3. Deep Dive on Key Pathways
Examine leading edge genes in top pathways, check individual gene expression in original DE results, and look up pathway diagrams in KEGG/Reactome databases.

### 4. Export for Publications
Use CSV results for supplementary tables, SVG plots for figures (300+ DPI), and include enrichment summary in results section. Document database versions, parameters, and software versions in methods.

## Related Skills

**Prerequisites (run before this skill):**
- **bulk-rnaseq-counts-to-de-deseq2** - DESeq2 differential expression analysis, generates required DE results
- **de-results-to-gene-lists** - Filters and annotates DE results, prepares gene lists

**Complementary (run alongside):**
- **de-results-to-plots** - Visualize DE results before enrichment to understand expression patterns

**Downstream:**
- Pathway visualization tools - Coming soon
- Network analysis of enriched pathways - Coming soon
- Integration with other omics data - Coming soon

## References

### Primary Citations

1. **clusterProfiler:** Yu G, et al. (2012) clusterProfiler: an R package for comparing biological themes among gene clusters. OMICS. DOI: 10.1089/omi.2011.0118

2. **GSEA method:** Subramanian A, et al. (2005) Gene set enrichment analysis: A knowledge-based approach for interpreting genome-wide expression profiles. PNAS. DOI: 10.1073/pnas.0506580102

3. **MSigDB:** Liberzon A, et al. (2015) The Molecular Signatures Database Hallmark Gene Set Collection. Cell Systems. DOI: 10.1016/j.cels.2015.12.004

4. **Method benchmarking:** Geistlinger L, et al. (2021) Toward a gold standard for benchmarking gene set enrichment analysis. Brief Bioinform. DOI: 10.1093/bib/bbz158

### Additional Resources

**Detailed documentation:**
- [references/gsea_ora_comparison.md](references/gsea_ora_comparison.md) - Comprehensive GSEA vs ORA comparison
- [references/database_guide.md](references/database_guide.md) - Gene set database selection guide
- [references/interpretation_guidelines.md](references/interpretation_guidelines.md) - Results interpretation guide
- [references/gsea_ora_validation_framework.md](references/gsea_ora_validation_framework.md) - Validation framework

**Scripts:**
- [scripts/load_de_results.R](knowledge_base/scripts/functional-enrichment-from-degs/load_de_results.R) - Load and standardize DE results
- [scripts/prepare_gene_lists.R](knowledge_base/scripts/functional-enrichment-from-degs/prepare_gene_lists.R) - Create ranked/filtered gene lists
- [scripts/get_msigdb_genesets.R](knowledge_base/scripts/functional-enrichment-from-degs/get_msigdb_genesets.R) - Retrieve MSigDB gene sets
- [scripts/run_gsea.R](knowledge_base/scripts/functional-enrichment-from-degs/run_gsea.R) - Execute GSEA
- [scripts/run_ora.R](knowledge_base/scripts/functional-enrichment-from-degs/run_ora.R) - Execute ORA
- [scripts/generate_plots.R](knowledge_base/scripts/functional-enrichment-from-degs/generate_plots.R) - Visualization functions
- [scripts/export_results.R](knowledge_base/scripts/functional-enrichment-from-degs/export_results.R) - Export results and summaries

**Evaluation:**
- [assets/eval/](assets/eval/) - Evaluation test cases and benchmarking materials
