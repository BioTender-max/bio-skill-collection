#!/usr/bin/env python3
"""Small helper for grouped polars-dovmed literature queries."""

import argparse
import copy
import concurrent.futures
import json
import os
import re
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

ASYNC_ENDPOINTS = {
    "/api/search_literature": "search_literature",
    "/api/scan_literature_advanced": "scan_literature_advanced",
}
SUPPORT_CONCEPT_TOKENS = (
    "host",
    "hosts",
    "infect",
    "infection",
    "interact",
    "interaction",
    "symbio",
    "pathway",
    "metab",
    "association",
    "range",
)
GENERIC_SUPPORT_TERMS = {
    "host",
    "hosts",
    "infect",
    "infects",
    "infected",
    "infection",
    "infections",
    "amoeba",
    "amoebae",
    "protist",
    "protists",
    "microeukaryote",
    "microeukaryotes",
    "symbiont",
    "symbionts",
    "association",
    "associations",
    "range",
}
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?;:])\s+|\n+")
MAX_SENTENCE_CONTEXT_CHARS = 450
WINDOW_WORDS = 80
WINDOW_STRIDE = 40
FULLTEXT_CONTEXT_RADIUS = 260
MAX_TERM_SPANS_PER_TERM = 4
MAX_FULLTEXT_CONTEXTS = 36
CONTEXT_SNIPPET_CHARS = 240
DEFAULT_LOCAL_REPO = str(Path("~/dev/polars-dovmed").expanduser())
CLEAN_YEAR_BANDS = ("2024_plus", "2021_2023", "2010_2020", "pre_2010")
RECENT_YEAR_BANDS = ("2024_plus", "2021_2023")
YEAR_BAND_ALIASES = {
    "pre_2010": "pre_2010",
    "pre-2010": "pre_2010",
    "pre2010": "pre_2010",
    "before_2010": "pre_2010",
    "before-2010": "pre_2010",
    "2010_2020": "2010_2020",
    "2010-2020": "2010_2020",
    "2010_to_2020": "2010_2020",
    "2010to2020": "2010_2020",
    "2021_2023": "2021_2023",
    "2021-2023": "2021_2023",
    "2021_to_2023": "2021_2023",
    "2021to2023": "2021_2023",
    "2024_plus": "2024_plus",
    "2024+": "2024_plus",
    "post_2023": "2024_plus",
    "post-2023": "2024_plus",
    "after_2023": "2024_plus",
    "after-2023": "2024_plus",
    "since_2024": "2024_plus",
    "post_2020": "post_2020",
    "post-2020": "post_2020",
    "post2020": "post_2020",
    "after_2020": "post_2020",
    "after-2020": "post_2020",
    "recent": "post_2020",
}


def load_env_file(path):
    env_path = Path(path).expanduser()
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def normalize_year_band(value):
    normalized = str(value).strip().lower()
    if not normalized or normalized == "all":
        return None
    if normalized == "clean_split":
        return "clean_split"
    if normalized == "recent_split":
        return "recent_split"
    if normalized not in YEAR_BAND_ALIASES:
        allowed = ", ".join(sorted(set(YEAR_BAND_ALIASES.values()) | {"clean_split", "recent_split"}))
        raise ValueError(f"unsupported year band '{value}'. Use one of: {allowed}")
    return YEAR_BAND_ALIASES[normalized]


def parse_year_bands(values):
    bands = []
    for raw_value in values or []:
        for item in str(raw_value).split(","):
            normalized = normalize_year_band(item)
            if normalized == "clean_split":
                bands.extend(CLEAN_YEAR_BANDS)
            elif normalized == "recent_split":
                bands.extend(RECENT_YEAR_BANDS)
            elif normalized:
                bands.append(normalized)
    deduped = []
    for band in bands:
        if band not in deduped:
            deduped.append(band)
    return deduped


