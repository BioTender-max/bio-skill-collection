# Nextflow on HPC (Slurm/PBS) playbook

## Why Nextflow for HPC bioinformatics
- Nextflow’s executor layer lets you keep pipeline logic independent of the execution platform (local vs Slurm vs PBS).
- Each process is executed as a scheduler job under HPC executors.
- Caching/resume is first-class (good for long, multi-step genomics pipelines).

## Minimal repository layout (DSL2)
- `main.nf`
- `nextflow.config`
- `modules/`
  - `fastqc.nf`
  - `align_bwa.nf`
- Optional: `conf/` for profile-specific configs

## Minimal DSL2 skeleton (main.nf)
```nextflow
nextflow.enable.dsl=2

include { FASTQC } from './modules/fastqc'

workflow {
  reads_ch = Channel.fromPath(params.reads)
  FASTQC(reads_ch)
}
```

## Minimal module example (modules/fastqc.nf)
```nextflow
process FASTQC {
  tag "$reads.baseName"

  input:
    path reads

  output:
    path "${reads.baseName}_fastqc.zip"
    path "${reads.baseName}_fastqc.html"

  script:
  """
  fastqc -t ${task.cpus} $reads
  """
}
```

## HPC config example (nextflow.config)
```groovy
nextflow.enable.dsl=2

params {
  reads  = null
  outdir = "results"
}

// Prefer setting workDir to fast scratch on HPC when possible
// workDir = "/scratch/$USER/nxf-work"

profiles {
  local {
    process.executor = 'local'
  }

  slurm {
    process.executor = 'slurm'
    process.queue    = 'compute'
    process.cpus     = 4
    process.memory   = '16 GB'
    process.time     = '2h'

    // Protect the scheduler / shared FS from too many tiny jobs
    // executor.queueSize       = 100
    // executor.submitRateLimit = '10 sec'
  }

  pbs {
    process.executor = 'pbs'
    process.queue    = 'workq'
    process.cpus     = 4
    process.memory   = '16 GB'
    process.time     = '2h'
  }
}
```

Run:
- Local: `nextflow run main.nf -profile local --reads 'data/*.fastq.gz'`
- Slurm:  `nextflow run main.nf -profile slurm --reads '/path/*.fastq.gz'`
- Resume: `nextflow run main.nf -profile slurm -resume --reads '/path/*.fastq.gz'`

## Resuming and caching (agent guidance)
- Use `-resume` to reuse cached task results.
- Preserve the work directory and `.nextflow/` cache for resumability.
- Avoid nondeterministic inputs if you want reliable cache hits.
- Be deliberate about cleanup: aggressive cleanup trades off resumability/debuggability.

## Filesystem performance guidance (HPC)
- Put the **work directory** on fast scratch if available.
- Consider `scratch true` for processes that benefit from node-local execution, staging only final outputs.
- Avoid generating huge numbers of tiny intermediate files when possible (pipe/stream between tools).

## Pitfalls
- Too many tiny processes → scheduler overhead + filesystem pressure.
- Mis-specified resources → jobs killed by scheduler; start conservative and tune with trace reports.
- Container policy mismatches (Docker blocked on HPC) → plan for Singularity/Apptainer or Conda.

