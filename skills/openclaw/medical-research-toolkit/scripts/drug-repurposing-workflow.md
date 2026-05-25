# Drug Repurposing Workflow — Complete Example

**Goal**: Find non-standard-care drugs for Myasthenia Gravis (MG) using all available APIs.

## Step 1: Identify Disease Targets

### Query OpenTargets for MG-associated targets

```bash
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "opentargets_search",
      "arguments": {
        "query": "myasthenia gravis",
        "entity_type": "disease"
      }
    },
    "id": 1
  }'
```

**Response includes:**
```json
{
  "disease_id": "MONDO_0005179",
  "name": "myasthenia gravis",
  ...
}
```

### Get top targets for MG

```bash
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "opentargets_get_associations",
      "arguments": {
        "disease_id": "MONDO_0005179",
        "size": 30
      }
    },
    "id": 2
  }'
```

**Save the top 5-10 target IDs from this result.**

---

## Step 2: Find Genes/Proteins Causing MG

### Query OMIM for genetic basis

```bash
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "omim_search_entries",
      "arguments": {
        "search_term": "myasthenia gravis",
        "api_key": "YOUR_OMIM_API_KEY"
      }
    },
    "id": 3
  }'
```

**Look for:**
- CHRNE (acetylcholine receptor epsilon)
- RAPSN (receptor-associated protein of the synapse)
- Other neuromuscular junction proteins

### Get detailed gene info

```bash
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "omim_get_entry",
      "arguments": {
        "mim_number": "601296",
        "api_key": "YOUR_OMIM_API_KEY"
      }
    },
    "id": 4
  }'
```

---

## Step 3: Find Existing and Investigational Drugs

### Search ChEMBL for approved drugs for MG

```bash
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "chembl_find_drugs_by_indication",
      "arguments": {
        "indication": "myasthenia gravis",
        "max_results": 20
      }
    },
    "id": 5
  }'
```

**Note:** These are FDA-approved; already known.

### Find unapproved drugs targeting MG genes

For each target gene (CHRNE, RAPSN, etc.):

```bash
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "chembl_find_drugs_by_target",
      "arguments": {
        "target_name": "CHRNE",
        "include_all_mechanisms": true,
        "max_results": 30
      }
    },
    "id": 6
  }'
```

**This returns:**
- Approved drugs (for comparison)
- Phase 1/2/3 investigational drugs (repurposing candidates)
- Compounds in research (preclinical)

### Check mechanism of action for candidates

```bash
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "chembl_get_mechanism",
      "arguments": {
        "molecule_id": "CHEMBL_ID_FROM_PREVIOUS_RESULT"
      }
    },
    "id": 7
  }'
```

---

## Step 4: Check Clinical Trials

### Find active trials for top candidates

```bash
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "ctg_search_studies",
      "arguments": {
        "condition": "myasthenia gravis",
        "intervention": "your-candidate-drug-name",
        "recruitment_status": "RECRUITING",
        "max_results": 10
      }
    },
    "id": 8
  }'
```

### Alternative: Search by intervention type

```bash
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "ctg_search_studies",
      "arguments": {
        "condition": "myasthenia gravis",
        "intervention": "monoclonal antibody",
        "recruitment_status": "RECRUITING",
        "max_results": 20
      }
    },
    "id": 9
  }'
```

### Get trial details

```bash
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "ctg_get_study",
      "arguments": {
        "nct_id": "NCT05123456"
      }
    },
    "id": 10
  }'
```

---

## Step 5: Search Literature

### Find mechanistic papers

```bash
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "pubmed_search_articles",
      "arguments": {
        "diseases": ["myasthenia gravis"],
        "keywords": ["immunotherapy", "autoimmune"],
        "max_results": 30
      }
    },
    "id": 11
  }'
```

### Find papers on specific mechanism

```bash
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "pubmed_search_articles",
      "arguments": {
        "query": "complement inhibition neuromuscular junction",
        "max_results": 20
      }
    },
    "id": 12
  }'
```

### Get full article for top papers

```bash
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "pubmed_get_article",
      "arguments": {
        "pmid": "PMID_FROM_PREVIOUS_RESULT",
        "include_full_text": true
      }
    },
    "id": 13
  }'
```

