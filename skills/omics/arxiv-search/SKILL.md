---
name: arxiv-search
description: Search arXiv preprints through the official arXiv API and turn arXiv IDs into local Markdown summaries. Use when you need CS, math, physics, or quantitative biology preprints, especially recent submissions that may not yet appear in peer-reviewed literature indexes.
user-invocable: true
---

# arXiv Search

Search arXiv through its official API for discovery, shortlisting, recent-preprint tracking, and local Markdown note generation from arXiv IDs.

## Instructions

1. Prefer this skill when the request is about arXiv-native preprints, recent submissions, or fields where arXiv coverage is strong: computer science, mathematics, physics, statistics, quantitative biology, and quantitative finance.
2. Use the bundled CLI:
   - In this repository: `skills/arxiv-search/scripts/search`
   - After installation: `~/.agents/skills/arxiv-search/scripts/search`
   - Markdown summary builder: `skills/arxiv-search/scripts/summarize`
3. The CLI supports two query modes:
   - Plain-text mode: bare words are converted into an `all:` query joined with `AND`
   - Raw mode: if the query already uses arXiv syntax such as `ti:`, `au:`, `abs:`, `cat:`, `submittedDate:`, `AND`, `OR`, or `ANDNOT`, it is passed through unchanged
4. For exact phrase matching in plain-text mode, add `--phrase`.
5. For recent-paper discovery, prefer `--sort submittedDate --order descending`, and optionally add `--days N`.
6. Use `--category <cat>` when the scope should stay narrow, for example `cs.LG`, `cs.AI`, `stat.ML`, or `q-bio.QM`.
7. For author-specific requests, do not rely on a single name form.
   - By default, run the supplied full-name form and an abbreviated-first-name form separately, for example `au:"Peter Nugent"` and `au:"P. Nugent"`.
   - Present these result sets separately in the final answer instead of silently merging them.
   - Call out that abbreviated-first-name matches can be ambiguous and may include a different person with the same initial and surname.
8. Treat arXiv API output as discovery metadata. If exact version, withdrawn status, or human-readable abstract-page details matter, verify the final candidates on arxiv.org before presenting a final answer.
9. If the user wants peer-reviewed biomedical full text rather than preprints, use `/polars-dovmed` instead.
10. If the user needs massive bulk harvesting rather than interactive search, the arXiv docs recommend OAI-PMH rather than large search result slices.
11. Use `scripts/summarize` when the user wants stable local notes for specific arXiv IDs. This writes Markdown files containing paper metadata, abstract, links, and a blank `## Notes` section for follow-up annotation.
12. Do not rely on server-side `submittedDate:[...]` queries for user-facing workflows. As observed on March 18, 2026 UTC, official arXiv API requests using `submittedDate` returned `HTTP 500` even for the example pattern shown in the arXiv API manual. The bundled CLI therefore applies `--days` as a local filter on returned `published` timestamps instead of sending `submittedDate` to the API.
13. Respect arXiv API pacing. The bundled CLI caches identical requests, coordinates a default 3.1-second minimum interval between API calls through a local state file, and retries `HTTP 429` responses with backoff. For broad discovery, still prefer one scoped query over many small queries.

## Quick Reference

| Task | Action |
|------|--------|
| Search script | `skills/arxiv-search/scripts/search` |
| Summary builder | `skills/arxiv-search/scripts/summarize` |
| Base API | `https://export.arxiv.org/api/query` |
| Default mode | Plain-text terms compiled to `all:` query terms |
| Raw query | Pass arXiv syntax directly, e.g. `cat:cs.LG AND ti:diffusion` |
| Author search | Run full-name and abbreviated-first-name `au:` queries separately, e.g. `au:"Peter Nugent"` and `au:"P. Nugent"` |
| Exact phrase | Add `--phrase` |
| Recent submissions | `--sort submittedDate --order descending` |
| Relative date filter | `--days 30` with local post-filtering |
| Category filter | `--category cs.LG` |
| ID lookup | `--ids 2501.01234,2406.00001` |
| Write local notes | `skills/arxiv-search/scripts/summarize 2501.01234 --output-dir arxiv-summaries` |
| Network timeout | `--timeout 20` |
| Pacing/cache | default `--min-interval 3.1`, `--retries 2`, `--retry-backoff 60`, cache under `~/.cache/omics-skills/arxiv-search` |
| Help | `skills/arxiv-search/scripts/search --help` |