def parse_args():
    load_env_file("~/.config/polars-dovmed/.env")
    parser = argparse.ArgumentParser()
    parser.add_argument("--query")
    parser.add_argument(
        "--allow-flat-query",
        action="store_true",
        help="Explicitly allow exploratory free-text search via /api/search_literature",
    )
    parser.add_argument("--queries-file")
    parser.add_argument("--group", action="append", default=[])
    parser.add_argument("--details", nargs="+")
    parser.add_argument(
        "--mode",
        choices=["advanced", "discovery"],
        default="discovery",
        help="Structured-search mode for --queries-file/--group. Default is discovery for fast candidate retrieval.",
    )
    parser.add_argument("--max-results", type=int, default=25)
    parser.add_argument("--fast-mode", action="store_true")
    parser.add_argument(
        "--search-columns",
        default="title,abstract_text,full_text",
        help="Comma-separated columns for advanced structured search",
    )
    parser.add_argument(
        "--extract-matches",
        choices=["primary", "secondary", "both", "none"],
        default="none",
        help="Extraction mode for advanced structured search",
    )
    parser.add_argument(
        "--add-group-counts",
        choices=["primary", "secondary", "both"],
        default="primary",
        help="Group-count mode for advanced structured search",
    )
    parser.add_argument("--year", type=int)
    parser.add_argument(
        "--year-band",
        choices=[
            "all",
            "pre_2010",
            "2010_2020",
            "post_2020",
            "2021_2023",
            "2024_plus",
        ],
        default="all",
        help="Restrict API/local search to a materialized publication-year band.",
    )
    parser.add_argument(
        "--year-bands",
        action="append",
        default=[],
        help=(
            "Fan one API query out over multiple materialized year bands in parallel. "
            "Use a comma-separated list such as 2024_plus,2021_2023 or the presets "
            "recent_split and clean_split."
        ),
    )
    parser.add_argument(
        "--year-band-workers",
        type=int,
        default=2,
        help="Maximum concurrent hosted API jobs for --year-bands.",
    )
    parser.add_argument("--timeout", type=int)
    parser.add_argument("--base-url", default="https://api.newlineages.com")
    parser.add_argument("--api-key")
    parser.add_argument(
        "--corpus",
        choices=["pmc", "biorxiv", "both"],
        help="Corpus selector for hosted API requests and local scans.",
    )
    parser.add_argument(
        "--execution-mode",
        choices=["auto", "api", "local"],
        default="auto",
        help="Use the hosted API or force a local parquet-backed scan.",
    )
    parser.add_argument(
        "--local-corpus",
        choices=["pmc", "biorxiv", "both"],
        default="pmc",
        help="Which local corpus alias to use when execution mode resolves to local.",
    )
    parser.add_argument(
        "--local-repo-dir",
        default=DEFAULT_LOCAL_REPO,
        help="Path to the local polars-dovmed repo used for local scans.",
    )
    parser.add_argument(
        "--local-output-dir",
        help="Optional output directory for local dovmed scan results.",
    )
    parser.add_argument("--save-payload")
    parser.add_argument("--save-response")
    parser.add_argument("--save-discovery-payload")
    parser.add_argument("--save-discovery-response")
    parser.add_argument(
        "--details-rerank-limit",
        type=int,
        default=8,
        help="How many discovery candidates to fetch with get_paper_details for second-pass reranking",
    )
    parser.add_argument(
        "--skip-details-rerank",
        action="store_true",
        help="Skip the automatic discovery -> details -> rerank second pass",
    )
    parser.add_argument(
        "--auto-advanced-refinement",
        action="store_true",
        help="Run an additional advanced structured scan after discovery when the first pass is still too loose",
    )
    parser.add_argument(
        "--sync",
        action="store_true",
        help="Use the legacy synchronous request path instead of async jobs",
    )
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument(
        "--poll-timeout",
        type=int,
        default=900,
        help="Maximum seconds to wait for async job completion",
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=2,
        help="Fallback poll interval in seconds when the API does not specify one",
    )
    parser.add_argument(
        "--discovery-fallback",
        action="store_true",
        help="If a structured advanced query fails or times out, retry a simplified flat discovery query built from query-group names",
    )
    parser.add_argument("--raw", action="store_true")
    args = parser.parse_args()
    chosen = sum(
        bool(value) for value in (args.query, args.queries_file, args.group, args.details)
    )
    if chosen != 1:
        parser.error(
            "provide exactly one of --query, --queries-file, --group, or --details"
        )
    if args.query and not args.allow_flat_query:
        parser.error(
            "--query is exploratory free-text search only; use --queries-file/--group with a structured JSON query, "
            "or pass --allow-flat-query to opt in explicitly"
        )
    try:
        args.year_bands = parse_year_bands(args.year_bands)
    except ValueError as exc:
        parser.error(str(exc))
    if args.year_bands and args.year_band != "all":
        parser.error("use either --year-band for a single band or --year-bands for parallel fan-out")
    if args.year_bands and args.details:
        parser.error("--year-bands applies to search requests, not paper-details lookups")
    if args.year_band_workers < 1:
        parser.error("--year-band-workers must be at least 1")
    return args


def load_api_key(explicit_key):
    api_key = explicit_key or os.environ.get("POLARS_DOVMED_API_KEY")
    if not api_key:
        raise SystemExit("missing POLARS_DOVMED_API_KEY")
    return api_key


def determine_execution_mode(args):
    if args.execution_mode != "auto":
        return args.execution_mode
    corpus = effective_corpus(args)
    # --query and --details are only supported by the API path. Route them
    # there even without a key so the user sees a clear missing-key error
    # instead of the generic "local mode does not support ..." message.
    if args.query or args.details:
        return "api"
    if args.api_key or os.environ.get("POLARS_DOVMED_API_KEY"):
        return "api"
    if corpus != "pmc":
        return "local"
    return "local"


def effective_corpus(args):
    return args.corpus or args.local_corpus


def parse_group(spec):
    if "=" not in spec:
        raise SystemExit(f"invalid group '{spec}', expected name=term1,term2")
    name, raw_terms = spec.split("=", 1)
    terms = [term.strip() for term in raw_terms.split(",") if term.strip()]
    if not name or not terms:
        raise SystemExit(f"invalid group '{spec}', expected name=term1,term2")
    return name, [[term] for term in terms]


