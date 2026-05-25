# BRAKER

Pipeline for eukaryotic genome annotation using GeneMark and AUGUSTUS.

## Official Documentation
- GitHub: https://github.com/Gaius-Augustus/BRAKER
- Manual: https://github.com/Gaius-Augustus/BRAKER/blob/master/docs/userguide.pdf

## Installation

### Container (Recommended)

```bash
# Singularity
singularity build braker3.sif docker://teambraker/braker3:latest
singularity exec braker3.sif braker.pl

# Docker
docker pull teambraker/braker3:latest
docker run -v $(pwd):/data teambraker/braker3:latest braker.pl
```

### Manual Setup

Requires:
- GeneMark-ETP (https://github.com/gatech-genemark/GeneMark-ETP)
- AUGUSTUS 3.5.0+ (https://github.com/Gaius-Augustus/Augustus)
- Perl modules: File::Spec::Functions, Hash::Merge, Parallel::ForkManager, YAML

```bash
export GENEMARK_PATH=/path/to/GeneMark/
export AUGUSTUS_CONFIG_PATH=/path/to/Augustus/config/
export AUGUSTUS_BIN_PATH=/path/to/Augustus/bin/
export AUGUSTUS_SCRIPTS_PATH=/path/to/Augustus/scripts/
```

## Key Command-Line Flags

| Flag | Description |
|------|-------------|
| `--genome=FILE` | Input genome (softmasked FASTA) |
| `--bam=FILE` | RNA-Seq alignments (BAM format) |
| `--prot_seq=FILE` | Protein database for homology |
| `--threads=INT` | Number of CPU threads |
| `--ab_initio` | De novo prediction without evidence |
| `--fungus` | Enable fungal-specific parameters |
| `--stranded=+,-,.` | RNA-Seq strandedness |
| `--UTR=on` | Predict untranslated regions |
| `--makehub` | Generate UCSC Genome Browser hub |
| `--busco_lineage` | Run BUSCO completeness check |
| `--gff3` | Output in GFF3 format |

## Common Usage Examples

### RNA-Seq Based Prediction

```bash
braker.pl \
    --genome=genome.fa \
    --bam=rnaseq.bam \
    --threads=8 \
    --softmasking
```

### Protein Homology Based

```bash
braker.pl \
    --genome=genome.fa \
    --prot_seq=orthodb_proteins.fa \
    --threads=8
```

### Combined RNA-Seq + Proteins (Highest Accuracy)

```bash
braker.pl \
    --genome=genome.fa \
    --bam=rnaseq.bam \
    --prot_seq=proteins.fa \
    --threads=16 \
    --gff3
```

### Ab Initio (Genome Only)

```bash
braker.pl \
    --genome=genome.fa \
    --ab_initio \
    --threads=8
```

### Fungal Genome with UTR Prediction

```bash
braker.pl \
    --genome=genome.fa \
    --bam=rnaseq.bam \
    --fungus \
    --UTR=on \
    --threads=8
```

## Input/Output Formats

**Inputs:**
- Genome: Softmasked FASTA (repeats in lowercase)
- RNA-Seq: Coordinate-sorted, indexed BAM files
- Proteins: FASTA sequences (OrthoDB recommended)

**Outputs:**
- `braker.gtf` - Gene structures (GTF format)
- `braker.gff3` - Gene structures (GFF3 format)
- `braker.aa` - Protein sequences
- `braker.codingseq` - CDS sequences
- `augustus.hints.gtf` - AUGUSTUS predictions with hints
- Species parameter files (in AUGUSTUS config)

## Performance Tips

### Genome Preparation
- Use high-quality assemblies (avoid fragmented genomes)
- Remove very short scaffolds (<1kb)
- Apply repeat masking (softmasking preferred)
- Simplify scaffold names (avoid special characters)

### RNA-Seq Requirements
- High coverage of introns improves training
- Multiple RNA-Seq samples increase accuracy
- Coordinate-sort and index BAM files
- Specify strandedness if known

### Protein Database Selection
- Use OrthoDB or similar curated databases
- Include diverse representatives of protein families
- More proteins = better homology evidence

### Resource Allocation
- Allocate 4-8GB RAM per thread
- More threads reduce wall-clock time
- I/O-bound on large genomes (use SSD if possible)

### Quality Control
- Always run BUSCO on final predictions
- Visually inspect predictions in genome browser
- Check for unrealistic gene counts

## Pipeline Modes

1. **Genome only** - GeneMark-ES (lowest accuracy)
2. **RNA-Seq** - GeneMark-ET + RNA hints (medium accuracy)
3. **Proteins** - GeneMark-EP + protein hints (variable accuracy)
4. **RNA-Seq + Proteins** - GeneMark-ETP combined (highest accuracy)
