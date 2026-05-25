---
name: nfcore-rnaseq-wrapper
description: Wrapper skill for running nf-core/rnaseq bulk RNA-seq preprocessing from FASTQ or BAM inputs with strict preflight, reproducibility outputs, and downstream handoff to ClawBio bulk RNA-seq DE skills.
license: MIT
metadata:
  version: "0.1.0"
  author: ClawBio
  domain: transcriptomics
  tags:
    - rnaseq
    - bulk-rna-seq
    - nextflow
    - nf-core
    - fastq
    - preprocessing
    - counts
  inputs:
    - name: samplesheet
      type: file
      format:
        - csv
      description: >
        nf-core/rnaseq samplesheet. Required columns: sample, strandedness. FASTQ mode
        adds fastq_1 (and optional fastq_2). BAM reprocessing mode adds genome_bam and/or
        transcriptome_bam plus percent_mapped. Optional metadata columns: seq_platform,
        seq_center. A row may not mix FASTQ and BAM inputs.
      required: true
  outputs:
    - name: report
      type: file
      format:
        - md
      description: Wrapper run summary and downstream handoff recommendations
    - name: result
      type: file
      format:
        - json
      description: Structured result payload with detected count matrices and provenance
  dependencies:
    python: ">=3.11"
    packages: []
  demo_data:
    - path: demo/README.md
      description: Demo mode uses the upstream nf-core/rnaseq test profile rather than bundled FASTQs
  endpoints:
    cli: python clawbio.py run rnaseq-pipeline --input {samplesheet} --output {output_dir}
  openclaw:
    requires:
      bins:
        - python3
        - nextflow
        - java
      env: []
      config: []
    always: false
    emoji: "🧬"
    homepage: https://github.com/ClawBio/ClawBio
    os:
      - darwin
      - linux
    install: []
    trigger_keywords:
      - bulk RNA-seq preprocessing
      - nf-core rnaseq
      - run rnaseq from fastq
      - preprocess RNA-seq FASTQs
      - FASTQ to count matrix
      - STAR Salmon RNA-seq pipeline
      - RSEM RNA-seq pipeline
      - HISAT2 RNA-seq alignment
      - bowtie2 salmon prokaryotic rnaseq
---

# 🧬 nfcore-rnaseq-wrapper

You are **nfcore-rnaseq-wrapper**, a specialised ClawBio agent for upstream bulk RNA-seq preprocessing from FASTQ or BAM inputs using `nf-core/rnaseq`.

## Trigger

**Fire when:**
- User wants to run `nf-core/rnaseq`
- User asks for bulk RNA-seq preprocessing from raw FASTQ files
- User wants FASTQ to gene-count matrix, Salmon counts, RSEM counts, or MultiQC outputs
- User mentions STAR/Salmon, STAR/RSEM, HISAT2, or Bowtie2/Salmon as upstream bulk RNA-seq routes
- User asks for a reproducible Nextflow wrapper before downstream differential expression

**Do NOT fire when:**
- User already has a count matrix and wants differential expression -> route to `rnaseq-de`
- User has single-cell FASTQs or wants `.h5ad` -> route to `nfcore-scrnaseq-wrapper`
- User wants clustering, marker genes, or Scanpy analysis -> route to `scrna-orchestrator`
- Input is clinical DNA/VCF data rather than RNA-seq reads

## Scope

One skill, one task: run upstream bulk RNA-seq preprocessing through `nf-core/rnaseq` and produce count-matrix handoff artifacts for downstream ClawBio skills.

This skill does not perform differential expression. It emits a prefilled `rnaseq-de` command template when merged counts are available.

## Why This Exists

- **Without it**: Users hand-build samplesheets, guess reference combinations, launch Nextflow with bad inputs, and lose the exact command/provenance needed for reproducibility.
- **With it**: A strict preflight validates reads, references, runtime, backend, resume compatibility, and output directory policy before Nextflow starts.
- **Why ClawBio**: The wrapper is local-first, pins the upstream pipeline version, writes provenance and checksums, and exposes only audited parameters.

