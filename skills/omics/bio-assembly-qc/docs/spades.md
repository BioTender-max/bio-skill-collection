# SPAdes v4.2.0 Usage Guide

## Official Documentation
- Website: https://github.com/ablab/spades
- Manual: https://github.com/ablab/spades#manual

## Installation

**Via Conda/Pixi:**
```bash
conda install -c bioconda spades=4.2.0
```

**Binary Download:**
Download pre-compiled binaries from the [releases page](https://github.com/ablab/spades/releases).

**Requirements:**
- Python 3.8+
- g++ 9.0+ (if building from source)
- zlib and libbz2

**Verification:**
```bash
spades.py --test
```

## Key Command-Line Flags

| Flag | Purpose |
|------|---------|
| `--isolate` | Standard bacterial genome assembly (recommended) |
| `--sc` | Single-cell bacterial assembly |
| `--plasmid` | Plasmid discovery and assembly |
| `--meta` | Metagenomic assembly |
| `--metaplasmid` | Metagenomic plasmid discovery |
| `--metaviral` | Viral genome assembly from metagenomic data |
| `--rna` | Transcriptome assembly |
| `-1` / `-2` | Paired-end read files (left/right) |
| `-s` | Unpaired reads |
| `--pacbio` | PacBio long reads for hybrid assembly |
| `--nanopore` | Oxford Nanopore reads for hybrid assembly |
| `-o` | Output directory |
| `-t` | Number of threads |
| `-m` | Memory limit in GB |
| `-k` | K-mer sizes (comma-separated, odd values) |
| `--only-assembler` | Skip read correction |
| `--careful` | Reduce mismatches and indels (slower) |
| `--continue` | Resume from last checkpoint |

## Common Usage Examples

**Standard bacterial genome (Illumina paired-end):**
```bash
spades.py --isolate -1 reads_R1.fastq.gz -2 reads_R2.fastq.gz \
  -o spades_output -t 16 -m 64
```

**Metagenomic assembly:**
```bash
spades.py --meta -1 reads_R1.fastq.gz -2 reads_R2.fastq.gz \
  -o metaspades_output -t 16 -m 128
```

**Hybrid assembly (Illumina + PacBio):**
```bash
spades.py --isolate -1 reads_R1.fastq.gz -2 reads_R2.fastq.gz \
  --pacbio pacbio_reads.fastq.gz -o hybrid_output -t 16 -m 64
```

**IonTorrent single-end reads:**
```bash
spades.py --iontorrent -s iontorrent_reads.fastq.gz \
  -o iontorrent_output -t 8 -m 32
```

**Custom k-mer sizes:**
```bash
spades.py --isolate -1 reads_R1.fastq.gz -2 reads_R2.fastq.gz \
  -k 21,33,55,77 -o custom_kmers -t 16 -m 64
```

## Input/Output Formats

**Supported Input:**
- FASTQ (uncompressed or gzip-compressed)
- Second-generation sequencing: Illumina, IonTorrent
- Supplementary long reads: PacBio, Oxford Nanopore
- Paired-end, mate-pair, or unpaired reads

**Output Files (in output directory):**
- `contigs.fasta` — Final assembled contigs
- `scaffolds.fasta` — Scaffolded contigs
- `assembly_graph.fastg` — Assembly graph
- `assembly_graph_with_scaffolds.gfa` — Graph in GFA format
- `spades.log` — Detailed execution log
- `params.txt` — Command-line parameters used
- `corrected/` — Corrected reads (if not using --only-assembler)
- `K*/` — Intermediate files for each k-mer size

## Performance Tips

1. **Memory management:**
   - Set `-m` to 80-90% of available RAM
   - For low memory, use `--only-assembler` to skip read correction

2. **Thread optimization:**
   - Use `-t` equal to physical CPU cores
   - Diminishing returns beyond 16-32 threads for most datasets

3. **K-mer selection:**
   - Default auto-selection works well for most cases
   - For large genomes (>100 Mbp), add larger k-mers: `-k 21,33,55,77,99,127`
   - For low-coverage data, use smaller k-mers: `-k 21,33,55`

4. **Resume interrupted runs:**
   - Use `--continue` to restart from the last checkpoint
   - Saves hours on large assemblies

5. **Quality vs speed:**
   - `--careful` improves accuracy but increases runtime by 2-3x
   - `--only-assembler` saves 30-50% runtime by skipping correction

6. **Disk space:**
   - Requires 10-20x the compressed input size
   - Clean up intermediate files after successful assembly

7. **Troubleshooting:**
   - Check `spades.log` and `params.txt` for debugging
   - Use `--isolate` for bacterial genomes instead of default mode
   - For hybrid assembly, ensure long reads are in separate file(s)
