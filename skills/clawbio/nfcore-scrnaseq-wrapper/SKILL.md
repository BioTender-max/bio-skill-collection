---
name: nfcore-scrnaseq-wrapper
version: "0.1.0"
author: ClawBio
description: Wrapper skill for running nf-core/scrnaseq upstream single-cell RNA-seq preprocessing from FASTQ with strict preflight, reproducibility outputs, and downstream handoff to ClawBio scRNA skills.
inputs:
  - name: samplesheet
    type: file
    format: [csv]
    description: "nf-core/scrnaseq samplesheet CSV with required columns: sample, fastq_1, fastq_2"
    required: true
outputs:
  - name: report
    type: file
    format: [md]
    description: Wrapper run summary and downstream handoff recommendations
  - name: result
    type: file
    format: [json]
    description: Structured result payload with detected outputs and provenance
trigger_keywords:
  - scrnaseq
  - nf-core scrnaseq
  - run scrnaseq from fastq
  - preprocess 10x fastqs
  - generate h5ad from single-cell fastq
  - single-cell preprocessing
  - nextflow scrna pipeline
  - 10x chromium fastq pipeline
  - starsolo upstream processing
  - alevin-fry fastq to counts
  - run nextflow scrnaseq
  - upstream single-cell pipeline
  - fastq to h5ad single cell
  - 10x genomics fastq pipeline
license: MIT
metadata:
  domain: transcriptomics
  tags: [scrna, single-cell, nextflow, nf-core, fastq, 10x, h5ad, preprocessing]
  dependencies:
    python: ">=3.11"
    packages: []
  endpoints:
    cli: python skills/nfcore-scrnaseq-wrapper/nfcore_scrnaseq_wrapper.py --input {samplesheet} --output {output_dir}
  openclaw:
    requires:
      bins: [python3, nextflow, java]
    always: false
    emoji: "🧫"
    homepage: https://github.com/ClawBio/ClawBio
    os: [darwin, linux]
---

# nfcore-scrnaseq-wrapper

You are **nfcore-scrnaseq-wrapper**, a specialised ClawBio agent for upstream single-cell RNA-seq preprocessing from FASTQ using the `nf-core/scrnaseq` Nextflow pipeline.

## Trigger

**Fire when:**
- User wants to run `scrnaseq` from raw FASTQ files
- User asks to preprocess 10x Chromium single-cell data
- User wants to execute `nf-core/scrnaseq`
- User wants to generate `.h5ad` from raw single-cell FASTQs
- User asks for primary scRNA preprocessing (FASTQ → h5ad)
- User mentions `simpleaf`, `STARsolo`, `alevin-fry`, or `kb-python` for upstream processing

**Do NOT fire when:**
- User already has an `.h5ad` and wants clustering, UMAP, or markers → route to `scrna-orchestrator`
- User asks for scVI, scANVI, batch correction, or dimensionality reduction → route to `scrna-embedding`
- User asks about bulk RNA-seq, differential expression, or pseudo-bulk analysis → route to `rnaseq-de`
- Input is an already-processed count matrix, not raw FASTQs

## Scope

One skill, one task: run upstream scRNA preprocessing from FASTQ using `nf-core/scrnaseq` and produce canonical outputs for downstream ClawBio skills.

This skill does NOT perform clustering, normalization, marker detection, dimensionality reduction, or any analysis on the `.h5ad` it produces.

## Why This Exists

- **Without it**: Users hand-build samplesheets, guess reference combinations, miss backend issues, and struggle to locate the correct `.h5ad` for downstream analysis.
- **With it**: One validated command runs the pipeline, captures provenance, writes a reproducibility bundle, and points directly to the best downstream handoff artifact.
- **Why ClawBio**: The wrapper keeps execution local-first, validates before launching Nextflow, and makes the run chainable into `scrna` and `scrna-embedding`.

## Core Capabilities

