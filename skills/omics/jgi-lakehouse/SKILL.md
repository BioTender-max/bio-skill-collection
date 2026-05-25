---
name: jgi-lakehouse
description: Queries JGI Lakehouse (Dremio) for genomics metadata from GOLD, IMG, Mycocosm, Phytozome. Downloads genome files from JGI filesystem using IMG taxon OIDs and links JGI taxon OIDs to read files through PMO/GOLD identifiers and JAMO. Use when working with JGI data, GOLD projects, IMG annotations, or downloading genomes.
---

# JGI Lakehouse Skill

## Quick Start

**What is it?** JGI's unified data warehouse (651 tables) + filesystem access to genome files.

**Two data access methods:**
1. **Lakehouse (Dremio)** → Metadata, annotations, taxonomy (no sequences)
2. **JGI Filesystem** → Actual genome files (FNA, FAA, GFF) via taxon OID

**SQL Dialect:** ANSI SQL (not PostgreSQL)
- Use `CAST(x AS type)` not `::`
- Use `REGEXP_LIKE()` not `~`
- Identifiers with dashes need double quotes: `"gold-db-2 postgresql"`

```sql
-- Quick test
SELECT gold_id, project_name FROM "gold-db-2 postgresql".gold.project
WHERE is_public = 'Yes' LIMIT 5;
```

---

## When to Use

- Query JGI genomics metadata (GOLD, IMG, Mycocosm, Phytozome)
- Find genomes and/or metagenomes by taxonomy, ecosystem, or phenotype. 
- Download microbial genomes with IMG taxon OIDs
- Cross-reference GOLD projects with IMG annotations


---

## Best practices
 - When reporting results from database queries, always provide a clear summary of the exact criteria that were used for filtering. This should include a list of each field that was used in the query/filter, and the query/filter was applied (string used in exact match, regular expression, exact number searched for or range, etc) 

---

## Data Access: Lakehouse vs Filesystem

| Need | Source | Access Method |
|------|--------|---------------|
| Metadata (taxonomy, projects) | Lakehouse | SQL via REST API |
| Gene annotations (COG, Pfam, KO) | Lakehouse | SQL via REST API |
| **Genome sequences (FNA)** | **JGI Filesystem** | Copy from `/clusterfs/jgi/img_merfs-ro/` |
| **Protein sequences (FAA)** | **JGI Filesystem** | Copy from `/clusterfs/jgi/img_merfs-ro/` |
| Metagenome proteins only | Lakehouse | `numg-iceberg.faa` table |

**Critical insight:** The Lakehouse is a METADATA warehouse. Genome sequences must be accessed from the JGI filesystem.

---

## Key Data Sources

| Source | Path | Contents |
|--------|------|----------|
| GOLD | `"gold-db-2 postgresql".gold.*` | Projects, studies, samples, taxonomy |
| IMG | `"img-db-2 postgresql".img_core_v400.*` | Taxons, genes, annotations (244 tables) |
| Portal | `"portal-db-1".portal.*` | Download tracking, file paths |
| Mycocosm | `"myco-db-1 mysql".<organism>.*` | Fungal genomes (2,711 schemas) |
| Phytozome | `"plant-db-7 postgresql".*` | Plant genomics — see [docs/phytozome.md](docs/phytozome.md) |
| NUMG | `"numg-iceberg"."numg-iceberg".*` | Metagenome proteins, Pfam hits |

**Full table catalog:** See [docs/data-catalog.md](docs/data-catalog.md)

**Phytozome (plant-db-7 / plant-db-4):** Read [docs/phytozome.md](docs/phytozome.md) before writing any queries against these sources.

---

## NUMG (Metagenome Proteins) Agent Workflow

Use NUMG when the task is metagenome protein sequence/domain analysis.

Scope rules:
- `numg-iceberg` is metagenome-focused.
- Do not use NUMG for isolate genome protein retrieval; use IMG filesystem packages.

Core tables:
- `"numg-iceberg"."numg-iceberg".faa`
  - `oid`, `gene_oid`, `faa` (protein sequence)
- `"numg-iceberg"."numg-iceberg".gene2pfam`
  - `oid`, `gene_oid`, `pfam`, `evalue`, alignment coordinate fields

Recommended query flow:

