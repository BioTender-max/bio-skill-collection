# Tool Documentation

Last updated: 2026-02-01

## Assembly tools

### SPAdes v4.0.0+
Versatile genome assembler for short-read data (Illumina, IonTorrent) with support for hybrid assembly using long reads. v4.0.0 is the final feature release; the project continues with bug-fix-only updates.

- Documentation: [spades.md](spades.md)
- Official website: https://github.com/ablab/spades
- Use cases: bacterial genomes, metagenomes, plasmids, single-cell, hybrid assemblies

### Flye / metaFlye v2.9.5+
Long-read assembler for PacBio and Oxford Nanopore data with sophisticated repeat resolution. metaFlye mode (`--meta`) is the baseline for long-read metagenome assembly when HiFi-tuned alternatives are not available.

- Documentation: [flye.md](flye.md)
- Official website: https://github.com/fenderglass/Flye
- Use cases: PacBio/ONT isolates and metagenomes; ONT-only HiFi-poor datasets

### metaMDBG v1.1 (preferred for HiFi metagenomes)
Minimizer-based de Bruijn graph assembler tuned for PacBio HiFi metagenomes. Produces ~2× more circularized high-quality MAGs than metaFlye on HiFi data and recovers more viruses and plasmids (*Nature Biotechnology* 2024, DOI: 10.1038/s41587-023-01983-6).

- Official website: https://github.com/GaetanBenoitDev/metaMDBG
- Use cases: PacBio HiFi metagenomes (preferred over metaFlye for this read type)

### myloasm (optional, large or diverse long-read datasets)
Fast long-read metagenome assembler released in 2025. Consider when runtime is the binding constraint on diverse or very large datasets and the read profile matches its assumptions. Document the choice in the run log.

- Source: see preprint and project repo when adding to your environment

## Quality Control Tools

### QUAST v5.3+
Comprehensive assembly quality assessment tool providing contiguity, completeness, and correctness metrics.

- Documentation: [quast.md](quast.md)
- Official website: http://quast.sourceforge.net/
- Use cases: Assembly QC, assembler comparison, reference-based/free evaluation

## Quick Start

**Typical workflow:**
```bash
# 1. Assemble with SPAdes (short reads)
spades.py --isolate -1 reads_R1.fastq.gz -2 reads_R2.fastq.gz -o spades_out -t 16

# OR assemble with Flye (long reads)
flye --nano-hq ont_reads.fastq.gz --genome-size 5m --out-dir flye_out --threads 16

# 2. Evaluate assembly quality
quast.py spades_out/contigs.fasta -r reference.fasta -o qc_results -t 8
```

## Tool selection guide

| Read type | Genome type | Recommended tool | Alternative |
|-----------|-------------|------------------|-------------|
| Illumina paired-end | Bacterial isolate | `spades.py --isolate` | — |
| Illumina paired-end | Metagenomic | `spades.py --meta` | — |
| PacBio HiFi | Isolate | `flye --pacbio-hifi` | — |
| PacBio HiFi | Metagenomic | **metaMDBG v1.1** | metaFlye `--meta --pacbio-hifi` |
| ONT Q20+ | Isolate | `flye --nano-hq` | — |
| ONT Q20+ | Metagenomic | metaFlye `--meta --nano-hq` | myloasm (when speed-bound) |
| Illumina + PacBio | Hybrid | SPAdes (hybrid) | Flye + short-read polishing |
| Illumina + ONT | Hybrid | SPAdes (hybrid) | Flye + short-read polishing |

## Performance Considerations

| Tool | Memory (bacterial) | Memory (human) | Runtime (bacterial) | Runtime (human) |
|------|-------------------|----------------|---------------------|-----------------|
| SPAdes | 8-32 GB | 128-256 GB | 1-4 hours | 24-72 hours |
| Flye | 2-4 GB | 141-450 GB | 1-2 hours | 780-4000 CPU hours |
| QUAST | 2-8 GB | 16-64 GB | 5-30 minutes | 1-4 hours |

## Additional Resources

- All tools available via pixi (see `pixi.toml` in skill root)
- Paper summaries with use cases: `../summaries/`