1. **Strict Preflight**: Validate Java, Nextflow, backend, samplesheet, FASTQs, and references before execution.
2. **Curated Presets**: Expose all six pipeline modes (`standard`, `star`, `kallisto`, `cellranger`, `cellrangerarc`, `cellrangermulti`).
3. **Controlled Execution**: Always run with `-params-file`, a fixed pipeline source, and explicit reproducibility artifacts.
4. **Output Resolution**: Detect MultiQC, pipeline_info, `.h5ad`, `.rds`, and select a canonical `preferred_h5ad` when possible.
5. **Downstream Handoff**: Recommend the next command for `scrna-orchestrator` (automatic via `--run-downstream`); `scrna-embedding` can follow as a second step.

## Input Formats

| Format | Extension | Required columns | Optional columns |
|--------|-----------|------------------|------------------|
| Samplesheet | `.csv` | `sample`, `fastq_1`, `fastq_2` | `expected_cells`, `seq_center`, `sample_type`, `fastq_barcode`, `feature_type` |
| Demo mode | n/a | none — test profile provides its own data | — |

## Workflow

1. **Validate**: Check the selected preset, samplesheet structure, FASTQ accessibility, references, Java, Nextflow, and backend.
2. **Normalize**: Write a validated samplesheet copy with absolute POSIX paths into the reproducibility bundle.
3. **Configure**: Build one effective `params.yaml` and a fixed Nextflow command.
4. **Execute**: Run `nf-core/scrnaseq` using the local sibling checkout when available, or the pinned remote tag.
5. **Parse**: Detect MultiQC, pipeline_info, `.h5ad`, `.rds`, and CellBender-derived outputs.
6. **Generate**: Write `report.md`, `result.json`, provenance JSON files, and reproducibility artifacts.
7. **Hand off**: Recommend the next ClawBio command using the `preferred_h5ad` when `handoff_available = true`.

## Algorithm / Methodology

The wrapper executes a strictly ordered 7-step pipeline. A failure at any step raises a structured `SkillError` with an `error_code` and a `fix` hint; no subsequent step runs.

1. **Pipeline source resolution** (`pipeline_source.py`): Prefer a local sibling `scrnaseq/` checkout (pinned commit, audit-safe). Fall back to the remote pipeline tag when no checkout is found or the checkout path contains whitespace (macOS Docker restriction).

2. **Samplesheet validation** (`samplesheet_builder.py`): Parse the CSV, resolve FASTQ paths relative to the CSV parent directory, normalize sample-name whitespace to underscores, verify readability and FASTQ extensions, reject FASTQ basenames with whitespace, enforce consistent `expected_cells` (≥1) and `seq_center` for repeated sample rows, reject exact duplicate FASTQ rows, and write a normalized copy with absolute POSIX paths to `reproducibility/samplesheet.valid.csv`.

3. **Preflight** (`preflight.py`): Verify Java (≥17) and Nextflow (≥25.04.0). Compare version tuples after zero-padding to 3 elements (avoids false negatives such as `(24, 4) < (24, 4, 0)`). For `docker`, run `docker info` and gate on exit code. For `conda`/`mamba`, locate the binary. For `singularity`/`apptainer`, accept either binary interchangeably. For `wave` and `gpu`, no binary check is needed (Nextflow-native features). All subprocess calls have a 30-second timeout.

4. **Params construction** (`params_builder.py`): Translate the preset + CLI flags into a `params.yaml` consumed by Nextflow via `-params-file`. All file paths use `.as_posix()` for forward-slash consistency across platforms. `igenomes_ignore` is automatically set to `true` whenever any explicit reference path is provided (suppresses nf-schema DNS validation of the default iGenomes S3 URL). Skip flags are only written when `true`, keeping `params.yaml` minimal.

5. **Command build + execution** (`command_builder.py`, `executor.py`): Construct the `nextflow run` command with `-params-file` and `-work-dir <output>/upstream/work`, then launch via `subprocess.Popen` with stdout and stderr piped to log files on disk — never buffered in RAM. On `TimeoutExpired`, the process is killed and `EXECUTION_FAILED` is raised.

