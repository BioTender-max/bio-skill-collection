# Tool Documentation

Updated: 2026-02-01

## Overview

This directory contains practical usage guides for structure prediction and annotation tools. Each guide includes installation instructions, command-line flags, common usage patterns, and performance tips.

## Tools

### Structure prediction

- **[boltz](boltz.md)** - Boltz-2 (MIT license, CUDA, NVIDIA cuEquivariance kernels)
  - GitHub: https://github.com/jwohlwend/boltz
  - Use for: default structure and complex prediction, protein-ligand binding affinity, drug discovery
  - Notes: replaces Boltz-1; ~1000× faster than FEP for affinity; benchmarked competitively with AlphaFold3

- **[colabfold](colabfold.md)** - ColabFold with MMseqs2-GPU MSA backend
  - GitHub: https://github.com/sokrypton/ColabFold
  - Use for: cases where a wider MSA than Boltz-2 builds is needed
  - Notes: MMseqs2-GPU backend provides ~31.8× MSA-generation speedup over the standard AF2 pipeline

- **ESMFold** - fast monomer pre-screening only (15–20 GB VRAM)
  - Not used for final predictions; route ESMFold candidates to Boltz-2

> AlphaFold3 is intentionally not part of this stack (non-commercial license, 40–80 GB VRAM, no clear quality gap for the workflows here). Use Boltz-2.

### Structure search and annotation

- **[foldseek](foldseek.md)** - Foldseek v9+ with `--gpu 1` mode (ProstT5 on CUDA Turing+)
  - GitHub: https://github.com/steineggerlab/foldseek
  - Use for: structure similarity search, clustering, large-scale database searches; ~4–27× speedup over CPU Foldseek

- **[tm-vec](tm-vec.md)** - Transformer-based structure embedding for rapid similarity search
  - GitHub: https://github.com/tymor22/tm-vec
  - Use for: fast pre-screening, large-scale structure comparisons, vector-based search

## Quick reference

### When to use each tool

| Task | Tool | Reason |
|------|------|--------|
| Fast structure pre-screening (embedding) | TM-Vec | Vector-based search; seconds across millions of proteins |
| Fast monomer pre-screening (structure) | ESMFold | Lowest VRAM; lower accuracy — triage only |
| Default structure + complex + affinity | Boltz-2 | MIT license; CUDA-native; strong benchmark performance |
| Wider MSA than Boltz-2 builds | ColabFold + MMseqs2-GPU | Fastest MSA pipeline for AF2-style runs |
| Detailed structure search | Foldseek v9 (`--gpu 1`) | High sensitivity, GPU-accelerated structural alignment |
| Structure clustering | Foldseek | Built-in clustering algorithms |

### Installation Quick Start

```bash
# tm-vec
conda create -n tmvec faiss-cpu python=3.9 -c pytorch
conda activate tmvec
pip install tm-vec

# foldseek
conda install -c conda-forge -c bioconda foldseek

# colabfold
# See LocalColabFold: https://github.com/YoshitakaMo/localcolabfold

# boltz
pip install boltz[cuda] -U
```

## Typical Workflow

### Structure-Based Annotation Pipeline

1. **Fast pre-screening** (optional, for large datasets)
   - Use tm-vec to quickly filter candidates
   - Reduces search space for detailed analysis

2. **Structure prediction**
   - Default: Boltz-2 (structure, complex, and binding affinity)
   - Wider MSA needed: ColabFold with MMseqs2-GPU backend
   - Triage only: ESMFold

3. **Detailed structure search**
   - Use Foldseek v9 (`--gpu 1` on Turing+ GPUs) against PDB, AlphaFoldDB, or custom databases
   - High-sensitivity mode for distant homologs
   - Fast mode for close homologs

4. **Clustering** (for large result sets)
   - Use foldseek easy-cluster to group similar structures
   - Identify representative structures for annotation

## Performance Considerations

### Speed Comparison (approximate)
- **tm-vec**: Fastest (vector search, seconds for millions)
- **foldseek**: Fast (structure alignment, minutes for large DBs)
- **colabfold**: Moderate (structure prediction, minutes to hours)
- **boltz**: Moderate to slow (complex prediction with affinity)

### Resource Requirements

| Tool | RAM | GPU | Storage |
|------|-----|-----|---------|
| tm-vec | Low-Moderate | Optional | Low (embeddings) |
| foldseek | Moderate-High* | Optional | Moderate (databases) |
| colabfold | Moderate | Recommended | High (~940GB for local DBs) |
| boltz | Moderate | Recommended | Moderate |

*foldseek RAM can be reduced with `--sort-by-structure-bits 0`

## Additional Resources

### Reference Databases

**Foldseek/Structure Search:**
- AlphaFoldDB (AFDB50): ~54M structures
- PDB: Experimental structures
- Custom databases from predicted structures

**TM-vec:**
- CATH domains database
- SWISS-PROT sequences (pre-embedded)

## Support and Issues

- Tool-specific issues: Report to respective GitHub repositories
- Skill implementation: See main skill documentation in `../SKILL.md`
