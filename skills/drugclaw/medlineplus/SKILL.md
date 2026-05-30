---
name: medlineplus-drug-info
description: >
  Query MedlinePlus for consumer-oriented drug and health-topic information.
  Accepts drug names, RxCUI codes, NDC codes, or ICD-10-CM diagnosis codes.
  Uses two free, keyless NLM APIs: the Web Service (keyword search) and
  MedlinePlus Connect (code-based lookup).
---

# MedlinePlus Drug Info Skill

Search MedlinePlus drug / health-topic pages. Auto-detects input type:

| Input Pattern | Detected As | Example | Endpoint Used |
|---|---|---|---|
| `0069-3060-30` | NDC code | NDC → drug page | Connect (NDC) |
| `637188` (5-7 digits) | RxCUI | RxNorm concept | Connect (RxCUI) |
| `E11.9`, `J45.20` | ICD-10-CM | Diagnosis code → topic | Connect (ICD-10) |
| anything else | free text | `metformin`, `aspirin` | Connect (name) + wsearch |

Both APIs are free, require no API key, and are rate-limited to 85 req/min.

## API

| Function | Input | Returns |
|---|---|---|
| `search(query, max_results=10)` | single entity string | `dict` with `connect_results`, `wsearch_results` |
| `search_batch(queries, max_results=10)` | list of entity strings | `dict[str, dict]` |
| `summarize(result)` | one `search()` result dict | compact text for LLM |
| `to_json(result)` | one `search()` result dict | `list[dict]` flat records |

### Result dict structure

```python
{
    "query": "metformin",
    "input_type": "text",          # ndc | rxcui | icd10 | text
    "connect_results": [           # from MedlinePlus Connect
        {"title": "...", "url": "...", "summary": "...", "source": "..."},
    ],
    "wsearch_results": [           # from keyword web service
        {"title": "...", "url": "...", "snippet": "...", "rank": "..."},
    ],
    "errors": [],
}
```

## Usage

See `if __name__ == "__main__"` block in `57_MEDLINEPLUS_DRUG_INFO.py` for
runnable examples covering: drug name, RxCUI, NDC, ICD-10, batch search,
summarize, and JSON output.

## Key Fields

| Field | Source | Description |
|---|---|---|
| `title` | Connect / wsearch | MedlinePlus page title |
| `url` | Connect / wsearch | Direct link to MedlinePlus page |
| `summary` | Connect | HTML-stripped page summary (≤400 chars) |
| `snippet` | wsearch | Keyword-in-context excerpt (≤300 chars) |
| `source` | Connect | Content attribution (e.g., AHFS, ASHP) |
| `rank` | wsearch | Relevance rank returned by NLM |

## Data Source

- **Provider**: U.S. National Library of Medicine (NLM)
- **Web Service**: `https://wsearch.nlm.nih.gov/ws/query` (XML, keyword search)
- **Connect API**: `https://connect.medlineplus.gov/service` (JSON, code-based)
- **Rate limit**: 85 requests / minute / IP
- **Update frequency**: daily (Tue–Sat)
- **License**: Public domain (U.S. Government work); attribution to MedlinePlus.gov requested
