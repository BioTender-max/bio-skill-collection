# CheckM2 v1.0.2

Rapid assessment of genome quality (completeness and contamination) for bacterial and archaeal bins using machine learning.

## Official Documentation
- GitHub: https://github.com/chklovski/CheckM2
- Publication: Chklovski et al. (2023) *Nature Methods*
- Database: Zenodo (v1.1.0)
- Version: 1.0.2

## Installation

**Conda/Mamba (recommended):**
```bash
mamba create -n checkm2 -c bioconda -c conda-forge checkm2
conda activate checkm2
```

**From source:**
```bash
git clone --recursive https://github.com/chklovski/checkm2.git
cd checkm2
conda env create -n checkm2 -f checkm2.yml
conda activate checkm2
python setup.py install
```

**PyPI:**
```bash
# Create conda environment first for dependencies
conda create -n checkm2 python=3.8
conda activate checkm2
pip install CheckM2
```

## Database Setup

**Download database (required):**
```bash
# Default location: ~/.local/share/CheckM2
checkm2 database --download

# Custom location
checkm2 database --download --path /custom/path/checkm2_db/
```

**Set database path (if not default):**
```bash
export CHECKM2DB="/path/to/checkm2_db/"
```

**Database version:** v1.1.0 (available at https://zenodo.org/record/14897628)

## Key Command-Line Flags

| Flag | Description |
|------|-------------|
| `--input` | Folder with bins or list of individual FASTA files |
| `--output-directory` | Output directory for results |
| `-x, --extension` | File extension (e.g., "fa", "fasta", "gz") |
| `-t, --threads` | Number of parallel threads |
| `--genes` | Use pre-computed protein predictions |
| `--stdout` | Print results to stdout instead of file |
| `--lowmem` | Reduce DIAMOND RAM usage (slower runtime) |
| `--database_path` | Custom database location |
| `--force` | Overwrite existing output directory |
| `--resume` | Resume from previous run |

## Common Usage Examples

### Standard bin quality assessment
```bash
checkm2 predict --threads 30 \
  --input bins/ \
  --output-directory checkm2_output/
```

### Multiple files from different locations
```bash
checkm2 predict --threads 16 \
  --input ../sample1/bin1.fa ../../sample2/bin2.fna /path/to/bin3.fasta \
  --output-directory checkm2_output/
```

### With gzipped files
```bash
checkm2 predict --threads 20 \
  --input bins/ \
  --extension gz \
  --output-directory checkm2_output/
```

### Using pre-computed gene predictions
```bash
# Run Prodigal separately
prodigal -i bin1.fasta -a bin1.faa -p meta

# Run CheckM2 with protein files
checkm2 predict --threads 16 \
  --input protein_dir/ \
  --genes \
  --output-directory checkm2_output/
```

### Low memory mode
```bash
checkm2 predict --threads 16 \
  --input bins/ \
  --output-directory checkm2_output/ \
  --lowmem
```

### Resume interrupted run
```bash
checkm2 predict --threads 30 \
  --input bins/ \
  --output-directory checkm2_output/ \
  --resume
```

## Input Requirements

**Genome/bin files:**
- FASTA format (nucleotide sequences)
- Can be gzipped (specify with `-x gz`)
- Multiple files in a directory or listed individually
- Minimum size: ~50 kb (very small bins may have unreliable estimates)

**OR protein predictions:**
- FASTA format (amino acid sequences)
- Use `--genes` flag
- Must be generated with Prodigal or compatible tool

## Output Format

**Main output file:** `quality_report.tsv`

Tab-delimited with columns:
- `Name` - Bin/genome name
- `Completeness` - Estimated completeness (0-100%)
- `Contamination` - Estimated contamination (0-100%)
- `Completeness_Model_Used` - Model used for prediction
- `Translation_Table_Used` - Genetic code used
- `Coding_Density` - Fraction of genome coding
- `Contig_N50` - N50 of contigs
- `Average_Gene_Length` - Mean gene length
- `Genome_Size` - Total genome size (bp)
- `GC_Content` - GC percentage
- `Total_Coding_Sequences` - Number of predicted genes
- `Additional_Notes` - Warnings or notes

Example output:
```
Name      Completeness  Contamination  Completeness_Model_Used  Translation_Table_Used
bin.1.fa  98.3          0.8            Specific Model           11
bin.2.fa  87.6          2.1            Specific Model           11
bin.3.fa  45.2          0.3            General Model            11
```

## Quality Thresholds

**MIMAG standards (Bowers et al. 2017):**
- **High-quality:** ≥90% complete, ≤5% contamination, 23S/16S/5S rRNA, ≥18 tRNAs
- **Medium-quality:** ≥50% complete, ≤10% contamination
- **Low-quality:** <50% complete, <10% contamination

**Common filtering:**
```bash
# High-quality bins (strict)
awk -F'\t' '$2 >= 90 && $3 <= 5' quality_report.tsv

# Medium-quality bins
awk -F'\t' '$2 >= 50 && $3 <= 10' quality_report.tsv
```

## Performance Tips

1. **Threading**: Scales well up to 30-40 threads
2. **Memory**: Default mode ~16 GB RAM; `--lowmem` reduces to ~8 GB
3. **Database location**: Place on fast SSD for better performance
4. **Pre-computed genes**: Save time when running multiple analyses
5. **Resume capability**: Use `--resume` if runs are interrupted
6. **Batch size**: Process hundreds to thousands of bins efficiently

## Comparison with CheckM1

**CheckM2 advantages:**
- **Speed**: ~20-30x faster than CheckM1
- **Memory**: Lower memory footprint
- **Accuracy**: Improved estimates using machine learning
- **Database**: Smaller, more efficient database

**Migration from CheckM1:**
CheckM2 is a drop-in replacement with comparable or better accuracy.

## Output Interpretation

**Completeness:**
- Percentage of expected marker genes present
- Higher is better (aim for ≥90% for high-quality)

**Contamination:**
- Percentage of marker genes duplicated (indicates mixed genomes)
- Lower is better (aim for ≤5% for high-quality)

**Model used:**
- "Specific Model": Domain/phylum-specific markers used
- "General Model": Broader marker set (lower confidence)

**Warnings:**
- Low coding density: May indicate poor assembly or eukaryotic contamination
- Unusual translation table: Check domain classification

## Integration with Binning

```bash
# Run binning
metabat2 -i contigs.fasta -a depth.txt -o bins/bin -t 16

# Assess quality
checkm2 predict --threads 30 --input bins/ --output-directory qc/

# Filter high-quality bins
awk -F'\t' '$2 >= 90 && $3 <= 5 {print $1}' qc/quality_report.tsv > hq_bins.txt

# Copy high-quality bins
mkdir hq_bins/
while read bin; do
  cp bins/$bin hq_bins/
done < hq_bins.txt
```

## Common Issues

- **Database not found**: Set `CHECKM2DB` environment variable or use `--database_path`
- **Low completeness**: Bin may be incomplete, fragmented, or from novel lineage
- **High contamination**: Bin contains multiple genomes; refine with additional binning
- **Memory errors**: Use `--lowmem` flag
- **Slow performance**: Ensure database is on fast storage; increase threads

## Domain Specificity

CheckM2 is designed for **bacterial and archaeal genomes only**.

For eukaryotic bins, use **EukCC** instead:
```bash
# Classify bins first
# Then run domain-specific QC
checkm2 predict --input bacteria_bins/ --output-directory qc_bacteria/
eukcc single --input eukaryote_bins/ --output-directory qc_eukaryotes/
```

## Citation

Chklovski A, Parks DH, Woodcroft BJ, Tyson GW. (2023)
CheckM2: a rapid, scalable and accurate tool for assessing microbial genome quality using machine learning.
*Nature Methods* 20:1203-1212. https://doi.org/10.1038/s41592-023-01940-w
