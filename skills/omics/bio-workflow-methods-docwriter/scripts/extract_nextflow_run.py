#!/usr/bin/env python3
"""Extract a minimal run manifest from Nextflow `trace.txt` + `work/` directory.

This script is intentionally conservative:
- It reads task rows from `trace.txt`.
- It maps each `hash` (e.g., `45/ab752a`) to `work/<hash>/`.
- It reads `.command.sh` when present and embeds it into the manifest.
- It does NOT guess tool versions.

Usage:
  python scripts/extract_nextflow_run.py --trace trace.txt --workdir work --out run_manifest.yaml \
      --pipeline-name rnaseq --commit-sha <sha> --launch-command "nextflow run ..."

"""

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

import yaml


def sniff_dialect(path: Path) -> csv.Dialect:
    sample = path.read_text(errors='ignore')[:4096]
    try:
        return csv.Sniffer().sniff(sample, delimiters=[',', '\t'])
    except Exception:
        # Nextflow trace is often tab-separated; fall back to tab.
        class Tab(csv.Dialect):
            delimiter = '\t'
            quotechar = '"'
            escapechar = None
            doublequote = True
            skipinitialspace = False
            lineterminator = '\n'
            quoting = csv.QUOTE_MINIMAL
        return Tab()


def read_command(work_task_dir: Path) -> Optional[str]:
    for fname in ['.command.sh', '.command.run', '.command.bash']:
        p = work_task_dir / fname
        if p.exists():
            return p.read_text(errors='ignore')
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--trace', required=True, type=Path, help='Nextflow trace file (e.g., trace.txt)')
    ap.add_argument('--workdir', required=True, type=Path, help='Nextflow work directory (e.g., work/)')
    ap.add_argument('--out', required=True, type=Path, help='Output manifest path (.yaml or .json)')
    ap.add_argument('--pipeline-name', required=True, help='Pipeline name')
    ap.add_argument('--pipeline-version', default='', help='Pipeline version (tag) if known')
    ap.add_argument('--repo-url', default='', help='Repo URL if known')
    ap.add_argument('--commit-sha', default='', help='Commit SHA if known')
    ap.add_argument('--engine-version', default='', help='Nextflow version if known')
    ap.add_argument('--launch-command', default='', help='Exact nextflow launch command (quoted)')

    args = ap.parse_args()

    dialect = sniff_dialect(args.trace)
    with args.trace.open(newline='', errors='ignore') as f:
        reader = csv.DictReader(f, dialect=dialect)
        rows = list(reader)

    steps: List[Dict[str, Any]] = []
    for i, row in enumerate(rows, start=1):
        task_hash = (row.get('hash') or '').strip()
        task_name = (row.get('name') or '').strip() or f'task_{i}'
        work_task_dir = args.workdir / task_hash if task_hash else None

        cmd = None
        workdir_str = ''
        if work_task_dir and work_task_dir.exists():
            workdir_str = str(work_task_dir)
            cmd = read_command(work_task_dir)

        steps.append({
            'step_id': f'nf-task-{i}',
            'name': task_name,
            'status': (row.get('status') or '').strip(),
            'exit_code': (row.get('exit') or '').strip(),
            'workdir': workdir_str,
            'command': cmd or 'NOT CAPTURED',
            'resources': {
                'duration': row.get('duration'),
                'realtime': row.get('realtime'),
                'cpu_pct': row.get('%cpu'),
                'peak_rss': row.get('peak_rss'),
                'peak_vmem': row.get('peak_vmem'),
            }
        })

    manifest: Dict[str, Any] = {
        'run_id': 'NOT CAPTURED',
        'workflow_summary': '',
        'workflow': {
            'engine': 'nextflow',
            'engine_version': args.engine_version,
            'pipeline': {
                'name': args.pipeline_name,
                'version': args.pipeline_version,
                'repo_url': args.repo_url,
                'commit_sha': args.commit_sha,
                'launch_command': args.launch_command,
            },
            'execution': {
                'workdir': str(args.workdir),
            }
        },
        'steps': steps,
        'outputs': [],
        'evidence': [str(args.trace), str(args.workdir)]
    }

    if args.out.suffix.lower() in {'.yml', '.yaml'}:
        args.out.write_text(yaml.safe_dump(manifest, sort_keys=False))
    else:
        args.out.write_text(json.dumps(manifest, indent=2))

    print(f"Wrote: {args.out}")


if __name__ == '__main__':
    main()