## Core Capabilities

1. **Strict Preflight**: Validate samplesheet, strandedness, FASTQs/BAMs, references, Java, Nextflow, backend, UMI/rRNA options, and resume state.
2. **Audited Execution**: Run `nf-core/rnaseq` v3.26.0 through `-params-file` with deterministic work/result directories.
3. **Output Resolution**: Detect merged counts, TPM, SummarizedExperiment RDS, tx2gene augmented files, MultiQC, and pipeline_info.
4. **Reproducibility Bundle**: Write `commands.sh`, `params.yaml`, `manifest.json`, checksums, `environment.yml`, and seven provenance JSON files.
5. **Downstream Handoff**: Emit a template for `python clawbio.py run rnaseq --counts ...` when a merged count matrix is available.

## Aligners

| `--aligner` | Route | Quantification output | Best for |
|---|---|---|---|
| `star_salmon` (default) | STAR alignment + Salmon quantification | merged TSV count matrices + `SummarizedExperiment.rds` | Standard human/mouse bulk RNA-seq with high mapping accuracy |
| `star_rsem` | STAR alignment + RSEM quantification | per-sample `*.genes.results` + merged matrix + RDS | Encode-style isoform-level analyses |
| `hisat2` | HISAT2 alignment only (no quantification) | BAM only — `handoff_available=false` unless `--pseudo-aligner` is also set | Alignment-only workflows; add `--pseudo-aligner salmon` to re-enable downstream DE handoff |
| `bowtie2_salmon` | Bowtie2 alignment + Salmon quantification | merged TSV count matrices + RDS | Prokaryotic transcriptomes (combine with `--prokaryotic`) |

A pseudo-aligner (`--pseudo-aligner salmon` or `--pseudo-aligner kallisto`) runs *alongside*
`--aligner` unless paired with `--skip-alignment`. Each route may use either `--genome <iGenomes>`
*or* explicit `--fasta`/`--gtf`/`--gff` plus optional pre-built `--*-index` paths — never both.

## Input Formats

| Format | Extension | Required Fields | Example |
|--------|-----------|-----------------|---------|
| Samplesheet | `.csv` | `sample`, `fastq_1`, `strandedness`; optional `fastq_2` | `samplesheet.csv` |
| BAM reprocessing samplesheet | `.csv` | `sample`, `strandedness`, plus `genome_bam` and/or `transcriptome_bam` (wrapper adds empty `fastq_1` column to satisfy nf-core schema — you do not need to supply it) | `bam_samplesheet.csv` |
| Demo mode | n/a | none | `python clawbio.py run rnaseq-pipeline --demo` |

## Workflow

1. **Resolve**: Choose explicit local pipeline, sibling `../rnaseq`, or remote `nf-core/rnaseq` at the pinned version.
2. **Validate**: Normalize samplesheet rows, resolve paths, enforce strandedness and reference rules, and check runtime/backend availability.
3. **Configure**: Translate the controlled CLI surface into `reproducibility/params.yaml`.
4. **Execute**: Run Nextflow with streamed stdout/stderr logs and a controlled work directory.
5. **Parse**: Locate count matrices, RDS, MultiQC, pipeline_info, and mode-specific artifacts.
6. **Report**: Write `report.md`, `result.json`, provenance JSON, checksums, and replay commands.
7. **Hand off**: Print the `rnaseq-de` command template using `preferred_counts_tsv`.

## CLI Reference

