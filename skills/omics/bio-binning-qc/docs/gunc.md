# GUNC v1.0.6

Detection of chimerism and contamination in prokaryotic genomes using lineage homogeneity analysis.

## Official Documentation
- GitHub: https://github.com/grp-bork/gunc
- Documentation: https://grp-bork.embl-community.io/gunc/
- Publication: Orakov et al. (2021) *Genome Biology*
- Version: 1.0.6

## Installation

**Conda/Bioconda (recommended):**
```bash
conda install -c bioconda gunc
# or
mamba install -c bioconda gunc
```

**PyPI:**
```bash
pip install gunc
```

**From source:**
```bash
git clone https://github.com/grp-bork/gunc.git
cd gunc
pip install -e .
```

## Database Setup

**Download database:**
GUNC requires one of two reference databases:

```bash
# Option 1: ProGenomes database
gunc download_db -db progenomes -o gunc_db/

# Option 2: GTDB database (larger, more comprehensive)
gunc download_db -db gtdb -o gunc_db/
```

**Database sizes:**
- ProGenomes: ~7 GB
- GTDB: ~30 GB

**Recommendation:** Use GTDB for most comprehensive detection, ProGenomes for faster processing.

## Key Command-Line Flags

| Flag | Description |
|------|-------------|
| `-i, --input_dir` | Directory containing genome FASTA files |
| `-r, --input_file` | Single genome FASTA file |
| `-d, --db_file` | Path to GUNC database |
| `-o, --out_dir` | Output directory |
| `-t, --threads` | Number of threads |
| `--detailed_output` | Generate detailed per-contig output |
| `--sensitive` | Use sensitive mode (slower, more accurate) |
| `--temp_dir` | Temporary directory for intermediate files |

## Common Usage Examples

### Run on directory of bins
```bash
gunc run --input_dir bins/ \
  --db_file gunc_db/gunc_db_progenomes2.1.dmnd \
  --out_dir gunc_output/ \
  --threads 16
```

### Run on single genome
```bash
gunc run --input_file bin1.fasta \
  --db_file gunc_db/gunc_db_progenomes2.1.dmnd \
  --out_dir gunc_output/ \
  --threads 8
```

### With detailed output and sensitive mode
```bash
gunc run --input_dir bins/ \
  --db_file gunc_db/gunc_db_gtdb.dmnd \
  --out_dir gunc_output/ \
  --threads 16 \
  --detailed_output \
  --sensitive
```

### Using GTDB database
```bash
gunc run --input_dir bins/ \
  --db_file gunc_db/gunc_db_gtdb.dmnd \
  --out_dir gunc_output/ \
  --threads 32
```

## Input Requirements

**Genome/bin files:**
- FASTA format (nucleotide sequences)
- Prokaryotic genomes (bacteria and archaea)
- Can be complete genomes or MAGs
- Minimum size: ~100 kb (smaller bins may have unreliable results)

**Domain specificity:**
GUNC is designed for **prokaryotic genomes only**. Do not use on eukaryotic bins.

## Output Format

**Main output file:** `GUNC.progenomes_2.1.maxCSS_level.tsv` (or GTDB equivalent)

Key columns:
- `genome` - Genome/bin name
- `n_genes_called` - Number of genes predicted
- `n_genes_mapped` - Number of genes mapped to database
- `n_contigs` - Number of contigs
- `taxonomic_level` - Level where contamination detected
- `proportion_genes_retained_in_major_clades` - Fraction of genes in dominant clade
- `genes_retained_index` - Gene retention metric
- `clade_separation_score` (CSS) - Main contamination metric
- `contamination_portion` - Estimated contamination fraction
- `n_effective_surplus_clades` - Number of contaminant lineages
- `mean_hit_identity` - Average sequence identity to database
- `reference_representation_score` - Reference genome coverage
- `pass.GUNC` - Binary pass/fail flag

## Understanding CSS (Clade Separation Score)

**CSS is the primary metric for detecting chimeras:**
- Range: 0.0 to 1.0
- **CSS > 0.45**: Genome flagged as putatively contaminated/chimeric
- Lower values: More homogeneous (likely single organism)
- Higher values: More heterogeneous (likely chimeric or contaminated)

**Interpretation:**
- CSS 0.0-0.30: Clean genome (high confidence)
- CSS 0.30-0.45: Borderline (review manually)
- CSS 0.45-0.60: Likely contaminated
- CSS >0.60: Highly chimeric

## Quality Filtering

**Flag contaminated bins:**
```bash
# Extract bins that pass GUNC
awk -F'\t' '$NF == "True" {print $1}' GUNC.progenomes_2.1.maxCSS_level.tsv > passing_bins.txt

# Extract contaminated bins (CSS > 0.45)
awk -F'\t' '$8 > 0.45 {print $1}' GUNC.progenomes_2.1.maxCSS_level.tsv > contaminated_bins.txt
```