6. **Output parsing** (`outputs_parser.py`): Scan the upstream results tree for MultiQC HTML, `pipeline_info/`, `.h5ad` (combined matrix preferred over per-sample, filtered preferred over raw), `.rds`, and CellBender-derived files. `handoff_available` is set to `true` only when a `preferred_h5ad` is confirmed on disk.

7. **Provenance + reporting** (`provenance.py`, `reporting.py`): Write JSON provenance bundles, a SHA-256 checksum manifest (files only — never directories), `environment.yml`, a portable `commands.sh`, `report.md`, and `result.json`.

## Presets

| Preset | Aligner | Use case |
|--------|---------|---------|
| `standard` | simpleaf (alevin-fry) | Default for 10x GEX; fast, memory-efficient |
| `star` | STARsolo | Best FASTQ QC metrics; supports RNA velocity (`--star-feature "Gene Velocyto"`) |
| `kallisto` | kb-python / BUStools | Pseudo-alignment; fastest; lamanno/nac RNA velocity via `--kb-workflow` |
| `cellranger` | CellRanger | CellRanger v2/v3 compatibility; requires CellRanger binary in PATH |
| `cellrangerarc` | CellRanger ARC | Multiome (GEX + ATAC); accepts prebuilt `--cellranger-index` or reference-build inputs |
| `cellrangermulti` | CellRanger Multi | GEX + VDJ + feature barcoding; `--cellranger-multi-barcodes` required for CMO/FFPE multiplexing |

Each preset requires at least one reference option: `--genome <iGenomes_shortcut>` OR a pre-built index (`--star-index`, `--simpleaf-index`, etc.) OR `--fasta` + `--gtf`.

## CLI Reference

```bash
# Standard usage
python skills/nfcore-scrnaseq-wrapper/nfcore_scrnaseq_wrapper.py \
  --input samplesheet.csv --output ./scrnaseq_run

# Preflight check only (no Nextflow execution)
python skills/nfcore-scrnaseq-wrapper/nfcore_scrnaseq_wrapper.py \
  --input samplesheet.csv --output ./scrnaseq_run --check

# Demo mode (runs the upstream nf-core test profile; forces star preset; Docker must be running)
python skills/nfcore-scrnaseq-wrapper/nfcore_scrnaseq_wrapper.py \
  --demo --output ./scrnaseq_demo

# Via ClawBio runner
python clawbio.py run scrnaseq-pipeline --input samplesheet.csv --output ./scrnaseq_run
python clawbio.py run scrnaseq-pipeline --demo --output ./scrnaseq_demo

# STARsolo with local FASTA+GTF (STAR index built by the pipeline)
python skills/nfcore-scrnaseq-wrapper/nfcore_scrnaseq_wrapper.py \
  --input samplesheet.csv --output ./run --preset star --protocol 10XV3 \
  --fasta /refs/hg38.fa --gtf /refs/hg38.gtf

# STARsolo with prebuilt STAR index
python skills/nfcore-scrnaseq-wrapper/nfcore_scrnaseq_wrapper.py \
  --input samplesheet.csv --output ./run --preset star --protocol 10XV3 \
  --star-index /refs/star_index

# STARsolo RNA velocity
python skills/nfcore-scrnaseq-wrapper/nfcore_scrnaseq_wrapper.py \
  --input samplesheet.csv --output ./run --preset star \
  --star-feature "Gene Velocyto" --star-ignore-sjdbgtf \
  --fasta /refs/hg38.fa --gtf /refs/hg38.gtf

# Simpleaf (standard) with UMI resolution override
python skills/nfcore-scrnaseq-wrapper/nfcore_scrnaseq_wrapper.py \
  --input samplesheet.csv --output ./run --preset standard --protocol 10XV3 \
  --simpleaf-umi-resolution cr-like-em --genome GRCh38

# Kallisto RNA velocity (NAC workflow)
python skills/nfcore-scrnaseq-wrapper/nfcore_scrnaseq_wrapper.py \
  --input samplesheet.csv --output ./run --preset kallisto \
  --kb-workflow nac --fasta /refs/hg38.fa --gtf /refs/hg38.gtf

# Air-gapped cluster: local iGenomes mirror
python skills/nfcore-scrnaseq-wrapper/nfcore_scrnaseq_wrapper.py \
  --input samplesheet.csv --output ./run --preset star --protocol 10XV3 \
  --genome GRCh38 --igenomes-base /mnt/local_igenomes

# CellRanger Multi (CMO multiplexing)
python skills/nfcore-scrnaseq-wrapper/nfcore_scrnaseq_wrapper.py \
  --input samplesheet.csv --output ./run --preset cellrangermulti \
  --cellranger-index /refs/refdata-gex-GRCh38 \
  --gex-cmo-set /refs/cmo_set.csv \
  --cellranger-multi-barcodes /refs/multi_barcodes.csv
```

