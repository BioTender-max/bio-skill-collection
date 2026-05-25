#!/usr/bin/env python3
"""Quick smoke test for the polars-dovmed skill."""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def parse_args():
    skill_dir = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="Run a quick end-to-end smoke test for the polars-dovmed skill"
    )
    parser.add_argument(
        "--run-dir",
        default=str(skill_dir / "runs" / "smoke-test"),
        help="Directory where prompt, query, payloads, responses, and summary will be saved",
    )
    parser.add_argument(
        "--prompt-file",
        default=str(skill_dir / "fixtures" / "smoke_prompt.txt"),
        help="Fixture prompt to copy into the run directory",
    )
    parser.add_argument(
        "--query-file",
        default=str(skill_dir / "fixtures" / "smoke_query.json"),
        help="Structured query JSON fixture to copy into the run directory",
    )
    parser.add_argument(
        "--details-pmc-id",
        default="3383453",
        help="Known PMC identifier used to validate paper-details lookup normalization",
    )
    parser.add_argument(
        "--base-url",
        default="https://api.newlineages.com",
        help="API base URL to test",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=3,
        help="Maximum discovery results to request",
    )
    parser.add_argument(
        "--expect-min-results",
        type=int,
        default=1,
        help="Minimum number of discovery papers expected for success",
    )
    return parser.parse_args()


def run_cli(args):
    cmd = [sys.executable, *args]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "cmd": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def load_json_from_stdout(run_result, label):
    if run_result["returncode"] != 0:
        raise SystemExit(
            f"{label} command failed with exit code {run_result['returncode']}:\n"
            f"{run_result['stderr'] or run_result['stdout']}"
        )
    try:
        return json.loads(run_result["stdout"])
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"{label} did not emit valid JSON.\nSTDOUT:\n{run_result['stdout']}\nSTDERR:\n{run_result['stderr']}"
        ) from exc


def save_text(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main():
    args = parse_args()
    skill_dir = Path(__file__).resolve().parents[1]
    run_dir = Path(args.run_dir).expanduser().resolve()
    run_dir.mkdir(parents=True, exist_ok=True)

    prompt_src = Path(args.prompt_file).expanduser().resolve()
    query_src = Path(args.query_file).expanduser().resolve()
    prompt_dst = run_dir / "prompt.txt"
    query_dst = run_dir / "query.json"
    prompt_dst.write_text(prompt_src.read_text(encoding="utf-8"), encoding="utf-8")
    query_dst.write_text(query_src.read_text(encoding="utf-8"), encoding="utf-8")

    query_script = skill_dir / "scripts" / "query_literature.py"

    discovery = run_cli(
        [
            str(query_script),
            "--queries-file",
            str(query_dst),
            "--mode",
            "discovery",
            "--max-results",
            str(args.max_results),
            "--base-url",
            args.base_url,
            "--save-payload",
            str(run_dir / "payload_discovery.json"),
            "--save-response",
            str(run_dir / "results_discovery.json"),
            "--raw",
        ]
    )
    save_text(run_dir / "discovery.stdout.json", discovery["stdout"])
    save_text(run_dir / "discovery.stderr.txt", discovery["stderr"])
    discovery_json = load_json_from_stdout(discovery, "discovery")

    details = run_cli(
        [
            str(query_script),
            "--details",
            args.details_pmc_id,
            "--base-url",
            args.base_url,
            "--save-payload",
            str(run_dir / "payload_details.json"),
            "--save-response",
            str(run_dir / "results_details.json"),
            "--raw",
        ]
    )
    save_text(run_dir / "details.stdout.json", details["stdout"])
    save_text(run_dir / "details.stderr.txt", details["stderr"])
    details_json = load_json_from_stdout(details, "details")

    papers = discovery_json.get("papers") or []
    checks = {
        "discovery_mode": discovery_json.get("mode") == "discovery",
        "discovery_strategy": discovery_json.get("strategy_used") in {"discovery", "discovery_fallback"},
        "discovery_elapsed_ms": isinstance(discovery_json.get("elapsed_ms"), int),
        "discovery_min_results": len(papers) >= args.expect_min_results,
        "discovery_has_signal_terms": bool(discovery_json.get("signal_terms")),
        "discovery_has_ranking": bool(papers) and isinstance(papers[0].get("ranking"), dict),
        "details_found": details_json.get("found", 0) >= 1,
        "details_normalized": args.details_pmc_id not in details_json.get("missing_ids", []),
        "details_has_normalized_ids": bool(details_json.get("normalized_pmc_ids")),
    }
    success = all(checks.values())

    summary = {
        "success": success,
        "base_url": args.base_url,
        "run_dir": str(run_dir),
        "prompt_path": str(prompt_dst),
        "query_path": str(query_dst),
        "checks": checks,
        "discovery": {
            "strategy_used": discovery_json.get("strategy_used"),
            "elapsed_ms": discovery_json.get("elapsed_ms"),
            "discovery_query": discovery_json.get("discovery_query"),
            "signal_terms": discovery_json.get("signal_terms"),
            "returned": discovery_json.get("returned"),
            "first_paper": (papers or [None])[0],
        },
        "details": {
            "requested": details_json.get("requested"),
            "normalized_requested": details_json.get("normalized_requested"),
            "normalized_pmc_ids": details_json.get("normalized_pmc_ids"),
            "found": details_json.get("found"),
            "missing_ids": details_json.get("missing_ids"),
        },
        "artifacts": {
            "payload_discovery": str(run_dir / "payload_discovery.json"),
            "results_discovery": str(run_dir / "results_discovery.json"),
            "payload_details": str(run_dir / "payload_details.json"),
            "results_details": str(run_dir / "results_details.json"),
            "summary": str(run_dir / "summary.json"),
        },
    }

    save_text(run_dir / "summary.json", json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    raise SystemExit(0 if success else 1)


if __name__ == "__main__":
    main()
