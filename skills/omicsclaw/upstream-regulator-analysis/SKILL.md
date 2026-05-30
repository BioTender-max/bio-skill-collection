---
id: upstream-regulator-analysis
name: Upstream Regulator Analysis
category: multi_omics
short-description: "Integrate ChIP-Atlas TF binding data with RNA-seq differential expression to identify upstream regulators driving transcriptomic changes."
detailed-description: "Identifies transcription factors driving differential expression by integrating ChIP-Atlas peak enrichment (433,000+ public ChIP-seq experiments) with RNA-seq DE results. Submits DE gene lists to ChIP-Atlas API, downloads target gene lists for top enriched TFs, computes Fisher's exact test for target-DE overlap, measures directional concordance (activator vs repressor), and ranks TFs by a combined regulatory score. Supports 10 genomes including human (hg38, hg19), mouse (mm10, mm9), rat (rn6), and model organisms."
starting-prompt: Identify upstream regulators driving my differential expression results using ChIP-Atlas binding data . .
---

# Upstream Regulator Analysis

Identify transcription factors (TFs) driving observed differential expression by integrating **ChIP-Atlas TF binding data** (epigenomics) with **RNA-seq DE results** (transcriptomics). Ranks TFs by a combined regulatory score incorporating binding enrichment, target-DE overlap (Fisher's exact test), and directional concordance (activator vs repressor).

## When to Use This Skill

**Use when you:**
- Have DE results and want to identify TFs driving expression changes
- Need to go beyond simple gene list enrichment to mechanistic TF-level evidence
- Want to distinguish **activators** (targets upregulated) from **repressors** (targets downregulated)
- Want to integrate epigenomics (ChIP-seq) with transcriptomics (RNA-seq) in one analysis

**Don't use for:**
- Single-cell DE results (designed for bulk RNA-seq DE)
- Organisms not in ChIP-Atlas (see supported genomes below)
- Histone mark analysis (use `chip-atlas-peak-enrichment` directly)
- When you only need TF binding enrichment without target gene integration

**Requires:** Internet access (ChIP-Atlas API + data server). Runtime: **15-25 minutes** (API polling + target gene downloads).

## Installation

```bash
pip install pandas numpy scipy requests matplotlib seaborn reportlab
```

| Package | Version | License | Commercial Use |
|---------|---------|---------|----------------|
| pandas | ≥1.5 | BSD-3 | ✅ Permitted |
| numpy | ≥1.21 | BSD-3 | ✅ Permitted |
| scipy | ≥1.9 | BSD-3 | ✅ Permitted |
| requests | ≥2.28 | Apache-2.0 | ✅ Permitted |
| matplotlib | ≥3.6 | PSF | ✅ Permitted |
| seaborn | ≥0.12 | BSD-3 | ✅ Permitted |
| reportlab | ≥3.6 | BSD | ✅ Permitted |

**Sibling skill dependencies:** Requires `chip-atlas-peak-enrichment` and `chip-atlas-target-genes` directories at the same level.

## Inputs

- **DE results CSV/TSV** with columns: gene symbol, log2 fold change, adjusted p-value
  - Supports DESeq2 (`log2FoldChange`, `padj`), edgeR (`logFC`, `FDR`), limma (`logFC`, `adj.P.Val`)
  - Column names auto-detected; override with parameters if needed
- **Genome:** hg38, hg19, mm10, mm9, rn6, dm6, dm3, ce11, ce10, sacCer3

## Outputs

**Analysis objects:**
- `analysis_object.pkl` - Complete analysis for downstream use
  - Load with: `import pickle; obj = pickle.load(open('analysis_object.pkl', 'rb'))`
  - Contains: regulon_scores, enrichment results, target gene data, DE data, parameters

**CSV results:**
- `regulon_scores_all.csv` - All scored TFs with regulatory score, Fisher's p-value, concordance, direction
- `regulon_scores_top.csv` - Top 20 TFs
- `target_overlaps.csv` - Per-TF target gene overlap with DE status (up/down)
- `enrichment_up.csv` / `enrichment_down.csv` - ChIP-Atlas peak enrichment results

**Visualizations (PNG + SVG):**
- `upstream_regulators_top_regulators` - Bar chart: TFs ranked by regulatory score
- `upstream_regulators_target_overlap` - Stacked bar: TF targets classified as up/down/unchanged
- `upstream_regulators_evidence_scatter` - Scatter: ChIP enrichment vs Fisher significance
- `upstream_regulators_heatmap` - Clustermap: TFs × regulatory evidence metrics

**Reports:**
- `summary_report.md` - Human-readable analysis summary
- `analysis_report.pdf` - Publication-quality PDF with Introduction, Methods, Results, Conclusions
  - Requires: `pip install reportlab` (optional — markdown report generated regardless)

## Clarification Questions

1. **Input Files** (ASK THIS FIRST):
   - Do you have DE results (CSV/TSV) to analyze?
   - If uploaded: Is this the DE results file you'd like to find upstream regulators for?
   - Expected columns: gene symbol + log2FoldChange + adjusted p-value
   - **Or use example data?** Three options:
     - a) **Estrogen/MCF7 dataset** (recommended) — real DE results from GSE51403 (estradiol-treated MCF7 breast cancer cells, ~58K genes). Expected top regulator: ESR1
     - b) **Airway dataset** — real DE results from GSE52778 (dexamethasone-treated airway smooth muscle cells, ~58K genes). Expected top regulator: NR3C1
     - c) Synthetic TP53-driven data (~200 genes, fast, offline)

