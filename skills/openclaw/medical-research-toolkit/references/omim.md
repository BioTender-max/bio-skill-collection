# OMIM (Online Mendelian Inheritance in Man)

Catalog genetic diseases and gene-phenotype relationships. Find inheritance patterns, clinical features, and genetic associations.

## Key Tools

### `omim_search_entries` — Search OMIM by disease or gene

```json
{
  "name": "omim_search_entries",
  "arguments": {
    "search_term": "myasthenia gravis",
    "api_key": "your-omim-api-key"
  }
}
```

**Arguments:**
- `search_term` (str): Disease name or gene symbol
- `api_key` (str): OMIM API key (REQUIRED — get from https://omim.org/api)

**Returns:** OMIM entries with MIM numbers, titles, descriptions

### `omim_get_entry` — Get OMIM entry details

```json
{
  "name": "omim_get_entry",
  "arguments": {
    "mim_number": "601296",
    "api_key": "your-omim-api-key"
  }
}
```

**Arguments:**
- `mim_number` (str): OMIM MIM number (from search)
- `api_key` (str): OMIM API key (REQUIRED)

**Returns:** Full entry including:
- Description (clinical features, etiology)
- Inheritance pattern
- Molecular genetics
- Related references
- Links to genes and variants

### `omim_search_genes` — Search genes in OMIM

```json
{
  "name": "omim_search_genes",
  "arguments": {
    "gene_symbol": "CHRNE",
    "api_key": "your-omim-api-key"
  }
}
```

**Arguments:**
- `gene_symbol` (str): HGNC gene symbol
- `api_key` (str): OMIM API key (REQUIRED)

**Returns:** OMIM gene entries

### `omim_get_gene` — Get gene entry details

```json
{
  "name": "omim_get_gene",
  "arguments": {
    "mim_number": "100700",
    "api_key": "your-omim-api-key"
  }
}
```

**Returns:** Gene information including:
- Location (chromosome, band)
- Function description
- Associated diseases
- Molecular variants reported
- Literature references

### `omim_search_phenotypes` — Search phenotypes/traits

```json
{
  "name": "omim_search_phenotypes",
  "arguments": {
    "search_term": "muscle weakness autosomal recessive",
    "api_key": "your-omim-api-key"
  }
}
```

**Returns:** Phenotype entries matching criteria

### `omim_get_phenotype` — Get phenotype details

```json
{
  "name": "omim_get_phenotype",
  "arguments": {
    "mim_number": "601296",
    "api_key": "your-omim-api-key"
  }
}
```

**Returns:** Phenotype (disease) details with inheritance, features, genetics

## Use Cases

### Find Genes Causing Disease

```json
{
  "name": "omim_search_entries",
  "arguments": {
    "search_term": "myasthenia gravis",
    "api_key": "your-key"
  }
}
```

Then get details:
```json
{
  "name": "omim_get_entry",
  "arguments": {
    "mim_number": "mim_from_search",
    "api_key": "your-key"
  }
}
```

Look for **Molecular Genetics** section — lists genes causing this disease.

### Check Inheritance Pattern

```json
{
  "name": "omim_search_entries",
  "arguments": {
    "search_term": "your-disease",
    "api_key": "your-key"
  }
}
```

Returns inheritance patterns:
- Autosomal dominant (AD)
- Autosomal recessive (AR)
- X-linked
- Mitochondrial
- Multifactorial

### Find Genetic Variants

For a gene:
```json
{
  "name": "omim_get_gene",
  "arguments": {
    "mim_number": "gene_mim_number",
    "api_key": "your-key"
  }
}
```

Lists variants causing disease in that gene.

### Rare Disease Diagnosis

1. Describe symptoms/phenotype → search OMIM
2. Get candidate disease entries
3. Get gene list from each entry
4. Check if patient mutations match known variants

## Data Fields

**Disease/Phenotype entries:**
- Clinical features (what symptoms?)
- Inheritance pattern
- Molecular basis (genes, mutations)
- Genetic heterogeneity (multiple genes cause same disease)
- Phenotypic series (related but distinct disorders)
- Links to genes
- References and citations

**Gene entries:**
- Function description
- Chromosomal location
- Associated diseases
- Molecular variants known
- Expression patterns
- Protein info

**Inheritance patterns:**
- AD (Autosomal Dominant) — 1 mutated copy causes disease
- AR (Autosomal Recessive) — 2 mutated copies needed
- XL (X-Linked) — mutations on X chromosome
- MT (Mitochondrial) — mutations in mitochondrial DNA

## Workflow: Genetic Disease Analysis

1. **Find disease entry** (`search_entries`)
2. **Get inheritance pattern** (`get_entry`)
3. **Identify genes** (from entry details)
4. **Get gene-specific info** (`get_gene`)
5. **Check variant database** (link to ClinVar, etc.)
6. **Map to phenotype** (`get_phenotype`)

## Important Notes

- **API key required**: All OMIM tools require authentication
- **Medical-curated**: OMIM entries written by medical experts
- **Variant focus**: Best for monogenic (single-gene) disorders
- **Heterogeneity**: Note when multiple genes cause same phenotype
- **Updated regularly**: Monthly updates with new discoveries

## Getting an OMIM API Key

1. Go to https://omim.org/api
2. Create account
3. Request API key
4. Get key via email
5. Use in all OMIM API calls

## Rate Limits

- API key required
- Generous limits with key (1000s of requests/day)
- Results cached (30-day TTL)

## Examples

### Example 1: Find genes causing Myasthenia Gravis

```json
{
  "method": "tools/call",
  "params": {
    "name": "omim_search_entries",
    "arguments": {
      "search_term": "myasthenia gravis",
      "api_key": "your-omim-api-key"
    }
  }
}
```

### Example 2: Get full details for disease entry

```json
{
  "method": "tools/call",
  "params": {
    "name": "omim_get_entry",
    "arguments": {
      "mim_number": "601296",
      "api_key": "your-omim-api-key"
    }
  }
}
```

### Example 3: Get gene details (CHRNE)

```json
{
  "method": "tools/call",
  "params": {
    "name": "omim_search_genes",
    "arguments": {
      "gene_symbol": "CHRNE",
      "api_key": "your-omim-api-key"
    }
  }
}
```

### Example 4: Find inheritance patterns for autosomal recessive neuromuscular disorders

```json
{
  "method": "tools/call",
  "params": {
    "name": "omim_search_phenotypes",
    "arguments": {
      "search_term": "autosomal recessive neuromuscular",
      "api_key": "your-omim-api-key"
    }
  }
}
```
