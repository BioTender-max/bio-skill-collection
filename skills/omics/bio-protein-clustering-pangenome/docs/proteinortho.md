# ProteinOrtho Usage Guide

## Official Documentation
- GitLab: https://gitlab.com/paulklemm_PHD/proteinortho
- Manual: http://legacy.bioinf.uni-leipzig.de/Software/proteinortho/manual.html
- Debian Manpage: https://manpages.debian.org/testing/proteinortho/proteinortho.1.en.html
- Paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC10751348/

## Installation

### Conda/Bioconda (Recommended)
```bash
# Add Bioconda channels
conda config --add channels bioconda
conda config --add channels conda-forge
conda config --set channel_priority strict

# Install ProteinOrtho
conda install proteinortho
```

### Homebrew
```bash
brew install proteinortho
```

### Debian/Ubuntu
```bash
apt install proteinortho
```

### Docker
```bash
docker pull quay.io/biocontainers/proteinortho
```

### Manual Installation
Download from GitLab repository and run directly:
```bash
git clone https://gitlab.com/paulklemm_PHD/proteinortho.git
cd proteinortho
./proteinortho6.pl --help
```

## Key Command-Line Flags

### Basic Syntax
```bash
proteinortho6 [OPTIONS] FASTA1 FASTA2 [FASTA...]
```

### Alignment Program Selection
- `-p=PROGRAM` - Blast program selection (default: diamond)
  - `diamond` - Fast protein aligner (default, recommended)
  - `blastp+` - NCBI BLAST+ protein search
  - `blastn+` - NCBI BLAST+ nucleotide search
  - `mmseqs` - MMseqs2 fast clustering
  - `autoblastp` - Auto-detect BLAST version
  - `autoblastn` - Auto-detect BLAST version (nucleotide)

### Similarity Thresholds
- `-e=FLOAT` - E-value threshold for BLAST/Diamond (default: 1e-05)
- `-identity=INT` - Minimum percent identity (default: 25%)
- `-cov=INT` - Minimum alignment coverage percentage (default: 50%)
- `-sim=FLOAT` - Minimum similarity for additional hits, 0-1 (default: 0.95)
- `-conn=FLOAT` - Minimum algebraic connectivity threshold (default: 0.1)

### Output Configuration
- `-project=NAME` - Prefix for output files (default: myproject)
- `-desc` - Generate description files for NCBI FASTA headers
- `-singles` - Include singleton genes (no matches)
- `-selfblast` - Detect paralogs within same genome

### Performance Options
- `-cpus=INT` - Number of CPU cores (default: auto-detect)
- `-step=INT` - Control execution stages
  - `0` - Run all steps (default)
  - `1` - Generate indices only
  - `2` - Run BLAST searches
  - `3` - Perform clustering
- `-jobs=M/N` - Distributed processing (run job N of M total jobs)
- `-keep` - Keep temporary BLAST files for reuse
- `-force` - Recalculate all BLAST results (ignore cache)
- `-clean` - Remove temporary files after completion

### Advanced Features
- `-synteny` - Enable synteny analysis using GFF files (PoFF extension)
- `-verbose` - Display detailed progress information
- `-debug` - Output debugging information

## Common Usage Examples

### Basic Ortholog Detection
```bash
# Detect orthologs in 4 bacterial genomes
proteinortho6 -project=bacteria \
    genome1.faa \
    genome2.faa \
    genome3.faa \
    genome4.faa
```

### Protein Clustering for Pangenome Analysis
```bash
# High-stringency clustering (90% identity, 80% coverage)
proteinortho6 -project=pangenome \
    -p=diamond \
    -identity=90 \
    -cov=80 \
    -e=1e-10 \
    -cpus=16 \
    *.faa

# Output: pangenome.proteinortho.tsv
```

