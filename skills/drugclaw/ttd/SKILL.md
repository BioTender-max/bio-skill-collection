---
name: TTD
description: >
  Query the Therapeutic Target Database (TTD) for drug-target-disease interaction data.
  Use this skill when the user asks about therapeutic targets, drugs, diseases, or their
  relationships — including target-drug mappings, clinical status of drugs, disease indications,
  UniProt/gene associations, and pathway annotations. Triggers on queries like "what drugs
  target EGFR", "which diseases is Imatinib used for", "find targets for lung cancer", or
  any lookup involving TTD IDs, gene symbols, drug names, or disease names.
---

# TTD — Therapeutic Target Database

**Source:** https://ttd.idrblab.cn/  
**Paper:** https://academic.oup.com/nar/article/52/D1/D1465/7275004  
**Data dir:** `resources_metadata/dti/TTD`

## Data files (4 required)

| File | Content |
|------|---------|
| `P1-01-TTD_target_download.txt` | Target info: name, UniProt, gene, type, function, disease indication, pathway |
| `P2-01-TTD_target_drug.txt` | Target ↔ Drug links with clinical status (Approved / Phase I–III / Experimental) |
| `P1-06-Target_disease.txt` | Target ↔ Disease associations |
| `P1-07-Drug_disease.txt` | Drug ↔ Disease associations |

**File formats:**
- `P1-01`, `P2-01` — block format: blank-line separated records, each line `<ID>\t<KEY>\t<VALUE>`
- `P1-06`, `P1-07` — TSV with header row

---

## Query API

### `query(entities, entity_type="auto", data_dir=DATA_DIR)`

Returns a **list of dicts**, one per queried entity.

| Parameter | Type | Description |
|-----------|------|-------------|
| `entities` | `str` or `list[str]` | One or more entity names / IDs |
| `entity_type` | `"auto"` / `"target"` / `"drug"` / `"disease"` | Restrict search; `"auto"` tries target → drug → disease |
| `data_dir` | `str` | Path to TTD data directory |

### `query_json(entities, ...)` → `str`

Same as `query()` but returns a JSON string. Use for LLM consumption.

---

## Input formats accepted

| Input | Examples |
|-------|---------|
| Gene / protein name | `"EGFR"`, `"TP53"`, `"BCR-ABL"` |
| Drug name | `"Imatinib"`, `"Gefitinib"`, `"Osimertinib"` |
| Disease name | `"Lung cancer"`, `"Diabetes mellitus"` (partial match supported) |
| TTD Target ID | `"TTDTARGET00001"` |
| TTD Drug ID | `"D0Y4GH"` |

Matching is **case-insensitive**; disease names support **partial matching**.

---

## Output structure

### Target result
```json
{
  "query": "EGFR",
  "entity_type": "target",
  "ttd_id": "TTDTARGET00001",
  "name": "Epidermal growth factor receptor",
  "uniprot": "P00533",
  "gene": "EGFR",
  "target_type": "Successful target",
  "function": "Receptor tyrosine kinase...",
  "disease": "Non-small-cell lung cancer [ICD-11: 2C25]",
  "pathway": "EGFR signaling pathway",
  "drugs": [
    {"drug_id": "D0Y4GH", "drug_name": "Gefitinib", "clinical_status": "Approved"},
    {"drug_id": "D08VGC", "drug_name": "Erlotinib", "clinical_status": "Approved"}
  ]
}
```

### Drug result
```json
{
  "query": "Imatinib",
  "entity_type": "drug",
  "drug_id": "D0IQX1",
  "drug_name": "Imatinib",
  "targets": [
    {"ttd_target_id": "TTDTARGET00002", "target_name": "BCR-ABL",
     "clinical_status": "Approved", "drug_id": "D0IQX1"}
  ],
  "diseases": ["Chronic myelogenous leukemia", "Gastrointestinal stromal tumor"]
}
```

### Disease result
```json
{
  "query": "Lung cancer",
  "entity_type": "disease",
  "disease_name": "non-small-cell lung cancer",
  "targets": [
    {"ttd_target_id": "TTDTARGET00001", "target_name": "EGFR"}
  ],
  "drugs": ["Gefitinib", "Osimertinib", "Erlotinib"]
}
```

### Not found
```json
{"query": "XYZ123", "entity_type": "not_found", "message": "No match found in TTD."}
```

---

## Usage examples

```python
from 17_TTD import query, query_json

# Single entity
results = query("EGFR")

# Multiple entities (mixed types — auto-detected)
results = query(["EGFR", "Imatinib", "Lung cancer"])

# Restrict to drug search only
results = query(["Gefitinib", "Osimertinib"], entity_type="drug")

# JSON string output (for LLM)
print(query_json("TP53"))
```

CLI (demo runs with EGFR / Imatinib / Lung cancer if no args):
```bash
python 17_TTD.py EGFR Imatinib "Lung cancer"
python 17_TTD.py TTDTARGET00001
```

---

## Notes

- **`entity_type="auto"`** stops at the first match type per entity (target → drug → disease). Use explicit type to resolve ambiguity.
- **`drugs` in target results** lists all TTD-linked drugs; filter `clinical_status == "Approved"` for marketed drugs.
- **Disease partial matching** — `"lung cancer"` will match `"non-small-cell lung cancer"`. The first candidate is returned; use `entity_type="disease"` with a more specific name if needed.
- **Multi-value fields** (e.g. multiple pathways for one target) are returned as lists.