## Input Requirements

- Python 3
- A search query or one or more arXiv IDs
- Reasonable request pacing for repeated calls:
  - arXiv recommends a 3-second delay between consecutive API requests
  - the CLI caches identical API URLs and uses a local pacing-state file by default
- For Markdown note generation:
  - one or more arXiv IDs
  - optional `--output-dir` (default: `arxiv-summaries`)
  - optional `--force` to overwrite existing files
- Optional search modifiers:
  - `--phrase` to treat the full plain-text query as one phrase
  - `--category <cat>` to constrain by arXiv category
  - `--days <N>` for a recent-submission window, applied locally to returned `published` timestamps
  - `--sort relevance|lastUpdatedDate|submittedDate`
  - `--order ascending|descending`
  - `--start <N>` for paging
  - `--timeout <seconds>` when the network is slow or partially blocked
- Optional pacing/cache modifiers:
  - `--min-interval <seconds>` to adjust the minimum interval between API calls across CLI invocations
  - `--retries <N>` and `--retry-backoff <seconds>` to adjust retry behavior for `HTTP 429`
  - `--cache-dir <path>` or `ARXIV_SEARCH_CACHE_DIR` to choose the local response cache and pacing-state directory
  - `--no-cache` to disable response-cache reads/writes while retaining pacing
- When writing raw queries, use official arXiv field prefixes and operators:
  - `ti`, `au`, `abs`, `co`, `jr`, `cat`, `rn`, `all`
  - `AND`, `OR`, `ANDNOT`
- For author-specific searches, prefer separate raw `au:` queries for the full name and abbreviated-first-name form rather than a single merged query.
- Avoid `submittedDate:[YYYYMMDDTTTT+TO+YYYYMMDDTTTT]` in routine use until arXiv-side failures are resolved.

## Output

- JSON with:
  - request metadata (`query`, `compiled_query`, `start`, `max_results`, `sort_by`, `sort_order`)
  - `query_mode` showing whether the CLI used raw or plain-text compilation
  - `days_filter` metadata when `--days` is used
  - `warnings` when the CLI applied local workarounds
  - feed metadata (`total_results`, `items_per_page`, `start_index`, `updated`)
  - normalized result records with:
    - `title`
    - `summary`
    - `authors`
    - `arxiv_id`
    - `abs_url`
    - `pdf_url`
    - `published`
    - `updated`
    - `primary_category`
    - `categories`
    - `comment`, `journal_ref`, `doi` when present
  - `request_url` for traceability
- For `scripts/summarize`:
  - JSON describing written files and missing IDs
  - one Markdown file per returned arXiv ID, containing metadata, abstract, citation, and a `## Notes` section

## Quality Gates

- [ ] Query mode is appropriate: plain-text convenience or raw arXiv syntax
- [ ] Result count is scoped tightly enough to inspect the first page of titles
- [ ] Recent-paper requests use `submittedDate` sorting and/or a date filter
- [ ] `--days` is understood as a local filter, not a server-side `submittedDate` query
- [ ] Category-sensitive requests use `--category` or raw `cat:` filters
- [ ] Author-specific requests check full-name and abbreviated-first-name variants separately
- [ ] The final answer keeps abbreviated-name matches separate and labels them as potentially ambiguous
- [ ] Final answer distinguishes arXiv preprints from peer-reviewed literature
- [ ] Exact metadata claims were verified on arxiv.org when version/date details matter
- [ ] Repeated calls are paced to avoid `HTTP 429 Rate exceeded`