### Nucleotide-Based Analysis
```bash
# For nucleotide sequences (DNA/RNA)
proteinortho6 -project=nucleotide \
    -p=blastn+ \
    -identity=95 \
    -cov=90 \
    genome1.fna \
    genome2.fna \
    genome3.fna
```

### Include Singletons and Paralogs
```bash
# Comprehensive analysis including unique genes
proteinortho6 -project=complete \
    -singles \
    -selfblast \
    -identity=70 \
    -cov=70 \
    *.faa
```

### Synteny-Aware Analysis
```bash
# Use gene context information (requires GFF files)
proteinortho6 -project=synteny \
    -synteny \
    genome1.faa \
    genome2.faa \
    genome1.gff \
    genome2.gff
```

### Fast Analysis with MMseqs2
```bash
# Use MMseqs2 backend for speed
proteinortho6 -project=fast \
    -p=mmseqs \
    -identity=50 \
    -cov=50 \
    -cpus=32 \
    *.faa
```

### Distributed Computing
```bash
# Step 1: Generate indices on master node
proteinortho6 -step=1 -project=distributed *.faa

# Step 2: Run BLAST jobs distributed across 10 nodes
# On node 1:
proteinortho6 -step=2 -jobs=10/1 -project=distributed *.faa
# On node 2:
proteinortho6 -step=2 -jobs=10/2 -project=distributed *.faa
# ... repeat for nodes 3-10

# Step 3: Perform clustering on master node
proteinortho6 -step=3 -project=distributed *.faa
```

## Input/Output Formats

### Input Files
- **Protein FASTA** (.faa, .fasta) - Amino acid sequences
- **Nucleotide FASTA** (.fna, .fasta) - DNA/RNA sequences (use `-p=blastn+`)
- **GFF files** - Gene annotations for synteny analysis (optional)

**FASTA header requirements:**
- Unique identifiers per protein
- Format: `>gene_id` or `>genome|gene_id`

### Output Files

#### Primary Output: `<project>.proteinortho.tsv`
Tab-separated ortholog groups:

| Column | Description |
|--------|-------------|
| 1 | Number of species in orthogroup |
| 2 | Number of genes in orthogroup |
| 3 | Algebraic connectivity |
| 4+ | Gene IDs per genome (comma-separated if multi-copy) |

**Example:**
```
# Species	Genes	Alg.-Conn.	genome1.faa	genome2.faa	genome3.faa
3	3	1.0	gene001	gene101	gene201
2	4	0.8	gene002,gene003	*	gene202,gene203
```

- `*` = No gene from this genome in the orthogroup
- `gene1,gene2` = Multiple genes (paralogs) from same genome

#### Additional Outputs
- `<project>.blast-graph` - All-vs-all similarity graph
- `<project>.proteinortho-graph` - Orthology graph
- `<project>.proteinortho.html` - Visual summary report
- `<project>.proteinortho.summary` - Statistics summary

### Parsing ProteinOrtho Output
```python
import pandas as pd

# Read orthogroup table
df = pd.read_csv('pangenome.proteinortho.tsv', sep='\t', comment='#')

# Extract genome columns (skip first 3 metadata columns)
genome_cols = df.columns[3:]

# Create presence/absence matrix
def count_genes(cell):
    if cell == '*':
        return 0
    return len(cell.split(','))

presence = df[genome_cols].apply(lambda col: col.apply(count_genes))
presence_binary = (presence > 0).astype(int)

# Identify single-copy orthologs (1 gene per genome, all genomes)
single_copy = (presence == 1).all(axis=1)
core_single_copy = df[single_copy]

print(f"Total orthogroups: {len(df)}")
print(f"Single-copy orthologs: {single_copy.sum()}")
```

## Performance Tips

### Speed Optimization
```bash
# Use Diamond (default) - fastest protein aligner
proteinortho6 -p=diamond -cpus=32 *.faa

# Use MMseqs2 for very large datasets (>1000 genomes)
proteinortho6 -p=mmseqs -cpus=64 *.faa

# Relax thresholds for faster processing
proteinortho6 -identity=50 -cov=50 -e=1e-03 *.faa
```

