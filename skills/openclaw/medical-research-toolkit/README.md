# Medical Research Toolkit

Query 14+ biomedical databases for drug repurposing, target discovery, clinical evidence, and literature research.

**Everything you need to build evidence-based research workflows using modern biomedical data.**

## What's Included

- **Complete SKILL.md** — Getting started guide with quick examples
- **6 Database Guides** — PubMed, ClinicalTrials, ChEMBL, OpenTargets, OpenFDA, OMIM
- **2 API References** — 8 additional databases + ID mapping
- **1 Complete Workflow** — Drug repurposing example with all curl commands

## Quick Start

1. **Read** [SKILL.md](./SKILL.md) — 5 minute overview
2. **Pick a use case** — Drug repurposing, target discovery, clinical evidence review, or literature mining
3. **Read the relevant database guide** — E.g., [ChEMBL Guide](./references/chembl.md)
4. **Copy/adapt the example queries** — Use the curl commands provided
5. **Scale up** — Build your full research workflow

## Structure

```
medical-research-toolkit/
├── SKILL.md                          # Main guide (START HERE)
├── references/
│   ├── pubmed.md                     # Literature search
│   ├── clinical-trials.md            # Clinical trial search
│   ├── chembl.md                     # Drug-target data
│   ├── opentargets.md                # Disease-target links
│   ├── openfda.md                    # Drug safety & FDA data
│   ├── omim.md                       # Genetic diseases
│   └── other-apis.md                 # Reactome, UniProt, KEGG, GWAS, etc.
└── scripts/
    └── drug-repurposing-workflow.md  # Step-by-step example
```

## Key Features

✅ **14+ Databases** — ChEMBL, PubMed, ClinicalTrials, OpenTargets, OpenFDA, OMIM, Reactome, UniProt, KEGG, GWAS, and more

✅ **No Setup** — Use the production endpoint immediately (https://mcp.cloud.curiloo.com)

✅ **Real Examples** — Every database has actual curl commands you can run

✅ **Complete Workflows** — Full drug repurposing pipeline with all steps

✅ **Clear Documentation** — Written for researchers (medical jargon included but explained)

✅ **Multiple Use Cases** — Drug repurposing, target discovery, clinical evidence, literature mining

## Common Use Cases

### Find Unapproved Drugs for a Disease

1. [OpenTargets Guide](./references/opentargets.md) — Find disease targets
2. [ChEMBL Guide](./references/chembl.md) — Find drugs targeting those genes
3. [ClinicalTrials Guide](./references/clinical-trials.md) — Check for ongoing trials
4. [OpenFDA Guide](./references/openfda.md) — Verify safety profile

### Build Literature Review

1. [PubMed Guide](./references/pubmed.md) — Search relevant papers
2. Filter by gene, disease, chemical, or keyword
3. Get full text for key papers

### Discover Novel Targets

1. [OpenTargets Guide](./references/opentargets.md) — Find disease targets
2. [GWAS Guide](./references/other-apis.md) — Check genetic associations
3. [Reactome Guide](./references/other-apis.md) — Understand biological mechanisms
4. [UniProt Guide](./references/other-apis.md) — Get protein details

### Assess Candidate Drug Safety

1. [OpenFDA Guide](./references/openfda.md) — Search adverse events
2. [PubMed Guide](./references/pubmed.md) — Search case reports/literature
3. [ClinicalTrials Guide](./references/clinical-trials.md) — Check trial data

## API Endpoint

**Production (Recommended):**
```
https://mcp.cloud.curiloo.com/tools/unified/mcp
```

Includes all 14+ databases unified into one endpoint.

**Individual endpoints also available** — See SKILL.md for URLs

## Example Query

```bash
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "pubmed_search_articles",
      "arguments": {
        "query": "myasthenia gravis treatment",
        "max_results": 10
      }
    },
    "id": 1
  }'
```

Returns: Top 10 PubMed articles on MG treatment

## Documentation Organization

- **SKILL.md** — High-level overview, workflows, and quick reference
- **references/*.md** — Deep dives into each database (read as needed)
- **scripts/*.md** — Complete worked examples

Start with SKILL.md. Refer to specific database guides as needed.

## API Keys

Most APIs are **free and don't require keys**. Optional keys for higher rate limits:

| Database | Key Required? | Why? | Get Key |
|----------|---------------|------|---------|
| OMIM | **Yes** | Proprietary medical data | https://omim.org/api |
| OpenFDA | Optional | Higher rate limits | https://open.fda.gov |
| NCI Clinical Trials | Optional | Higher rate limits | https://clinicaltrialsapi.cancer.gov |
| All others | No | Public endpoints | (not needed) |

## Questions?

Refer to the relevant database guide. All tools have examples and explanations of what they return.

---

**Source**: https://github.com/pascalwhoop/medical-mcps

**Author**: Pascal Brockmeyer (@pascalwhoop)

**Organization**: Every Cure (https://www.everycure.org) — Reimagining drug development through computational drug repurposing
