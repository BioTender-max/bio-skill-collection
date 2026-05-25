# Additional Biomedical Databases

Quick reference for other available databases in the toolkit.

## Reactome — Pathway Analysis

**What it does:** Curated pathways, protein interactions, disease mechanisms.

**Key tools:**
- `reactome_query_pathways` — Find pathways by keyword/gene
- `reactome_get_pathway` — Get pathway details
- `reactome_get_disease_pathways` — Find disease-specific pathways

**Use case:** Understanding biological mechanisms:
```json
{
  "name": "reactome_get_disease_pathways",
  "arguments": {
    "disease_name": "myasthenia gravis"
  }
}
```

Returns: Immune system pathways relevant to MG

**Data:** Manually curated pathway diagrams, peer-reviewed

---

## UniProt — Protein Database

**What it does:** Protein sequences, annotations, disease associations, cross-references.

**Key tools:**
- `uniprot_search_proteins` — Search by name, function, disease
- `uniprot_get_protein` — Get protein details
- `uniprot_get_disease_associations` — Disease links for protein
- `uniprot_map_ids` — Convert between database IDs

**Use case:** Get protein details for a gene:
```json
{
  "name": "uniprot_search_proteins",
  "arguments": {
    "query": "acetylcholine receptor",
    "reviewed": true
  }
}
```

Returns: Curated Swiss-Prot entries (high quality)

**Data:** Functional annotations, disease associations, subcellular location, interaction partners

---

## KEGG — Pathways and Systems

**What it does:** Metabolic pathways, disease pathways, drug-target networks.

**Key tools:**
- `kegg_list_pathways` — Browse available pathways
- `kegg_get_pathway_info` — Get pathway diagram info
- `kegg_find_pathways` — Search by keyword
- `kegg_get_disease` — Disease-specific pathways
- `kegg_get_gene` — Gene annotation

**Use case:** Find metabolic pathways for a drug target:
```json
{
  "name": "kegg_get_pathway_info",
  "arguments": {
    "pathway_id": "hsa04115"
  }
}
```

Returns: Pathway diagram with all genes/proteins/compounds

**Data:** Metabolic, signaling, and disease pathway maps

---

## GWAS Catalog — Genetic Associations

**What it does:** Genome-wide association studies linking variants to traits/diseases.

**Key tools:**
- `gwas_search_associations` — Find variants associated with trait
- `gwas_search_traits` — Find traits/diseases
- `gwas_get_variant` — Details for specific variant (rsID)
- `gwas_search_studies` — Find studies for disease

**Use case:** Find genetic variants associated with disease:
```json
{
  "name": "gwas_search_associations",
  "arguments": {
    "query": "myasthenia gravis",
    "p_upper": 0.00001
  }
}
```

Returns: Significant variants (p < 0.00001) with effect sizes

**Data:** Meta-analysis of 10,000+ studies; population frequency; effect sizes

---

## Pathway Commons — Integrated Pathways

**What it does:** Aggregated pathway data from Reactome, BioPAX, NCI PID, etc.

**Key tools:**
- `pathwaycommons_search` — Search pathways/proteins
- `pathwaycommons_graph` — Get network graph (neighborhood, paths)
- `pathwaycommons_traverse` — Query using graph expressions

**Use case:** Find protein interaction networks:
```json
{
  "name": "pathwaycommons_graph",
  "arguments": {
    "source": "TP53",
    "kind": "neighborhood",
    "limit": 20
  }
}
```

Returns: Proteins interacting with TP53

**Data:** Multi-source pathway integration

---

## MyGene.info — Gene Annotations

**What it does:** Unified gene information across multiple databases.

**Key tools:**
- `mygene_get_gene` — Get gene by symbol/ID
- `mygene_search_genes` — Search by gene name/synonym

**Use case:** Get full gene info (location, aliases, external IDs):
```json
{
  "name": "mygene_get_gene",
  "arguments": {
    "gene_id_or_symbol": "TP53"
  }
}
```

Returns: Gene location, aliases, Uniprot ID, Mouse/Rat orthologs, etc.

**Data:** Cross-references to Ensembl, Uniprot, NCBI, OMIM, etc.

---

## MyDisease.info — Disease Annotations

**What it does:** Unified disease information across multiple sources.

**Key tools:**
- `mydisease_get_disease` — Get disease by MONDO/name
- `mydisease_search_diseases` — Search disease database

**Use case:** Get disease details:
```json
{
  "name": "mydisease_get_disease",
  "arguments": {
    "disease_id": "MONDO_0005179"
  }
}
```

Returns: Disease synonyms, associations, cross-references

