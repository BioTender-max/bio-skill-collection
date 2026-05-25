# Dremio SQL Quick Reference

Concise guide for agents querying the JGI Lakehouse.

---

## SQL Dialect

**Dremio uses ANSI SQL** (not PostgreSQL or MySQL). Key points:

- ANSI SQL standard with Dremio extensions
- String literals: single quotes `'value'`
- Identifiers with special chars: double quotes `"schema-name"`
- Case-insensitive keywords, case-sensitive identifiers in quotes

---

## Core Syntax Patterns

### SELECT
```sql
SELECT column1, column2
FROM "source-name".schema.table
WHERE condition
ORDER BY column1 DESC
LIMIT 100;
```

### Table References
```sql
-- PostgreSQL source (quotes required for dashes)
"gold-db-2 postgresql".gold.project

-- MySQL source
"myco-db-1 mysql".Aalte1.allmodels

-- Iceberg tables
"numg-iceberg"."numg-iceberg".gene2pfam

-- Spaces (pre-computed views)
IMG.pfam_hits
```

### Aggregations
```sql
SELECT ecosystem, COUNT(*) as cnt
FROM "gold-db-2 postgresql".gold.project
GROUP BY ecosystem
HAVING COUNT(*) > 10
ORDER BY cnt DESC
LIMIT 20;
```

### Joins
```sql
SELECT p.gold_id, p.project_name, o.organism_name
FROM "gold-db-2 postgresql".gold.project p
JOIN "gold-db-2 postgresql".gold.organism_v2 o
  ON p.organism_id = o.organism_id
WHERE p.is_public = 'Yes'
LIMIT 50;
```

---

## Iceberg Time Travel

Only works on Iceberg tables (e.g., `numg-iceberg`).

### By Timestamp
```sql
SELECT * FROM "numg-iceberg"."numg-iceberg".gene2pfam
AT TIMESTAMP '2025-01-01 00:00:00'
LIMIT 100;
```

### By Snapshot ID
```sql
SELECT * FROM myTable AT SNAPSHOT '5393090506354317772';
```

### Get Available Snapshots
```sql
SELECT * FROM TABLE(table_history('"numg-iceberg"."numg-iceberg".gene2pfam'));
SELECT * FROM TABLE(table_snapshot('"numg-iceberg"."numg-iceberg".gene2pfam'));
```

---

## NUMG Protein Patterns

NUMG tables are for metagenome protein workflows.

### Inspect NUMG tables
```sql
SHOW TABLES IN "numg-iceberg"."numg-iceberg";
DESCRIBE "numg-iceberg"."numg-iceberg".faa;
DESCRIBE "numg-iceberg"."numg-iceberg".gene2pfam;
```

### Filter Pfam hits
```sql
SELECT oid, gene_oid, pfam, evalue
FROM "numg-iceberg"."numg-iceberg".gene2pfam
WHERE pfam IN ('pfam00001', 'pfam00004')
LIMIT 100;
```

### Join domains to sequences
```sql
SELECT p.oid, p.gene_oid, p.pfam, p.evalue, f.faa
FROM "numg-iceberg"."numg-iceberg".gene2pfam p
JOIN "numg-iceberg"."numg-iceberg".faa f
  ON p.oid = f.oid
 AND p.gene_oid = f.gene_oid
WHERE p.pfam = 'pfam00001'
LIMIT 100;
```

Notes:
- Join on both `oid` and `gene_oid`.
- Use exact normalized Pfam IDs (for example `pfam00001`), not case transforms.
- For isolate genome proteins, use IMG filesystem packages instead of NUMG.

---

## Data Types

| Category | Types |
|----------|-------|
| Numeric | `INT`, `BIGINT`, `DECIMAL`, `FLOAT`, `DOUBLE` |
| String | `VARCHAR` |
| Binary | `VARBINARY` |
| Boolean | `BOOLEAN` |
| Date/Time | `DATE`, `TIME`, `TIMESTAMP`, `INTERVAL` |
| Complex | `STRUCT`, `LIST`, `MAP` |

### Complex Type Access
```sql
-- Struct field
address['city']

-- List element (0-indexed)
orders[0]

-- Map value
metadata['key']
```

---

## Key Differences from PostgreSQL

| Feature | PostgreSQL | Dremio |
|---------|------------|--------|
| Arrays | `array[1,2,3]` | `LIST` type |
| JSON | `jsonb` | `STRUCT`, `MAP` |
| String concat | `\|\|` | `CONCAT()` or `\|\|` |
| Regex match | `~`, `~*` | Use `REGEXP_LIKE()` |
| Case insensitive | `ILIKE` | `ILIKE` supported |
| Null handling | `COALESCE` | `COALESCE`, `NVL` |
| Limit + Offset | `LIMIT n OFFSET m` | `LIMIT n OFFSET m` |