### Key flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--preset` | string | `standard` | Aligner preset |
| `--profile` | string | `docker` | Execution backend: `docker`, `conda`, `mamba`, `singularity`, `apptainer`, `podman`, `shifter`, `charliecloud`, `wave`, `gpu` |
| `--pipeline-version` | string | `4.1.0` | Remote `nf-core/scrnaseq` tag or commit (used when no local sibling checkout is found) |
| `--protocol` | string | `None` | Chemistry/protocol forwarded to the aligner. Required and non-`auto` for `standard`, `star`, and `kallisto`. `standard`/simpleaf additionally rejects `smartseq`. For `cellranger`, `cellrangerarc`, and `cellrangermulti` any value is accepted — `auto` is the typical upstream recommendation |
| `--genome` | string | — | iGenomes shortcut (`GRCh38`, `mm10`, etc.) — mutually exclusive with `--fasta`/`--gtf` and all index flags |
| `--igenomes-base` | string | — | Base URL or local path for iGenomes (default `s3://ngi-igenomes/igenomes/`). Use for local mirrors or air-gapped clusters |
| `--fasta` | path | — | Genome FASTA (`.fa`, `.fna`, `.fasta`, `.gz` variants; no whitespace in path) |
| `--gtf` | path | — | Gene annotation GTF |
| `--star-index` | path | — | Prebuilt STAR genome index directory |
| `--simpleaf-index` | path | — | Prebuilt simpleaf/alevin-fry index |
| `--kallisto-index` | path | — | Prebuilt kallisto index |
| `--cellranger-index` | path | — | Prebuilt CellRanger or CellRanger ARC reference |
| `--transcript-fasta` | path | — | Transcriptome FASTA for simpleaf |
| `--txp2gene` | path | — | Transcript-to-gene mapping for simpleaf |
| `--barcode-whitelist` | path | — | Custom barcode whitelist (per-aligner format) |
| `--star-feature` | enum | — | STARsolo feature type: `Gene`, `GeneFull`, `Gene Velocyto` |
| `--star-ignore-sjdbgtf` | flag | — | Do not use GTF for SJDB construction (required for `Gene Velocyto`) |
| `--seq-center` | string | — | Sequencing center name for BAM read group tag |
| `--simpleaf-umi-resolution` | enum | — | UMI resolution strategy for alevin-fry: `cr-like`, `cr-like-em`, `parsimony`, `parsimony-em`, `parsimony-gene`, `parsimony-gene-em` |
| `--kb-workflow` | enum | — | Kallisto workflow: `standard`, `lamanno`, `nac` |
| `--kb-t1c` | path | — | cDNA transcripts-to-capture file for RNA velocity (lamanno/nac) |
| `--kb-t2c` | path | — | Intron transcripts-to-capture file for RNA velocity (lamanno/nac) |
| `--skip-cellbender` | flag | — | Disable the CellBender ambient RNA removal subworkflow |
| `--skip-emptydrops` | flag | — | Skip emptyDrops cell calling (independent of `--skip-cellbender`) |
| `--skip-fastqc` | flag | — | Skip FastQC quality control |
| `--skip-multiqc` | flag | — | Skip MultiQC report generation |
| `--skip-cellranger-renaming` | flag | — | Skip automatic sample renaming in CellRanger modules |
| `--skip-cellrangermulti-vdjref` | flag | — | Skip mkvdjref in cellrangermulti (when VDJ data is absent or a prebuilt `--cellranger-vdj-index` is supplied) |
| `--save-reference` | flag | — | Save the built reference index for future reuse |
| `--save-align-intermeds` | flag | — | Save alignment intermediate BAM files (disabled by default) |
| `--expected-cells` | int | — | Override expected cell count (≥1) for all samples |
| `--email` | string | — | Email address for pipeline completion notification |
| `--multiqc-title` | string | — | Custom title for the MultiQC report |
| `--resume` | flag | — | Nextflow resume (checksum-verified against prior manifest) |
| `--run-downstream` | flag | — | Opt in to `scrna_orchestrator` handoff after pipeline completion |
| `--cellrangerarc-config` | path | — | Config JSON for CellRanger ARC index construction |
| `--cellrangerarc-reference` | string | — | Reference genome name used inside the CellRanger ARC config |
| `--motifs` | path | — | Motif file (e.g. JASPAR) for CellRanger ARC |
| `--cellranger-vdj-index` | path | — | Prebuilt CellRanger VDJ reference |
| `--gex-frna-probe-set` | path | — | Probe set CSV for FFPE fixed RNA profiling (`cellrangermulti`) |
| `--gex-target-panel` | path | — | Target panel CSV for targeted GEX (`cellrangermulti`) |
| `--gex-cmo-set` | path | — | CMO reference CSV for multiplexed samples (`cellrangermulti`) |
| `--gex-barcode-sample-assignment` | path | — | Barcode-to-sample assignment CSV for OCM multiplexing (`cellrangermulti`) |
| `--fb-reference` | path | — | Feature-barcode reference CSV for antibody capture (`cellrangermulti`) |
| `--vdj-inner-enrichment-primers` | path | — | V(D)J cDNA enrichment primer sequences (`cellrangermulti`) |
| `--cellranger-multi-barcodes` | path | — | Multiplexed sample samplesheet for CMO/FFPE demultiplexing (`cellrangermulti`) |

