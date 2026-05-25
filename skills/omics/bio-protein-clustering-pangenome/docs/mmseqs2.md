# MMseqs2 Usage Guide

## Official Documentation
- GitHub: https://github.com/soedinglab/MMseqs2
- Website: https://mmseqs.com
- Wiki: https://github.com/soedinglab/MMseqs2/wiki

## Installation

### Conda (Recommended)
```bash
conda install -c conda-forge -c bioconda mmseqs2
```

### Homebrew
```bash
brew install mmseqs2
```

### Docker
```bash
docker pull ghcr.io/soedinglab/mmseqs2
```

### Static Binaries
Download from https://mmseqs.com/latest
- Choose variant based on CPU: AVX2, SSE4.1, SSE2
- GPU support available for NVIDIA GPUs (Turing generation or newer)

## Key Command-Line Flags

### Clustering Workflows
- `easy-cluster` - Cascaded clustering algorithm for FASTA/FASTQ files
- `easy-linclust` - Linear-time clustering (recommended for large datasets >1M sequences)

### Critical Parameters
- `--min-seq-id FLOAT` - Sequence identity threshold (0.0-1.0, default: varies by workflow)
- `-c FLOAT` - Coverage threshold (0.0-1.0, e.g., 0.8 for 80% coverage)
- `--cov-mode INT` - Coverage calculation mode
  - `0` - bidirectional coverage (default)
  - `1` - query coverage (target covered by query)
  - `2` - target coverage (query covered by target)
  - `3` - target coverage if above id, query coverage otherwise
- `-s FLOAT` - Sensitivity (1.0 = fast, 7.0 = very sensitive)
- `--threads INT` - Number of CPU threads (default: auto-detect)

### Database Management
- `--compress` - Compress database (reduces size ~3.5x for DNA, ~1.7x for proteins)
- `--split-memory-limit SIZE` - Control memory usage for large datasets

### Output Format
- `--format-output STR` - Customize output columns (see wiki for available fields)

## Common Usage Examples

### Basic Protein Clustering
```bash
# Fast linear-time clustering for large datasets
mmseqs easy-linclust proteins.faa clusterRes tmp --min-seq-id 0.5 -c 0.8

# Cascaded clustering for higher sensitivity
mmseqs easy-cluster proteins.faa clusterRes tmp --min-seq-id 0.3 -c 0.5
```

### Protein Clustering for Pangenome Analysis
```bash
# Cluster proteins with 90% identity and 80% coverage
mmseqs easy-cluster proteins.faa orthogroups tmp \
    --min-seq-id 0.9 \
    -c 0.8 \
    --cov-mode 0 \
    -s 4.0 \
    --threads 8

# Output files:
# orthogroups_cluster.tsv - cluster assignments
# orthogroups_rep_seq.fasta - representative sequences
```

### High Sensitivity Ortholog Detection
```bash
# Use higher sensitivity for closely related species
mmseqs easy-cluster proteins.faa orthologs tmp \
    --min-seq-id 0.7 \
    -c 0.7 \
    --cov-mode 1 \
    -s 7.0 \
    --cluster-mode 0

# cluster-mode 0 = set cover (greedy incremental)
# cluster-mode 1 = connected component
# cluster-mode 2 = greedy incremental (default)
```

### GPU-Accelerated Clustering
```bash
# Utilize GPU for faster processing (requires NVIDIA GPU)
mmseqs easy-cluster proteins.faa clusterRes tmp \
    --min-seq-id 0.5 \
    -c 0.8 \
    --gpu 1
```

### Create and Reuse Database
```bash
# Create MMseqs2 database once
mmseqs createdb proteins.faa proteinsDB

# Create index for repeated searches
mmseqs createindex proteinsDB tmp

# Use database for clustering
mmseqs cluster proteinsDB clusterDB tmp --min-seq-id 0.5
mmseqs createtsv proteinsDB proteinsDB clusterDB clusterRes.tsv
```

## Input/Output Formats

### Input
- **FASTA/FASTQ** protein or nucleotide sequences
- **MMseqs2 database** (created with `createdb`)

