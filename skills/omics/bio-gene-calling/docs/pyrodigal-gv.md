# Prodigal-GV

Modified Prodigal for improved viral gene calling, especially for giant viruses.

## Official Documentation
- GitHub: https://github.com/apcamargo/prodigal-gv

## Installation

```bash
# Conda/Mamba (recommended)
conda install -c bioconda prodigal-gv

# Pre-built binaries
# Download from: https://github.com/apcamargo/prodigal-gv/releases

# From source
git clone https://github.com/apcamargo/prodigal-gv.git
cd prodigal-gv
make
```

## Key Features

- 10 additional metagenomic models for viruses
- Optimized for giant viruses (mimiviruses, chlorella viruses)
- Supports alternative genetic codes (11 and 15)
- Specialized models for gut phages and NCLDV
- Compatible with standard Prodigal usage

## Command-Line Flags

```bash
prodigal-gv [options] -i input.fna -a proteins.faa
```

**Common Options:**
- `-p meta` - Metagenomic mode (required for viral prediction)
- `-i FILE` - Input sequence file (FASTA)
- `-a FILE` - Output protein sequences
- `-d FILE` - Output DNA sequences of genes
- `-o FILE` - Output gene coordinates (GFF-like)
- `-q` - Quiet mode (suppress stderr)

## Common Usage Examples

### Standard Viral Gene Calling

```bash
prodigal-gv -p meta -i viral_genome.fna -a proteins.faa > genes.gff 2>&1
```

### Generate All Output Formats

```bash
prodigal-gv -p meta \
    -i genome.fna \
    -a proteins.faa \
    -d genes.fna \
    -o genes.gff
```

### Parallel Processing

```bash
# Using the provided parallel script
./parallel-prodigal-gv.py -t 8 -q -i genome.fna -a proteins.faa
```

## Input/Output Formats

**Input:**
- FASTA nucleotide sequences (.fna, .fasta)
- DNA sequences (single or multi-FASTA)

**Output:**
- GFF-like gene coordinates (stdout or `-o`)
- Protein sequences in FASTA (via `-a`)
- Gene nucleotide sequences in FASTA (via `-d`)
- Training info (via `-t` for reuse)

## Differences from Standard Prodigal

**Additional Metagenomic Models:**
1. Giant viruses (mimivirus-like)
2. Chlorella viruses
3. Alternative genetic codes (11, 15)
4. Gut phage optimizations
5. NCLDV (nucleo-cytoplasmic large DNA viruses)

These models improve gene calling accuracy for non-standard viral genomes.

## Performance Tips

- Always use `-p meta` for viral genomes
- Use parallel script for large datasets
- Models automatically selected based on GC content
- No training required in metagenomic mode
- Quiet mode (`-q`) reduces output overhead
