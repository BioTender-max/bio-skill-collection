---
name: query-stringdb
description: Query STRING for protein-protein interactions. Use when user asks about protein interactions, interaction networks, binding partners, or interactome. Triggers on "string", "protein interaction", "interaction network", "binding partners", "interactome", "PPI".
---

# STRING Protein Interaction Database

Query the STRING API for protein-protein interaction networks.

## When to Use

- User asks about a protein's interaction partners
- User wants to build an interaction network
- User asks about functional associations between genes
- User wants interaction confidence scores

## How to Execute

```python
import requests
import json

BASE_URL = "https://version-12-0.string-db.org/api"

# 1. Get interaction partners
def get_interactions(genes, species=9606, score_threshold=400):
    url = f"{BASE_URL}/json/network"
    params = {
        "identifiers": "%0d".join(genes),
        "species": species,
        "required_score": score_threshold,
        "caller_identity": "bioclaw"
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()

# 2. Get functional enrichment
def get_enrichment(genes, species=9606):
    url = f"{BASE_URL}/json/enrichment"
    params = {
        "identifiers": "%0d".join(genes),
        "species": species,
        "caller_identity": "bioclaw"
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()

# 3. Get interaction partners (expand network)
def get_partners(gene, species=9606, limit=10):
    url = f"{BASE_URL}/json/interaction_partners"
    params = {
        "identifiers": gene,
        "species": species,
        "limit": limit,
        "caller_identity": "bioclaw"
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()

# 4. Download network image
def download_network_image(genes, species=9606, output_path="/workspace/group/network.png"):
    url = f"{BASE_URL}/highres_image/network"
    params = {
        "identifiers": "%0d".join(genes),
        "species": species,
        "caller_identity": "bioclaw"
    }
    r = requests.get(url, params=params)
    with open(output_path, 'wb') as f:
        f.write(r.content)
    return output_path

# Example
interactions = get_interactions(["BRCA1", "BRCA2", "TP53"])
for i in interactions[:10]:
    print(f"{i['preferredName_A']} <-> {i['preferredName_B']}  score: {i['score']}")
    print(f"  Sources: experimental={i.get('escore',0)}, database={i.get('dscore',0)}, textmining={i.get('tscore',0)}")
```

## Score Thresholds

- 900+ = Highest confidence
- 700+ = High confidence
- 400+ = Medium confidence (default)
- 150+ = Low confidence

## Species IDs

Human=9606, Mouse=10090, Rat=10116, Fly=7227, Yeast=4932, E.coli=511145

## Follow-up Suggestions

- "Want me to do enrichment analysis on this network?"
- "Should I expand the network to include more partners?"
- "Want me to download the network image?"
