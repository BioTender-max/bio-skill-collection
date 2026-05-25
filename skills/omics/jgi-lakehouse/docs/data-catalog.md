# JGI Lakehouse Data Catalog

Complete map of available data sources in the JGI Dremio Lakehouse.

> For definitions of IMG/GOLD terms (analysis project types, quality flags, sequencing status, IDs, taxonomy systems), see [img_and_gold_terms.md](img_and_gold_terms.md).

**Last Updated**: 2025-02-02

**Total Tables**: 651

---

## Quick Reference: Where to Find What

| Data Need | Source | Path |
|-----------|--------|------|
| Sequencing projects, studies, samples | GOLD | `"gold-db-2 postgresql".gold.*` |
| NCBI taxonomy | GOLD | `"gold-db-2 postgresql".gold.ncbi_taxonomy` |
| IMG microbial genomes | IMG-DB-2 | `"img-db-2 postgresql".img_core_v400.*` |
| IMG gene annotations | IMG-DB-2 | `"img-db-2 postgresql".img_core_v400.*` |
| Fungal genomes (Mycocosm) | MYCO-DB-1 | `"myco-db-1 mysql".<organism>.*` |
| Plant genomes (Phytozome) | PLANT-DB-7 | `"plant-db-7 postgresql".*` |
| JGI Portal data | PORTAL-DB-1 | `"portal-db-1".portal.*` |
| Biosynthetic gene clusters | IMG-DB-1 | `"img-db-1 mysql".abc.*` |
| RNAseq experiments | IMG-DB-2 | `"img-db-2 postgresql".img_rnaseq.*` |
| Proteomics data | IMG-DB-2 | `"img-db-2 postgresql".img_proteome.*` |
| SRA experiments | GOLD | `"gold-db-2 postgresql".gold.sra_*` |
| Protein families (Pfam) | IMG Space | `IMG.pfam_hits` |
| **File paths for downloads** | Portal | `"portal-db-1".portal.downloadRequestFiles` |
| **IMG taxon OID mapping** | Portal | `"portal-db-1".portal.imgTaxonOids` |

---

## Table Counts by Source

| Source | Tables | Description |
|--------|--------|-------------|
| `img-db-2.img_core_v400` | 244 | Core IMG data |
| `portal-db-1.portal` | 87 | Portal data, file paths |
| `img-db-2.img_ext` | 84 | Extended annotations |
| `img-db-2.img_gold` | 72 | GOLD integration |
| `portal-db-1.dataSubmission` | 26 | Data submissions |
| `portal-db-1.JGIPortal` | 18 | Projects, resources |
| `img-db-1.abc` | 18 | Biosynthetic clusters |
| `img-db-2.img_proteome` | 15 | Proteomics |
| `portal-db-1.PAAF` | 11 | Authentication |
| `img-db-2.img_rnaseq` | 11 | RNAseq |
| `img-db-2.img_methylome` | 10 | Methylation |
| `img-db-2.img_i_taxon` | 8 | Taxon history |
| `portal-db-1.visualization` | 7 | Visualization |
| `img-db-1.img` | 5 | Core taxon data |
| `IMG Space` | 3 | Pre-computed views |
| `numg-iceberg` | 2 | Metagenome proteins |

---

## Data Sources Overview

### Primary Sources

| Source | Type | Description | Use For |
|--------|------|-------------|---------|
| `gold-db-2 postgresql` | PostgreSQL | GOLD database | Projects, studies, samples, organisms, taxonomy |
| `img-db-2 postgresql` | PostgreSQL | IMG/M database | Microbial genomes, gene annotations, functions |
| `img-db-1 mysql` | MySQL | IMG auxiliary | Biosynthetic clusters, taxon metadata |
| `plant-db-7 postgresql` | PostgreSQL | Phytozome | Plant genomics data |
| `myco-db-1 mysql` | MySQL | Mycocosm | Fungal genome annotations |
| `portal-db-1` | MySQL | JGI Portal | User data, downloads, submissions |

### Auxiliary Sources

| Source | Type | Description |
|--------|------|-------------|
| `numg-iceberg` | Iceberg/S3 | NUMG data (faa, gene2pfam) |
| `Samples` | Iceberg/S3 | Sample metadata |
| `IMG` | Space | Pre-computed views (status can vary by backing object health) |

> Operational note: `IMG.gene_feature` has been observed to fail with
> backing-object errors in some environments. Use
> `"img-db-2 postgresql".img_core_v400.*` tables as the reliable fallback.

---

## GOLD Database (gold-db-2 postgresql)

**Path**: `"gold-db-2 postgresql".gold.<table>`

