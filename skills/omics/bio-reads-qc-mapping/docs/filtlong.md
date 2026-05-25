# Filtlong - Long Read Quality Filtering

## Overview

Filtlong is a tool for filtering long reads by quality. It can take a set of long reads and produce a smaller, better subset using both read length (longer is better) and read identity (higher is better) when choosing which reads pass the filter. Works with both Nanopore and PacBio data.

## Official Documentation

- [Filtlong GitHub Repository](https://github.com/rrwick/Filtlong)
- [Filtlong README](https://github.com/rrwick/Filtlong/blob/main/README.md)

## Installation

```bash
# Via conda/mamba
conda install -c bioconda filtlong

# Via pixi (recommended for this workflow)
pixi add filtlong

# From source
git clone https://github.com/rrwick/Filtlong.git
cd Filtlong
make
```

## Key Command-Line Flags

### Basic Syntax
```bash
filtlong [options] input.fastq.gz | gzip > output.fastq.gz
```

### Output Thresholds
- `--min_length <int>` (or `-l`) - Discard reads shorter than this length (e.g., 1000)
- `--keep_percent <float>` (or `-p`) - Keep only the best percent of reads (by bp, not count)
- `--target_bases <int>` (or `-t`) - Remove worst reads until only this many bases remain
- `--min_mean_q <float>` - Discard reads with mean quality below this threshold
- `--min_window_q <float>` - Discard reads with window quality below this threshold

### External References
- `--assembly <file>` (or `-a`) - Reference assembly in FASTA format
- `--illumina_1 <file>` (or `-1`) - Illumina reads R1 (for quality assessment)
- `--illumina_2 <file>` (or `-2`) - Illumina reads R2 (for quality assessment)

### Read Modification
- `--trim` - Trim bases from start/end that don't match reference kmers
- `--split <int>` - Split reads when this many consecutive bases fail to match reference
- `--window_size <int>` - Window size for quality filtering (default: 250)

### Score Weights
- `--length_weight <float>` - Weight for length score (default: 1)
- `--mean_q_weight <float>` - Weight for mean quality score (default: 1)
- `--window_q_weight <float>` - Weight for window quality score (default: 1)

### Output Control
- `--verbose` - Verbose output to stderr
- `--version` - Display version and exit

## Common Usage Examples

### Basic Length Filtering

```bash
filtlong --min_length 1000 input.fastq.gz | gzip > filtered.fastq.gz
```

### Keep Best Reads by Percentage

```bash
filtlong --keep_percent 90 input.fastq.gz | gzip > filtered.fastq.gz
```

### Target Specific Coverage

```bash
# Keep best reads totaling 500 Mbp
filtlong --target_bases 500000000 input.fastq.gz | gzip > filtered.fastq.gz
```

### Quality-Based Filtering

```bash
filtlong --min_mean_q 10 --min_window_q 10 \
  input.fastq.gz | gzip > filtered.fastq.gz
```

### Reference-Guided Filtering

```bash
filtlong --assembly reference.fasta \
  --min_length 1000 \
  input.fastq.gz | gzip > filtered.fastq.gz
```

### Illumina-Assisted Filtering

```bash
filtlong \
  --illumina_1 illumina_R1.fastq.gz \
  --illumina_2 illumina_R2.fastq.gz \
  --min_length 1000 \
  input.fastq.gz | gzip > filtered.fastq.gz
```

### Trim Low-Quality Ends

```bash
filtlong --assembly reference.fasta \
  --trim \
  --min_length 1000 \
  input.fastq.gz | gzip > filtered.fastq.gz
```

### Split Chimeric Reads

```bash
filtlong --assembly reference.fasta \
  --split 500 \
  --min_length 1000 \
  input.fastq.gz | gzip > filtered.fastq.gz
```

### Aggressive Filtering for High-Quality Subset

```bash
filtlong \
  --min_length 5000 \
  --keep_percent 50 \
  --min_mean_q 12 \
  input.fastq.gz | gzip > filtered.fastq.gz
```

### Combined Filtering Strategy

```bash
filtlong \
  --assembly reference.fasta \
  --illumina_1 illumina_R1.fastq.gz \
  --illumina_2 illumina_R2.fastq.gz \
  --min_length 1000 \
  --keep_percent 90 \
  --trim \
  input.fastq.gz | gzip > filtered.fastq.gz
```

## Input/Output Formats

### Input Formats
- FASTQ (gzipped or uncompressed)
- Supports both Nanopore and PacBio data
- Can handle multiple input files (concatenated)

### Output Format
- FASTQ (typically piped to gzip)
- Writes to stdout by default

### Reference Formats
- FASTA for `--assembly`
- FASTQ (gzipped or uncompressed) for Illumina reads

## Performance Tips

### Memory Usage
- Filtlong loads all reads into memory for scoring
- Memory requirement: ~10-20 bytes per base of input
- For 10GB of reads, expect ~100-200GB RAM usage
- Consider filtering in batches for very large datasets

### Processing Speed
- Single-threaded operation
- Speed depends on:
  - Read count and total bases
  - Whether external references are used
  - Trimming/splitting operations

### Optimization Strategies
- Use `--target_bases` instead of `--keep_percent` when possible (faster)
- Pre-filter by length first if you have a hard length cutoff
- Avoid `--trim` and `--split` if not needed (significant slowdown)
- Process gzipped files directly (no need to decompress)

### Pipeline Integration
- Use pipes to avoid writing intermediate files
- Combine with other tools efficiently:

```bash
# Filtlong → minimap2 → samtools
filtlong --min_length 1000 input.fastq.gz | \
  minimap2 -ax map-ont reference.fa - | \
  samtools sort -o output.bam
```

## Scoring System

Filtlong assigns each read a quality score based on:

1. **Length score** - Longer reads score higher
2. **Mean quality score** - Higher average base quality
3. **Window quality score** - Consistent quality across read

### With External References

When using `--assembly` or Illumina reads:
- Reads are scored based on kmer matches to reference
- Matches increase score, mismatches decrease score
- Helps identify high-quality reads without relying on quality scores alone

### Score Weights

Adjust relative importance:
```bash
# Emphasize length over quality
filtlong --length_weight 2 --mean_q_weight 1 input.fastq.gz

# Emphasize quality over length
filtlong --length_weight 1 --mean_q_weight 3 input.fastq.gz
```

## Parameter Recommendations

### Nanopore Genomic DNA (Standard)
```bash
filtlong --min_length 1000 --keep_percent 90
```

### Nanopore Genomic DNA (High Quality)
```bash
filtlong --min_length 5000 --keep_percent 50 --min_mean_q 10
```

### PacBio CLR
```bash
filtlong --min_length 500 --keep_percent 90
```

### PacBio HiFi (Less Aggressive)
```bash
filtlong --min_length 1000 --keep_percent 95 --min_mean_q 15
```

### Target Coverage (e.g., 50X for 100 Mbp genome)
```bash
filtlong --target_bases 5000000000 --min_length 1000
```

### Reference-Guided (Best Quality)
```bash
filtlong \
  --assembly reference.fasta \
  --illumina_1 R1.fastq.gz \
  --illumina_2 R2.fastq.gz \
  --min_length 1000 \
  --keep_percent 75 \
  --trim
```

### Quick Pre-Filter (Length Only)
```bash
filtlong --min_length 1000
```

## Common Workflows

### Pre-Assembly Filtering
```bash
# Filter for best long reads before assembly
filtlong \
  --target_bases 5000000000 \
  --min_length 5000 \
  --verbose \
  raw_reads.fastq.gz | gzip > filtered_reads.fastq.gz
```

### Hybrid Assembly Preparation
```bash
# Use Illumina reads to assess long read quality
filtlong \
  --illumina_1 illumina_R1.fastq.gz \
  --illumina_2 illumina_R2.fastq.gz \
  --min_length 2000 \
  --keep_percent 80 \
  nanopore_reads.fastq.gz | gzip > filtered_nanopore.fastq.gz
```

### Polishing Read Selection
```bash
# Select high-quality reads for polishing
filtlong \
  --assembly draft_assembly.fasta \
  --min_length 1000 \
  --keep_percent 90 \
  --trim \
  reads.fastq.gz | gzip > polishing_reads.fastq.gz
```