def load_queries_file(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError as exc:
        raise SystemExit(f"queries file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid queries file '{path}': {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"invalid queries file '{path}', expected a JSON object")
    return data


def resolve_year(paper):
    year = paper.get("year")
    if isinstance(year, int):
        return year
    if isinstance(year, str) and year.isdigit():
        return int(year)
    match = re.match(r"(\d{4})", paper.get("publication_date") or "")
    return int(match.group(1)) if match else None


def compact_paper(paper):
    ranking = paper.get("ranking") or {}
    triage = paper.get("triage") or {}
    return {
        "pmc_id": paper.get("pmc_id"),
        "pmid": paper.get("pmid"),
        "corpus": paper.get("corpus"),
        "source": paper.get("source"),
        "title": paper.get("title"),
        "journal": paper.get("journal"),
        "year": resolve_year(paper),
        "publication_date": paper.get("publication_date"),
        "doi": paper.get("doi"),
        "ranking_score": ranking.get("score"),
        "title_signal_hits": ranking.get("title_signal_hits"),
        "abstract_signal_hits": ranking.get("abstract_signal_hits"),
        "group_count_total": ranking.get("group_count_total"),
        "total_matches": ranking.get("total_matches"),
        "triage_score": triage.get("score"),
        "concept_coverage": triage.get("concept_coverage"),
        "support_concept_coverage": triage.get("support_concept_coverage"),
        "support_specificity_score": triage.get("support_specificity_score"),
        "specific_support_group_hits": triage.get("specific_support_group_hits"),
        "best_local_context_score": triage.get("best_local_context_score"),
        "best_local_concept_coverage": triage.get("best_local_concept_coverage"),
        "local_joint_contexts": triage.get("local_joint_contexts"),
        "anchor_support_contexts": triage.get("anchor_support_contexts"),
        "best_local_context_source": triage.get("best_local_context_source"),
        "best_local_context_snippet": triage.get("best_local_context_snippet"),
        "matched_concepts": triage.get("matched_concepts"),
    }


def build_structured_request(primary_queries, args):
    payload = {
        "primary_queries": primary_queries,
        "corpus": effective_corpus(args),
        "year_band": None if args.year_band == "all" else args.year_band,
        "search_columns": [col.strip() for col in args.search_columns.split(",") if col.strip()],
        "extract_matches": args.extract_matches,
        "add_group_counts": args.add_group_counts,
        "max_results": args.max_results,
        "mode": args.mode,
    }
    return "/api/scan_literature_advanced", payload


def build_request(args):
    if args.details:
        corpus = effective_corpus(args)
        if corpus == "biorxiv":
            return "/api/get_paper_details", {"corpus": corpus, "dois": args.details}
        return "/api/get_paper_details", {"corpus": corpus, "pmc_ids": args.details}
    if args.queries_file:
        return build_structured_request(load_queries_file(args.queries_file), args)
    if args.group:
        return build_structured_request(dict(parse_group(spec) for spec in args.group), args)
    payload = {
        "query": args.query,
        "corpus": effective_corpus(args),
        "year_band": None if args.year_band == "all" else args.year_band,
        "max_results": args.max_results,
        "extract_matches": False,
        "fast_mode": args.fast_mode,
    }
    return "/api/search_literature", payload


def build_discovery_request(args):
    if not args.queries_file:
        raise SystemExit("--discovery-fallback requires --queries-file")
    original_mode = args.mode
    args.mode = "discovery"
    try:
        return build_structured_request(load_queries_file(args.queries_file), args)
    finally:
        args.mode = original_mode


def maybe_save_json(path, payload):
    if not path:
        return
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def local_output_dir(args):
    if args.local_output_dir:
        return Path(args.local_output_dir).expanduser()
    if args.save_response:
        response_path = Path(args.save_response)
        return response_path.with_suffix("")
    return Path(tempfile.mkdtemp(prefix="dovmed_local_scan_"))


def compact_local_paper(row):
    publication_date = row.get("publication_date") or ""
    year = None
    match = re.match(r"(\d{4})", publication_date)
    if match:
        year = int(match.group(1))
    return {
        "pmc_id": row.get("pmc_id") or None,
        "doi": row.get("doi") or None,
        "title": row.get("title") or None,
        "journal": row.get("journal") or None,
        "year": year,
        "publication_date": publication_date or None,
        "source": row.get("source") or "pmc",
        "version": row.get("version"),
        "total_matches": row.get("total_matches"),
    }


def execute_local_scan(args):
    if args.query or args.details:
        raise SystemExit(
            "local mode currently supports --queries-file or --group, not --query or --details"
        )
    if args.group:
        queries = dict(parse_group(spec) for spec in args.group)
        query_file = Path(tempfile.mkdtemp(prefix="dovmed_query_")) / "query.json"
        query_file.write_text(json.dumps(queries, indent=2) + "\n", encoding="utf-8")
    else:
        queries = load_queries_file(args.queries_file)
        query_file = Path(args.queries_file)

    repo_dir = Path(args.local_repo_dir).expanduser()
    output_dir = local_output_dir(args)
    output_dir.parent.mkdir(parents=True, exist_ok=True)

    command = [
        os.path.expanduser("~/.pixi/bin/pixi"),
        "run",
        "dovmed",
        "scan",
        "--corpus",
        effective_corpus(args),
        "--year-band",
        args.year_band,
        "--queries-file",
        str(query_file),
        "--search-columns",
        args.search_columns,
        "--extract-matches",
        args.extract_matches,
        "--add-group-counts",
        args.add_group_counts,
        "--output-path",
        str(output_dir),
    ]
    if args.verbose:
        command.append("--verbose")

    payload = {
        "execution_mode": "local",
        "corpus": effective_corpus(args),
        "repo_dir": str(repo_dir),
        "command": command,
        "primary_queries": queries,
    }
    maybe_save_json(args.save_payload, payload)

    result = subprocess.run(
        command,
        cwd=repo_dir,
        capture_output=True,
        text=True,
    )

    processed_path = output_dir / "processed.parquet"
    legacy_processed_path = output_dir / "prcoessed.parquet"
    papers = []
    readable_processed_path = processed_path if processed_path.exists() else legacy_processed_path
    if readable_processed_path.exists():
        import polars as pl

        df = pl.read_parquet(readable_processed_path)
        papers = [compact_local_paper(row) for row in df.head(args.max_results).to_dicts()]

    response = {
        "execution_mode": "local",
        "corpus": effective_corpus(args),
        "repo_dir": str(repo_dir),
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "output_dir": str(output_dir),
        "processed_parquet": str(readable_processed_path)
        if readable_processed_path.exists()
        else None,
        "flattened_csv": str(output_dir / "flattened.csv")
        if (output_dir / "flattened.csv").exists()
        else None,
        "papers": papers,
    }
    maybe_save_json(args.save_response, response)

    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or result.stdout.strip() or "local dovmed scan failed")
    return response


def companion_json_path(path, suffix):
    if not path:
        return None
    output = Path(path)
    ext = output.suffix or ".json"
    return str(output.with_name(f"{output.stem}_{suffix}{ext}"))


def make_request(base_url, endpoint, api_key, *, method="GET", payload=None):
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    headers = {
        "User-Agent": "Mozilla/5.0",
        "X-API-Key": api_key,
    }
    if payload is not None:
        headers["Content-Type"] = "application/json"
    return urllib.request.Request(
        f"{base_url}{endpoint}",
        data=data,
        headers={
            **headers,
        },
        method=method,
    )


def request_json(base_url, endpoint, api_key, *, timeout, method="GET", payload=None):
    request = make_request(
        base_url,
        endpoint,
        api_key,
        method=method,
        payload=payload,
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def post_json(base_url, endpoint, api_key, payload, timeout):
    return request_json(
        base_url,
        endpoint,
        api_key,
        timeout=timeout,
        method="POST",
        payload=payload,
    )


def build_submitted_request(endpoint, payload, use_async_jobs):
    if not use_async_jobs:
        return endpoint, payload
    return "/api/jobs", {
        "job_type": ASYNC_ENDPOINTS[endpoint],
        "payload": payload,
    }


def build_parallel_submitted_request(endpoint, payload, year_bands, use_async_jobs):
    requests = []
    for band in year_bands:
        band_payload = copy.deepcopy(payload)
        band_payload["year_band"] = band
        submitted_endpoint, submitted_payload = build_submitted_request(
            endpoint,
            band_payload,
            use_async_jobs,
        )
        requests.append(
            {
                "year_band": band,
                "endpoint": submitted_endpoint,
                "payload": submitted_payload,
                "target_endpoint": endpoint,
                "target_payload": band_payload,
            }
        )
    return {
        "parallel_year_bands": year_bands,
        "requests": requests,
    }


def run_async_job(
    base_url,
    endpoint,
    api_key,
    payload,
    *,
    poll_timeout,
    poll_interval,
):
    submitted_endpoint, submitted_payload = build_submitted_request(
        endpoint,
        payload,
        use_async_jobs=True,
    )
    job = post_json(
        base_url,
        submitted_endpoint,
        api_key,
        submitted_payload,
        timeout=min(max(poll_timeout, 30), 120),
    )
    job_id = job.get("job_id")
    if not job_id:
        raise RuntimeError(f"async job submission failed: {job}")

    deadline = time.monotonic() + poll_timeout
    result_endpoint = f"/api/jobs/{job_id}/result"
    while True:
        result_wrapper = request_json(
            base_url,
            result_endpoint,
            api_key,
            timeout=60,
        )
        status = result_wrapper.get("status")
        if status == "succeeded":
            result = result_wrapper.get("result")
            if isinstance(result, dict):
                return result
            raise RuntimeError(f"async job {job_id} succeeded without a JSON result")
        if status == "failed":
            result = result_wrapper.get("result") or {}
            error = result_wrapper.get("error") or result.get("error") or "async job failed"
            raise RuntimeError(f"async job {job_id} failed: {error}")
        if time.monotonic() >= deadline:
            raise RuntimeError(
                f"async job {job_id} timed out after {poll_timeout}s"
            )
        sleep_for = result_wrapper.get("poll_after_sec") or poll_interval
        time.sleep(max(1, int(sleep_for)))


def execute_request(
    base_url,
    endpoint,
    api_key,
    payload,
    *,
    timeout,
    use_async_jobs,
    poll_timeout,
    poll_interval,
):
    try:
        if use_async_jobs:
            return run_async_job(
                base_url,
                endpoint,
                api_key,
                payload,
                poll_timeout=poll_timeout,
                poll_interval=poll_interval,
            )
        return post_json(base_url, endpoint, api_key, payload, timeout)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(
            f"http error {exc.code}: {exc.read().decode('utf-8')}"
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"request failed: {exc.reason}") from exc


def paper_identity(paper):
    corpus = paper.get("corpus") or paper.get("source") or "pmc"
    for key in ("pmc_id", "doi", "pmid"):
        value = paper.get(key)
        if value:
            return corpus, key, str(value).lower()
    return (
        corpus,
        "title_year",
        str(paper.get("title") or "").strip().lower(),
        resolve_year(paper),
    )


def merge_parallel_year_band_results(year_bands, band_results, elapsed_ms):
    per_band_by_name = {item["year_band"]: item for item in band_results}
    papers = []
    seen = set()
    total_found = 0
    summaries = []
    failures = []
    for band in year_bands:
        band_item = per_band_by_name.get(band)
        if not band_item:
            continue
        if band_item.get("error"):
            failures.append({"year_band": band, "error": band_item["error"]})
            continue
        result = band_item["result"]
        total_found += result.get("total_found") or 0
        band_papers = result.get("papers") or []
        summaries.append(
            {
                "year_band": band,
                "elapsed_ms": result.get("elapsed_ms"),
                "total_found": result.get("total_found"),
                "returned": len(band_papers),
                "strategy_used": result.get("strategy_used"),
            }
        )
        for paper in band_papers:
            key = paper_identity(paper)
            if key in seen:
                continue
            seen.add(key)
            merged_paper = dict(paper)
            merged_paper.setdefault("search_year_band", band)
            papers.append(merged_paper)
    return {
        "strategy_used": "parallel_year_bands",
        "parallel_year_bands": list(year_bands),
        "elapsed_ms": elapsed_ms,
        "total_found": total_found,
        "papers": papers,
        "year_band_results": summaries,
        "year_band_errors": failures,
    }


def execute_parallel_year_band_requests(
    args,
    endpoint,
    api_key,
    payload,
    *,
    timeout,
    use_async_jobs,
    poll_timeout,
    poll_interval,
):
    if endpoint not in ASYNC_ENDPOINTS:
        raise RuntimeError("--year-bands only supports search endpoints")
    year_bands = list(args.year_bands)
    max_workers = min(args.year_band_workers, len(year_bands))
    started = time.monotonic()

    def run_band(band):
        band_payload = copy.deepcopy(payload)
        band_payload["year_band"] = band
        try:
            result = execute_request(
                args.base_url,
                endpoint,
                api_key,
                band_payload,
                timeout=timeout,
                use_async_jobs=use_async_jobs,
                poll_timeout=poll_timeout,
                poll_interval=poll_interval,
            )
            return {"year_band": band, "result": result}
        except Exception as exc:
            return {"year_band": band, "error": str(exc)}

    band_results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(run_band, band) for band in year_bands]
        for future in concurrent.futures.as_completed(futures):
            band_results.append(future.result())

    elapsed_ms = int((time.monotonic() - started) * 1000)
    merged = merge_parallel_year_band_results(year_bands, band_results, elapsed_ms)
    if not merged["papers"] and merged["year_band_errors"]:
        errors = "; ".join(
            f"{item['year_band']}: {item['error']}" for item in merged["year_band_errors"]
        )
        raise RuntimeError(f"parallel year-band search failed: {errors}")
    return merged


def summarize_papers(papers, target_year):
    kept = []
    missing_year = 0
    filtered_year = 0
    for paper in papers:
        compact = compact_paper(paper)
        paper_year = compact["year"]
        if target_year is None:
            kept.append(compact)
            continue
        if paper_year is None:
            missing_year += 1
            continue
        if paper_year == target_year:
            kept.append(compact)
        else:
            filtered_year += 1
    return kept, missing_year, filtered_year


def has_incomplete_citation(papers):
    for paper in papers:
        if paper["year"] is None or not paper.get("doi"):
            return True
    return False


def normalize_pattern(pattern):
    cleaned = pattern.replace("(?i)", "")
    return cleaned.replace("\\b", r"\b")


def pattern_matches_text(pattern, text):
    if not text:
        return False
    cleaned = normalize_pattern(pattern)
    try:
        return re.search(cleaned, text, flags=re.IGNORECASE) is not None
    except re.error:
        return re.search(re.escape(cleaned), text, flags=re.IGNORECASE) is not None


def field_texts(paper):
    return {
        "title": paper.get("title") or "",
        "abstract": paper.get("abstract_text") or paper.get("abstract") or "",
        "full_text": paper.get("full_text") or "",
    }


def normalize_space(text):
    return re.sub(r"\s+", " ", text or "").strip()


def truncate_text(text, limit=CONTEXT_SNIPPET_CHARS):
    normalized = normalize_space(text)
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3].rstrip() + "..."


