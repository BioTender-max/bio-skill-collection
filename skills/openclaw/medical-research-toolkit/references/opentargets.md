# OpenTargets Platform

Link genes to diseases with evidence. Find therapeutic targets with supporting evidence from literature, genetics, and clinical data.

## Key Tools

### `opentargets_search` — Search targets and diseases

```json
{
  "name": "opentargets_search",
  "arguments": {
    "query": "myasthenia gravis",
    "entity_type": "disease",
    "max_results": 10
  }
}
```

**Arguments:**
- `query` (str): Target gene name, protein name, or disease name
- `entity_type` (str, optional): `target`, `disease`, or omit for both
- `max_results` (int, optional): Results to return

**Returns:** Targets (gene symbols, Uniprot IDs) or diseases (MONDO IDs, names)

### `opentargets_get_associations` — Get target-disease links

```json
{
  "name": "opentargets_get_associations",
  "arguments": {
    "disease_id": "MONDO_0005179",
    "size": 20
  }
}
```

**Arguments:**
- `disease_id` (str): MONDO disease identifier (from search)
- `size` (int, optional, default 10): Results per page
- `from_page` (int, optional): Pagination

**Returns:** Target-disease associations ranked by evidence strength (0-1 score)

### `opentargets_get_evidence` — Get evidence for target-disease link

```json
{
  "name": "opentargets_get_evidence",
  "arguments": {
    "disease_id": "MONDO_0005179",
    "target_id": "ENSG00000047457",
    "size": 20
  }
}
```

**Arguments:**
- `disease_id` (str): MONDO disease ID
- `target_id` (str): Ensembl gene ID
- `size` (int, optional): Evidence records to return

**Returns:** Evidence supporting the link:
- Literature (PubMed citations)
- Genetics (GWAS hits, Mendelian randomization)
- Protein expression (tissue specificity)
- Clinical trial data
- Drug/compound interactions

## Use Cases

### Find Disease Targets

```json
{
  "name": "opentargets_search",
  "arguments": {
    "query": "myasthenia gravis",
    "entity_type": "disease"
  }
}
```

Returns MONDO disease ID. Then get associated targets:

```json
{
  "name": "opentargets_get_associations",
  "arguments": {
    "disease_id": "MONDO_0005179",
    "size": 50
  }
}
```

### Find Top Targets for Disease

Same as above — sorted by association strength (highest confidence first)

### Get Evidence Type Breakdown

For each target:
```json
{
  "name": "opentargets_get_evidence",
  "arguments": {
    "disease_id": "MONDO_0005179",
    "target_id": "ENSG00000047457"
  }
}
```

Returns which data types support this link (genetics? literature? trials?)

### Cross-Check with ChEMBL

1. Find disease targets (OpenTargets)
2. Search for drugs targeting each gene (ChEMBL)
3. Combine results for repurposing candidates

## Data Fields

**Association score:**
- 0-1 scale (higher = more evidence)
- Combines genetics, literature, expression, pathways, clinical data
- Each data type contributes independently

**Evidence types:**
- **Genetics**: GWAS hits, causal variants, Mendelian randomization
- **Literature**: Co-mentioned in PubMed abstracts
- **Expression**: Tissue/cell type expression patterns
- **Pathways**: Protein interactions, pathway membership
- **Clinical**: Trial outcomes, drug response associations

**Target properties:**
- Gene symbol
- Ensembl ID
- UniProt ID
- Protein type (kinase, GPCR, antibody target, etc.)

**Disease properties:**
- MONDO ID (standardized disease ontology)
- Name
- Synonyms
- Ancestor diseases (hierarchy)

## Workflow: Target Prioritization

1. **Find disease targets** (`search` → `get_associations`)
2. **Rank by evidence strength** (association score)
3. **Check evidence types** (`get_evidence`) — which data types?
4. **Filter by genetics** (GWAS hits more reliable)
5. **Check druggability** (is it a kinase? GPCR? enzyme?)
6. **Find drugs** (`chembl_find_drugs_by_target`)
7. **Check trials** (`ctg_search_by_intervention`)

## Notes

- **Disease ontology**: MONDO (Monarch Disease Ontology) — standardized, hierarchical
- **Gene identifiers**: Ensembl gene IDs (standard in research)
- **Evidence integration**: Multiple data types combined into single score
- **Updates**: Quarterly updates with new literature and trials
- **Clinical validity**: Higher scores indicate more rigorous evidence

## Rate Limits

- No API key required
- Public GraphQL endpoint
- Results cached (30-day TTL)

## Examples

### Example 1: Find all targets associated with Myasthenia Gravis

```json
{
  "method": "tools/call",
  "params": {
    "name": "opentargets_search",
    "arguments": {
      "query": "myasthenia gravis",
      "entity_type": "disease"
    }
  }
}
```

Get disease ID from result, then:

```json
{
  "method": "tools/call",
  "params": {
    "name": "opentargets_get_associations",
    "arguments": {
      "disease_id": "MONDO_0005179",
      "size": 50
    }
  }
}
```

### Example 2: Get evidence supporting a target-disease link

```json
{
  "method": "tools/call",
  "params": {
    "name": "opentargets_get_evidence",
    "arguments": {
      "disease_id": "MONDO_0005179",
      "target_id": "ENSG00000047457"
    }
  }
}
```

### Example 3: Find targets with genetic evidence (GWAS)

```json
{
  "method": "tools/call",
  "params": {
    "name": "opentargets_search",
    "arguments": {
      "query": "multiple sclerosis",
      "entity_type": "disease"
    }
  }
}
```

Get disease ID, then get associations and filter for genetics evidence type.
