# eggNOG-mapper Usage Guide

## Overview

eggNOG-mapper is a tool for fast genome-wide functional annotation through orthology assignment. It uses precomputed orthologous groups and phylogenies from the eggNOG database to transfer functional information from sequences with known annotation to novel sequences.

## Official Documentation

- GitHub Repository: https://github.com/eggnogdb/eggnog-mapper
- Bioconda Package: https://bioconda.github.io/recipes/eggnog-mapper/README.html
- eggNOG Database: http://eggnog-mapper.embl.de/
- Installation Guide: https://deepwiki.com/eggnogdb/eggnog-mapper/2-installation-and-setup

## Installation

### Conda/Mamba (Recommended)

```bash
# Using mamba (faster)
mamba install -c bioconda eggnog-mapper

# Using conda
conda install -c bioconda eggnog-mapper
```

### Pip Installation

```bash
# Install latest version
pip install eggnog-mapper

# Install specific version
pip install eggnog-mapper==2.1.13
```

### Requirements
- Python 3.7 or higher
- Dependencies: biopython, psutil, wget

## Database Setup

### Download eggNOG Databases

```bash
# Set data directory
export EGGNOG_DATA_DIR=/path/to/eggnog-data

# Download all databases (requires ~100GB)
download_eggnog_data.py --data_dir $EGGNOG_DATA_DIR

# Download specific taxonomic scope
download_eggnog_data.py --data_dir $EGGNOG_DATA_DIR -y

# Download bacteria only
download_eggnog_data.py --data_dir $EGGNOG_DATA_DIR -y Bacteria

# Download with DIAMOND database
download_eggnog_data.py --data_dir $EGGNOG_DATA_DIR -y --dmnd
```

### Database Components
- **eggnog.db**: Core orthology database
- **eggnog_proteins.dmnd**: DIAMOND database for sequence search
- ***.hmm**: HMM profiles for orthologous groups
- Taxonomic-specific databases (optional)

## Key Command-Line Options

### Basic Options
- `-i, --input` - Input FASTA file (required)
- `-o, --output` - Output base name (required)
- `--data_dir` - eggNOG data directory
- `-m, --mode` - Search mode (diamond, hmmer, mmseqs, cache)
- `--cpu` - Number of CPU threads

### Search Options
- `--dmnd_db` - DIAMOND database path
- `--sensmode` - DIAMOND sensitivity (default, fast, mid-sensitive, sensitive, more-sensitive, very-sensitive, ultra-sensitive)
- `--evalue` - E-value threshold (default: 0.001)
- `--score` - Minimum bit score
- `--pident` - Minimum percentage identity
- `--query_cover` - Minimum query coverage
- `--subject_cover` - Minimum subject coverage

### Taxonomic Scope
- `--tax_scope` - Taxonomic scope (auto, bacteria, archaea, eukaryota, viruses)
- `--target_orthologs` - Target ortholog selection (all, one2one)
- `--go_evidence` - GO evidence codes to include

### Output Options
- `--output_dir` - Output directory
- `--no_annot` - Skip functional annotation
- `--no_file_comments` - Exclude header comments
- `--report_orthologs` - Include ortholog information
- `--md5` - Use MD5 hashes for sequence IDs

### Advanced Options
- `--override` - Override existing results
- `--resume` - Resume interrupted run
- `--temp_dir` - Temporary directory
- `--dbmem` - Load database into memory (faster, requires RAM)

## Common Usage Examples

### Basic annotation with DIAMOND
```bash
emapper.py -i proteins.faa -o annotation \
  --data_dir $EGGNOG_DATA_DIR \
  --cpu 16
```

### Bacteria-specific annotation
```bash
emapper.py -i bacterial_proteins.faa -o bacteria_annot \
  --data_dir $EGGNOG_DATA_DIR \
  --dmnd_db $EGGNOG_DATA_DIR/bacteria.dmnd \
  --tax_scope Bacteria \
  --cpu 32
```

### Sensitive search with coverage filters
```bash
emapper.py -i proteins.faa -o annotation \
  --data_dir $EGGNOG_DATA_DIR \
  --sensmode very-sensitive \
  --evalue 1e-10 \
  --query_cover 50 \
  --subject_cover 50 \
  --cpu 32
```

