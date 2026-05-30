---
id: polygenic-risk-score-prs-catalog
name: Polygenic Risk Score (PGS Catalog)
category: genomics_genetics
short-description: "Calculate polygenic risk scores using pre-computed weights from the PGS Catalog for single or multiple traits with population comparisons."
detailed-description: "Apply pre-computed polygenic risk score (PRS) weights from the PGS Catalog to target genotypes. Supports multi-trait scoring (e.g., cardiometabolic risk panel), population-stratified comparisons across 5 super-populations using 1000 Genomes Phase 3, and combined risk dashboards with correlation matrices and composite risk rankings. No GWAS summary statistics or LD computation needed — uses peer-reviewed, published scoring weights from 5,000+ available traits."
starting-prompt: Calculate polygenic risk scores for cardiometabolic traits using the PGS Catalog with 1000 Genomes example data . .
---

# Polygenic Risk Score (PGS Catalog)

## When to Use This Skill

- **You have a trait of interest** and want to calculate PRS using published, peer-reviewed weights
- **Multi-trait risk profiling** (e.g., cardiometabolic panel: CAD, T2D, LDL, BMI, blood pressure)
- **Population comparisons** of genetic risk across ancestry groups
- **No GWAS summary statistics needed** — uses pre-computed weights from PGS Catalog
- **Quick PRS** — minutes per trait (download + score), no LD computation required

**For de novo PRS from raw GWAS summary statistics**, use the `polygenic-risk-score` skill (LDpred2-auto) instead.

## Installation

```r
install.packages(c("data.table", "ggplot2", "ggprism", "dplyr", "R.utils", "jsonlite", "remotes"))
remotes::install_github("privefl/bigsnpr")
```

| Software | Version | License | Commercial Use | Install |
|----------|---------|---------|----------------|---------|
| bigsnpr | ≥1.12 | GPL-3 | ✅ Permitted | `remotes::install_github("privefl/bigsnpr")` |
| data.table | ≥1.14 | MPL-2.0 | ✅ Permitted | `install.packages('data.table')` |
| ggplot2 | ≥3.4 | MIT | ✅ Permitted | `install.packages('ggplot2')` |
| ggprism | ≥1.0.3 | GPL (≥3) | ✅ Permitted | `install.packages('ggprism')` |
| dplyr | ≥1.1 | MIT | ✅ Permitted | `install.packages('dplyr')` |
| jsonlite | ≥1.8 | MIT | ✅ Permitted | `install.packages('jsonlite')` |
| R.utils | ≥2.12 | LGPL (≥2.1) | ✅ Permitted | `install.packages('R.utils')` |

## Inputs

- **Target genotypes:** PLINK binary format (.bed/.bim/.fam) — or use 1000 Genomes Phase 3 example data (2,490 individuals, 5 super-populations)
- **PGS Catalog score IDs:** One or more PGS IDs (e.g., `PGS000018` for CAD) — use `search_pgs_catalog()` to discover available scores
- **Genome build:** GRCh37 (default, matches 1000 Genomes) or GRCh38

## Outputs

**Per-trait files:**
- `prs_scores_<trait>.csv` — Individual PRS (z-scores, percentiles, population labels)
- `distribution_<trait>.png/svg` — PRS distribution histogram
- `population_<trait>.png/svg` — PRS by super-population boxplot

**Combined files:**
- `combined_prs_scores.csv` — All individuals x all traits (wide format) + composite risk
- `prs_correlation_matrix.csv` — Trait-trait PRS correlation matrix
- `population_summary.csv` — Mean PRS by super-population per trait
- `match_reports.csv` — Variant matching summary per trait

**Dashboard plots:**
- `dashboard_correlation_matrix.png/svg` — Heatmap of trait PRS correlations
- `dashboard_composite_risk.png/svg` — Composite risk distribution by population
- `dashboard_population_heatmap.png/svg` — Mean PRS by trait x super-population

**Analysis objects (RDS):**
- `prs_analysis.rds` — Complete analysis object for downstream use
  - Load with: `obj <- readRDS('prs_analysis.rds')`
  - Contains: combined_scores, per_trait, cor_matrix, match_reports, snp_weights, trait_info

## Clarification Questions

1. **Input Data** (ASK THIS FIRST):
   - Do you have specific genotype files (.bed/.bim/.fam) to score?
   - **Or use 1000 Genomes Phase 3 example data?** (2,490 individuals, 26 populations, 5 super-populations)

2. **Traits to Score:**
   - *(If using example data)* The demo scores 5 cardiometabolic traits (CAD, T2D, LDL, BMI, SBP). Choose analysis mode:
     - a) Full cardiometabolic panel — all 5 traits (recommended)
     - b) Select specific traits from the panel
   - *(If using your own data)* What traits do you want to score? Use `search_pgs_catalog("trait name")` to find PGS IDs.

3. **Analysis Options:**
   - a) Standard analysis with dashboard (recommended)
   - b) Individual trait scoring only (no dashboard)

## Standard Workflow

> **Note:** Run from the OmicsClaw root directory and add the workflow scripts to `sys.path`:
> ```python
> import sys; import os; sys.path.insert(0, os.path.abspath('knowledge_base/scripts/polygenic-risk-score-prs-catalog'))
> ```

🚨 **MANDATORY: USE SCRIPTS EXACTLY AS SHOWN - DO NOT WRITE INLINE CODE** 🚨

