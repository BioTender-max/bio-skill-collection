# CheckV Usage Guide

## Official Documentation
- PyPI: https://pypi.org/project/checkv/
- Bitbucket: https://bitbucket.org/berkeleylab/checkv
- Publication: Nayfach, S., et al. (2020). "CheckV assesses the quality and completeness of metagenome-assembled viral genomes." Nature Biotechnology

## Overview
CheckV is a fully automated tool for assessing the quality of single-contig viral genomes. It identifies closed genomes, estimates completeness of genome fragments, and removes flanking host regions from integrated proviruses.

## Installation

### Conda (Recommended)
```bash
conda install -c conda-forge -c bioconda checkv
```

### Pip
```bash
pip install checkv
```

Note: When using pip, you must separately install:
- DIAMOND v2.1.8 (avoid v2.1.9 - known issues)
- HMMER v3.3
- Prodigal-gv v2.6.3

### Docker
```bash
docker pull antoniopcamargo/checkv
```

## Database Setup

Download and configure database:
```bash
checkv download_database ./
export CHECKVDB=/path/to/checkv-db
```

## Key Commands & Flags

### Full Pipeline (Recommended)
```bash
checkv end_to_end INPUT OUTPUT [OPTIONS]
```

### Individual Modules

| Command | Purpose |
|---------|---------|
| `checkv contamination` | Identify and remove host contamination |
| `checkv completeness` | Estimate genome completeness |
| `checkv complete_genomes` | Predict closed genomes based on terminal repeats |
| `checkv quality_summary` | Generate integrated quality report |

### Common Options

| Flag | Description |
|------|-------------|
| `-t, --threads` | Number of threads (default: 1) |
| `-d, --database` | Path to CheckV database |
| `--restart` | Restart from last incomplete step |
| `--quiet` | Suppress progress messages |

## Common Usage Examples

### Standard quality assessment
```bash
checkv end_to_end viral_contigs.fna output_dir -t 16
```

### With custom database path
```bash
checkv end_to_end viral_contigs.fna output_dir -t 16 -d /path/to/checkv-db
```

### Run individual modules
```bash
# Step 1: Check for contamination
checkv contamination viral_contigs.fna output_dir -t 16

# Step 2: Estimate completeness
checkv completeness viral_contigs.fna output_dir -t 16

# Step 3: Identify complete genomes
checkv complete_genomes viral_contigs.fna output_dir

# Step 4: Generate summary
checkv quality_summary viral_contigs.fna output_dir
```

## Input/Output

### Input Format
- FASTA file with viral contig sequences
- Typically output from viral detection tools (geNomad, VirSorter2, etc.)

### Key Output Files

| File | Description |
|------|-------------|
| `quality_summary.tsv` | **Primary output** - integrated results with quality tiers |
| `completeness.tsv` | Detailed completeness estimates for each contig |
| `contamination.tsv` | Host contamination details and trimmed coordinates |
| `complete_genomes.tsv` | List of predicted closed/complete genomes |
| `proviruses.fna` | Extracted proviral sequences with host regions removed |
| `viruses.fna` | High-quality viral sequences |

### Quality Tiers

CheckV classifies sequences into five quality categories (consistent with MIUViG standards):

| Tier | Completeness | Description |
|------|--------------|-------------|
| Complete | 100% | Closed genomes with terminal repeats |
| High-quality | >90% | Nearly complete genomes |
| Medium-quality | 50-90% | Partial genomes, suitable for most analyses |
| Low-quality | <50% | Fragmentary genomes |
| Undetermined | N/A | No completeness estimate available |

## Performance Tips

1. Use multiple threads (`-t 16` or higher) for faster processing
2. Pre-filter contigs by length (>5kb recommended) to reduce runtime
3. Ensure sufficient memory for DIAMOND searches (4-8GB typical)
4. Use `--restart` to resume interrupted runs
5. Set `CHECKVDB` environment variable to avoid specifying database path repeatedly

## Integration with Viromics Workflow

CheckV is the quality control step after viral detection:
1. Input: Viral contigs from geNomad or similar tools
2. Output: Quality-filtered viral sequences with completeness estimates
3. Downstream: High/medium quality sequences proceed to vConTACT3 for clustering
4. Filtering: Apply project-specific thresholds (e.g., >50% complete, <5% contamination)

## Troubleshooting

- **Low completeness estimates**: May indicate truly fragmentary genomes or novel viral groups
- **High contamination**: Check provirus predictions; may need manual curation
- **No quality tier assigned**: Sequence may be too divergent from reference database
- **DIAMOND errors**: Verify DIAMOND version (use v2.1.8, not v2.1.9)
