# PharmKG

> **Subcategory**: `drug_knowledgebase` &nbsp;|&nbsp; **Access mode**: `Local File`

**Purpose**: Pharmaceutical knowledge graph  

**Coverage**: Multi-relational drug KG (drug-gene-disease-pathway)  

## Setup

1. Prepare a real PharmKG triples file such as `train.tsv`.
2. Prefer a locally mirrored file under `resources_metadata/drug_knowledgebase/PharmKG/`.
3. If you use the public GitHub repository, note that the repository archive itself does not contain the triples file expected by this runtime skill.
4. Set `train_tsv` in config (see below).

## Configuration

| Key | Type / Description |
|-----|--------------------|
| `train_tsv` | path to PharmKG train.tsv |

## Usage

```python
from drugclaw.skills.drug_knowledgebase.pharmkg import PharmKGSkill

skill = PharmKGSkill(config={
    "train_tsv": "...",  # path to PharmKG train.tsv
})

if skill.is_available():
    results = skill.retrieve(
        entities={"drug": ["imatinib"]},
        query="mechanism",
        max_results=20,
    )
    for r in results:
        print(r.source_entity, r.relationship, r.target_entity)
```

## Output (`RetrievalResult`)

| Field | Description |
|-------|-------------|
| `source_entity` | Drug name |
| `target_entity` | Target / disease / ADE / partner |
| `relationship` | Relation type |
| `weight` | Confidence / score (0–1 or raw) |
| `evidence_text` | Human-readable summary |
| `sources` | Source IDs (PMID, DOI, etc.) |
| `metadata` | Extra fields specific to this skill |

## Data Source

- Homepage: <https://github.com/MindRank-Biotech/PharmKG>
- Verified runtime note: the public GitHub repo is reachable, but its archive does not directly provide the `train.tsv` file expected by this skill. A local mirrored data file is currently the reliable path.
