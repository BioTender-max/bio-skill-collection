---
name: query-clinvar
description: Query ClinVar for clinical variant significance. Use when user asks about variant pathogenicity, genetic variants, clinical significance, or disease-causing mutations. Triggers on "clinvar", "pathogenic", "variant significance", "clinical significance", "disease variant", "mutation pathogenicity".
---

# ClinVar Clinical Variant Database

Query NCBI ClinVar for clinical significance of genetic variants.

## When to Use

- User asks if a variant is pathogenic
- User wants to find known pathogenic variants in a gene
- User asks about clinical significance of SNPs
- User wants variant-disease associations

## How to Execute

```python
from Bio import Entrez
import json

Entrez.email = "bioclaw@example.com"

# 1. Search ClinVar
def search_clinvar(query, max_results=10):
    handle = Entrez.esearch(db="clinvar", term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    return record

# 2. Fetch variant details
def fetch_clinvar(id_list):
    ids = ",".join(str(i) for i in id_list)
    handle = Entrez.efetch(db="clinvar", id=ids, rettype="vcv", retmode="xml")
    result = handle.read()
    handle.close()
    return result

# 3. Summary for ClinVar IDs
def clinvar_summary(id_list):
    ids = ",".join(str(i) for i in id_list)
    handle = Entrez.esummary(db="clinvar", id=ids, retmode="json")
    result = json.loads(handle.read())
    handle.close()
    return result

# Example: Find pathogenic BRCA1 variants
search = search_clinvar("BRCA1[gene] AND clinsig_pathogenic[prop]", max_results=5)
print(f"Total pathogenic BRCA1 variants: {search['Count']}")

if search['IdList']:
    summaries = clinvar_summary(search['IdList'])
    for uid in search['IdList']:
        info = summaries['result'].get(str(uid), {})
        title = info.get('title', 'N/A')
        clinical_sig = info.get('clinical_significance', {}).get('description', 'N/A')
        genes = info.get('genes', [{}])
        gene = genes[0].get('symbol', 'N/A') if genes else 'N/A'
        print(f"\nVariant: {title}")
        print(f"Gene: {gene}")
        print(f"Clinical significance: {clinical_sig}")
```

## Common Search Patterns

- Pathogenic variants in gene: `BRCA1[gene] AND clinsig_pathogenic[prop]`
- By rsID: `rs6025[rsid]`
- By disease: `"breast cancer"[dis] AND clinsig_pathogenic[prop]`
- By chromosome region: `17[chr] AND 43000000:44000000[chrpos37]`
- Germline variants: `BRCA1[gene] AND origin_germline[prop]`

## Clinical Significance Categories

- Pathogenic, Likely pathogenic, Uncertain significance, Likely benign, Benign

## Follow-up Suggestions

- "Want me to check the allele frequency in gnomAD?"
- "Should I look up this variant in Ensembl for more context?"
- "Want me to find all pathogenic variants in this gene?"
