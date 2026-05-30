---
name: phee-query
description: >
  Query the PHEE pharmacovigilance event extraction dataset. Use whenever the
  user asks about annotated adverse drug events, pharmacovigilance case reports,
  drug–effect associations from medical literature, or wants to find PHEE
  examples mentioning a drug name, adverse effect, or condition.
---

# PHEE Query Skill

Search PHEE annotated pharmacovigilance events by drug name, adverse effect,
or free text. Substring matching is case-insensitive across all event fields.

| Input Pattern | Match Logic |
|---|---|
| drug name (e.g. `phenytoin`) | substring on `drug`, `treatment`, `combination_drug`, and `text` |
| adverse effect (e.g. `hepatotoxicity`) | substring on `effect`, `treatment_disorder`, and `text` |
| any other text | substring on all event fields and full sentence |

## API

| Function | Input | Returns |
|---|---|---|
| `load_phee(data_dir)` | directory path | list[dict] (cached) |
| `search(records, entity)` | single entity string | list[dict] |
| `search_batch(records, entities)` | list of entity strings | dict[str, list[dict]] |
| `summarize(hits, entity)` | hit list + label | compact text (sentence count, ADE/PTE counts, top drugs & effects) |
| `to_json(hits)` | hit list | list[dict] |

## Record Schema

Each record returned by `search`:

```
{
  "id": "8908396_3",
  "text": "A 52-year-old Black woman on phenytoin therapy ...",
  "split": "train",
  "events": [
    {
      "event_type": "Adverse_event | Potential_therapeutic_event",
      "trigger": ["developed"],
      "subject": ["A 52-year-old Black woman ..."],
      "subject_age": ["52-year-old"],
      "subject_gender": ["woman"],
      "subject_race": ["Black"],
      "subject_population": [],
      "subject_disorder": ["post-traumatic epilepsy"],
      "treatment": ["phenytoin therapy ..."],
      "drug": ["phenytoin"],
      "dosage": [],
      "freq": [],
      "route": [],
      "duration": [],
      "treatment_disorder": ["post-traumatic epilepsy"],
      "combination_drug": [],
      "effect": ["transient hemiparesis"]
    }
  ]
}
```

## Usage

See `if __name__ == "__main__"` block in `38_PHEE.py` for runnable examples
covering: single drug search, single effect search, batch search, and JSON
output.

## Data

- **Source**: PHEE dataset (Zenodo record 7689970), EMNLP 2022
- **Files**: `train.json` (~2,900 sentences), `dev.json` (~960), `test.json` (~960)
- **Path**: `DATA_DIR` variable in `38_PHEE.py`
  (`resources_metadata/drug_nlp/PHEE/data/json`)
- **Event types**: `Adverse_event`, `Potential_therapeutic_event`
- **Main arguments**: Subject, Treatment, Effect
- **Sub-arguments**: Subject (age, gender, race, population, disorder); Treatment (drug, dosage, freq, route, duration, disorder, combination.drug)
