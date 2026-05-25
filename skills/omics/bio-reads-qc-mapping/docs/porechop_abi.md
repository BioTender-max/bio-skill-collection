# Porechop - Nanopore Adapter Trimmer

## Overview

Porechop is a tool for finding and removing adapters from Oxford Nanopore reads. Adapters on the ends of reads are trimmed off, and when a read has an adapter in its middle, it is treated as chimeric and chopped into separate reads. Porechop can handle barcoded runs and demultiplex reads.

**Note:** The original developer has declared Porechop as abandonware, though it remains widely used in Nanopore pipelines. Alternative tools include Porechop_ABI for improved adapter detection.

## Official Documentation

- [Porechop GitHub Repository](https://github.com/rrwick/Porechop)
- [ARTIC Network Fork](https://github.com/artic-network/Porechop)
- [Porechop_ABI (Alternative)](https://github.com/bonsai-team/Porechop_ABI)

## Installation

```bash
# Via conda/mamba
conda install -c bioconda porechop

# Via pixi (recommended for this workflow)
pixi add porechop

# From source
git clone https://github.com/rrwick/Porechop.git
cd Porechop
python3 setup.py install
```

## Key Command-Line Flags

### Basic Syntax
```bash
porechop -i INPUT [-o OUTPUT] [options]
```

### Input/Output
- `-i <file>`, `--input <file>` - FASTA/FASTQ input or directory (required)
- `-o <file>`, `--output <file>` - Output FASTA/FASTQ (default: stdout)
- `--format <format>` - Output format (auto, fasta, fastq, fasta.gz, fastq.gz)

### Threading
- `-t <int>`, `--threads <int>` - Number of threads for adapter alignment (default: 4)

### Adapter Search
- `--adapter_threshold <float>` - Minimum % match for an adapter (default: 90.0)
- `--check_reads <int>` - Number of reads to check for adapters (default: 10000)
- `--scoring_scheme <str>` - Alignment scoring scheme (default: "3,-6,-5,-2")

### End Adapter Trimming
- `--end_size <int>` - Number of bp at read ends to search for adapters (default: 150)
- `--min_trim_size <int>` - Minimum bp to trim from read ends (default: 4)
- `--extra_end_trim <int>` - Additional bp to trim from ends (default: 2)
- `--end_threshold <float>` - Min % match for end adapters (default: 75.0)

### Middle Adapter Splitting
- `--no_split` - Skip splitting reads with middle adapters
- `--discard_middle` - Discard reads with middle adapters
- `--middle_threshold <float>` - Min % match for middle adapters (default: 85.0)
- `--extra_middle_trim_good_side <int>` - Extra bp trim on good side (default: 10)
- `--extra_middle_trim_bad_side <int>` - Extra bp trim on bad side (default: 100)
- `--min_split_read_size <int>` - Minimum size for split reads (default: 1000)

### Barcode Demultiplexing
- `-b <dir>`, `--barcode_dir <dir>` - Output directory for demultiplexed reads
- `--barcode_threshold <float>` - Min % match for barcodes (default: 75.0)
- `--barcode_diff <float>` - Min % difference between best/second barcode (default: 5.0)
- `--require_two_barcodes` - Only demultiplex reads with barcodes at both ends
- `--untrimmed` - Output untrimmed reads to file
- `--discard_unassigned` - Discard reads without barcode match

### Output Control
- `-v <int>`, `--verbosity <int>` - Progress info: 0=none, 1=some, 2=lots, 3=full (default: 1)

## Common Usage Examples

### Basic Adapter Trimming

```bash
porechop -i input.fastq -o output.fastq
```

### Trim with Multiple Threads

```bash
porechop -i input.fastq -o output.fastq -t 16
```

### Discard Chimeric Reads

```bash
porechop -i input.fastq -o output.fastq --discard_middle
```

### No Read Splitting (Trim Only)

```bash
porechop -i input.fastq -o output.fastq --no_split
```

### Output to Gzipped FASTQ

```bash
porechop -i input.fastq -o output.fastq.gz --format fastq.gz
```

### Demultiplex Barcoded Reads

```bash
porechop -i input.fastq -b demultiplexed_reads/ -t 16
```

### Demultiplex with Strict Barcode Matching

```bash
porechop -i input.fastq -b demultiplexed_reads/ \
  --barcode_threshold 80 \
  --require_two_barcodes \
  --discard_unassigned
```

### Process Directory of FASTQ Files

```bash
porechop -i fastq_directory/ -o trimmed_output.fastq -t 16
```

### Conservative Trimming (Less Aggressive)

```bash
porechop -i input.fastq -o output.fastq \
  --end_threshold 80 \
  --middle_threshold 90 \
  --extra_end_trim 0
```

### Aggressive Trimming

```bash
porechop -i input.fastq -o output.fastq \
  --end_threshold 70 \
  --extra_end_trim 5 \
  --extra_middle_trim_bad_side 150
```

### Verbose Output for Debugging

```bash
porechop -i input.fastq -o output.fastq -v 3
```

## Input/Output Formats

### Input Formats
- FASTQ (gzipped or uncompressed)
- FASTA (gzipped or uncompressed)
- Directory containing FASTQ files (processed recursively)

### Output Formats
- FASTQ (default)
- FASTA
- Gzipped versions (fastq.gz, fasta.gz)
- Outputs to stdout if no `-o` specified

### Barcode Demultiplexing Output
- Creates separate files per barcode in output directory
- Format: `BC01.fastq`, `BC02.fastq`, etc.
- `none.fastq` for reads without barcode match (unless `--discard_unassigned`)

## Performance Tips

### Threading
- Use `-t` to set threads equal to CPU cores
- Optimal: 8-16 threads for most datasets
- Adapter alignment is parallelized across threads

### Memory Usage
- Porechop has modest memory requirements
- Typically <2GB RAM for most operations
- Scales with read length and number of concurrent threads

### Speed Optimization
- Reduce `--check_reads` if adapter set is well-known (faster startup)
- Use `--no_split` if chimeric reads are rare (faster processing)
- Process gzipped files directly (automatic detection)

### Disk I/O
- Output to compressed format to save disk space
- Use pipes to avoid intermediate files
- Process input directory in one pass

## Adapter Detection

Porechop includes built-in adapters for:
- Native barcoding kits (NBD103, NBD104, NBD114, etc.)
- PCR barcoding kits (PCR12, PCR96, etc.)
- Rapid barcoding kits (RBK001, RBK004, RB096, etc.)
- Standard ONT adapters (including reverse complement)

### Adapter Search Process

1. **Initial scan**: Checks first N reads (default: 10000)
2. **Adapter identification**: Finds which adapters are present
3. **End trimming**: Searches read ends (default: 150bp) for adapters
4. **Middle detection**: Searches full read for internal adapters
5. **Splitting/trimming**: Removes or splits based on adapter location

## Parameter Recommendations

### Standard Nanopore Run
```bash
porechop -i input.fastq -o output.fastq -t 16
```

### Conservative Trimming (Keep More Data)
```bash
porechop -i input.fastq -o output.fastq \
  -t 16 \
  --end_threshold 80 \
  --middle_threshold 90 \
  --no_split
```

### Aggressive Trimming (Higher Quality)
```bash
porechop -i input.fastq -o output.fastq \
  -t 16 \
  --end_threshold 70 \
  --extra_end_trim 5 \
  --discard_middle
```

### Barcoded Run (Standard)
```bash
porechop -i input.fastq -b barcodes/ -t 16
```

### Barcoded Run (Strict)
```bash
porechop -i input.fastq -b barcodes/ \
  -t 16 \
  --barcode_threshold 80 \
  --barcode_diff 10 \
  --require_two_barcodes \
  --discard_unassigned
```

### Quick Processing (Skip Chimera Detection)
```bash
porechop -i input.fastq -o output.fastq \
  -t 16 \
  --no_split \
  --check_reads 5000
```

## Common Workflows

### Simple Adapter Trimming Pipeline
```bash
# Trim adapters
porechop -i raw_reads.fastq -o trimmed_reads.fastq -t 16

# Quality filter with Filtlong
filtlong --min_length 1000 trimmed_reads.fastq | gzip > filtered_reads.fastq.gz

# Map with minimap2
minimap2 -ax map-ont reference.fa filtered_reads.fastq.gz > mapped.sam
```

### Demultiplex and Process Each Barcode
```bash
# Demultiplex
porechop -i multiplexed.fastq -b barcodes/ -t 16

# Process each barcode
for bc in barcodes/BC*.fastq; do
    barcode=$(basename $bc .fastq)
    filtlong --min_length 1000 $bc | \
      minimap2 -ax map-ont reference.fa - | \
      samtools sort -o ${barcode}.bam
done
```

### Conservative Trim + Assembly Prep
```bash
porechop -i raw_reads.fastq -o trimmed_reads.fastq \
  -t 16 \
  --end_threshold 75 \
  --no_split

filtlong --target_bases 5000000000 \
  --min_length 5000 \
  trimmed_reads.fastq | gzip > assembly_reads.fastq.gz
```

## Alternatives and Notes

### When to Use Porechop
- Standard Nanopore adapter trimming
- Barcoded runs requiring demultiplexing
- Chimeric read detection and splitting
- Legacy pipelines with Porechop dependencies

### Alternatives to Consider
- **Porechop_ABI**: Improved ab initio adapter detection
- **Guppy**: ONT's official basecaller includes adapter trimming
- **Dorado**: Next-gen ONT basecaller with built-in adapter removal
- **Cutadapt**: General-purpose adapter trimmer (works with ONT)

### Maintenance Status
- Original Porechop is no longer maintained
- ARTIC Network fork includes minor updates
- Consider modern alternatives for new pipelines
- Still widely used and functional for standard use cases
