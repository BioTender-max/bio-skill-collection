---
name: cadec-query
description: >
  Query the CADEC (CSIRO Adverse Drug Event Corpus). Use whenever the user asks
  about adverse drug event mentions in consumer health text, entity annotations
  from patient forum posts, MedDRA/SNOMED-CT normalised ADR spans, or wants to
  look up drugs, symptoms, or coded entities in the CADEC corpus.
---

# CADEC Query Skill

Search CADEC annotated patient forum posts by any entity. Auto-detects type:

| Input Pattern | Detected As | Match Logic |
|---|---|---|
| `10019211` (8 digits) | MedDRA code | exact on normalizations.code |
| `22253000` (6-18 digits) | SNOMED CT code | exact on normalizations.code |
| anything else | free text | substring on entity text, type, or doc_id |

## API

| Function | Input | Returns |
|---|---|---|
| `load_cadec(path)` | JSON path | list[dict] (cached) |
| `search(entity)` | single entity string | list[dict] |
| `search_batch(entities)` | list of entity strings | dict[str, list[dict]] |
| `summarize(hits, entity)` | hits + label | compact text |
| `to_json(hits)` | list[dict] | same list (JSON-ready) |

## Entity Types in Corpus

| Type | Description |
|---|---|
| ADR | Adverse Drug Reaction |
| Drug | Medication mention |
| Disease | Pre-existing condition |
| Symptom | Patient-reported symptom |
| Finding | Clinical finding |

## Usage

See `if __name__ == "__main__"` block in `34_CADEC.py` for runnable examples:
drug name search, ADR text search, MedDRA code lookup, batch search, JSON output.

## Data

- **Source**: CADEC v2, CSIRO (AskaPatient.com forum posts)
- **Local file**: `cadec_combined.json` built from BRAT `.txt` + `.ann` files
- **Annotations**: Original spans + MedDRA + SNOMED CT normalisations
- **Stats**: ~1,250 documents, ~7,600 entity annotations
- **Path**: `DATA_PATH` variable in `34_CADEC.py`
- **Citation**: Karimi et al., 2015. *J Biomed Inform* 55:73–81