The Genomes OnLine Database - primary source for JGI project/sample metadata.

### Core Tables (with record counts)

| Table | Records | Description |
|-------|---------|-------------|
| `project` | 705,395 | Sequencing projects |
| `analysis_project` | 620,264 | Analysis tracking |
| `organism_v2` | 598,061 | Organism information |
| `sra_experiment_v2` | 447,795 | SRA experiments |
| `biosample` | 273,139 | Biological samples |
| `study` | 70,440 | Research studies |
| `publication` | 32,985 | Related publications |
| `ncbi_taxonomy` | 3,453,361 | NCBI taxonomy |

### Key Tables by Category

#### Projects & Studies
- `project` - Core sequencing project metadata (gold_id, project_name, ncbi_taxonomy_name, sequencing_method, seq_status, ecosystem)
- `study` - Research studies with ecosystem classification
- `analysis_project` - Analysis project tracking with status
- `project_biosample` - Project-biosample relationships
- `project_publication` - Project-publication links

#### Samples & Organisms
- `biosample` - Sample metadata (habitat, location, lat/lon, collection info)
- `organism_v2` - Organism information (taxonomy, strain, culture collection)
- `organism_habitat` - Organism habitat associations
- `organism_metabolism` - Metabolic characteristics
- `organism_phenotype` - Phenotype data

#### Sequencing & Assembly
- `library` - Sequencing library information
- `assembly` - Genome assembly metadata
- `sequencing_method` - Technologies used
- `sra_experiment_v2`, `sra_run_v2`, `sra_sample_v2` - SRA data

#### External Database Integration
- `ncbi_taxonomy` - Full NCBI taxonomy (3.4M records)
- `ncbi_assembly` - NCBI assembly data
- `genbank` - GenBank integration
- `gtdb` - GTDB taxonomy
- `img_taxon` - IMG/M taxon links

#### Controlled Vocabularies (cv* tables)
~100+ tables for standardized values:
- `cvhabitat`, `cvecosystem_classification_2` - Environment
- `cvmetabolism`, `cvenergy_source` - Metabolism
- `cvseq_status`, `cvseq_quality` - Sequencing
- `cvdisease`, `cvphenotype` - Biology

### Example Queries

```sql
-- Find public metagenome projects
SELECT gold_id, project_name, ecosystem, ecosystem_type, seq_status
FROM "gold-db-2 postgresql".gold.project
WHERE is_public = 'Yes'
  AND ecosystem = 'Environmental'
LIMIT 100;

-- Get study with ecosystem path
SELECT gold_id, study_name, ecosystem, ecosystem_category, ecosystem_type, ecosystem_subtype
FROM "gold-db-2 postgresql".gold.study
WHERE is_public = 'Yes'
LIMIT 50;

-- Find samples with geographic coordinates
SELECT gold_id, biosample_name, habitat, geographic_location, latitude, longitude
FROM "gold-db-2 postgresql".gold.biosample
WHERE latitude IS NOT NULL AND is_public = 'Yes'
LIMIT 100;

-- Join project with organism taxonomy
SELECT p.gold_id, p.project_name, o.organism_name, o.genus, o.species
FROM "gold-db-2 postgresql".gold.project p
JOIN "gold-db-2 postgresql".gold.organism_v2 o ON p.organism_id = o.organism_id
WHERE p.is_public = 'Yes'
LIMIT 50;
```

---

## IMG Database (img-db-2 postgresql)

**Path**: `"img-db-2 postgresql".<schema>.<table>`

Integrated Microbial Genomes database - gene annotations, functions, and genomic features.

**→ For comprehensive IMG table documentation, see [IMG-tables-reference.md](IMG-tables-reference.md)**

### Schemas

| Schema | Description |
|--------|-------------|
| `img_core_v400` | Core IMG data (taxons, genes, annotations) - 100 tables |
| `img_gold` | GOLD integration tables |
| `img_ext` | Extended annotations and external links |
| `img_rnaseq` | RNAseq experiments and datasets |
| `img_proteome` | Proteomics data |
| `img_methylome` | Methylation data |
| `img_i_taxon` | Taxon information |

### Key Tables in img_core_v400

- `taxon` - IMG taxon metadata
- `gene` - Gene information
- `gene_ko_terms` - KEGG Orthology assignments
- `gene_cog_groups` - COG assignments
- `gene_img_interpro_hits` - InterPro domains
- `gene_go_terms` - Gene Ontology terms
- `biocyc_*` - BioCyc pathway data (29 tables)
- `bc_type` - Biosynthetic cluster types
- `enzyme*` - Enzyme/EC definitions and relationships
- `compound*` - Chemical compound data
- `dt_*` - Pre-computed/denormalized data tables