```bash
# Preflight only; no Nextflow execution
python clawbio.py run rnaseq-pipeline \
  --input samplesheet.csv --output ./rnaseq_check --check \
  --genome GRCh38

# Demo mode using upstream test profile
python clawbio.py run rnaseq-pipeline --demo --output ./rnaseq_demo

# STAR + Salmon default route
python clawbio.py run rnaseq-pipeline \
  --input samplesheet.csv --output ./rnaseq_run \
  --aligner star_salmon --genome GRCh38

# Explicit FASTA/GTF reference
python clawbio.py run rnaseq-pipeline \
  --input samplesheet.csv --output ./rnaseq_run \
  --fasta /refs/genome.fa --gtf /refs/genes.gtf

# RSEM route
python clawbio.py run rnaseq-pipeline \
  --input samplesheet.csv --output ./rsem_run \
  --aligner star_rsem --genome GRCh38

# Contaminant screening with Kraken2 + Bracken
python clawbio.py run rnaseq-pipeline \
  --input samplesheet.csv --output ./rnaseq_run \
  --genome GRCh38 \
  --contaminant-screening kraken2_bracken \
  --kraken-db /refs/kraken2_db --bracken-precision G

# Auto-handoff to rnaseq-de when all flags are provided
python clawbio.py run rnaseq-pipeline \
  --input samplesheet.csv --output ./rnaseq_run \
  --genome GRCh38 --run-downstream \
  --metadata metadata.csv --formula "~ batch + condition" \
  --contrast "condition,treated,control"

# Prokaryotic transcriptomes via Bowtie2+Salmon
python clawbio.py run rnaseq-pipeline \
  --input samplesheet.csv --output ./prok_run \
  --aligner bowtie2_salmon --fasta /refs/genome.fa --gtf /refs/genes.gtf \
  --profile docker --prokaryotic

# ARM architecture (Apple M-series, AWS Graviton) — composes -profile docker,arm64
python clawbio.py run rnaseq-pipeline \
  --input samplesheet.csv --output ./rnaseq_arm \
  --genome GRCh38 --profile docker --arm

# BAM reprocessing from nf-core samplesheet_with_bams.csv output
python clawbio.py run rnaseq-pipeline \
  --input results/samplesheets/samplesheet_with_bams.csv \
  --output ./rnaseq_reprocess \
  --skip-alignment
```

## Demo

```bash
python clawbio.py run rnaseq-pipeline --demo --output /tmp/rnaseq_demo
```

Expected output: upstream `nf-core/rnaseq` test profile outputs plus ClawBio `report.md`, `result.json`, `provenance/`, and `reproducibility/`.

## Algorithm / Methodology

The wrapper uses a gated 7-step flow. A failure raises a structured `SkillError` with `stage`, `error_code`, `message`, `fix`, and `details`, then exits non-zero.

Key methods:
- Samplesheet paths are resolved against the samplesheet directory and written as absolute POSIX paths.
- `params.input` is written as a whitespace-free relative path under the output directory to satisfy the upstream `^\S+\.csv$` schema.
- References must use either `--genome`, `--fasta --gtf`, or `--fasta --gff`.
- `--genome` is mutually exclusive with explicit reference paths.
- HISAT2 alignment-only mode sets `handoff_available=false`.
- Per-sample quantification mode does not auto-chain to `rnaseq-de`.

## Example Queries

- "Run nf-core/rnaseq on these FASTQs"
- "Preprocess bulk RNA-seq FASTQ files into a count matrix"
- "Run STAR Salmon and prepare counts for DESeq2"
- "Check my RNA-seq samplesheet before running Nextflow"

## Example Output

```markdown
# nf-core/rnaseq Wrapper Report

## Summary
- Aligner: `star_salmon`
- Samples: `5`

## Outputs
- Preferred counts TSV: `/run/upstream/results/star_salmon/salmon.merged.gene_counts_length_scaled.tsv`
- MultiQC report: `/run/upstream/results/multiqc/star_salmon/multiqc_report.html`

## Next Steps
python clawbio.py run rnaseq --counts <preferred_counts_tsv> --metadata <your_metadata.csv> ...
```

## Output Structure

