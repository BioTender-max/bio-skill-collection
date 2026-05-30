# LiverTox Lookup Skill

## Description

Lookup LiverTox drug entries using the canonical packaged fixture file.

## Data

- Path: `resources_metadata/drug_toxicity/LiverTox/livertox.json`
- Schema: list of objects with `drug`, `title`, `ncbi_book_id`

## API

- `load_documents(path=DATA_PATH)` -> `list[dict]`
- `lookup_entities(entities)` -> `dict[str, list[dict]]`

`lookup_entities` returns up to 5 matches per entity with `section` and `snippet`
fields used by `retrieve.py`.
