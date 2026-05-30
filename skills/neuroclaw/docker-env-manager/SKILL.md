---
name: docker-env-manager
description: "Use this skill whenever the user wants to pull, run, build, compose, list, prune, manage, or otherwise handle Docker containers, images, volumes, networks, or Docker Compose projects, or when a NeuroClaw skill (e.g. wmh-segmentation, freesurfer-processor in container mode) requires a clean, isolated, GPU-enabled Docker environment (e.g. 'pull mars-wmh image', 'run container with GPU', 'docker compose up', 'prune unused images', 'build custom dockerfile', 'manage nvidia docker'). Triggers include: 'docker run', 'docker pull', 'docker compose', 'docker build', 'docker env', 'manage container', 'nvidia docker', 'pull image', 'docker prune', 'containerize'. This skill is the **mandatory gatekeeper for all Docker operations** in NeuroClaw: it ALWAYS plans first, shows commands + risks + best practices, and waits for explicit user confirmation before executing anything. All actual Docker execution is routed through `claw-shell`."
license: MIT License (NeuroClaw custom skill – freely modifiable within the project)
layer: subagent
skill_type: tool
dependencies:
  - claw-shell
  - dependency-planner
---
# Docker Environment Manager (Tool Layer)

## Overview

Docker is the backbone for reproducible, containerized, GPU-accelerated environments in NeuroClaw — especially for deep-learning and neuroimaging skills (MARS-WMH nnU-Net, future nnU-Net models, containerized FreeSurfer, etc.) that require exact runtime isolation, NVIDIA GPU passthrough, and large pre-built images.

This skill acts as the **interface-layer orchestrator** for all common Docker operations, preventing permission issues, GPU misconfiguration, port conflicts, and storage bloat while enforcing best practices (named containers, volume mounts, `--gpus all`, docker-compose for multi-service stacks, dry-run previews, and safe pruning).

**Strict workflow (never skipped):**
1. Parse user intent from the request or context (pull / run / build / compose / prune / list / cleanup).
2. Detect current Docker setup (`docker --version`, `docker info`, NVIDIA Container Toolkit via `nvidia-smi` through `claw-shell`, available disk space, GPU status).
3. Propose a safe, best-practice plan:
   - Always prefer named containers/volumes over anonymous ones
   - Suggest `--gpus all` + volume mounts for NeuroClaw GPU skills
   - Recommend `docker-compose.yml` for reproducible multi-container stacks
   - Use `--dry-run` equivalents and plan preview by default
   - Warn about large image pulls (several GB), permission issues (`chmod -R 777` on data dirs), and GPU driver mismatches
   - Route **all** actual `docker run/pull/build` commands through `claw-shell`
4. Show numbered plan + exact commands + estimated time/size + risks.
5. Wait for explicit user confirmation (“YES”, “execute”, “proceed”).
6. On approval: delegate execution safely to `claw-shell` (with logging), capture output, report success/failure, and suggest next steps.

**Core safety & best-practice rules**
- Never run destructive commands (`docker system prune -a`, `docker rm -f`) without double confirmation
- All shell-level Docker commands **must** go through `claw-shell` (centralized logging + safety gate)
- Prefer `docker compose` over legacy `docker-compose`
- Integrate with `dependency-planner` for installing Docker + NVIDIA Container Toolkit
- Log all actions to `./logs/docker_YYYYMMDD_HHMMSS.log`

## Quick Reference (Common NeuroClaw Tasks)

| Task                                      | Recommended Approach (after user confirmation)                          |
|-------------------------------------------|-------------------------------------------------------------------------|
| Pull latest model image                   | `docker pull ghcr.io/miac-research/wmh-nnunet:latest` (then tag)       |
| Run GPU container with data mount         | `docker run --rm --gpus all -v $(pwd)/data:/data image ...`            |
| Docker Compose stack                      | `docker compose -f docker-compose.yml up -d`                           |
| Build custom Dockerfile                   | `docker build -t neuroclaw-custom .`                                   |
| List containers / images                  | `docker ps -a` / `docker images`                                       |
| Safe cleanup of unused resources          | `docker system prune --dry-run` → confirm → execute via claw-shell     |
| Fix common permission issues              | `chmod -R 777 output_dir` (auto-included in plans)                     |
| GPU check & NVIDIA Toolkit install        | Hand over to `dependency-planner` if `nvidia-smi` fails               |

## Installation

This skill is pure Python orchestration — no external binaries needed beyond a working Docker installation.

**Required prerequisites (must exist before activation):**
- Working Docker Engine (with NVIDIA Container Toolkit for GPU skills)
- `claw-shell` (mandatory — all Docker commands are routed here)
- `dependency-planner` (recommended companion for installing Docker + NVIDIA Container Toolkit)
- Basic shell access

To register in NeuroClaw:
```bash
# Place files in: skills/docker-env-manager/
# Update SOUL.md and/or USER.md with trigger phrases
```