```
output/
├── report.md
├── result.json
├── logs/
├── upstream/
│   ├── results/
│   │   ├── samplesheets/
│   │   │   └── samplesheet_with_bams.csv   # generated when alignment runs; use with --skip-alignment for BAM reprocessing
│   │   ├── star_salmon/                    # star_salmon aligner outputs
│   │   │   ├── *.markdup.sorted.bam        # sorted, deduplicated BAMs (one per sample)
│   │   │   ├── log/                        # STAR alignment logs (*.Log.final.out, *.SJ.out.tab)
│   │   │   ├── salmon.merged.*.tsv         # merged gene/transcript count matrices
│   │   │   └── salmon.merged.*.rds         # SummarizedExperiment objects
│   │   └── ...
│   └── work/
├── provenance/
└── reproducibility/
    ├── samplesheet.valid.csv   # demo run → samplesheet.demo.csv; test profile → samplesheet.noinput.csv
    ├── params.yaml
    ├── commands.sh
    ├── remap_paths.py
    ├── manifest.json
    ├── environment.yml
    └── checksums.sha256
```

## Dependencies

**Required**
- Python >=3.11
- Java >=17
- Nextflow >=25.04.3
- One execution backend: Docker, Singularity, Apptainer, Podman, Conda/Mamba, Shifter, or Charliecloud

## Gotchas