### Example Queries

```sql
-- Get IMG taxons with GOLD links
SELECT taxon_oid, taxon_display_name, gold_id
FROM "img-db-2 postgresql".img_gold.gold_analysis_project
LIMIT 100;

-- RNAseq experiments (NOTE: columns are exp_oid, exp_name, NOT experiment_id/experiment_name)
SELECT exp_oid, exp_name, description
FROM "img-db-2 postgresql".img_rnaseq.rnaseq_experiment
LIMIT 50;
```

---

## IMG Auxiliary Database (img-db-1 mysql)

**Path**: `"img-db-1 mysql".<schema>.<table>`

### Schemas

| Schema | Description |
|--------|-------------|
| `abc` | Biosynthetic gene clusters (AntiSMASH/ABC) |
| `abc_restored` | Backup of abc data |
| `actino_abc` | Actinomycete-specific clusters |
| `img` | Core taxon data |
| `cluster` | Workflow statistics |

### Key Tables in abc

- `bcg_region` - Biosynthetic gene cluster regions
- `bcg_region_genes` - Genes in BGC regions
- `bcg_type` - BGC type classifications
- `bcg_gene_pfams` - Pfam domains in BGC genes
- `npatlas` - Natural Products Atlas links
- `taxon_bcg_type` - Taxon BGC type associations

### Example Queries

```sql
-- Get biosynthetic cluster types
SELECT * FROM "img-db-1 mysql".abc.bcg_type LIMIT 20;

-- Find BGC regions with genes
SELECT r.region_id, r.scaffold_id, COUNT(g.gene_oid) as gene_count
FROM "img-db-1 mysql".abc.bcg_region r
JOIN "img-db-1 mysql".abc.bcg_region_genes g ON r.region_id = g.region_id
GROUP BY r.region_id, r.scaffold_id
LIMIT 50;
```

---

## Mycocosm Database (myco-db-1 mysql)

**Path**: `"myco-db-1 mysql".<organism_code>.<table>`

Fungal genomics portal database. Each fungal genome has its own schema named by organism code (e.g., `Aalte1`, `Abobi1`).

### Structure

**2,711 organism schemas**, each containing:

| Table | Description |
|-------|-------------|
| `allmodels` | Gene models |
| `blastp` | BLASTP results |
| `annotation_state` | Annotation status |
| `chromInfo` | Chromosome information |
| `ec` | EC number assignments |
| `go` | GO term annotations |
| `ipr` | InterPro domains |
| `kog` | KOG classifications |
| `pfam` | Pfam domains |
| `signalp` | Signal peptides |
| `tmhmm` | Transmembrane domains |
| `caiwe*` | CAIWE analysis tables |
| `BlatEST*` | EST mapping data |

### Example Queries

```sql
-- List available fungal genomes (first 20)
SHOW SCHEMAS IN "myco-db-1 mysql" LIMIT 20;

-- Get gene models for a specific organism
SELECT * FROM "myco-db-1 mysql".Aalte1.allmodels LIMIT 100;

-- Get Pfam annotations for an organism
SELECT * FROM "myco-db-1 mysql".Aalte1.pfam LIMIT 100;
```

---

## Phytozome Database (plant-db-7 postgresql)

**Path**: `"plant-db-7 postgresql".<schema>.<table>`

Plant genomics database.

### Schemas

| Schema | Description |
|--------|-------------|
| `denormalized` | Pre-joined proteome data |
| `expression` | Gene expression data |
| `genetic_code` | Genetic code tables |
| `go` | GO annotations |
| `json_export` | JSON-formatted views |
| `phillips` | Atlas expression data |

### Key Tables

- `denormalized.all_partitioned_proteomes` - All proteomes
- `expression.gene` - Gene expression
- `expression.experiment_set` - Experiment metadata
- `phillips.atlas_*` - Single-cell atlas data

### Example Queries

```sql
-- Get expression experiments
SELECT * FROM "plant-db-7 postgresql".expression.experiment_set LIMIT 20;

-- Access gene expression data
SELECT * FROM "plant-db-7 postgresql".expression.gene LIMIT 100;
```

---

## JGI Portal Database (portal-db-1)

**Path**: `"portal-db-1".<schema>.<table>`

JGI Data Portal operational database.

### Schemas

| Schema | Description |
|--------|-------------|
| `portal` | Main portal data |
| `dataSubmission` | Data submission tracking |
| `JGIPortal` | Projects and resources |
| `PAAF` | User authentication/authorization |
| `visualization` | Data visualization configs |

