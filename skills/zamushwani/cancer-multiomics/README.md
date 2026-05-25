# cancer-multiomics

Multi-omics analysis skill for TCGA and GEO cancer datasets. Covers four data types with tested protocols and correct defaults.

```mermaid
graph TD
    A["cancer-multiomics<br>SKILL.md"] --> B["Expression<br>DESeq2 · clusterProfiler"]
    A --> C["Mutation<br>maftools · TMB · signatures"]
    A --> D["Copy Number<br>GISTIC2 · segment analysis"]
    A --> E["Methylation<br>minfi · ChAMP · DMRcate"]
    style A fill:#1a1a2e,stroke:#00d9ff,color:#fff,stroke-width:2px
    style B fill:#1a1a2e,stroke:#4ecdc4,color:#fff,stroke-width:2px
    style C fill:#1a1a2e,stroke:#ff6b6b,color:#fff,stroke-width:2px
    style D fill:#1a1a2e,stroke:#87b13f,color:#fff,stroke-width:2px
    style E fill:#1a1a2e,stroke:#276DC3,color:#fff,stroke-width:2px
```

## Usage

```bash
# Claude Code
cp SKILL.md your-project/.claude/skills/

# Cursor
cp SKILL.md your-project/.cursor/skills/
```

## Validation

Tests in [`tests/`](tests/) run against TCGA-LUAD and check:

- Expression: DEG counts, sample counts, gene pre-filtering
- Mutation: TP53/KRAS/EGFR frequencies, TMB range, EGFR-KRAS mutual exclusivity
- CNV: segment interpretation, gain/loss classification, gene-level mapping
- Methylation: beta-value range, M-value conversion, DMP detection

```bash
Rscript tests/run_all.R          # run everything
Rscript tests/run_all.R expression  # run one
```
