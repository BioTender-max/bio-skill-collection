#!/usr/bin/env python3
"""Generate a SLURM sbatch script from resource and launch parameters."""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import sys
from typing import Dict, List, Optional, Sequence, Tuple, TypedDict


_JOB_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
_WALLTIME_RE = re.compile(r"^(?:(?P<days>[0-9]+)-)?(?P<hours>[0-9]{1,3}):(?P<mins>[0-9]{2}):(?P<secs>[0-9]{2})$")
# Slurm --mem/--mem-per-cpu/--mem-per-gpu accept integer MB by default, or an
# integer with a suffix in [K|M|G|T]. Keep validation strict to avoid generating
# scripts that Slurm rejects.
_MEM_RE = re.compile(r"^[0-9]+(?:[KMGT])?$", re.IGNORECASE)
_ENV_KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

class SlurmResources(TypedDict):
    nodes: int
    ntasks: int
    ntasks_per_node: Optional[int]
    cpus_per_task: int
    mem: Optional[str]
    mem_per_cpu: Optional[str]
    gpus_per_node: Optional[int]
    gpu_type: Optional[str]


def _validate_job_name(name: str) -> str:
    if not name or not _JOB_NAME_RE.match(name):
        raise ValueError(
            "job-name must match /^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$/ (no spaces)"
        )
    return name


def _normalize_walltime(value: str) -> str:
    m = _WALLTIME_RE.match(value.strip())
    if not m:
        raise ValueError("time must be HH:MM:SS or D-HH:MM:SS")
    days = int(m.group("days") or "0")
    hours = int(m.group("hours"))
    mins = int(m.group("mins"))
    secs = int(m.group("secs"))
    if days < 0 or hours < 0:
        raise ValueError("time must be non-negative")
    if not (0 <= mins <= 59) or not (0 <= secs <= 59):
        raise ValueError("time minutes/seconds must be in [00,59]")
    if days > 0:
        return f"{days}-{hours:02d}:{mins:02d}:{secs:02d}"
    return f"{hours:02d}:{mins:02d}:{secs:02d}"


