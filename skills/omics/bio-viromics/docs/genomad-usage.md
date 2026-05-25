# geNomad Usage Guide

## Official Documentation
- Primary: https://portal.nersc.gov/genomad/
- GitHub: https://github.com/apcamargo/genomad
- Citation: Camargo, A. P., et al. (2023). "Identification of mobile genetic elements with geNomad." Nature Biotechnology, DOI: 10.1038/s41587-023-01953-y

## Overview
geNomad identifies virus and plasmid genomes from nucleotide sequences with state-of-the-art classification performance. It provides taxonomic assignment using the latest ICTV taxonomy and includes functional annotation for identified mobile genetic elements.

## Installation

### Pixi (Recommended)
```bash
pixi global install -c conda-forge -c bioconda genomad
```

### Mamba (Isolated Environment)
```bash
mamba create -n genomad -c conda-forge -c bioconda genomad
mamba activate genomad
```

### Docker
```bash
docker pull antoniopcamargo/genomad
docker run --rm -ti -v "$(pwd):/app" antoniopcamargo/genomad
```

## Database Setup

Download required database before first use:
```bash
genomad download-database .
```

The database directory (`genomad_db`) contains marker profiles, taxonomic data, and functional annotations.

## Key Commands & Flags

### Main Command
```bash
genomad end-to-end [OPTIONS] INPUT OUTPUT DATABASE
```

### Important Flags

| Flag | Description |
|------|-------------|
| `--cleanup` | Remove intermediate files to save storage space |
| `--splits N` | Divide database searches into N chunks to reduce memory usage |
| `--relaxed` | Disable post-classification filters for lenient predictions |
| `--conservative` | Apply aggressive filters for strict, high-confidence results |
| `-t, --threads` | Number of threads to use for parallel processing |

## Common Usage Examples

### Basic viral detection
```bash
genomad end-to-end input.fna.gz output_dir genomad_db
```

### Memory-optimized run with cleanup
```bash
genomad end-to-end --cleanup --splits 8 input.fna.gz output_dir genomad_db
```

### Conservative mode for high-confidence results
```bash
genomad end-to-end --conservative --cleanup input.fna.gz output_dir genomad_db
```

### Relaxed mode for metatranscriptomes
```bash
genomad end-to-end --relaxed --splits 8 metatranscriptome.fna.gz output_dir genomad_db
```

## Input/Output

### Input Formats
- FASTA files (nucleotide sequences)
- Compressed formats: `.gz`, `.bz2`, `.xz`
- Works with: isolate genomes, metagenomes, metatranscriptomes

### Output Files
Located in specified output directory:
- Summary files with classification results
- FASTA sequences of identified viruses/plasmids
- Gene annotations and functional predictions
- Protein predictions
- Taxonomic assignments

## Performance Tips

1. Use `--splits` to reduce memory usage on large datasets
2. Enable `--cleanup` to minimize disk space usage
3. Adjust thread count based on available CPU cores
4. Use `--conservative` for publication-quality results
5. Use `--relaxed` for exploratory analysis or diverse samples
6. Compress input files to reduce I/O overhead

## Integration with Viromics Workflow

geNomad serves as the initial viral detection step in the bio-viromics pipeline:
1. Identifies candidate viral contigs from assembly
2. Provides initial taxonomic classification
3. Outputs cleaned viral sequences for downstream QC (CheckV)
4. Generates annotations for functional analysis
