# InterProScan Usage Guide

## Overview

InterProScan is a genome-scale protein function classification tool that combines different protein signature recognition methods from the InterPro consortium member databases. It provides functional analysis by scanning protein sequences against predictive models (signatures) from multiple databases.

## Official Documentation

- Official Documentation: https://interproscan-docs.readthedocs.io/
- GitHub Repository: https://github.com/ebi-pf-team/interproscan
- Running Guide: https://interproscan-docsdev.readthedocs.io/en/stable/HowToRun.html
- Installation Guide: https://interproscan-docsdev.readthedocs.io/en/stable/HowToInstall.html
- InterPro Website: https://www.ebi.ac.uk/interpro/

## Installation

### InterProScan 6 (Nextflow-based)

Recommended for most users, supports Docker, Singularity, and Apptainer:

```bash
# Install Nextflow
curl -s https://get.nextflow.io | bash

# Run InterProScan6
nextflow run ebi-pf-team/interproscan6 \
  -profile docker,local \
  --input proteins.faa \
  --datadir /path/to/interpro_data
```

### Traditional Installation

```bash
# Download from EBI FTP
wget ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/5.XX-XX.X/interproscan-5.XX-XX.X-64-bit.tar.gz

# Extract
tar -pxvzf interproscan-5.XX-XX.X-64-bit.tar.gz

# Index HMM models
cd interproscan-5.XX-XX.X
python3 setup.py -f interproscan.properties
```

### Conda/Bioconda

```bash
conda install -c bioconda interproscan
```

### One-time initialization after install

Some packaged InterProScan installs still require the bundled HMM databases to
be pressed/indexed before real runs succeed.

```bash
cd /path/to/InterProScan
python3 setup.py -f interproscan.properties
```

If `hmmscan` reports missing binary auxfiles or tells you to run `hmmpress`
first, run this setup step before retrying.

## Key Command-Line Options

### Basic Options
- `-i, --input` - Input FASTA file (required)
- `-b, --output-file-base` - Output file base name
- `-o, --outfile` - Explicit output filename
- `-f, --formats` - Output formats (TSV, XML, JSON, GFF3)
- `-d, --output-dir` - Output directory
- `-cpu` - Number of CPU cores to use

### Application Selection
- `-appl, --applications` - Specific analyses to run (comma-separated)
  - Available: Pfam, PRINTS, ProSiteProfiles, SMART, HAMAP, PIRSF, SUPERFAMILY, Gene3D, Phobius, TMHMM, SignalP, Coils, MobiDBLite, PANTHER, ProSitePatterns, CDD

### Advanced Options
- `-goterms` - Include Gene Ontology terms in output
- `-pathways` - Include pathway annotations
- `-iprlookup` - Enable InterPro lookup (map to InterPro entries)
- `-pa` - Enable precalculated match lookup (faster, requires network)
- `-dp` - Disable precalculated match lookup
- `-t` - Sequence type (p=protein, n=nucleotide)
- `-seqtype` - Explicit sequence type
- `-ms` - Minimum sequence length (default: 15)

### Output Control
- `-T, --tempdir` - Temporary directory location
- `-dra` - Disable residue-level annotation
- `-verbose` - Verbose logging
- `-version` - Print version and exit

## Operational Pitfalls That Commonly Break Runs

### 1. `-b`, `-o`, and `-d` are mutually exclusive

Use exactly one of these output modes:

- `-b /path/to/output_base`
- `-d /path/to/output_dir`
- `-o /path/to/output.tsv` with a single `-f` format

Do not combine them.

Correct:

```bash
./interproscan.sh -i proteins.faa -b results/interpro_run -f TSV
```

Also correct:

```bash
./interproscan.sh -i proteins.faa -d results/interpro_dir -f TSV
```

Incorrect:

```bash
./interproscan.sh -i proteins.faa -b interpro_run -d results -f TSV
```

### 2. Protein FASTA files must not contain `*`

InterProScan rejects protein sequences containing stop-symbol asterisks.

Check first:

```bash
rg -n '\\*' proteins.faa
```

Strip them deliberately if they are expected ORF stop symbols:

```bash
python - <<'PY'
from pathlib import Path
inp = Path("proteins.faa")
out = Path("proteins.no_stop.faa")
with inp.open() as fh, out.open("w") as oh:
    for line in fh:
        if line.startswith(">"):
            oh.write(line)
        else:
            oh.write(line.replace("*", ""))
PY
```

Then run InterProScan on `proteins.no_stop.faa`.

### 3. Packaged installs may need helper binaries on `PATH`

Some packaged installs ship ProSite helpers in a bundled subdirectory while the
default `interproscan.properties` still references bare executable names such as
`ps_scan.pl`, `pfscan`, and `pfsearch`.

Validate resolution before large runs:

```bash
command -v ps_scan.pl
command -v pfscan
command -v pfsearch
```

If needed, prepend the bundled directory:

```bash
export INTERPROSCAN_HOME=/path/to/InterProScan
export PATH="${INTERPROSCAN_HOME}/bin/prosite:${PATH}"
```

If a packaged install still fails on helper binaries after this, prefer fixing
the environment first and rerunning the smoke test rather than launching the
full cluster job blind.

### 4. Validate the exact installation with a tiny smoke test

Before launching a large cluster run, execute a login-node smoke test on 1-2
proteins with the exact CLI you plan to submit:

```bash
./interproscan.sh \
  -i smoke_input.faa \
  -b smoke_run \
  -f TSV \
  -cpu 1 \
  -dp \
  -iprlookup \
  -goterms \
  -pa \
  -T ./tmp
```

Only submit the large job after the smoke test reaches completion and writes the
expected TSV output.

## Common Usage Examples

### Basic protein annotation
```bash
./interproscan.sh -i proteins.faa -b results -f TSV
```

### With GO terms and pathways
```bash
./interproscan.sh -i proteins.faa -b results \
  -f TSV,GFF3 -goterms -iprlookup -pathways
```

### Run specific analyses only
```bash
# Pfam and Gene3D only
./interproscan.sh -i proteins.faa -b results \
  -appl Pfam,Gene3D -f TSV
```

### Multiple output formats
```bash
./interproscan.sh -i proteins.faa -b results \
  -f TSV,XML,JSON,GFF3 -goterms -iprlookup
```

### With increased CPU usage
```bash
./interproscan.sh -i proteins.faa -b results \
  -f TSV -cpu 32 -goterms -iprlookup
```

### Using precalculated matches
```bash
# Faster execution using EBI's precalculated matches
./interproscan.sh -i proteins.faa -b results \
  -f TSV -pa -goterms -iprlookup
```

### InterProScan 6 with Nextflow
```bash
nextflow run ebi-pf-team/interproscan6 \
  -profile docker,slurm \
  --input proteins.faa \
  --datadir /data/interpro \
  --outdir results \
  --formats TSV,GFF3 \
  --goterms \
  --pathways
```

## Available Analyses

### Core Databases
- **Pfam**: Protein families based on HMMs
- **PRINTS**: Fingerprints - groups of conserved motifs
- **ProSiteProfiles**: Protein domain profiles
- **ProSitePatterns**: Protein domain patterns
- **SMART**: Simple Modular Architecture Research Tool
- **PANTHER**: Protein family classification
- **Gene3D**: CATH-Gene3D structural domains
- **SUPERFAMILY**: SCOP structural domains
- **HAMAP**: High-quality Automated Annotation
- **PIRSF**: PIR SuperFamily classifications
- **CDD**: Conserved Domain Database

### Specialized Analyses
- **SignalP**: Signal peptide prediction
- **TMHMM**: Transmembrane helix prediction
- **Phobius**: Combined signal peptide and transmembrane prediction
- **Coils**: Coiled-coil regions
- **MobiDBLite**: Protein disorder prediction

## Output Formats

### TSV (Tab-Separated Values)
Most common format, contains:
1. Protein accession
2. Sequence MD5 digest
3. Sequence length
4. Analysis
5. Signature accession
6. Signature description
7. Start location
8. Stop location
9. Score
10. Status
11. Date
12. InterPro accession
13. InterPro description
14. GO terms (if requested)
15. Pathways (if requested)