### Memory Management
- Diamond backend: Low memory footprint
- BLAST+: Higher memory, use for small datasets (<100 genomes)
- MMseqs2: Memory-efficient for large-scale analysis

### Reusing Previous Results
```bash
# First run
proteinortho6 -keep -project=run1 *.faa

# Add new genomes without recalculating existing comparisons
proteinortho6 -project=run1 *.faa new_genome.faa
# (automatically reuses cached BLAST results)
```

### Distributed Processing
For large datasets, use `-jobs=M/N` to parallelize across cluster nodes:
```bash
# Total 100 jobs, run job 1
proteinortho6 -step=2 -jobs=100/1 -project=large *.faa
```

## Parameter Recommendations for Pangenome Analysis

### Same Species (Strain Comparison)
```bash
# High identity, high coverage
proteinortho6 -project=strains \
    -identity=95 \
    -cov=90 \
    -e=1e-10 \
    -singles \
    *.faa
```

### Same Genus (Inter-Species)
```bash
# Moderate stringency
proteinortho6 -project=genus \
    -identity=70 \
    -cov=70 \
    -e=1e-07 \
    -singles \
    *.faa
```

### Distant Relatives (Cross-Genus)
```bash
# Lower identity, relaxed coverage
proteinortho6 -project=distant \
    -identity=30 \
    -cov=50 \
    -e=1e-05 \
    -conn=0.05 \
    *.faa
```

### Paralog Detection
```bash
# Include self-BLAST to find duplications
proteinortho6 -project=paralogs \
    -selfblast \
    -singles \
    -identity=80 \
    -cov=80 \
    *.faa
```

### Synteny-Aware (Closely Related)
```bash
# Use gene neighborhood for better ortholog resolution
proteinortho6 -project=synteny \
    -synteny \
    -identity=80 \
    -cov=75 \
    genome1.faa genome1.gff \
    genome2.faa genome2.gff \
    genome3.faa genome3.gff
```

## Troubleshooting

### No Orthologs Found
- **Issue**: Empty or very small orthogroups
- **Solution**: Lower `-identity` and `-cov` thresholds
- **Check**: Verify input FASTA files contain valid protein sequences

### Too Many Singletons
- **Issue**: >30% of genes are singletons
- **Solution**:
  - Lower identity threshold
  - Check annotation quality
  - Verify genomes are from related taxa

### Slow Performance
- **Issue**: Long runtime on large datasets
- **Solution**:
  - Use `-p=diamond` or `-p=mmseqs`
  - Increase `-cpus`
  - Use distributed mode (`-jobs=M/N`)
  - Relax E-value threshold

### Memory Errors
- **Issue**: Out of memory during BLAST
- **Solution**:
  - Use Diamond instead of BLAST+
  - Split into smaller batches with `-jobs`
  - Increase `-e` threshold to reduce hits

## Key Features

### ProteinOrtho6 Advantages
- **Pseudo-reciprocal best hit**: More accurate than simple RBH
- **Graph-based clustering**: Handles paralogs better than pairwise methods
- **Algebraic connectivity**: Quality metric for orthogroup coherence
- **Synteny integration**: Uses gene context (PoFF extension)
- **Multiple backends**: Diamond, BLAST+, MMseqs2 support
- **Minimal dependencies**: Only 10 direct dependencies in Bioconda

### Comparison with Other Tools
- **vs MMseqs2**: More accurate paralog discrimination, slower
- **vs OrthoFinder**: Faster, less phylogenetic detail
- **vs OrthoMCL**: Simpler installation, no database required

## Benchmarks
- **Portability**: Runs on Linux, macOS, Windows (WSL)
- **Scalability**: Tested on 1000+ genomes
- **Dependencies**: Minimal (10 packages in Bioconda)