## Output Structure

```text
output_directory/
├── report.md                         # Wrapper run summary
├── result.json                       # Structured result payload
├── logs/
│   ├── stdout.txt                    # Nextflow stdout
│   └── stderr.txt                    # Nextflow stderr
├── upstream/
│   └── results/                      # nf-core/scrnaseq output tree
│       ├── fastqc/                   # Per-read FastQC reports
│       ├── multiqc/                  # MultiQC HTML and data
│       │   └── multiqc_report.html
│       ├── pipeline_info/            # Execution report, timeline, trace, DAG
│       └── <aligner>/                # Aligner-specific outputs
│           ├── <sample>/             # Per-sample STAR/simpleaf/kallisto outputs
│           └── mtx_conversions/      # AnnData (.h5ad), SCE (.rds), Seurat (.rds)
│               ├── <sample>_filtered_matrix.h5ad
│               ├── <sample>_raw_matrix.h5ad
│               ├── combined_filtered_matrix.h5ad   ← preferred_h5ad (when present)
│               └── combined_raw_matrix.h5ad
├── reproducibility/
│   ├── samplesheet.valid.csv         # Normalized samplesheet (absolute POSIX paths)
│   ├── params.yaml                   # Effective Nextflow parameters
│   ├── commands.sh                   # Portable replay script
│   ├── environment.yml               # Conda environment spec (for reference)
│   ├── checksums.sha256              # SHA-256 for samplesheet, params, refs, h5ad, MultiQC
│   ├── manifest.json                 # Run metadata: preset, profile, versions, checksums
│   ├── macos_docker.config           # macOS+Docker workarounds (VirtioFS, ARM64, STAR FIFOs)
│   └── remap_paths.py                # Helper for replaying on a different machine
└── provenance/
    ├── inputs.json                   # Samplesheet and reference paths + checksums
    ├── invocation.json               # Timestamp, preset, profile, pipeline version
    ├── preflight.json                # Java/Nextflow/backend info
    ├── upstream.json                 # Pipeline source resolution details
    ├── outputs.json                  # Detected artifacts
    ├── runtime.json                  # Execution timing
    └── skill.json                    # Skill name and version
```

