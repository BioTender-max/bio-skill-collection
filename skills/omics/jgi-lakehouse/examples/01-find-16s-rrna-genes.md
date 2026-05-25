# Find 16S rRNA Genes by Taxonomy

Query IMG/M for 16S rRNA gene metadata by taxonomic group.

## Use Case
Find 16S rRNA genes for a bacterial family (e.g., Rhodobacteraceae) to identify organisms or retrieve sequences.

## Key Tables
- `"img-db-2 postgresql".img_core_v400.gene` - Gene metadata
- `"img-db-2 postgresql".img_core_v400.taxon` - Organism taxonomy

## SQL Pattern

```sql
SELECT
    g.gene_oid,
    g.locus_tag,
    g.product_name,
    g.dna_seq_length,
    g.start_coord,
    g.end_coord,
    g.strand,
    t.taxon_oid,
    t.taxon_display_name,
    t.genus,
    t.family
FROM "img-db-2 postgresql".img_core_v400.gene g
JOIN "img-db-2 postgresql".img_core_v400.taxon t ON g.taxon = t.taxon_oid
WHERE g.locus_type = 'rRNA'
  AND g.product_name LIKE '%16S%'
  AND (t.taxon_display_name LIKE '%Rhodobacter%'
       OR t.taxon_display_name LIKE '%Paracoccus%')
ORDER BY t.genus, t.taxon_display_name
LIMIT 100
```

## Pitfalls & Solutions

### 1. Family Field Not Populated
**Problem:** `WHERE family = 'Rhodobacteraceae'` returns few or no results.

**Solution:** Use name pattern matching instead:
```sql
WHERE t.taxon_display_name LIKE '%Rhodobacter%'
   OR t.taxon_display_name LIKE '%Paracoccus%'
```

### 2. Sequences Not in Database
**Problem:** Looking for actual DNA sequences.

**Solution:** Lakehouse contains **metadata only**. To get sequences:
1. Use `gene_oid` with IMG/M web interface: `https://img.jgi.doe.gov/cgi-bin/m/main.cgi?section=GeneDetail&gene_oid={gene_oid}`
2. Download genome and extract by coordinates (`start_coord`, `end_coord`, `strand`)

### 3. Filter for Full-Length 16S
```sql
-- Full-length bacterial 16S is ~1500bp
WHERE g.dna_seq_length BETWEEN 1400 AND 1600
```

## Variations

### By Genus
```sql
WHERE t.genus = 'Pseudomonas'
```

### By Domain
```sql
WHERE t.domain = 'Bacteria'
  AND g.locus_type = 'rRNA'
  AND g.product_name LIKE '%16S%'
```

### Count by Genus
```sql
SELECT t.genus, COUNT(*) as gene_count
FROM "img-db-2 postgresql".img_core_v400.gene g
JOIN "img-db-2 postgresql".img_core_v400.taxon t ON g.taxon = t.taxon_oid
WHERE g.locus_type = 'rRNA'
  AND g.product_name LIKE '%16S%'
  AND t.family LIKE '%Rhodobacter%'
GROUP BY t.genus
ORDER BY gene_count DESC
LIMIT 20
```

## Python Usage (optional)
See `find_16s_rrna_genes.py` for a complete Python script using `rest_client.query()`.
