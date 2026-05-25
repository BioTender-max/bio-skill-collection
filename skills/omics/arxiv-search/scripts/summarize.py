#!/usr/bin/env python3
"""Write local Markdown summaries for arXiv IDs."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
import re

from search import fetch_results_by_ids


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch arXiv IDs and write local Markdown summary files."
    )
    parser.add_argument(
        "ids",
        nargs="+",
        help="One or more arXiv IDs. Comma-delimited values are also accepted.",
    )
    parser.add_argument(
        "--output-dir",
        default="arxiv-summaries",
        help="Directory for generated Markdown files (default: arxiv-summaries)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=20,
        help="Network timeout in seconds (default: 20)",
    )
    return parser


def split_ids(values: list[str]) -> list[str]:
    ids = []
    for value in values:
        ids.extend(part.strip() for part in value.split(","))
    return [paper_id for paper_id in ids if paper_id]


def safe_filename(arxiv_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", arxiv_id)


def join_authors(authors: list[str]) -> str:
    if not authors:
        return "Unknown"
    return ", ".join(authors)


def build_markdown(paper: dict[str, object]) -> str:
    arxiv_id = paper.get("arxiv_id") or "unknown"
    title = paper.get("title") or "Untitled"
    authors = join_authors(paper.get("authors") or [])
    published = paper.get("published") or "Unknown"
    updated = paper.get("updated") or "Unknown"
    primary_category = paper.get("primary_category") or "Unknown"
    categories = ", ".join(paper.get("categories") or []) or "Unknown"
    doi = paper.get("doi")
    journal_ref = paper.get("journal_ref")
    comment = paper.get("comment")
    abs_url = paper.get("abs_url") or ""
    pdf_url = paper.get("pdf_url") or ""
    abstract = paper.get("summary") or ""
    saved_at = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")

    lines = [
        f"# {title}",
        "",
        f"- arXiv ID: `{arxiv_id}`",
        f"- Authors: {authors}",
        f"- Published: {published}",
        f"- Updated: {updated}",
        f"- Primary category: {primary_category}",
        f"- Categories: {categories}",
    ]
    if doi:
        lines.append(f"- DOI: {doi}")
    if journal_ref:
        lines.append(f"- Journal reference: {journal_ref}")
    if comment:
        lines.append(f"- Comment: {comment}")
    if abs_url:
        lines.append(f"- Abstract page: {abs_url}")
    if pdf_url:
        lines.append(f"- PDF: {pdf_url}")
    lines.extend(
        [
            f"- Saved: {saved_at}",
            "",
            "## Abstract",
            "",
            abstract.strip(),
            "",
            "## Citation",
            "",
            f"{authors}. {title}. arXiv:{arxiv_id}.",
            "",
            "## Notes",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        ids = split_ids(args.ids)
        request_url, parsed = fetch_results_by_ids(ids, args.timeout)
        papers = parsed["results"]
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        written_files = []
        returned_ids = set()
        for paper in papers:
            arxiv_id = paper.get("arxiv_id")
            if not arxiv_id:
                continue
            returned_ids.add(arxiv_id)
            path = output_dir / f"{safe_filename(arxiv_id)}.md"
            if path.exists() and not args.force:
                raise FileExistsError(f"{path} already exists; rerun with --force to overwrite")
            path.write_text(build_markdown(paper), encoding="utf-8")
            written_files.append({"arxiv_id": arxiv_id, "path": str(path)})

        requested_ids = set(ids)
        missing_ids = sorted(requested_ids - returned_ids)
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"success": False, "error": str(exc)}, indent=2))
        return 1

    print(
        json.dumps(
            {
                "success": True,
                "type": "arxiv_markdown_summary",
                "request_url": request_url,
                "requested_ids": ids,
                "fetched_count": len(papers),
                "written_files": written_files,
                "missing_ids": missing_ids,
                "output_dir": str(Path(args.output_dir)),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