**Data:** MONDO terminology, linked databases

---

## MyChem.info — Chemical/Drug Info

**What it does:** Unified chemical and drug information.

**Key tools:**
- `mychem_get_drug` — Get drug by name/ID
- `mychem_search_drugs` — Search chemical database

**Use case:** Find chemical compound details:
```json
{
  "name": "mychem_get_drug",
  "arguments": {
    "drug_id": "aspirin"
  }
}
```

Returns: Chemical structure, synonyms, pharmacology, external IDs

**Data:** SMILES, InChI, PubChem, DrugBank integration

---

## Node Normalization API — ID Mapping

**What it does:** Convert between database identifiers (CURIE normalization).

**Key tools:**
- `nodenorm_get_normalized_nodes` — Map IDs across databases
- `nodenorm_get_curie_prefixes` — List supported databases
- `nodenorm_get_semantic_types` — Supported entity types

**Use case:** Convert gene IDs:
```json
{
  "name": "nodenorm_get_normalized_nodes",
  "arguments": {
    "curie": "HGNC:11998",
    "conflation": null
  }
}
```

Returns: Equivalent IDs in NCBI Gene, Uniprot, Ensembl, etc.

**Data:** Cross-database identifier mappings

---

## MyVariant.info — Variant Annotations

**What it does:** Genetic variant effect predictions and annotations.

**Key tools:**
- `myvariant_get_variant` — Get variant details by ID
- `myvariant_search_variants` — Search variants by gene, rsID, consequence

**Use case:** Get variant effect prediction:
```json
{
  "name": "myvariant_search_variants",
  "arguments": {
    "query": "TP53",
    "filter": "consequence:missense"
  }
}
```

Returns: Variants with SIFT/PolyPhen predictions, clinical significance

**Data:** dbSNP, ClinVar, gnomAD population frequencies, CADD scores

---

## Combination Strategies

### Gene → Protein → Pathways → Drug Targets

1. `mygene_get_gene` — Get gene info
2. `uniprot_get_protein` — Get protein function
3. `reactome_query_pathways` — Find pathways
4. `chembl_find_drugs_by_target` — Find drugs

### Disease → Targets → Drugs → Trials

1. `opentargets_search` — Find disease targets
2. `opentargets_get_associations` — Rank by evidence
3. `chembl_find_drugs_by_target` — Find drugs
4. `ctg_search_by_intervention` — Find trials

### Variant → Gene → Disease → Treatments

1. `myvariant_get_variant` — Get variant effects
2. `mygene_get_gene` — Get gene info
3. `omim_search_genes` — Check disease link
4. `chembl_find_drugs_by_target` — Treatment options

---

## API Key Requirements

| Database | Key Required? | How to Get |
|----------|---------------|-----------|
| Reactome | No | Public |
| UniProt | No | Public |
| KEGG | No | Public |
| GWAS | No | Public |
| Pathway Commons | No | Public |
| MyGene.info | No | Public |
| MyDisease.info | No | Public |
| MyChem.info | No | Public |
| Node Normalization | No | Public |
| MyVariant.info | No | Public |
| **OMIM** | **Yes** | https://omim.org/api |
| **NCI Clinical Trials** | Optional | https://clinicaltrialsapi.cancer.gov |
| **OpenFDA** | Optional | https://open.fda.gov/apis |

---

## Choosing Which Database

| Goal | Use This |
|------|----------|
| Find disease targets | OpenTargets, OMIM |
| Find drugs for disease | ChEMBL, clinical trials |
| Check safety profile | OpenFDA, PubMed |
| Understand mechanism | Reactome, KEGG, Pathway Commons |
| Find genetic variants | GWAS, MyVariant, OMIM |
| Get protein info | UniProt, MyGene.info |
| Review literature | PubMed, preprints |
| Map IDs between databases | Node Normalization |

---

## Performance Tips

1. **Cache results** — 30-day TTL, no need to re-query often
2. **Batch queries** — Combine multiple criteria in single call
3. **Combine databases** — Use one to find IDs for another
4. **Filter early** — Reduce results before detailed queries
5. **Use disease ontology** — MONDO IDs are standardized

---

## Troubleshooting

**No results?**
- Try alternative terms (gene symbol vs protein name)
- Check spelling
- Use disease ontology IDs (MONDO, OMIM numbers)
- Try related keywords

**Too many results?**
- Add filters (phase, recruitment status, etc.)
- Limit result count
- Sort by relevance/evidence score
- Focus on specific domain

**ID format issues?**
- Use Node Normalization API to convert IDs
- Prefix with database (e.g., `HGNC:TP53`)
- Check which ID format each database expects
