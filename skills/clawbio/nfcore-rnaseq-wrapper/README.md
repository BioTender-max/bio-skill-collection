# nfcore-rnaseq-wrapper

ClawBio wrapper for running `nf-core/rnaseq` bulk RNA-seq preprocessing from FASTQ/BAM inputs with strict preflight, reproducibility artifacts, provenance, and explicit handoff to downstream bulk RNA-seq DE skills.

## Scope

- Upstream bulk RNA-seq preprocessing via Nextflow.
- Supported aligners: `star_salmon`, `star_rsem`, `hisat2`, `bowtie2_salmon`.
- Validated samplesheet input with absolute normalized FASTQ/BAM paths.
- Reproducibility bundle, provenance bundle, `report.md`, and `result.json`.
- Canonical merged count matrix detection for downstream `rnaseq`.

## Out Of Scope

- Differential expression, contrasts, PCA, volcano plots, or interpretation.
- Automatic execution of `rnaseq-de` without the full flag set (`--run-downstream`, `--metadata`, `--formula`, `--contrast` are all required to trigger the handoff; otherwise only a replay template is written).
- Arbitrary free-form Nextflow passthrough flags (use `--nextflow-config` to supply custom config files).

## Quick Start

```bash
python clawbio.py run rnaseq-pipeline --demo --output ./outputs/rnaseq_demo
```

For real data:

```bash
python clawbio.py run rnaseq-pipeline \
  --input samplesheet.csv \
  --output ./rnaseq_run \
  --aligner star_salmon \
  --genome GRCh38
```

Use `--check` to run preflight without launching Nextflow.