### With ortholog reporting
```bash
emapper.py -i proteins.faa -o annotation \
  --data_dir $EGGNOG_DATA_DIR \
  --report_orthologs \
  --cpu 16
```

### Using HMM search mode
```bash
emapper.py -i proteins.faa -o annotation \
  --data_dir $EGGNOG_DATA_DIR \
  -m hmmer \
  --cpu 32
```

### Resume interrupted run
```bash
emapper.py -i proteins.faa -o annotation \
  --data_dir $EGGNOG_DATA_DIR \
  --resume \
  --cpu 16
```

### Fast mode for large datasets
```bash
emapper.py -i proteins.faa -o annotation \
  --data_dir $EGGNOG_DATA_DIR \
  --sensmode fast \
  --dbmem \
  --cpu 64
```

## Search Modes

### Diamond Mode (Default)
- Fastest method
- Uses DIAMOND for sequence similarity search
- Good for large-scale annotations
- Recommended for most use cases

```bash
emapper.py -i proteins.faa -o results -m diamond
```

### HMMER Mode
- Uses HMM profiles
- More sensitive for remote homologs
- Slower than DIAMOND
- Good for divergent sequences

```bash
emapper.py -i proteins.faa -o results -m hmmer
```

### MMseqs2 Mode
- Fast alternative to DIAMOND
- Good sensitivity/speed tradeoff
- Requires MMseqs2 installation

```bash
emapper.py -i proteins.faa -o results -m mmseqs
```

### Cache Mode
- Use pre-computed annotations
- For re-annotation with updated database
- Fastest option

```bash
emapper.py -i proteins.faa -o results -m cache
```

## Output Files

### Main Output (.emapper.annotations)
Tab-separated file with columns:
1. `query` - Query sequence ID
2. `seed_ortholog` - Best matching ortholog
3. `evalue` - E-value of match
4. `score` - Bit score
5. `eggNOG_OGs` - Orthologous groups
6. `max_annot_lvl` - Taxonomic level of annotation
7. `COG_category` - COG functional category
8. `Description` - Functional description
9. `Preferred_name` - Gene name
10. `GOs` - Gene Ontology terms
11. `EC` - Enzyme Commission numbers
12. `KEGG_ko` - KEGG orthology
13. `KEGG_Pathway` - KEGG pathways
14. `KEGG_Module` - KEGG modules
15. `KEGG_Reaction` - KEGG reactions
16. `KEGG_rclass` - KEGG reaction class
17. `BRITE` - BRITE hierarchy
18. `KEGG_TC` - Transport classification
19. `CAZy` - Carbohydrate-active enzymes
20. `BiGG_Reaction` - BiGG reactions
21. `PFAMs` - Pfam domains

### Seed Orthologs (.emapper.seed_orthologs)
Details of best matching sequences.

### Hits (.emapper.hits)
All significant hits from sequence search.

### Orthologs (.emapper.orthologs)
Ortholog predictions (if `--report_orthologs` used).

## Input Requirements

### FASTA Format
```
>protein_id1
MKTIIALSYIFCLVFADYKDDDDKSEQUENCE...
>protein_id2
MALWMRLLPLLALLALWGPDPAAAFVNQHLC...
```

### Requirements
- Protein sequences (amino acids)
- Valid FASTA format
- Unique sequence identifiers

## Performance Tips

1. **Use DIAMOND mode**: Fastest for large datasets
2. **Load database in memory**: Use `--dbmem` if sufficient RAM available
3. **Adjust sensitivity**: Use `--sensmode fast` for quick screening
4. **Set appropriate taxonomic scope**: Use `--tax_scope` to reduce search space
5. **Use multiple CPUs**: Set `--cpu` to available cores
6. **Fast storage for temp files**: Set `--temp_dir` to SSD location
7. **Pre-filter sequences**: Remove short or low-quality sequences
8. **Resume capability**: Use `--resume` for interrupted large runs
9. **Batch processing**: Split very large files into manageable chunks

## Workflow Integration

