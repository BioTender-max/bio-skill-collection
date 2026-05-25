# TaxonKit Usage Guide

## Overview

TaxonKit is a practical and efficient command-line toolkit for comprehensive manipulation of NCBI Taxonomy data. It is implemented in Go and provides cross-platform support with fast performance.

## Official Documentation

- Official Website: https://bioinf.shenwei.me/taxonkit/
- GitHub Repository: https://github.com/shenwei356/taxonkit
- Usage Documentation: https://bioinf.shenwei.me/taxonkit/usage/
- Citation: https://doi.org/10.1016/j.jgg.2021.03.006 (Journal of Genetics and Genomics 2021)

## Installation

### Binary Download
```bash
# Download from GitHub releases
wget https://github.com/shenwei356/taxonkit/releases/download/v0.20.0/taxonkit_linux_amd64.tar.gz
tar -zxvf taxonkit_linux_amd64.tar.gz
```

### Conda/Bioconda
```bash
conda install -c bioconda taxonkit
```

### Go Install
```bash
go install github.com/shenwei356/taxonkit@latest
```

## Database Setup

### Download NCBI Taxonomy Data
```bash
# Download taxdump
wget ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz
tar -zxvf taxdump.tar.gz

# Create data directory
mkdir -p ~/.taxonkit

# Copy required files
cp names.dmp nodes.dmp delnodes.dmp merged.dmp ~/.taxonkit/
```

### Custom Data Directory
```bash
# Set environment variable
export TAXONKIT_DB=/path/to/taxdump

# Or use --data-dir flag
taxonkit --data-dir /path/to/taxdump <command>
```

## Key Commands

### lineage - Query Taxonomic Lineage
```bash
# Get lineage for TaxIDs
echo "9606" | taxonkit lineage
# Output: 9606    cellular organisms;Eukaryota;Opisthokonta;Metazoa;...

# With taxonomic names
echo "9606" | taxonkit lineage -n
```

### reformat - Reformat Lineage
```bash
# Standard seven-rank format (K;P;C;O;F;G;S)
echo "9606" | taxonkit lineage | taxonkit reformat
# Output: 9606    ...    Eukaryota;Chordata;Mammalia;Primates;Hominidae;Homo;Homo sapiens

# Custom format
echo "9606" | taxonkit lineage | taxonkit reformat -f "{k};{p};{c};{o};{f};{g};{s}"
```

### name2taxid - Convert Names to TaxIDs
```bash
# Convert scientific names to TaxIDs
echo "Homo sapiens" | taxonkit name2taxid
# Output: Homo sapiens    9606

# From file
taxonkit name2taxid species_names.txt -o species_taxids.txt
```

### list - List Taxonomic Subtrees
```bash
# List all descendants of a TaxID
taxonkit list --ids 9606

# With taxonomic names and indentation
taxonkit list --ids 9606 -n -r --indent "  "
```

### filter - Filter TaxIDs by Rank Range
```bash
# Filter at genus rank and below
cat taxids.txt | taxonkit filter -L genus

# Filter at specific rank
cat taxids.txt | taxonkit filter -E species

# Filter between ranks
cat taxids.txt | taxonkit filter -L genus -H species
```

### lca - Compute Lowest Common Ancestor
```bash
# Compute LCA for multiple TaxIDs
echo "9606,9597" | taxonkit lca
# Output: LCA of 9606,9597: 9604 (Hominidae)
```

## Key Command-Line Options

### Global Options
- `--data-dir` - Directory containing NCBI taxonomy files (default: ~/.taxonkit)
- `--threads (-j)` - Number of CPUs (default: 4)
- `--out-file (-o)` - Output file (default: stdout)
- `--verbose` - Print verbose information
- `--line-buffered` - Use line buffering for immediate output

### Lineage Options
- `-n, --show-name` - Show scientific name
- `-r, --show-rank` - Show taxonomic rank
- `-L, --show-lineage-taxids` - Show lineage TaxIDs
- `-t, --show-status-code` - Show status code

### Reformat Options
- `-f, --format` - Output format (default: "{k};{p};{c};{o};{f};{g};{s}")
- `-d, --delimiter` - Field delimiter (default: tab)
- `-F, --fill-miss-rank` - Fill missing ranks with placeholder
- `-P, --add-prefix` - Add rank prefix to names
- `-r, --miss-rank-repl` - Replacement for missing ranks
- `-R, --miss-rank-repl-prefix` - Prefix for missing rank replacement

### Name2taxid Options
- `-s, --sci-name` - Only search scientific names
- `-r, --show-rank` - Show taxonomic rank

### List Options
- `-i, --ids` - Comma-separated TaxIDs
- `-n, --show-name` - Show scientific names
- `-r, --show-rank` - Show taxonomic ranks
- `--indent` - Indent string for tree display

