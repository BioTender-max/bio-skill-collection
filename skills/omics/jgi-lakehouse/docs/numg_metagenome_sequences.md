# NUMG: Metagenome Sequences and Functional Annotations

## Overview

The NUMG (Non-redundant Unified Metagenome Gene catalog) data provides sequence-level access to JGI metagenomes directly in the Lakehouse. Unlike the rest of the Lakehouse (which is metadata-only), NUMG tables store **actual nucleotide and protein sequences** alongside functional annotations, partitioned per metagenome.

**Scale:** ~86,800 metagenomes with full sequence and annotation data.

---

## Quick Reference: Which Source to Use

Three NUMG-related sources exist in the Lakehouse. Use **`numg read only`** for all production queries.

| Source | Tables | Status | Use |
|--------|--------|--------|-----|
| `numg read only` | 9 | Fully accessible | **Primary source — use this** |
| `numg-iceberg` | 2 (faa, gene2pfam) | Accessible, subset | Legacy/alternative access |
| `numg-hive ro` | 3 (fna only works) | Partially broken | Avoid |

---

## Partition Structure

All tables in `numg read only` are partitioned by metagenome `oid` (the IMG taxon OID), stored Hive-style. Every table has:

| Column | Type | Description |
|--------|------|-------------|
| `oid` | VARCHAR | IMG metagenome taxon OID (partition key) |
| `dir0` | VARCHAR | Hive partition path, format `oid=<oid>` (same info as `oid`, redundant) |

**Always filter by `oid`** when querying a specific metagenome — this triggers partition pruning and avoids full-table scans across ~86,800 metagenomes.

---

## Table Schemas: `numg read only`

**Path prefix:** `"numg read only".numg.<table>`

### Sequences

#### `fna` — Contig nucleotide sequences

| Column | Type | Description |
|--------|------|-------------|
| `oid` | VARCHAR | Metagenome taxon OID |
| `dir0` | VARCHAR | Hive partition path |
| `scaffold_oid` | VARCHAR | Contig/scaffold identifier |
| `fna` | VARCHAR | Full nucleotide sequence (DNA) |

#### `faa` — Predicted protein sequences

| Column | Type | Description |
|--------|------|-------------|
| `oid` | VARCHAR | Metagenome taxon OID |
| `dir0` | VARCHAR | Hive partition path |
| `gene_oid` | VARCHAR | Gene/protein identifier |
| `faa` | VARCHAR | Full amino acid sequence |

---

### Contig & Gene Metadata

#### `scaffold_stats` — Per-contig assembly statistics

| Column | Type | Description |
|--------|------|-------------|
| `oid` | VARCHAR | Metagenome taxon OID |
| `dir0` | VARCHAR | Hive partition path |
| `scaffold_oid` | VARCHAR | Contig/scaffold identifier |
| `length` | BIGINT | Contig length (bp) |
| `gc` | DOUBLE | GC content (fraction, 0–1) |
| `n_genes` | BIGINT | Number of predicted genes |

#### `scaffold_genes` — Gene coordinates on contigs

| Column | Type | Description |
|--------|------|-------------|
| `oid` | VARCHAR | Metagenome taxon OID |
| `dir0` | VARCHAR | Hive partition path |
| `scaffold_oid` | VARCHAR | Contig/scaffold identifier |
| `gene_oid` | VARCHAR | Gene identifier |
| `locus_type` | VARCHAR | Feature type (e.g. `CDS`, `rRNA`, `tRNA`) |
| `locus_tag` | VARCHAR | Gene locus tag |
| `product_name` | VARCHAR | Gene product description |
| `start_coord` | BIGINT | Start coordinate on contig |
| `end_coord` | BIGINT | End coordinate on contig |
| `strand` | VARCHAR | Strand (`+` or `-`) |
| `source` | VARCHAR | Annotation source |

#### `gene_copy` — Gene copy number estimates

