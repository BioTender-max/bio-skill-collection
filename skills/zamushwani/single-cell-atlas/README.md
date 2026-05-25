# single-cell-atlas

Single-cell RNA-seq QC, preprocessing, integration, clustering, and cell type annotation. Dual-language: Seurat v5 (R) and scanpy (Python).

```mermaid
graph TD
    A["single-cell-atlas<br>SKILL.md"] --> B["QC filtering<br>MAD-based thresholds"]
    A --> C["Doublet detection<br>scDblFinder · Scrublet"]
    A --> D["Normalization<br>SCTransform v2 · scran"]
    A --> E["Integration<br>Harmony · scVI · CCA"]
    A --> F["Clustering & annotation<br>Leiden · CellTypist · scType"]
    style A fill:#1a1a2e,stroke:#00d9ff,color:#fff,stroke-width:2px
    style B fill:#1a1a2e,stroke:#4ecdc4,color:#fff,stroke-width:2px
    style C fill:#1a1a2e,stroke:#ff6b6b,color:#fff,stroke-width:2px
    style D fill:#1a1a2e,stroke:#87b13f,color:#fff,stroke-width:2px
    style E fill:#1a1a2e,stroke:#276DC3,color:#fff,stroke-width:2px
    style F fill:#1a1a2e,stroke:#e84d3c,color:#fff,stroke-width:2px
```

## Usage

```bash
# Claude Code
cp SKILL.md your-project/.claude/skills/

# Cursor
cp SKILL.md your-project/.cursor/skills/
```

## Languages covered

| Step | R (Seurat v5) | Python (scanpy) |
|------|---------------|-----------------|
| QC metrics | `PercentageFeatureSet()` | `sc.pp.calculate_qc_metrics()` |
| MAD filtering | Manual or `scater::isOutlier()` | Manual MAD computation |
| Doublets | `scDblFinder()` | `sc.pp.scrublet()` |
| Normalization | `SCTransform()` or `NormalizeData()` | `sc.pp.normalize_total()` + `log1p()` |
| Feature selection | `FindVariableFeatures()` | `sc.pp.highly_variable_genes()` |
| Integration | `IntegrateLayers()` / `RunHarmony()` | `harmony_integrate()` / scVI |
| Clustering | `FindClusters(algorithm=4)` | `sc.tl.leiden()` |
| Annotation | scType | CellTypist |
