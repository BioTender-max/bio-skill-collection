# EukCC v2.x

Quality assessment tool for eukaryotic metagenome-assembled genomes (MAGs) using marker genes.

## Official Documentation
- GitHub: https://github.com/EBI-Metagenomics/EukCC
- Publication: Saary et al. (2020) *Genome Biology*
- Version: 2.x

## Installation

**Container (recommended):**
```bash
# Docker
docker pull quay.io/microbiome-informatics/eukcc

# Singularity
singularity pull docker://quay.io/microbiome-informatics/eukcc
```

**Conda/Bioconda:**
```bash
conda install -c bioconda eukcc
```

**Manual dependencies:**
If installing without container, ensure these are available:
- metaeuk (v4.a0f584d)
- pplacer
- epa-ng (v0.3.8)
- hmmer (v3.3)
- minimap2
- bwa
- samtools

## Database Setup

**Download EukCC2 database (v1.2):**
```bash
wget http://ftp.ebi.ac.uk/pub/databases/metagenomics/eukcc/eukcc2_db_ver_1.2.tar.gz
tar -xzvf eukcc2_db_ver_1.2.tar.gz

# Set environment variable
export EUKCC2_DB=$(realpath eukcc2_db_ver_1.2)
```

**Database size:** ~2.5 GB compressed, ~4 GB uncompressed

## Key Command-Line Flags

| Flag | Description |
|------|-------------|
| `--debug` | Enable debug logging for troubleshooting |
| `--threads` | Number of threads to use |
| `--db` | Path to EukCC2 database |

