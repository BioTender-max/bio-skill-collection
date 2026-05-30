# DILI Skill

## Runtime Mode

`DILISkill` uses live ChEMBL REST endpoints for hepatotoxicity-related evidence.

## Canonical Local Fixture (Example Surface)

`example.py` uses the canonical packaged offline file:

- `resources_metadata/drug_toxicity/DILI/dili.csv`
- Columns: `drug`, `warning_type`, `molecule_chembl_id`

## Example API

- `load_dili(path=DATA_PATH)` -> `list[dict]`
- `query_dili(entities, data_path=DATA_PATH)` -> `list[dict]`

`query_dili` returns records in the shape expected by `retrieve.py`:
`source`, `match_count`, and `matches` (or `{"error": ...}`).
