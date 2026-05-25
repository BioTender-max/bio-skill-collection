---
name: query-pdb
description: Query RCSB PDB for experimental protein structures. Use when user asks about crystal structures, X-ray, cryo-EM, NMR structures, or PDB IDs. Triggers on "pdb", "crystal structure", "cryo-em", "x-ray structure", "protein crystal", "experimental structure".
---

# RCSB PDB Database Query

Query the RCSB Protein Data Bank for experimental 3D structures.

## When to Use

- User asks for experimental structures of a protein
- User provides a PDB ID (e.g., "6LU7")
- User wants to find structures solved by X-ray, cryo-EM, or NMR
- User asks about resolution, ligands, or binding sites

## How to Execute

```python
import requests
import json

# 1. Text search (simple keyword)
def search_pdb(query_text, max_results=5):
    url = "https://search.rcsb.org/rcsbsearch/v2/query"
    query = {
        "query": {
            "type": "terminal",
            "service": "full_text",
            "parameters": {"value": query_text}
        },
        "return_type": "entry",
        "request_options": {"paginate": {"start": 0, "rows": max_results}}
    }
    r = requests.post(url, json=query)
    r.raise_for_status()
    return r.json()

# 2. Advanced search (by gene + organism + method)
def advanced_search_pdb(gene_name, organism="Homo sapiens", method=None, max_results=5):
    nodes = [
        {"type": "terminal", "service": "text",
         "parameters": {"attribute": "rcsb_entity_source_organism.rcsb_gene_name.value",
                        "operator": "exact_match", "value": gene_name}},
        {"type": "terminal", "service": "text",
         "parameters": {"attribute": "rcsb_entity_source_organism.ncbi_scientific_name",
                        "operator": "exact_match", "value": organism}}
    ]
    if method:
        nodes.append({"type": "terminal", "service": "text",
                      "parameters": {"attribute": "exptl.method", "operator": "exact_match", "value": method}})
    query = {
        "query": {"type": "group", "logical_operator": "and", "nodes": nodes},
        "return_type": "entry",
        "request_options": {"paginate": {"start": 0, "rows": max_results},
                           "sort": [{"sort_by": "rcsb_accession_info.deposit_date", "direction": "desc"}]}
    }
    r = requests.post("https://search.rcsb.org/rcsbsearch/v2/query", json=query)
    r.raise_for_status()
    return r.json()

# 3. Get entry details
def get_pdb_entry(pdb_id):
    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

# 4. Download structure
def download_pdb(pdb_id, output_dir="/workspace/group"):
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    r = requests.get(url)
    r.raise_for_status()
    path = f"{output_dir}/{pdb_id}.pdb"
    with open(path, 'w') as f:
        f.write(r.text)
    return path

# Example
results = search_pdb("human insulin")
for hit in results.get("result_set", []):
    pdb_id = hit["identifier"]
    details = get_pdb_entry(pdb_id)
    title = details.get("struct", {}).get("title", "N/A")
    method = details.get("exptl", [{}])[0].get("method", "N/A")
    resolution = details.get("rcsb_entry_info", {}).get("resolution_combined", ["N/A"])[0]
    print(f"{pdb_id}: {title}")
    print(f"  Method: {method}, Resolution: {resolution} Å")
```

## Common Methods

- `X-RAY DIFFRACTION` — crystal structures
- `ELECTRON MICROSCOPY` — cryo-EM
- `SOLUTION NMR` — NMR in solution

## Follow-up Suggestions

- "Want me to download this structure and analyze binding sites?"
- "Should I compare with the AlphaFold prediction?"
- "Want me to find ligands bound in this structure?"
