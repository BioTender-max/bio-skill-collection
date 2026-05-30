---
id: cell-cell-communication
name: Cell-Cell Communication Analysis (CellChat)
category: transcriptomics
short-description: "Infer and visualize cell-cell communication networks from scRNA-seq data using CellChat v2 ligand-receptor interaction analysis."
detailed-description: "Analyze intercellular communication from annotated single-cell RNA-seq data using CellChat v2. Infers ligand-receptor interactions between cell populations, builds communication probability networks, computes signaling pathway activity, and identifies dominant sender/receiver/mediator roles. Generates chord diagrams, network plots, bubble plots, and signaling role heatmaps. Accepts Seurat objects directly — chains from scrnaseq-seurat-core-analysis."
starting-prompt: Analyze cell-cell communication from my scRNA-seq data using CellChat to identify ligand-receptor interactions and signaling networks between cell types.
---

# Cell-Cell Communication Analysis (CellChat v2)

## When to Use This Skill

✅ **Use when:**
- You have an annotated scRNA-seq dataset (Seurat object with cell type labels)
- You want to identify ligand-receptor interactions between cell types
- You want to visualize communication networks (chord diagrams, bubble plots)
- You want to find dominant sender/receiver cell populations
- **Chains from** `scrnaseq-seurat-core-analysis` output (`seurat_processed.rds`)

❌ **Don't use when:**
- Data is not annotated (run `scrnaseq-seurat-core-analysis` first)
- You need spatial cell-cell communication (CellChat v2 supports this but requires spatial coordinates)
- You want gene regulatory networks (use `grn-pyscenic` instead)
- You have bulk RNA-seq data

## Installation

| Package | Version | License | Commercial Use | Installation |
|---------|---------|---------|----------------|--------------|
| CellChat | ≥2.0.0 | GPL-3 | ✅ Permitted | `devtools::install_github("jinworks/CellChat")` |
| Seurat | ≥5.0.0 | MIT | ✅ Permitted | `install.packages('Seurat')` |
| SeuratData | ≥0.2.1 | GPL-3 | ✅ Permitted | `devtools::install_github('satijalab/seurat-data')` |
| NMF | ≥0.23.0 | GPL-2+ | ✅ Permitted | `install.packages('NMF')` |
| circlize | ≥0.4.12 | MIT | ✅ Permitted | `install.packages('circlize')` |
| ComplexHeatmap | ≥2.12.0 | MIT | ✅ Permitted | `BiocManager::install('ComplexHeatmap')` |
| ggprism | ≥1.0.3 | GPL-3 | ✅ Permitted | `install.packages('ggprism')` |
| presto | ≥1.0.0 | GPL-3 | ✅ Permitted | `remotes::install_github('immunogenomics/presto')` |
| ggalluvial | ≥0.12.0 | GPL-2 | ✅ Permitted | `install.packages('ggalluvial')` |
| rmarkdown | ≥2.20 | GPL-3 | ✅ Permitted | `install.packages('rmarkdown')` |

⚠️ **CellChat must be installed from GitHub** (not CRAN). Use the **jinworks** repository (active), not sqjin (archived).

## Inputs

**Required:**
- **Seurat object (.rds)** with:
  - Normalized expression data (`@assays$RNA@data`)
  - Cell type annotations in metadata (e.g., `celltype` column)
  - Minimum 3 cell types, ≥10 cells per type recommended

**Accepted sources:**
- `seurat_processed.rds` from `scrnaseq-seurat-core-analysis` (chains directly)
- Any annotated Seurat v5 object
- Example PBMC data (auto-loaded if no file provided)

## Outputs

**CSV tables:**
- `significant_interactions.csv` — All significant L-R pairs with source, target, pathway, probability
- `pathway_summary.csv` — Pathway-level communication summary
- `interaction_count_matrix.csv` — Cell type × cell type interaction counts
- `interaction_strength_matrix.csv` — Cell type × cell type communication weights
- `signaling_roles.csv` — Centrality scores (sender, receiver, mediator, influencer per pathway)
- `top_interactions.csv` — Top 20 interactions ranked by probability