```sql
-- 1) Confirm available NUMG tables
SHOW TABLES IN "numg-iceberg"."numg-iceberg";

-- 2) Inspect schema before writing joins/filters
DESCRIBE "numg-iceberg"."numg-iceberg".faa;
DESCRIBE "numg-iceberg"."numg-iceberg".gene2pfam;

-- 3) Domain filter (use exact lowercase pfam IDs)
SELECT oid, gene_oid, pfam, evalue
FROM "numg-iceberg"."numg-iceberg".gene2pfam
WHERE pfam IN ('pfam00001', 'pfam00004')
LIMIT 100;

-- 4) Join domains to protein sequences
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

Important NUMG rules:
- Join on both `oid` and `gene_oid` (not `gene_oid` alone).
- Keep Pfam filters exact (`pfam00001`, not case-transformed).
- Always start with `LIMIT` and expand only after verifying row shape.

See also: [examples/05-query-numg-metagenome-proteins.md](examples/05-query-numg-metagenome-proteins.md)

---

## Downloading Genomes with IMG Taxon OIDs

### Option 1: JGI Filesystem (Fastest)

```bash
# Genome packages are at:
/clusterfs/jgi/img_merfs-ro/img_web/img_web_data/download/{taxon_oid}.tar.gz

# Example: Copy and extract
cp /clusterfs/jgi/img_merfs-ro/img_web/img_web_data/download/8136918376.tar.gz .
tar -xzf 8136918376.tar.gz
```

**Package contents:**
- `{taxon_oid}.fna` - Genome assembly
- `{taxon_oid}.genes.faa` - Protein sequences
- `{taxon_oid}.genes.fna` - Gene nucleotide sequences
- `{taxon_oid}.gff` - GFF annotations
- `{taxon_oid}.cog.tab.txt` - COG annotations
- `{taxon_oid}.pfam.tab.txt` - Pfam annotations
- `{taxon_oid}.ko.tab.txt` - KEGG KO annotations

---

## Linking Assemblies To Reads

Use this workflow when you need to go from an IMG metagenome assembly to the underlying JGI reads.

### 1. Start from the assembly taxon OID

Assemblies live under:

```bash
/clusterfs/jgi/img_merfs-ro/img_web_data_merfs/{taxon_oid}/assembled/
```

### 2. Pull the JGI/GOLD linkage fields from metadata

For a metagenome taxon OID, the most useful linkage fields are:

- `img_jgi_project_id`
- `sequencing_gold_id`
- `sample_gold_id`
- `study_gold_id`
- `gold_project_id`
- `gold_pmo_project_id`
- `gold_its_spid`

In practice, `img_jgi_project_id` is often the strongest key for JAMO because it behaves like the PMO project identifier used by `jamo info ... pmoid`.

### 3. Prefer JAMO `pmoid` for JGI read lookup

Native JAMO lookup types are listed by:

```bash
apptainer run docker://doejgi/jamo-dori:latest jamo info help
```

For legacy JGI metagenomes, this usually works better than `raw_normal spid`:

```bash
apptainer run docker://doejgi/jamo-dori:latest \
  jamo info all pmoid <img_jgi_project_id>
```

If you only want FASTQ rows, filter the output:

```bash
apptainer run docker://doejgi/jamo-dori:latest \
  jamo info all pmoid <img_jgi_project_id> | rg 'fastq(\\.gz)?'
```

### 4. Direct taxon-OID lookup is still useful

This queries JAMO by the IMG taxon OID embedded in metadata:

```bash
apptainer run docker://doejgi/jamo-dori:latest \
  jamo info all custom '{"metadata.gold_data.img_oid": 3300000030, "file_name": {"$regex": ".*fastq(\\\\.gz)?$"}}'
```

This can recover reads even when the older `spid` route is blank, but in recent re-audits `pmoid` recovered many more JGI rows.

### 5. `spid` is valid, but not sufficient

If you already have a verified sequencing project ID, this is still worth trying:

```bash
apptainer run docker://doejgi/jamo-dori:latest \
  jamo info raw_normal spid <gold_its_spid>
```

But do not stop there. In several JGI cases:

- `raw_normal spid` returned nothing
- `all pmoid <img_jgi_project_id>` returned usable FASTQ records

### 6. Inspect and fetch the actual file

Inspect one metadata record:

```bash
apptainer run docker://doejgi/jamo-dori:latest jamo show <metadata_id>
```

Fetch a file by filename:

```bash
apptainer run docker://doejgi/jamo-dori:latest \
  jamo fetch -s dori all filename <file_name>
