---
name: stitch-query
description: >
  Query the STITCH chemical-protein interaction database. Use whenever the user
  asks about chemical-protein interactions, drug-target binding, compound action
  modes, or wants to look up any entity (chemical name, STITCH CID, STRING
  protein ID) in STITCH.
---

# STITCH Query Skill

Search STITCH for chemical–protein interactions via REST API. Auto-detects input type:

| Input Pattern | Detected As | Example |
|---|---|---|
| `CIDm00002244` / `CIDs00002244` | STITCH chemical ID | direct lookup |
| `9606.ENSP00000352121` | STRING protein ID | direct lookup |
| anything else | free text | resolved via `/resolve` first |

## API

| Function | Input | Returns |
|---|---|---|
| `resolve(name, species)` | chemical / protein name | `list[dict]` with stringId, preferredName |
| `resolve_batch(names, species)` | list of names | `list[dict]` (via `/resolveList`) |
| `get_interactors(id, species, limit, required_score)` | single ID | `list[dict]` with partner IDs + scores |
| `get_actions(id, species, limit, required_score)` | single ID | `list[dict]` with mode (activation/inhibition/binding…) |
| `get_interactions(ids, species, required_score)` | list of IDs | `list[dict]` pairwise interactions among inputs |
| `search(entity, species, limit, required_score)` | single entity (any type) | `dict` with resolved_id, interactors, actions |
| `search_batch(entities, species, limit, required_score)` | list or comma-separated string | `dict[str, dict]` |
| `summarize(result, entity)` | search() result + label | compact text |
| `to_json(result)` | any result | JSON string |

## Key Fields

**Interactors** — `stringId_A`, `stringId_B`, `preferredName_A`, `preferredName_B`, `score`, `nscore`, `fscore`, `pscore`, `ascore`, `escore`, `dscore`, `tscore`

**Actions** — `stringId_A`, `stringId_B`, `preferredName_A`, `preferredName_B`, `mode` (activation / inhibition / binding / catalysis / reaction / expression / ptmod), `action`, `is_directional`, `a_is_acting`, `score`

## Score Channels

| Abbrev | Meaning |
|---|---|
| nscore | neighborhood (genomic context) |
| fscore | gene fusion |
| pscore | phylogenetic co-occurrence |
| ascore | co-expression |
| escore | experimental evidence |
| dscore | curated database evidence |
| tscore | text mining |
| score  | combined score (0–1000; 400=medium, 700=high, 900=highest) |

## Usage

See `if __name__ == "__main__"` block in `45_STITCH.py` for runnable examples covering: free-text name, STITCH CID, batch search, and JSON output.

## Data Source

- **Provider**: STITCH / STRING Consortium (EMBL, CPR, SIB, KU)
- **Primary URL**: `http://stitch.embl.de/api`
- **Fallback URL**: `https://string-db.org/api` (STITCH data merged into STRING 12+)
- **Auth**: None (public API; rate-limited — avoid parallel bulk requests)
- **Species**: Default 9606 (Homo sapiens); pass NCBI taxonomy ID for other organisms