**Visualizations (PNG + SVG):**
- `interaction_count_network` — Circle plot of interaction counts
- `interaction_strength_network` — Circle plot of communication strength
- `chord_aggregated` — Chord diagram of the full communication network
- `bubble_ligand_receptor` — Bubble plot of L-R pairs by cell type pairs
- `signaling_outgoing_heatmap` — Outgoing signaling patterns by cell type
- `signaling_incoming_heatmap` — Incoming signaling patterns by cell type
- `signaling_role_scatter` — Dominant senders vs receivers scatter

**Analysis objects (RDS):**
- `cellchat_object.rds` — Complete CellChat object for downstream use
  - Load with: `cellchat <- readRDS('cellchat_object.rds')`
  - Required for: multi-condition comparison, pathway-specific deep dives

**Reports:**
- `analysis_report.md` — Markdown report (always generated)
- `analysis_report.pdf` — PDF report (requires rmarkdown + LaTeX)

## Clarification Questions

🚨 **ALWAYS ask Question 1 FIRST. Do not proceed before the user answers.**

### 1. Input Files (ASK THIS FIRST):
- **Do you have an annotated Seurat object (.rds) from scRNA-seq analysis?**
  - If yes: provide the path to the `.rds` file
  - Expected: Seurat v5 object with cell type labels in metadata
- **Or use example data?** — PBMC 3k dataset (human immune cells, 2,638 cells, 8 cell types)
  - Uses `source("scripts/load_data.R"); seurat_obj <- load_example_pbmc()`

> 🚨 **IF EXAMPLE DATA SELECTED:** Parameters are pre-defined. Skip to Question 4 (or proceed directly to Step 1). Do NOT ask questions 2-3.

### 2. Species (own data only):
- a) Human (CellChatDB.human) — default
- b) Mouse (CellChatDB.mouse)

### 3. Cell Type Column (own data only):
- Which metadata column contains cell type annotations?
  - Common: `celltype`, `singler_labels`, `cell_type`, `predicted.celltype.l2`
  - Check with: `colnames(seurat_obj@meta.data)`

### 4. Analysis Scope (structured — works for demo and own data):
- a) **All signaling types** (Secreted + ECM-Receptor + Cell-Cell Contact) — ✅ recommended
- b) Secreted signaling only
- c) Cell-Cell Contact only

## Standard Workflow

> **Note:** Run from the OmicsClaw root directory and add the workflow scripts to `sys.path`:
> ```python
> import sys; import os; sys.path.insert(0, os.path.abspath('knowledge_base/scripts/cell-cell-communication'))
> ```

🚨 **MANDATORY: USE SCRIPTS EXACTLY AS SHOWN — DO NOT WRITE INLINE CODE** 🚨

**Step 1 — Load data:**
```r
source("scripts/load_data.R")
seurat_obj <- load_cellchat_data()  # example PBMC data
# OR: seurat_obj <- load_cellchat_data("path/to/seurat_processed.rds")
```

**Step 2 — Run CellChat analysis:**
```r
source("scripts/run_cellchat.R")
cellchat <- run_cellchat_analysis(seurat_obj, species = "human", group.by = "celltype")
```
**DO NOT write inline CellChat code. Just source the script and call the function.**

**Step 3 — Generate visualizations:**
```r
source("scripts/cellchat_plots.R")
generate_all_plots(cellchat, output_dir = "results")
```
🚨 **DO NOT write inline plotting code. Just use the script.** 🚨

**Step 4 — Export results:**
```r
source("scripts/export_results.R")
export_all(cellchat, seurat_obj = seurat_obj, output_dir = "results")
```
**DO NOT write custom export code. Use export_all().**

**✅ VERIFICATION — You should see:**
- After Step 1: `"✓ Data loaded successfully! [N] cells, [M] cell types"`
- After Step 2: `"✓ CellChat analysis completed! [N] significant interactions across [M] pathways"`
- After Step 3: `"✓ All plots generated successfully! [6] visualizations saved"`
- After Step 4: `"=== Export Complete ==="`

