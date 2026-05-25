---
name: query-reactome
description: Query Reactome for biological pathways and reactions. Use when user asks about signaling cascades, biological processes, pathway diagrams, or reaction details. Triggers on "reactome", "signaling cascade", "biological pathway", "pathway diagram", "reaction mechanism".
---

# Reactome Pathway Database

Query the Reactome ContentService and AnalysisService APIs.

## When to Use

- User asks about detailed biological pathways
- User wants pathway diagrams
- User asks about specific reactions in a pathway
- User wants to do pathway enrichment with a gene list

## How to Execute

```python
import requests
import json

CONTENT_URL = "https://reactome.org/ContentService"
ANALYSIS_URL = "https://reactome.org/AnalysisService"

# 1. Search pathways by keyword
def search_pathways(keyword, species="Homo sapiens"):
    url = f"{CONTENT_URL}/search/query"
    params = {"query": keyword, "species": species, "types": "Pathway", "cluster": True}
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()

# 2. Get pathway details
def get_pathway(pathway_id):
    url = f"{CONTENT_URL}/data/query/{pathway_id}"
    r = requests.get(url, headers={"Accept": "application/json"})
    r.raise_for_status()
    return r.json()

# 3. Get genes/proteins in a pathway
def get_pathway_participants(pathway_id):
    url = f"{CONTENT_URL}/data/participants/{pathway_id}"
    r = requests.get(url, headers={"Accept": "application/json"})
    r.raise_for_status()
    return r.json()

# 4. Gene list pathway enrichment
def pathway_enrichment(gene_list):
    url = f"{ANALYSIS_URL}/identifiers/projection"
    genes_text = "\n".join(gene_list)
    headers = {"Content-Type": "text/plain"}
    r = requests.post(url, data=genes_text, headers=headers)
    r.raise_for_status()
    return r.json()

# 5. Look up a gene in Reactome
def query_gene(gene_symbol):
    url = f"{CONTENT_URL}/data/query/{gene_symbol}"
    r = requests.get(url, headers={"Accept": "application/json"})
    r.raise_for_status()
    return r.json()

# Example: DNA repair pathways
results = search_pathways("DNA repair")
entries = results.get("results", [])
for entry in entries[:5]:
    for e in entry.get("entries", []):
        print(f"{e.get('stId', 'N/A')}: {e.get('name', 'N/A')}")

# Pathway enrichment
enrichment = pathway_enrichment(["BRCA1", "BRCA2", "TP53", "ATM", "CHEK2"])
for p in enrichment.get("pathways", [])[:5]:
    name = p.get("name", "N/A")
    pval = p.get("entities", {}).get("pValue", "N/A")
    found = p.get("entities", {}).get("found", 0)
    print(f"{name} — p={pval:.2e}, {found} genes found")
```

## Common Pathway IDs

- DNA Repair: `R-HSA-73894`
- Apoptosis: `R-HSA-109581`
- Cell Cycle: `R-HSA-1640170`
- Immune System: `R-HSA-168256`

## Follow-up Suggestions

- "Want me to do pathway enrichment with your gene list?"
- "Should I compare with KEGG pathways?"
- "Want me to find upstream regulators of this pathway?"
