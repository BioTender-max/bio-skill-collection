---
name: query-geo
description: Query NCBI GEO for gene expression datasets. Use when user asks about RNA-seq datasets, microarray data, expression data, GEO accessions, or finding public datasets. Triggers on "geo", "gene expression omnibus", "expression dataset", "RNA-seq dataset", "microarray dataset", "GSE", "GDS".
---

# NCBI GEO Database Query

Query Gene Expression Omnibus for public expression datasets.

## When to Use

- User wants to find RNA-seq or microarray datasets
- User asks about gene expression studies for a disease/tissue
- User provides a GEO accession (GSE/GDS) to look up
- User wants to download expression data

## How to Execute

```python
from Bio import Entrez
import json

Entrez.email = "bioclaw@example.com"

# 1. Search GEO datasets
def search_geo(query, max_results=10, db="gds"):
    handle = Entrez.esearch(db=db, term=query, retmax=max_results, sort="relevance")
    record = Entrez.read(handle)
    handle.close()
    return record

# 2. Get dataset summaries
def geo_summary(id_list, db="gds"):
    ids = ",".join(str(i) for i in id_list)
    handle = Entrez.esummary(db=db, id=ids, retmode="json")
    result = json.loads(handle.read())
    handle.close()
    return result

# 3. Search for Series (GSE)
def search_gse(keyword, organism="Homo sapiens", max_results=10):
    query = f'"{keyword}" AND "{organism}"[Organism] AND gse[ETYP]'
    return search_geo(query, max_results)

# Example: Find breast cancer RNA-seq datasets
search = search_gse("breast cancer RNA-seq", max_results=5)
print(f"Found {search['Count']} datasets")

if search['IdList']:
    summaries = geo_summary(search['IdList'])
    for uid in search['IdList']:
        info = summaries['result'].get(str(uid), {})
        title = info.get('title', 'N/A')
        gse = info.get('accession', 'N/A')
        gpl = info.get('gpl', 'N/A')
        n_samples = info.get('n_samples', 'N/A')
        summary = info.get('summary', 'N/A')[:200]
        print(f"\n{gse}: {title}")
        print(f"  Platform: {gpl}, Samples: {n_samples}")
        print(f"  Summary: {summary}...")
        print(f"  URL: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gse}")
```

## Search Syntax

- By keyword: `"CRISPR" AND gse[ETYP]`
- By organism: `"Homo sapiens"[Organism]`
- By platform: `"Illumina"[Platform]`
- By date: `"2024/01:2026/12"[PDAT]`
- Combine: `"breast cancer" AND "RNA-seq" AND "Homo sapiens"[Organism] AND gse[ETYP]`

## Follow-up Suggestions

- "Want me to download the expression matrix for this dataset?"
- "Should I do differential expression analysis?"
- "Want me to check what genes are differentially expressed?"
