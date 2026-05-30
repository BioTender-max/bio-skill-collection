---
name: fda-orange-book-query
description: >
  Query or inspect the FDA Orange Book - FDA-Approved Drug Products Listing resource for drug-centric tasks with emphasis on drug knowledgebase Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# FDA Orange Book - FDA-Approved Drug Products Listing

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `65_FDA_Orange_Book.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Drug Knowledgebase`

## API Surface

| Function | Purpose |
|---|---|
| `download_orange_book()` | See `65_FDA_Orange_Book.py` for exact input/output behavior. |
| `search_approved_drugs()` | See `65_FDA_Orange_Book.py` for exact input/output behavior. |
| `get_drug_approval_info()` | See `65_FDA_Orange_Book.py` for exact input/output behavior. |
| `preview_products_file()` | See `65_FDA_Orange_Book.py` for exact input/output behavior. |

## Usage

Read `65_FDA_Orange_Book.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `maintainers/smoke/65_FDA_Orange_Book_smoke_test.py`
- Run: `python maintainers/smoke/65_FDA_Orange_Book_smoke_test.py`

## Notes

- Review `if __name__ == "__main__"` in `65_FDA_Orange_Book.py` first when generating runnable query code.
- Primary link from the example: <https://www.accessdata.fda.gov/scripts/cder/ob/>
- The repository does not keep monthly Orange Book snapshots under version control; on network failure the example writes a tiny built-in offline fixture for smoke testing.
- Inspect the validation script directly for its current assertions and sample entities.

## Data Source

- <https://www.accessdata.fda.gov/scripts/cder/ob/>
- <https://api.fda.gov/drug/ndc.json>