2. **Analysis Options:**
   - *(If using example data)* Choose analysis parameters:
     - a) Standard analysis (top 10 TFs, q < 0.05) (recommended)
     - b) Comprehensive analysis (top 15 TFs, q < 0.1)
   - *(If using your own data)* What species/genome?
     - a) Human (hg38)
     - b) Human (hg19)
     - c) Mouse (mm10)
     - d) Other (specify)

## Standard Workflow

> **Note:** Run from the OmicsClaw root directory and add the workflow scripts to `sys.path`:
> ```python
> import sys; import os; sys.path.insert(0, os.path.abspath('knowledge_base/scripts/upstream-regulator-analysis'))
> ```

🚨 **MANDATORY: USE SCRIPTS EXACTLY AS SHOWN - DO NOT WRITE INLINE CODE** 🚨

**Step 1 - Load data:**
```python
# For example data (real estrogen/MCF7 dataset, downloads from EBI Expression Atlas):
from load_example_data import load_example_data
de_data = load_example_data(source="estrogen")

# Alternative: airway dataset (dexamethasone, real data):
de_data = load_example_data(source="airway")

# For synthetic data (offline, fast, TP53-driven):
de_data = load_example_data(source="synthetic")

# For user data:
from load_de_results import load_de_results
de_data = load_de_results("path/to/de_results.csv")
```
**✅ VERIFICATION:** `"✓ Data loaded successfully: N total genes, M DE genes (X up, Y down)"`

**Step 2 - Run integration analysis:**
```python
from run_integration_workflow import run_integration_workflow
results = run_integration_workflow(de_data, genome="hg38", output_dir="regulator_results")
```
**DO NOT write inline API code or custom scoring. Just call the workflow function.**

⏱️ **This step takes 15-25 minutes** (ChIP-Atlas API polling + target gene downloads).

**✅ VERIFICATION:** `"✓ Integration analysis completed successfully!"`

**Step 3 - Generate visualizations:**
```python
from generate_all_plots import generate_all_plots
generate_all_plots(results, output_dir="regulator_results")
```
🚨 **DO NOT write inline plotting code (ggplot, ggsave, etc.). Just use the script.** 🚨

**✅ VERIFICATION:** `"✓ All visualizations generated successfully!"`

**Step 4 - Export results:**
```python
from export_all import export_all
export_all(results, output_dir="regulator_results")
```
**DO NOT write custom export code. Use export_all().**

**✅ VERIFICATION:** `"=== Export Complete ==="`

