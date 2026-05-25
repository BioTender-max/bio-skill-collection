# Tool Documentation

This directory contains comprehensive usage guides for the bioinformatics tools used in the bio-reads-qc-mapping skill.

**Last Updated:** 2026-05-15

## Tools Covered

### Short Read Processing
- **[bbduk.md](bbduk.md)** - Quality control, adapter trimming, and contamination filtering
- **[bbmap.md](bbmap.md)** - Short read alignment to reference genomes

### Long Read Processing
- **[porechop_abi.md](porechop_abi.md)** - Oxford Nanopore adapter trimming and demultiplexing
- **[filtlong.md](filtlong.md)** - Long read quality filtering (Nanopore/PacBio)

### Universal Read Mapping
- **[minimap2.md](minimap2.md)** - Versatile aligner for both short and long reads

## Quick Reference

| Tool | Primary Use | Input | Output |
|------|-------------|-------|--------|
| bbduk | Short read QC/trimming | FASTQ | FASTQ |
| bbmap | Short read mapping | FASTQ | SAM/BAM |
| Porechop_ABI | ONT adapter trimming | FASTQ | FASTQ |
| Filtlong | Long read filtering | FASTQ | FASTQ |
| minimap2 | Universal read mapping | FASTQ/FASTA | SAM/PAF |

## Common Workflows

### Short Read QC and Mapping
```bash
bbtools() {
  docker run --rm -u "$(id -u):$(id -g)" \
    -v "$PWD":/work -w /work \
    bryce911/bbtools:39.84 "$@"
}

# 1. Quality control and adapter trimming
bbtools bbduk.sh in1=R1.fq in2=R2.fq out1=clean_R1.fq out2=clean_R2.fq \
  ref=adapters.fa ktrim=r k=23 mink=11 hdist=1 qtrim=rl trimq=20

# 2. Map to reference
bbtools bbmap.sh ref=reference.fa in1=clean_R1.fq in2=clean_R2.fq out=mapped.sam
```

### Nanopore Read QC and Mapping
```bash
# 1. Trim adapters
porechop_abi -i raw.fastq -o trimmed.fastq -t 16

# 2. Quality filter
filtlong --min_length 1000 --keep_percent 90 trimmed.fastq | gzip > filtered.fastq.gz

# 3. Map to reference
minimap2 -ax map-ont reference.fa filtered.fastq.gz > mapped.sam
```

### PacBio Read QC and Mapping
```bash
# 1. Quality filter
filtlong --min_length 1000 --keep_percent 90 raw.fastq | gzip > filtered.fastq.gz

# 2. Map to reference (HiFi)
minimap2 -ax map-hifi reference.fa filtered.fastq.gz > mapped.sam
```

## Installation

Run BBTools programs through Bryce Foster's official Docker image. As of
2026-05-15, `bryce911/bbtools:39.84` and `latest` point to digest
`sha256:60d73ca4d99e12434e3ef2135d7441e025272afc5493a580e365a3cbe7fcadc5`.

Install non-BBTools dependencies via conda/mamba or pixi:

```bash
# BBTools container
docker pull bryce911/bbtools:39.84

# Other tools
conda install -c bioconda minimap2 filtlong porechop_abi
pixi add minimap2 filtlong porechop_abi
```

## Documentation Sources

- **bbduk/bbmap**: [BBTools JGI DOE](https://jgi.doe.gov/data-and-tools/software-tools/bbtools/) | [GitHub](https://github.com/BioInfoTools/BBMap)
- **minimap2**: [GitHub](https://github.com/lh3/minimap2) | [Manual](https://lh3.github.io/minimap2/minimap2.html)
- **Filtlong**: [GitHub](https://github.com/rrwick/Filtlong)
- **Porechop_ABI**: [GitHub](https://github.com/bonsai-team/Porechop_ABI) (actively maintained successor to the unmaintained Porechop)

## Performance Guidelines

### Memory Requirements
| Tool | Typical RAM | Notes |
|------|-------------|-------|
| bbduk | 1-4 GB | Small references; 85% of RAM for large refs |
| bbmap | 4-32 GB | Depends on reference size |
| minimap2 | 4-16 GB | Use -I flag to limit memory |
| Filtlong | 10-20x input | ~10-20 bytes per input base |
| Porechop_ABI | <2 GB | Modest requirements |

### Threading Recommendations
- **bbduk/bbmap**: 4-12 threads (diminishing returns beyond 12)
- **minimap2**: 8-16 threads optimal
- **Porechop_ABI**: 8-16 threads optimal
- **Filtlong**: Single-threaded only

### Speed Optimization Tips
1. Use compressed input/output directly (all tools support gzip)
2. Pre-build indices for repeated mapping operations
3. Use appropriate presets for your data type
4. Pipe between tools to avoid intermediate files
5. Use fast local storage (SSD) for temporary files

## File Format Support

| Format | bbduk | bbmap | minimap2 | Filtlong | Porechop_ABI |
|--------|-------|-------|----------|----------|----------|
| FASTQ | ✓ | ✓ | ✓ | ✓ | ✓ |
| FASTQ.gz | ✓ | ✓ | ✓ | ✓ | ✓ |
| FASTA | ✓ | ✓ | ✓ | - | ✓ |
| SAM | ✓ (in) | ✓ | ✓ (out) | - | - |
| BAM | ✓ (in) | ✓ | - | - | - |
| PAF | - | - | ✓ (out) | - | - |

## Getting Help

Each tool provides built-in help:

```bash
bbtools() {
  docker run --rm -u "$(id -u):$(id -g)" \
    -v "$PWD":/work -w /work \
    bryce911/bbtools:39.84 "$@"
}

bbtools bbduk.sh --help
bbtools bbmap.sh --help
minimap2 --help
filtlong --help
porechop_abi --help
```

For detailed usage examples and parameter recommendations, see the individual tool documentation files in this directory.
