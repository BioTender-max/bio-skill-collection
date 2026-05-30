---
name: WHO-EML-query
description: >
  Query the WHO Model List of Essential Medicines (23rd list, 2023).
  Use whenever the user asks about essential medicines, WHO-recommended drugs,
  dosage forms, therapeutic sections, or AWaRe antibiotic classification.
---

# WHO Essential Medicines List Query Skill

Search ~500 WHO essential medicines by name, section, or section number. Case-insensitive substring match.

| Input Example | Matches On |
|---|---|
| `amoxicillin` | medicine name |
| `antimalarial` | section hierarchy (full path) |
| `diabetes` | section hierarchy |
| `6.2` | section_num prefix |

## API

| Function | Input | Returns |
|---|---|---|
| `load_eml(cache_path)` | JSON path | list[dict] |
| `build_cache(pdf_path, cache_path)` | PDF + cache paths | list[dict] (parses PDF → JSON) |
| `search(data, entity)` | single string | list[dict] |
| `search_batch(data, entities)` | list of strings | dict[str, list[dict]] |
| `summarize(hits, entity)` | list[dict] + label | compact text |
| `to_json(hits)` | list[dict] | list[dict] |

## Record Schema

| Field | Example |
|---|---|
| `medicine` | `amoxicillin` |
| `section_num` | `6.2.1` |
| `section_name` | `Anti-infective medicines > Antibacterials > Access group antibiotics` |
| `dosage_forms` | `["Capsule: 250 mg; 500 mg", "Oral liquid: 125 mg/5 mL"]` |

## Usage

See `if __name__ == "__main__"` block in `59_WHO_EML.py` for runnable examples.

## Data

- **Source**: WHO Model List of Essential Medicines – 23rd List (2023)
- **PDF**: `WHO EML 23rd List (2023).pdf` in `DATA_DIR`
- **Cache**: `who_eml_23.json` (auto-built on first run from PDF)
- **License**: CC BY-NC-SA 3.0 IGO
- **Dependency**: `pip install pypdf`