### Output
- **Cluster TSV** (from `easy-cluster`/`easy-linclust`)
  - Column 1: Representative sequence ID
  - Column 2: Member sequence ID
  - Each row represents one cluster membership

- **Representative sequences** (`*_rep_seq.fasta`)
  - FASTA file containing one sequence per cluster

### Converting to Presence/Absence Matrix
```python
# Parse MMseqs2 cluster output
import pandas as pd

# Read cluster assignments
clusters = pd.read_csv('clusterRes_cluster.tsv', sep='\t',
                       header=None, names=['representative', 'member'])

# Extract genome IDs (assuming format: genome_id|protein_id)
clusters['genome'] = clusters['member'].str.split('|').str[0]
clusters['orthogroup'] = 'OG_' + clusters['representative'].astype(str)

# Create presence/absence matrix
matrix = clusters.pivot_table(
    index='orthogroup',
    columns='genome',
    values='member',
    aggfunc='count',
    fill_value=0
)
matrix = (matrix > 0).astype(int)
```

## Performance Tips

### Speed vs Sensitivity Trade-offs
```bash
# FAST: Large datasets (>100k sequences), 95%+ identity
mmseqs easy-linclust proteins.faa out tmp --min-seq-id 0.95 -s 1.0

# BALANCED: Medium sensitivity, good for 70-90% identity
mmseqs easy-cluster proteins.faa out tmp --min-seq-id 0.7 -s 4.0

# SENSITIVE: Distant homologs, <50% identity
mmseqs easy-cluster proteins.faa out tmp --min-seq-id 0.3 -s 7.0
```

### Memory Optimization
```bash
# Limit memory usage (useful for large datasets)
mmseqs easy-cluster proteins.faa out tmp \
    --split-memory-limit 50G \
    --threads 8

# Remove temporary files to save disk space
# (MMseqs2 auto-creates tmp directory, can be large)
rm -rf tmp/
```

### Multi-Server Scaling
```bash
# Compile with MPI support for distributed computing
# cmake -DHAVE_MPI=1 ..
mpirun -np 64 mmseqs cluster proteinsDB clusterDB tmp
```

### Pre-Indexing for Repeated Searches
```bash
# Create index once, reuse for multiple analyses
mmseqs createindex proteinsDB tmp --threads 16

# Subsequent clustering will be faster
mmseqs cluster proteinsDB clusterDB tmp --min-seq-id 0.5
```

## Parameter Recommendations for Pangenome Analysis

### Closely Related Strains (Same Species)
```bash
# High identity threshold for intra-species comparisons
mmseqs easy-cluster proteins.faa orthogroups tmp \
    --min-seq-id 0.95 \
    -c 0.9 \
    --cov-mode 0 \
    -s 4.0
```

### Related Species (Same Genus)
```bash
# Moderate identity for inter-species orthologs
mmseqs easy-cluster proteins.faa orthogroups tmp \
    --min-seq-id 0.7 \
    -c 0.7 \
    --cov-mode 0 \
    -s 5.0
```

### Distant Relatives (Cross-Genus)
```bash
# Lower identity, higher sensitivity
mmseqs easy-cluster proteins.faa orthogroups tmp \
    --min-seq-id 0.3 \
    -c 0.5 \
    --cov-mode 1 \
    -s 7.0
```

## Troubleshooting

### Out of Memory Errors
- Use `--split-memory-limit` to process in chunks
- Reduce `--threads` to decrease parallel memory usage
- Use `easy-linclust` instead of `easy-cluster` for very large datasets

### Too Few/Many Clusters
- **Too few clusters**: Lower `--min-seq-id` or `-c` thresholds
- **Too many clusters**: Increase `--min-seq-id` or use `--cluster-mode 0`

### Slow Performance
- Use `easy-linclust` for linear-time clustering (10-100x faster)
- Reduce sensitivity (`-s 1.0` for fastest)
- Enable GPU acceleration (`--gpu 1`)
- Pre-create database index with `createindex`

## Benchmarks
- **Performance**: ~10,000x faster than BLAST
- **Scalability**: Tested on datasets with 100M+ sequences
- **Accuracy**: Comparable sensitivity to PSI-BLAST at high sensitivity settings