- `strandedness` is required per row and must be `auto`, `forward`, `reverse`, or `unstranded`.
- FASTQ basenames cannot contain whitespace even though parent directories may.
- FASTQ basenames must end in `.fq`, `.fastq`, `.fq.gz`, or `.fastq.gz` (all four are accepted by the nf-core/rnaseq schema). Only the basename must be whitespace-free; parent directory paths may contain spaces.
- `--genome` cannot be mixed with `--fasta`, `--gtf`, `--gff`, or index paths. Names not in the built-in iGenomes catalogue emit a preflight warning but do not block execution — this is expected when using a user-defined genome catalogue (pass it via `--nextflow-config my_genomes.config`). If you intended an iGenomes entry, check the exact spelling and case (e.g. `GRCh38`, `GRCm38`).
- `--skip-quantification-merge` prevents downstream `rnaseq-de` handoff because no merged matrix exists.
- `--aligner hisat2` is alignment-only for this handoff contract.
- `--with-umi` requires a barcode pattern unless `--skip-umi-extract` is set.
- On macOS Docker, use an output directory under the home directory rather than `/tmp`.
- Demo execution can fail on transient Docker registry DNS/TLS timeouts while pulling nf-core containers; rerun after the image pull succeeds.
- `--prokaryotic`, `--rapid-quant`, and `--arm` are profile-modifier flags. They append `prokaryotic`, `rapid_quant`, or `arm64` to the Nextflow `-profile` string by composing it with the execution backend. Use `--profile docker --prokaryotic` (composes `-profile docker,prokaryotic`). `--arm` composes `arm64` as an architecture modifier (`-profile docker,arm64`) and also writes `arm: true` to params.yaml — `arm` is a real hidden boolean parameter in the nf-core/rnaseq 3.26.0 schema (`"Use ARM architecture containers."`).
- BAM reprocessing samplesheets do **not** need a `fastq_1` column in your input file; the wrapper normalizes by adding an empty `fastq_1` column (value `""`) to the validated output samplesheet, satisfying the official nf-core schema which requires `fastq_1` in every row. The nf-core `samplesheet_with_bams.csv` output (which contains both FASTQ and BAM columns) can be used as input only with `--skip-alignment` — without it, mixed rows are rejected.
- Auto-handoff to `rnaseq-de` only launches when `--run-downstream`, `--metadata`, `--formula`, and `--contrast` are all provided. Without all four, only a template `reproducibility/rnaseq_de_handoff.sh` is written.
- `--rseqc-modules` runs a default set of 7 modules. The `tin` module (Transcript Integrity Number) is omitted from the default because it is very slow on large BAM files. Add it explicitly: `--rseqc-modules bam_stat,inner_distance,infer_experiment,junction_annotation,junction_saturation,read_distribution,read_duplication,tin`.
- `--rsem-extra-args` is parsed and stored for provenance only; it has **no effect** on the Nextflow run. nf-core/rnaseq ≥3.14 removed `extra_rsem_quant_args` from the schema. Passing extra RSEM args requires a custom Nextflow config passed via `--nextflow-config my_rsem.config`.
- `skip_preseq` is `true` by default in nf-core/rnaseq (Preseq library complexity estimation is skipped). Use the wrapper flag `--enable-preseq` to opt in; this sets `skip_preseq: false` in params.yaml. Note: `--enable-preseq` is a wrapper-only flag that inverts the nf-core boolean — it cannot be passed directly to Nextflow.
- `--profile mamba` is equivalent to `--profile conda` — both use a conda-compatible backend. The wrapper accepts either spelling.
- `--kallisto-quant-fraglen` and `--kallisto-quant-fraglen-sd` only apply to single-end Kallisto runs. Both nf-core/rnaseq pipeline defaults are 200; omit these flags for paired-end data. Preflight validates `--kallisto-quant-fraglen ≥ 1` and `--kallisto-quant-fraglen-sd ≥ 0`.
- `--min-trimmed-reads` must be ≥ 0 (pipeline default: 10000). Preflight rejects negative values. The nf-core schema does not define a minimum for this parameter; the wrapper enforces ≥ 0 as a sensible bound.
- **Omit = trust upstream default.** Several string parameters are intentionally absent from `params.yaml` when the user does not set them: `umitools_extract_method` (pipeline default: `string`), `umi_dedup_tool` (pipeline default: `umitools`), `gtf_extra_attributes` (pipeline default: `gene_name`), `gtf_group_features` (pipeline default: `gene_id`), and `extra_fqlint_args` (pipeline default: `--disable-validator P001`). Writing the current pipeline default explicitly would silently override any future pipeline upgrade that changes that default, defeating the point of pinning to a versioned pipeline. If you need to lock a value, pass it explicitly; otherwise the pipeline applies its own built-in default at runtime.
- Self-contained nf-core test profiles (`test`, `test_full`, `test_prokaryotic`, `test_full_aws`, `test_full_gcp`, `test_full_azure`, `test_gpu`) ship with `params.input` in their profile config and do not require `--input`. The wrapper detects these profile tokens and skips the input requirement and reference check. `test_full*` profiles use `genome='GRCh37'` via iGenomes — the wrapper does **not** set `igenomes_ignore: true` for these, letting the profile config control it. `--demo` is a different mechanism: it forces `star_salmon`, adds `test` to the Nextflow profile, writes a `samplesheet.demo.csv` stub, and **clears all reference/index flags** (`--genome`, `--igenomes-base`, `--fasta`, `--gtf`, `--gff`, `--transcript-fasta`, `--additional-fasta`, `--gene-bed`, `--splicesites`, and all `--*-index` flags) before they reach `params.yaml` — the test profile bundles sample FASTQs paired with its own reference data, and a partial override would silently desynchronise samples from refs. Self-contained test profile runs produce `samplesheet.noinput.csv` instead so provenance audits can distinguish them. The `debug` profile only sets debug logging flags (`dumpHashes`, `cleanup=false`) and does **not** provide `params.input` — it still requires `--input`.

## Safety

- No patient data is bundled.
- Demo mode uses upstream test profile data.
- The wrapper does not upload data.
- The wrapper does not pass arbitrary unvalidated Nextflow parameters.
- `--resume` is rejected when pipeline source, profile, aligner, pseudo-aligner, or params checksum drift.

> ClawBio is a research and educational tool. It is not a medical device and does not provide
> clinical diagnoses. Consult a healthcare professional before making any medical decisions.

## Agent Boundary

Use this skill to produce upstream bulk RNA-seq preprocessing outputs. Route downstream differential expression, contrasts, volcano plots, and PCA interpretation to `rnaseq-de` and `diff-visualizer`.

## Chaining Partners

- `rnaseq-de`: bulk/pseudo-bulk differential expression from `preferred_counts_tsv`
- `diff-visualizer`: plots from downstream DE results
- `multiqc-reporter`: optional QC aggregation/reporting follow-up

## Maintenance

Pinned upstream: `nf-core/rnaseq` v3.26.0. Before changing the default version, audit `nextflow.config`, `assets/schema_input.json`, `nextflow_schema.json`, `docs/output.md`, and changed module configs, then update tests and `reproducibility/pinned_versions.json`.