def is_support_concept(concept_name):
    lower = concept_name.lower()
    return any(token in lower for token in SUPPORT_CONCEPT_TOKENS)


def term_specificity(term):
    cleaned = normalize_pattern(term).strip().strip("\"'").lower()
    if not cleaned:
        return 0.0
    score = 1.0
    if cleaned in GENERIC_SUPPORT_TERMS:
        score -= 0.6
    if " " in cleaned:
        score += 2.0
    if "-" in cleaned or "/" in cleaned:
        score += 0.5
    if len(cleaned) >= 10:
        score += 0.8
    if any(char.isdigit() for char in cleaned):
        score += 0.5
    return max(score, 0.2)


def group_specificity(group):
    return max((term_specificity(term) for term in group if term), default=0.0)


def split_into_word_windows(text, max_words=WINDOW_WORDS, stride=WINDOW_STRIDE):
    words = normalize_space(text).split()
    if not words:
        return []
    if len(words) <= max_words:
        return [" ".join(words)]
    windows = []
    for start in range(0, len(words), stride):
        chunk = words[start : start + max_words]
        if not chunk:
            break
        windows.append(" ".join(chunk))
        if start + max_words >= len(words):
            break
    return windows


def split_into_sentence_contexts(text):
    normalized = normalize_space(text)
    if not normalized:
        return []
    pieces = [piece.strip() for piece in SENTENCE_SPLIT_RE.split(normalized) if piece.strip()]
    contexts = []
    for piece in pieces:
        if len(piece) <= MAX_SENTENCE_CONTEXT_CHARS:
            contexts.append(piece)
        else:
            contexts.extend(split_into_word_windows(piece))
    return contexts