## Example Output

`result.json` (abbreviated):
```json
{
  "skill": "scrnaseq-pipeline",
  "version": "0.1.0",
  "summary": {
    "preset": "star",
    "aligner_effective": "star",
    "pipeline_source_kind": "remote_repo",
    "pipeline_version_or_commit": "4.1.0",
    "profile": "docker",
    "preferred_h5ad": "<output>/upstream/results/star/mtx_conversions/combined_filtered_matrix.h5ad",
    "handoff_available": true,
    "samples_detected": 2,
    "cellbender_used": false
  }
}
```

`report.md` closes with:
```
## Next Steps
- python clawbio.py run scrna --input <preferred_h5ad> --output <dir>
- python clawbio.py run scrna-embedding --input <preferred_h5ad> --output <dir>
```

## Gotchas

- **Preflight runs before any Nextflow call.** If Java, Nextflow, or the backend are missing or too old, the pipeline never starts and you get a structured JSON error with `error_code` and a `fix` hint. Nextflow ≥25.04.0 is required.
- **`--genome` conflicts with any explicit reference flag.** Providing `--genome` alongside `--fasta`, `--gtf`, or any index flag raises `CONFLICTING_REFERENCES` in preflight. Use either `--genome <shortcut>` or explicit flags — never both.
- **`igenomes_ignore` is set automatically.** Whenever any explicit reference path (fasta, gtf, any index) is provided, the wrapper writes `igenomes_ignore: true` to suppress nf-schema DNS validation of the default iGenomes S3 URL. You do not need to set this manually. Use `--igenomes-base` only for local iGenomes mirrors.
- **Protocol compatibility is enforced before Nextflow starts.** `standard`, `star`, and `kallisto` presets require an explicit non-`auto` protocol (e.g., `10XV3`, `dropseq`, or a supported custom chemistry string). `standard`/simpleaf additionally rejects `smartseq` — use `star` or `kallisto` for Smart-seq data. `cellranger`, `cellrangerarc`, and `cellrangermulti` accept any protocol value; `auto` is the typical upstream recommendation but is not enforced.
- **`--skip-cellbender` and `--skip-emptydrops` are independent flags.** `--skip-cellbender` disables the CellBender ambient RNA removal subworkflow; `--skip-emptydrops` disables the emptyDrops cell calling step. Both are written as separate parameters in `params.yaml` and each replays as its own flag in `commands.sh`. Setting one does not imply the other.
- **`--demo` forces preset=star and skip_cellbender=true.** The nf-core upstream `test` profile ships STAR-compatible data and explicitly disables CellBender (which does not work on small test datasets). If a different preset is requested with `--demo`, the wrapper warns and overrides it.
- **`preferred_h5ad` may be absent.** If no combined matrix is produced and there are multiple per-sample files, `handoff_available` is `false`. Always check `result.json` before chaining to `scrna-orchestrator` or `scrna-embedding`.
- **No arbitrary Nextflow passthrough.** All pipeline configuration flows through the preset system and `params.yaml`. Direct `-c`, `--outdir`, or custom Nextflow flags cannot be injected.
- **`--resume` enforces strict compatibility.** The wrapper checks that the stored manifest matches the current preset, profile, and pipeline source. Mismatches raise `INVALID_RESUME_STATE`.
- **RNA velocity requires two coordinated flags.** For STARsolo: `--star-feature "Gene Velocyto"` AND `--star-ignore-sjdbgtf` must be passed together. For Kallisto: `--kb-workflow lamanno` or `nac` with `--kb-t1c` and `--kb-t2c`.
- **`cellrangerarc` config and reference are paired.** Providing `--cellrangerarc-config` without `--cellrangerarc-reference` (or vice versa) raises `INVALID_PRESET_CONFIGURATION`. `--motifs` is optional and independent.
- **`cellrangermulti` validates against the samplesheet.** `feature_type=ab` requires `--fb-reference`; `feature_type=cmo` requires `--cellranger-multi-barcodes`; `feature_type=vdj` with `--skip-cellrangermulti-vdjref` requires `--cellranger-vdj-index`. CMO, FFPE probe-set, and OCM multiplexing modes are mutually exclusive.
- **FASTA schema validation.** The FASTA path must match `^\S+\.fn?a(sta)?(\.gz)?$` (the nf-core/scrnaseq 4.1.0 schema). Paths with whitespace or non-standard extensions are rejected in preflight.
- **Local checkout must be a sibling directory.** The wrapper looks for `../scrnaseq` relative to the ClawBio repo root. If the checkout path contains whitespace (common on macOS), the wrapper warns and falls back to the remote pipeline. Ensure `ClawBio/` and `scrnaseq/` share the same parent folder.
- **macOS Docker workaround is applied automatically.** On macOS with Docker, `macos_docker.config` is written to the reproducibility bundle and passed to Nextflow. It sets `stageInMode = "copy"` (avoids VirtioFS EDEADLK), `--platform linux/amd64` (Rosetta emulation), and routes STAR `_STARtmp` to the container's `/tmp` (avoids VirtioFS FIFO limitation). Output directories under `/tmp` emit a WARNING — use a path under HOME.

