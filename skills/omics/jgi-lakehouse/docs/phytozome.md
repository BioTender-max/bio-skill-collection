# Phytozome

Phytozome is the JGI's plant genomics resource. This guide explains how to find plant gene, protein, family, expression, synteny, and homolog information through the lakehouse — even if you've never used Phytozome before.

## What's here, in one paragraph

Phytozome covers hundreds of fully-sequenced plant species. For each species (called a **proteome**), there are protein-coding genes, transcripts, proteins, functional annotations (PFAM, PANTHER, InterPro, GO), protein families and pairwise homology, gene expression measurements across tissues/conditions, and pre-computed co-expression. The lakehouse holds the metadata and annotations; the actual DNA/protein sequence text isn't here.

## Sources

| Source | What it is | When to use |
|--------|-----------|-------------|
| `"plant-db-7 postgresql"` | PostgreSQL CHADO mirror | Everything except gene documents and homologs (catalog, families, GO, expression, synteny, publications) |
| `"plant-db-4"` | MongoDB | Per-gene documents and pairwise homolog lookups |

## Two firm rules

1. **For `"plant-db-7 postgresql"`, every query must be wrapped in `external_query`.** Do not use Dremio's source-qualified path form (`"plant-db-7 postgresql"."public"."feature"`) for queries — wrap them in `TABLE("plant-db-7 postgresql".external_query('...'))` so PostgreSQL plans them natively.
2. **For `"plant-db-7 postgresql"`, use only the schemas `public`, `denormalized`, and `json_export`.** No other schema may be referenced. This applies inside `external_query` bodies as well: do not `FROM <other>.table`, do not join across to another schema, do not list other schemas. The acceptable set is fixed.

---

## How users typically describe what they want, and where to start

