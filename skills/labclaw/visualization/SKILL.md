# Scientific Visualization

## Overview
Publication-quality scientific figure generation. GENERAL: language-agnostic (R, Python, Julia, or any tool).

## Aesthetic System (ScienceClaw Standard)

### Palette Selection
| Group Count | Recommended Palette |
|-------------|-------------------|
| 2-5 groups | NPG or Lancet |
| 6-12 groups | Paired |
| >12 groups | colorRampPalette |
| Diverging data | RdBu |
| Sequential data | viridis |
| Up/Down/NS | "#E64B35" / "#4DBBD5" / "#999999" |

### Journal Figure Sizing
| Format | Width | Height | Base Size | DPI |
|--------|-------|--------|-----------|-----|
| Single column | 8.5 cm | 7 cm | 11 pt | 300 |
| 1.5 column | 12 cm | 9 cm | 12 pt | 300 |
| Double column | 17.5 cm | 10 cm | 13 pt | 300 |
| PPT | 25 cm | 18 cm | 16 pt | 150 |

### Theme Rules
- Clean, minimal. No unnecessary gridlines.
- theme_classic() or theme_bw() as starting points (R) / white background in matplotlib
- Consistent margins across all figures in a project
- Arial or Helvetica font family

### Code Rules
- Adjustable parameters at the TOP of every script
- Return the plot object (don't hardcode file saving)
- Output formats: PNG (300+ dpi), PDF (vector), SVG

## Chart Type Guide
- **Distribution**: boxplot, violin, density, histogram, jitter
- **Comparison**: barplot, grouped bar, dotplot, radar
- **Correlation**: scatter, correlation matrix, bubble
- **Composition**: pie, ring, Venn, UpSet, stacked bar
- **Genomics**: volcano, Manhattan, Q-Q, GSEA, UMAP/tSNE, heatmap
- **Survival**: Kaplan-Meier, Cox forest plot
- **Network**: Sankey, chord, network graph
- **Spatial**: spatial transcriptomics, geographic

## 35 Detailed Chart Skill References
Available in `mcp-servers/visualization/skills/` — one .md file per chart type with full aesthetic guidelines, data requirements, and code examples.