## Safety

- **Local-first**: User FASTQs and outputs remain on the local filesystem.
- **Strict preflight**: Nextflow is never invoked if validation fails.
- **No hallucinated outputs**: Only artifacts confirmed on disk are reported.
- **Disclaimer**: Every report includes the ClawBio medical disclaimer.

## Agent Boundary

The agent dispatches and explains; this skill executes.

**Agent**: Interpret the user's preprocessing intent, choose the preset, and verify that `handoff_available` is `true` in `result.json` before routing to downstream skills.

**Skill**: Validate environment and inputs, run the pipeline with controlled parameters, write all provenance and reproducibility artifacts, and report the detected `preferred_h5ad`.

## Chaining Partners

| Skill | When to chain |
|-------|--------------|
| `scrna-orchestrator` | After a successful run, pass `preferred_h5ad` for clustering, QC, and markers |
| `scrna-embedding` | Pass `preferred_h5ad` for scVI/scANVI batch integration and latent embeddings |
| `multiqc-reporter` | Re-aggregate QC across multiple wrapper runs |

## Maintenance

**Review cadence**: After each nf-core/scrnaseq major release. Check `NEXTFLOW_MIN_VERSION` (`schemas.py`), `SUPPORTED_PRESETS`, `SUPPORTED_PROFILES`, and this SKILL.md for accuracy.

**Staleness signals**:
- Preflight rejects a Nextflow version that the current pipeline supports → update `NEXTFLOW_MIN_VERSION` in `schemas.py` and `reproducibility/pinned_versions.json`.
- New aligners appear upstream but are absent from `PRESET_ALIGNERS` → add to `schemas.py` and update tests.
- The VirtioFS macOS workaround (`stageInMode = "copy"`) is only necessary while Apple Silicon runs Docker via QEMU. Remove `_write_macos_docker_config` when a native arm64 Docker runtime eliminates VirtioFS deadlocks.

**Deprecation criteria**: Deprecate if nf-core/scrnaseq releases a Python SDK with equivalent preflight, params, and provenance APIs.

## Citations

- [nf-core/scrnaseq 4.1.0](https://nf-co.re/scrnaseq/4.1.0)
- [nf-core/scrnaseq usage](https://nf-co.re/scrnaseq/4.1.0/docs/usage/)
- [nf-core/scrnaseq parameters](https://nf-co.re/scrnaseq/4.1.0/parameters/)
- [nf-core/scrnaseq output](https://nf-co.re/scrnaseq/4.1.0/docs/output/)
- [Nextflow](https://www.nextflow.io/)
- [Alevin-fry / Simpleaf](https://simpleaf.readthedocs.io/)
- [STARsolo](https://github.com/alexdobin/STAR/blob/master/docs/STARsolo.md)
- [kb-python / BUStools](https://www.kallistobus.tools/)