```

That prints the staged scratch path, typically under:

```bash
/clusterfs/jgi/scratch/dsi/...
```

Important:

- if the file is already `RESTORED`, you can use the staged path immediately
- if the file is `PURGED`, `jamo fetch` only starts the restore; you must wait until the staged path exists and has non-zero size before using it

Simple wait pattern:

```bash
while [[ ! -s /clusterfs/jgi/scratch/dsi/.../file.fastq.gz ]]; do sleep 10; done
```

### Practical rule

For JGI metagenome read recovery, use this priority:

1. `jamo info all pmoid <img_jgi_project_id>`
2. `jamo info all custom '{"metadata.gold_data.img_oid": ...}'`
3. `jamo info raw_normal spid <gold_its_spid>`

Do not assume "no reads" until all three have been checked.
Do not assume a fetched file is ready until the staged path is actually restored.

---

## Portal Downloads (Mycocosm / Phytozome)

The portal tracks downloadable files for Mycocosm and Phytozome in
`"portal-db-1".portal.downloadRequestFiles`. Use `filePath` to copy data
from the JGI filesystem (`/global/dna/dm_archive/...`).

**Mycocosm (fungal genomes/proteins):**
```sql
SELECT filePath, fileType
FROM "portal-db-1".portal.downloadRequestFiles
WHERE LOWER(filePath) LIKE '%mycocosm%'
  AND (filePath LIKE '%.fasta%' OR filePath LIKE '%.fa%' OR filePath LIKE '%.faa%')
LIMIT 20;
```

**Phytozome (plant genomes/proteins):**
```sql
SELECT filePath, fileType
FROM "portal-db-1".portal.downloadRequestFiles
WHERE LOWER(filePath) LIKE '%phytozome%'
  AND (filePath LIKE '%.fa%' OR filePath LIKE '%.fna%' OR filePath LIKE '%.faa%')
LIMIT 20;
```

**Download from filesystem:**
```bash
cp /global/dna/dm_archive/<path/from-filePath> .
```

Notes:
- `fileType` typically includes `Assembly`, `Annotation`, or `Sequence`.
- `virtualPath` can provide a user-facing download label but `filePath` is the real location.

---

## Query Best Practices

⚠️ **CRITICAL:** When building queries, distinguish between **exploration** and **comprehensive analysis**:

### Exploration Queries
Use `LIMIT` for quick validation during development:
```sql
-- For testing query structure and results
SELECT gold_id, project_name
FROM "gold-db-2 postgresql".gold.project
WHERE is_public = 'Yes'
LIMIT 10;  -- ✓ OK for testing
```

### Comprehensive Queries
**Remove `LIMIT` and other result-limiting clauses** when answering actual questions:
```sql
-- For getting actual dataset counts/results
SELECT COUNT(DISTINCT taxon_oid)
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE genome_type = 'metagenome'
  AND is_public = 'Yes';
-- ✓ No LIMIT - gets true total
```

**Common pitfalls:**
- ❌ `LIMIT 100` on initial exploration → assumes only 100 results exist
- ❌ `LIMIT 50` on a "find all" query → misses 99% of data
- ❌ Using `FETCH FIRST N ROWS` → same issue as LIMIT

**Best practice:**
1. Use `LIMIT` with COUNT(*) or small `LIMIT` during development
2. Once query logic is correct, **remove LIMIT** to get true results
3. For very large result sets, use aggregation (COUNT, GROUP BY) to summarize instead

---

## Common Queries

### Find Bacterial Isolate Genomes
```sql
-- Get count of all finished bacterial isolates
SELECT COUNT(DISTINCT taxon_oid) as total_isolates
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE domain = 'Bacteria'
  AND genome_type = 'isolate'
  AND is_public = 'Yes'
  AND seq_status = 'Finished';

-- Get sample of isolates (if you need details)
SELECT taxon_oid, taxon_display_name, phylum, genus, species
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE domain = 'Bacteria'
  AND genome_type = 'isolate'
  AND is_public = 'Yes'
  AND seq_status = 'Finished'
