# Flye v2.9.6 Usage Guide

## Official Documentation
- Website: https://github.com/fenderglass/Flye
- Manual: https://github.com/fenderglass/Flye/blob/2.9.6/docs/USAGE.md

## Installation

**Via Conda/Pixi:**
```bash
conda install -c bioconda flye=2.9.6
```

**Via pip:**
```bash
pip install flye
```

**From source:**
```bash
git clone https://github.com/fenderglass/Flye
cd Flye
python setup.py install
```

**Requirements:**
- Python 3.7+
- C++ compiler (for building from source)

## Key Command-Line Flags

| Flag | Purpose |
|------|---------|
| `--pacbio-raw` | PacBio regular CLR reads (<20% error) |
| `--pacbio-corr` | PacBio corrected reads |
| `--pacbio-hifi` | PacBio HiFi reads (<1% error) |
| `--nano-raw` | ONT regular reads, pre-Guppy5 (<20% error) |
| `--nano-corr` | ONT corrected reads |
| `--nano-hq` | ONT high-quality reads (Guppy5+ SUP, Q20, 3-5% error) |
| `--genome-size` | Estimated genome size (e.g., 5m, 2.6g) |
| `--out-dir` | Output directory |
| `--threads` | Number of threads |
| `--iterations` | Number of polishing iterations (default: 1) |
| `--meta` | Metagenome assembly mode |
| `--plasmids` | Enable plasmid detection |
| `--scaffold` | Enable scaffolding (disabled by default since v2.9) |
| `--no-alt-contigs` | Remove alternative contigs from final assembly |
| `--keep-haplotypes` | Preserve heterozygous structural variants |
| `--asm-coverage` | Assembly coverage threshold |
| `--min-overlap` | Minimum overlap between reads (auto-selected up to 10kb) |
| `--resume` | Resume from the last completed stage |
| `--resume-from` | Resume from specific stage (e.g., assembly, polishing) |

## Common Usage Examples

**Bacterial genome (ONT high-quality reads):**
```bash
flye --nano-hq ont_reads.fastq.gz --genome-size 5m \
  --out-dir flye_output --threads 16
```

**Bacterial genome (PacBio HiFi):**
```bash
flye --pacbio-hifi hifi_reads.fastq.gz --genome-size 5m \
  --out-dir flye_output --threads 16
```

**Human genome (ONT Q20+ reads):**
```bash
flye --nano-hq ont_q20.fastq.gz --genome-size 3g \
  --out-dir human_assembly --threads 64 --scaffold
```

**Metagenome assembly:**
```bash
flye --nano-hq meta_reads.fastq.gz --genome-size 100m \
  --meta --out-dir metaflye_output --threads 32
```

**With plasmid detection:**
```bash
flye --nano-hq reads.fastq.gz --genome-size 5m \
  --plasmids --out-dir flye_plasmids --threads 16
```

**Resume interrupted assembly:**
```bash
flye --nano-hq reads.fastq.gz --genome-size 5m \
  --out-dir flye_output --threads 16 --resume
```

## Input/Output Formats

**Supported Input:**
- FASTA or FASTQ (uncompressed or gzip-compressed)
- PacBio raw CLR, corrected, or HiFi reads
- Oxford Nanopore raw, corrected, or high-quality reads
- Multiple input files can be specified (space-separated)

**Output Files (in output directory):**
- `assembly.fasta` — Final polished assembly
- `assembly_info.txt` — Contig statistics and coverage
- `assembly_graph.gfa` — Assembly graph with paths and coverage
- `assembly_graph.gv` — Graph in GraphViz format
- `flye.log` — Detailed execution log
- `params.json` — Parameters used for assembly
- `00-assembly/` — Raw assembly before polishing
- `10-consensus/` — Consensus sequences
- `20-repeat/` — Repeat graph analysis
- `30-contigger/` — Contig construction
- `40-polishing/` — Polishing iterations

## Performance Tips

1. **Read type selection:**
   - Use `--nano-hq` for ONT Guppy5+ SUP mode (Q20+ reads)
   - Use `--pacbio-hifi` for HiFi reads (99%+ accuracy)
   - Correct read type dramatically affects assembly quality

2. **Genome size estimation:**
   - Provide accurate `--genome-size` estimate
   - For metagenomes, estimate total metagenome size
   - Affects coverage calculations and repeat resolution

3. **Memory requirements (benchmarks from documentation):**
   - E. coli (5 Mbp, 50x): 2 GB RAM, 2 hours
   - Human genome (3 Gbp, 30-60x): 141-450 GB RAM, 780-4000 CPU hours
   - Scale memory with genome size and coverage

4. **Thread optimization:**
   - Use all available cores for large genomes
   - Diminishing returns beyond 64 threads
   - I/O becomes bottleneck with too many threads

5. **Coverage considerations:**
   - Minimum: 30x coverage for bacterial genomes
   - Optimal: 50-100x coverage for complex genomes
   - Higher coverage improves repeat resolution

6. **Polishing iterations:**
   - Default 1 iteration usually sufficient for HiFi/Q20 reads
   - Increase to 2-3 for lower quality data
   - Use external polishers (Medaka, Racon) for further improvement

7. **Metagenome assembly:**
   - Use `--meta` flag for metagenomic data
   - Requires higher coverage (100x+) for low-abundance organisms
   - Set realistic `--genome-size` as total metagenome size

8. **Disk space:**
   - Requires 50-100x the input file size
   - Use `--resume` to avoid re-running failed assemblies
   - Clean intermediate directories after successful completion

9. **Graph visualization:**
   - View `assembly_graph.gfa` with Bandage or AGB
   - GFA includes read coverage (RC tags) for manual curation
   - Useful for identifying misassemblies or structural variants

10. **Scaffolding:**
    - Disabled by default since v2.9
    - Enable with `--scaffold` for chromosome-level assemblies
    - Works best with high-coverage, long-read data
