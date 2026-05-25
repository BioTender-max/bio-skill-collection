# Prefect on HPC (Slurm): two common patterns

## Pattern A: Prefect → Slurm worker (one Slurm job per flow run)
Best when:
- Each flow run is a substantial HPC workload.
- You want Slurm to enforce quotas/policies.
- Prefect is used for orchestration, metadata, retries, UI.

### Conceptual steps
1. Install `prefect-slurm`
2. Create a Slurm work pool (`--type slurm`)
3. Configure Slurm REST API + token handling
4. Start a Slurm worker bound to that work pool

### Operational notes
- Ensure flow-run jobs can reach the Prefect API endpoint (Cloud or self-hosted).
- Decide where outputs live (shared filesystem vs object store).
- If your cluster uses modules/conda, prefer sourcing environment files before running the flow.

### Pitfalls
- Requires Slurm REST API enabled and reachable.
- Token/credentials management can be a stumbling block.
- If compute nodes have restricted networking, Prefect API reachability can fail.

## Pattern B: Prefect + Dask-jobqueue on Slurm (Dask spins up worker jobs)
Best when:
- You need distributed Python across multiple nodes for in-memory or partitioned compute.
- You can tolerate more moving parts and debug complexity.

### Template
```python
from dask_jobqueue import SLURMCluster
from dask.distributed import Client
from prefect import flow, task
from prefect_dask.task_runners import DaskTaskRunner

def build_cluster() -> Client:
    cluster = SLURMCluster(
        cores=8,
        processes=1,
        memory="32GB",
        walltime="02:00:00",
        queue="compute",
        # job_extra_directives=[...],  # cluster-specific
    )
    cluster.scale(jobs=10)  # or cluster.adapt(minimum=1, maximum=10)
    return Client(cluster)

@task
def heavy_step(x: int) -> int:
    return x * x

@flow(task_runner=DaskTaskRunner(address=build_cluster().scheduler.address))
def hpc_flow(items: list[int]) -> list[int]:
    futures = [heavy_step.submit(x) for x in items]
    return [f.result() for f in futures]
```

### Pitfalls (double scheduling)
You may end up with:
- Prefect schedules the flow run
- Dask schedules tasks
- Slurm schedules Dask workers

It can be correct, but increases startup latency and debugging complexity.

## Recommendation for CLI-heavy bioinformatics on HPC
If most steps are external CLI tools (bwa, samtools, gatk, etc.), prefer **Nextflow** for the compute plane.
See: [nextflow-hpc.md](nextflow-hpc.md)

