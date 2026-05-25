# Tool Documentation

**Last Updated:** 2026-02-01

This directory contains practical usage guides for the tools used in the bio-stats-ml-reporting skill.

## Tools

### Data Processing & Analytics
- **[DuckDB](duckdb.md)** (v1.4.3) - SQL analytics database for aggregating and joining results
  - CLI usage, Parquet/TSV handling, performance optimization
  - Official docs: https://duckdb.org/docs/stable/

### Machine Learning
- **[scikit-learn](scikit-learn.md)** (v1.8.0) - ML library for baseline models and cross-validation
  - Classification, regression, model selection, pipelines
  - Official docs: https://scikit-learn.org/stable/

- **[XGBoost](xgboost.md)** (v3.1.3) - Gradient boosting library for high-performance models
  - Parameter tuning, feature importance, early stopping
  - Official docs: https://xgboost.readthedocs.io/

### Reference Validation
- **[crossrefapi](crossrefapi.md)** (v1.7.0) - Python client for Crossref API to validate DOIs
  - Bibliographic metadata retrieval, batch validation, citation formatting
  - Official docs: https://github.com/fabiobatalha/crossrefapi

## Documentation Format

Each tool guide includes:
- Installation commands
- Key parameters/flags
- Common usage examples for stats/ML/reporting workflows
- Input/output formats
- Performance tips
- Typical bioinformatics workflow examples

## Quick Reference

### Typical Workflow

```bash
# 1. Aggregate results with DuckDB
duckdb results/analysis.duckdb < aggregate_features.sql

# 2. Train models with scikit-learn and XGBoost
python train_models.py

# 3. Validate references with crossrefapi
python validate_references.py

# 4. Generate report
python generate_report.py
```

### File Locations

- Input: `results/*.parquet`, `metadata.tsv`
- Models: `results/bio-stats-ml-reporting/models/`
- Metrics: `results/bio-stats-ml-reporting/metrics.tsv`
- Report: `results/bio-stats-ml-reporting/report.md`
- Logs: `results/bio-stats-ml-reporting/logs/`

## Tool Installation

All tools are managed via pixi (see `pixi.toml` in skill directory):

```bash
# Install all dependencies
pixi install

# Run in pixi environment
pixi run python train_models.py
```

## Contributing

When updating documentation:
1. Verify commands against official docs
2. Test examples with real data
3. Keep examples concise and practical
4. Focus on bioinformatics/stats use cases
5. Update this README with the current date
