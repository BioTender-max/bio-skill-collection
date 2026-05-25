# Foldseek

Fast protein structure search and clustering using 3Di structural alphabet and alignment.

## Official Documentation

- GitHub: https://github.com/steineggerlab/foldseek
- Paper: https://www.nature.com/articles/s41587-023-01773-0
- Webserver: https://search.foldseek.com

## Installation

### Precompiled Binaries
```bash
# Linux AVX2
wget https://mmseqs.com/foldseek/foldseek-linux-avx2.tar.gz
tar xvzf foldseek-linux-avx2.tar.gz

# Linux GPU (requires NVIDIA drivers ≥525.60.13, glibc ≥2.17)
wget https://mmseqs.com/foldseek/foldseek-linux-gpu.tar.gz
tar xvzf foldseek-linux-gpu.tar.gz

# macOS
wget https://mmseqs.com/foldseek/foldseek-osx-universal.tar.gz
tar xvzf foldseek-osx-universal.tar.gz
```

### Conda
```bash
conda install -c conda-forge -c bioconda foldseek
```

## Key Commands

### Structure Search
```bash
foldseek easy-search query.pdb target.pdb results.tsv tmpFolder
```

### Structure Clustering
```bash
foldseek easy-cluster input.pdb output_prefix tmpFolder
```

### Database Creation
```bash
# From PDB/mmCIF files
foldseek createdb structures/ targetDB
foldseek createindex targetDB tmp

# From FASTA using ProstT5 language model
foldseek databases ProstT5 weights tmp
foldseek createdb sequences.fasta db --prostt5-model weights --gpu 1

# Prepare for GPU search
foldseek makepaddedseqdb db db_pad
```

### Multimer/Complex Search
```bash
foldseek easy-multimersearch query.pdb.gz target.pdb.gz result tmpFolder
```

## Command-Line Flags

### Search Parameters

| Flag | Description | Default | Example |
|------|-------------|---------|---------|
| `-s` | Sensitivity (speed/accuracy tradeoff) | 9.5 | `-s 7.5` (faster), `-s 12.0` (more sensitive) |
| `-e` | E-value threshold (lower = stricter) | 0.001 | `-e 0.00001` |
| `-c` | Coverage requirement (fraction) | 0.0 | `-c 0.9` (90% coverage) |
| `--alignment-type` | Alignment method | 2 | `1` (TMalign global), `2` (3Di+AA local) |
| `--gpu` | Enable GPU acceleration | 0 | `--gpu 1` |
| `--threads` | Number of CPU threads | all | `--threads 8` |

### Output Formatting

| Flag | Description | Example |
|------|-------------|---------|
| `--format-output` | Custom output columns | `"query,target,fident,evalue,bits"` |
| `--format-mode` | Output format type | `0` (TSV), `3` (HTML), `5` (PDB) |

Default output columns: `query, target, fident, alnlen, mismatch, gapopen, qstart, qend, tstart, tend, evalue, bits`

### Memory Optimization

| Flag | Description | Impact |
|------|-------------|--------|
| `--sort-by-structure-bits` | Sort by structural similarity | `0` disables (saves ~75% RAM) |
| `--split-memory-limit` | RAM limit for splits | Default: system RAM |

## Input/Output Formats

### Input
- PDB files (flat or gzipped)
- mmCIF files (flat or gzipped)
- FASTA protein sequences (with ProstT5 model)

### Output
- **Tab-separated values** (default): columns defined by `--format-output`
- **Interactive HTML** (`--format-mode 3`): alignment visualization
- **Superposed PDB** (`--format-mode 5`): Cα-only aligned structures

### Clustering Output
`easy-cluster` generates:
- `_clu.tsv` - Representative/member mappings
- `_repseq.fasta` - Representative sequences
- `_allseq.fasta` - All cluster members

## Common Usage Examples

### Fast search against AlphaFold structures
```bash
foldseek easy-search query.pdb afdb50 results.tsv tmp -s 7.5 -e 0.001
```

### High-sensitivity search with coverage filter
```bash
foldseek easy-search query.pdb target.pdb results.tsv tmp -s 12.0 -c 0.8
```

### GPU-accelerated search
```bash
foldseek easy-search query.pdb target_pad.pdb results.tsv tmp --gpu 1
```

### Custom output with alignments
```bash
foldseek easy-search query.pdb target.pdb results.tsv tmp \
  --format-output "query,target,qaln,taln,evalue,bits"
```

### Cluster at 90% sequence identity
```bash
foldseek easy-cluster structures.pdb clusters tmp --min-seq-id 0.9
```

### Generate HTML visualization
```bash
foldseek easy-search query.pdb target.pdb results.html tmp --format-mode 3
```

## Memory Requirements

RAM formula: `(6 bytes Cα + 1 3Di byte + 1 AA byte) × database residues`

Example: 54M AFDB50 entries require ~151GB RAM
- Disable `--sort-by-structure-bits 0` to reduce to ~35GB

## Performance Tips

- Use `-s 7.5` for faster searches with acceptable sensitivity
- Enable GPU with `--gpu 1` for 5-10x speedup on large databases
- Create padded database (`makepaddedseqdb`) for GPU searches
- Use `--split-memory-limit` to control RAM usage on large datasets
- Disable `--sort-by-structure-bits 0` if memory is constrained
- Pre-create and index databases for repeated searches

## Webserver Alternative

For quick searches without local installation: https://search.foldseek.com
- Browser-based querying against AlphaFoldDB and PDB
- No local installation required
