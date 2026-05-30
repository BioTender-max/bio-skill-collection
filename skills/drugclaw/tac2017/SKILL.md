---
name: tac2017-adr
description: >
  Query TAC 2017 ADR annotated drug labels for adverse drug reactions.
  Use whenever the user asks about ADRs extracted from FDA drug labels,
  MedDRA-normalized adverse reactions, or wants to look up a drug name,
  ADR string, or MedDRA code in the TAC 2017 ADR corpus.
---

# TAC 2017 ADR Query Skill

Search 200 FDA drug labels annotated with adverse reactions, severity,
and MedDRA normalization from the TAC 2017 shared task.

## Entity Auto-detection

| Input Pattern | Detected As | Match Logic |
|---|---|---|
| `10019211` (8 digits) | MedDRA ID | exact on `meddra_pt_id` or `meddra_llt_id` |
| `ACTEMRA` (known drug) | Drug name | exact (case-insensitive) on drug label name |
| `headache` (known ADR) | ADR string | exact on ADR reaction string |
| anything else | Free text | substring on drug names, ADR strings, MedDRA PT/LLT names |

## API

| Function | Input | Returns |
|---|---|---|
| `search(entity)` | single entity string | `list[dict]` — matching label hit(s) |
| `search_batch(entities)` | list of entity strings | `dict[str, list[dict]]` |
| `summarize(hits, entity)` | hit list + query label | compact LLM-readable text |
| `to_json(hits)` | hit list | `list[dict]` (JSON-serializable) |
| `list_drugs()` | — | sorted list of all drug names |
| `stats()` | — | dataset-level statistics dict |

## Hit Dict Structure

Each hit returned by `search()` contains:

| Field | Type | Description |
|---|---|---|
| `drug` | str | Drug label name |
| `source_file` | str | XML filename |
| `sections` | list[str] | Annotated section names (e.g. "adverse reactions") |
| `mention_counts` | dict | Count per mention type (AdverseReaction, Severity, …) |
| `num_reactions` | int | Total unique reactions in this label |
| `positive_adrs` | list[str] | Positive (non-negated, non-hypothetical) ADR strings |
| `reactions` | list[dict] | Each with `adr`, `meddra_pt`, `meddra_pt_id`, optional `meddra_llt`, `meddra_llt_id`, `flag` |

## Usage

See `if __name__ == "__main__"` block in `37_TAC_2017_ADR.py` for runnable
examples covering: drug name lookup, ADR string search, MedDRA ID search,
batch search, and JSON output.

```python
from importlib.machinery import SourceFileLoader
tac = SourceFileLoader("tac2017", "/path/to/37_TAC_2017_ADR.py").load_module()

# Single drug
hits = tac.search("ACTEMRA")
print(tac.summarize(hits, "ACTEMRA"))

# ADR across all labels
hits = tac.search("headache")
print(tac.summarize(hits, "headache"))

# MedDRA PT ID
hits = tac.search("10019211")

# Batch
results = tac.search_batch(["ENBREL", "nausea", "10002198"])
```

## Data

- **Source**: TAC 2017 ADR shared task (NLM / FDA)
- **Files**: `gold_xml/` (99 test labels) + `train_xml/` (101 training labels), each annotated XML
- **Annotations**: Mentions (AdverseReaction, Severity, Factor, DrugClass, Negation, Animal), Relations (Negated, Hypothetical, Effect), Reactions (unique ADRs with MedDRA PT/LLT normalization)
- **MedDRA version**: 18.1
- **Path**: `DATA_DIR` variable in `37_TAC_2017_ADR.py`
- **Reference**: https://bionlp.nlm.nih.gov/tac2017adversereactions/
