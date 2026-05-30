---
name: faers-query
description: >
  Query the FDA Adverse Event Reporting System (FAERS) via openFDA API.
  Use whenever the user asks about adverse drug reactions, side effects,
  drug safety signals, or wants to look up reported adverse events for
  one or more drug names.
---

# FAERS Query Skill

Query adverse event reports from FDA's FAERS database. No API key required.

## API

| Function | Input | Returns |
|---|---|---|
| `get_metadata()` | — | `{total, last_updated}` |
| `count_reactions(drug, top_n)` | single drug name | `[{term, count}, ...]` |
| `count_reactions_batch(drugs, top_n)` | list of drug names | `{drug: [{term, count}, ...]}` |
| `search_adverse_events(drug, limit)` | single drug name | raw openFDA response dict |
| `summarize_reactions(reactions, drug)` | reaction list + label | compact one-line text |

## Usage

See `if __name__ == "__main__"` block in `faers_query.py` for runnable examples covering: single drug query, batch query, metadata retrieval, raw report inspection, and LLM-friendly summary output.

## Notes

- Drug names should be uppercase (auto-converted internally).
- Input accepts a single string or a list of strings for batch queries.
- `summarize_reactions` produces compact `DRUG: reaction(count), ...` format suitable for LLM context.
- Source: openFDA Drug Adverse Events endpoint (`https://api.fda.gov/drug/event.json`).
