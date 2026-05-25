# bio-metric-system

**Step 4: Metric system design (评价指标体系构建)**

Build a defensible set of quantitative and qualitative metrics by extracting them from related work or adapting them from adjacent fields.

## Purpose

1. Extract evaluation metrics from existing literature
2. Borrow metrics from adjacent domains when needed
3. Organize metrics into quantitative and qualitative groups
4. Explain what each metric measures and how it should be computed

## Input Format

```text
topic: [research topic]
paper_count: [number of related papers]
task_system: [task system from Step 2]
```

## Workflow

### Step 4.1: Extract metrics from existing work

If `paper_count >= 5`, review the Results / Benchmark sections of the strongest related papers and extract:

- metric name
- what it evaluates
- formula or computation method
- expected range
- how often it appears in the field

### Step 4.2: Borrow metrics from adjacent domains

If the literature is still thin, adapt metrics from a nearby field.

Examples:

- clustering agreement -> ARI / NMI
- modality agreement -> Pearson / cosine similarity
- reconstruction / registration -> MSE / MAE
- biological relevance -> marker recovery / enrichment scores

### Step 4.3: Organize the metric system

Split metrics into:

- **Quantitative metrics**
  - integration quality
  - modality consistency
  - registration / alignment quality
  - biological agreement
- **Qualitative metrics**
  - spatial plots
  - feature plots
  - latent visualizations
  - heatmaps
  - pathway / enrichment figures

### Step 4.4: Standardize each metric

For each metric, define:

- English name
- optional Chinese reference in parentheses
- category
- what it measures
- formula (if needed)
- range / interpretation
- software implementation
- task relevance
- mapped figure / panel

## Output Format

```markdown
# Metric System

## Metric Sources
- Extracted from related papers:
- Borrowed from adjacent domains:

## Quantitative Metrics

### ARI (Adjusted Rand Index)
- Category:
- What it measures:
- Formula:
- Range:
- Interpretation:
- Implementation:
- Relevant tasks:
- Figure mapping:

### NMI (Normalized Mutual Information)
- Category:
- What it measures:
- Formula:
- Range:
- Interpretation:
- Implementation:
- Relevant tasks:
- Figure mapping:

### Pearson correlation
- Category:
- What it measures:
- Formula:
- Range:
- Interpretation:
- Implementation:
- Relevant tasks:
- Figure mapping:

## Qualitative Metrics / Visual Readouts
- spatial domain map
- feature plot
- violin plot
- UMAP / latent visualization
- heatmap
- pathway enrichment figure

## Next Step
- Use the metric system to build the analysis system in Step 5
```

## Recommended Core Metrics

For most manuscript-planning runs, include at least:

- ARI
- NMI
- Macro-F1 or annotation accuracy
- Pearson / cosine similarity when cross-modal agreement matters
- MSE / MAE when reconstruction or alignment quality matters
- at least one biological validation readout

## Usage

```bash
/bio-metric-system "spatial multi-omics integration | paper_count: 5 | task_system: [task system from Step 2]"
```

## Notes

1. Do not overload the paper with too many metrics; prefer a compact but defendable set.
2. Match each metric to a specific task claim.
3. Include at least one metric that reflects biological value, not just technical fit.
