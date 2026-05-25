---
name: query-kegg
description: Query KEGG for biological pathways and gene info. Use when user asks about metabolic pathways, signaling pathways, pathway genes, or KEGG IDs. Triggers on "kegg", "pathway", "metabolic pathway", "signaling pathway", "pathway genes".
---

# KEGG Pathway Database Query

Query the KEGG REST API for biological pathways, genes, and compounds.

## When to Use

- User asks about biological pathways (glycolysis, apoptosis, etc.)
- User wants to find which pathways a gene is in
- User asks about KEGG pathway IDs
- User wants pathway gene lists

## How to Execute

```python
import requests

BASE_URL = "https://rest.kegg.jp"

# 1. Find pathways by keyword
def find_pathways(keyword, organism="hsa"):
    url = f"{BASE_URL}/find/pathway/{keyword}"
    r = requests.get(url)
    lines = r.text.strip().split('\n')
    results = []
    for line in lines:
        if line:
            parts = line.split('\t')
            pid = parts[0].replace("map", organism) if organism else parts[0]
            results.append({"id": pid, "name": parts[1] if len(parts) > 1 else ""})
    return results

# 2. Get pathway details
def get_pathway(pathway_id):
    url = f"{BASE_URL}/get/{pathway_id}"
    r = requests.get(url)
    return r.text

# 3. Get genes in a pathway
def get_pathway_genes(pathway_id):
    url = f"{BASE_URL}/link/genes/{pathway_id}"
    r = requests.get(url)
    genes = []
    for line in r.text.strip().split('\n'):
        if line:
            parts = line.split('\t')
            if len(parts) >= 2:
                genes.append(parts[1])
    return genes

# 4. Get gene info
def get_gene(kegg_gene_id):
    url = f"{BASE_URL}/get/{kegg_gene_id}"
    r = requests.get(url)
    return r.text

# 5. Find genes by name
def find_gene(gene_name, organism="hsa"):
    url = f"{BASE_URL}/find/{organism}/{gene_name}"
    r = requests.get(url)
    return r.text

# 6. List all human pathways
def list_pathways(organism="hsa"):
    url = f"{BASE_URL}/list/pathway/{organism}"
    r = requests.get(url)
    return r.text

# Example
pathways = find_pathways("apoptosis")
for p in pathways[:5]:
    print(f"{p['id']}: {p['name']}")
```

## API Pattern

`https://rest.kegg.jp/<operation>/<argument>`

| Operation | Example | Use |
|-----------|---------|-----|
| `list` | `/list/pathway/hsa` | List all human pathways |
| `find` | `/find/pathway/cancer` | Search by keyword |
| `get` | `/get/hsa:672` | Get BRCA1 gene info |
| `link` | `/link/genes/hsa00010` | Get genes in pathway |
| `conv` | `/conv/genes/ncbi-geneid:672` | Convert IDs |

## Organism Codes

- `hsa` = Human, `mmu` = Mouse, `rno` = Rat, `dme` = Fly, `sce` = Yeast, `eco` = E. coli

## Follow-up Suggestions

- "Want me to get the full gene list for this pathway?"
- "Should I visualize which of your genes overlap with this pathway?"
- "Want me to check related pathways?"