### Key Tables in portal

- `downloadLog` - Download statistics
- `downloadRequests` - User download requests
- `genomeadmin_audit` - Genome administration logs
- `alignmentDbs` - Alignment database registry
- `blastDbs_current` - BLAST database registry
- **`downloadRequestFiles`** - Links taxon OIDs to file paths on JGI filesystem
- **`imgTaxonOids`** - IMG taxon OID mappings

### File Path Tables (Critical for Downloads)

These tables map IMG taxon OIDs to actual file paths on the JGI filesystem.

#### downloadRequestFiles

Links download requests to actual file paths. Key columns:

| Column | Type | Description |
|--------|------|-------------|
| `taxonOid` | BIGINT | IMG taxon OID |
| `filePath` | VARCHAR | Path to file on JGI filesystem |
| `fileType` | VARCHAR | Type of file (faa, fna, gff, etc.) |
| `fileSize` | BIGINT | File size in bytes |

#### imgTaxonOids

Maps IMG taxon OIDs to other identifiers:

| Column | Type | Description |
|--------|------|-------------|
| `taxonOid` | BIGINT | IMG taxon OID |
| `goldId` | VARCHAR | GOLD project ID |
| `ncbiTaxId` | INTEGER | NCBI taxonomy ID |

### JGI Filesystem Paths

Genome data is stored on the JGI filesystem at these locations:

| Path Pattern | Content |
|--------------|---------|
| `/clusterfs/jgi/img_merfs-ro/img_web/img_web_data/download/{taxon_oid}.tar.gz` | Genome packages |
| `/clusterfs/jgi/img_merfs-ro/img_web_data_merfs/{taxon_oid}/` | Per-taxon data directories |

Genome tar.gz packages typically contain:
- `*.fna` - Nucleotide sequences (contigs/scaffolds)
- `*.genes.fna` - Gene nucleotide sequences
- `*.faa` - Protein sequences
- `*.gff` - Gene annotations
- `*.cog.txt` - COG assignments
- `*.pfam.txt` - Pfam annotations
- `*.ko.txt` - KEGG Orthology assignments

### Key Tables in JGIPortal

- `Projects` - JGI projects
- `ProjectContacts` - Project contact information
- `ProjectProposals` - Linked proposals
- `ProjectResources` - Associated resources

### Example Queries

```sql
-- Find file paths for a specific taxon OID
SELECT taxonOid, filePath, fileType
FROM "portal-db-1".portal.downloadRequestFiles
WHERE taxonOid = 2728369577
LIMIT 10;

-- Get IMG taxon OIDs with GOLD IDs
SELECT taxonOid, goldId
FROM "portal-db-1".portal.imgTaxonOids
WHERE goldId IS NOT NULL
LIMIT 100;

-- Join portal with IMG to find downloadable genomes
SELECT
    t.taxon_oid,
    t.taxon_display_name,
    f.filePath,
    f.fileType
FROM "img-db-2 postgresql".img_core_v400.taxon t
JOIN "portal-db-1".portal.downloadRequestFiles f
    ON t.taxon_oid = f.taxonOid
WHERE t.domain = 'Bacteria'
LIMIT 50;
```

---

## IMG Space (Pre-computed Views)

**Path**: `IMG.<dataset>`

Pre-materialized views for common queries.

| Dataset | Description |
|---------|-------------|
| `gene_feature` | Gene feature annotations |
| `pfam_hits` | Pfam domain hits |
| `pfam00136` | Specific Pfam family data |

### Example Queries

```sql
-- Query Pfam hits directly
SELECT * FROM IMG.pfam_hits LIMIT 100;
```

---

## NUMG Iceberg Tables

**Path**: `"numg-iceberg".numg-iceberg.<table>`

Modern columnar storage for large-scale genomics data.

| Table | Description |
|-------|-------------|
| `faa` | Protein sequences (FAA format) |
| `gene2pfam` | Gene to Pfam mappings |

### Table Schemas (practical subset)

`faa`:
- `oid` - metagenome/sample grouping identifier
- `gene_oid` - gene/protein identifier
- `faa` - amino acid sequence

`gene2pfam`:
- `oid`, `gene_oid`
- `pfam`
- `evalue`, `bit_score`, `align_length`
- `query_start`, `query_end`, `subj_start`, `subj_end`

### Features
- Supports time travel queries
- Efficient columnar storage
- Partitioned for performance

### Example Queries

