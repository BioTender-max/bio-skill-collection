# 🧬 Seq Wrangler

**ClawBio skill** — FASTQ QC, alignment, and BAM processing pipeline for NGS data.

Part of the [ClawBio](https://github.com/ClawBio/ClawBio) bioinformatics AI agent skill library.

## Quick Start

```bash
# Demo (no external tools needed)
python skills/seq-wrangler/seq_wrangler.py --demo --output /tmp/demo

# Single sample paired-end
python skills/seq-wrangler/seq_wrangler.py \
    --r1 sample_R1.fastq.gz \
    --r2 sample_R2.fastq.gz \
    --index ref/hg38 \
    --aligner bowtie2 \
    --output results/

# Batch mode via samplesheet
python skills/seq-wrangler/seq_wrangler.py \
    --samplesheet samples.csv \
    --index ref/hg38 \
    --output results/
```

## What it produces
```bash
output/
├── report.md # Full alignment and QC report
├── summary.json # Per-sample stats as JSON
├── bam/
│ └── sample_sorted.bam # Final sorted, markdup BAM + .bai index
├── alignment/
│ └── sample.sam # Intermediate SAM (only with --keep-sam)
└── reproducibility/
├── commands.sh # Reproduce this exact run
├── environment.yml # Conda environment
├── checksums.sha256 # SHA-256 of all input files
└── run_metadata.json # Full run parameters
```

## Options

| Flag | Description | Default |
|---|---|---|
| `--r1` | FASTQ R1 or single-end FASTQ | — |
| `--r2` | FASTQ R2 for paired-end | — |
| `--samplesheet` | CSV with columns `sample,fastq1,fastq2` | — |
| `--index` | Aligner index prefix | required |
| `--aligner` | `bwa`, `bowtie2`, or `minimap2` | `bwa` |
| `--genome-build` | `GRCh38` or `GRCh37` | `GRCh38` |
| `--output` | Output directory | required |
| `--threads` | Number of threads | auto |
| `--mapq` | MAPQ filter threshold | `20` |
| `--trim` | Run fastp trimming before alignment | off |
| `--remove-duplicates` | Remove duplicates with `samtools markdup -r` | off |
| `--keep-sam` | Keep intermediate SAM files | off |
| `--run-fastqc` | Run FastQC if available | off |
| `--run-multiqc` | Run MultiQC aggregation if available | off |
| `--demo` | Run with synthetic data, no tools needed | off |

## Pipeline steps

1. **FastQC** — per-sample quality assessment (optional)
2. **fastp** — adapter trimming and QC (optional, `--trim`)
3. **Alignment** — BWA MEM / Bowtie2 / Minimap2
4. **samtools view** — filter by MAPQ threshold
5. **samtools sort -n** — sort by read name
6. **samtools fixmate** — fix mate-pair information
7. **samtools sort** — coordinate sort
8. **samtools markdup** — mark (or remove) PCR duplicates
9. **samtools index** — index final BAM
10. **samtools flagstat / coverage / stats** — alignment statistics
11. **MultiQC** — aggregated QC report (optional)
12. **Report** — Markdown report + reproducibility bundle

## Dependencies

Install via conda (recommended):

```bash
conda install -c bioconda samtools bowtie2 bwa minimap2 fastqc fastp multiqc
```

Or use the included environment file:

```bash
conda env create -f skills/seq-wrangler/reproducibility/environment.yml
conda activate clawbio-seq-wrangler
```

## Run Tests

```bash
python -m pytest skills/seq-wrangler/tests/ -v
```

## Author

Contributed by [Daniel Garbozo](https://github.com/DanielGarbozo)  — resolves [Issue #10](https://github.com/ClawBio/ClawBio/issues/10).