⚠️ **CRITICAL - DO NOT:**
- ❌ **Write inline API code** → **STOP: Use `run_integration_workflow()`**
- ❌ **Write inline plotting code** → **STOP: Use `generate_all_plots()`**
- ❌ **Write custom export code** → **STOP: Use `export_all()`**
- ❌ **Write custom Fisher's test code** → **STOP: Built into `score_regulons()`**

**⚠️ IF SCRIPTS FAIL - Script Failure Hierarchy:**
1. **Fix and Retry (90%)** - Install missing package, re-run script
2. **Modify Script (5%)** - Edit the script file itself, document changes
3. **Use as Reference (4%)** - Read script, adapt approach, cite source
4. **Write from Scratch (1%)** - Only if genuinely impossible, explain why

**NEVER skip directly to writing inline code without trying the script first.**

## Common Issues

| Error | Cause | Solution |
|-------|-------|----------|
| **ImportError: sibling skill not found** | Missing chip-atlas-peak-enrichment or chip-atlas-target-genes | Ensure both sibling skills are installed at the same directory level |
| **API 400 error** | Empty cellClass or invalid parameters | Use `cell_class="All cell types"` (must be non-empty) |
| **Both enrichment analyses failed** | Too few DE genes per direction | Need ≥3 genes in at least one direction (up or down) |
| **No TFs passed enrichment threshold** | Stringent cutoff or few DE genes | Try `min_enrichment_qvalue=0.1` or add more DE genes |
| **Target gene download timeout** | Large TF file or slow connection | Script retries; if persistent, reduce `max_tfs` |
| **No TFs with target gene data** | Enriched TFs are histone marks | Filter with `antigen_class="TFs and others"` (default) |
| **SVG export failed** | Missing svglite/cairo | Normal - PNG always generated; SVG is optional |

## Interpretation Guidelines

### Regulatory Score
Combined evidence: `-log10(Fisher P) × Concordance × -log10(ChIP Q)`

| Score | Evidence |
|-------|----------|
| >100 | Very strong — high ChIP enrichment + significant target overlap + high concordance |
| 50-100 | Strong |
| 20-50 | Moderate |
| <20 | Weak — interpret with caution |

### Direction Classification
- **Activator** (concordance >60%, majority up): TF likely activates these genes
- **Repressor** (concordance >60%, majority down): TF likely represses these genes
- **Mixed** (concordance ≤60%): No clear directional bias — context-dependent regulation

### Key Caveats
- Results biased toward well-studied TFs/cell types in ChIP-Atlas
- Binding enrichment ≠ regulatory causation (validate with perturbation)
- Directional labels assume simple activation/repression (ignores context-dependent regulation)
- Combined score is a heuristic ranking, not a formal multi-test correction
- Fisher's test assumes independence (may be violated if targets cluster in pathways)

## Suggested Next Steps

After identifying upstream regulators:
- **Validate binding:** Use `chip-atlas-target-genes` to examine cell-type-specific binding patterns for top TFs
- **Functional enrichment:** Use `functional-enrichment-from-degs` on TF-target gene subsets
- **Co-expression:** Use `gene-correlation-archs4` to check if TF and targets co-express
- **Network inference:** Use `grn-pyscenic` for single-cell GRN validation
- **Literature review:** Use `literature-review` to validate TF-disease associations

## Related Skills

- `chip-atlas-peak-enrichment` - Component: TF binding enrichment analysis
- `chip-atlas-target-genes` - Component: TF target gene retrieval
- `bulk-rnaseq-counts-to-de-deseq2` - Upstream: generates DE results input
- `de-results-to-gene-lists` - Upstream: generates filtered gene lists
- `functional-enrichment-from-degs` - Complementary: pathway-level enrichment

## References

- Zou Z, et al. (2024) ChIP-Atlas 3.0: a gene regulation data-mining platform. *Nucleic Acids Res.* 52(W1):W159-W166
- Oki S, et al. (2018) ChIP-Atlas: a data-mining suite. *EMBO Rep.* 19(12):e46255
- Fisher RA (1922) On the interpretation of chi-squared. *J R Stat Soc.* 85(1):87-94
