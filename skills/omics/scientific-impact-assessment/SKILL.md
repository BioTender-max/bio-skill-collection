---
name: scientific-impact-assessment
description: Assess paper and journal impact using OpenAlex citation counts, optional Altmetric data, and curated journal impact-factor references. Use when comparing papers, journals, or literature shortlists by reach and influence.
---

# Scientific Impact Assessment

Use this skill to measure the reach of a paper with citation, attention, and journal-level context.

## Instructions

1. Prefer a DOI or OpenAlex work ID as input.
   - If you only have a title, use `/crossref-lookup` first to resolve a DOI before running this skill.
2. Use the bundled CLI:
   - In this repository: `skills/scientific-impact-assessment/scripts/measure-impact`
   - After installation: `~/.agents/skills/scientific-impact-assessment/scripts/measure-impact`
3. OpenAlex is the default source for paper-level citation data.
   - The CLI retrieves `cited_by_count`, publication year, journal/source name, and citation history from OpenAlex.
4. Altmetric is optional and should be treated as conditional enrichment.
   - Current Altmetric documentation says an API key is required for Details Page API access.
   - If `ALTMETRIC_API_KEY` is not available, the CLI should report Altmetric as unavailable instead of failing.
5. Journal-level impact factors come from the curated references table in `references/journal_metrics_2024.tsv`.
   - These are curated public web values, mostly from official publisher pages.
   - The `Science` row uses a labeled third-party fallback because no public official AAAS JIF page was located during skill creation on March 19, 2026.
6. Keep paper-level and journal-level metrics separate in the final answer.
   - Do not present journal impact factor as a proxy for article quality.
   - Do not present Altmetric attention as equivalent to scholarly citation impact.
7. If the journal is not in the curated table, return the OpenAlex result anyway and say the journal-level reference lookup was not available.

## Quick Reference

| Task | Action |
|------|--------|
| Measure by DOI | `skills/scientific-impact-assessment/scripts/measure-impact --doi 10.1038/s41586-024-00000-0` |
| Measure by OpenAlex ID | `skills/scientific-impact-assessment/scripts/measure-impact --openalex-id W2741809807` |
| Add OpenAlex polite-pool email | `--mailto you@example.org` |
| Enable Altmetric enrichment | `--altmetric-api-key "$ALTMETRIC_API_KEY"` |
| Text summary output | `--format text` |
| Save JSON report | `--output impact-report.json` |
| Journal metrics table | `references/journal_metrics_2024.tsv` |
| Deployment regression test | `python3 -m unittest tests/test_scientific_impact_assessment.py -v` |

## Input Requirements

- Python 3
- One of:
  - `--doi <doi>`
  - `--openalex-id <id>`
- Optional:
  - `--mailto <email>` for OpenAlex polite-pool identification
  - `--altmetric-api-key <key>` or `ALTMETRIC_API_KEY`
  - `--output <path>`
  - `--format json|text`

## Output

- OpenAlex-derived paper metadata including:
  - title
  - DOI
  - OpenAlex ID
  - publication year
  - citation count
  - citation history by year
  - journal/source name
- Altmetric summary when an API key is available and the record exists
- curated journal-level impact-factor context when the journal matches the bundled references table
- explicit status values when Altmetric or journal-level lookup is unavailable

## Quality Gates

- [ ] The input is resolved to a DOI or OpenAlex work ID before lookup
- [ ] OpenAlex citation data is reported separately from journal-level metrics
- [ ] Altmetric is marked optional and unavailable when no API key is configured
- [ ] Journal impact factors are read from the bundled references table, not improvised from memory
- [ ] Any third-party journal metric source is labeled as such in the output

## Examples

### Example 1: DOI-based report

```bash
skills/scientific-impact-assessment/scripts/measure-impact \
  --doi 10.1038/s41586-024-00000-0 \
  --format text
```

### Example 2: OpenAlex ID plus Altmetric

```bash
skills/scientific-impact-assessment/scripts/measure-impact \
  --openalex-id W2741809807 \
  --mailto you@example.org \
  --altmetric-api-key "$ALTMETRIC_API_KEY" \
  --output impact-report.json
```

## Troubleshooting

**Issue**: Altmetric is always unavailable.  
**Solution**: Check whether `ALTMETRIC_API_KEY` is set. Current Altmetric docs require a key for all Details Page API endpoints.

**Issue**: The journal-level lookup is empty.  
**Solution**: The journal is probably not in `references/journal_metrics_2024.tsv` yet. Return the OpenAlex paper metrics and add the journal later if you can source a public metric page.

**Issue**: Only a title is available.  
**Solution**: Resolve the title to a DOI first with `/crossref-lookup`, then rerun this skill using the DOI for a deterministic lookup.

## Related Skills

- `/crossref-lookup` — resolve DOIs before scoring impact
- `/polars-dovmed` — retrieve the full text that backs the impact claim
