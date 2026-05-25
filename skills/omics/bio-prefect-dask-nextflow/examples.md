# Examples (Prefect-only, Nextflow-only, Hybrid)

## Example 1: Prefect + Dask local QC
Use when:
- You’re iterating quickly on a workstation.
- Steps are Python-heavy or need dynamic branching.

Blueprint:
- A Prefect flow maps over samples and runs tasks via `.submit()`.
- DaskTaskRunner runs tasks in parallel on a LocalCluster.
- Outputs written to `results/` with deterministic paths.

## Example 2: Nextflow on Slurm for alignment
Use when:
- You’re executing a classic file-based genomics pipeline on HPC.

Blueprint processes:
- FASTQC → ALIGN (bwa mem) → SORT/INDEX (samtools) → METRICS
- Profiles: `local`, `slurm`, `pbs`
- Run with `-resume` to recover from partial failures.

## Example 3: Hybrid: Prefect orchestrates batches, Nextflow executes compute
Pattern:
- Prefect flow:
  1. Ingest new samples (LIMS/DB/S3)
  2. Validate inputs + stage to shared/scratch
  3. Batch samples (e.g., 50 samples/run)
  4. Submit a Nextflow run per batch (via CLI or as a scheduler job)
  5. Parse Nextflow reports (trace/timeline) and publish artifacts/metrics
  6. Notify on failure; optionally require approval for reruns

Watch-outs:
- Don’t double-retry (Prefect retries + Nextflow retries) without a clear policy.
- Standardize work/results paths so Prefect can locate outputs reliably.

