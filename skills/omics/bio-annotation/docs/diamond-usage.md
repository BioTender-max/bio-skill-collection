# DIAMOND Usage Guide

## Overview

DIAMOND is an accelerated BLAST-compatible local sequence aligner designed for high-performance analysis of large sequence datasets. It achieves 100x-10,000x speedup compared to BLAST while maintaining similar sensitivity.

## Official Documentation

- GitHub Repository: https://github.com/bbuchfink/diamond
- Official Website: http://www.diamondsearch.org
- Documentation: https://github.com/bbuchfink/diamond_docs/blob/master/Documentation.MD
- Citation: https://doi.org/10.1038/s41592-021-01101-x (Nature Methods 2021)

## Installation

### Binary Download (Recommended)
```bash
wget http://github.com/bbuchfink/diamond/releases/download/v2.1.18/diamond-linux64.tar.gz
tar xzf diamond-linux64.tar.gz
```

### Conda/Bioconda
```bash
conda install -c bioconda -c conda-forge diamond=2.1.18
```

### Other Methods
- FreeBSD: `pkg install diamond`
- Docker containers available
- Compile from source with `-DCMAKE_BUILD_MARCH=native` for optimal performance

## Key Commands

### makedb - Build Database
```bash
diamond makedb --in reference.faa --db reference
```

With taxonomy:
```bash
diamond makedb --in reference.faa --db reference \
  --taxonmap prot.accession2taxid.gz \
  --taxonnodes nodes.dmp \
  --taxonnames names.dmp
```

### blastp - Protein vs Protein Alignment
```bash
diamond blastp --query proteins.faa --db reference.dmnd \
  --out results.tsv --outfmt 6 --threads 8
```

### blastx - Translated DNA vs Protein Alignment
```bash
diamond blastx --query reads.fna --db reference.dmnd \
  --out results.tsv --outfmt 6 --threads 8
```

## Key Command-Line Options

### General Options
- `--threads (-p)` - Number of CPU threads
- `--db (-d)` - Database file
- `--out (-o)` - Output file
- `--verbose (-v)` - Verbose console output
- `--quiet` - Disable console output

### Alignment Sensitivity Modes
- `--faster` - Fastest mode, lowest sensitivity
- `--fast` - Fast mode
- `--mid-sensitive` - Mid-sensitive mode
- `--sensitive` - Sensitive mode (default-like)
- `--more-sensitive` - More sensitive mode
- `--very-sensitive` - Very sensitive mode
- `--ultra-sensitive` - Highest sensitivity, slowest

### Filtering Options
- `--evalue (-e)` - Maximum e-value (default: 0.001)
- `--min-score` - Minimum bit score
- `--id` - Minimum identity percentage
- `--query-cover` - Minimum query coverage percentage
- `--subject-cover` - Minimum subject coverage percentage
- `--max-target-seqs (-k)` - Maximum target sequences (default: 25)
- `--top` - Report alignments within percentage range of top score

### Performance Options
- `--memory-limit (-M)` - Memory limit in GB (default: 16)
- `--block-size (-b)` - Sequence block size in billions of letters (default: 2.0)
- `--index-chunks (-c)` - Number of chunks for index processing (default: 4)
- `--tmpdir (-t)` - Directory for temporary files

### Taxonomy Options
- `--taxonlist` - Restrict search to specific taxon IDs (comma-separated)
- `--taxon-exclude` - Exclude specific taxon IDs (comma-separated)

## Output Formats

### Format Specification
```bash
--outfmt 6    # BLAST tabular (default)
--outfmt 0    # BLAST pairwise
--outfmt 5    # BLAST XML
--outfmt 100  # DIAMOND alignment archive (DAA)
--outfmt 101  # SAM
--outfmt 102  # Taxonomic classification
--outfmt 103  # PAF
```

### Custom Tabular Output
```bash
--outfmt 6 qseqid sseqid pident length evalue bitscore staxids
```

Available fields:
- `qseqid` - Query sequence ID
- `sseqid` - Subject sequence ID
- `pident` - Percentage identity
- `length` - Alignment length
- `qstart/qend` - Query alignment coordinates
- `sstart/send` - Subject alignment coordinates
- `evalue` - E-value
- `bitscore` - Bit score
- `staxids` - Subject taxonomy IDs
- `sscinames` - Subject scientific names

## Common Usage Examples

### Basic protein annotation
```bash
# Prefer a clustered nr database (e.g. clusterednr) for much faster search at
# comparable sensitivity. Check whether one is available under $BIO_DB_ROOT
# before running; if not, build one from a sequence-clustered nr FASTA or
# fall back to full nr and record the choice in the run log.
diamond blastp --query proteins.faa --db clusterednr.dmnd \
  --out annotations.tsv --outfmt 6 --threads 16 \
  --max-target-seqs 1 --evalue 1e-5
```

### Sensitive search with taxonomy
```bash
# Prefer clusterednr.dmnd over full nr.dmnd when available — same sensitivity
# in most annotation contexts, far less runtime.
diamond blastp --query proteins.faa --db clusterednr.dmnd \
  --out annotations.tsv --threads 16 --sensitive \
  --outfmt 6 qseqid sseqid pident length evalue bitscore staxids sscinames \
  --max-target-seqs 5
```

### Fast screening with coverage filters
```bash
diamond blastp --query proteins.faa --db reference.dmnd \
  --out results.tsv --threads 32 --fast \
  --query-cover 50 --subject-cover 50 --id 30
```

### Long read alignment
```bash
diamond blastx --query long_reads.fna --db proteins.dmnd \
  --out results.tsv --long-reads --threads 16
```

## Input/Output Formats

### Input
- **Query**: FASTA format (protein for blastp, DNA for blastx)
- **Database**: DIAMOND database (.dmnd) created with makedb

### Output
- **Tabular**: Tab-separated values (most common)
- **DAA**: Binary archive format (can be converted with `diamond view`)
- **SAM**: Sequence Alignment/Map format
- **XML**: BLAST XML format

## Performance Tips

1. **Use appropriate sensitivity mode**: Start with default/fast modes and increase sensitivity only if needed
2. **Optimize memory**: Set `--memory-limit` to ~75% of available RAM
3. **Adjust block size**: Increase `--block-size` for large databases on high-memory systems
4. **Use temporary directory on fast storage**: Set `--tmpdir` to SSD location
5. **Pre-filter by taxonomy**: Use `--taxonlist` to restrict search space
6. **Compile from source**: Build with `-DCMAKE_BUILD_MARCH=native` for architecture-specific optimizations
7. **Reduce output**: Use `--max-target-seqs 1` if only best hit needed
8. **Enable compression**: Use `--compress 1` for large output files

## Workflow Integration

### Build database once
```bash
diamond makedb --in uniprot_sprot.faa --db uniprot_sprot
```

### Run annotation with optimal settings
```bash
diamond blastp --query proteins.faa --db uniprot_sprot.dmnd \
  --out annotations.tsv --outfmt 6 \
  --threads 32 --sensitive \
  --max-target-seqs 1 --evalue 1e-10 \
  --query-cover 50 --compress 1
```

### Convert DAA to tabular
```bash
diamond view --daa results.daa --out results.tsv --outfmt 6
```

## Version Information

This documentation is based on DIAMOND v2.1.6.160 and reflects features available as of January 2026.
