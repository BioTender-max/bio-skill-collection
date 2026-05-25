# vConTACT3 Usage Guide

## Official Documentation
- ReadTheDocs: https://vcontact3.readthedocs.io/
- Bitbucket: https://bitbucket.org/MAVERICLab/vcontact3

## Overview
vConTACT3 is a viral genome clustering and taxonomic assignment tool that improves upon previous versions through enhanced speed, scalability, and accuracy. It uses gene-sharing networks and protein cluster analysis for hierarchical viral classification.

## Installation

### Bioconda/Mamba (New Environment - Recommended)
```bash
mamba create --name vcontact3 python=3.10
mamba activate vcontact3
mamba install -c bioconda vcontact3
```

### Bioconda/Mamba (Base Environment)
```bash
mamba install -c bioconda vcontact3
```

Requires Python >=3.10 and <3.12

### Pip Installation (Latest Version)
```bash
git clone https://bitbucket.org/MAVERICLab/vcontact3.git
cd vcontact3
python -m pip install .
```

Note: MMSeqs2 must be separately installed when using pip

### Requirements File Method
```bash
git clone https://bitbucket.org/MAVERICLab/vcontact3.git
cd vcontact3
mamba install -c bioconda --file requirements.txt
pip install .
```

### Optional: ANI Export Support
```bash
pip install vclust
```

## Key Commands & Flags

### Main Subcommands

| Command | Purpose |
|---------|---------|
| `vcontact3 version` | Display current version |
| `vcontact3 prepare_databases` | Download and setup reference databases |
| `vcontact3 run` | Perform clustering and taxonomic assignment |

### Run Command Options

| Flag | Description |
|------|-------------|
| `--nucleotide` | Input nucleotide sequence file (FASTA) |
| `--proteins` | Pre-predicted protein sequences (FASTA) |
| `--gene2genome` | Gene-to-genome mapping file (TSV) |
| `--len-nucleotide` | Genome length data (TSV) |
| `--output` | Output directory for results |
| `--db-domain` | Database domain selection (e.g., prokaryotes) |
| `--exports` | Output format types (graphml, d3js, completeness) |
| `-t, --threads` | Number of threads for parallel processing |
| `-h, --help` | Display help message |

## Common Usage Examples

### Basic nucleotide input workflow
```bash
vcontact3 run --nucleotide genomes.fna --output results_dir
```

### Protein-based workflow
```bash
vcontact3 run \
  --proteins proteins.faa \
  --gene2genome gene2genome.tsv \
  --len-nucleotide genome_lengths.tsv \
  --output results_dir
```

### Custom configuration with multiple exports
```bash
vcontact3 run \
  --nucleotide genomes.fna \
  --db-domain prokaryotes \
  --exports graphml d3js completeness \
  --output results_dir
```

### Database preparation
```bash
vcontact3 prepare_databases --output-dir ./vcontact3_db
```

### Multi-threaded analysis
```bash
vcontact3 run \
  --nucleotide viral_genomes.fna \
  --output results \
  -t 32
```

## Input/Output

### Input Formats

**Nucleotide mode:**
- FASTA file with viral genome sequences
- Simplest workflow for most users

**Protein mode (advanced):**
- `--proteins`: FASTA with predicted proteins
- `--gene2genome`: TSV mapping protein IDs to genome IDs
- `--len-nucleotide`: TSV with genome lengths

### Output Files

Located in specified output directory:
- **genome_by_genome_overview.csv** - Main clustering results
- **viral_cluster_overview.csv** - Cluster composition and taxonomy
- **membership.tsv** - Genome-to-cluster assignments
- **taxonomy_assignments.tsv** - Taxonomic classifications
- **network files** - GraphML/D3.js network visualizations (if requested)
- **ANI matrices** - Genome similarity data (if vclust installed)
- **completeness reports** - Quality metrics (if requested)

## Performance Tips

1. Use `--nucleotide` mode for simplest workflow
2. Increase thread count (`-t`) for large datasets
3. Use protein mode only if you have pre-computed gene calls
4. Install vclust for ANI-based similarity analysis
5. Limit export formats to only what you need to reduce runtime
6. Pre-filter low-quality genomes using CheckV before clustering

## Integration with Viromics Workflow

vConTACT3 performs clustering and taxonomic assignment after quality control:
1. Input: High/medium quality viral genomes from CheckV
2. Analysis: Gene-sharing network construction and hierarchical clustering
3. Output: Genome clusters and taxonomic assignments
4. Downstream: Use clusters for diversity analysis and taxonomy for ecological interpretation

## Platform Compatibility

- Linux x86_64: Fully supported
- Intel Macs: Expected to work
- Apple Silicon: May require Rosetta terminal emulation or compilation from source

## Troubleshooting

- **Memory issues**: Reduce dataset size or use more powerful hardware
- **MMSeqs2 not found (pip install)**: Install MMSeqs2 separately from source
- **Python version errors**: Ensure Python 3.10 or 3.11 (not 3.12+)
- **Database errors**: Run `vcontact3 prepare_databases` to download references