### Filter Options
- `-E, --equal-to` - Filter at specific rank
- `-L, --lower-than` - Filter at rank and below
- `-H, --higher-than` - Filter at rank and above
- `-d, --discard-noranks` - Discard unranked TaxIDs
- `-r, --save-predictable-norank` - Save predictable unranked TaxIDs

## Common Usage Examples

### Resolve taxonomy from DIAMOND output
```bash
# Extract TaxIDs from DIAMOND results (column 13)
cut -f13 diamond_results.tsv | \
  taxonkit lineage -n -r | \
  taxonkit reformat -f "{k};{p};{c};{o};{f};{g};{s}" > taxonomy.tsv
```

### Get full lineage with names
```bash
echo "562" | taxonkit lineage -n -r -L
# Shows Escherichia coli with full lineage and ranks
```

### Convert list of species names
```bash
cat species_list.txt | \
  taxonkit name2taxid | \
  taxonkit lineage | \
  taxonkit reformat > species_taxonomy.tsv
```

### Filter for genus-level and below
```bash
cat all_taxids.txt | \
  taxonkit filter -L genus | \
  taxonkit lineage -n -r > genus_and_species.tsv
```

### Create taxonomic summary
```bash
# Get all bacterial species
echo "2" | taxonkit list --ids 2 | \
  taxonkit filter -E species | \
  taxonkit lineage -n -r > bacteria_species.tsv
```

### LCA for sequence clusters
```bash
# Find common ancestor for TaxIDs in a cluster
echo "9606,9597,9598" | taxonkit lca -d ","
```

## Input/Output Formats

### Input
- **TaxIDs**: Plain text, one per line or comma-separated
- **Names**: Scientific names, one per line
- **Stdin**: Pipeline-friendly, accepts piped input

### Output
- **Tab-separated**: Default output format
- **Custom delimiters**: Configurable with `-d`
- **Formatted lineage**: Seven-rank format or custom

## Reformat Format String

Format placeholders:
- `{k}` - Kingdom
- `{p}` - Phylum
- `{c}` - Class
- `{o}` - Order
- `{f}` - Family
- `{g}` - Genus
- `{s}` - Species
- `{t}` - Subspecies/strain

Example formats:
```bash
# NCBI seven-rank
-f "{k};{p};{c};{o};{f};{g};{s}"

# With rank prefixes
-f "{K};{P};{C};{O};{F};{G};{S}" -P

# Custom separator
-f "{k}|{p}|{c}|{o}|{f}|{g}|{s}"
```

## Performance Tips

1. **Use appropriate thread count**: Set `-j` to available CPU cores
2. **Keep data local**: Place taxdump in fast storage (SSD)
3. **Use line buffering**: Add `--line-buffered` for real-time output in pipelines
4. **Batch processing**: Process multiple TaxIDs together rather than one at a time
5. **Cache lookups**: TaxonKit caches taxonomy data in memory for fast repeated queries
6. **Pre-filter TaxIDs**: Remove duplicates before processing to avoid redundant lookups
7. **Use specific commands**: Use `filter` before `lineage` to reduce processing

## Workflow Integration

### DIAMOND + TaxonKit Pipeline
```bash
# Run DIAMOND with taxonomy.
# Prefer clusterednr.dmnd over full nr.dmnd when available (check $BIO_DB_ROOT
# first; build from a clustered nr FASTA if missing) — far faster, comparable
# taxonomy assignment quality for typical annotation tasks.
diamond blastp --query proteins.faa --db clusterednr.dmnd \
  --out results.tsv --outfmt 6 qseqid sseqid staxids evalue bitscore \
  --threads 32

# Extract and resolve taxonomy
cut -f3 results.tsv | \
  sed '1d' | \
  taxonkit lineage -n -r | \
  taxonkit reformat -f "{k};{p};{c};{o};{f};{g};{s}" | \
  paste results.tsv - > results_with_taxonomy.tsv
```

### Create taxonomic summary report
```bash
# Count sequences per phylum
cut -f3 results.tsv | \
  taxonkit lineage | \
  taxonkit reformat -f "{p}" | \
  cut -f3 | \
  sort | uniq -c | \
  sort -rn > phylum_counts.txt
```

### Handle missing TaxIDs
```bash
# Fill missing ranks with "unclassified"
echo "12345" | \
  taxonkit lineage | \
  taxonkit reformat -F -r "unclassified"
```

## Troubleshooting

### Update taxonomy database
```bash
# Download latest taxdump
cd ~/.taxonkit
wget ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz
tar -zxvf taxdump.tar.gz --overwrite
```

### Handle merged/deleted TaxIDs
```bash
# TaxonKit automatically handles merged and deleted TaxIDs
# using merged.dmp and delnodes.dmp
```

### Check TaxonKit version
```bash
taxonkit version
```

## Version Information

This documentation is based on TaxonKit v0.14.2-v0.20.0 and reflects features available as of January 2026.
