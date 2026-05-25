---
name: query-interpro
description: Query InterPro for protein domains and families. Use when user asks about protein domains, functional sites, protein families, domain architecture, or motifs. Triggers on "interpro", "protein domain", "domain architecture", "protein family", "functional site", "motif".
---

# InterPro Protein Domain Database

Query the InterPro REST API for protein domains, families, and functional sites.

## When to Use

- User asks about domains in a protein
- User wants to know what family a protein belongs to
- User asks about functional sites or motifs
- User wants domain architecture visualization

## How to Execute

```python
import requests
import json

BASE_URL = "https://www.ebi.ac.uk/interpro/api"

# 1. Get protein annotation (domains/families for a UniProt ID)
def get_protein_domains(uniprot_id):
    url = f"{BASE_URL}/protein/uniprot/{uniprot_id}"
    r = requests.get(url, headers={"Accept": "application/json"})
    r.raise_for_status()
    return r.json()

# 2. Get InterPro entry details
def get_interpro_entry(interpro_id):
    url = f"{BASE_URL}/entry/interpro/{interpro_id}"
    r = requests.get(url, headers={"Accept": "application/json"})
    r.raise_for_status()
    return r.json()

# 3. Search InterPro by text
def search_interpro(query, max_results=10):
    url = f"{BASE_URL}/entry/interpro"
    params = {"search": query, "page_size": max_results}
    r = requests.get(url, params=params, headers={"Accept": "application/json"})
    r.raise_for_status()
    return r.json()

# 4. Get domain matches for a protein
def get_domain_matches(uniprot_id):
    url = f"{BASE_URL}/protein/uniprot/{uniprot_id}/entry/interpro"
    r = requests.get(url, headers={"Accept": "application/json"})
    r.raise_for_status()
    return r.json()

# Example: TP53 domains
domains = get_domain_matches("P04637")
for result in domains.get("results", []):
    meta = result.get("metadata", {})
    name = meta.get("name", "N/A")
    ipr_type = meta.get("type", "N/A")
    accession = meta.get("accession", "N/A")
    proteins = result.get("proteins", [])
    if proteins:
        locations = proteins[0].get("entry_protein_locations", [])
        for loc in locations:
            for frag in loc.get("fragments", []):
                start = frag.get("start", "?")
                end = frag.get("end", "?")
                print(f"{accession} ({ipr_type}): {name} [{start}-{end}]")
```

## Entry Types

- `domain` — Structural/functional domain
- `family` — Protein family
- `homologous_superfamily` — Distant homologs
- `repeat` — Repeated motif
- `site` — Active/binding site

## Follow-up Suggestions

- "Want me to compare domains across species?"
- "Should I map these domains onto the 3D structure?"
- "Want me to find other proteins with the same domain?"