## NeuroClaw recommended wrapper script

```python
# docker_env_manager.py
import subprocess
import argparse
import sys
from pathlib import Path
from datetime import datetime

def run_docker_cmd(cmd, dry_run=False):
    full_cmd = ["docker"] + cmd
    print("Would run (via claw-shell):", " ".join(full_cmd))
    # In real implementation: delegate to claw-shell skill after user confirmation
    # e.g. tool_call("claw_shell_run", {"command": " ".join(full_cmd)})

def get_docker_info():
    try:
        version = subprocess.check_output(["docker", "--version"]).decode().strip()
        info = subprocess.check_output(["docker", "info", "--format", "{{.ServerVersion}}"]).decode().strip()
        return f"Docker {version} | Engine {info}"
    except:
        return "Docker not found or error."

def check_gpu():
    try:
        return subprocess.check_output(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"]).decode().strip()
    except:
        return "No NVIDIA GPU detected or NVIDIA Container Toolkit missing"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NeuroClaw Docker Environment Manager")
    parser.add_argument("--request", required=True, help="User request (pull/run/compose/prune...)")
    parser.add_argument("--dry-run", action="store_true", help="Only show plan")
    args = parser.parse_args()
```

## Harness-Aware Container Isolation & Security Standards

All Docker operations performed via docker-env-manager **must** enforce strict isolation, security boundaries, and reproducibility standards.

### Container Specification Format (Declarative Registry)

Each containerized skill **must** include a Docker specification manifest:

**File**: `skills/{skill_name}/docker-spec.json`

```json
{
  "skill_name": "wmh-segmentation",
  "container_name": "neuroclaw-wmh-seg",
  "image": "ghcr.io/miac-research/wmh-nnunet:latest",
  "image_hash": "sha256:abc123...",
  "container_security": {
    "read_only_root": true,
    "cap_drop": ["ALL"],
    "cap_add": ["NET_BIND_SERVICE"],
    "security_opts": ["no-new-privileges:true"],
    "user": "1000:1000",
    "privileged": false
  },
  "resource_limits": {
    "memory_limit": "16G",
    "memory_swap": "16G",
    "cpus": "4",
    "pids_limit": 512,
    "ulimits": {
      "nofile": 1024,
      "nproc": 512
    }
  },
  "network_config": {
    "network": "bridge",
    "expose_ports": [],
    "environment_whitelist": [
      "CUDA_VISIBLE_DEVICES",
      "TORCH_HOME"
    ]
  },
  "volume_mounts": {
    "/data": {
      "bind": "{data_path}",
      "mode": "ro",
      "required": true
    },
    "/output": {
      "bind": "{output_path}",
      "mode": "rw",
      "required": true
    },
    "/tmp": {
      "bind": "/dev/shm",
      "mode": "rw",
      "size_limit": "8G"
    }
  },
  "gpu_config": {
    "enabled": true,
    "device_ids": "all",
    "driver_capabilities": "compute,utility"
  },
  "logging": {
    "driver": "json-file",
    "options": {
      "max-size": "10m",
      "max-file": "3"
    }
  }
}
```

### Container Execution Protocol

**Step 1: Pre-execution container validation**
```bash
# Verify image integrity
docker inspect ${image_hash} --format='{{.RepoDigests}}'

# Check for vulnerabilities (if vulnerability scanner available)
trivy image --severity HIGH,CRITICAL ${image}

# Verify GPU access
nvidia-smi -L  # List all GPUs

# Pre-flight resource check
docker stats --no-stream ${existing_container_name} || true
```

**Step 2: Secure container creation**
Template (auto-generated based on docker-spec.json):
```bash
docker run \
  --name ${CONTAINER_NAME} \
  --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges:true \
  --user 1000:1000 \
  --memory=${MEMORY_LIMIT} \
  --memory-swap=${MEMORY_LIMIT} \
  --cpus=${CPU_LIMIT} \
  --pids-limit=512 \
  --gpus=all \
  --env CUDA_VISIBLE_DEVICES=${GPU_DEVICES} \
  -v ${DATA_PATH}:/data:ro \
  -v ${OUTPUT_PATH}:/output:rw \
  -v /dev/shm:/tmp:rw \
  --log-driver=json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  --network=bridge \
  ${IMAGE} \
  ${COMMAND}
```

**Step 3: Post-execution audit logging**
```json
{
  "execution_time": "2026-04-05T14:32:00Z",
  "container_id": "abc123def456",
  "image": "ghcr.io/miac-research/wmh-nnunet:latest",
  "command": "python inference.py --input /data --output /output",
  "exit_code": 0,
  "resource_usage": {
    "memory_peak_mb": 8192,
    "cpu_time_seconds": 1203.5,
    "gpu_memory_peak_mb": 6144,
    "io_read_bytes": 5368709120,
    "io_write_bytes": 2684354560
  },
  "security_events": [],
  "status": "SUCCESS"
}
```

