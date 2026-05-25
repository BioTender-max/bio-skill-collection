#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JOURNAL_METRICS = SKILL_ROOT / "references" / "journal_metrics_2024.tsv"
DOI_PATTERN = re.compile(r"^10\.\d{4,}/\S+$", re.IGNORECASE)


def normalize_doi(raw_doi: str) -> str:
    doi = raw_doi.strip()
    doi = re.sub(r"^doi:\s*", "", doi, flags=re.IGNORECASE)
    doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi, flags=re.IGNORECASE)
    if not DOI_PATTERN.match(doi):
        raise ValueError(f"Invalid DOI: {raw_doi}")
    return doi


def normalize_openalex_id(raw_id: str) -> str:
    candidate = raw_id.strip()
    if candidate.startswith("https://openalex.org/"):
        candidate = candidate.rsplit("/", 1)[-1]
    if not re.fullmatch(r"W\d+", candidate):
        raise ValueError(f"Invalid OpenAlex ID: {raw_id}")
    return candidate


def normalize_name(value: str) -> str:
    lowered = value.casefold()
    lowered = lowered.replace("&", " and ")
    lowered = re.sub(r"[^a-z0-9]+", " ", lowered)
    return " ".join(lowered.split())


def fetch_json(url: str, headers: dict[str, str] | None = None) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "scientific-impact-assessment/1.0 (+https://github.com/fschulz/omics-skills)",
            **(headers or {}),
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def openalex_url_from_args(doi: str | None, openalex_id: str | None, mailto: str | None) -> str:
    base = "https://api.openalex.org/works"
    if doi:
        target = f"https://doi.org/{doi}"
        path = urllib.parse.quote(target, safe=":/")
    else:
        path = normalize_openalex_id(openalex_id or "")
    url = f"{base}/{path}"
    if mailto:
        url = f"{url}?{urllib.parse.urlencode({'mailto': mailto})}"
    return url


def fetch_openalex_work(doi: str | None, openalex_id: str | None, mailto: str | None) -> dict[str, Any]:
    return fetch_json(openalex_url_from_args(doi=doi, openalex_id=openalex_id, mailto=mailto))


def parse_openalex_work(payload: dict[str, Any]) -> dict[str, Any]:
    ids = payload.get("ids") or {}
    primary_source = ((payload.get("primary_location") or {}).get("source") or {})
    doi = ids.get("doi") or payload.get("doi")
    normalized_doi = normalize_doi(doi) if doi else None
    percentile = payload.get("cited_by_percentile_year") or {}
    return {
        "openalex_id": ids.get("openalex") or payload.get("id"),
        "doi": normalized_doi,
        "title": payload.get("display_name"),
        "publication_year": payload.get("publication_year"),
        "cited_by_count": payload.get("cited_by_count"),
        "citation_percentile_min": percentile.get("min"),
        "citation_percentile_max": percentile.get("max"),
        "counts_by_year": payload.get("counts_by_year") or [],
        "journal_name": primary_source.get("display_name"),
        "journal_issn_l": primary_source.get("issn_l"),
        "type": payload.get("type"),
    }