### Complete annotation pipeline
```bash
# Set up environment
export EGGNOG_DATA_DIR=/data/eggnog

# Download databases (once)
download_eggnog_data.py --data_dir $EGGNOG_DATA_DIR -y

# Run annotation
emapper.py -i proteins.faa -o annotation \
  --data_dir $EGGNOG_DATA_DIR \
  --dmnd_db $EGGNOG_DATA_DIR/eggnog_proteins.dmnd \
  --sensmode very-sensitive \
  --cpu 32 \
  --report_orthologs \
  --output_dir results/
```

### Parse annotations
```bash
# Extract GO terms
cut -f1,10 annotation.emapper.annotations | grep -v "^#" > go_terms.tsv

# Extract KEGG pathways
cut -f1,13 annotation.emapper.annotations | grep -v "^#" > kegg_pathways.tsv

# Extract COG categories
cut -f1,7 annotation.emapper.annotations | grep -v "^#" > cog_categories.tsv
```

### Filter by annotation quality
```bash
# Keep only high-confidence annotations (e-value < 1e-10)
awk -F'\t' '$3 < 1e-10' annotation.emapper.annotations > high_conf.tsv
```

## Understanding COG Categories

COG functional categories:
- **J**: Translation, ribosomal structure and biogenesis
- **K**: Transcription
- **L**: Replication, recombination and repair
- **D**: Cell cycle control, cell division, chromosome partitioning
- **M**: Cell wall/membrane/envelope biogenesis
- **N**: Cell motility
- **O**: Post-translational modification, protein turnover, chaperones
- **T**: Signal transduction mechanisms
- **U**: Intracellular trafficking, secretion, and vesicular transport
- **V**: Defense mechanisms
- **C**: Energy production and conversion
- **E**: Amino acid transport and metabolism
- **F**: Nucleotide transport and metabolism
- **G**: Carbohydrate transport and metabolism
- **H**: Coenzyme transport and metabolism
- **I**: Lipid transport and metabolism
- **P**: Inorganic ion transport and metabolism
- **Q**: Secondary metabolites biosynthesis, transport and catabolism
- **S**: Function unknown

## Troubleshooting

### Database download issues
```bash
# Download with resume capability
download_eggnog_data.py --data_dir $EGGNOG_DATA_DIR -y --resume

# Check downloaded files
ls -lh $EGGNOG_DATA_DIR/
```

### Memory issues
```bash
# Don't use --dbmem on limited RAM systems
emapper.py -i proteins.faa -o results \
  --data_dir $EGGNOG_DATA_DIR \
  --cpu 32
```

### Slow performance
```bash
# Use fast mode and appropriate taxonomic scope
emapper.py -i proteins.faa -o results \
  --data_dir $EGGNOG_DATA_DIR \
  --sensmode fast \
  --tax_scope Bacteria \
  --cpu 64
```

### Check version
```bash
emapper.py --version
```

## HPC Resource Guidelines (Benchmarked March 2026)

These numbers are from real runs on NERSC Perlmutter (shared_milan partition)
annotating viral EVE proteins against the full eggNOG v5.0.2 database (diamond mode,
`--sensitive --iterate` default).

### Database sizes on disk

| File | Size |
|------|------|
| eggnog.db | 39 GB |
| eggnog_proteins.dmnd | 8.7 GB |
| eggnog.taxa.db | 266 MB |
| **Total** | **~48 GB** |

### `--dbmem` is dangerous: do NOT use with ≤64 GB RAM

`--dbmem` loads `eggnog.db` (39 GB) + diamond DB (8.7 GB) into memory.
Combined with the annotation engine and OS overhead this requires **>80 GB RAM**.
At 32 GB it will OOM-kill during the annotation phase (diamond search may
complete, but the subsequent annotation step loads eggnog.db and kills the job).
At 64 GB it is marginal and often OOM-kills as well.

**Recommendation:** Only use `--dbmem` when requesting ≥128 GB RAM.
For shared-queue HPC jobs, **omit `--dbmem`** entirely — disk-based
access is slower but reliable and fits in 64 GB.

### Resource requirements per chunk (without `--dbmem`)