def find_pattern_spans(pattern, text, max_hits=MAX_TERM_SPANS_PER_TERM):
    if not text:
        return []
    cleaned = normalize_pattern(pattern)
    try:
        regex = re.compile(cleaned, flags=re.IGNORECASE)
    except re.error:
        regex = re.compile(re.escape(cleaned), flags=re.IGNORECASE)
    spans = []
    for match in regex.finditer(text):
        spans.append(match.span())
        if len(spans) >= max_hits:
            break
    return spans


def merge_windows(windows):
    if not windows:
        return []
    merged = []
    for start, end in sorted(windows):
        if not merged or start > merged[-1][1] + 40:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return [(start, end) for start, end in merged]


def build_local_contexts(paper, primary_queries):
    texts = field_texts(paper)
    contexts = []
    seen = set()

    def add_context(source, text):
        normalized = normalize_space(text)
        if not normalized:
            return
        key = (source, normalized)
        if key in seen:
            return
        seen.add(key)
        contexts.append({"source": source, "text": normalized})

    if texts["title"]:
        add_context("title", texts["title"])
    for sentence in split_into_sentence_contexts(texts["abstract"]):
        add_context("abstract", sentence)

    full_text = texts["full_text"]
    if full_text:
        windows = []
        for concept, groups in primary_queries.items():
            if concept == "disqualifying_terms":
                continue
            for group in groups:
                for term in group:
                    for start, end in find_pattern_spans(term, full_text):
                        windows.append(
                            (
                                max(0, start - FULLTEXT_CONTEXT_RADIUS),
                                min(len(full_text), end + FULLTEXT_CONTEXT_RADIUS),
                            )
                        )
        for start, end in merge_windows(windows)[:MAX_FULLTEXT_CONTEXTS]:
            for sentence in split_into_sentence_contexts(full_text[start:end]):
                add_context("full_text", sentence)
    return contexts


def analyze_context_against_queries(text, primary_queries):
    matched_group_counts = {}
    matched_group_scores = {}
    specific_support_group_hits = 0
    support_specificity_score = 0.0
    for concept, groups in primary_queries.items():
        if concept == "disqualifying_terms":
            continue
        matched_groups = 0
        matched_score = 0.0
        for group in groups:
            terms = [term for term in group if term]
            if terms and all(pattern_matches_text(term, text) for term in terms):
                matched_groups += 1
                specificity = group_specificity(group)
                matched_score += specificity
                if is_support_concept(concept) and specificity >= 2.0:
                    specific_support_group_hits += 1
        matched_group_counts[concept] = matched_groups
        matched_group_scores[concept] = round(matched_score, 3)
        if is_support_concept(concept):
            support_specificity_score += matched_score
    matched_concepts = [concept for concept, count in matched_group_counts.items() if count > 0]
    support_concepts = [concept for concept in matched_concepts if is_support_concept(concept)]
    return {
        "matched_group_counts": matched_group_counts,
        "matched_group_scores": matched_group_scores,
        "matched_concepts": matched_concepts,
        "concept_coverage": len(matched_concepts),
        "support_concept_coverage": len(support_concepts),
        "support_specificity_score": round(support_specificity_score, 3),
        "specific_support_group_hits": specific_support_group_hits,
        "total_group_matches": sum(matched_group_counts.values()),
    }