| Natural-language request | Section below |
|--------------------------|--------------|
| "What plant species are in Phytozome?" / "Show me the list of proteomes" | [Discover available proteomes](#discover-available-proteomes) |
| "Find Arabidopsis gene AT1G01010" / "Look up gene X" / "Info on gene PAC:27370627" | [Find info on a gene](#find-info-on-a-gene) |
| "What's the defline (description) of gene X?" | [Get the defline of a gene](#get-the-defline-of-a-gene) |
| "Show me the exons / CDS / UTR structure of a transcript" | [Gene structure](#gene-structure-exons-cds-utrs-introns) |
| "Where is gene X on the chromosome?" / "What's the genomic position?" | [Chromosomal location](#chromosomal-location-of-a-genetranscript) |
| "What genes are next to gene X?" / "Show me the neighborhood" | [Gene neighborhood](#gene-neighborhood-genes-near-a-target-gene) |
| "Find all genes with PFAM PF00001" / "All proteins with kinase domain PF00069" | [Find genes/proteins by PFAM, PANTHER, or InterPro accession](#find-genesproteins-by-pfam-panther-or-interpro-accession) |
| "Find all proteins attached to GO term GO:0052742" | [Find proteins by GO term](#find-proteins-by-go-term) |
| "What gene family does this gene belong to?" | [Family membership of a gene](#family-membership-of-a-gene) |
| "Show me all members of family/cluster X" | [Members of a family/cluster](#members-of-a-familycluster) |
| "Show me the HMM constituents of a method" | [HMM constituents](#hmm-constituents-precomputed) |
| "Tell me about cluster X" / "How many members does cluster Y have?" | [Cluster-level details](#cluster-level-details) |
| "What atlas groups exist?" / "Which atlas contains this proteome?" | [Atlas (cross-proteome groupings)](#atlas-cross-proteome-groupings) |
| "What metabolic pathways are in proteome X?" / "What pathways does gene Y participate in?" | [Metabolic Pathways](#metabolic-pathways) |
| "Find biosamples for proteome X" / "Sample/tissue metadata" | [Biosamples / experimental material](#biosamples--experimental-material) |
| "Get NCBI / RefSeq / UniProt links for a gene or proteome" | [Cross-references to external databases](#cross-references-to-external-databases) |
| "Find homologs of gene X in Arabidopsis" / "Diamond hits for gene Y" | [Find homologs of a gene](#find-homologs-of-a-gene) |
| "What expression data do we have?" / "List bulk RNA-seq datasets" | [Discover available expression datasets](#discover-available-expression-datasets) |
| "What's the expression of gene X across tissues?" | [Get expression for a gene](#get-expression-for-a-gene) |
| "What genes are co-expressed with gene X?" | [Find co-expressed genes](#find-co-expressed-genes) |
| "Find syntenic regions for gene X" / "Compare synteny between species" | [Synteny](#synteny) |
| "What papers describe genome 444?" | [Publications for a proteome](#publications-for-a-proteome) |

---

## Identifier types you will encounter

Naive users often hand you one identifier; figuring out what kind it is matters. Phytozome uses several at once:

| Identifier example | What it is | Where it's used |
|--------------------|-----------|-----------------|
| `444`, `461`, `231` | **phytozome_genome_id** (proteome ID) — short integer assigned per species/annotation release | URLs like `/info/444`, JOIN key to `pac_proteome_properties.phytozome_genome_id` and `pac_genome_worklist.accession` |
| `Ptrichocarpa`, `Athaliana` | **organism abbreviation** (short Latin-ish code) | `organism.abbreviation`, `pac_synteny_grps.organism1` |
| `poplar`, `Arabidopsis thaliana` | **common_name** or **organism_name** | `pac_proteome_properties.common_name` / `.organism_name` |
| `PAC:27370627` (or just `27370627`) | **PAC ID** — Phytozome's persistent ID for a gene, transcript, or protein. Different PAC IDs for the gene, transcript, and protein records of the same locus | `feature.uniquename` |
| `AT1G01010`, `Bradi1g20596` | **locus / gene name** as displayed in genome browsers | `feature.name` |
| `AT1G01010.1` | **transcript name** (locus + dot + transcript number) | `feature.name` for transcripts |
| `PF00001`, `pfam00001` | **PFAM accession** | `dbxref.accession` where `db.name = 'PFAM'` (db_id = 11) |
| `PTHR12345` | **PANTHER accession** | `dbxref.accession` where `db.name = 'PANTHER'` (db_id = 101) |
| `IPR000123` | **InterPro accession** | `dbxref.accession` where `db.name = 'InterPro'` (db_id = 161) |
| `GO:0052742` | **GO term** | `dbxref.accession` where `db.name = 'GO'` |

When given an ambiguous string, prefer the most specific match first. If it starts with `PAC:` or is a long numeric string, it's a PAC ID; if it looks like `AT1G…` or `Bradi…`, it's a gene name; if it's 3-4 digits, it's probably a phytozome_genome_id.

---

## Querying patterns: PostgreSQL vs MongoDB

### For `"plant-db-7 postgresql"` — wrap everything in `external_query`

`external_query` sends your SQL straight to PostgreSQL. Dremio's own SQL translator over JDBC can be 100-1000x slower for CHADO joins; do not use it for these queries.

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT ... FROM ... WHERE ...
  ')
)
```

Escaping rule: every single quote inside the body must be **doubled**: `'foo'` → `''foo''`.

Inside the body, use plain PostgreSQL names. The default `search_path` is `public`, so `feature` works; reference other schemas with their prefix (`denormalized.pac_synteny_grps`).

### For `"plant-db-4"` (MongoDB) — Dremio SQL directly

`external_query` is **not supported** on MongoDB sources. Each MongoDB collection appears as a Dremio table. There is a ~1-2s per-query floor — fine for analytical work, not for latency-sensitive serving (use MongoDB directly if you need that).

```sql
SELECT * FROM "plant-db-4"."phytozome_v14"."genes_231" WHERE ...
```

---

## Schemas

Under `"plant-db-7 postgresql"`, the **only** schemas you may query are:

| Schema | Contents |
|--------|----------|
| `public` | Raw CHADO tables and matviews |
| `denormalized` | Pre-joined synteny groups and pairs, HMM constituent data |
| `json_export` | Export-ready JSON views (`pac_gene_view`, `pac_transcript_view`, `pac_protein_annotation_view`, `pac_exon_view`, `pac_organism_view`, `pac_annotation_info_view`) |

Every query in this guide draws from these three schemas. Any other schema name you see (in the catalog browser, in `information_schema.schemata`, in old code, or anywhere else) is out of scope for this guide and must not be queried. This is non-negotiable.

### Tables and matviews used by the API (use the same set)

**`public` tables** — `biomaterial`, `biomaterialpropjson`, `db`, `dbxref`, `dbxref_relationship`, `dbxrefprop`, `feature`, `feature_dbxref`, `feature_pub`, `feature_relationship`, `featureloc`, `featureprop`, `featurepropjson`, `grp`, `grpmember`, `grpprop`, `organism`, `organism_dbxref`, `pac_protein_family`, `pub`

**`public` materialized views** — `defline`, `metabolic_pathway`, `pac_gene_expression2`, `pac_genome_worklist`, `pac_metabolic_pathway`, `pac_proteome_properties`, `pac_synteny_view`

**`denormalized`** — `denormalized.pac_synteny_grps`, `denormalized.pac_synteny_pairs`, `denormalized.hmm_constituent_jsonb`, `denormalized.hmm_nonconstituent_jsonb`

PostgreSQL materialized views (matviews) are queryable but **not enumerated** by Dremio (no `SHOW TABLES`, no catalog browser, no `INFORMATION_SCHEMA.TABLES` entry). To list them at runtime:

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT schemaname, matviewname
    FROM pg_matviews
    WHERE schemaname IN (''public'', ''denormalized'', ''json_export'')
    ORDER BY schemaname, matviewname
  ')
)
```

---

## CHADO data model — the bits you need

Phytozome uses the CHADO biological schema. The handful of tables you need to know:

| Table | Role |
|-------|------|
| `feature` | The universal record. One row per gene, transcript (mRNA), protein (peptide), exon, CDS, UTR, scaffold, chromosome, **and** proteome. Always filter by `type_id` (see Key Type IDs). Key columns: `feature_id`, `uniquename` (PAC ID), `name` (locus / gene name), `type_id`, `organism_id`, `dbxref_id`, `residues` (sequence — often NULL in the lakehouse). |
| `feature_relationship` | Parent/child links between features. `subject_id` and `object_id` both point to `feature.feature_id`; `type_id` says what relationship (gene → transcript, transcript → protein, transcript → exon, etc.). |
| `featureprop` | Key/value-style annotation per feature. `feature_id` + `type_id` + `value` + `rank`. Used for defline, symbol, gene_type, longest-transcript flag, etc. |
| `featurepropjson` | Same shape but the `value` is a JSON blob (e.g. co-expression coefficient arrays). |
| `featureloc` | Chromosomal/scaffold location of a feature. `feature_id` (the located feature), `srcfeature_id` (the scaffold/chromosome it's on), `fmin`/`fmax` (0-based half-open coordinates), `strand` (+1 or -1). |
| `dbxref` | External cross-reference. One row per (database, accession) pair. Key columns: `dbxref_id`, `db_id`, `accession`, `description`. |
| `db` | The cross-reference database catalog. `db_id`, `name` ("PFAM", "PANTHER", "InterPro", "GO", "PACProteome", etc.). |
| `feature_dbxref` | Links a feature to a dbxref. Used to attach PFAM/PANTHER/InterPro/GO/etc. annotations to individual proteins. |
| `dbxref_relationship` | Links between two dbxrefs. Used to link a proteome's dbxref to an external dbxref (e.g. NCBI Assembly accession). |
| `grp`, `grpmember`, `grpprop` | Generic CHADO group tables. Used here for atlas groups, pathway memberships, and certain family operations. |
| `pub`, `feature_pub` | Publications and the features they describe. |
| `organism`, `organism_dbxref` | Species records and links to NCBI taxonomy. |
| `biomaterial`, `biomaterialpropjson` | Sample / experimental material records. |

Phytozome-specific matviews on top of CHADO:

| Matview | Role |
|---------|------|
| `pac_proteome_properties` | One row per proteome with assembly/annotation stats, BUSCO completeness, restriction policy, common/organism names. |
| `pac_genome_worklist` | The (dbxref_id, organism_id) → phytozome_genome_id mapping. Join key from feature to proteome. |
| `pac_protein_family` | Protein → cluster → method (PFAM/PANTHER/InterPro). `protein_id` joins `feature.feature_id`; `dbxref_id` joins `dbxref.dbxref_id`. |
| `pac_gene_expression2` | Bulk RNA-seq expression. One row per (gene, sample). |
| `pac_metabolic_pathway` | Maps proteome → pathway membership. |
| `metabolic_pathway` | Pathway → feature membership. |
| `pac_synteny_view` | Per-pair synteny rollup used by the API. |
| `defline` | Pre-joined feature deflines. |

In `denormalized`:

| Object | Role |
|--------|------|
| `denormalized.pac_synteny_grps` | Synteny groups: proteome_id1/organism1, proteome_id2/organism2, chrom, start/end, group uniquename. |
| `denormalized.pac_synteny_pairs` | Gene pairs within each synteny group. |
| `denormalized.hmm_constituent_jsonb`, `denormalized.hmm_nonconstituent_jsonb` | Pre-built JSON blobs of HMM constituent/non-constituent members per method. |

In `json_export`:

| View | Role |
|------|------|
| `json_export.pac_gene_view`, `pac_transcript_view`, `pac_protein_annotation_view`, `pac_exon_view`, `pac_organism_view`, `pac_annotation_info_view` | One-row-per-entity rollups designed for JSON export (gene/transcript/protein/exon/organism/annotation). Useful when you need a flat-record summary instead of joining CHADO tables yourself. |

---

## Discover what kinds of annotation each gene/protein has

The cheap way to enumerate what *could* be attached is to read the small catalog tables, not to scan the big linking tables. `feature_dbxref` is hundreds of millions of rows; `featureprop` is tens of millions. Don't `GROUP BY` over them just to find out which methods/properties exist.

### External databases catalogued (instant)

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT db_id, name, description
    FROM db
    ORDER BY name
  ')
)
```

The `db` table is small (a few hundred rows). It lists every external database the data model knows about — PFAM, PANTHER, InterPro, GO, NCBI Taxonomy, PACProteome, etc.

### Featureprop properties catalogued (instant)

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT ct.cvterm_id AS type_id,
           ct.name      AS property,
           cv.name      AS controlled_vocab
    FROM cvterm ct
    JOIN cv ON cv.cv_id = ct.cv_id
    WHERE cv.name IN (''feature_property'', ''sequence'', ''curated'')
    ORDER BY cv.name, ct.name
  ')
)
```

`cvterm` is small. This returns every property type_id that a CHADO `featureprop` row could carry, without scanning featureprop itself.

### If you really need usage counts (sampled, not exact)

For "which databases are actually used heavily" use a small sample of `feature_dbxref` rather than a full scan:

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT db.name, COUNT(*) AS sample_attachments
    FROM feature_dbxref fd TABLESAMPLE SYSTEM (1)
    JOIN dbxref dx ON dx.dbxref_id = fd.dbxref_id
    JOIN db        ON db.db_id     = dx.db_id
    GROUP BY db.name
    ORDER BY sample_attachments DESC
  ')
)
```

`TABLESAMPLE SYSTEM (1)` reads ~1% of the table blocks — orders of magnitude faster than a full scan. Counts are approximate but the *ordering* (heavily-used vs rarely-used) is reliable.

---

## Discover available proteomes

This is the first step when a user says "what plants are in Phytozome?" or asks for a list of species.

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT phytozome_genome_id, common_name, organism_name, organism_abbreviation,
           annotation_version, assembly_version,
           transcript_count, locus_count, scaffold_count, scaffold_n50,
           eukaryote_busco_completeness, embryophyte_busco_completeness,
           data_restriction_policy
    FROM pac_proteome_properties
    ORDER BY organism_name
  ')
)
```

To match a user's free-text species mention to a proteome:

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT phytozome_genome_id, common_name, organism_name
    FROM pac_proteome_properties
    WHERE LOWER(common_name)   LIKE ''%poplar%''
       OR LOWER(organism_name) LIKE ''%populus%''
  ')
)
```

---

## Find info on a gene

The user typically gives you a **locus name** (`AT1G01010`), a **transcript name** (`AT1G01010.1`), or a **PAC ID** (`PAC:27370627`). Resolve to the gene, transcript, and protein PAC IDs plus the proteome:

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT t.uniquename  AS transcript_id,
           g.uniquename  AS gene_id,
           t.name        AS transcript_name,
           g.name        AS gene_name,
           p.name        AS protein_name,
           w.accession   AS proteome_id
    FROM feature t
    JOIN feature_relationship gt ON t.feature_id = gt.subject_id
    JOIN feature g              ON g.feature_id = gt.object_id
    JOIN feature_relationship tp ON t.feature_id = tp.object_id
    JOIN feature p              ON p.feature_id = tp.subject_id
    JOIN pac_genome_worklist w  ON t.dbxref_id = w.dbxref_id
                               AND t.organism_id = w.organism_id
    WHERE t.uniquename = ''PAC:27370627''
       OR t.name       = ''AT1G01010.1''
  ')
)
```

For richer per-transcript info (chromosome, coordinates, gene type, etc.), use the JSON view in `json_export`:

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT * FROM json_export.pac_transcript_view
    WHERE uniquename = ''PAC:27370627''
  ')
)
```

### List all transcripts in a proteome

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT f.uniquename, f.name
    FROM feature f
    JOIN pac_genome_worklist w
      ON f.dbxref_id = w.dbxref_id AND f.organism_id = w.organism_id
    WHERE w.accession = ''444''
      AND f.type_id = 349       -- mRNA
    ORDER BY f.name
  ')
)
```

---

## Gene structure: exons, CDS, UTRs, introns

Each transcript has multiple child features (exons, CDS segments, UTRs) linked via `feature_relationship` where the transcript is the `object_id` and the structural piece is the `subject_id`. Filter by `type_id` to pick the kind you want.

Common structural type IDs (verify with `cvterm` if you need others):

| type_id | feature kind |
|---------|--------------|
| 818 | gene |
| 349 | mRNA (transcript) |
| 219 | peptide (protein) |
| 220 | exon |
| 240 | CDS |
| 295 | five_prime_UTR |
| 296 | three_prime_UTR |

### Exons of a transcript, in order along the chromosome

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT e.uniquename AS exon_id,
           l.fmin       AS exon_start,
           l.fmax       AS exon_end,
           l.strand
    FROM feature t
    JOIN feature_relationship fr ON fr.object_id = t.feature_id
    JOIN feature e               ON e.feature_id = fr.subject_id
    JOIN featureloc l            ON l.feature_id = e.feature_id
    WHERE t.uniquename = ''PAC:27370627''
      AND t.type_id = 349
      AND e.type_id = 220
    ORDER BY l.fmin
  ')
)
```

Same template with `e.type_id = 240` for CDS, `295` for 5' UTR, `296` for 3' UTR.

### Use the pre-joined exon view

For exon information that's also linked back to the parent gene/transcript:

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT * FROM json_export.pac_exon_view
    WHERE transcript_uniquename = ''PAC:27370627''
  ')
)
```

---

## Chromosomal location of a gene/transcript

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT f.uniquename, f.name,
           src.uniquename AS scaffold,
           src.name       AS scaffold_name,
           l.fmin, l.fmax, l.strand
    FROM feature f
    JOIN featureloc l ON l.feature_id = f.feature_id
    JOIN feature src  ON src.feature_id = l.srcfeature_id
    WHERE f.uniquename = ANY(ARRAY[''PAC:27370627''])
  ')
)
```

`srcfeature_id` is the scaffold/chromosome the feature lives on. `fmin`/`fmax` are 0-based half-open. `strand` is `+1` or `-1`.

## Gene neighborhood: genes near a target gene

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    WITH target AS (
      SELECT l.srcfeature_id, l.fmin, l.fmax, f.organism_id, f.dbxref_id
      FROM feature f
      JOIN featureloc l ON l.feature_id = f.feature_id
      WHERE f.uniquename = ''PAC:27370627''
        AND f.type_id = 818
    )
    SELECT n.uniquename AS neighbor_gene_id,
           n.name       AS neighbor_gene_name,
           nl.fmin, nl.fmax, nl.strand,
           nl.fmin - t.fmax AS distance_from_target
    FROM target t
    JOIN featureloc nl ON nl.srcfeature_id = t.srcfeature_id
    JOIN feature n     ON n.feature_id     = nl.feature_id
    WHERE n.type_id = 818
      AND ABS(nl.fmin - t.fmax) < 50000     -- within 50 kb
    ORDER BY ABS(nl.fmin - t.fmax)
  ')
)
```

---

## Get the defline of a gene

Defline = the curated descriptive sentence for a gene ("photosystem II reaction center protein D1", etc.).

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT f.uniquename, fp.value AS defline
    FROM feature f
    JOIN featureprop fp ON f.feature_id = fp.feature_id
    WHERE fp.type_id = 39157
      AND f.type_id  = 818      -- gene
      AND f.uniquename = ANY(ARRAY[''PAC:27370627'', ''PAC:27370628''])
  ')
)
```

---

## Find genes/proteins by PFAM, PANTHER, or InterPro accession

This is the answer to "find me everything with PFAM domain X." Phytozome assigns proteins to families/clusters built on each annotation method:

- **PFAM** — `db.name = 'PFAM'`, db_id = 11
- **PANTHER** — `db.name = 'PANTHER'`, db_id = 101
- **InterPro** — `db.name = 'InterPro'`, db_id = 161

Each PFAM/PANTHER/InterPro accession maps to one or more **clusters** (groups of related proteins). Each cluster has members across all proteomes.

### All proteins assigned to a PFAM/PANTHER/InterPro accession

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT g.cluster_id, g.name AS cluster_name,
           d.accession AS method_id, d.description AS method_name,
           o.abbreviation AS organism,
           w.accession AS phytozome_genome_id,
           f.name AS protein_name,
           f.uniquename AS transcript_id
    FROM pac_protein_family g
    JOIN feature f                  ON g.protein_id = f.feature_id
    JOIN dbxref d                   ON g.dbxref_id  = d.dbxref_id
    JOIN organism o                 ON o.organism_id = f.organism_id
    JOIN pac_genome_worklist w      ON w.dbxref_id = f.dbxref_id
                                   AND w.organism_id = f.organism_id
    WHERE f.type_id = 219           -- peptide / protein
      AND d.db_id IN (11, 101, 161) -- PFAM, PANTHER, InterPro
      AND d.accession = ANY(ARRAY[''PF00001'', ''PTHR12345'', ''IPR000123''])
    ORDER BY d.accession, o.abbreviation, f.name
  ')
)
```

Limit to a single proteome by adding `AND w.accession = '444'`.

### What family/method does a specific protein belong to?

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT g.cluster_id,
           d.accession    AS method_id,
           d.description  AS method_name,
           f.name         AS protein_name,
           f.uniquename   AS transcript_id
    FROM pac_protein_family g
    JOIN feature f  ON g.protein_id = f.feature_id
    JOIN dbxref d   ON g.dbxref_id  = d.dbxref_id
    WHERE f.type_id = 219
      AND f.uniquename = ''PAC:27370627''
  ')
)
```

---

## Find proteins by GO term

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT DISTINCT f_protein.feature_id,
                    f_protein.uniquename AS protein_id
    FROM dbxref dx
    JOIN feature_dbxref fd       ON fd.dbxref_id = dx.dbxref_id
    JOIN feature_relationship fr ON fr.subject_id = fd.feature_id
    JOIN feature f_protein       ON f_protein.feature_id = fr.object_id
    WHERE dx.accession = ''GO:0052742''
      AND f_protein.type_id = 219
  ')
)
```

---

## Family membership of a gene

(See [the family/method query above](#what-familymethod-does-a-specific-protein-belong-to).) The protein-level family table is `pac_protein_family`.

## Members of a family/cluster

If the user gives you a numeric `cluster_id`:

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT g.cluster_id,
           d.accession   AS method_id,
           w.accession   AS proteome_id,
           f.name        AS protein_name,
           f.uniquename  AS transcript_id
    FROM pac_protein_family g
    JOIN feature f             ON g.protein_id = f.feature_id
    JOIN dbxref d              ON g.dbxref_id  = d.dbxref_id
    JOIN pac_genome_worklist w ON f.dbxref_id = w.dbxref_id
                              AND f.organism_id = w.organism_id
    WHERE f.type_id = 219
      AND g.cluster_id = ANY(ARRAY[12345, 12346])
    ORDER BY w.accession, f.name
  ')
)
```

---

## Find homologs of a gene

Pairwise homologs (Diamond hits) live in MongoDB at `"plant-db-4".diamond_homologs_v14.homologs_<query_pid>_<target_pid>`. The collection name encodes the **query proteome** and **target proteome**: `homologs_231_444` is hits of every gene in proteome 231 against proteome 444.

### Homologs of a single gene against one target species

```sql
SELECT *
FROM "plant-db-4"."diamond_homologs_v14"."homologs_231_444"
WHERE "queryIdentifier" = 'PAC:27370627';
```

### Homologs against every other species

There is one collection per (query, target) proteome pair — hundreds per query proteome. List them, then loop:

```sql
SELECT TABLE_NAME
FROM INFORMATION_SCHEMA."TABLES"
WHERE TABLE_SCHEMA = 'plant-db-4.diamond_homologs_v14'
  AND TABLE_NAME LIKE 'homologs_231_%'
ORDER BY TABLE_NAME;
```

---

## Get a gene record from MongoDB

Each proteome has a `genes_<pid>` collection with the full curated gene document (identifiers, locations, annotations, expression summary, family memberships, etc.).

```sql
SELECT *
FROM "plant-db-4"."phytozome_v14"."genes_231"
WHERE "primaryidentifier" = 'PAC:27370627'
LIMIT 1;
```

To see what proteomes have gene documents:

```sql
SELECT TABLE_NAME
FROM INFORMATION_SCHEMA."TABLES"
WHERE TABLE_SCHEMA = 'plant-db-4.phytozome_v14'
  AND TABLE_NAME LIKE 'genes_%'
ORDER BY TABLE_NAME;
```

---

## Discover available expression datasets

Bulk RNA-seq expression is in the matview `pac_gene_expression2`. **It is large (tens of millions of rows)** — manifest-style discovery queries must be written to avoid scanning it more than needed. Prefer the patterns below in this order.

### Just the list of datasets (fastest)

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT DISTINCT experiment_group
    FROM pac_gene_expression2
    ORDER BY 1
  ')
)
```

### Dataset + library count

Use `COUNT(DISTINCT sample_name)` (the library count is small — typically dozens per dataset). Avoid `COUNT(DISTINCT uniquename)` in the same query unless you really need a gene count: it forces a giant per-group dedup over millions of values.

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT experiment_group,
           COUNT(DISTINCT sample_name) AS library_count
    FROM pac_gene_expression2
    GROUP BY experiment_group
    ORDER BY 1
  ')
)
```

### Add gene counts only if needed

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT experiment_group,
           COUNT(DISTINCT uniquename)  AS gene_count,
           COUNT(DISTINCT sample_name) AS library_count
    FROM pac_gene_expression2
    GROUP BY experiment_group
    ORDER BY 1
  ')
)
```

### Which species have expression data (sub-second)

`pac_gene_expression2` is large (~90M rows). Asking which species/proteomes appear in it via `SELECT DISTINCT` or even a CTE forces a full scan. The fast form **flips the question**: drive from the small `pac_genome_worklist` matview (one row per proteome) and use `EXISTS` to probe `pac_gene_expression2`. With the index on `pac_gene_expression2 (organism_id, dbxref_id)`, each probe is an index lookup and the whole query is sub-millisecond.

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT w.accession  AS proteome_id,
           pp.common_name,
           pp.organism_name
    FROM pac_genome_worklist w
    JOIN pac_proteome_properties pp
      ON pp.phytozome_genome_id = w.accession
    WHERE EXISTS (
      SELECT 1 FROM pac_gene_expression2 p
      WHERE p.organism_id = w.organism_id
        AND p.dbxref_id   = w.dbxref_id
    )
    ORDER BY pp.organism_name
  ')
)
```

**Do not** rewrite this as `SELECT DISTINCT organism_id, dbxref_id FROM pac_gene_expression2 ...` — that still scans the whole table even with the index. The EXISTS form above lets the planner probe via index per proteome.

### Which datasets cover which species

Same idea: drive from the small `pac_genome_worklist` table; probe `pac_gene_expression2` for the dataset list per proteome. With the index on `(organism_id, dbxref_id)` this is sub-second.

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT w.accession  AS proteome_id,
           pp.common_name,
           pp.organism_name,
           (SELECT array_agg(DISTINCT experiment_group ORDER BY experiment_group)
            FROM pac_gene_expression2 p
            WHERE p.organism_id = w.organism_id
              AND p.dbxref_id   = w.dbxref_id) AS experiment_groups
    FROM pac_genome_worklist w
    JOIN pac_proteome_properties pp
      ON pp.phytozome_genome_id = w.accession
    WHERE EXISTS (
      SELECT 1 FROM pac_gene_expression2 p
      WHERE p.organism_id = w.organism_id
        AND p.dbxref_id   = w.dbxref_id
    )
    ORDER BY pp.organism_name
  ')
)
```

### Just the dataset names

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT DISTINCT experiment_group
    FROM pac_gene_expression2
    ORDER BY 1
  ')
)
```

## Get expression for a gene

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT p.uniquename AS gene_id,
           p.name AS genename,
           p.value AS defline,
           p.sample_name AS libraryname,
           p.experiment_group,
           p.expression
    FROM pac_gene_expression2 p
    WHERE p.uniquename = ANY(ARRAY[''PAC:32803800''])
    ORDER BY 1, 4, 3
  ')
)
```

Columns: `uniquename` (PAC ID), `name` (gene name), `value` (defline), `sample_name` (library / sample), `experiment_group` (dataset), `expression` (TPM or FPKM depending on dataset).

---

## Find co-expressed genes

Co-expression is pre-computed (Pearson coefficients) and stored as a JSON blob per gene in `featurepropjson` with `type_id = 39249`.

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT f.name AS name,
           f.uniquename AS uniquename,
           p.value AS coexpression
    FROM featurepropjson p, feature f
    WHERE p.feature_id = f.feature_id
      AND p.type_id = 39249
      AND f.uniquename = ANY(ARRAY[''PAC:27370627''])
  ')
)
```

The `coexpression` column is a JSON array — one entry per experiment group, each containing a `data` array of `{name, uniquename, coexpression, p-value}` records. Apply threshold and `top_n` filtering in Python:

```python
import json

threshold, count = 0.9, 25
for row in results:
    data = json.loads(row['coexpression'])
    for group in data:
        top = sorted(
            (g for g in group['data'] if g['coexpression'] > threshold),
            key=lambda x: -x['coexpression']
        )[:count]
        print(group['group_name'], top)
```

---

## Atlas (cross-proteome groupings)

Phytozome organizes proteomes into curated "atlas" groups (e.g. Bryophytes, Liverworts, etc.). These are simple groups in the `grp` table with `type_id = 39343`.

### List all atlas groups

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT g.uniquename AS atlas_id,
           g.name       AS atlas_label,
           p.value      AS member_proteome_ids
    FROM grp g, grpprop p
    WHERE g.type_id = 39343
      AND p.grp_id  = g.grp_id
    ORDER BY g.name
  ')
)
```

`member_proteome_ids` is a delimited list of phytozome_genome_id values.

### Which atlas group(s) contain a given proteome?

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT g.uniquename AS atlas_id, g.name AS atlas_label
    FROM grp g, grpprop p
    WHERE g.type_id = 39343
      AND p.grp_id  = g.grp_id
      AND p.value LIKE ''%444%''
  ')
)
```

(For a more exact match, parse `value` instead of `LIKE`.)

---

## Metabolic Pathways

### List all pathways

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT DISTINCT uniquename AS pathway_id,
           name              AS pathway_name
    FROM metabolic_pathway_proteome
    ORDER BY name
  ')
)
```

### Pathways found in a given proteome

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT DISTINCT uniquename AS pathway_id,
           name              AS pathway_name,
           proteome
    FROM metabolic_pathway_proteome
    WHERE proteome = ANY(ARRAY[''444''])
    ORDER BY name
  ')
)
```

### Pathways a gene participates in

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT DISTINCT g.uniquename AS pathway_id,
           g.name              AS pathway_name,
           f.name              AS gene_name,
           f.uniquename        AS pac_id
    FROM metabolic_pathway g, feature f
    WHERE g.feature_id = f.feature_id
      AND f.type_id = 818
      AND f.uniquename = ANY(ARRAY[''PAC:27370627''])
  ')
)
```

### Genes in a given pathway

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT DISTINCT g.uniquename AS pathway_id,
           g.name              AS pathway_name,
           f.name              AS gene_name,
           f.uniquename        AS pac_id,
           w.accession         AS proteome_id
    FROM metabolic_pathway g
    JOIN feature f             ON g.feature_id = f.feature_id
    JOIN pac_genome_worklist w ON f.dbxref_id  = w.dbxref_id
                              AND f.organism_id = w.organism_id
    WHERE g.uniquename = ''PWY-1234''
      AND f.type_id = 818
  ')
)
```

---

## Biosamples / experimental material

`biomaterial` holds samples used in the data. `biomaterialpropjson` carries structured per-sample metadata (tissue, condition, growth stage, etc.) as JSON.

### Browse biomaterials for a proteome

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT b.biomaterial_id, b.name, b.dbxref_id, bpj.value AS metadata_json
    FROM biomaterial b
    LEFT JOIN biomaterialpropjson bpj ON bpj.biomaterial_id = b.biomaterial_id
    LIMIT 50
  ')
)
```

Parse `metadata_json` client-side to filter by tissue, treatment, etc.

---

## Cross-references to external databases

CHADO stores cross-references to external resources (NCBI Taxonomy, GenBank, RefSeq, UniProt, etc.) in `dbxref` joined via `feature_dbxref` (for per-feature xrefs) or `dbxref_relationship` (for proteome-level xrefs).

### What external databases are linked to a feature?

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT db.name AS database, d.accession, d.description
    FROM feature f
    JOIN feature_dbxref fd ON fd.feature_id = f.feature_id
    JOIN dbxref d          ON d.dbxref_id    = fd.dbxref_id
    JOIN db                ON db.db_id       = d.db_id
    WHERE f.uniquename = ''PAC:27370627''
    ORDER BY db.name, d.accession
  ')
)
```

### Cross-references for a proteome (NCBI Assembly, etc.)

The API includes proteome-level external DBs whose `db_id` is in `{173, 209, 210, 213, 214, 216}` (NCBI Assembly, NCBI BioProject, NCBI BioSample, NCBI Taxonomy, etc.).

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT db.name AS database, d.accession, d.description
    FROM dbxref w
    JOIN dbxref_relationship r ON r.subject_id = w.dbxref_id
    JOIN dbxref d              ON d.dbxref_id   = r.object_id
    JOIN db                    ON db.db_id      = d.db_id
    WHERE w.accession = ''444''
      AND db.db_id IN (173, 209, 210, 213, 214, 216)
  ')
)
```

---

## Synteny

### What synteny comparisons are available?

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT DISTINCT proteome_id1, organism1, proteome_id2, organism2
    FROM denormalized.pac_synteny_grps
    ORDER BY organism1, organism2
  ')
)
```

### Syntenic genes for a given gene

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT p.gene1, p.gene2,
           g.organism1, g.chrom1, p.start1, p.end1,
           g.organism2, g.chrom2, p.start2, p.end2
    FROM denormalized.pac_synteny_grps  g,
         denormalized.pac_synteny_pairs p
    WHERE p.grp_uniquename = g.uniquename
      AND (LOWER(p.gene1) = ''potri.001g000400.1''
           OR LOWER(p.gene2) = ''potri.001g000400.1'')
      AND g.organism1 IN (''Ptrichocarpa'', ''Athaliana'')
  ')
)
```

---

## Publications for a proteome

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT w.accession AS proteome_id,
           p.uniquename AS doi, p.title, p.volumetitle AS journal,
           p.volume, p.issue, p.pages, p.pyear AS year,
           CASE WHEN fp.rank = 0 THEN ''reference_publication'' ELSE ''related_publication'' END AS reference_type
    FROM pub p, feature f, feature_pub fp, pac_genome_worklist w
    WHERE p.pub_id = fp.pub_id
      AND f.feature_id = fp.feature_id
      AND f.dbxref_id = w.dbxref_id
      AND f.organism_id = w.organism_id
      AND f.type_id = 1608      -- proteome
      AND w.accession = ''444''
    ORDER BY reference_type, p.pyear DESC
  ')
)
```

---

## HMM constituents (precomputed)

For methods (PFAM/PANTHER/InterPro families) where Phytozome maintains HMM-based "constituent" and "non-constituent" categorization, lookup is fast via `denormalized`:

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT uniquename, method_id, data
    FROM denormalized.hmm_constituent_jsonb
    WHERE method_id = ''PF00069''
  ')
)
```

`data` is a JSON blob describing the constituent members of the HMM cluster. Use `denormalized.hmm_nonconstituent_jsonb` for the non-constituent set.

---

## Cluster-level details

Given a numeric cluster_id (e.g. from a family-membership query):

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT DISTINCT g.name AS cluster_name, g.cluster_id,
           d.accession AS method_id, d.description AS method_name,
           g.size AS member_count
    FROM pac_protein_family g, dbxref d
    WHERE g.dbxref_id = d.dbxref_id
      AND g.cluster_id = ANY(ARRAY[12345])
  ')
)
```

---

## Reference tables

### Key feature types (`feature.type_id`)

| type_id | feature kind |
|---------|--------------|
| 818 | gene |
| 349 | mRNA / transcript |
| 219 | peptide / protein |
| 1608 | proteome |
| 220 | exon |
| 240 | CDS |
| 295 | five_prime_UTR |
| 296 | three_prime_UTR |

### Featureprop type IDs (selected)

| type_id | property |
|---------|----------|
| 39157 | defline |
| 39233 | annotation_locus_count |
| 39234 | annotation_transcript_count |
| 39249 | coexpression JSON |
| 39253 | family_size (in grpprop) |
| 39252 | gat (in grpprop) |
| 39260 | family cluster (grp.type_id for family clusters) |
| 39256 | metabolic pathway grp.type_id |
| 39261 | eukaryote_busco_completeness |
| 39262 | embryophyte_busco_completeness |
| 39342 | busco_completeness |
| 39267 | data_restriction_policy |
| 39343 | atlas group |
| 39341 | gene_defline (alternative defline type) |

To find or verify any type_id, query `cvterm` joined to `cv`:

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT cv.name AS controlled_vocab, ct.name AS term, ct.cvterm_id AS type_id
    FROM cvterm ct
    JOIN cv     ON cv.cv_id = ct.cv_id
    WHERE ct.name IN (''defline'', ''gene'', ''mRNA'', ''polypeptide'')
  ')
)
```

### Method databases (`dbxref.db_id`)

| Database | db_id | Used for |
|----------|-------|----------|
| PFAM | 11 | protein family / domain hits |
| PANTHER | 101 | protein family classification |
| InterPro | 161 | integrated domain hits |
| PACProteome | (varies) | proteome accession registry — the `dbxref.accession` is the phytozome_genome_id |
| NCBI Taxonomy | (varies) | organism cross-reference |

External proteome-level xrefs typically have db_id in the set `{173, 209, 210, 213, 214, 216}` (NCBI Assembly, BioProject, BioSample, etc.). The exact mapping per `db_id` can be inspected with:

```sql
SELECT * FROM TABLE(
  "plant-db-7 postgresql".external_query('
    SELECT db_id, name, description
    FROM db
    WHERE db_id IN (11, 101, 161, 173, 209, 210, 213, 214, 216)
    ORDER BY db_id
  ')
)
```

---

## Critical Pitfalls

| Wrong | Correct |
|-------|---------|
| Querying any schema other than `public`, `denormalized`, or `json_export` under `"plant-db-7 postgresql"` | Use only those three; the rest are out of scope |
| Querying `"plant-db-7 postgresql"` without `external_query` | Wrap every CHADO query in `TABLE("plant-db-7 postgresql".external_query('...'))` |
| Trying `external_query` on `plant-db-4` (MongoDB) | Not supported; use Dremio SQL directly |
| Single quotes inside `external_query` body not escaped | Double them: `'foo'` → `''foo''` |
| Expecting matviews in Dremio's catalog browser | They don't appear; query `pg_matviews` via `external_query` |
| Assuming a gene/transcript/protein share a PAC ID | They have distinct PAC IDs; the gene's, transcript's, and protein's are all different |
| Filtering `feature` without `type_id` | Always filter by `type_id` — `feature` holds genes, mRNAs, proteins, and proteomes |
| Expecting MongoDB-fast point lookups via Dremio | Dremio has a ~1-2s per-query floor; for live-serving go to MongoDB directly |
| Querying for sequences | Not available; metadata only |
| `::` type cast in Dremio SQL | Use `CAST(x AS type)` |
| `~` regex in Dremio SQL | Use `REGEXP_LIKE(col, pattern)` |
