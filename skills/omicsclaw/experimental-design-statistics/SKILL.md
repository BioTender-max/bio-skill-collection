---
id: experimental-design-statistics
name: Experimental Design
category: experimental_design
short-description: Design genomics experiments with power analysis, sample size estimation, batch design, and multiple testing correction.
detailed-description: Guide statistical experimental design for genomics studies including power analysis, sample size estimation, batch-balanced layouts, and multiple testing correction. Use when planning new experiments, justifying sample sizes for grants, optimizing budget constraints (depth vs. replicates), or designing batch structures. Supports RNA-seq, ATAC-seq, scRNA-seq, ChIP-seq, methylation, and proteomics. Includes pilot data-based power estimation, optimal batch assignment algorithms, and modern multiple testing methods (IHW, adaptive shrinkage). Best for pre-experiment planning with 4+ samples per group.
starting-prompt: Help me design a genomics experiment with power analysis and optimal batch assignment . .
---

# Experimental Design and Statistical Planning

Comprehensive workflow for statistical experimental design in genomics, from power analysis and sample size determination to batch-balanced experimental layouts and multiple testing strategy.

## When to Use This Skill

Use this skill when you need to:
- ✅ **Plan new experiments** - Design from scratch with statistical rigor
- ✅ **Justify sample sizes** - Calculate required replicates for grant proposals
- ✅ **Perform power analysis** - Determine statistical power for proposed designs
- ✅ **Design batch layouts** - Create balanced assignments preventing confounding
- ✅ **Optimize budgets** - Balance sequencing depth vs. number of replicates
- ✅ **Select correction methods** - Choose appropriate multiple testing approaches

**Don't use this skill for:**
- ❌ Post-experiment analysis → Use appropriate DE analysis skills
- ❌ Simple two-sample comparisons with fixed n → Use power calculators directly

**Key Concept:** Proper experimental design is the foundation of reproducible science. Good design prevents confounding, maximizes statistical power, and ensures results are interpretable.

## Installation

### Required Software

| Software | Version | License | Commercial Use | Installation |
|----------|---------|---------|----------------|--------------|
| DESeq2 | ≥1.30.0 | LGPL (≥3) | ✅ Permitted | `BiocManager::install('DESeq2')` |
| RNASeqPower | ≥1.30.0 | LGPL | ✅ Permitted | `BiocManager::install('RNASeqPower')` |
| ssizeRNA | ≥1.3.2 | GPL-2 | ✅ Permitted | `BiocManager::install('ssizeRNA')` |
| powsimR | ≥1.2.3 | GPL-3 | ✅ Permitted | `BiocManager::install('powsimR')` |
| IHW | ≥1.18.0 | Artistic-2.0 | ✅ Permitted | `BiocManager::install('IHW')` |
| osat | ≥1.38.0 | Artistic-2.0 | ✅ Permitted | `install.packages('osat')` |
| ggplot2 | ≥3.3.0 | MIT | ✅ Permitted | `install.packages('ggplot2')` |
| ggprism | ≥1.0.3 | GPL-3 | ✅ Permitted | `install.packages('ggprism')` |
| jsonlite | ≥1.7.0 | MIT | ✅ Permitted | `install.packages('jsonlite')` |
| pasilla | ≥1.18.0 | Artistic-2.0 | ✅ Permitted | `BiocManager::install('pasilla')` |

**Optional (for example data):**
- pasilla - Example RNA-seq pilot data for testing

**Quick install:**

```r
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install(c("DESeq2", "RNASeqPower", "ssizeRNA", "powsimR", "IHW", "pasilla"))
install.packages(c("osat", "ggplot2", "ggprism", "jsonlite"))
```

**License Compliance:** All packages use LGPL, GPL, Artistic-2.0, or MIT licenses that permit commercial use in AI agent applications.

**Full installation instructions and version details:** [references/software_requirements.md](references/software_requirements.md)

## Inputs

**Required:**
- **Experimental design info**: Assay type, n conditions, sample relationship, planned n
- **Effect size expectations**: Target fold change, variability (CV or pilot data)
- **Statistical requirements**: Target power (0.80/0.90), α (0.05), multiple testing preference

**Optional:**
- **Practical constraints**: Budget, sample availability, batch structure, sequencing depth, covariates