def load_journal_metrics(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            aliases = [item.strip() for item in (row.get("aliases") or "").split("|") if item.strip()]
            row["aliases"] = aliases
            row["value"] = float(row["value"])
            rows.append(row)
    return rows


def lookup_journal_metric(journal_metrics: list[dict[str, Any]], journal_name: str | None) -> dict[str, Any]:
    if not journal_name:
        return {"matched": False, "reason": "no_journal_name"}
    query = normalize_name(journal_name)
    for row in journal_metrics:
        candidates = [row["journal_name"], *row["aliases"]]
        if any(normalize_name(candidate) == query for candidate in candidates):
            return {
                "matched": True,
                "journal_name": row["journal_name"],
                "category": row["category"],
                "metric_name": row["metric_name"],
                "metric_year": int(row["metric_year"]),
                "value": row["value"],
                "source_url": row["source_url"],
                "source_kind": row["source_kind"],
                "verified_date": row["verified_date"],
                "notes": row["notes"],
            }
    return {"matched": False, "reason": "not_in_reference_table", "query": journal_name}


def summarize_altmetric_payload(payload: dict[str, Any] | None, reason: str | None = None) -> dict[str, Any]:
    if payload is None:
        return {"status": "unavailable", "reason": reason or "not_requested"}
    return {
        "status": "available",
        "score": payload.get("score"),
        "journal": payload.get("journal"),
        "details_url": payload.get("details_url") or payload.get("url"),
        "cited_by_posts_count": payload.get("cited_by_posts_count"),
        "cited_by_news_outlets_count": payload.get("cited_by_msm_count"),
        "cited_by_tweeters_count": payload.get("cited_by_tweeters_count"),
        "cited_by_policies_count": payload.get("cited_by_policies_count"),
        "cited_by_patents_count": payload.get("cited_by_patents_count"),
        "readers_count": payload.get("readers_count"),
    }


def fetch_altmetric_summary(doi: str | None, api_key: str | None) -> dict[str, Any]:
    if not doi:
        return summarize_altmetric_payload(None, reason="doi_required")
    if not api_key:
        return summarize_altmetric_payload(None, reason="no_api_key")
    encoded_doi = urllib.parse.quote(doi, safe="")
    url = f"https://api.altmetric.com/v1/doi/{encoded_doi}?{urllib.parse.urlencode({'key': api_key})}"
    try:
        payload = fetch_json(url)
    except urllib.error.HTTPError as exc:
        return summarize_altmetric_payload(None, reason=f"http_{exc.code}")
    except urllib.error.URLError:
        return summarize_altmetric_payload(None, reason="network_error")
    return summarize_altmetric_payload(payload)


def build_report_from_payloads(
    openalex_payload: dict[str, Any],
    journal_metrics: list[dict[str, Any]],
    *,
    altmetric_payload: dict[str, Any] | None = None,
    altmetric_reason: str | None = None,
) -> dict[str, Any]:
    openalex_summary = parse_openalex_work(openalex_payload)
    journal_metric = lookup_journal_metric(journal_metrics, openalex_summary.get("journal_name"))
    altmetric_summary = summarize_altmetric_payload(altmetric_payload, reason=altmetric_reason)
    return {
        "openalex": openalex_summary,
        "altmetric": altmetric_summary,
        "journal_metric": journal_metric,
    }


def build_live_report(args: argparse.Namespace) -> dict[str, Any]:
    doi = normalize_doi(args.doi) if args.doi else None
    openalex_id = normalize_openalex_id(args.openalex_id) if args.openalex_id else None
    journal_metrics = load_journal_metrics(Path(args.journal_metrics))
    openalex_payload = fetch_openalex_work(doi=doi, openalex_id=openalex_id, mailto=args.mailto)
    altmetric_summary = fetch_altmetric_summary(doi=doi, api_key=args.altmetric_api_key)
    openalex_summary = parse_openalex_work(openalex_payload)
    journal_metric = lookup_journal_metric(journal_metrics, openalex_summary.get("journal_name"))
    return {
        "openalex": openalex_summary,
        "altmetric": altmetric_summary,
        "journal_metric": journal_metric,
    }


def format_text(report: dict[str, Any]) -> str:
    openalex = report["openalex"]
    journal_metric = report["journal_metric"]
    altmetric = report["altmetric"]
    lines = [
        f"Title: {openalex.get('title') or 'n/a'}",
        f"DOI: {openalex.get('doi') or 'n/a'}",
        f"OpenAlex ID: {openalex.get('openalex_id') or 'n/a'}",
        f"Publication year: {openalex.get('publication_year') or 'n/a'}",
        f"Cited by count: {openalex.get('cited_by_count')}",
        f"Journal: {openalex.get('journal_name') or 'n/a'}",
    ]
    if journal_metric.get("matched"):
        lines.append(
            f"Journal impact factor ({journal_metric['metric_year']}): {journal_metric['value']} [{journal_metric['source_kind']}]"
        )
    else:
        lines.append(f"Journal impact factor: unavailable ({journal_metric.get('reason')})")
    if altmetric.get("status") == "available":
        lines.append(f"Altmetric score: {altmetric.get('score')}")
    else:
        lines.append(f"Altmetric: unavailable ({altmetric.get('reason')})")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Assess publication impact with OpenAlex, optional Altmetric, and journal metrics.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--doi", help="DOI for the work to assess")
    group.add_argument("--openalex-id", help="OpenAlex work ID, e.g. W2741809807")
    parser.add_argument(
        "--mailto",
        default=os.environ.get("OPENALEX_MAILTO"),
        help="Email for OpenAlex polite-pool usage",
    )
    parser.add_argument(
        "--altmetric-api-key",
        default=os.environ.get("ALTMETRIC_API_KEY"),
        help="Altmetric Details Page API key",
    )
    parser.add_argument(
        "--journal-metrics",
        default=str(DEFAULT_JOURNAL_METRICS),
        help="Path to the curated journal metrics TSV",
    )
    parser.add_argument("--format", choices=("json", "text"), default="json")
    parser.add_argument("--output", help="Write output to a file instead of stdout")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        report = build_live_report(args)
    except Exception as exc:  # pragma: no cover - exercised through CLI failure paths
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    rendered = json.dumps(report, indent=2) if args.format == "json" else format_text(report)
    if args.output:
        Path(args.output).write_text(rendered + ("\n" if not rendered.endswith("\n") else ""), encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
