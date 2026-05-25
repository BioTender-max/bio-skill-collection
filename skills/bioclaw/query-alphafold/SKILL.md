---
name: query-alphafold
description: Query AlphaFold protein structure predictions. Use when user asks about protein structure, 3D structure, protein folding, or structure prediction. Triggers on "alphafold", "protein structure", "3D structure", "folding", "pLDDT", "structure prediction".
---

# AlphaFold Structure Database Query

Query the AlphaFold EBI API for predicted protein structures.

## When to Use

- User asks about a protein's predicted 3D structure
- User wants to download PDB/CIF structure files
- User asks about structure confidence (pLDDT scores)
- User wants to visualize protein structure

## How to Execute

```python
import requests
import json

BASE_URL = "https://alphafold.ebi.ac.uk/api"

# 1. Get prediction info
def get_alphafold_prediction(uniprot_id):
    url = f"{BASE_URL}/prediction/{uniprot_id}"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

# 2. Download structure file
def download_structure(uniprot_id, output_dir="/workspace/group", fmt="pdb", version="v4"):
    filename = f"AF-{uniprot_id}-F1-model_{version}.{fmt}"
    url = f"https://alphafold.ebi.ac.uk/files/{filename}"
    r = requests.get(url)
    r.raise_for_status()
    filepath = f"{output_dir}/{filename}"
    with open(filepath, 'wb') as f:
        f.write(r.content)
    return filepath

# 3. Get per-residue confidence (pLDDT)
def get_plddt(uniprot_id):
    url = f"{BASE_URL}/prediction/{uniprot_id}"
    r = requests.get(url)
    data = r.json()
    if isinstance(data, list) and data:
        cif_url = data[0].get("cifUrl", "")
        plddt_url = data[0].get("paeImageUrl", "")
        return {"cifUrl": cif_url, "paeImageUrl": plddt_url, "data": data[0]}
    return data

# Example
data = get_alphafold_prediction("P04637")  # TP53
if isinstance(data, list) and data:
    entry = data[0]
    print(f"UniProt: {entry.get('uniprotAccession')}")
    print(f"Gene: {entry.get('gene', 'N/A')}")
    print(f"Organism: {entry.get('organismScientificName', 'N/A')}")
    print(f"Model confidence: {entry.get('globalMetricValue', 'N/A')}")
    print(f"PDB URL: {entry.get('pdbUrl', 'N/A')}")
    print(f"CIF URL: {entry.get('cifUrl', 'N/A')}")
```

## Endpoints

| Endpoint | URL | Use |
|----------|-----|-----|
| Prediction | `/api/prediction/{uniprot_id}` | Get model info & download URLs |
| Summary | `/api/uniprot/summary/{uniprot_id}.json` | Brief summary |
| Annotations | `/api/annotations/{uniprot_id}` | Per-residue annotations |

## Download Formats

- PDB: `AF-{UNIPROT_ID}-F1-model_v4.pdb`
- CIF: `AF-{UNIPROT_ID}-F1-model_v4.cif`
- PAE image: Available from prediction endpoint

## Follow-up Suggestions

- "Want me to analyze the structure confidence by region?"
- "Should I compare this to the experimental PDB structure?"
- "Want me to identify disordered regions?"
