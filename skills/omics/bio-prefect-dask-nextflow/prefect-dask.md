# Prefect + Dask playbook (local-first, scalable to clusters)

## What this gives you
- Prefect handles orchestration (retries, states, schedules, artifacts).
- Dask handles parallel execution of Prefect tasks (local or distributed).

## Install
Prefer the official extra:
- `pip install "prefect[dask]"`

## Local setup (optional but recommended)
1. Start a local Prefect server/UI:
   - `prefect server start`
2. Run flows locally during development (you can still run without the UI).

## Key rules (agent should enforce)
- **Concurrency requires `.submit()` or `.map()`**. Direct task calls run sequentially.
- `DaskTaskRunner` uses multiprocessing → guard flow invocation with:
  `if __name__ == "__main__":`
- Default behavior: if no Dask scheduler address is provided, Prefect can create a temporary local cluster.

## Minimal template: sample-parallel QC
```python
from __future__ import annotations

from pathlib import Path
import subprocess

from prefect import flow, task
from prefect_dask.task_runners import DaskTaskRunner

@task(retries=2, retry_delay_seconds=30)
def fastqc(reads: Path, outdir: Path) -> Path:
    outdir.mkdir(parents=True, exist_ok=True)
    sample_out = outdir / reads.stem
    sample_out.mkdir(exist_ok=True)

    cmd = ["fastqc", "-o", str(sample_out), str(reads)]
    subprocess.run(cmd, check=True)

    # Return a deterministic artifact path
    return sample_out

@flow(
    name="qc-fastq",
    task_runner=DaskTaskRunner(
        cluster_kwargs={"n_workers": 4, "threads_per_worker": 1}
    ),
)
def qc_flow(reads_glob: str, outdir: str = "results/qc") -> list[str]:
    reads = list(Path(".").glob(reads_glob))
    futures = [fastqc.submit(r, Path(outdir)) for r in reads]
    results = [f.result() for f in futures]
    return [str(p) for p in results]

if __name__ == "__main__":
    qc_flow("data/*.fastq.gz")
```

## Connecting to an existing Dask cluster
If a Dask scheduler is already running (local or remote):

```python
from prefect import flow
from prefect_dask.task_runners import DaskTaskRunner

@flow(task_runner=DaskTaskRunner(address="tcp://scheduler-host:8786"))
def my_flow():
    ...
```

## Tuning guidance
- Prefer **coarse-ish task granularity** (1 task per sample or per chunk), not 10k tiny tasks.
- Pass **paths/URIs**, not huge objects.
- Make tasks idempotent: write outputs to deterministic locations and check for existence.

## When NOT to use DaskTaskRunner
- Work is mostly “shell out to many tiny CLI calls on HPC” (Nextflow is usually a better fit).
- Tasks depend on non-picklable state (open DB connections, open file handles, GPU contexts) that isn’t recreated inside the task.