```sql
-- Query gene to Pfam mappings
SELECT * FROM "numg-iceberg"."numg-iceberg".gene2pfam LIMIT 100;

-- Time travel (if snapshots exist)
SELECT * FROM "numg-iceberg"."numg-iceberg".gene2pfam
AT TIMESTAMP '2025-01-01 00:00:00'
LIMIT 100;

-- Join Pfam hits to amino acid sequences
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

---

## Cross-Database Joins

### GOLD + IMG Integration

```sql
-- Link GOLD projects to IMG analysis
SELECT
    g.gold_id,
    g.project_name,
    i.taxon_oid,
    i.analysis_project_id
FROM "gold-db-2 postgresql".gold.project g
JOIN "gold-db-2 postgresql".gold.img_taxon i
    ON g.gold_id = i.analysis_project_id
WHERE g.is_public = 'Yes'
LIMIT 50;
```

### GOLD + SRA Integration

```sql
-- Get SRA experiments for GOLD projects (NOTE: column is library_instrument, NOT platform)
SELECT
    p.gold_id,
    p.project_name,
    s.sra_experiment_id,
    s.library_instrument
FROM "gold-db-2 postgresql".gold.project p
JOIN "gold-db-2 postgresql".gold.sra_experiment_v2 s
    ON p.project_id = s.project_id
LIMIT 50;
```

---

## Performance Tips

1. **Always use LIMIT** - Start with small limits, increase as needed
2. **Select specific columns** - Avoid `SELECT *` for wide tables
3. **Filter early** - Add WHERE clauses to reduce data scanned
4. **Use VDS when available** - Virtual datasets are pre-optimized
5. **Check for indexes** - Join on indexed columns when possible
6. **Paginate large results** - Use OFFSET for large result sets

---

## Common Patterns

### Ecosystem Queries
```sql
-- Find all environmental studies
WHERE ecosystem = 'Environmental'

-- Marine samples
WHERE ecosystem_type = 'Aquatic' AND ecosystem_subtype = 'Marine'
```

### Public Data Filter
```sql
-- Always filter for public data in user-facing queries
WHERE is_public = 'Yes'
```

### GOLD ID Patterns
- `Gs*` - Study
- `Gp*` - Project
- `Ga*` - Analysis Project
- `Gb*` - Biosample
- `Go*` - Organism

---

## Genome Download Workflow

The Lakehouse contains **metadata only** - actual genome sequences are on the JGI filesystem.

### Two-Step Process

1. **Query Lakehouse** for taxon OIDs and metadata
2. **Access JGI Filesystem** for actual sequence files

### Step 1: Find Genomes with IMG Taxon OIDs

```sql
-- Find bacterial isolate genomes with taxon OIDs
SELECT
    t.taxon_oid,
    t.taxon_display_name,
    t.domain,
    t.phylum,
    t.ir_class,
    t.ir_order,
    t.family,
    t.genus,
    t.species,
    t.seq_status,
    t.genome_type
FROM "img-db-2 postgresql".img_core_v400.taxon t
WHERE t.domain = 'Bacteria'
  AND t.genome_type = 'isolate'
  AND t.is_public = 'Yes'
LIMIT 10;
```

### Step 2: Access Files on JGI Filesystem

```bash
# Check if genome package exists
TAXON_OID=2728369577
ls -la /clusterfs/jgi/img_merfs-ro/img_web/img_web_data/download/${TAXON_OID}.tar.gz

# Extract to working directory
tar -xzf /clusterfs/jgi/img_merfs-ro/img_web/img_web_data/download/${TAXON_OID}.tar.gz -C ./genomes/

# Or access per-taxon directory directly
ls /clusterfs/jgi/img_merfs-ro/img_web_data_merfs/${TAXON_OID}/
```

### Automated Download Script

See `scripts/download_img_genomes.py` for a complete workflow that:
1. Queries Lakehouse for genomes matching criteria
2. Checks file availability on JGI filesystem
3. Copies/extracts genome packages to working directory

### Important Notes

- **Lakehouse access requires** `DREMIO_PAT` environment variable
- **Filesystem access requires** JGI cluster account with appropriate permissions
- **numg-iceberg tables** contain metagenome proteins only, not isolate genomes
- **Genome packages** are tar.gz archives with sequences, annotations, and functional assignments

---

## Related Documentation

- [img_and_gold_terms.md](img_and_gold_terms.md) - Full IMG/GOLD glossary: definitions for all terms, project types, quality flags, IDs, and sequencing concepts
- [IMG_data_types.md](IMG_data_types.md) - Guide to analysis project types with query patterns
- [IMG-tables-reference.md](IMG-tables-reference.md) - Complete IMG table catalog (244 tables)
- [explore_IMG_genomes.md](explore_IMG_genomes.md) - Genome metadata query guide (taxonomy, quality, size, GTDB)
