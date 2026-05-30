---
name: unitox-query
description: >
  Query the UniTox drug toxicity database. Use whenever the user asks about
  organ-system toxicity ratings for a drug, multi-organ toxicity profiles,
  or wants to look up any entity (drug name, SMILES, SPL_ID) in UniTox.
---

# UniTox Query Skill

Search UniTox records by any entity. Auto-detects type by pattern:

| Input Pattern | Detected As | Match Logic |
|---|---|---|
| `b2b3be70-17d8-...` (UUID) | SPL_ID | exact on `SPL_ID` |
| long string with `=`, `[`, `]`, `@` | SMILES | exact on `smiles` / `all_smiles` |
| anything else | free text | case-insensitive substring on `generic_name` |

## API

| Function | Input | Returns |
|---|---|---|
| `load_unitox(path)` | TSV path | list[dict] (cached) |
| `search(entity)` | single entity string | list[dict] |
| `search_batch(entities)` | list of entity strings | dict[str, list[dict]] |
| `summarize(hits, entity)` | hits + label | compact ratings-only text |
| `summarize_with_reasoning(hits, entity, systems)` | hits + label + organ list | text with truncated reasoning |
| `to_json(hits)` | hits | list[dict] (ratings + metadata) |
| `list_drugs()` | – | sorted list of all drug names |

## Toxicity Systems (8 organs)

Each drug has ternary rating (`No` / `Low` / `High`) and binary rating (`Yes` / `No`) for:

| System key | Organ |
|---|---|
| `cardiotoxicity` | Heart |
| `dermatological_toxicity` | Skin |
| `hematological` | Blood |
| `infertility` | Reproductive |
| `liver_toxicity` | Liver |
| `ototoxicity` | Ear / Hearing |
| `pulmonary_toxicity` | Lung |
| `renal_toxicity` | Kidney |

## Usage

See `if __name__ == "__main__"` block in `28_UniTox.py` for runnable examples covering: single drug name search, batch search, JSON output, detailed reasoning for specific organ systems, and total drug count.

## Data

- **Source**: UniTox v1 from Zenodo (https://zenodo.org/records/11627822)
- **Paper**: https://doi.org/10.1101/2024.06.21.24309315
- **Format**: CSV or TSV (delimiter auto-detected from header line)
- **Columns**: `generic_name`, 8 × (`*_reasoning`, `*_ternary_rating`, `*_binary_rating`), `smiles`, `all_smiles`, `SPL_ID`
- **Path**: `DATA_PATH` variable in `28_UniTox.py`
- **Method**: GPT-4o extraction from FDA drug labels; 85–96% clinician concordance
