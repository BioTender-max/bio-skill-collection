---
name: query-opentarget
description: Query OpenTargets for drug targets, disease associations, and therapeutic evidence. Use when user asks about drug targets, disease mechanisms, target validation, or drug-disease associations. Triggers on "opentarget", "drug target", "target validation", "disease association", "therapeutic target", "drug for disease".
---

# OpenTargets Platform Query

Query the OpenTargets Platform GraphQL API for drug-target-disease associations.

## When to Use

- User asks about drug targets for a disease
- User wants disease-gene associations
- User asks about drugs targeting a specific gene
- User wants evidence for target validation

## How to Execute

```python
import requests
import json

OPENTARGETS_URL = "https://api.platform.opentargets.org/api/v4/graphql"

def query_opentargets(graphql_query, variables=None):
    payload = {"query": graphql_query, "variables": variables or {}}
    r = requests.post(OPENTARGETS_URL, json=payload, headers={"Content-Type": "application/json"})
    r.raise_for_status()
    return r.json()

# 1. Search for a target (gene)
def search_target(gene_name):
    query = '''
    query searchTarget($name: String!) {
      search(queryString: $name, entityNames: ["target"], page: {index: 0, size: 5}) {
        hits { id name description entity }
      }
    }'''
    return query_opentargets(query, {"name": gene_name})

# 2. Get diseases associated with a target
def target_diseases(ensembl_id, size=10):
    query = '''
    query targetDiseases($ensemblId: String!, $size: Int!) {
      target(ensemblId: $ensemblId) {
        id approvedSymbol approvedName
        associatedDiseases(page: {index: 0, size: $size}) {
          count
          rows { disease { id name } score
            datasourceScores { componentId score } }
        }
      }
    }'''
    return query_opentargets(query, {"ensemblId": ensembl_id, "size": size})

# 3. Get targets for a disease
def disease_targets(disease_id, size=10):
    query = '''
    query diseaseTargets($diseaseId: String!, $size: Int!) {
      disease(efoId: $diseaseId) {
        id name
        associatedTargets(page: {index: 0, size: $size}) {
          count
          rows { target { id approvedSymbol approvedName } score }
        }
      }
    }'''
    return query_opentargets(query, {"diseaseId": disease_id, "size": size})

# 4. Get drugs for a target
def target_drugs(ensembl_id):
    query = '''
    query targetDrugs($ensemblId: String!) {
      target(ensemblId: $ensemblId) {
        id approvedSymbol
        knownDrugs(size: 10) {
          count
          rows { drug { id name } mechanismOfAction phase status
            disease { id name } }
        }
      }
    }'''
    return query_opentargets(query, {"ensemblId": ensembl_id})

# 5. Search diseases
def search_disease(disease_name):
    query = '''
    query searchDisease($name: String!) {
      search(queryString: $name, entityNames: ["disease"], page: {index: 0, size: 5}) {
        hits { id name description entity }
      }
    }'''
    return query_opentargets(query, {"name": disease_name})

# Example: Find top drug targets for Alzheimer's
result = search_disease("Alzheimer")
hits = result.get("data", {}).get("search", {}).get("hits", [])
if hits:
    disease_id = hits[0]["id"]
    targets = disease_targets(disease_id, size=5)
    disease = targets.get("data", {}).get("disease", {})
    print(f"Disease: {disease.get('name')} ({disease.get('id')})")
    for row in disease.get("associatedTargets", {}).get("rows", []):
        t = row["target"]
        print(f"  {t['approvedSymbol']} ({t['approvedName']}) — score: {row['score']:.3f}")
```

## Common Disease IDs (EFO)

- Alzheimer's: `EFO_0000249`
- Breast cancer: `EFO_0000305`
- Type 2 diabetes: `EFO_0001360`
- Parkinson's: `EFO_0002508`

## Follow-up Suggestions

- "Want me to check what drugs are in clinical trials for this target?"
- "Should I look at the evidence breakdown by data source?"
- "Want me to find the top genetic associations?"
