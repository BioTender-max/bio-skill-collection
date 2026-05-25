# BBMap - Short Read Aligner

## Overview

BBMap is a fast, accurate splice-aware aligner for DNA and RNA sequencing reads. It is part of the BBTools suite and is designed for speed and sensitivity with support for genomic and transcriptomic data.

## Official Documentation

- [BBMap Official Site](https://bbmap.org/)
- [BBMap Documentation](https://bbmap.org/docs.html)
- [BBMap GitHub Repository](https://github.com/BioInfoTools/BBMap)
- [Usage Guide](https://github.com/BioInfoTools/BBMap/blob/master/docs/UsageGuide.txt)

## Installation

BBMap is part of the BBTools suite. Prefer Bryce Foster's official BBTools
container for reproducible runs:

```bash
docker pull bryce911/bbtools:39.84

bbtools() {
  docker run --rm -u "$(id -u):$(id -g)" \
    -v "$PWD":/work -w /work \
    bryce911/bbtools:39.84 "$@"
}

bbtools bbmap.sh --help
```

As of 2026-05-15, `bryce911/bbtools:39.84` and `latest` point to digest
`sha256:60d73ca4d99e12434e3ef2135d7441e025272afc5493a580e365a3cbe7fcadc5`.

## Key Command-Line Flags

### Input/Output
- `ref=<file>` - Reference genome (FASTA format)
- `in=<file>` - Input reads (single-end)
- `in1=<file>` `in2=<file>` - Input reads (paired-end)
- `out=<file>` - Output SAM/BAM file
- `outu=<file>` - Unmapped reads output
- `outm=<file>` - Mapped reads output

### Mapping Parameters
- `k=<int>` - Kmer length (default: 13)
- `minid=<float>` - Minimum identity (0-1, default: 0.76)
- `maxindel=<int>` - Maximum indel length (default: 16000)
- `minhits=<int>` - Minimum number of kmer hits (default: 2)

### Speed/Sensitivity Macros
- `fast` - Fast mode (reduced sensitivity)
  - Sets: tipsearch=20, maxindel=80, minhits=2
- `slow` - Slow mode (greater sensitivity)
  - Sets: tipsearch=150, minhits=1, minratio=0.45
- `vslow` - Very slow mode (maximum sensitivity)

### Mapping Modes
- `perfectmode=t` - Only allow perfect mappings
- `semiperfectmode=t` - Allow perfect and semiperfect mappings
- `vslow=t` - Very sensitive mapping mode

### Ambiguous Read Handling
- `ambig=best` - Use best mapping only (default)
- `ambig=toss` - Discard ambiguously mapped reads
- `ambig=random` - Select random mapping
- `ambig=all` - Output all mappings

### Coverage and Statistics
- `covstats=<file>` - Per-scaffold coverage statistics
- `scafstats=<file>` - Per-scaffold mapping statistics
- `bhist=<file>` - Base composition histogram
- `qhist=<file>` - Quality histogram
- `aqhist=<file>` - Accuracy histogram

### Quality Filtering
- `minaveragequality=<int>` - Minimum average base quality
- `minlength=<int>` - Minimum read length
- `trimq=<int>` - Trim bases below this quality

### Performance
- `threads=<int>` - Number of threads (default: auto)
- `-Xmx<memory>` - Java heap memory (e.g., -Xmx20g)

## Common Usage Examples

### Basic Mapping (Single-End)

```bash
bbtools bbmap.sh ref=reference.fa in=reads.fq out=mapped.sam
```

### Paired-End Mapping

```bash
bbtools bbmap.sh ref=reference.fa \
  in1=read1.fq in2=read2.fq \
  out=mapped.sam
```

### Fast Mapping Mode

```bash
bbtools bbmap.sh ref=reference.fa \
  in=reads.fq out=mapped.sam \
  fast=t
```

### High Sensitivity Mapping

```bash
bbtools bbmap.sh ref=reference.fa \
  in=reads.fq out=mapped.sam \
  slow=t minid=0.90
```

### Mapping with Coverage Statistics

```bash
bbtools bbmap.sh ref=reference.fa \
  in1=read1.fq in2=read2.fq \
  out=mapped.sam \
  covstats=coverage.txt \
  scafstats=scaffold_stats.txt
```

### Mapping Long Reads (PacBio)

```bash
bbtools bbmap.sh -Xmx20g \
  ref=reference.fa in=pacbio.fastq \
  out=mapped.sam \
  k=7 maxlen=1000 minlen=200 \
  minratio=0.15 slow=t \
  maxindel1=40 maxindel2=400
```

### Index Reference Separately

```bash
# Build index
bbtools bbmap.sh ref=reference.fa

# Map reads using existing index
bbtools bbmap.sh in=reads.fq out=mapped.sam
```

### Filter by Identity and Length

```bash
bbtools bbmap.sh ref=reference.fa \
  in=reads.fq out=mapped.sam \
  minid=0.95 minlength=100
```

### Output BAM Format

```bash
bbtools bbmap.sh ref=reference.fa \
  in=reads.fq out=mapped.bam
```

## Input/Output Formats

### Reference Formats
- FASTA (uncompressed or gzipped)

### Read Input Formats
- FASTQ (gzipped or uncompressed)
- FASTA
- SAM/BAM

### Output Formats
- SAM (default)
- BAM (specify .bam extension)

### Index Files
- BBMap creates index files in `/ref/` subdirectory
- Index is reused automatically when same reference is used

## Performance Tips

### Memory Allocation
- Use `-Xmx<memory>` to set heap size
- Recommended: 85% of available physical memory
- Example: `-Xmx27g` for 32GB machine
- Minimum: 3-4GB for small genomes

### Indexing Strategy
- Build index once, reuse for multiple runs
- Index is stored in `/ref/` by default
- Use `nodisk=t` to keep index in memory (faster, requires more RAM)

### Threading
- BBMap scales well with multiple threads
- Optimal: 4-16 threads for most datasets
- Beyond 16 threads shows diminishing returns

### Speed Optimization
- Use `fast=t` for 2-3x speed increase with minimal sensitivity loss
- Reduce `maxindel` if you expect few large indels
- Increase `minhits` for faster mapping with higher identity reads
- Use `semiperfectmode=t` for ultra-fast mapping of high-quality reads

### Disk I/O
- Use compressed input to reduce disk bottleneck
- Consider RAM disk for index files on memory-rich systems
- Output to BAM instead of SAM to save disk space

## Parameter Recommendations

### Illumina Short Reads (High Quality)
```bash
fast=t minid=0.95 maxindel=100
```

### Illumina Short Reads (Standard)
```bash
minid=0.90 maxindel=100 minhits=2
```

### Divergent Reference Mapping
```bash
slow=t minid=0.85 minratio=0.40
```

### RNA-Seq Mapping
```bash
intronlen=10 ambig=random minid=0.95
```

### PacBio/Nanopore Long Reads
```bash
k=7 slow=t minid=0.70 maxindel1=40 maxindel2=400 minratio=0.15
```

## Coverage Statistics Output

The `covstats` output includes:
- Per-scaffold coverage depth
- Percent covered
- Read counts
- Average fold coverage

The `scafstats` output includes:
- Mapped reads per scaffold
- Mapping quality statistics
- Error rates
