---
name: 52_NDF_RT
description: >
  Query NDF-RT (National Drug File Reference Terminology) via the NCI EVS REST
  API. Use when looking up drug mechanisms of action, physiological effects,
  pharmacologic classes, chemical structures, or drug–disease relationships
  (may_treat / may_prevent) in NDF-RT. Accepts drug names or NDF-RT codes.
---

# NDF-RT Query Skill

Search NDF-RT concepts by drug name or NDF-RT code via the NCI EVS REST API.
Auto-detects entity type by pattern:

| Input Pattern | Detected As | Lookup Logic |
|---|---|---|
| `N0000145918` | NDF-RT code (`N` + 10 digits) | direct concept GET |
| anything else | free text | full-text search endpoint |

## API

| Function | Input | Returns |
|---|---|---|
| `search(entity, limit)` | single entity string | `dict` with `entity`, `type`, `results` |
| `search_batch(entities, limit)` | list of entity strings | `dict[str, dict]` |
| `summarize(result, entity)` | search result dict + label | compact multi-line text |
| `to_json(result)` | search result dict | `list[dict]` |

### Result dict structure

Each item in `results` contains:

| Key | Description |
|---|---|
| `code` | NDF-RT concept code |
| `name` | Preferred concept name |
| `kind` | Concept kind (e.g. `DRUG_KIND`, `DISEASE_KIND`) |
| `properties` | flat `{type: value}` property dict |
| `roles` | list of `{type, relatedCode, relatedName}` role relationships |
| `parents` | list of `{code, name}` ISA parent concepts |
| `synonyms` | deduplicated list of synonym strings |

### Key NDF-RT relationship types (roles)

| Role | Meaning |
|---|---|
| `has_MoA` | mechanism of action |
| `has_PE` | physiological effect |
| `has_EPC` | established pharmacologic class |
| `may_treat` | indicated disease/condition |
| `may_prevent` | preventable disease/condition |
| `CI_with` | contraindicated with |
| `has_Chemical_Structure` | chemical structure classification |

## Usage

See `if __name__ == "__main__"` block in `52_NDF_RT.py` for runnable examples
covering: drug name search, code lookup, batch search, JSON output, and root
concept listing.

## Data

- **Source**: NCI EVS REST API (`https://api-evsrest.nci.nih.gov/api/v1`)
- **Terminology**: `ndfrt`
- **Auth**: none required
- **Rate limits**: not documented; use reasonable request spacing
- **Maintainer**: U.S. Department of Veterans Affairs / NCI Enterprise Vocabulary Services
