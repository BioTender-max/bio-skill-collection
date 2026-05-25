# Tool Documentation

Updated: 2026-02-01

This directory contains practical usage guides for protein clustering and pangenome analysis tools.

## Available Tools

### Primary clustering tools

| Tool | Best for | Speed | Documentation |
|------|----------|-------|---------------|
| **OrthoFinder v3** | Default orthology inference, gene + species trees | Medium | [orthofinder.md](orthofinder.md) |
| **MMseqs2 (CPU or GPU)** | Sequence clustering and search backbones; very large datasets | Very fast | [mmseqs2.md](mmseqs2.md) |
| **ProteinOrtho v6+** | Large pangenomes where OrthoFinder is RAM-limited | Fast | [proteinortho.md](proteinortho.md) |

### Quick selection guide

- Default orthology inference up to a few hundred genomes → **OrthoFinder v3** (7% accuracy gain over v2, lower RAM at scale).
- Very large pangenomes where OrthoFinder is too RAM-heavy → **ProteinOrtho v6** (graph-based RBH; PoFF extension adds synteny support).
- Sequence clustering at any scale → **MMseqs2** v15-6f452+ (`easy-cluster` or `easy-linclust`). Add `--gpu` on CUDA Turing+ for ~20× speedup at near-identical sensitivity.
- Synteny across many genomes → run alongside `ntSynt` or MCScanX (see SKILL.md).

> **Retired:** OrthoMCL has been dropped from this workflow. Existing pipelines should migrate to OrthoFinder v3.

## Tool comparison

### Features

| Feature | MMseqs2 | ProteinOrtho | OrthoFinder |
|---------|---------|--------------|-------------|
| Installation | Easy | Easy | Easy |
| Dependencies | Minimal | Minimal | Moderate |
| Scalability | Excellent (GPU optional) | Good | Good |
| Gene trees | No | No | Yes |
| Synteny support | No | Yes (PoFF) | No |
| Paralog detection | Basic | Good | Excellent |
| Speed (1000 genomes) | Hours | Days | Days |

### Typical runtimes

**Dataset: 100 bacterial genomes, ~300k proteins, 16 CPU cores**

| Tool | Approximate runtime |
|------|---------------------|
| MMseqs2 (easy-linclust) | 10–30 minutes |
| MMseqs2 (easy-cluster) | 1–3 hours |
| MMseqs2 (easy-cluster, GPU) | ~5–10 minutes (CUDA Turing+) |
| ProteinOrtho (DIAMOND) | 2–6 hours |
| OrthoFinder v3 (DIAMOND) | 3–10 hours |
| OrthoFinder v3 (MSA mode) | 10–40 hours |

## Documentation Contents

Each tool guide includes:

1. **Official Documentation Links**
   - GitHub/website
   - Papers and manuals

2. **Installation Instructions**
   - Conda/Bioconda (recommended)
   - Docker containers
   - Manual installation

3. **Key Command-Line Flags**
   - Clustering parameters
   - Performance options
   - Output configuration

4. **Common Usage Examples**
   - Basic clustering
   - Pangenome analysis
   - Performance optimization

5. **Input/Output Formats**
   - FASTA requirements
   - Output file descriptions
   - Parsing examples (Python)

6. **Performance Tips**
   - Speed vs accuracy trade-offs
   - Memory management
   - Parameter recommendations

7. **Troubleshooting**
   - Common errors
   - Solutions and workarounds

## Common Workflow

### 1. Basic Pangenome Analysis

```bash
# Fast clustering for presence/absence matrix
mmseqs easy-cluster proteins.faa orthogroups tmp \
    --min-seq-id 0.9 \
    -c 0.8 \
    --threads 16
```

### 2. Phylogenomic Analysis

```bash
# Comprehensive analysis with gene trees
orthofinder -f protein_fastas/ \
    -S diamond \
    -M msa \
    -t 32

# Extract single-copy orthologs for phylogeny
# Results in: Orthogroups_SingleCopyOrthologues.txt
```

### 3. Large-Scale Metagenomics

```bash
# Incremental approach for 1000+ MAGs
orthofinder -f CoreMAGs_50/ -n Core -S mmseqs -t 64
orthofinder --core Results_Core/ --assign AllMAGs/ -t 64
```

## Parameter Guidelines

### Taxonomic Distance vs Parameters

| Comparison Level | Identity (%) | Coverage (%) | E-value |
|------------------|--------------|--------------|---------|
| Same strain | 95-100 | 90-95 | 1e-10 |
| Same species | 85-95 | 80-90 | 1e-7 |
| Same genus | 70-85 | 70-80 | 1e-5 |
| Same family | 50-70 | 60-70 | 1e-5 |
| Cross-family | 30-50 | 50-60 | 1e-3 |

### Tool-Specific Recommendations

#### MMseqs2
- **Closely related (>95% identity)**: `easy-linclust` with `-s 1.0`
- **Moderate divergence (70-95%)**: `easy-cluster` with `-s 4.0`
- **Distant homologs (<70%)**: `easy-cluster` with `-s 7.0`

#### ProteinOrtho
- **Same species**: `-identity=95 -cov=90 -p=diamond`
- **Same genus**: `-identity=70 -cov=70 -p=diamond`
- **With synteny**: `-synteny` (requires GFF files)

#### OrthoFinder
- **Fast orthogroups**: `-S diamond -og`
- **Phylogenomics**: `-S diamond -M msa`
- **Large-scale (>100 species)**: Core + assign workflow


## Output Analysis

### Converting to Presence/Absence Matrix

All tools output orthogroup assignments that can be converted to binary matrices for downstream analysis.

**Common format:**
```
Orthogroup    genome1    genome2    genome3
OG0000001     gene001    gene101    gene201
OG0000002     gene002    *          gene202
```

**Python parsing example:**
```python
import pandas as pd

# Read orthogroup table
og = pd.read_csv('orthogroups.tsv', sep='\t', index_col=0)

# Create binary presence/absence matrix
presence = og.notna().astype(int)

# Calculate core/accessory/cloud
n_genomes = len(og.columns)
freq = presence.sum(axis=1) / n_genomes

core = og[freq >= 0.99]        # ≥99% of genomes
accessory = og[(freq >= 0.15) & (freq < 0.99)]  # 15-99%
cloud = og[freq < 0.15]        # <15%
```

## Additional Resources

### Pangenome Pipelines
- **GET_HOMOLOGUES**: Comprehensive bacterial pangenome analysis
- **Roary**: Fast prokaryotic pangenome pipeline
- **PEPPAN**: Accurate reconstruction with paralog scoring
- **Anvi'o**: Integrated pangenomics with visualization
- **RIBAP**: Core genome annotation beyond species level

### References
See [../SKILL.md](../SKILL.md) for comprehensive references and concepts.

## Getting Help

1. **Check tool documentation** in this directory
2. **Review SKILL.md** for pangenome concepts
3. **Search Biostars** for community solutions
4. **GitHub Issues** for tool-specific problems

## Contributing

To update documentation:
1. Verify information against official sources
2. Test commands on sample datasets
3. Include practical examples
4. Keep concise and focused on common use cases