### GFF3 (Generic Feature Format)
Suitable for genome browsers and downstream tools.

### XML
Structured format for programmatic parsing.

### JSON
Machine-readable structured format.

## Input Requirements

### FASTA Format
```
>sequence_id1 optional description
MKTIIALSYIFCLVFADYKDDDDKSEQUENCE...
>sequence_id2
MALWMRLLPLLALLALWGPDPAAAFVNQHLC...
```

### Requirements
- Minimum sequence length: 15 amino acids (configurable with `-ms`)
- Valid amino acid characters
- Unique sequence identifiers

## Performance Tips

1. **Enable precalculated matches**: Use `-pa` for faster results on known sequences
2. **Use appropriate CPU count**: Set `-cpu` to available cores (don't exceed physical cores)
3. **Select specific analyses**: Use `-appl` to run only needed databases
4. **Use SSD for temp directory**: Set `-T` to fast storage location
5. **Split large files**: Process large datasets in batches
6. **Use InterProScan 6**: Nextflow-based version handles parallelization better
7. **Disable unnecessary features**: Skip `-goterms` or `-pathways` if not needed
8. **Local data directory**: Keep InterPro data on local fast storage

## Workflow Integration

### Complete annotation pipeline
```bash
# Run InterProScan with all annotations
./interproscan.sh -i proteins.faa -b interpro_results \
  -f TSV,GFF3 -goterms -iprlookup -pathways \
  -cpu 64 -T /scratch/tmp
```

### Parse TSV output
```bash
# Extract Pfam domains
grep "Pfam" interpro_results.tsv > pfam_domains.tsv

# Extract GO terms (column 14)
cut -f1,14 interpro_results.tsv | grep -v "^$" > go_annotations.tsv
```

### Convert to different formats
```bash
# Re-run with different output format (uses cached results)
./interproscan.sh -i proteins.faa -b results_json \
  -f JSON -goterms -iprlookup
```

## Interpreting Results

### Understanding E-values and Scores
- Lower E-values indicate more significant matches
- Different analyses use different scoring systems
- Check signature-specific documentation for score interpretation

### InterPro Entries
- InterPro entries integrate multiple signatures
- Single InterPro entry may contain multiple database signatures
- Use `-iprlookup` to map signatures to InterPro entries

### GO Terms
- Three ontologies: Molecular Function (F), Biological Process (P), Cellular Component (C)
- Format: GO:XXXXXXX|term name|ontology
- Multiple GO terms separated by pipe (|)

## Troubleshooting

### Out of memory errors
```bash
# Increase Java heap space in interproscan.properties
-Xmx4000m  # Change to higher value like -Xmx16000m
```

### Slow performance
```bash
# Use precalculated matches
./interproscan.sh -i proteins.faa -b results -pa

# Or select specific fast analyses
./interproscan.sh -i proteins.faa -b results -appl Pfam,Gene3D
```

### Temporary file issues
```bash
# Specify temp directory with more space
./interproscan.sh -i proteins.faa -b results -T /path/to/large/tmp
```

### Check installation
```bash
./interproscan.sh --version
./interproscan.sh --help
```

## Configuration

### interproscan.properties
Key settings:
- `number.of.embedded.workers` - Parallel workers
- `maxnumber.of.embedded.workers` - Maximum workers
- `precalculated.match.lookup.service.url` - Precalculated match service

### Environment Variables
- `JAVA_OPTS` - Java options (e.g., `-Xmx16G`)
- `TMPDIR` - Temporary directory

## Best Practices for Annotation Workflows

1. **Always include GO terms and pathways**: Use `-goterms -iprlookup -pathways`
2. **Use TSV and GFF3 formats**: TSV for analysis, GFF3 for visualization
3. **Enable precalculated matches**: Saves compute time for known sequences
4. **Monitor resource usage**: InterProScan can be memory-intensive
5. **Keep data updated**: Regularly update InterPro databases
6. **Validate input**: Check FASTA format before processing
7. **Archive results**: Save all output formats for future reference

## Version Information

This documentation is based on InterProScan v5-6 and reflects features available as of January 2026. Check the official documentation for version-specific details.
