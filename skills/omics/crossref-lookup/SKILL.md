---
name: crossref-lookup
description: Query the Crossref REST API for DOI validation, title search, citation metadata, and bibliography audits. Use when you need DOI lookup, title-to-DOI matching, or reference metadata cleanup.
---

# Crossref Lookup

Use this skill for citation metadata work backed by the Crossref REST API.

## Instructions

1. Prefer this skill when the user needs DOI validation, title search, citation metadata, or bibliography auditing.
2. Use the bundled CLI:
   - In this repository: `skills/crossref-lookup/scripts/lookup`
   - After installation: `~/.agents/skills/crossref-lookup/scripts/lookup`
3. Choose the narrowest mode that matches the request:
   - `--doi` for validating or enriching one DOI
   - `--title` for title-to-DOI discovery
   - `--validate-file` for one DOI per line
   - `--audit-bibliography` for a bibliography file such as `.bib` or plain text
4. Normalize DOI strings before interpreting failures.
   - Acceptable raw forms include `10.xxxx/...`, `doi:10.xxxx/...`, and `https://doi.org/10.xxxx/...`
5. If the user has a contact email for polite-pool requests, pass it with `--email`.
6. Treat Crossref as citation metadata, not full text.
   - If exact abstract-page wording, final pagination, or publisher formatting matters, verify the shortlisted record on the publisher or DOI landing page.
7. When title search returns multiple plausible records, keep the ambiguity explicit instead of selecting a match silently.

## Quick Reference

| Task | Action |
|------|--------|
| Validate DOI | `skills/crossref-lookup/scripts/lookup --doi 10.1038/nature12373` |
| Search by title | `skills/crossref-lookup/scripts/lookup --title "CRISPR-Cas9 genome editing"` |
| Validate a DOI list | `skills/crossref-lookup/scripts/lookup --validate-file dois.txt` |
| Audit bibliography | `skills/crossref-lookup/scripts/lookup --audit-bibliography refs.bib` |
| Citation style | `--style apa|vancouver|ama|ieee|chicago` |
| Write to file | `--output crossref-report.txt` |
| Polite-pool email | `--email you@example.org` |

## Input Requirements

- Python 3 with network access
- One of:
  - a DOI via `--doi`
  - a title via `--title`
  - a file path for `--validate-file`
  - a bibliography file path for `--audit-bibliography`
- Optional:
  - `--style` for formatted citation output
  - `--output` for saving the report
  - `--email` for the Crossref user agent

## Output

- DOI validation status and normalized DOI when `--doi` is used
- title, journal, year, and formatted citation when metadata is found
- ranked title-search candidates for `--title`
- summary counts plus invalid/error entries for file validation and bibliography audits
- optional output file if `--output` is set

## Quality Gates

- [ ] The lookup mode matches the user request
- [ ] DOI inputs are normalized before treating them as invalid
- [ ] Ambiguous title matches are presented as candidates rather than a silent single answer
- [ ] Citation formatting uses the requested style when style matters
- [ ] The final answer distinguishes Crossref metadata from publisher full text

## Examples

### Example 1: Validate a DOI

```bash
skills/crossref-lookup/scripts/lookup --doi "10.1038/nature12373"
```

### Example 2: Search by title

```bash
skills/crossref-lookup/scripts/lookup \
  --title "CRISPR-Cas9 genome editing" \
  --email you@example.org
```

### Example 3: Audit a bibliography

```bash
skills/crossref-lookup/scripts/lookup \
  --audit-bibliography refs.bib \
  --output crossref-audit.txt
```

## Troubleshooting

**Issue**: The DOI looks valid but Crossref says it is missing.  
**Solution**: Normalize the DOI first and retry. If it still fails, report that Crossref did not return a record instead of assuming publisher error.

**Issue**: Title search returns multiple plausible matches.  
**Solution**: Return the shortlist with DOI, journal, and year so the user can disambiguate.

**Issue**: Bibliography audit reports missing DOIs for many entries.  
**Solution**: Treat that as a coverage gap, not proof that the citations are invalid. Crossref metadata may be incomplete for some records.

## Related Skills

- `/polars-dovmed` — full-text PMC Open Access search when the DOI is unknown
- `/arxiv-search` — source-native preprint search on arXiv
- `/biorxiv-search` — source-native preprint search on bioRxiv
- `/scientific-impact-assessment` — citation counts and journal impact
