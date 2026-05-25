#!/usr/bin/env python3
"""Aggregate and rank AI scientist evaluation JSON files.

Usage:
    python scripts/aggregate_reviews.py review1.json review2.json --out_md leaderboard.md
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


def load_review(path: Path) -> Dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if "overall" not in data or "total_score_100" not in data["overall"]:
        raise ValueError(f"{path} is missing overall.total_score_100")
    return data


def category_score(data: Dict[str, Any], names: Tuple[str, ...]) -> float:
    for item in data.get("scores", []):
        if item.get("category") in names:
            try:
                return float(item.get("weighted_points", 0))
            except (TypeError, ValueError):
                return 0.0
    return 0.0


def gate_fail_count(data: Dict[str, Any]) -> int:
    return sum(1 for item in data.get("gate_checks", []) if item.get("status") == "fail")


def red_flag_count(data: Dict[str, Any]) -> int:
    return len(data.get("red_flags", []))


def sort_key(data: Dict[str, Any]) -> Tuple[float, float, float, float, float]:
    total = float(data["overall"].get("total_score_100", 0))
    task = category_score(data, ("task_completion",))
    repro = category_score(data, ("reproducibility",))
    validation = category_score(data, ("validation_robustness", "benchmarking"))
    penalties = gate_fail_count(data) + red_flag_count(data)
    return (total, task, repro, validation, -penalties)


def format_markdown(reviews: List[Tuple[Path, Dict[str, Any]]]) -> str:
    lines = []
    lines.append("# AI Scientist Leaderboard")
    lines.append("")
    lines.append("| Rank | Submission | Scientist | Score | Recommendation | Gate fails | Red flags |")
    lines.append("|---:|---|---|---:|---|---:|---:|")
    for idx, (path, data) in enumerate(reviews, start=1):
        submission = data.get("submission_id", path.stem)
        scientist = data.get("scientist_name", "")
        score = float(data["overall"].get("total_score_100", 0))
        recommendation = data["overall"].get("recommendation", "")
        lines.append(
            f"| {idx} | {submission} | {scientist} | {score:.1f} | {recommendation} | {gate_fail_count(data)} | {red_flag_count(data)} |"
        )
    lines.append("")
    if reviews:
        winner = reviews[0][1]
        lines.append("## Winner")
        lines.append("")
        lines.append(
            f"{winner.get('submission_id', reviews[0][0].stem)} "
            f"({winner.get('scientist_name', '').strip()}) ranks first with "
            f"{float(winner['overall'].get('total_score_100', 0)):.1f}/100."
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate and rank AI scientist evaluation JSON files")
    parser.add_argument("reviews", nargs="+", help="Paths to evaluation JSON files")
    parser.add_argument("--out_md", help="Optional markdown output path")
    args = parser.parse_args()

    loaded: List[Tuple[Path, Dict[str, Any]]] = []
    for review_path in args.reviews:
        path = Path(review_path)
        loaded.append((path, load_review(path)))

    loaded.sort(key=lambda item: sort_key(item[1]), reverse=True)
    markdown = format_markdown(loaded)
    print(markdown)

    if args.out_md:
        Path(args.out_md).write_text(markdown, encoding="utf-8")


if __name__ == "__main__":
    main()