| Column | Type | Description |
|--------|------|-------------|
| `oid` | VARCHAR | Metagenome taxon OID |
| `dir0` | VARCHAR | Hive partition path |
| `gene_oid` | VARCHAR | Gene identifier |
| `gene_copy` | BIGINT | Estimated copy number |

---

### Functional Annotations

#### `gene_product` — Gene product names

| Column | Type | Description |
|--------|------|-------------|
| `oid` | VARCHAR | Metagenome taxon OID |
| `dir0` | VARCHAR | Hive partition path |
| `gene_oid` | VARCHAR | Gene identifier |
| `gene_display_name` | VARCHAR | Human-readable product name |
| `img_product_source` | VARCHAR | Source of product annotation |

#### `gene2pfam` — Pfam domain annotations

| Column | Type | Description |
|--------|------|-------------|
| `oid` | VARCHAR | Metagenome taxon OID |
| `dir0` | VARCHAR | Hive partition path |
| `gene_oid` | VARCHAR | Gene identifier |
| `pfam` | VARCHAR | Pfam accession (lowercase, e.g. `pfam00001`) |
| `percent_identity` | DOUBLE | Percent identity to HMM |
| `query_start` | BIGINT | Query alignment start |
| `query_end` | BIGINT | Query alignment end |
| `subj_start` | BIGINT | Subject alignment start |
| `subj_end` | BIGINT | Subject alignment end |
| `evalue` | DOUBLE | E-value |
| `bit_score` | DOUBLE | Bit score |
| `align_length` | DOUBLE | Alignment length |

#### `ko_genes` — KEGG KO annotations

| Column | Type | Description |
|--------|------|-------------|
| `oid` | VARCHAR | Metagenome taxon OID |
| `dir0` | VARCHAR | Hive partition path |
| `ko` | VARCHAR | KO identifier (e.g. `KO:K00001`) |
| `genes` | VARCHAR | Tab-separated list of gene OIDs assigned to this KO |

> **Note:** `ko_genes` is denormalized — all gene OIDs for a given KO are stored as a single tab-separated string in the `genes` column, not as individual rows. Use `scaffold_genes` or `gene_product` to get per-gene annotations.

---

### Taxonomy

#### `phyloDist-contigLin` — Per-contig taxonomic lineage

| Column | Type | Description |
|--------|------|-------------|
| `oid` | VARCHAR | Metagenome taxon OID |
| `dir0` | VARCHAR | Hive partition path |
| `scaffold_oid` | VARCHAR | Contig/scaffold identifier |
| `lineage` | VARCHAR | Semicolon-separated taxonomic lineage (e.g. `Bacteria;Pseudomonadota;Gammaproteobacteria;...`) |
| `"rank"` | BIGINT | Taxonomic depth of lineage (number of levels) |
| `percentage` | DOUBLE | Fraction of contig assigned to this lineage |

> **Note:** `rank` is a reserved word in Dremio SQL — always quote it: `"rank"`.

---

## What Is NOT Present

| Annotation type | Available? | Notes |
|----------------|------------|-------|
| Pfam | Yes | `gene2pfam` |
| KEGG KO | Yes | `ko_genes` (denormalized) |
| Gene product names | Yes | `gene_product` |
| COG | No | Not in NUMG tables |
| TIGRFAM | No | Not in NUMG tables |
| InterPro | No | Not in NUMG tables |
| tRNA/rRNA separate tables | No | Use `locus_type` in `scaffold_genes` |

---

## Query Examples

### 1. Get all contigs with stats for a specific metagenome

```sql
SELECT scaffold_oid, length, gc, n_genes
FROM "numg read only".numg.scaffold_stats
WHERE oid = '2001200001'
ORDER BY length DESC;
```

### 2. Get nucleotide sequence of a specific contig

```sql
SELECT scaffold_oid, fna
FROM "numg read only".numg.fna
WHERE oid = '2001200001'
  AND scaffold_oid = '2001201185';
```

