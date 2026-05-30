---
name: ADReCS-query
description: >
  Query the ADReCS (Adverse Drug Reaction Classification System) v3.3 database.
  Use whenever the user asks about adverse drug reactions, drug safety profiles,
  ADR classification, ADR severity/frequency, or wants to look up any entity
  (drug name, BADD Drug ID, DrugBank ID, ATC code, CAS RN, PubChem CID, KEGG ID,
  ADR term, ADReCS ID, MedDRA code, MeSH ID) in ADReCS.
---

# ADReCS Query Skill

Search ADReCS v3.3 records by any entity. Auto-detects type by prefix:

| Input Pattern | Detected As | Example |
|---|---|---|
| `BADD_D00142` | BADD Drug ID | exact on drug_id column |
| `DB00945` | DrugBank ID | resolved via Drug_information |
| `A02BC01` | ATC code | resolved via Drug_information |
| `50-78-2` | CAS RN | resolved via Drug_information |
| `CID2244` or bare digits | PubChem CID | resolved via Drug_information |
| `D00109` (5-digit) | KEGG ID | resolved via Drug_information |
| `08.06.02.001` | ADReCS ID | substring on ADReCS_ID column |
| `10003781` (8-digit) | MedDRA code | resolved via ADR_ontology |
| `D######` (6+ digit) | MeSH ID | resolved via ADR_ontology |
| anything else | free text | substring on drug_name OR ADR_term |

## API

| Function | Input | Returns |
|---|---|---|
| `load_drug_adr(path)` | txt path | DataFrame (Drug–ADR pairs) |
| `load_drug_info(path)` | xlsx path | DataFrame (drug metadata) |
| `load_adr_ontology(path)` | xlsx path | DataFrame (ADR hierarchy) |
| `search(entity)` | single entity string | DataFrame of matching Drug–ADR rows |
| `search_batch(entities)` | list of entity strings | dict[str, DataFrame] |
| `summarize(hits, entity)` | DataFrame + label | compact LLM-readable text |
| `to_json(hits)` | DataFrame | list[dict] |

## Usage

See `if __name__ == "__main__"` block in `62_ADReCS.py` for runnable examples covering: drug name lookup, BADD Drug ID, DrugBank ID, ADR term, ADReCS ID prefix, batch search, and JSON output.

## Data

- **Source**: ADReCS v3.3 — [https://www.bio-add.org/ADReCS/](https://www.bio-add.org/ADReCS/)
- **Primary file**: `Drug_ADR_v3.3.txt` (drug–ADR association pairs)
- **Drug metadata**: `Drug_information_v3.3.xlsx` (name, synonyms, DrugBank/KEGG/PubChem/ATC/CAS cross-refs)
- **ADR hierarchy**: `ADR_ontology_v3.3.xlsx` (ADReCS ID, ADR term, MedDRA code, MeSH ID, 4-level classification)
- **Path**: `DATA_DIR` variable in `62_ADReCS.py`

## Citation

Cai MC et al. (2015) ADReCS: an ontology database for aiding standardization and hierarchical classification of adverse drug reaction terms. *Nucleic Acids Research* 43(D1):D907–D913.