def analyze_paper_against_queries(paper, primary_queries):
    texts = field_texts(paper)
    combined_text = " ".join(value for value in texts.values() if value)
    matched_group_counts = {}
    matched_group_scores = {}
    title_support_hits = 0
    abstract_support_hits = 0
    full_text_support_hits = 0
    support_specificity_score = 0.0
    specific_support_group_hits = 0

    for concept, groups in primary_queries.items():
        if concept == "disqualifying_terms":
            continue
        matched_groups = 0
        matched_score = 0.0
        for group in groups:
            terms = [term for term in group if term]
            if terms and all(pattern_matches_text(term, combined_text) for term in terms):
                matched_groups += 1
                matched_score += group_specificity(group)
                if is_support_concept(concept) and group_specificity(group) >= 2.0:
                    specific_support_group_hits += 1
        matched_group_counts[concept] = matched_groups
        matched_group_scores[concept] = round(matched_score, 3)
        if is_support_concept(concept):
            support_specificity_score += matched_score
        if matched_groups <= 0 or not is_support_concept(concept):
            continue
        if any(
            group and all(pattern_matches_text(term, texts["title"]) for term in group if term)
            for group in groups
        ):
            title_support_hits += 1
        if any(
            group and all(pattern_matches_text(term, texts["abstract"]) for term in group if term)
            for group in groups
        ):
            abstract_support_hits += 1
        if any(
            group and all(pattern_matches_text(term, texts["full_text"]) for term in group if term)
            for group in groups
        ):
            full_text_support_hits += 1

    matched_concepts = [concept for concept, count in matched_group_counts.items() if count > 0]
    support_concepts = [concept for concept in matched_concepts if is_support_concept(concept)]
    total_group_matches = sum(matched_group_counts.values())
    return {
        "matched_group_counts": matched_group_counts,
        "matched_group_scores": matched_group_scores,
        "matched_concepts": matched_concepts,
        "concept_coverage": len(matched_concepts),
        "support_concept_coverage": len(support_concepts),
        "support_specificity_score": round(support_specificity_score, 3),
        "specific_support_group_hits": specific_support_group_hits,
        "title_support_hits": title_support_hits,
        "abstract_support_hits": abstract_support_hits,
        "full_text_support_hits": full_text_support_hits,
        "total_group_matches": total_group_matches,
    }


def analyze_local_contexts(paper, primary_queries):
    contexts = build_local_contexts(paper, primary_queries)
    best = None
    local_joint_contexts = 0
    anchor_support_contexts = 0

    for context in contexts:
        analysis = analyze_context_against_queries(context["text"], primary_queries)
        if analysis["concept_coverage"] == 0:
            continue
        local_score = (
            analysis["concept_coverage"] * 220
            + analysis["support_concept_coverage"] * 120
            + int(analysis["support_specificity_score"] * 130)
            + analysis["specific_support_group_hits"] * 95
            + analysis["total_group_matches"] * 18
        )
        if analysis["concept_coverage"] >= 2:
            local_joint_contexts += 1
            local_score += 120
        if analysis["support_concept_coverage"] > 0 and analysis["concept_coverage"] > analysis["support_concept_coverage"]:
            anchor_support_contexts += 1
            local_score += 110
        if context["source"] == "title":
            local_score += 40
        elif context["source"] == "abstract":
            local_score += 20

        candidate = {
            "score": local_score,
            "source": context["source"],
            "snippet": truncate_text(context["text"]),
            **analysis,
        }
        if best is None or (
            candidate["score"],
            candidate["concept_coverage"],
            candidate["support_concept_coverage"],
        ) > (
            best["score"],
            best["concept_coverage"],
            best["support_concept_coverage"],
        ):
            best = candidate

    if best is None:
        return {
            "best_local_context_score": 0,
            "best_local_concept_coverage": 0,
            "best_local_context_source": None,
            "best_local_context_snippet": None,
            "local_joint_contexts": 0,
            "anchor_support_contexts": 0,
        }
    return {
        "best_local_context_score": best["score"],
        "best_local_concept_coverage": best["concept_coverage"],
        "best_local_context_source": best["source"],
        "best_local_context_snippet": best["snippet"],
        "local_joint_contexts": local_joint_contexts,
        "anchor_support_contexts": anchor_support_contexts,
    }


def triage_score(paper, analysis):
    discovery_ranking = paper.get("ranking") or {}
    score = (
        int(discovery_ranking.get("score") or 0)
        + analysis["concept_coverage"] * 240
        + analysis["support_concept_coverage"] * 120
        + int(analysis["support_specificity_score"] * 110)
        + analysis["specific_support_group_hits"] * 90
        + analysis["title_support_hits"] * 120
        + analysis["abstract_support_hits"] * 70
        + analysis["full_text_support_hits"] * 25
        + analysis["total_group_matches"] * 20
        + analysis["best_local_context_score"] * 2
        + analysis["local_joint_contexts"] * 90
        + analysis["anchor_support_contexts"] * 110
    )
    if analysis["support_concept_coverage"] > 0 and analysis["specific_support_group_hits"] == 0:
        score -= 80
    if analysis["support_concept_coverage"] > 0 and analysis["best_local_concept_coverage"] < 2:
        score -= 140
    return score


def paper_lookup_key(paper):
    return paper.get("pmc_id") or (paper.get("doi") or "").strip().lower()