### 3. Get all protein sequences for a metagenome

```sql
SELECT gene_oid, faa
FROM "numg read only".numg.faa
WHERE oid = '2001200001';
```

### 4. Get gene coordinates on a specific contig

```sql
SELECT gene_oid, locus_type, product_name, start_coord, end_coord, strand
FROM "numg read only".numg.scaffold_genes
WHERE oid = '2001200001'
  AND scaffold_oid = '2001201185'
ORDER BY start_coord;
```

### 5. Get all Pfam annotations for a metagenome (with e-value filter)

```sql
SELECT gene_oid, pfam, evalue, bit_score
FROM "numg read only".numg.gene2pfam
WHERE oid = '2001200001'
  AND evalue < 1e-5
ORDER BY evalue;
```

### 6. Find genes with a specific Pfam domain across a metagenome

```sql
SELECT g.gene_oid, g.pfam, g.evalue, f.faa
FROM "numg read only".numg.gene2pfam g
JOIN "numg read only".numg.faa f
  ON g.oid = f.oid AND g.gene_oid = f.gene_oid
WHERE g.oid = '2001200001'
  AND g.pfam = 'pfam00001'
ORDER BY g.evalue;
```

### 7. Get per-contig taxonomic assignments

```sql
SELECT scaffold_oid, lineage, "rank", percentage
FROM "numg read only".numg."phyloDist-contigLin"
WHERE oid = '2010170003'
ORDER BY scaffold_oid;
```

### 8. Count metagenomes with NUMG data

```sql
-- Total distinct metagenomes in NUMG
SELECT COUNT(DISTINCT oid) AS n_metagenomes
FROM "numg read only".numg.fna;
```

### 9. Link NUMG metagenome to IMG/GOLD metadata

```sql
-- Get metagenome metadata for a set of NUMG oids
SELECT
  t.taxon_oid,
  t.taxon_display_name,
  t.analysis_project_id,
  ap.ecosystem,
  ap.ecosystem_category,
  ap.ecosystem_type
FROM "img-db-2 postgresql".img_core_v400.taxon t
JOIN "gold-db-2 postgresql".gold.analysis_project ap
  ON t.analysis_project_id = ap.gold_id
WHERE t.taxon_oid IN (2001200001, 2001200003, 2004247004)
  AND t.is_public = 'Yes';
```

---

## Coverage (as of 2026-03)

| Table | Distinct metagenomes (oid) |
|-------|---------------------------|
| `fna` | ~86,793 |
| `faa` | ~86,794 |
| `gene2pfam` | ~86,643 |

---

## Pitfalls

| Wrong | Correct |
|-------|---------|
| Query without `oid` filter | Always filter by `oid` to trigger partition pruning |
| `SELECT rank FROM ...` | `SELECT "rank" FROM ...` — `rank` is a reserved word |
| Explode `ko_genes.genes` with SQL | `genes` is a tab-separated string; parse outside SQL or use `scaffold_genes` for per-gene KO |
| Pfam in uppercase (`PF00001`) | Use lowercase format: `pfam00001` |
| Join `gene2pfam` to `faa` on `gene_oid` only | Join on **both** `oid AND gene_oid` |
| Use `numg-hive ro` for faa/gene2pfam | Those tables fail; use `numg read only` instead |

---

## Related Documentation

- [data-catalog.md](data-catalog.md) - All Lakehouse sources and table overview
- [metagenome_metadata.md](metagenome_metadata.md) - Ecosystem/habitat metadata via GOLD Analysis Projects
- [metagenome_comparability.md](metagenome_comparability.md) - Quality metrics and comparability across metagenomes
- [IMG_data_types.md](IMG_data_types.md) - IMG genome and metagenome type definitions
- [examples/05-query-numg-metagenome-proteins.md](../examples/05-query-numg-metagenome-proteins.md) - NUMG query workflow for protein + Pfam
