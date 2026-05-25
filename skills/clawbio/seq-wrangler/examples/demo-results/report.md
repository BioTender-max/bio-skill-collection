# Seq Wrangler Report

**Date**: 2026-04-19 04:31 UTC
**Tool**: ClawBio Seq Wrangler v0.1.0
**Mode**: Demo (synthetic data)

---

## Run parameters

| Parameter | Value |
|-----------|-------|
| Aligner | bwa |
| MAPQ threshold | ≥20 |
| Duplicate handling | Mark only |
| Samples processed | 2 |

---

## Results per sample

### CTRL_REP1 (Paired-end)

**Alignment statistics**

| Metric | Value |
|--------|-------|
| Total reads | 10,000,000 |
| Mapped reads | 9,750,000 (97.5%) |
| Duplicates | 850,000 |
| Properly paired | 9,500,000 |

**Coverage (top chromosomes)**

| Chromosome | Mean depth | Breadth |
|------------|------------|---------|
| chr1 | 28.4x | 97.0% |
| chr2 | 27.9x | 96.0% |
| chrX | 14.2x | 91.0% |
| chrM | 1842.0x | 100.0% |

**Insert size**: mean 312.4 bp | median 305.0 bp | std 48.2 bp

**BAM**: `examples/demo-results/bam/CTRL_REP1_sorted.bam`

### TREAT_REP1 (Single-end)

**Alignment statistics**

| Metric | Value |
|--------|-------|
| Total reads | 8,500,000 |
| Mapped reads | 8,200,000 (96.5%) |
| Duplicates | 600,000 |

**Coverage (top chromosomes)**

| Chromosome | Mean depth | Breadth |
|------------|------------|---------|
| chr1 | 24.1x | 95.0% |
| chr2 | 23.8x | 94.0% |
| chrX | 23.5x | 94.0% |
| chrM | 1560.0x | 100.0% |

**BAM**: `examples/demo-results/bam/TREAT_REP1_sorted.bam`


---

## Methods

- **QC**: FastQC per-sample quality assessment
- **Trimming**: fastp (if --trim flag used)
- **Alignment**: bwa with MAPQ ≥ 20 filter
- **BAM processing**: samtools sort -n → fixmate → coordinate-sort → markdup (mark only) → index
- **Coverage**: samtools coverage (per-chromosome mean depth and breadth)
- **Insert size**: samtools stats IS histogram (paired-end only)
- **MultiQC**: aggregated QC report across samples (if --run-multiqc)

## Input checksums

- `demo_ctrl_R1.fastq.gz`: demo data (no file on disk)- `demo_treat_R1.fastq.gz`: demo data (no file on disk)

## Disclaimer

> ClawBio Seq Wrangler is a research and educational tool. Results must be validated before use in clinical or production settings.