**Combined filtering with CheckM2:**
```bash
# High-quality, non-chimeric bins
# CheckM2: ≥90% complete, ≤5% contamination
# GUNC: pass.GUNC == True

# Join results
join -t $'\t' \
  <(awk -F'\t' '$2>=90 && $3<=5 {print $1}' checkm2/quality_report.tsv | sort) \
  <(awk -F'\t' '$NF=="True" {print $1}' gunc_output/GUNC.*.tsv | sort) \
  > high_quality_clean_bins.txt
```

## Performance Tips

1. **Database selection**: ProGenomes for speed, GTDB for comprehensiveness
2. **Threading**: Scales well with CPU cores (16-32 threads typical)
3. **Sensitive mode**: Use for critical applications (slower but more accurate)
4. **Batch processing**: Process all bins in one run for efficiency
5. **Memory**: ~8-16 GB RAM for typical runs; more for GTDB with many bins

## Output Interpretation

**pass.GUNC flag:**
- `True`: Genome passes (CSS ≤ 0.45 at all taxonomic levels)
- `False`: Genome fails (CSS > 0.45 at some level)

**contamination_portion:**
- Estimated fraction of genome that is contamination
- Used to quantify extent of chimerism

**n_effective_surplus_clades:**
- Number of distinct contaminant lineages detected
- Higher values indicate more complex contamination

**taxonomic_level:**
- Taxonomic rank where contamination was detected
- Examples: "phylum", "class", "order", "family", "genus"
- Lower ranks indicate closely related contaminants (harder to detect)

## Comparison with CheckM/CheckM2

GUNC complements CheckM2:
- **CheckM2**: Detects contamination via marker gene duplication
- **GUNC**: Detects chimerism via lineage heterogeneity

**Key difference:**
GUNC can detect contamination that CheckM2 misses, especially:
- Contamination from closely related taxa
- Chimeric assemblies from mis-binning
- Contamination without marker gene duplication

**Best practice:** Use both tools together.

## Integration with Binning QC

```bash
# Complete QC workflow
# 1. Assess completeness and contamination
checkm2 predict --input bins/ --output-directory checkm2_qc/ -t 16

# 2. Detect chimerism
gunc run --input_dir bins/ \
  --db_file gunc_db/gunc_db_progenomes2.1.dmnd \
  --out_dir gunc_qc/ \
  --threads 16

# 3. Filter high-quality, non-chimeric bins
comm -12 \
  <(awk -F'\t' '$2>=90 && $3<=5 {print $1}' checkm2_qc/quality_report.tsv | sort) \
  <(awk -F'\t' '$NF=="True" {print $1}' gunc_qc/GUNC.*.tsv | sort) \
  > high_quality_bins.txt

# 4. Copy passing bins
mkdir final_bins/
while read bin; do
  cp bins/$bin final_bins/
done < high_quality_bins.txt
```

## Common Issues

- **Database not found**: Ensure `--db_file` points to `.dmnd` file
- **No genes mapped**: Bin may be from novel lineage not in database
- **High CSS but low CheckM2 contamination**: Likely chimeric assembly
- **Memory errors**: Reduce thread count or use ProGenomes database
- **Slow performance**: Use ProGenomes or reduce `--sensitive` flag

## Advanced Usage

### Detailed per-contig output
```bash
gunc run --input_dir bins/ \
  --db_file gunc_db/gunc_db_progenomes2.1.dmnd \
  --out_dir gunc_output/ \
  --threads 16 \
  --detailed_output
```

This generates per-contig taxonomic assignments, useful for:
- Identifying contaminating contigs
- Manual bin refinement
- Understanding contamination sources

### Refining contaminated bins

For bins that fail GUNC, consider:
1. **Re-binning** with stricter parameters
2. **Manual curation** using detailed output to remove contaminating contigs
3. **Alternative binners** or ensemble approaches
4. **Increased sequencing depth** to improve coverage-based binning

## Sensitivity Mode

The `--sensitive` flag increases detection accuracy at the cost of runtime:
- More thorough database search
- Better handling of divergent sequences
- Recommended for final QC of high-value genomes

## Citation

Orakov A, Fullam A, Coelho LP, Khedkar S, Szklarczyk D, Mende DR, Schmidt TSB, Bork P. (2021)
GUNC: detection of chimerism and contamination in prokaryotic genomes.
*Genome Biology* 22:178. https://doi.org/10.1186/s13059-021-02393-0

## Key Findings from Publication

- 5.7% of GenBank genomes are undetected chimeras
- 5.2% of RefSeq genomes are contaminated
- 15-30% of "high-quality" MAGs in recent studies are chimeric
- GUNC detects contamination types missed by existing methods
