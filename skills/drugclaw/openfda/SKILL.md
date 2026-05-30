---
name: openfda-human-drug
description: >
  Query FDA drug labeling data via openFDA. Use whenever the user asks about
  drug prescribing information — indications, warnings, dosage, adverse reactions,
  contraindications, or administration routes. Supports single or batch lookup
  by brand/generic name or by indication/condition.
---

# openFDA Human Drug Skill

Query structured SPL (Structured Product Labeling) data from the FDA. No API key needed (≤1 000 req/day).

## Input → Detection

| Input Example | Routed To |
|---|---|
| `"ASPIRIN"` or `["METFORMIN","LISINOPRIL"]` | `search_drug` — brand/generic name lookup |
| `"hypertension"` or `["diabetes","migraine"]` | `search_by_indication` — indication text search |
| *(no input)* | `count_by_route` — top administration routes |

All search functions accept **a single string or a list of strings**.

## API

| Function | Input | Returns |
|---|---|---|
| `search_drug(query, limit)` | str \| list[str], int | `{term: [label_dicts]}` |
| `search_by_indication(query, limit)` | str \| list[str], int | `{condition: [label_dicts]}` |
| `count_by_route(top_n)` | int | `[{term, count}]` |
| `summarize(results)` | dict from above | compact multi-line text |

Each `label_dict` contains: `brand_name`, `generic_name`, `manufacturer`, `route`, `substance_name`, `product_type`, `indications`, `contraindications`, `warnings`, `dosage`, `adverse_reactions`.

## Usage

See `if __name__ == "__main__"` block in `05_openFDA_Human_Drug.py` for runnable examples covering: single drug, batch drugs, single indication, batch indications, route counts, and raw JSON output.

## Notes

- Long text fields (`indications`, `warnings`, etc.) are truncated to keep payloads concise.
- On HTTP/query errors the result dict contains an `error` key for that term.
- Endpoint: `https://api.fda.gov/drug/label.json`
