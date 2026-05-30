---
name: rxnorm-query
description: >
  Query the RxNorm drug naming and normalization API. Use whenever the user asks
  to look up an RxCUI, normalize a drug name, find drug interactions, retrieve
  brand/trade names, or resolve any clinical drug name via RxNorm. Supports
  single drug or batch queries. Trigger on mentions of RxNorm, RxCUI, drug
  normalization, drug interaction lookup, or brand-name resolution.
---

# RxNorm Query Skill

Look up clinical drug information via the RxNorm REST API (no API key required).

## Capabilities

| Function | Input | Returns |
|---|---|---|
| `find_rxcui(name)` | drug name string | RxCUI string or None |
| `get_drug_info(rxcui)` | RxCUI string | full info dict |
| `get_drug_interactions(rxcui)` | RxCUI string | list of interaction dicts |
| `get_related_drugs(rxcui, tty)` | RxCUI + term type | list of related drug dicts |
| `normalize_drug_name(name)` | approximate drug string | normalized name string |
| `query(entity)` | **str or list[str]** | dict keyed by drug name |
| `summarize(results)` | output of `query()` | compact text summary |

## Quick Start

```python
from 08_RxNorm import query, summarize

# Single drug
results = query("aspirin")
print(summarize(results))

# Batch drugs
results = query(["tylenol", "metformin", "ibuprofen"])
print(summarize(results))
```

## `query()` Output Schema

```
{
  "<drug_name>": {
    "rxcui": "1191" | None,
    "normalized_name": "aspirin",
    "interactions": [
      {"description": "...", "severity": "...", "drugs": ["...", "..."]}
    ],
    "related": [
      {"rxcui": "...", "name": "...", "tty": "..."}
    ]
  }
}
```

## Notes

- **API**: RxNorm REST — `https://rxnav.nlm.nih.gov/REST`
- **Auth**: None required
- **Rate limits**: NLM asks for reasonable use; no hard key-based limit
- **Related drug types** (`tty`): `BN` (brand name), `SBD` (branded dose), `SCD` (clinical dose), etc.