### Data Privacy & Isolation Guardrails

**Mandatory privacy checks before container execution**:

1. **Input data anonymization verification**:
   - Scan for known PII patterns (patient IDs, medical record numbers, names, birthdates)
   - Flag any unredacted identifiable information
   - Hash-verify input against reference dataset (prevent contamination)

2. **Output post-processing**:
   - Scan generated files for embedded PII or metadata
   - Automatically redact timestamps, user paths from logs
   - Generate sanitized output copies for sharing

3. **Filesystem sandboxing audit**:
   - Verify no mounts point to system directories (/, /etc, /root, /home)
   - Enforce read-only root filesystem
   - Whitelist environment variables (drop all except approved list)

**Generated audit report** (`container_privacy_audit.json`):
```json
{
  "container": "wmh-seg-20260405",
  "privacy_scan": {
    "input_files_scanned": 50,
    "pii_detected": 0,
    "output_files_sanitized": 50,
    "suspicious_environment_vars": 0,
    "mount_violations": 0,
    "status": "CLEARED"
  },
  "isolation_verification": {
    "readonly_root": true,
    "privilege_dropping": true,
    "network_isolation": true,
    "capability_dropping": true
  }
}
```

### Container Reproducibility & Layer Verification

**Image integrity checking** (SHA256 verification at run time):

```bash
# Pull image and verify digest
EXPECTED_DIGEST="sha256:abc123..."
docker pull ${IMAGE}
ACTUAL_DIGEST=$(docker inspect ${IMAGE} --format='{{index .RepoDigests 0}}' | cut -d'@' -f2)

if [ "$EXPECTED_DIGEST" != "$ACTUAL_DIGEST" ]; then
  echo "ERROR: Image digest mismatch. Potential supply chain attack."
  exit 1
fi
```

**Layer-by-layer audit trail** (`container_layer_manifest.json`):
```json
{
  "image": "ghcr.io/miac-research/wmh-nnunet:latest",
  "total_layers": 12,
  "base_image": "nvidia/cuda:12.1-cudnn8-runtime-ubuntu22.04",
  "layers": [
    {
      "layer_index": 0,
      "digest_sha256": "def456...",
      "size_bytes": 1234567,
      "instruction": "FROM nvidia/cuda:12.1-cudnn8-runtime-ubuntu22.04"
    },
    {
      "layer_index": 1,
      "digest_sha256": "ghi789...",
      "size_bytes": 567890,
      "instruction": "RUN apt-get update && apt-get install -y python3-dev..."
    }
  ],
  "final_image_hash": "sha256:abc123...",
  "verification_timestamp": "2026-04-05T14:20:00Z"
}
```

### Checkpoint & Resume with Container State

Long-running containerized tasks support state persistence:

```bash
# 1. Create checkpoint from running container
docker checkpoint create ${CONTAINER_ID} checkpoint_20260405_143000

# 2. Auto-saved checkpoint metadata
docker checkpoint ls ${CONTAINER_ID}  # Lists all available checkpoints

# 3. Resume from checkpoint (if host supports CRIU)
docker start --checkpoint checkpoint_20260405_143000 ${CONTAINER_ID}
```

## Important Notes & Limitations

- **User confirmation is mandatory** — no silent destructive actions
- All actual Docker commands are **delegated to `claw-shell`** for centralized logging and safety
- Large image pulls (e.g. nnU-Net models) → warn about size/time and disk space
- Common fixes (`chmod -R 777` on mounted directories, `newgrp docker`) are automatically included in plans
- Windows users are encouraged to use WSL2 + Docker Desktop for best compatibility
- GPU passthrough requires NVIDIA Container Toolkit (installed via `dependency-planner`)
- Rollback support: keep `docker-compose.yml` + image tags as backups

## When to Call This Skill

- Any request containing “docker”, “container”, “pull image”, “run with GPU”, “docker compose”, “prune”, “build Dockerfile”
- Before running Docker-based skills (wmh-segmentation, future containerized models)
- When `dependency-planner` detects missing Docker/NVIDIA toolkit
- Reproducibility, sharing, or team collaboration tasks involving containers

## Complementary / Related Skills

- `claw-shell` → **mandatory** safe execution of all Docker commands (tmux `claw` session)
- `dependency-planner` → install Docker Engine + NVIDIA Container Toolkit
- `multi-search-engine` → lookup latest Docker Hub / GitHub Container Registry instructions

## Reference

Custom interface-layer skill for NeuroClaw, addressing containerized environment setup gaps identified in the MedicalClaw / OpenClaw evaluation and aligned with 2026 Docker + NVIDIA best practices (GPU passthrough, compose reproducibility, claw-shell routing).

---
Created At: 2026-03-25 23:08 HKT  
Last Updated At: 2026-04-05 02:01 HKT 
Author: chengwang96