**Detailed input requirements:** [references/experimental_design_best_practices.md#input-requirements](references/experimental_design_best_practices.md#input-requirements)

## Outputs

**Power and sample size:**
- `power_analysis_results.csv` - Power calculations for scenarios
- `sample_size_recommendation.txt` - Required n with justification
- `power_vs_n_curve.png` + `.svg` - Power relationship visualizations

**Batch design:**
- `batch_layout_for_lab.csv` - Lab-ready sample-to-batch assignments
- `batch_design_validation.txt` - Confounding check results
- `batch_design_plot.png` + `.svg` - Visual layout

**Documentation:**
- `statistical_analysis_plan.md` - Complete pre-registration plan
- `lab_protocol_checklist.md` - Step-by-step processing guide
- `design_parameters.json` - All parameters (human-readable)

**Analysis objects (RDS) - For downstream use:**
- `batch_design.rds` - Complete batch design object
  - Load with: `batch_design <- readRDS('batch_design.rds')`
  - Required for: Batch effect correction workflows
- `design_parameters.rds` - Complete design parameters
  - Load with: `design_params <- readRDS('design_parameters.rds')`
  - Required for: Analysis validation, replication studies

## Clarification Questions

Before starting, gather the following information:

### 1. **Input Files** (ASK THIS FIRST):
   - Do you have pilot data or existing results files to inform the experimental design?
   - If uploaded: Are these pilot data files (DESeq2 objects, count matrices) you'd like to use for power calculations?
   - Expected formats: RDS (DESeqDataSet), CSV/TSV (count matrices)
   - **Or use literature-based estimates?** We can use tissue-specific variability values from published data ([references/cv_tissue_database.csv](references/cv_tissue_database.csv)).

### 2. **Assay Type**
- **Bulk RNA-seq**, **scRNA-seq**, **ATAC-seq**, **ChIP-seq**, **Methylation**, **Proteomics**, or **Other**

### 3. **Experimental Structure**
- **Conditions**: 2 (case-control), 3+ (multi-group), or factorial design?
- **Planned n**: Replicates per condition (or "unknown")
- **Sample type**: Independent, paired, or repeated measures
- **Covariates**: Variables to balance (sex, age, batch, site)

### 4. **Effect Size & Variability**
- **Target fold change**: Large (≥2x), moderate (1.5-2x), small (1.2-1.5x)
- **Pilot data**: Available? (Provide DESeq2 object, count matrix, or path)
- **No pilot data**: Will use tissue-specific CV from [references/cv_tissue_database.csv](references/cv_tissue_database.csv)

### 5. **Statistical Requirements**
- **Power**: 0.80 (standard), 0.90 (grants), or custom
- **Alpha (α)**: 0.05 (standard), 0.01 (stringent), or custom
- **Multiple testing**: BH-FDR (standard), IHW (more power), Bonferroni (stringent), or need guidance

### 6. **Practical Constraints**
- **Budget**: Maximum samples or runs
- **Sample availability**: Limited? Account for failures (add 10-20% buffer)?
- **Batch structure**: Processed in batches? Batch size?
- **Sequencing depth**: Target reads (RNA-seq: 15-30M, ATAC-seq: 25-50M, scRNA-seq: 50-100K/cell)

### 7. **Primary Objective**
- **Power analysis**, **sample size determination**, **batch design**, **multiple testing guidance**, **complete design**, or **budget optimization**

**Comprehensive clarification guide:** [references/experimental_design_best_practices.md#clarification-questions](references/experimental_design_best_practices.md#clarification-questions)

## Standard Workflow

> **Note:** Run from the OmicsClaw root directory and add the workflow scripts to `sys.path`:
> ```python
> import sys; import os; sys.path.insert(0, os.path.abspath('knowledge_base/scripts/experimental-design-statistics'))
> ```

🚨 **MANDATORY: USE SCRIPTS EXACTLY AS SHOWN - DO NOT WRITE INLINE CODE** 🚨

The experimental design workflow follows 4 steps: **Load** → **Calculate** → **Visualize** → **Export**

### **Step 1 - Load Parameters**

```r
source("scripts/load_example_data.R")
pilot_data <- load_example_data()
```

**With pilot data (preferred):**
- Uses `pilot_data$dds` for power calculations
- Uses `pilot_data$cv$median` for sample size estimation
- Provides realistic variability estimates

**Without pilot data (alternative):**
```r
source("scripts/load_example_data.R")
cv_db <- load_cv_database()
# Select appropriate tissue type from cv_db
```

**✅ VERIFICATION:** You MUST see: `"✓ Example pilot data loaded successfully!"`

**Decision:** Pilot data provides more accurate estimates. See [power_analysis_guidelines.md#pilot-vs-literature](references/power_analysis_guidelines.md#pilot-vs-literature)

---

### **Step 2 - Calculate Design**

🚨 **DO NOT write inline calculation code. Use the provided scripts.**

**A. Power Analysis** - Calculate power for your proposed design
```r
source("scripts/power_rnaseq.R")
power_result <- calc_power_rnaseq(
  depth = 20,
  n_per_group = 6,
  cv = pilot_data$cv$median,
  fold_change = 2,
  alpha = 0.05
)
```
**DO NOT write inline power calculation code. Just source the script and call the function.**

**B. Sample Size Determination** - Calculate required n from pilot data
```r
source("scripts/sample_size_de.R")
required_n <- samplesize_from_pilot(
  pilot_dds = pilot_data$dds,
  fold_change = 1.5,
  power = 0.8,
  fdr = 0.05
)
```
**DO NOT write inline sample size code. Use the function from the script.**

**C. Batch Assignment** - Generate balanced batch layout
```r
source("scripts/batch_assignment.R")
batch_design <- assign_samples_to_batches(
  metadata = pilot_data$metadata,
  batch_size = 8,
  balance_vars = c("condition", "sex")
)
```
**DO NOT manually create batch assignments. Use the OSAT-optimized function.**

⚠️ **CRITICAL - DO NOT:**
- ❌ Write inline power calculation code → **STOP: Use calc_power_rnaseq()**
- ❌ Write inline plotting code (ggsave, ggplot, etc.) → **STOP: Use visualization scripts**
- ❌ Manually assign samples to batches → **STOP: Use assign_samples_to_batches()**
- ❌ Write custom balancing algorithms → **STOP: Script uses OSAT's optimal algorithms**
- ❌ Try to install svglite → scripts handle SVG fallback automatically

**⚠️ IF SCRIPTS FAIL - Script Failure Hierarchy:**
1. **Fix and Retry (90%)** - Install missing package, re-run script
2. **Modify Script (5%)** - Edit the script file itself, document changes
3. **Use as Reference (4%)** - Read script, adapt approach, cite source
4. **Write from Scratch (1%)** - Only if genuinely impossible, explain why

**NEVER skip directly to writing inline code without trying the script first.**

**✅ VERIFICATION:** You should see:
- After power analysis: `"✓ Power analysis completed successfully!"`
- After sample size: `"✓ Sample size calculation completed successfully!"`
- After batch design: `"✓ Batch design generated successfully!"`

**CRITICAL RULE:** Batch must NEVER confound with condition. See [batch_effect_mitigation.md#cardinal-rule](references/batch_effect_mitigation.md#cardinal-rule)

**Decision points:**
- Power ≥0.80? If not, increase n or adjust expectations. See [power_analysis_guidelines.md#interpreting-power](references/power_analysis_guidelines.md#interpreting-power)
- Required n exceed budget? See [budget optimization](references/experimental_design_best_practices.md#budget-optimization)
- Confounding detected? Regenerate with different constraints. See [batch_effect_mitigation.md#troubleshooting](references/batch_effect_mitigation.md#troubleshooting)

---

### **Step 3 - Visualize Design**

**A. Generate power curves:**
```r
source("scripts/plot_power_curves.R")
plot_power_vs_samplesize(
  cv = pilot_data$cv$median,
  fold_changes = c(1.5, 2, 3),
  depth = 20,
  output_file = "design_results/power_vs_n"
)
```

**B. Validate and visualize batch design:**
```r
source("scripts/batch_validation.R")
confounding_check <- check_confounding(batch_design, "condition")
visualize_batch_design(
  batch_design,
  condition_var = "condition",
  output_file = "design_results/batch_design"
)
```

🚨 **DO NOT write inline plotting code (ggsave, ggplot, etc.). Use the visualization scripts.** 🚨

**The scripts handle PNG + SVG export with graceful fallback for SVG dependencies.**

**✅ VERIFICATION:** You should see:
- `"Saving power curve plots:"` followed by PNG + SVG file paths
- `"PASS: No confounding detected"` or `"WARNING: Batch is CONFOUNDED"`
- `"Saving batch design plots:"` followed by PNG + SVG file paths

**Output formats:** Always generates both PNG (for presentations) and SVG (for publications) with graceful fallback.

---

### **Step 4 - Export All Results**

```r
source("scripts/export_design.R")
export_complete_design(batch_design, design_params, output_dir = "design_results")
```

**DO NOT write custom export code. Use export_complete_design().**

**✅ VERIFICATION:** You MUST see: `"=== Export Complete ==="`

This will generate:
1. `batch_layout_for_lab.csv` - Lab-ready sample assignments
2. `statistical_analysis_plan.md` - Pre-registration analysis plan
3. `lab_protocol_checklist.md` - Lab processing checklist
4. `batch_design.rds` - Batch design object (for downstream use)
5. `design_parameters.rds` - Design parameters (for downstream use)
6. `design_parameters.json` - Design parameters (human-readable)

**RDS objects are CRITICAL** for downstream workflows and validation studies.

---

### **Complete Workflow Example**

For a complete experimental design with all steps:

```r
# Step 1: Load pilot data
source("scripts/load_example_data.R")
pilot_data <- load_example_data()

# Step 2: Calculate design parameters
source("scripts/power_rnaseq.R")
source("scripts/sample_size_de.R")
source("scripts/batch_assignment.R")

power_result <- calc_power_rnaseq(depth = 20, n_per_group = 6, cv = 0.4, fold_change = 2)
required_n <- samplesize_from_pilot(pilot_data$dds, fold_change = 1.5, power = 0.8)
batch_design <- assign_samples_to_batches(pilot_data$metadata, batch_size = 8,
                                          balance_vars = c("condition"))

# Step 3: Visualize and validate
source("scripts/plot_power_curves.R")
source("scripts/batch_validation.R")

plot_power_vs_samplesize(cv = 0.4, fold_changes = c(1.5, 2, 3),
                         output_file = "design_results/power_vs_n")
check_confounding(batch_design, "condition")
visualize_batch_design(batch_design, "condition", output_file = "design_results/batch_design")

# Step 4: Export all results
source("scripts/export_design.R")
design_params <- list(assay = "RNA-seq", conditions = c("control", "treated"),
                     n_per_group = 6, power = 0.85, alpha = 0.05,
                     effect_size = 2, multiple_testing = "BH-FDR")
export_complete_design(batch_design, design_params, output_dir = "design_results")
```

**Note:** Specific parameters depend on your experimental requirements (see Clarification Questions).

## Decision Guide

**Three critical decisions:**
- **Pilot vs Literature:** Use pilot data if available (more accurate). Literature CV acceptable as fallback.
- **Sample Size vs Depth:** Prioritize more samples over deeper sequencing for DE. 15-20M reads sufficient for RNA-seq.
- **Multiple Testing:** BH-FDR (standard), IHW (more power), Bonferroni (stringent).

**See:** [experimental_design_best_practices.md#decision-guide](references/experimental_design_best_practices.md#decision-guide) for comprehensive guidance and common usage patterns (power analysis only, batch design only, budget optimization).

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Power <0.80 with max budget | Effect size too small or CV too high | Increase n, increase depth, or revise effect size expectations. See [references/power_analysis_guidelines.md#low-power](references/power_analysis_guidelines.md#low-power) |
| Batch confounding detected | Unequal condition distribution across batches | Regenerate with stricter balance constraints or adjust batch size. See [references/batch_effect_mitigation.md#troubleshooting](references/batch_effect_mitigation.md#troubleshooting) |
| Required n exceeds sample availability | Pilot data shows high variability or small effect | Consider paired design, blocking by major covariates, or revise target fold-change. See [references/experimental_design_best_practices.md#budget-optimization](references/experimental_design_best_practices.md#budget-optimization) |
| Can't balance all covariates | Too many variables for batch size | Prioritize key covariates (condition > sex > age > others). Some minor imbalance acceptable. See [references/batch_effect_mitigation.md#covariate-priority](references/batch_effect_mitigation.md#covariate-priority) |
| CV estimate varies widely | Pilot data has outliers or low counts | Filter low-count genes (mean <10) before CV calculation. Use median, not mean CV. See [references/power_analysis_guidelines.md#cv-estimation](references/power_analysis_guidelines.md#cv-estimation) |
| Power calculations give n<3 | Very large effect size or low variability | Warning: n<3 too low for valid inference. Plan for minimum n=3-4 even if calculations suggest n=2 |
| Multiple testing correction too stringent | Many tests, low discovery rate | Consider IHW (more powerful than BH-FDR) or independent filtering. See [references/multiple_testing_guide.md#choosing](references/multiple_testing_guide.md#choosing) |

**Detailed troubleshooting:** [references/troubleshooting_guide.md](references/troubleshooting_guide.md)

## Suggested Next Steps

After completing experimental design:

1. **Execute Experiment** - Use batch assignment file to guide sample processing
2. **Perform DE Analysis** - Use bulk-rnaseq-counts-to-de-deseq2, scrnaseq-scanpy-core-analysis, or appropriate skill
3. **Apply Multiple Testing** - Use pre-specified correction method from statistical plan
4. **Validate Results** - Check batch effects were controlled, verify power calculations

## Related Skills

**Upstream:** None - this is typically the first step in a project

**Downstream (after data collection):**
- **bulk-rnaseq-counts-to-de-deseq2** - Differential expression analysis
- **functional-enrichment-from-degs** - Pathway analysis
- **de-results-to-plots** - Visualization

**Alternative/complementary:**
- **bulk-omics-clustering** - Discover natural groupings post-hoc
- **batch-correction-combat** - Computational batch correction if needed

## References

**Detailed documentation:**
- [references/experimental_design_best_practices.md](references/experimental_design_best_practices.md) - General design principles, decision guide, common patterns
- [references/power_analysis_guidelines.md](references/power_analysis_guidelines.md) - Detailed power calculation methods, pilot vs literature
- [references/batch_effect_mitigation.md](references/batch_effect_mitigation.md) - Preventing/controlling batch effects, cardinal rule, troubleshooting
- [references/multiple_testing_guide.md](references/multiple_testing_guide.md) - Choosing correction methods
- [references/qc_guidelines.md](references/qc_guidelines.md) - Quality control checkpoints
- [references/troubleshooting_guide.md](references/troubleshooting_guide.md) - Common problems and solutions
- [references/software_requirements.md](references/software_requirements.md) - Installation and licenses
- [references/cv_tissue_database.csv](references/cv_tissue_database.csv) - Tissue-specific variability estimates

**Scripts:** See scripts/ directory for all analysis functions:
- Data loading: [load_example_data.R](knowledge_base/scripts/experimental-design-statistics/load_example_data.R)
- Power/sample size: [power_rnaseq.R](knowledge_base/scripts/experimental-design-statistics/power_rnaseq.R), [power_atacseq.R](knowledge_base/scripts/experimental-design-statistics/power_atacseq.R), [sample_size_de.R](knowledge_base/scripts/experimental-design-statistics/sample_size_de.R), [sample_size_scrna.R](knowledge_base/scripts/experimental-design-statistics/sample_size_scrna.R)
- Batch design: [batch_assignment.R](knowledge_base/scripts/experimental-design-statistics/batch_assignment.R), [batch_validation.R](knowledge_base/scripts/experimental-design-statistics/batch_validation.R)
- Visualization: [plot_power_curves.R](knowledge_base/scripts/experimental-design-statistics/plot_power_curves.R)
- Export: [export_design.R](knowledge_base/scripts/experimental-design-statistics/export_design.R) (includes RDS saving)

**Key Papers:**
- Hart SN et al. (2013) *J Comput Biol* 20(12):970-978 - RNA-seq sample size
- Schurch NJ et al. (2016) *RNA* 22(6):839-851 - Biological replicates needed
- Leek JT et al. (2010) *Nat Rev Genet* 11(10):733-739 - Batch effects impact
- Benjamini & Hochberg (1995) *J R Stat Soc Series B* 57(1):289-300 - FDR control
- Love MI et al. (2014) *Genome Biol* 15(12):550 - DESeq2 methods