def merge_and_rerank_details(discovery_result, details_result, primary_queries):
    discovery_by_id = {
        paper_lookup_key(paper): paper for paper in discovery_result.get("papers") or []
    }
    triaged = []
    for paper in details_result.get("papers") or []:
        discovery_paper = discovery_by_id.get(paper_lookup_key(paper), {})
        analysis = analyze_paper_against_queries(paper, primary_queries)
        analysis.update(analyze_local_contexts(paper, primary_queries))
        triaged_paper = dict(paper)
        triaged_paper["ranking"] = discovery_paper.get("ranking") or {}
        triaged_paper["triage"] = {
            "score": triage_score(discovery_paper, analysis),
            **analysis,
        }
        triaged.append(triaged_paper)
    triaged.sort(
        key=lambda paper: (
            paper["triage"]["score"],
            paper["triage"]["best_local_context_score"],
            paper["triage"]["support_concept_coverage"],
            paper["triage"]["concept_coverage"],
            (paper.get("ranking") or {}).get("score") or 0,
        ),
        reverse=True,
    )
    return triaged


def recommended_next_step(triaged_papers, primary_queries):
    concept_count = len([key for key in primary_queries if key != "disqualifying_terms"])
    if not triaged_papers:
        return "advanced_refinement_recommended"
    top = triaged_papers[0].get("triage") or {}
    if concept_count > 1 and top.get("concept_coverage", 0) < min(2, concept_count):
        return "advanced_refinement_recommended"
    if any(is_support_concept(key) for key in primary_queries if key != "disqualifying_terms"):
        if top.get("support_concept_coverage", 0) == 0:
            return "advanced_refinement_recommended"
    return "details_triage_sufficient"


