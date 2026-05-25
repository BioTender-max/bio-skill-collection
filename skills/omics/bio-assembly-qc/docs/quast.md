# QUAST v5.3.0 Usage Guide

## Official Documentation
- Website: http://quast.sourceforge.net/
- Manual: http://quast.sourceforge.net/docs/manual.html
- GitHub: https://github.com/ablab/quast

## Installation

**Via Conda/Pixi:**
```bash
conda install -c bioconda quast=5.3.0
```

**Via pip:**
```bash
pip install quast
```

**From tarball:**
```bash
wget https://github.com/ablab/quast/releases/download/quast_5.3.0/quast-5.3.0.tar.gz
tar -xzf quast-5.3.0.tar.gz
cd quast-5.3.0
./setup.py install
```

**Requirements:**
- Python 3.5+
- Perl 5.6.0+ (for GeneMarkS)
- Java (for GRIDSS)
- matplotlib, joblib, simplejson (installed automatically)

## Key Command-Line Flags

| Flag | Purpose |
|------|---------|
| `-r <file>` | Reference genome (enables reference-based metrics) |
| `-g <file>` | Gene annotations (GFF/BED/NCBI format) |
| `-m <int>` | Minimum contig length (default: 500 bp) |
| `-t <int>` | Number of threads (default: 25% of CPUs) |
| `-o <dir>` | Output directory |
| `-l <labels>` | Comma-separated assembly names for report |
| `--large` | Optimized for genomes >100 Mbp |
| `--k-mer-stats` | Compute k-mer-based quality metrics |
| `-e` / `--eukaryote` | Eukaryotic genome (affects gene prediction) |
| `--fungus` | Fungal genome |
| `--gene-finding` | Enable gene prediction (with GeneMarkS) |
| `--conserved-genes-finding` | Search for BUSCO orthologs |
| `--fast` | Fast mode (skip time-consuming analyses) |
| `--no-plots` | Skip plot generation |
| `--no-html` | Skip HTML report generation |
| `--no-snps` | Skip SNP calling |
| `--memory-efficient` | Reduce memory usage |
| `--space-efficient` | Reduce disk usage (skip auxiliary files) |
| `--min-identity <float>` | Minimum alignment identity (default: 95.0) |
| `--ambiguity-usage <all\|one\|none>` | Ambiguous base handling |

## Common Usage Examples

**Basic assembly QC without reference:**
```bash
quast.py assembly.fasta -o quast_output -t 8
```

**With reference genome:**
```bash
quast.py assembly.fasta -r reference.fasta \
  -o quast_ref_output -t 8
```

**Compare multiple assemblies:**
```bash
quast.py assembly1.fasta assembly2.fasta assembly3.fasta \
  -r reference.fasta -l "SPAdes,Flye,Canu" \
  -o comparison_output -t 16
```

**With gene annotations:**
```bash
quast.py assembly.fasta -r reference.fasta \
  -g genes.gff -o quast_genes -t 8
```

**Large genome (>100 Mbp):**
```bash
quast.py large_assembly.fasta -r reference.fasta \
  --large --k-mer-stats -o large_genome_qc -t 32
```

**Eukaryotic genome with gene finding:**
```bash
quast.py eukaryote_assembly.fasta -r reference.fasta \
  --eukaryote --gene-finding --conserved-genes-finding \
  -o eukaryote_qc -t 16
```

**Fast mode for quick check:**
```bash
quast.py assembly.fasta -r reference.fasta \
  --fast --no-plots -o quick_check -t 4
```

**Metagenomic assemblies:**
```bash
metaquast.py metagenome_assembly.fasta \
  -r ref1.fasta,ref2.fasta,ref3.fasta \
  -o metaquast_output -t 16
```

## Input/Output Formats

**Supported Input:**
- Assemblies: FASTA (uncompressed, gzip, or bzip2)
- References: FASTA (uncompressed, gzip, or bzip2)
- Reads: FASTQ (Illumina, PacBio, Oxford Nanopore)
- Annotations: GFF 2/3, BED, NCBI gene format, tab-separated

**Output Files (in output directory):**
- `report.txt` — Plain text summary report
- `report.tsv` — Tab-separated report (easy to parse)
- `report.pdf` — PDF report with plots
- `report.html` — Interactive HTML report
- `icarus.html` — Interactive contig browser
- `transposed_report.tsv` — Metrics in columns, assemblies in rows
- `contigs_reports/` — Detailed per-contig analysis
- `contigs_reports/misassemblies_report.txt` — Misassembly details
- `contigs_reports/unaligned_report.txt` — Unaligned contigs
- `aligned_stats/` — Alignment statistics
- `genome_stats/` — Reference genome statistics
- `basic_stats/` — Basic assembly statistics
- `quast.log` — Execution log

## Key Metrics Explained

**Contiguity Metrics:**
- N50 / NG50: Longer is better (assembly contiguity)
- L50 / LG50: Smaller is better (number of large contigs)
- Total length: Should match expected genome size

**Completeness Metrics:**
- Genome fraction: Percentage of reference covered
- Duplication ratio: Should be close to 1.0
- Genes found: Number of complete genes

**Correctness Metrics:**
- Misassemblies: Fewer is better
- Mismatches per 100 kbp: Lower is better
- Indels per 100 kbp: Lower is better

## Performance Tips

1. **Speed optimization:**
   - Use `--fast` to skip time-consuming analyses
   - Disable plots with `--no-plots` if not needed
   - Skip SNP calling with `--no-snps` for large genomes

2. **Memory efficiency:**
   - Use `--memory-efficient` for limited RAM systems
   - Reduce threads with `-t 1` for very low memory
   - Use `--space-efficient` to minimize disk usage

3. **Thread scaling:**
   - Good scaling up to 16-32 threads
   - Use `-t` equal to physical CPU cores
   - Diminishing returns beyond 32 threads

4. **Large genome handling:**
   - Use `--large` for genomes >100 Mbp
   - Combine with `--k-mer-stats` for thorough evaluation
   - Consider `--memory-efficient` if RAM is limited

5. **Reference-free mode:**
   - Faster and requires less memory
   - Still provides basic metrics (N50, L50, total length)
   - No misassembly or correctness metrics

6. **K-mer statistics:**
   - Use `--k-mer-stats` for reference-free quality assessment
   - Detects errors even without reference genome
   - Adds 10-30% to runtime

7. **Gene prediction:**
   - `--gene-finding` requires GeneMarkS (separate license)
   - `--conserved-genes-finding` uses BUSCO (automatic download)
   - Both significantly increase runtime (2-10x)

8. **Metagenomic assemblies:**
   - Use `metaquast.py` instead of `quast.py`
   - Provide multiple reference genomes
   - Requires more memory and time (2-5x)

9. **Comparing many assemblies:**
   - QUAST handles 10-50 assemblies efficiently
   - Use meaningful labels with `-l` flag
   - Consider `--no-plots` for >20 assemblies

10. **Disk space:**
    - Basic run: 2-5x assembly size
    - With plots and reports: 5-10x assembly size
    - Use `--space-efficient` to reduce by 50%

11. **HTML report features:**
    - Interactive plots for comparing assemblies
    - Icarus contig browser for visual alignment inspection
    - Export plots as SVG for publications

12. **Interpreting results:**
    - Focus on NG50 (reference-based) over N50
    - Check misassembly rate (should be <1 per Mbp)
    - Verify genome fraction is >95% for complete assemblies
    - Compare multiple assemblers to find best result
