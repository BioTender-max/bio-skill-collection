# bio-analysis-system

**Step 5: Analysis system design (分析方法体系构建)**

Build the analysis layer for the manuscript by identifying which analyses, tools, and biological validations should support each figure and each task.

## Purpose

1. Extract analysis patterns from related work
2. Borrow useful analyses from adjacent domains when needed
3. Map analyses to BioClaw-compatible tools or fallback software
4. Explain why each analysis is included and what biological claim it supports
5. Connect analyses to figure panels

## Input Format

```text
topic: [research topic]
paper_count: [number of related papers]
task_system: [task system]
metric_system: [metric system]
dataset_catalog: [dataset catalog]
```

## Workflow

### Step 5.1: Extract analyses from existing work

If enough related papers exist, inspect their figures and extract:

- panel type
- analysis method
- software / package
- important parameters
- the scientific or biological conclusion the panel supports

### Step 5.2: Borrow from adjacent fields

If the field is still thin, adapt common analyses from nearby areas such as:

- clustering
- marker visualization
- latent embedding visualization
- pathway enrichment
- cell-cell communication
- spatial statistics
- GRN analysis

### Step 5.3: Categorize analyses

Use three broad groups:

- **Quantitative analyses**
  - clustering
  - metric computation
  - statistical tests
  - baseline comparisons
- **Qualitative analyses**
  - spatial visualization
  - feature / violin plots
  - UMAP / t-SNE
  - before / after alignment comparisons
  - heatmaps
- **Biological analyses**
  - cell annotation
  - marker genes
  - pathway enrichment
  - GRN
  - ligand-receptor communication
  - spatial statistics
  - trajectory analysis

### Step 5.4: Map to BioClaw or fallback tools

Whenever possible, map analysis needs to BioClaw-compatible skills or established tools.

Examples:

- clustering -> Scanpy / Leiden
- annotation -> CellTypist / SingleR
- marker plots -> Scanpy
- enrichment -> gseapy
- spatial statistics -> squidpy
- GRN -> pySCENIC
- communication -> CellChat-like workflow

### Step 5.5: Standardize analysis descriptions

For each analysis, define:

- category
- purpose
- biological claim supported
- preferred tool
- fallback tool
- key function
- recommended parameters
- inputs / outputs
- mapped task
- mapped figure / panel

## Output Format

```markdown
# Analysis System

## Analysis Sources
- Extracted from related papers:
- Borrowed from adjacent domains:

## Quantitative Analyses

### Clustering
- Category:
- Purpose:
- Biological claim supported:
- Preferred tool:
- Fallback tool:
- Key function:
- Recommended parameters:
- Inputs / outputs:
- Relevant tasks:
- Figure mapping:

### Metric computation
- Category:
- Purpose:
- Preferred tools:
- Relevant tasks:
- Figure mapping:

## Qualitative Analyses
- spatial plot
- marker / feature plot
- latent embedding plot
- heatmap
- before / after alignment visualization

## Biological Analyses
- annotation
- marker recovery
- pathway enrichment
- GRN
- communication
- trajectory

## Next Step
- Use the analysis system to design figures in Step 6
```

## Usage

```bash
/bio-analysis-system "spatial multi-omics integration | paper_count: 5 | task_system: [...] | metric_system: [...] | dataset_catalog: [...]"
```

## Notes

1. Prefer analyses that directly support paper claims.
2. Make the biological readouts visible early; they should not appear only at the very end.
3. Map each major analysis to a concrete figure panel.
