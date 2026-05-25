---
name: biorxiv-search
description: Search bioRxiv preprints through the official bioRxiv API and locally filter titles, abstracts, and authors for keyword queries. Use when you need recent biology preprints, bioRxiv-native metadata, date-range scans, DOI lookups, or author shortlists that may not yet appear in peer-reviewed literature indexes.
---

# bioRxiv Search

Search bioRxiv through its official API for recent-preprint discovery, date-range scans, DOI lookups, author shortlisting, and local keyword filtering over title, abstract, and author metadata.

## Instructions

1. Prefer this skill when the request is about bioRxiv-native preprints, recent biology submissions, or preprint metadata that may lag in PubMed, PMC, or Crossref.
2. Use the bundled CLI:
   - In this repository: `skills/biorxiv-search/scripts/search`
   - After installation: `~/.agents/skills/biorxiv-search/scripts/search`
3. The official bioRxiv API does not provide a general server-side keyword search endpoint.
   - Use the CLI to fetch metadata from a bounded recent window or explicit date range, then filter locally.
4. When keywords are provided, search `title`, `abstract`, and `authors` by default.
   - If the user wants abstract-only matching, pass `--fields abstract`.
5. Keep the search window bounded.
   - Use `--days N` for recent scans or `--start-date YYYY-MM-DD --end-date YYYY-MM-DD` for explicit intervals.
   - If you omit the interval, the CLI defaults to the most recent 30 days.
   - The CLI converts `--days N` into an explicit date range before calling the API so pagination stays predictable.
6. Use `--category <name>` when the topic should stay narrow.
   - The API accepts the bioRxiv category as a query parameter such as `cell_biology`, `genomics`, or `neuroscience`.
7. Use `--author` for author-specific requests.
   - By default, consider both the supplied full-name form and an abbreviated-first-name form, for example `--author "Peter Nugent"` and `--author "P. Nugent"`.
   - Do not silently merge these in the final answer. Report full-name matches and abbreviated-first-name matches in separate groups because initials can be ambiguous.
   - The CLI also expands obvious first-initial variants from the supplied author string, so prefer separate passes or a local partition of returned records by the literal `authors` text when you need clean buckets.
8. The API paginates 100 records at a time.
   - Increase `--scan-limit` when the query is broad and the first pages do not contain enough matches.
9. By default, the CLI collapses multiple versions of the same preprint and keeps the latest version for each DOI.
   - Use `--all-versions` only when version-by-version output matters.
10. Treat the API output as discovery metadata.
   - If exact citation details or the latest abstract-page presentation matter, verify the shortlisted candidates on bioRxiv or the DOI landing page before finalizing the answer.
11. If the user wants peer-reviewed biomedical literature or PMC full text rather than bioRxiv preprints, use `polars-dovmed` instead.

## Quick Reference

| Task | Action |
|------|--------|
| Search script | `skills/biorxiv-search/scripts/search` |
| Base API | `https://api.biorxiv.org/details/biorxiv/...` |
| Default search fields | `title,abstract,authors` |
| Recent window | `--days 30` |
| Date range | `--start-date YYYY-MM-DD --end-date YYYY-MM-DD` |
| DOI lookup | `--doi 10.1101/...` |
| Category filter | `--category cell_biology` |
| Author filter | `--author "Name"` |
| Author variant workflow | Check full-name and abbreviated-first-name variants separately; report them separately |
| Abstract-only filtering | `--fields abstract` |
| Deduping | latest version per DOI by default |
| Keep all versions | `--all-versions` |
| Network timeout | `--timeout 30` |
| Help | `skills/biorxiv-search/scripts/search --help` |

## Input Requirements

- Python 3
- One of:
  - a keyword query
  - a bioRxiv DOI via `--doi`
  - a request for recent/date-bounded preprints with no keyword query
- Optional interval controls:
  - `--days <N>` for the most recent `N` days
  - `--start-date YYYY-MM-DD --end-date YYYY-MM-DD` for an explicit date range
- Optional filters:
  - `--category <name>` for a bioRxiv subject category
  - `--author <name>` repeated for author substrings or name variants
  - `--fields title,abstract,authors` to restrict local keyword matching
  - `--phrase` to treat the whole query as one phrase instead of splitting on spaces
  - explicit `OR` in the query for broader local matching
  - `--scan-limit <N>` for how many API records to inspect locally
  - `--all-versions` to keep multiple versions of the same DOI
- If the user asks for very old or very broad searches, widen the date range deliberately and be explicit that recall depends on the chosen interval and `--scan-limit`.

