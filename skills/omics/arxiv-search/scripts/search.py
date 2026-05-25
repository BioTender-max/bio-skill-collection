#!/usr/bin/env python3
"""Search arXiv through the official API and emit normalized JSON."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


API_URL = "https://export.arxiv.org/api/query"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
USER_AGENT = "omics-skills-arxiv-search/1.0 (+https://github.com/fschulz/omics-skills)"
DEFAULT_MIN_INTERVAL_SECONDS = 3.1
DEFAULT_RETRIES = 2
DEFAULT_RETRY_BACKOFF_SECONDS = 60.0
RAW_QUERY_HINTS = (
    "ti:",
    "au:",
    "abs:",
    "co:",
    "jr:",
    "cat:",
    "rn:",
    "all:",
    "submittedDate:",
    "AND",
    "OR",
    "ANDNOT",
    "(",
    ")",
    "[",
    "]",
)


class ArxivHTTPError(RuntimeError):
    """HTTP error with enough metadata for retry handling."""

    def __init__(self, code: int, body: str, retry_after: str | None = None) -> None:
        super().__init__(f"HTTP {code} from arXiv API: {body}")
        self.code = code
        self.body = body
        self.retry_after = retry_after


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Search arXiv via the official API and print normalized JSON."
    )
    parser.add_argument("query", nargs="?", help="Plain-text query or raw arXiv search_query")
    parser.add_argument(
        "max_results",
        nargs="?",
        type=int,
        default=10,
        help="Number of results to request (default: 10)",
    )
    parser.add_argument(
        "--phrase",
        action="store_true",
        help="Treat the plain-text query as a single phrase",
    )
    parser.add_argument(
        "--category",
        help="Restrict results to an arXiv subject category, for example cs.LG",
    )
    parser.add_argument(
        "--days",
        type=int,
        help="Restrict to papers submitted within the last N days (UTC)",
    )
    parser.add_argument(
        "--sort",
        choices=("relevance", "lastUpdatedDate", "submittedDate"),
        default="relevance",
        help="Sort field (default: relevance)",
    )
    parser.add_argument(
        "--order",
        choices=("ascending", "descending"),
        default="descending",
        help="Sort order (default: descending)",
    )
    parser.add_argument(
        "--start",
        type=int,
        default=0,
        help="0-based result offset (default: 0)",
    )
    parser.add_argument(
        "--ids",
        help="Comma-delimited arXiv IDs to fetch directly",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=20,
        help="Network timeout in seconds (default: 20)",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=None,
        help="Directory for arXiv API response cache and pacing state",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable response-cache reads and writes; pacing still applies",
    )
    parser.add_argument(
        "--min-interval",
        type=float,
        default=DEFAULT_MIN_INTERVAL_SECONDS,
        help="Minimum seconds between arXiv API calls across invocations (default: 3.1)",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=DEFAULT_RETRIES,
        help="Number of retries for HTTP 429 responses (default: 2)",
    )
    parser.add_argument(
        "--retry-backoff",
        type=float,
        default=DEFAULT_RETRY_BACKOFF_SECONDS,
        help="Base seconds to wait after HTTP 429 when Retry-After is absent (default: 60)",
    )
    return parser


def compact_whitespace(text: str) -> str:
    return " ".join(text.split())


def is_raw_query(query: str) -> bool:
    return any(token in query for token in RAW_QUERY_HINTS)


def quote_term(term: str) -> str:
    escaped = term.replace("\\", "\\\\").replace('"', '\\"')
    if re.search(r"\s", escaped):
        return f'"{escaped}"'
    return escaped


def compile_plain_query(query: str, phrase: bool) -> str:
    text = compact_whitespace(query)
    if not text:
        raise ValueError("query must not be empty")
    if phrase:
        return f"all:{quote_term(text)}"
    return " AND ".join(f"all:{quote_term(token)}" for token in text.split())


def parse_arxiv_timestamp(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    try:
        return dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=dt.timezone.utc
        )
    except ValueError:
        return None


def apply_local_days_filter(
    results: list[dict[str, object]], days: int | None
) -> tuple[list[dict[str, object]], dict[str, object] | None]:
    if days is None:
        return results, None
    if days <= 0:
        raise ValueError("--days must be a positive integer")

    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)
    filtered = []
    excluded = 0
    undated = 0

    for result in results:
        published = parse_arxiv_timestamp(result.get("published"))
        if published is None:
            undated += 1
            continue
        if published >= cutoff:
            filtered.append(result)
        else:
            excluded += 1

    metadata = {
        "mode": "local_published_date",
        "days": days,
        "cutoff_utc": cutoff.isoformat(timespec="seconds"),
        "pre_filter_result_count": len(results),
        "post_filter_result_count": len(filtered),
        "excluded_older_count": excluded,
        "excluded_undated_count": undated,
    }
    return filtered, metadata


def compile_search_query(args: argparse.Namespace) -> str | None:
    if args.ids:
        return None
    if not args.query:
        raise ValueError("query is required unless --ids is provided")

    compiled = args.query if is_raw_query(args.query) else compile_plain_query(args.query, args.phrase)

    filters = []
    if args.category:
        filters.append(f"cat:{args.category}")

    if filters:
        compiled = f"{compiled} AND " + " AND ".join(filters)

    return compiled


def build_params(args: argparse.Namespace, compiled_query: str | None) -> dict[str, str]:
    if args.max_results < 1:
        raise ValueError("max_results must be >= 1")
    if args.max_results > 2000:
        raise ValueError("max_results must be <= 2000 per API call")
    if args.start < 0:
        raise ValueError("--start must be >= 0")

    params = {
        "start": str(args.start),
        "max_results": str(args.max_results),
        "sortBy": args.sort,
        "sortOrder": args.order,
    }
    if args.ids:
        params["id_list"] = args.ids
    if compiled_query:
        params["search_query"] = compiled_query
    return params


def fetch_results_by_ids(
    ids: list[str],
    timeout: int,
    cache_dir: Path,
    no_cache: bool,
    min_interval: float,
    retries: int,
    retry_backoff: float,
) -> tuple[str, dict[str, object]]:
    unique_ids = []
    seen = set()
    for raw_id in ids:
        paper_id = compact_whitespace(raw_id.strip().strip(","))
        if not paper_id or paper_id in seen:
            continue
        seen.add(paper_id)
        unique_ids.append(paper_id)
    if not unique_ids:
        raise ValueError("at least one arXiv ID is required")

    args = argparse.Namespace(
        max_results=len(unique_ids),
        start=0,
        sort="relevance",
        order="descending",
        ids=",".join(unique_ids),
    )
    params = build_params(args, None)
    request_url, xml_text = fetch_feed(
        params,
        timeout,
        cache_dir=cache_dir,
        no_cache=no_cache,
        min_interval=min_interval,
        retries=retries,
        retry_backoff=retry_backoff,
    )
    return request_url, parse_feed(xml_text)


def default_cache_dir() -> Path:
    override = os.environ.get("ARXIV_SEARCH_CACHE_DIR")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".cache" / "omics-skills" / "arxiv-search"


def cache_path(cache_dir: Path, request_url: str) -> Path:
    digest = hashlib.sha256(request_url.encode("utf-8")).hexdigest()
    return cache_dir / "responses" / f"{digest}.xml"


def wait_for_pacing(cache_dir: Path, min_interval: float) -> None:
    if min_interval <= 0:
        return
    cache_dir.mkdir(parents=True, exist_ok=True)
    state_path = cache_dir / "last_request_unix.txt"
    now = time.time()
    try:
        last_request = float(state_path.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        last_request = None
    if last_request is not None:
        delay = min_interval - (now - last_request)
        if delay > 0:
            time.sleep(delay)
    state_path.write_text(f"{time.time():.6f}\n", encoding="utf-8")


def parse_retry_after(value: str | None) -> float | None:
    if not value:
        return None
    try:
        seconds = float(value)
    except ValueError:
        return None
    return seconds if seconds >= 0 else None


def fetch_url_once(request_url: str, timeout: int) -> str:
    request = urllib.request.Request(request_url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise ArxivHTTPError(
            exc.code,
            body,
            retry_after=exc.headers.get("Retry-After"),
        ) from exc


def fetch_feed(
    params: dict[str, str],
    timeout: int,
    cache_dir: Path,
    no_cache: bool,
    min_interval: float,
    retries: int,
    retry_backoff: float,
) -> tuple[str, str]:
    query_string = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    request_url = f"{API_URL}?{query_string}"
    response_cache_path = cache_path(cache_dir, request_url)

    if not no_cache:
        try:
            return request_url, response_cache_path.read_text(encoding="utf-8")
        except OSError:
            pass

    attempts = max(0, retries) + 1
    for attempt in range(attempts):
        wait_for_pacing(cache_dir, min_interval)
        try:
            xml_text = fetch_url_once(request_url, timeout)
        except ArxivHTTPError as exc:
            if exc.code == 429 and attempt + 1 < attempts:
                delay = parse_retry_after(exc.retry_after)
                if delay is None:
                    delay = retry_backoff * (2**attempt)
                time.sleep(delay)
                continue
            raise RuntimeError(str(exc)) from exc

        if not no_cache:
            response_cache_path.parent.mkdir(parents=True, exist_ok=True)
            response_cache_path.write_text(xml_text, encoding="utf-8")
        return request_url, xml_text

    raise RuntimeError("arXiv API request failed after retry loop")


def text_or_none(parent: ET.Element, path: str) -> str | None:
    node = parent.find(path, ATOM_NS)
    if node is None or node.text is None:
        return None
    value = compact_whitespace(node.text)
    return value or None


def parse_result(entry: ET.Element) -> dict[str, object]:
    categories = [
        category.attrib["term"]
        for category in entry.findall("atom:category", ATOM_NS)
        if category.attrib.get("term")
    ]
    pdf_url = None
    abs_url = text_or_none(entry, "atom:id")

    for link in entry.findall("atom:link", ATOM_NS):
        href = link.attrib.get("href")
        title = link.attrib.get("title")
        rel = link.attrib.get("rel")
        if title == "pdf" and href:
            pdf_url = href
        elif rel == "alternate" and href:
            abs_url = href

    result = {
        "title": text_or_none(entry, "atom:title"),
        "summary": text_or_none(entry, "atom:summary"),
        "authors": [
            compact_whitespace(node.text)
            for node in entry.findall("atom:author/atom:name", ATOM_NS)
            if node.text
        ],
        "arxiv_id": (abs_url or "").rstrip("/").split("/")[-1] or None,
        "abs_url": abs_url,
        "pdf_url": pdf_url,
        "published": text_or_none(entry, "atom:published"),
        "updated": text_or_none(entry, "atom:updated"),
        "primary_category": (
            entry.find("arxiv:primary_category", ATOM_NS).attrib.get("term")
            if entry.find("arxiv:primary_category", ATOM_NS) is not None
            else None
        ),
        "categories": categories,
        "comment": text_or_none(entry, "arxiv:comment"),
        "journal_ref": text_or_none(entry, "arxiv:journal_ref"),
        "doi": text_or_none(entry, "arxiv:doi"),
    }
    return result


def parse_feed(xml_text: str) -> dict[str, object]:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        raise RuntimeError(f"Failed to parse arXiv Atom response: {exc}") from exc

    entries = [parse_result(entry) for entry in root.findall("atom:entry", ATOM_NS)]
    total_results = root.findtext("{http://a9.com/-/spec/opensearch/1.1/}totalResults")
    start_index = root.findtext("{http://a9.com/-/spec/opensearch/1.1/}startIndex")
    items_per_page = root.findtext("{http://a9.com/-/spec/opensearch/1.1/}itemsPerPage")

    return {
        "feed_updated": text_or_none(root, "atom:updated"),
        "total_results": int(total_results) if total_results else None,
        "start_index": int(start_index) if start_index else None,
        "items_per_page": int(items_per_page) if items_per_page else None,
        "results": entries,
    }


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        cache_dir = args.cache_dir or default_cache_dir()
        if args.min_interval < 0:
            raise ValueError("--min-interval must be >= 0")
        if args.retries < 0:
            raise ValueError("--retries must be >= 0")
        if args.retry_backoff < 0:
            raise ValueError("--retry-backoff must be >= 0")
        compiled_query = compile_search_query(args)
        params = build_params(args, compiled_query)
        request_url, xml_text = fetch_feed(
            params,
            args.timeout,
            cache_dir=cache_dir,
            no_cache=args.no_cache,
            min_interval=args.min_interval,
            retries=args.retries,
            retry_backoff=args.retry_backoff,
        )
        parsed = parse_feed(xml_text)
        filtered_results, days_filter = apply_local_days_filter(parsed["results"], args.days)
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"success": False, "error": str(exc)}, indent=2))
        return 1

    warnings = []
    if days_filter is not None:
        warnings.append(
            "Applied --days as a local published-date filter because arXiv "
            "submittedDate queries were observed returning HTTP 500 on 2026-03-18 UTC."
        )
        if args.sort != "submittedDate" or args.order != "descending":
            warnings.append(
                "For best recent-paper recall with --days, prefer "
                "--sort submittedDate --order descending."
            )

    response = {
        "success": True,
        "type": "arxiv_search",
        "query": args.query,
        "compiled_query": compiled_query,
        "query_mode": (
            "id_list"
            if args.ids
            else "raw"
            if args.query and is_raw_query(args.query)
            else "plain_text"
        ),
        "id_list": args.ids,
        "start": args.start,
        "max_results": args.max_results,
        "sort_by": args.sort,
        "sort_order": args.order,
        "timeout_seconds": args.timeout,
        "cache_dir": str(cache_dir),
        "cache_enabled": not args.no_cache,
        "min_interval_seconds": args.min_interval,
        "retries": args.retries,
        "retry_backoff_seconds": args.retry_backoff,
        "request_url": request_url,
        "feed_updated": parsed["feed_updated"],
        "total_results": parsed["total_results"],
        "start_index": parsed["start_index"],
        "items_per_page": parsed["items_per_page"],
        "days_filter": days_filter,
        "warnings": warnings,
        "result_count": len(filtered_results),
        "results": filtered_results,
    }
    print(json.dumps(response, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
