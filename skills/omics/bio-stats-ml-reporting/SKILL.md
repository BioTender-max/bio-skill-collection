---
name: bio-stats-ml-reporting
description: Aggregate results, train ML models, and produce reports with validated references.
---

# Bio Stats ML Reporting

Aggregate results, train ML models, and produce reports with validated references.

## Instructions

1. Join outputs in DuckDB v1.1+ and build feature tables. Arrow / DuckLake integration is the recommended bridge into ML pipelines for large datasets.
2. Train baseline models and evaluate with cross-validation.
   - CPU baseline: scikit-learn v1.5+ for linear/tree/clustering baselines; XGBoost v2.1.4+ for gradient boosting.
   - GPU node available (CUDA): set `device="cuda"` on XGBoost (native since v2.0) by default. For sklearn-compatible estimators (random forest, k-means, PCA, UMAP), use **RAPIDS cuML** as a drop-in replacement and record the device in the run log.
3. Generate reports and validate references.
4. For exploratory omics projects, aggregate discovery evidence across the literature-derived analysis playbook, annotation, phylogenomics, viromics, and comparative-genomics outputs.
5. **Comparative-axes rollup** — join the per-axis comparison artifacts produced by upstream skills into a single `comparative_axes_summary.tsv`. The rollup must have one row per (query genome, axis) and include:
   - `genome-property frontier` (size, gene count, etc. — link to `relative_genome_metrics.tsv` and `genome_size_frontier.tsv`)
   - `marker-gene census` (link to `marker_census.tsv`)
   - `family copy-number expansions/contractions` (link to `family_copy_number_comparison.tsv` and `family_expansion_candidates.tsv`)
   - `synteny / conserved neighborhoods` (link to `conserved_neighborhoods.tsv`)
   - `non-coding RNA census` (link to `ncRNA_census.tsv`)
   Each row records observation, comparison baseline, literature reference, status (notable / conserved / artifact / negative), and a follow-up test.
6. Produce an interesting-findings section that ranks candidate discoveries relative to the literature-derived baseline and separates:
   - strong candidates with multiple evidence types
   - plausible candidates needing validation
   - likely artifacts or conserved lineage features
   - explicit negative findings where nothing notable was detected
7. Include the comparison baseline, literature context, confidence, and next discriminating analyses for each candidate.

## Quick Reference

| Task | Action |
|------|--------|
| Run workflow | Follow the steps in this skill and capture outputs. |
| Validate inputs | Confirm required inputs and reference data exist. |
| Review outputs | Inspect reports and QC gates before proceeding. |
| Tool docs | See `docs/README.md`. |

## Input Requirements

Prerequisites:
- Tools available in the active environment (Pixi/conda/system). See `docs/README.md` for expected tools.
- Results tables and metadata are available.
Inputs:
- results/*.parquet or results/*.tsv
- metadata.tsv

## Output

- results/bio-stats-ml-reporting/models/
- results/bio-stats-ml-reporting/metrics.tsv
- results/bio-stats-ml-reporting/comparative_axes_summary.tsv
- results/bio-stats-ml-reporting/discovery_summary.tsv
- results/bio-stats-ml-reporting/report.md
- results/bio-stats-ml-reporting/logs/

## Quality Gates

- [ ] Model performance sanity checks pass.
- [ ] Reference validation passes.
- [ ] On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.
- [ ] Verify input tables are readable and schema-consistent.
- [ ] Discovery summary joins candidate genes/features to annotation evidence, comparison baseline, literature context, and confidence.
- [ ] `comparative_axes_summary.tsv` covers all five mandatory axes (genome-property frontier, marker-gene census, family copy-number, synteny/neighborhoods, ncRNA census) for every query genome, with rows for axes that produced negative findings.
- [ ] Final report states what is interesting, what is conserved/expected, what is likely artifact, and what should be tested next.

## Examples

### Example 1: Expected input layout

```text
results/*.parquet or results/*.tsv
metadata.tsv
```

## Troubleshooting

**Issue**: Missing inputs or reference databases
**Solution**: Verify paths and permissions before running the workflow.

**Issue**: Low-quality results or failed QC gates
**Solution**: Review reports, adjust parameters, and re-run the affected step.