def main():
    args = parse_args()
    execution_mode = determine_execution_mode(args)

    if execution_mode == "local":
        if args.year_bands:
            raise SystemExit(
                "--year-bands parallel fan-out is supported for hosted API mode; "
                "use --year-band for one local scan"
            )
        result = execute_local_scan(args)
        if args.raw:
            print(json.dumps(result, indent=2))
            return
        summary = {
            "endpoint": "local_scan",
            "execution_mode": "local",
            "corpus": effective_corpus(args),
            "returned": len(result.get("papers") or []),
            "output_dir": result.get("output_dir"),
            "processed_parquet": result.get("processed_parquet"),
            "flattened_csv": result.get("flattened_csv"),
            "papers": result.get("papers") or [],
            "warnings": [],
        }
        print(json.dumps(summary, indent=2))
        return

    api_key = load_api_key(args.api_key)
    endpoint, payload = build_request(args)
    timeout = args.timeout or (600 if endpoint.endswith("advanced") else 120)
    use_async_jobs = not args.sync and endpoint in ASYNC_ENDPOINTS
    if args.year_bands:
        submitted_payload_info = build_parallel_submitted_request(
            endpoint,
            payload,
            args.year_bands,
            use_async_jobs,
        )
    else:
        submitted_endpoint, submitted_payload = build_submitted_request(
            endpoint,
            payload,
            use_async_jobs,
        )
        submitted_payload_info = {
            "endpoint": submitted_endpoint,
            "payload": submitted_payload,
            "target_endpoint": endpoint,
            "target_payload": payload,
        }
    maybe_save_json(args.save_payload, submitted_payload_info)
    try:
        if args.year_bands:
            result = execute_parallel_year_band_requests(
                args,
                endpoint,
                api_key,
                payload,
                timeout=timeout,
                use_async_jobs=use_async_jobs,
                poll_timeout=args.poll_timeout,
                poll_interval=args.poll_interval,
            )
        else:
            result = execute_request(
                args.base_url,
                endpoint,
                api_key,
                payload,
                timeout=timeout,
                use_async_jobs=use_async_jobs,
                poll_timeout=args.poll_timeout,
                poll_interval=args.poll_interval,
            )
    except RuntimeError as exc:
        if args.discovery_fallback and endpoint.endswith("advanced"):
            endpoint, payload = build_discovery_request(args)
            use_async_jobs = not args.sync and endpoint in ASYNC_ENDPOINTS
            if args.year_bands:
                submitted_payload_info = build_parallel_submitted_request(
                    endpoint,
                    payload,
                    args.year_bands,
                    use_async_jobs,
                )
            else:
                submitted_endpoint, submitted_payload = build_submitted_request(
                    endpoint,
                    payload,
                    use_async_jobs,
                )
                submitted_payload_info = {
                    "endpoint": submitted_endpoint,
                    "payload": submitted_payload,
                    "target_endpoint": endpoint,
                    "target_payload": payload,
                }
            maybe_save_json(
                args.save_discovery_payload or args.save_payload,
                {
                    **submitted_payload_info,
                    "note": f"discovery fallback after advanced query failure: {exc}",
                },
            )
            if args.year_bands:
                result = execute_parallel_year_band_requests(
                    args,
                    endpoint,
                    api_key,
                    payload,
                    timeout=120,
                    use_async_jobs=use_async_jobs,
                    poll_timeout=args.poll_timeout,
                    poll_interval=args.poll_interval,
                )
            else:
                result = execute_request(
                    args.base_url,
                    endpoint,
                    api_key,
                    payload,
                    timeout=120,
                    use_async_jobs=use_async_jobs,
                    poll_timeout=args.poll_timeout,
                    poll_interval=args.poll_interval,
                )
        else:
            raise SystemExit(str(exc)) from None
    if (
        not args.skip_details_rerank
        and endpoint.endswith("advanced")
        and payload.get("mode") == "discovery"
        and payload.get("primary_queries")
        and result.get("papers")
    ):
        corpus = payload.get("corpus") or "pmc"
        candidate_id_field = "pmc_id"
        candidate_ids = []
        if corpus == "biorxiv":
            candidate_id_field = "doi"
            candidate_ids = [
                paper.get("doi")
                for paper in (result.get("papers") or [])[: max(1, args.details_rerank_limit)]
                if paper.get("doi")
            ]
        elif corpus == "pmc":
            candidate_ids = [
                paper.get("pmc_id")
                for paper in (result.get("papers") or [])[: max(1, args.details_rerank_limit)]
                if paper.get("pmc_id")
            ]
        if candidate_ids:
            details_payload = (
                {"corpus": "biorxiv", "dois": candidate_ids}
                if corpus == "biorxiv"
                else {"corpus": "pmc", "pmc_ids": candidate_ids}
            )
            details_result = execute_request(
                args.base_url,
                "/api/get_paper_details",
                api_key,
                details_payload,
                timeout=120,
                use_async_jobs=False,
                poll_timeout=args.poll_timeout,
                poll_interval=args.poll_interval,
            )
            maybe_save_json(
                companion_json_path(args.save_payload, "details_payload"),
                {
                    "endpoint": "/api/get_paper_details",
                    "payload": details_payload,
                },
            )
            maybe_save_json(
                companion_json_path(args.save_response, "details_response"),
                details_result,
            )
            triaged_papers = merge_and_rerank_details(
                result,
                details_result,
                payload["primary_queries"],
            )
            result["details_lookup"] = {
                "requested": details_result.get("requested"),
                "found": details_result.get("found"),
                "missing_ids": details_result.get("missing_ids"),
                f"candidate_{candidate_id_field}s": candidate_ids,
            }
            result["triaged_papers"] = triaged_papers
            result["recommended_next_step"] = recommended_next_step(
                triaged_papers,
                payload["primary_queries"],
            )
    if (
        args.auto_advanced_refinement
        and endpoint.endswith("advanced")
        and payload.get("mode") == "discovery"
        and payload.get("primary_queries")
        and (
            result.get("strategy_used") == "discovery_fallback"
            or result.get("recommended_next_step") == "advanced_refinement_recommended"
        )
    ):
        advanced_payload = dict(payload)
        advanced_payload["mode"] = "advanced"
        advanced_payload["max_results"] = max(
            args.max_results,
            min(args.details_rerank_limit, args.max_results),
        )
        try:
            if args.year_bands:
                advanced_result = execute_parallel_year_band_requests(
                    args,
                    endpoint,
                    api_key,
                    advanced_payload,
                    timeout=args.timeout or 600,
                    use_async_jobs=use_async_jobs,
                    poll_timeout=args.poll_timeout,
                    poll_interval=args.poll_interval,
                )
            else:
                advanced_result = execute_request(
                    args.base_url,
                    endpoint,
                    api_key,
                    advanced_payload,
                    timeout=args.timeout or 600,
                    use_async_jobs=use_async_jobs,
                    poll_timeout=args.poll_timeout,
                    poll_interval=args.poll_interval,
                )
            result["advanced_refinement"] = advanced_result
            result["recommended_next_step"] = "advanced_refinement_completed"
            maybe_save_json(
                companion_json_path(args.save_payload, "advanced_payload"),
                build_parallel_submitted_request(
                    endpoint,
                    advanced_payload,
                    args.year_bands,
                    use_async_jobs,
                )
                if args.year_bands
                else {
                    "endpoint": endpoint,
                    "payload": advanced_payload,
                },
            )
            maybe_save_json(
                companion_json_path(args.save_response, "advanced_response"),
                advanced_result,
            )
        except RuntimeError as exc:
            result["advanced_refinement"] = {"error": str(exc)}
            result["recommended_next_step"] = "advanced_refinement_failed"
    if (
        args.discovery_fallback
        and endpoint.endswith("advanced")
        and payload.get("mode") == "discovery"
    ):
        maybe_save_json(args.save_discovery_response or args.save_response, result)
    else:
        maybe_save_json(args.save_response, result)
    if args.raw:
        print(json.dumps(result, indent=2))
        return
    papers = (
        (result.get("advanced_refinement") or {}).get("papers")
        or result.get("triaged_papers")
        or result.get("papers")
        or []
    )
    compact, missing_year, filtered_year = summarize_papers(papers, args.year)
    summary = {
        "endpoint": endpoint,
        "mode": args.mode if args.queries_file or args.group else None,
        "strategy_used": result.get("strategy_used"),
        "elapsed_ms": result.get("elapsed_ms"),
        "parallel_year_bands": result.get("parallel_year_bands"),
        "year_band_results": result.get("year_band_results"),
        "year_band_errors": result.get("year_band_errors"),
        "signal_terms": result.get("signal_terms"),
        "discovery_query": result.get("discovery_query"),
        "reported_total": result.get("total_found"),
        "returned": len(papers),
        "paper_source": (
            "advanced_refinement"
            if (result.get("advanced_refinement") or {}).get("papers")
            else "details_triage"
            if result.get("triaged_papers")
            else "discovery"
        ),
        "details_lookup": result.get("details_lookup"),
        "advanced_refinement": (
            {
                "strategy_used": (result.get("advanced_refinement") or {}).get("strategy_used"),
                "elapsed_ms": (result.get("advanced_refinement") or {}).get("elapsed_ms"),
                "returned": len((result.get("advanced_refinement") or {}).get("papers") or []),
                "error": (result.get("advanced_refinement") or {}).get("error"),
            }
            if result.get("advanced_refinement") is not None
            else None
        ),
        "recommended_next_step": result.get("recommended_next_step"),
        "year_filter": args.year,
        "excluded_missing_year": missing_year,
        "excluded_nonmatching_year": filtered_year,
        "papers": compact,
        "warnings": [],
    }
    if missing_year:
        summary["warnings"].append(
            "Some papers lacked year metadata. Verify recent papers in PubMed or PMC."
        )
    if has_incomplete_citation(compact):
        summary["warnings"].append(
            "Some papers lacked complete citation metadata such as year or DOI."
        )
    if endpoint in ["/api/scan_literature_advanced", "/api/discover_literature"]:
        summary["warnings"].append(
            "Grouped scans improve recall for multi-concept biology queries."
        )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
