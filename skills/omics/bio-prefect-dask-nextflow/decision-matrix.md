# Decision matrix: Prefect + Dask vs Nextflow (HPC bioinformatics)

## One-sentence summary
- **Prefect + Dask**: Python-first orchestration + distributed Python task execution (excellent for dynamic, Python-heavy pipelines).
- **Nextflow**: DSL + scheduler-native execution for file-based scientific workflows (excellent on HPC with Slurm/PBS).

## Choose Prefect + Dask when…
- Steps are primarily **Python functions** (data transforms, API calls, ML inference/training, metadata handling).
- You need **dynamic control flow** (branching on results, adaptive batching).
- You want **tight integration** with Python libraries and services (DBs, message queues, REST APIs).
- You can run (or reach) a Prefect API (Cloud/self-hosted) from execution environments.

### Strengths
- Python-native: no separate DSL.
- Strong orchestration semantics: retries, state tracking, schedules, events.
- Easy local parallelism with Dask LocalCluster; can connect to existing Dask clusters.

### Pitfalls
- Too many tiny tasks → overhead (serialization, scheduling, logging).
- Non-picklable objects / global state can break under multiprocessing/distributed execution.
- HPC networking can complicate Dask (scheduler/worker ports) and Prefect connectivity.

## Choose Nextflow when…
- Pipeline is mostly **CLI bioinformatics tools** reading/writing files (FASTQ/BAM/VCF/FASTA, etc.).
- You need **HPC scheduler-native** execution (Slurm/PBS/LSF) and portability.
- Reproducibility matters: pinned containers/conda envs, consistent work directory, deterministic caching.
- You expect users to run the pipeline on many infrastructures (local, HPC, cloud) via profiles.

### Strengths
- HPC-friendly execution model: processes map cleanly to scheduler jobs.
- Built-in caching/resume and per-process resource directives.
- Rich ecosystem (e.g., nf-core) and strong portability patterns.

### Pitfalls
- Learning curve: DSL2, channels, process directives.
- Many tiny processes can overload schedulers and shared filesystems.
- Debugging is less “step-through” than Python.

## Choose Hybrid when…
Use Prefect as a **control plane** (metadata, batching, approvals, notifications, dashboards),
while Nextflow runs the **compute plane** (HPC-heavy, file-based steps).

## Anti-patterns
- Using Nextflow for workflows that require heavy in-memory Python object passing.
- Using Prefect+Dask to orchestrate thousands of short scheduler jobs where a scheduler-native engine is simpler.
- Double-scheduling without intent (Prefect schedules runs → Dask schedules tasks → Slurm schedules workers).

## Practical rule of thumb
- If your step is “**run a tool over files**” → Nextflow process.
- If your step is “**Python decides what to do next**” → Prefect task/flow.