def _validate_positive_int(name: str, value: int) -> int:
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def _validate_mem_spec(flag: str, value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    v = value.strip()
    if not v:
        raise ValueError(f"{flag} must be non-empty when provided")
    if not _MEM_RE.match(v):
        raise ValueError(
            f"{flag} must be an integer (MB) or an integer with suffix in [K|M|G|T] (e.g. 16000M, 16G)"
        )
    return v


def _validate_env_kv(pairs: Sequence[str]) -> List[Tuple[str, str]]:
    out: List[Tuple[str, str]] = []
    for item in pairs:
        if "=" not in item:
            raise ValueError(f"env must be KEY=VALUE (got {item!r})")
        key, value = item.split("=", 1)
        key = key.strip()
        if not _ENV_KEY_RE.match(key):
            raise ValueError(f"env key must be a valid identifier (got {key!r})")
        out.append((key, value))
    return out


def build_resources(
    *,
    nodes: int,
    ntasks: Optional[int],
    ntasks_per_node: Optional[int],
    cpus_per_task: int,
    mem: Optional[str],
    mem_per_cpu: Optional[str],
    gpus_per_node: Optional[int],
    gpu_type: Optional[str],
) -> SlurmResources:
    """Pure function: validate and normalize resource request."""
    nodes = _validate_positive_int("nodes", nodes)
    cpus_per_task = _validate_positive_int("cpus-per-task", cpus_per_task)

    if ntasks is not None and ntasks_per_node is not None:
        raise ValueError("Provide either --ntasks or --ntasks-per-node, not both")

    if ntasks_per_node is not None:
        ntasks_per_node = _validate_positive_int("ntasks-per-node", ntasks_per_node)
        derived_ntasks = nodes * ntasks_per_node
        ntasks = derived_ntasks
    else:
        ntasks = _validate_positive_int("ntasks", ntasks or 1)

    mem = _validate_mem_spec("--mem", mem)
    mem_per_cpu = _validate_mem_spec("--mem-per-cpu", mem_per_cpu)
    if mem is not None and mem_per_cpu is not None:
        raise ValueError("Provide either --mem or --mem-per-cpu, not both")

    if gpus_per_node is not None:
        gpus_per_node = _validate_positive_int("gpus-per-node", gpus_per_node)
        if gpu_type is not None and not gpu_type.strip():
            raise ValueError("gpu-type must be non-empty when provided")

    return {
        "nodes": nodes,
        "ntasks": ntasks,
        "ntasks_per_node": ntasks_per_node,
        "cpus_per_task": cpus_per_task,
        "mem": mem,
        "mem_per_cpu": mem_per_cpu,
        "gpus_per_node": gpus_per_node,
        "gpu_type": gpu_type.strip() if gpu_type is not None else None,
    }


def generate_sbatch_script(
    *,
    job_name: str,
    time_limit: str,
    partition: Optional[str],
    account: Optional[str],
    qos: Optional[str],
    constraint: Optional[str],
    reservation: Optional[str],
    exclusive: bool,
    output: Optional[str],
    error: Optional[str],
    mail_user: Optional[str],
    mail_type: Optional[str],
    workdir: Optional[str],
    modules: Sequence[str],
    env: Sequence[str],
    launcher: str,
    srun_extra: Optional[str],
    command: Sequence[str],
    resources: SlurmResources,
    cores_per_node: Optional[int] = None,
) -> Dict[str, object]:
    """Pure function: return JSON payload with the generated sbatch script."""
    job_name = _validate_job_name(job_name)
    time_limit = _normalize_walltime(time_limit)
    if not command:
        raise ValueError("Provide a run command after --")

    directives: List[str] = []
    directives.append(f"#SBATCH --job-name={job_name}")
    directives.append(f"#SBATCH --time={time_limit}")
    directives.append(f"#SBATCH --nodes={resources['nodes']}")

    if partition:
        directives.append(f"#SBATCH --partition={partition}")
    if account:
        directives.append(f"#SBATCH --account={account}")
    if qos:
        directives.append(f"#SBATCH --qos={qos}")

    if resources["ntasks_per_node"] is not None:
        directives.append(f"#SBATCH --ntasks-per-node={resources['ntasks_per_node']}")
    else:
        directives.append(f"#SBATCH --ntasks={resources['ntasks']}")
    directives.append(f"#SBATCH --cpus-per-task={resources['cpus_per_task']}")

    if resources["mem"] is not None:
        directives.append(f"#SBATCH --mem={resources['mem']}")
    if resources["mem_per_cpu"] is not None:
        directives.append(f"#SBATCH --mem-per-cpu={resources['mem_per_cpu']}")

    if resources["gpus_per_node"] is not None:
        if resources["gpu_type"]:
            directives.append(
                f"#SBATCH --gres=gpu:{resources['gpu_type']}:{resources['gpus_per_node']}"
            )
        else:
            directives.append(f"#SBATCH --gres=gpu:{resources['gpus_per_node']}")

    if output:
        directives.append(f"#SBATCH --output={output}")
    if error:
        directives.append(f"#SBATCH --error={error}")

    if mail_user:
        directives.append(f"#SBATCH --mail-user={mail_user}")
        if mail_type:
            directives.append(f"#SBATCH --mail-type={mail_type}")

    if constraint:
        directives.append(f"#SBATCH --constraint={constraint}")
    if reservation:
        directives.append(f"#SBATCH --reservation={reservation}")
    if exclusive:
        directives.append("#SBATCH --exclusive")

    warnings: List[str] = []
    derived: Dict[str, object] = {
        "ntasks": resources["ntasks"],
        "ntasks_per_node": resources["ntasks_per_node"],
        "cpus_total_requested": resources["ntasks"] * resources["cpus_per_task"],
    }

    if cores_per_node is not None:
        cores_per_node = _validate_positive_int("cores-per-node", cores_per_node)
        derived["cores_per_node"] = cores_per_node
        if resources["ntasks_per_node"] is not None:
            per_node = resources["ntasks_per_node"] * resources["cpus_per_task"]
            derived["cpus_per_node_requested"] = per_node
            if per_node > cores_per_node:
                warnings.append(
                    f"Oversubscription risk: ntasks-per-node*cpus-per-task={per_node} > cores-per-node={cores_per_node}"
                )

    env_pairs = _validate_env_kv(env)

    cmd_str = " ".join(shlex.quote(x) for x in command)
    if launcher == "srun":
        srun_bits = [
            "srun",
            f"--ntasks={resources['ntasks']}",
            f"--cpus-per-task={resources['cpus_per_task']}",
        ]
        if srun_extra:
            srun_bits.append(srun_extra.strip())
        run_line = " ".join(srun_bits + [cmd_str])
    elif launcher == "none":
        run_line = cmd_str
    else:
        raise ValueError("launcher must be one of: srun, none")

    lines: List[str] = []
    lines.append("#!/usr/bin/env bash")
    lines.append("set -euo pipefail")
    lines.append("")
    lines.extend(directives)
    lines.append("")

    lines.append('echo "job_id=${SLURM_JOB_ID:-unknown} start=$(date)"')
    lines.append('echo "node_list=${SLURM_JOB_NODELIST:-unknown}"')

    # Working directory
    if workdir:
        lines.append(f"cd {shlex.quote(workdir)}")
    else:
        lines.append('cd "${SLURM_SUBMIT_DIR:-$PWD}"')
    lines.append('echo "pwd=$(pwd)"')
    lines.append("")

    # Optional module loading
    if modules:
        lines.append("if command -v module >/dev/null 2>&1; then")
        lines.append("  module purge || true")
        for mod in modules:
            lines.append(f"  module load {shlex.quote(mod)}")
        lines.append("else")
        lines.append('  echo "warning: environment modules not available; skipping module load" >&2')
        lines.append("fi")
        lines.append("")

    # Threading environment
    lines.append(f"export OMP_NUM_THREADS={resources['cpus_per_task']}")
    lines.append("export OMP_PLACES=cores")
    lines.append("export OMP_PROC_BIND=close")
    for key, value in env_pairs:
        lines.append(f"export {key}={shlex.quote(value)}")
    lines.append("")

    lines.append(run_line)
    lines.append("")
    lines.append('echo "job_id=${SLURM_JOB_ID:-unknown} end=$(date)"')

    script = "\n".join(lines) + "\n"

    return {
        "inputs": {
            "job_name": job_name,
            "time": time_limit,
            "partition": partition,
            "account": account,
            "nodes": resources["nodes"],
            "ntasks": resources["ntasks"],
            "ntasks_per_node": resources["ntasks_per_node"],
            "cpus_per_task": resources["cpus_per_task"],
            "mem": resources["mem"],
            "mem_per_cpu": resources["mem_per_cpu"],
            "gpus_per_node": resources["gpus_per_node"],
            "gpu_type": resources["gpu_type"],
            "workdir": workdir,
            "modules": list(modules),
            "env": list(env),
            "launcher": launcher,
            "srun_extra": srun_extra,
            "command": list(command),
        },
        "results": {
            "directives": directives,
            "derived": derived,
            "warnings": warnings,
            "run_line": run_line,
            "script": script,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a SLURM sbatch script from resource and launch parameters.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("--job-name", required=True, help="SLURM job name (no spaces)")
    parser.add_argument(
        "--time",
        required=True,
        help="Walltime limit (HH:MM:SS or D-HH:MM:SS)",
    )
    parser.add_argument("--partition", default=None, help="SLURM partition")
    parser.add_argument("--account", default=None, help="SLURM account/project")
    parser.add_argument("--qos", default=None, help="SLURM QoS")
    parser.add_argument("--constraint", default=None, help="SLURM constraint")
    parser.add_argument("--reservation", default=None, help="SLURM reservation")
    parser.add_argument("--exclusive", action="store_true", help="Request exclusive node access")

    parser.add_argument("--nodes", type=int, default=1, help="Number of nodes")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--ntasks", type=int, default=None, help="Total MPI tasks/ranks")
    group.add_argument(
        "--ntasks-per-node",
        type=int,
        default=None,
        help="MPI tasks/ranks per node",
    )
    parser.add_argument(
        "--cpus-per-task",
        type=int,
        default=1,
        help="CPU cores per task (OpenMP threads)",
    )

    parser.add_argument("--mem", default=None, help="Memory per node (e.g. 32G)")
    parser.add_argument(
        "--mem-per-cpu",
        default=None,
        help="Memory per CPU core (e.g. 2G)",
    )
    parser.add_argument("--gpus-per-node", type=int, default=None, help="GPUs per node")
    parser.add_argument("--gpu-type", default=None, help="GPU type for --gres (optional)")

    parser.add_argument("--output", default=None, help="Stdout file pattern (e.g. slurm-%j.out)")
    parser.add_argument("--error", default=None, help="Stderr file pattern (e.g. slurm-%j.err)")
    parser.add_argument("--mail-user", default=None, help="Email address for notifications")
    parser.add_argument("--mail-type", default=None, help="Mail types (e.g. END,FAIL)")

    parser.add_argument(
        "--workdir",
        default=None,
        help="Working directory (default: SLURM_SUBMIT_DIR)",
    )
    parser.add_argument(
        "--module",
        action="append",
        default=[],
        help="Module to load (repeatable)",
    )
    parser.add_argument(
        "--env",
        action="append",
        default=[],
        help="Environment variable KEY=VALUE (repeatable)",
    )

    parser.add_argument(
        "--launcher",
        choices=["srun", "none"],
        default="srun",
        help="How to launch the command inside the allocation",
    )
    parser.add_argument(
        "--srun-extra",
        default=None,
        help="Extra text appended to the srun invocation (advanced)",
    )

    parser.add_argument(
        "--cores-per-node",
        type=int,
        default=None,
        help="Optional sanity-check: physical cores per node for oversubscription warnings",
    )
    parser.add_argument("--out", default=None, help="Write the script to this path")
    parser.add_argument("--json", action="store_true", help="Emit JSON payload")

    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="Command to run after `--` (e.g. -- ./simulate --config cfg.json)",
    )
    return parser.parse_args()


def _write_text(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    with open(path, "w", newline="\n") as f:
        f.write(text)


def main() -> None:
    args = parse_args()
    # argparse includes the `--` separator only as an option terminator, not in the remainder
    command = [c for c in args.command if c != "--"]

    try:
        resources = build_resources(
            nodes=args.nodes,
            ntasks=args.ntasks,
            ntasks_per_node=args.ntasks_per_node,
            cpus_per_task=args.cpus_per_task,
            mem=args.mem,
            mem_per_cpu=args.mem_per_cpu,
            gpus_per_node=args.gpus_per_node,
            gpu_type=args.gpu_type,
        )
        payload = generate_sbatch_script(
            job_name=args.job_name,
            time_limit=args.time,
            partition=args.partition,
            account=args.account,
            qos=args.qos,
            constraint=args.constraint,
            reservation=args.reservation,
            exclusive=args.exclusive,
            output=args.output,
            error=args.error,
            mail_user=args.mail_user,
            mail_type=args.mail_type,
            workdir=args.workdir,
            modules=args.module,
            env=args.env,
            launcher=args.launcher,
            srun_extra=args.srun_extra,
            command=command,
            resources=resources,
            cores_per_node=args.cores_per_node,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)

    script = str(payload["results"]["script"])
    if args.out:
        try:
            _write_text(args.out, script)
        except OSError as exc:
            print(f"Failed to write {args.out}: {exc}", file=sys.stderr)
            sys.exit(1)

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    if args.out:
        print(f"Wrote {args.out}")
        return

    print(script, end="")


if __name__ == "__main__":
    main()
