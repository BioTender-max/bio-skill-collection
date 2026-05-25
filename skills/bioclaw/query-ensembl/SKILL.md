---
name: query-ensembl
description: Query Ensembl for genomic data. Use when user asks about gene coordinates, genomic sequences, variants, gene structure, exons, transcripts, or species comparison. Triggers on "ensembl", "gene coordinates", "genomic location", "exon", "transcript", "variant location", "rsid", "rs number".
---

# Ensembl REST API Query

Query the Ensembl REST API for genomic annotations, sequences, and variants.

## When to Use

- User asks about a gene's genomic location, exons, or transcripts
- User wants to look up an rsID or variant
- User needs genomic/cDNA/protein sequences
- User asks about gene structure or regulatory features
- User wants cross-species gene information

## How to Execute

```python
import requests
import json

BASE_URL = "https://rest.ensembl.org"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

# 1. Gene lookup by symbol
def lookup_gene(symbol, species="homo_sapiens"):
    url = f"{BASE_URL}/lookup/symbol/{species}/{symbol}"
    r = requests.get(url, headers=HEADERS, params={"expand": 1})
    r.raise_for_status()
    return r.json()

# 2. Get sequence
def get_sequence(ensembl_id, seq_type="genomic"):
    url = f"{BASE_URL}/sequence/id/{ensembl_id}"
    r = requests.get(url, headers=HEADERS, params={"type": seq_type})
    r.raise_for_status()
    return r.json()

# 3. Variant lookup by rsID
def lookup_variant(rsid, species="homo_sapiens"):
    url = f"{BASE_URL}/variation/{species}/{rsid}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()

# 4. Get overlapping features in a region
def overlap_region(species, chrom, start, end, feature="gene"):
    url = f"{BASE_URL}/overlap/region/{species}/{chrom}:{start}-{end}"
    r = requests.get(url, headers=HEADERS, params={"feature": feature})
    r.raise_for_status()
    return r.json()

# 5. Cross-species homologs
def get_homologs(ensembl_id, target_species=None):
    url = f"{BASE_URL}/homology/id/{ensembl_id}"
    params = {}
    if target_species:
        params["target_species"] = target_species
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()

# Example: look up BRCA2
gene = lookup_gene("BRCA2")
print(f"Gene: {gene['display_name']}")
print(f"Ensembl ID: {gene['id']}")
print(f"Location: chr{gene['seq_region_name']}:{gene['start']}-{gene['end']}")
print(f"Strand: {'+' if gene['strand'] == 1 else '-'}")
print(f"Biotype: {gene['biotype']}")
print(f"Description: {gene.get('description', 'N/A')}")
```

## Key Endpoints

| Endpoint | Use |
|----------|-----|
| `/lookup/symbol/{species}/{symbol}` | Gene info by symbol |
| `/lookup/id/{id}` | Info by Ensembl ID |
| `/sequence/id/{id}?type=genomic` | Get sequence |
| `/variation/{species}/{rsid}` | Variant info |
| `/overlap/region/{species}/{chr}:{start}-{end}` | Features in region |
| `/homology/id/{id}` | Orthologs/paralogs |
| `/vep/{species}/hgvs/{hgvs}` | Variant effect prediction |

## Notes

- Region queries max 4,900,000 bp
- Species: `homo_sapiens`, `mus_musculus`, `danio_rerio`, `drosophila_melanogaster`
- Always use `application/json` Accept header

## Follow-up Suggestions

- "Want me to get the protein sequence for this gene?"
- "Should I check for known pathogenic variants?"
- "Want me to find orthologs in mouse?"
