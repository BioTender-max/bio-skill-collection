---
name: query-uniprot
description: Query UniProt protein database. Use when user asks about protein sequences, functions, annotations, domains, or protein identifiers. Triggers on "uniprot", "protein function", "protein sequence", "gene product", "protein info".
---

# UniProt Protein Database Query

Query the UniProt REST API for protein information.

## When to Use

- User asks about a protein's function, sequence, or annotation
- User provides a gene name and wants protein info
- User needs protein accession IDs
- User asks "what does gene X do" (protein level)

## How to Execute

```python
import requests
import json

BASE_URL = "https://rest.uniprot.org"

# 1. Search by gene name (default: human, reviewed/Swiss-Prot)
def search_uniprot(gene_name, organism_id=9606, max_results=5):
    url = f"{BASE_URL}/uniprotkb/search"
    params = {
        "query": f"gene_exact:{gene_name} AND organism_id:{organism_id} AND reviewed:true",
        "format": "json",
        "size": max_results,
        "fields": "accession,id,gene_names,protein_name,organism_name,length,cc_function,ft_domain,sequence"
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()

# 2. Get by accession ID
def get_uniprot_entry(accession):
    url = f"{BASE_URL}/uniprotkb/{accession}.json"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

# 3. Get FASTA sequence
def get_fasta(accession):
    url = f"{BASE_URL}/uniprotkb/{accession}.fasta"
    r = requests.get(url)
    r.raise_for_status()
    return r.text

# Example usage
data = search_uniprot("TP53")
for entry in data.get("results", []):
    acc = entry["primaryAccession"]
    name = entry.get("proteinDescription", {}).get("recommendedName", {}).get("fullName", {}).get("value", "N/A")
    gene = entry.get("genes", [{}])[0].get("geneName", {}).get("value", "N/A")
    length = entry.get("sequence", {}).get("length", "N/A")
    
    # Extract function
    functions = [c["texts"][0]["value"] for c in entry.get("comments", []) if c["commentType"] == "FUNCTION"]
    func_text = functions[0][:200] if functions else "N/A"
    
    print(f"Accession: {acc}")
    print(f"Protein: {name}")
    print(f"Gene: {gene}")
    print(f"Length: {length} aa")
    print(f"Function: {func_text}")
```

## Common Search Patterns

- By gene: `gene_exact:BRCA1 AND organism_id:9606`
- By keyword: `keyword:kinase AND organism_id:9606`
- By disease: `cc_disease:cancer AND organism_id:9606`
- By GO term: `go:apoptosis AND organism_id:9606`
- Species IDs: Human=9606, Mouse=10090, Rat=10116, Zebrafish=7955, Fly=7227, Yeast=559292

## Output Format

Present: Accession, protein name, gene, organism, length, function summary, and UniProt link.

## Follow-up Suggestions

- "Want me to get the AlphaFold structure for this protein?"
- "Should I check protein-protein interactions on STRING?"
- "Want me to BLAST this protein sequence?"