## Search Semantics

- The official bioRxiv API supports:
  - recent-post windows such as `30d`
  - explicit date ranges
  - DOI lookup
  - subject-category filtering
- The API does not support a general server-side keyword query for title or abstract.
  - The CLI performs local filtering after fetching metadata.
- For predictable paging, the CLI implements `--days N` as an explicit UTC date range instead of relying on the API's relative-date shorthand.
- Plain multi-word queries are local `AND` queries.
  - `single cell atlas` means all three terms must appear somewhere in the selected search fields.
- `OR` must be written explicitly to broaden synonyms or alternate phrasings.
  - `"organoid OR spheroid"`
  - `"CRISPR OR Cas9"`
- Quoted phrases are preserved when possible.
  - `"\"single cell\" atlas"` keeps `single cell` as one phrase and also requires `atlas`.
- `--fields abstract` restricts keyword filtering to abstracts only.
  - This is the flag to use when the user explicitly cares about abstract matches.
- Author filters can fragment across name variants.
  - For person-specific searches, check the full-name form and abbreviated-first-name form separately and keep those buckets separate in the final answer.

## Output

- JSON with:
  - request metadata (`query`, `query_groups`, interval, category, author filters, search fields)
  - API metadata (`pages_fetched`, `records_scanned`, `total_available`, `request_urls`)
  - warnings about defaulted windows, scan-limit truncation, or API limitations
  - normalized result records with:
    - `doi`
    - `title`
    - `authors`
    - `date`
    - `version`
    - `category`
    - `abstract`
    - `published`
    - `doi_url`
    - `biorxiv_url`
    - `matched_in`

## Quality Gates

- [ ] The request uses a bounded recent window or explicit date range
- [ ] The chosen `--scan-limit` is large enough for the query breadth
- [ ] The selected search fields match the user request, especially when abstract matching matters
- [ ] Author-specific requests use one or more reasonable name variants
- [ ] The final answer keeps abbreviated-name matches separate and labels them as potentially ambiguous
- [ ] The answer does not overstate recall for a broad historical search
- [ ] Final candidate metadata is verified on bioRxiv when exact citation/version details matter

## Examples

### Example 1: Recent keyword scan over title + abstract

```bash
skills/biorxiv-search/scripts/search "single cell atlas" 10 --days 30
```

### Example 2: Broaden with `OR`

```bash
skills/biorxiv-search/scripts/search '"organoid OR spheroid"' 15 \
  --days 90 \
  --category developmental_biology
```

### Example 3: Abstract-only keyword filtering

```bash
skills/biorxiv-search/scripts/search "CRISPR screen" 10 \
  --days 60 \
  --fields abstract
```

### Example 4: Author-specific search with separate variant reporting

```bash
skills/biorxiv-search/scripts/search "supernova" 20 \
  --days 365 \
  --author "Peter Nugent" \
  --author "P. Nugent"
```

### Example 5: DOI lookup

```bash
skills/biorxiv-search/scripts/search --doi 10.1101/682021
```

## Troubleshooting

**Issue**: Results are too broad  
**Solution**: Narrow the interval, add `--category`, restrict with `--fields`, or replace a loose query with a phrase or explicit `OR` terms.

**Issue**: Results are too sparse  
**Solution**: Increase `--days` or widen the date range, raise `--scan-limit`, and add alternate query terms with explicit `OR`.

**Issue**: Need abstract matches, not title matches  
**Solution**: Use `--fields abstract`.

**Issue**: Author search looks incomplete  
**Solution**: Repeat `--author` with explicit variants such as `"Peter Nugent"` and `"P. Nugent"`. If a middle initial is known, add that too, for example `"Peter E. Nugent"` and `"P. E. Nugent"`. Keep these result sets separate in the final answer because abbreviated forms can be ambiguous.

**Issue**: The API returns multiple versions of the same preprint  
**Solution**: Keep the default deduped output, or pass `--all-versions` if version-level output matters.

**Issue**: Broad historical search may be missing expected hits  
**Solution**: This usually means the interval or `--scan-limit` was too narrow. Widen them deliberately and say so in the final answer.

**Issue**: Need peer-reviewed literature rather than preprints  
**Solution**: Use `polars-dovmed` or another peer-reviewed-literature workflow instead of bioRxiv metadata search.

## Related Skills

- `/crossref-lookup` — resolve citation metadata from bioRxiv DOIs
- `/polars-dovmed` — switch here if the query wants peer-reviewed PMC full text instead of preprints