## Examples

### Example 1: Recent ML preprints

```bash
skills/arxiv-search/scripts/search "protein language model" 10 \
  --phrase \
  --category cs.LG \
  --sort submittedDate \
  --order descending \
  --days 30
```

### Example 2: Raw arXiv query syntax

```bash
skills/arxiv-search/scripts/search \
  'cat:cs.LG AND ti:"diffusion" ANDNOT abs:"survey"' \
  15 \
  --sort relevance
```

### Example 3: Quantitative biology preprints

```bash
skills/arxiv-search/scripts/search "single cell foundation model" 10 \
  --phrase \
  --category q-bio.QM \
  --sort submittedDate \
  --order descending
```

### Example 4: Author-specific search with separate name variants

```bash
skills/arxiv-search/scripts/search 'au:"Peter Nugent"' 20 \
  --sort submittedDate \
  --order descending

skills/arxiv-search/scripts/search 'au:"P. Nugent"' 20 \
  --sort submittedDate \
  --order descending
```

### Example 5: Fetch records by arXiv ID

```bash
skills/arxiv-search/scripts/search --ids 2501.01234,2406.00001
```

### Example 6: Build local Markdown summaries from arXiv IDs

```bash
skills/arxiv-search/scripts/summarize 2501.01234 2406.00001 \
  --output-dir arxiv-summaries
```

## Troubleshooting

**Issue**: Results are too broad  
**Solution**: Add `--category`, narrow the terms, or switch to a raw query with `ti:`/`abs:` fields.

**Issue**: Results are too sparse  
**Solution**: Remove an overly narrow category, drop `--phrase`, or use `OR` in a raw query.

**Issue**: Need the latest papers, not the most relevant  
**Solution**: Use `--sort submittedDate --order descending`, and add `--days N` when you want a recent window. The CLI applies the `--days` cutoff locally to avoid current arXiv API failures on `submittedDate` queries.

**Issue**: Need exact author or title matching  
**Solution**: Use a raw query with field prefixes such as `au:` and `ti:` rather than plain-text mode. For author searches, run full-name and abbreviated-first-name variants separately and report them separately.

**Issue**: Author search looks fragmented across name variants  
**Solution**: This is common on arXiv. Check both the full-name form and the abbreviated-first-name form, for example `au:"Peter Nugent"` and `au:"P. Nugent"`, then keep those result sets separate in the final answer because the abbreviated form may be ambiguous.

**Issue**: Need more than an interactive page of results  
**Solution**: Use `--start` for paging. For very large harvesting jobs, switch to OAI-PMH or bulk metadata workflows instead of pulling huge API slices.

**Issue**: The request hangs or times out  
**Solution**: Retry with a smaller `max_results`, increase `--timeout` modestly, or verify whether arXiv is reachable from the current environment.

**Issue**: Need reusable local notes instead of JSON search output  
**Solution**: Use `skills/arxiv-search/scripts/summarize <arxiv-id>... --output-dir <dir>` to create Markdown summaries.

**Issue**: Recent-date filtering returns an arXiv server error  
**Solution**: Do not send raw `submittedDate:[...]` filters in normal use. Prefer `--sort submittedDate --order descending --days N`, which uses local published-date filtering in the bundled CLI.

**Issue**: `HTTP 429 Rate exceeded`  
**Solution**: The CLI now caches identical API URLs, waits at least 3.1 seconds between API calls, and retries 429 responses with backoff. If 429 persists, wait several minutes, reduce query count, use one broad query plus local filtering, reuse cached JSON, or verify final IDs on official arxiv.org abstract pages.

## Related Skills

- `/crossref-lookup` — resolve citation metadata from arXiv DOIs
- `/polars-dovmed` — switch here if the query wants peer-reviewed PMC full text instead of preprints