**❌ IF YOU DON'T SEE THESE:** You wrote inline code. Stop and use source().

⚠️ **CRITICAL — DO NOT:**
- ❌ **Write inline CellChat code** → **STOP: Use `source("scripts/run_cellchat.R")`**
- ❌ **Write inline plotting code** → **STOP: Use `generate_all_plots()`**
- ❌ **Write custom export code** → **STOP: Use `export_all()`**
- ❌ **Try to install system-level dependencies** → CellChat handles its own deps

**⚠️ IF SCRIPTS FAIL — Script Failure Hierarchy:**
1. **Fix and Retry (90%)** — Install missing package, re-run script
2. **Modify Script (5%)** — Edit the script file itself, document changes
3. **Use as Reference (4%)** — Read script, adapt approach, cite source
4. **Write from Scratch (1%)** — Only if genuinely impossible, explain why

**NEVER skip directly to writing inline code without trying the script first.**

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| **CellChat not found** | Not installed from GitHub | `devtools::install_github("jinworks/CellChat")` — must use **jinworks** repo (not sqjin) |
| **"presto" required for Wilcoxon test** | Missing presto package | `remotes::install_github('immunogenomics/presto')` — script falls back to standard test if unavailable |
| **No significant interactions** | Too few cells per type or stringent filtering | Lower `min.cells` parameter or merge rare cell types |
| **Memory error on large datasets** | >50k cells uses substantial RAM | Subsample or increase memory; see [references/cellchat-guide.md](references/cellchat-guide.md) |
| **Chord diagram error** | Missing circlize package | `install.packages('circlize')` |
| **SVG export error "svglite required"** | Missing optional dependency | Use `generate_all_plots()` — it handles fallback automatically. DO NOT try to install svglite manually. |
| **svglite dependency conflict** | System library version mismatch | Normal — `generate_all_plots()` falls back to base R svg() device automatically. Both PNG and SVG will be created. |
| **"group.by not found"** | Wrong column name for cell types | Check: `colnames(seurat_obj@meta.data)` |
| **Seurat v5 slot error ("no slot of name images")** | Old Seurat object from v3/v4 | Script handles this — `UpdateSeuratObject()` is called automatically |
| **NMF not available** | NMF package not installed | `install.packages('NMF')` |
| **PDF report skipped** | No LaTeX installation | `install.packages('tinytex'); tinytex::install_tinytex()` — markdown report still available |

## Suggested Next Steps

After cell-cell communication analysis, consider:

1. **Multi-condition comparison** — Compare communication between disease vs healthy, treated vs untreated
   - See [references/cellchat-guide.md](references/cellchat-guide.md) for `mergeCellChat()` workflow
2. **Pathway deep dive** — Examine specific pathways (e.g., TNF, MHC-II) with hierarchy plots
3. **Gene regulatory networks** — Use `grn-pyscenic` to find transcription factors driving the communication
4. **Functional enrichment** — Run pathway analysis on sender/receiver gene sets

## Related Skills

| Skill | Relationship |
|-------|-------------|
| `scrnaseq-seurat-core-analysis` | **Upstream** — produces the annotated Seurat object input |
| `scrnaseq-scanpy-core-analysis` | Alternative upstream (Python-based, convert to Seurat for CellChat) |
| `grn-pyscenic` | Complementary — gene regulatory networks from same scRNA-seq data |

## References

- Jin S, et al. **Inference and analysis of cell-cell communication using CellChat.** *Nature Communications*. 2021;12:1088.
- Jin S, et al. **CellChat for systematic analysis of cell-cell communication from single-cell and spatially resolved transcriptomics.** *Nature Protocols*. 2024.
- [CellChat v2 GitHub (active)](https://github.com/jinworks/CellChat)
- [CellChat tutorials](https://github.com/jinworks/CellChat/tree/main/tutorial)
- Detailed patterns: [references/cellchat-guide.md](references/cellchat-guide.md)
- Visualization options: [references/visualization-guide.md](references/visualization-guide.md)