---

## Step 6: Check Safety Profile

### Search FDA adverse events

```bash
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "openfda_search_adverse_events",
      "arguments": {
        "drug_name": "your-candidate-drug",
        "limit": 50
      }
    },
    "id": 14
  }'
```

**Count:**
- Total adverse events
- Serious events
- Deaths or hospitalizations
- Trends over time

### Get FDA label

```bash
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "openfda_search_drug_labels",
      "arguments": {
        "drug_name": "your-candidate-drug",
        "section": "warnings"
      }
    },
    "id": 15
  }'
```

---

## Step 7: Understand Biological Context

### Get pathway information

```bash
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "reactome_get_disease_pathways",
      "arguments": {
        "disease_name": "myasthenia gravis"
      }
    },
    "id": 16
  }'
```

**Returns:** Immune system pathways relevant to MG (complement cascade, antibody-mediated attack, etc.)

### Get protein details

```bash
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "uniprot_search_proteins",
      "arguments": {
        "query": "acetylcholine receptor neuromuscular",
        "reviewed": true
      }
    },
    "id": 17
  }'
```

---

## Step 8: Summarize Findings

### Repurposing Candidate Report Template

```markdown
# Drug Repurposing Candidate: [Drug Name]

## Basic Info
- **ChEMBL ID**: [ID]
- **Mechanism**: [From ChEMBL]
- **Max Phase**: [Phase 1/2/3/Approved]
- **Indication**: [Original approved use, if any]

## MG Relevance
- **Target Gene/Protein**: [Gene names]
- **Target Mechanism**: [How does it affect MG targets?]
- **Evidence Strength**: [From OpenTargets score]

## Clinical Evidence
- **Active Trials**: [Count and list NCT IDs]
- **Trial Status**: [Recruiting/enrolling]
- **MG-Specific Data**: [Any trials in MG?]

## Safety Profile
- **Total Adverse Events**: [Count]
- **Serious Events**: [Count]
- **FDA Warnings**: [Black box? Contraindications?]
- **Mechanistic Risk**: [Expected side effects based on mechanism]

## Literature Support
- **Relevant Papers**: [Count]
- **Key Papers**: [List top 3 PMIDs]
- **Recent Data**: [Last 2 years?]

## Recommendation
- **Proceed with**: [Yes/No/Maybe]
- **Next Steps**: [Preclinical testing? Patient selection? Comorbidity check?]
- **Confidence Level**: [High/Medium/Low]
```

---

## Tips for Success

1. **Start broad** — Get all MG targets from OpenTargets
2. **Focus on genetics** — OMIM tells you what genes CAUSE MG (most important)
3. **Screen systematically** — Check each candidate against all 6 criteria
4. **Look for synergies** — Does drug address multiple pathways?
5. **Check recent data** — Trials and papers from last 2 years most relevant
6. **Don't miss safety** — One serious adverse event can kill a candidate
7. **Consider mechanism** — Does drug actually address MG etiology?

---

## Shortcuts for Common Scenarios

### Quick: "Find any drug for this disease"
1. OpenTargets (get targets)
2. ChEMBL (get drugs)
3. Trials (find active studies)
4. Done

### Medium: "Is this drug worth investigating?"
1. Find drug in ChEMBL (mechanism)
2. Map to disease targets (OpenTargets)
3. Check trials (ClinicalTrials)
4. Check safety (OpenFDA)
5. Done

### Deep: "Comprehensive repurposing analysis"
1. All 8 steps above
2. Add: Literature review (PubMed)
3. Add: Pathway analysis (Reactome)
4. Add: Genetic variants (GWAS, MyVariant)
5. Add: Protein function (UniProt)
6. Full report

---

## Questions?

See individual database references for:
- [PubMed](./references/pubmed.md)
- [ClinicalTrials.gov](./references/clinical-trials.md)
- [ChEMBL](./references/chembl.md)
- [OpenTargets](./references/opentargets.md)
- [OpenFDA](./references/openfda.md)
- [OMIM](./references/omim.md)
- [Other APIs](./references/other-apis.md)
