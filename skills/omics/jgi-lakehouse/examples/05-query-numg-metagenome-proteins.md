# Query NUMG Metagenome Proteins

Use this pattern when you need protein sequences and Pfam mappings from NUMG.

## Scope

- NUMG is for metagenome protein data.
- For isolate genome protein FASTA files, use IMG filesystem packages (`{taxon_oid}.tar.gz`), not NUMG.

## Tables

- `"numg-iceberg"."numg-iceberg".faa`
  - `oid`, `gene_oid`, `faa`
- `"numg-iceberg"."numg-iceberg".gene2pfam`
  - `oid`, `gene_oid`, `pfam`, `evalue`, coordinate and score columns

## Workflow

### 1) Confirm tables

```sql
SHOW TABLES IN "numg-iceberg"."numg-iceberg";
```

### 2) Inspect schemas

```sql
DESCRIBE "numg-iceberg"."numg-iceberg".faa;
DESCRIBE "numg-iceberg"."numg-iceberg".gene2pfam;
```

### 3) Filter Pfam hits

Use exact lowercase Pfam IDs.

```sql
SELECT oid, gene_oid, pfam, evalue
FROM "numg-iceberg"."numg-iceberg".gene2pfam
WHERE pfam IN ('pfam00001', 'pfam00004', 'pfam00136')
LIMIT 100;
```

### 4) Join to protein sequences

Join on both `oid` and `gene_oid`.

```sql
SELECT
  p.oid,
  p.gene_oid,
  p.pfam,
  p.evalue,
  f.faa
FROM "numg-iceberg"."numg-iceberg".gene2pfam p
JOIN "numg-iceberg"."numg-iceberg".faa f
  ON p.oid = f.oid
 AND p.gene_oid = f.gene_oid
WHERE p.pfam = 'pfam00001'
LIMIT 100;
```

### 5) Basic counts

```sql
SELECT pfam, COUNT(*) AS domain_hits
FROM "numg-iceberg"."numg-iceberg".gene2pfam
GROUP BY pfam
ORDER BY domain_hits DESC
LIMIT 20;
```

## Pitfalls

1. Do not join by `gene_oid` alone.
2. Do not use `LOWER(pfam)` on large scans; filter with exact normalized IDs.
3. Do not use NUMG for isolate package retrieval.
