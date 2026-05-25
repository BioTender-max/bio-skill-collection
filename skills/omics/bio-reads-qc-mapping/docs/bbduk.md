# BBDuk - Quality Control and Adapter Trimming

## Overview

BBDuk (Decontamination Using Kmers) is a high-performance tool from BBTools that combines quality-trimming, filtering, adapter-trimming, contaminant-filtering via kmer matching, sequence masking, GC-filtering, length filtering, entropy-filtering, and various other operations in a single pass.

## Official Documentation

- [BBDuk Guide - JGI DOE](https://jgi.doe.gov/data-and-tools/software-tools/bbtools/bb-tools-user-guide/bbduk-guide/)
- [BBDuk Guide - GitHub](https://github.com/BioInfoTools/BBMap/blob/master/docs/guides/BBDukGuide.txt)

## Installation

BBDuk is part of the BBTools suite. Prefer Bryce Foster's official BBTools
container for reproducible runs:

```bash
docker pull bryce911/bbtools:39.84

bbtools() {
  docker run --rm -u "$(id -u):$(id -g)" \
    -v "$PWD":/work -w /work \
    bryce911/bbtools:39.84 "$@"
}

bbtools bbduk.sh --help
```

As of 2026-05-15, `bryce911/bbtools:39.84` and `latest` point to digest
`sha256:60d73ca4d99e12434e3ef2135d7441e025272afc5493a580e365a3cbe7fcadc5`.

## Key Command-Line Flags

### Input/Output
- `in=<file>` - Input reads (single-end)
- `in1=<file>` `in2=<file>` - Input reads (paired-end, dual files)
- `out=<file>` - Output reads (single-end)
- `out1=<file>` `out2=<file>` - Output reads (paired-end, dual files)
- `interleaved` - Override autodetection of paired reads in single file

### Kmer Operations
- `k=<int>` - Kmer size (default: 27)
- `mink=<int>` - Look for shorter kmers at read ends (default: 8)
- `hdist=<int>` - Hamming distance for mismatches (default: 0)
- `ref=<file>` - Reference file for adapter/contaminant sequences

### Trimming Modes
- `ktrim=r` - Right-trim (3' adapters)
- `ktrim=l` - Left-trim (5' adapters)
- `ktrim=n` - Don't trim, just mask or filter
- `qtrim=rl` - Quality-trim both ends
- `qtrim=r` - Quality-trim right end only
- `qtrim=l` - Quality-trim left end only

### Quality Parameters
- `trimq=<float>` - Trim regions with average quality below this (default: 6)
- `minlength=<int>` - Discard reads shorter than this (default: 10)
- `minavgquality=<int>` - Discard reads with average quality below this

### Position-Based Trimming
- `forcetrimleft=<int>` (ftl) - Trim this many bases from left end
- `forcetrimright=<int>` (ftr) - Trim this many bases from right end
- `forcetrimright2=<int>` (ftr2) - Trim this many bases from right end of read 2

### Filtering Options
- `minlen=<int>` - Minimum read length
- `maxns=<int>` - Maximum number of Ns allowed
- `maq=<float>` - Minimum average quality
- `maxgc=<float>` - Maximum GC content (0-1)
- `mingc=<float>` - Minimum GC content (0-1)

### Performance Flags
- `threads=<int>` - Number of threads (default: auto)
- `tbo` - Trim adapters based on pair overlap detection
- `tpe` - Trim both reads to same length (for pairs)

## Common Usage Examples

### Basic Adapter Trimming (Single-End)

```bash
bbtools bbduk.sh -Xmx1g \
  in=reads.fq \
  out=clean.fq \
  ref=adapters.fa \
  ktrim=r k=23 mink=11 hdist=1
```

### Adapter Trimming (Paired-End)

```bash
bbtools bbduk.sh -Xmx1g \
  in1=read1.fq in2=read2.fq \
  out1=clean1.fq out2=clean2.fq \
  ref=adapters.fa \
  ktrim=r k=23 mink=11 hdist=1 \
  tpe tbo
```

### Quality and Adapter Trimming Combined

```bash
bbtools bbduk.sh -Xmx1g \
  in1=read1.fq in2=read2.fq \
  out1=clean1.fq out2=clean2.fq \
  ref=adapters.fa \
  ktrim=r k=23 mink=11 hdist=1 \
  qtrim=rl trimq=20 minlength=50 \
  tpe tbo
```

### Contaminant Filtering

```bash
bbtools bbduk.sh -Xmx1g \
  in=reads.fq \
  out=filtered.fq \
  ref=phix174_ill.ref.fa.gz \
  k=31 hdist=1
```

### Quality Filtering Only

```bash
bbtools bbduk.sh -Xmx1g \
  in=reads.fq \
  out=filtered.fq \
  qtrim=rl trimq=20 \
  minlength=50 \
  minavgquality=20 \
  maxns=2
```

## Input/Output Formats

### Supported Input Formats
- FASTQ (gzipped or uncompressed)
- FASTA
- SAM/BAM (reads only)

### Output Formats
- FASTQ (default)
- FASTA
- SAM

### Compression
- Automatically detects gzipped input
- Output can be gzipped by using `.gz` extension

## Performance Tips

### Memory Allocation
- Use `-Xmx1g` for small or no reference files
- For large references, use ~85% of physical memory (e.g., `-Xmx27g` on 32GB machine)
- Example: `bbtools bbduk.sh -Xmx27g ...`

### Threading
- BBDuk scales well with multiple threads
- Use `threads=auto` or specify manually with `threads=<n>`
- Diminishing returns beyond 8-12 threads for most operations

### Speed Optimization
- Use larger k-mer values (k=25-27) for faster processing
- Disable unnecessary operations (e.g., if only trimming adapters, don't use quality filtering)
- Process gzipped files directly to save disk I/O

### Disk I/O
- Use compressed input/output to reduce disk bottlenecks
- Consider using fast storage (SSD) for temporary files
- Use pipes between operations to avoid writing intermediate files

## Parameter Recommendations

### Illumina Short Reads
```bash
k=23 mink=11 hdist=1 qtrim=rl trimq=20 minlength=50
```

### Aggressive Quality Filtering
```bash
qtrim=rl trimq=25 minlength=75 minavgquality=25 maxns=0
```

### Conservative Quality Filtering
```bash
qtrim=rl trimq=15 minlength=35 minavgquality=15 maxns=5
```