**Step 1 - Load reference genotypes and PGS weights:**
```r
source("scripts/load_reference_data.R")
ref_data <- load_reference_data()

source("scripts/load_pgs_weights.R")
trait_weights <- load_demo_weights()
```
**DO NOT write custom download or parsing code. Use the scripts.**

**Step 2 - Score all traits:**
```r
source("scripts/score_traits.R")
```
**DO NOT write inline scoring code (big_prodVec, allele matching, etc.). Just source the script.**

**Step 3 - Generate visualizations:**
```r
source("scripts/generate_plots.R")
generate_all_plots(all_results, output_dir = "results")
```
🚨 **DO NOT write inline plotting code (ggsave, ggplot, geom_tile, etc.). Just use the script.** 🚨

**The script handles PNG + SVG export with graceful fallback for SVG dependencies.**

**Step 4 - Export results:**
```r
source("scripts/export_results.R")
export_all(all_results, output_dir = "results")
```
**DO NOT write custom export code. Use export_all().**

**✅ VERIFICATION - You should see:**
- After Step 1: `"✓ Reference data loaded successfully"` and `"✓ PGS Catalog weights loaded: 5/5 traits"`
- After Step 2: `"✓ Multi-trait PRS scoring completed successfully! (5 traits, 2490 individuals)"`
- After Step 3: `"✓ All plots generated successfully!"`
- After Step 4: `"=== Export Complete ==="`

**❌ IF YOU DON'T SEE THESE:** You wrote inline code. Stop and use source().

⚠️ **CRITICAL - DO NOT:**
- ❌ **Write inline scoring code** → **STOP: Use `source("scripts/score_traits.R")`**
- ❌ **Write inline plotting code (ggsave, ggplot, etc.)** → **STOP: Use `generate_all_plots()`**
- ❌ **Write custom export code** → **STOP: Use `export_all()`**
- ❌ **Try to install svglite** → script handles SVG fallback automatically

**⚠️ IF SCRIPTS FAIL - Script Failure Hierarchy:**
1. **Fix and Retry (90%)** — Install missing package, re-run script
2. **Modify Script (5%)** — Edit the script file itself, document changes
3. **Use as Reference (4%)** — Read script, adapt approach, cite source
4. **Write from Scratch (1%)** — Only if genuinely impossible, explain why

**NEVER skip directly to writing inline code without trying the script first.**

## Scoring Custom Traits

To score a single custom trait instead of the demo panel:
```r
source("scripts/load_reference_data.R")
ref_data <- load_reference_data()

source("scripts/load_pgs_weights.R")
# Search for available scores
scores <- search_pgs_catalog("your trait name")
# Download specific score
trait_weights <- list()
tw <- download_pgs_weights("PGS_ID_HERE")
trait_weights[["TRAIT"]] <- list(
    weights = tw$weights, pgs_id = tw$pgs_id, score_meta = tw$score_meta,
    trait_name = "Your Trait", short_name = "TRAIT"
)

# Then continue with Steps 2-4 as above
source("scripts/score_traits.R")
```

## Common Issues

| Error | Cause | Solution |
|-------|-------|----------|
| **"bigsnpr not found"** | **Missing core dependency** | **`remotes::install_github("privefl/bigsnpr")`** |
| **Download timeout** | **Large scoring file or slow connection** | **Set `options(timeout = 900)` before running Step 1** |
| **Low match rate (<50%)** | **Genome build mismatch** | **Ensure PGS weights and genotypes use same build (GRCh37 for 1000G)** |
| **PGS ID not found** | **Wrong or deprecated PGS ID** | **Use `search_pgs_catalog("trait")` to find valid IDs** |
| **SVG export error** | **Missing optional dependency** | **`generate_all_plots()` handles fallback automatically. DO NOT install svglite manually.** |
| **"catalog_data not found"** | **Wrong script for this skill** | **Use `score_traits.R` (not `pgs_catalog_scoring.R` from the LDpred2 skill)** |
| **Memory error during scoring** | **Very large scoring file** | **Normal for genome-wide scores. Ensure ≥8GB RAM available.** |

## Suggested Next Steps

After completing multi-trait PRS:
1. **Downstream analysis** — Load `prs_analysis.rds` for custom analyses
2. **Additional traits** — Add more PGS scores to expand the risk panel
3. **De novo PRS** — Use `polygenic-risk-score` skill for traits without PGS Catalog scores
4. **GWAS interpretation** — Pair with functional annotation skills

## Related Skills

- `polygenic-risk-score` — De novo PRS using LDpred2-auto (requires GWAS summary statistics)
- `eqtl-colocalization-coloc` — Colocalization of GWAS signals with eQTLs

## References

1. Lambert SA, et al. (2021). The Polygenic Score Catalog as an open database for reproducibility and systematic evaluation. *Nature Genetics*, 53(4), 420-425.
2. 1000 Genomes Project Consortium (2015). A global reference for human genetic variation. *Nature*, 526(7571), 68-74.
3. Privé F, et al. (2022). Portability of 245 polygenic scores when derived from the UK Biobank and applied to 9 ancestry groups from the same cohort. *AJHG*, 109(1), 12-23.
4. Khera AV, et al. (2018). Genome-wide polygenic scores for common diseases identify individuals with risk equivalent to monogenic mutations. *Nature Genetics*, 50(9), 1219-1224.
5. PGS Catalog: https://www.pgscatalog.org/
