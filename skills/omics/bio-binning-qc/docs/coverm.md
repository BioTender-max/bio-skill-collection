# CoverM v0.7.0

Read alignment statistics for metagenomics - compute coverage and depth from BAM files.

## Official Documentation
- GitHub: https://github.com/wwood/CoverM
- Version: 0.7.0

## Installation

**Bioconda (recommended):**
```bash
conda install -c conda-forge -c bioconda coverm
```

**From source:**
```bash
cargo install coverm
```

**With pixi:**
```bash
pixi install -a coverm
```

## Key Command-Line Flags

| Flag | Description |
|------|-------------|
| `-m, --methods` | Coverage calculation methods (mean, relative_abundance, covered_fraction, etc.) |
| `-t` | Number of threads |
| `-o` | Output file path |
| `--coupled` | Paired-end read files (forward reverse) |
| `--genome-fasta-files` | Reference genome/contig files |
| `--bam-files` | Pre-computed BAM alignment files |
| `--output-format` | Output format (default: tab-separated) |

## Common Usage Examples

### Compute genome-level coverage from reads
```bash
coverm genome \
  --coupled sample_1.1.fq.gz sample_1.2.fq.gz \
  --genome-fasta-files genome_1.fna genome_2.fna \
  -t 8 \
  -m mean relative_abundance covered_fraction \
  -o output_coverm.tsv
```

### Compute contig-level coverage for binning
```bash
coverm contig \
  --bam-files sample1.sorted.bam sample2.sorted.bam \
  -m mean variance \
  -o contig_coverage.tsv
```

### Generate BAM files for downstream use
```bash
coverm make \
  --coupled reads_1.fq.gz reads_2.fq.gz \
  --reference contigs.fasta \
  -o alignments/ \
  -t 16
```

## Input/Output Formats

**Inputs:**
- FASTQ files (raw paired-end reads)
- FASTA files (reference genomes/contigs)
- BAM files (pre-computed alignments, must be sorted)

**Output:**
Tab-separated file with:
- Column 1: Contig/genome name
- Remaining columns: Coverage metrics per sample

Example output:
```
contig_name    sample1_mean    sample1_variance    sample2_mean    sample2_variance
contig_001     45.2            12.3                38.9            10.1
contig_002     102.5           28.7                95.3            24.2
```

## Coverage Methods

- `mean`: Average coverage depth
- `relative_abundance`: Relative abundance (coverage × length / total)
- `covered_fraction`: Fraction of bases covered
- `variance`: Variance in coverage depth
- `trimmed_mean`: Mean after removing outliers
- `covered_bases`: Number of bases with coverage
- `rpkm`, `tpm`: Normalized expression metrics

## Performance Tips

1. **Threading**: Use `-t` to specify thread count for parallel processing
2. **Pre-computed BAM**: Generate BAM files once with `coverm make`, reuse for multiple analyses
3. **Mapper selection**: CoverM supports multiple aligners (minimap2, strobealign, bwa-mem2)
4. **Filter alignments**: Use `coverm filter` to remove low-identity alignments before coverage computation
5. **Memory**: For large datasets, consider processing in batches

## Integration with MetaBAT2

MetaBAT2 expects depth files in a specific format. Generate compatible output:

```bash
# Method 1: Use jgi_summarize_bam_contig_depths (from MetaBAT2)
jgi_summarize_bam_contig_depths --outputDepth depth.txt *.bam

# Method 2: Use CoverM with mean and variance
coverm contig \
  --bam-files *.bam \
  -m mean variance \
  -o depth.txt
```

## Common Issues

- **BAM files must be sorted**: Use `samtools sort` if needed
- **Reference mismatch**: Ensure BAM files align to the same reference as contig file
- **Memory constraints**: Use streaming mode for very large datasets