### Not Supported in Dremio
- `::` type casting (use `CAST(x AS type)`)
- CTEs with `MATERIALIZED` hint
- `RETURNING` clause
- `UPSERT` / `ON CONFLICT`
- Window frame `GROUPS` mode

---

## Schema Discovery

### List All Sources
```sql
SHOW CATALOGS;
```

### List Schemas in Source
```sql
SHOW SCHEMAS IN "gold-db-2 postgresql";
```

### List Tables in Schema
```sql
SHOW TABLES IN "gold-db-2 postgresql".gold;
```

### Describe Table
```sql
DESCRIBE "gold-db-2 postgresql".gold.project;
```

### Get Row Count Estimate
```sql
SELECT COUNT(*) FROM "gold-db-2 postgresql".gold.project;
```

---

## JGI-Specific Patterns

### Always Filter Public Data
```sql
WHERE is_public = 'Yes'
```

### GOLD ID Prefixes
| Prefix | Entity |
|--------|--------|
| `Gs` | Study |
| `Gp` | Project |
| `Ga` | Analysis Project |
| `Gb` | Biosample |
| `Go` | Organism |

### Common Ecosystem Filters
```sql
WHERE ecosystem = 'Environmental'
WHERE ecosystem_type = 'Aquatic' AND ecosystem_subtype = 'Marine'
WHERE ecosystem = 'Host-associated' AND ecosystem_type = 'Human'
```

### IMG Function/Domain ID Normalization

When querying IMG function/domain tables, use table-native ID formats:

```sql
-- KO terms: includes KO: prefix
WHERE ko_terms = 'KO:K00025'

-- Pfam family accessions are lowercase-style
WHERE pfam_family = 'pfam00001'

-- TIGR and COG/KOG are direct
WHERE ext_accession = 'TIGR01642'
WHERE cog = 'COG1389'
WHERE kog = 'KOG0001'
```

Avoid costly case transforms on large annotation tables (for example
`LOWER(pfam_family)`), prefer exact normalized values.

### Reproducible Isolate Filtering

For benchmark-style isolate queries, include all of:

```sql
WHERE genome_type = 'isolate'
  AND is_public = 'Yes'
  AND obsolete_flag = 'No'
```

`obsolete_flag` can change final counts materially.

---

## Performance Rules

1. **Always use LIMIT** - Never `SELECT *` without `LIMIT`
2. **Select specific columns** - Avoid `*` for wide tables
3. **Filter early** - Push predicates to reduce scan
4. **Use VDS** - Virtual datasets are pre-optimized
5. **Paginate** - Use `LIMIT n OFFSET m` for large results
6. **For very large OR queries**, run branch queries separately and union/dedupe client-side if a single monolithic SQL plan fails.

### Pagination Example
```sql
-- Page 1
SELECT * FROM table LIMIT 100 OFFSET 0;
-- Page 2
SELECT * FROM table LIMIT 100 OFFSET 100;
```

---

## Common Functions

### String
```sql
CONCAT(a, b)           -- Concatenate
LOWER(s), UPPER(s)     -- Case
TRIM(s)                -- Whitespace
SUBSTRING(s, start, len)
REGEXP_LIKE(s, pattern)
```

### Date/Time
```sql
CURRENT_DATE, CURRENT_TIMESTAMP
DATE_ADD(date, interval)
DATE_DIFF(date1, date2, unit)
EXTRACT(YEAR FROM ts)
TO_DATE(s, 'YYYY-MM-DD')
```

### Null Handling
```sql
COALESCE(a, b, c)      -- First non-null
NVL(a, default)        -- If null then default
NULLIF(a, b)           -- Null if equal
```

### Aggregates
```sql
COUNT(*), COUNT(DISTINCT col)
SUM(col), AVG(col)
MIN(col), MAX(col)
ARRAY_AGG(col)
```

---

## Error Handling

Common errors and fixes:

| Error | Cause | Fix |
|-------|-------|-----|
| `Source not found` | Wrong source name | Check `SHOW CATALOGS` |
| `Table not found` | Wrong path | Use full path with quotes |
| `Permission denied` | No access | Check token/permissions |
| `Query timeout` | Too much data | Add `LIMIT`, filter more |

---

## Quick Start Template

```sql
-- 1. Discover what's available
SHOW SCHEMAS IN "gold-db-2 postgresql";
SHOW TABLES IN "gold-db-2 postgresql".gold;

-- 2. Inspect table structure
DESCRIBE "gold-db-2 postgresql".gold.project;

-- 3. Sample data
SELECT gold_id, project_name, ecosystem, seq_status
FROM "gold-db-2 postgresql".gold.project
WHERE is_public = 'Yes'
LIMIT 10;

-- 4. Build your query incrementally
SELECT gold_id, project_name, organism_name
FROM "gold-db-2 postgresql".gold.project p
JOIN "gold-db-2 postgresql".gold.organism_v2 o
  ON p.organism_id = o.organism_id
WHERE p.is_public = 'Yes'
  AND p.ecosystem = 'Environmental'
LIMIT 100;
```