| Proteins per chunk | CPUs | RAM | Wall time (observed) | Notes |
|--------------------|------|-----|---------------------|-------|
| 5,000 | 8 | 64 GB | 1.5–3 h | Viral proteins, divergent sequences |
| 10,000 | 8 | 64 GB | 3–6 h | Set walltime ≥8 h |
| 5,000 | 8 | 32 GB | OOM | Fails in annotation phase |
| 5,000 + `--dbmem` | 8 | 32 GB | OOM | Fails: needs ≥128 GB |
| 5,000 + `--dbmem` | 8 | 128 GB | ~45 min | Fast but expensive |

### Recommended SLURM settings for chunked runs

```bash
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=08:00:00
#SBATCH --constraint=cpu

# Do NOT use --dbmem unless requesting >=128G
emapper.py -i chunk.faa -o chunk_out \
  -m diamond --cpu 8 \
  --data_dir $EGGNOG_DATA_DIR \
  --go_evidence non-electronic \
  --override
```

### Chunking strategy

- **5,000 proteins per chunk** is a good balance for 8-CPU shared-queue jobs
- For 100k+ proteins, create 20-25 chunks and submit as a SLURM array
- Submit a dependent finalization job to merge outputs:
  ```bash
  sbatch --dependency=afterok:$ARRAY_JOB finalize.sh
  ```
- Merge annotations with: `grep '^#query' chunk_001.emapper.annotations | head -1 > merged.tsv`
  then `grep -hv '^#' chunk_*/chunk_*.emapper.annotations >> merged.tsv`

### Database download URL fix (as of 2025-09)

The default download URL `eggnogdb.embl.de` is **dead** (returns 404).
The domain moved to `eggnog5.embl.de`. You must patch the download script:

```bash
# In download_eggnog_data.py (line ~15), change:
#   BASE_URL = f'http://eggnogdb.embl.de/download/emapperdb-{__DB_VERSION__}'
# to:
#   BASE_URL = f'http://eggnog5.embl.de/download/emapperdb-{__DB_VERSION__}'

sed -i 's|eggnogdb.embl.de|eggnog5.embl.de|g' \
  "$(which download_eggnog_data.py)"
```

This applies to eggnog-mapper v2.1.13 (latest as of March 2026).
The fix has been reported (GitHub issues #571, #574, #576) but not merged.

### Diamond binary PATH issue

eggnog-mapper resolves diamond via `shutil.which('diamond')`. In pixi/conda
environments the binary may not be on the system PATH inside SLURM jobs.
Fix by adding the env bin to PATH in your SBATCH script:

```bash
export PATH="/path/to/pixi/envs/default/bin:${PATH}"
```

## Best Practices

1. **Download appropriate databases**: Only download taxonomic scopes needed
2. **Use taxonomic scope**: Specify `--tax_scope` to improve accuracy
3. **Set reasonable thresholds**: Adjust e-value and coverage filters
4. **Enable ortholog reporting**: Use `--report_orthologs` for detailed analysis
5. **Monitor resource usage**: eggNOG-mapper can be memory-intensive; see resource table above
6. **Keep databases updated**: Regularly update eggNOG databases
7. **Validate input**: Check FASTA format before processing; strip `*` stop codons
8. **Save all outputs**: Keep seed orthologs and hits files for troubleshooting
9. **Use resume feature**: Enable `--resume` for large datasets
10. **Never use `--dbmem` with <128 GB RAM**: It will OOM-kill; see resource guidelines above
11. **Always test on login node first**: Run 2-3 proteins to verify PATH, DB access, and CLI before submitting arrays

## Integration with Other Tools

### Combine with InterProScan
```bash
# Run both for comprehensive annotation
emapper.py -i proteins.faa -o eggnog_results
interproscan.sh -i proteins.faa -o iprs_results
# Merge results downstream
```

### Integration with DIAMOND
```bash
# Use custom DIAMOND database
diamond makedb --in custom_proteins.faa -d custom
emapper.py -i proteins.faa -o results --dmnd_db custom.dmnd
```

## Version Information

This documentation is based on eggNOG-mapper v2.1.13 and reflects features available as of January 2026. The latest version is maintained on GitHub and Bioconda.