**Note:** EukCC2 has user-configurable marker set prevalence threshold (unlike v1's fixed 98%).

## Common Usage Examples

### Single genome assessment
```bash
eukcc single bin.fasta --db $EUKCC2_DB --threads 16
```

### Batch folder processing
```bash
eukcc folder bins_dir/ --db $EUKCC2_DB --threads 16
```

### With Docker container
```bash
docker run -v $(pwd):/data -v /path/to/db:/db \
  quay.io/microbiome-informatics/eukcc \
  eukcc single /data/bin.fasta --db /db/eukcc2_db_ver_1.2 --threads 8
```

### Debug mode for troubleshooting
```bash
eukcc single bin.fasta --db $EUKCC2_DB --threads 16 --debug
```

## Input Requirements

**Genome/bin files:**
- FASTA format (nucleotide sequences)
- Eukaryotic genomes or bins
- Size: Typically 1-500 Mbp
- Can be fragmented/incomplete MAGs

**Domain classification:**
EukCC is **specific to eukaryotes**. Pre-classify bins to avoid running CheckM2 on eukaryotic genomes or EukCC on prokaryotic genomes.

## Output Format

### Single mode output
**File:** `eukcc.csv`

Columns:
- Genome name
- Completeness (%)
- Contamination (%)
- Taxonomy prediction
- Number of marker genes found
- Additional QC metrics

Example:
```
genome,completeness,contamination,taxonomy,markers_found
bin1.fasta,95.2,1.3,Ascomycota,450
bin2.fasta,78.6,4.1,Metazoa,389
```

### Folder mode output
**Files:**
- `eukcc.csv` - High-quality bins (pass thresholds)
- `bad_quality.csv` - Low-quality bins (fail thresholds)
- Merged bin sequences (optional)
- Intermediate results in subdirectories

**Quality tiers:**
Quality assessment results are automatically split into pass/fail based on completeness and contamination thresholds.

## Quality Thresholds

**Typical eukaryotic MAG standards:**
- **High-quality:** ≥90% complete, ≤5% contamination
- **Medium-quality:** ≥50% complete, ≤10% contamination
- **Low-quality:** <50% complete or >10% contamination

**Filtering results:**
```bash
# High-quality eukaryotic bins
awk -F',' '$2 >= 90 && $3 <= 5' eukcc.csv | tail -n +2

# Medium-quality bins
awk -F',' '$2 >= 50 && $3 <= 10' eukcc.csv | tail -n +2
```

## Performance Tips

1. **Use containers**: Simplifies dependency management
2. **Database location**: Store on fast SSD for performance
3. **Threading**: Scales with available cores (8-32 typical)
4. **Batch processing**: Use `folder` mode for multiple bins
5. **Pre-classification**: Filter eukaryotic bins before running (saves time)

## Marker Set System

EukCC2 improvements over v1:
- **Configurable prevalence**: User can adjust marker gene presence threshold
- **Broader taxon coverage**: Expanded marker sets for diverse eukaryotes
- **Improved accuracy**: Better handling of incomplete genomes

Marker sets are taxon-specific, providing accurate estimates across:
- Fungi
- Protists
- Metazoa
- Plants
- Other eukaryotes

## Domain Classification

**Classify bins before QC to route to correct tool:**

```bash
# Example: Use EukRep or similar for domain classification
EukRep -i contigs.fasta -o eukaryotic.fasta --prokarya prokaryotic.fasta

# Or use taxonomy from binning tools
# Then run domain-specific QC:
checkm2 predict --input prokaryotic_bins/ --output-directory qc_prok/
eukcc folder eukaryotic_bins/ --db $EUKCC2_DB --threads 16
```

## Integration with Binning

```bash
# Run binning (e.g., MetaBAT2)
metabat2 -i contigs.fasta -a depth.txt -o bins/bin -t 16

# Classify bins by domain (example using simple approach)
# In practice, use proper classification tool
for bin in bins/*.fa; do
  # Check for eukaryotic markers (simplified)
  if grep -q "eukaryotic_marker" $bin; then
    mv $bin eukaryotic_bins/
  else
    mv $bin prokaryotic_bins/
  fi
done

# Run domain-specific QC
checkm2 predict --input prokaryotic_bins/ --output-directory qc_prok/ -t 16
eukcc folder eukaryotic_bins/ --db $EUKCC2_DB --threads 16
```

## Output Interpretation

**Completeness:**
- Percentage of expected taxon-specific marker genes present
- Higher values indicate more complete genome
- Aim for ≥90% for high-quality eukaryotic MAGs

**Contamination:**
- Percentage of marker genes duplicated or from different lineages
- Lower is better (aim for ≤5%)
- High contamination indicates mixed genomes

**Taxonomy:**
- Predicted taxonomic lineage based on marker genes
- Helps validate bin assignment
- May be broad for novel or poorly characterized taxa

## Common Issues

- **Database not found**: Set `EUKCC2_DB` environment variable
- **Low completeness**: Genome may be incomplete, fragmented, or from novel lineage
- **High contamination**: Bin contains multiple genomes; refine binning
- **Dependency errors**: Use container installation to avoid issues
- **Slow performance**: Ensure database on fast storage; check thread usage
- **No markers found**: Bin may not be eukaryotic (run CheckM2 instead)

## Comparison with CheckM/CheckM2

| Feature | CheckM2 | EukCC |
|---------|---------|-------|
| Domain | Bacteria, Archaea | Eukaryotes |
| Speed | Very fast | Moderate |
| Marker genes | Universal prokaryotic | Taxon-specific eukaryotic |
| Database size | ~3 GB | ~4 GB |
| Taxonomy | Limited | Detailed |

**Key takeaway:** Use CheckM2 for prokaryotes, EukCC for eukaryotes.

## Workflow Integration

```bash
# Complete binning and QC workflow
# 1. Binning
metabat2 -i contigs.fasta -a depth.txt -o bins/bin -t 16

# 2. Domain classification (example)
# Use proper classifier in practice
classify_bins.sh bins/ prokaryotic_bins/ eukaryotic_bins/

# 3. QC for prokaryotes
checkm2 predict --input prokaryotic_bins/ \
  --output-directory qc/prokaryotic/ -t 16

# 4. QC for eukaryotes
eukcc folder eukaryotic_bins/ \
  --db $EUKCC2_DB --threads 16

# 5. Contamination check (all bins)
gunc run --input_dir prokaryotic_bins/ \
  --db_file gunc_db --threads 16
```

## Advanced Features

### Custom marker prevalence threshold
EukCC2 allows adjustment of marker gene presence threshold for edge cases or novel taxa (consult documentation for details).

### Taxonomic placement
EukCC provides phylogenetic placement of bins, useful for validating taxonomic assignment and detecting novel lineages.

## Citation

Saary P, Mitchell AL, Finn RD. (2020)
Estimating the quality of eukaryotic genomes recovered from metagenomic analysis with EukCC.
*Genome Biology* 21:244. https://doi.org/10.1186/s13059-020-02155-4
