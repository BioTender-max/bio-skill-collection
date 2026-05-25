# immune-deconvolution

Estimate immune and stromal cell composition from bulk RNA-seq. Covers 9 methods through the immunedeconv unified interface, plus BayesPrism for single-cell-reference-based deconvolution.

```mermaid
graph TD
    A["immune-deconvolution<br>SKILL.md"] --> B["Absolute fractions<br>quanTIseq · EPIC"]
    A --> C["Relative proportions<br>CIBERSORT (22 types)"]
    A --> D["Enrichment scores<br>xCell (64 types) · MCP-counter"]
    A --> E["Purity estimation<br>ESTIMATE"]
    A --> F["Tumor-specific<br>TIMER · ConsensusTME"]
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

## Methods at a glance

| Method | Output type | Cell types | Input |
|--------|------------|------------|-------|
| quanTIseq | Absolute fractions | 10 immune + other | TPM |
| EPIC | Absolute fractions | 6 immune + cancer | TPM |
| CIBERSORT | Relative fractions | 22 immune subtypes | TPM (registration required) |
| xCell | Enrichment scores | 64 types | TPM |
| MCP-counter | Arbitrary scores | 8 immune + 2 stromal | TPM |
| TIMER | Regression scores | 6 immune | TPM + cancer type |
| ESTIMATE | Composite scores | Immune, stromal, purity | TPM |
| BayesPrism | Absolute fractions | Custom (from scRNA-seq) | Counts |