LIMIT 100;
```

### Link GOLD Project to IMG Taxon
```sql
SELECT COUNT(DISTINCT t.taxon_oid) as total_linked
FROM "img-db-2 postgresql".img_core_v400.taxon t
WHERE t.sequencing_gold_id IS NOT NULL;
```

### Find Genomes with File Paths (Portal)
```sql
SELECT COUNT(DISTINCT taxonOid) as total_tar_gz
FROM "portal-db-1".portal.downloadRequestFiles
WHERE taxonOid IS NOT NULL
  AND filePath LIKE '%.tar.gz';
```

---

## Critical Pitfalls

| Wrong | Correct |
|-------|---------|
| **Using `LIMIT` in comprehensive queries** | **Remove `LIMIT` when answering actual questions; use COUNT() for aggregation** |
| Join `ncbi_assembly` on `project_id` | `ncbi_assembly` has no `project_id`; use `bioproject` or `biosample` |
| `project.ecosystem` | Join `study` via `master_study_id` |
| `SHOW SCHEMAS IN "source"` | Works, but some syntax errors in older Dremio |
| Get sequences from Lakehouse | Download from JGI filesystem |
| `sra_experiment_v2.platform` | Use `library_instrument` |
| `gene_ko_terms = 'K00025'` | Use `gene_ko_terms = 'KO:K00025'` |
| Join NUMG on `gene_oid` only | Join on both `oid` and `gene_oid` |
| Case-normalizing large function tables | Use exact normalized values (`pfam00001`, `COG1389`, etc.) |
| Isolate benchmark counts vary | Add `obsolete_flag = 'No'` and `is_public = 'Yes'` |
| `IMG.gene_feature` fails expansion | Fallback to `"img-db-2 postgresql".img_core_v400.*` tables |
| `show_schemas()` misses sources | Use higher limit (e.g. `show_schemas(limit=2000)`) |

---

## Authentication

```bash
export DREMIO_PAT=$(cat ~/.secrets/dremio_pat)
```

Token setup: See [docs/authentication.md](docs/authentication.md)

---

## API Access

**REST API Base:** `http://lakehouse-1.jgi.lbl.gov:9047/api/v3`

```python
# Use scripts/rest_client.py
from rest_client import query
results = query("SELECT * FROM ... LIMIT 10")
```

## Arrow Flight (Python)

For higher-performance programmatic access, use Arrow Flight with Python.

```bash
python3 -m venv venv
. venv/bin/activate
pip install \
  https://github.com/dremio-hub/arrow-flight-client-examples/releases/download/dremio-flight-python-v1.1.0/dremio_flight-1.1.0-py3-none-any.whl
```

Full guide: [docs/arrow-flight-python.md](docs/arrow-flight-python.md)

---

## Documentation

### IMG Reference
- [docs/img_and_gold_terms.md](docs/img_and_gold_terms.md) - IMG/GOLD glossary: all terms, project types, quality flags, IDs, sequencing status, taxonomy systems
- [docs/IMG_data_types.md](docs/IMG_data_types.md) - Guide to analysis project types (isolates, MAGs, SAGs, metagenomes) with query patterns and data type counts
- [docs/IMG-tables-reference.md](docs/IMG-tables-reference.md) - Complete IMG table catalog (244 tables in img_core_v400)
- [docs/explore_IMG_genomes.md](docs/explore_IMG_genomes.md) - Genome metadata queries: NCBI/GTDB taxonomy, genome size, GC content, quality filters

### Lakehouse Catalog & SQL
- [docs/data-catalog.md](docs/data-catalog.md) - All data sources and key tables (GOLD, IMG, Portal, Mycocosm, Phytozome, NUMG)
- [docs/phytozome.md](docs/phytozome.md) - Phytozome plant genomics: proteomes, genes, families, PFAM/PANTHER/GO, expression, synteny, homologs
- [docs/sql-quick-reference.md](docs/sql-quick-reference.md) - Dremio SQL syntax

### Access & Downloads
- [docs/arrow-flight-python.md](docs/arrow-flight-python.md) - Arrow Flight Python setup and test
- [examples/05-query-numg-metagenome-proteins.md](examples/05-query-numg-metagenome-proteins.md) - NUMG workflow for protein+Pfam queries
- [examples/04-download-img-genomes.md](examples/04-download-img-genomes.md) - Download with taxon OIDs
- [scripts/download_img_genomes.py](scripts/download_img_genomes.py) - Automated download script
