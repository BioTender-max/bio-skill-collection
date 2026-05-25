# Exploring IMG Genomes: Genome Metadata Queries

This guide documents patterns for querying genome-level metadata (genome size, GC content, taxonomy, quality) across the IMG and GOLD databases. It is based on experience with genus-level taxon lookups but applies broadly to any genome metadata query.

---

## Two Taxonomy Systems

IMG stores **two independent classification systems** for the same genomes:

| System | Location | Join key | Notes |
|--------|----------|----------|-------|
| **NCBI taxonomy** | `img_core_v400.taxon` | `taxon_oid` (primary key) | Standard NCBI lineage; fields `domain`, `phylum`, `ir_class`, `ir_order`, `family`, `genus`, `species` embedded directly in the taxon row |
| **GTDB taxonomy (IMG-native)** | `img_core_v400.taxon_gtdbtk_lineage` | `taxon_oid` — direct, no fan-out | GTDB-Tk classifications for IMG genomes; pre-split into individual rank columns; also carries CheckM2 quality scores. Covers **Bacteria (99.8%) and Archaea (99.4%)** essentially completely. Taxons without GTDB are almost entirely data types GTDB doesn't apply to: metagenomes/metatranscriptomes (`*Microbiome` domain), Viruses, Plasmids, and Eukaryota. |

**Always query both** when doing a genus-level or higher search — GTDB frequently reclassifies genera (splitting, lumping, or renaming), so a NCBI genus search can miss genomes that GTDB assigns to a differently-named clade, and vice versa.

> **Note on the GOLD `gtdb` table**: `"gold-db-2 postgresql".gold.gtdb` covers all public NCBI genomes (not just IMG-annotated ones) and links via `ncbi_bioproject`, which can produce fan-out. Use it when you need to survey all NCBI public genomes, not just those in IMG.

### Querying NCBI taxonomy (IMG taxon table)
```sql
SELECT taxon_oid, taxon_display_name, genus, species, analysis_project_type
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE genus = 'MyGenus'
  AND is_public = 'Yes'
  AND obsolete_flag = 'No'
```

### Querying GTDB taxonomy (IMG taxon_gtdbtk_lineage table)

The `taxon_gtdbtk_lineage` table lives in `img_core_v400` and joins directly on `taxon_oid`:

| Column | Type | Description |
|--------|------|-------------|
| `taxon_oid` | BIGINT | IMG taxon OID — direct join key |
| `gtdbtk_lineage` | VARCHAR | Full lineage string (`d__Bacteria;p__...;g__MyGenus;s__...`) |
| `gtdbtk_domain` | VARCHAR | GTDB domain |
| `gtdbtk_phylum` | VARCHAR | GTDB phylum |
| `gtdbtk_class` | VARCHAR | GTDB class |
| `gtdbtk_order` | VARCHAR | GTDB order |
| `gtdbtk_family` | VARCHAR | GTDB family |
| `gtdbtk_genus` | VARCHAR | GTDB genus |
| `gtdbtk_species` | VARCHAR | GTDB species |
| `checkm_completeness` | FLOAT | CheckM2 completeness (%) |
| `checkm_contamination` | FLOAT | CheckM2 contamination (%) |
| `version_info` | VARCHAR | GTDB-Tk + database version string |

```sql
-- Match a GTDB genus and all sub-genera (e.g. MyGenus_A, MyGenus_B)
SELECT t.taxon_oid, t.taxon_display_name, t.analysis_project_type,
       g.gtdbtk_genus, g.gtdbtk_species,
       g.checkm_completeness, g.checkm_contamination
FROM "img-db-2 postgresql".img_core_v400.taxon t
JOIN "img-db-2 postgresql".img_core_v400.taxon_gtdbtk_lineage g
  ON t.taxon_oid = g.taxon_oid
WHERE REGEXP_LIKE(g.gtdbtk_genus, '^MyGenus')   -- matches MyGenus, MyGenus_A, MyGenus_B, …
  AND t.is_public = 'Yes'
  AND t.obsolete_flag = 'No'
```

Use `REGEXP_LIKE` with `^MyGenus` rather than `=` to catch GTDB sub-genera (e.g. `MyGenus_A`). Alternatively filter on the individual rank column with `LIKE 'MyGenus%'`. Because the join is on `taxon_oid`, there is **no fan-out** — one row per genome.

**GTDB-Tk only applies to Bacteria and Archaea.** Coverage for those domains is essentially complete (Bacteria 99.8%, Archaea 99.4%). Taxons without a GTDB entry are almost exclusively data types GTDB cannot classify: metagenomes and metatranscriptomes (`*Microbiome` domain, ~77% of uncovered), Viruses (~21%), Plasmids (~1%), and Eukaryota (~1%). Use `LEFT JOIN` when your query spans multiple domains or data types.

---

## Genome Size and GC Content

These fields are **not** in the `taxon` table itself. They live in `taxon_stats`:

| Field | Table | Description |
|-------|-------|-------------|
| `total_bases` | `img_core_v400.taxon_stats` | Total genome size in base pairs |
| `gc_percent` | `img_core_v400.taxon_stats` | GC content (%) |
| `n_scaffolds` | `img_core_v400.taxon_stats` | Number of scaffolds/contigs |

Join pattern:
```sql
SELECT t.taxon_oid, t.taxon_display_name,
       ts.total_bases / 1000000.0 AS genome_size_mb,
       ts.gc_percent,
       ts.n_scaffolds
FROM "img-db-2 postgresql".img_core_v400.taxon t
JOIN "img-db-2 postgresql".img_core_v400.taxon_stats ts
  ON t.taxon_oid = ts.taxon_oid
WHERE t.genus = 'MyGenus'
  AND t.is_public = 'Yes'
  AND t.obsolete_flag = 'No'
```

The GOLD `gtdb` table provides equivalent fields directly (`genome_size` in bp, `gc_percentage` in %) for all NCBI-deposited assemblies — useful when you want GTDB taxonomy + size/GC without going through IMG.

### Excluding plasmids and tiny records

The `taxon` table includes plasmid sequences (a few kb) alongside chromosomes. Always filter these out when computing genome size statistics:
```sql
AND ts.total_bases > 100000  -- exclude plasmids / very small records
```

---

## Quality Assessment

### `high_quality_flag` — what it means and when it's useful

`high_quality_flag` is **not** a mirror of `analysis_project_type`. It is IMG's internal QC assessment, and its usefulness varies by data type:

| Data type | `high_quality_flag = 'Yes'` | Interpretation |
|-----------|----------------------------|----------------|
| `Genome Analysis (Isolate)` | 98.1% (135,025 / 137,672) | **Meaningful QC gate.** The 1.9% flagged 'No' are genuinely lower-quality assemblies that failed IMG QC, independent of `seq_status` (there are Finished genomes with 'No' and Permanent Drafts with 'Yes'). Use as the primary quality filter for isolates. |
| `Metagenome-Assembled Genome` | 0.1% (22 / 18,721) | **Not informative.** Effectively always 'No'. The 22 'Yes' entries are legacy early-era records pre-dating modern MAG conventions. Do not use for MAG quality ranking. |
| `Single Cell Analysis (screened)` | 13.4% (270 / 2,014) | Somewhat informative — screened SAGs that passed QC. |
| `Single Cell Analysis (unscreened)` | 0.7% (56 / 8,124) | Mostly 'No'; not a reliable quality metric. |
| Metagenome/metatranscriptome types | NULL in >99% of records | Not applicable to community assemblies. |

### Quality filter by dataset type

```sql
-- Isolates: high_quality_flag is the right filter
WHERE t.analysis_project_type = 'Genome Analysis (Isolate)'
  AND t.high_quality_flag = 'Yes'

-- MAGs: ignore high_quality_flag; use CheckM2 from taxon_gtdbtk_lineage
-- High quality (MIMAG tier: ≥90% complete, ≤5% contaminated)
WHERE t.analysis_project_type = 'Metagenome-Assembled Genome'
  AND g.checkm_completeness >= 90
  AND g.checkm_contamination <= 5

-- MAGs: medium quality (MIMAG tier: ≥50% complete, ≤10% contaminated)
WHERE t.analysis_project_type = 'Metagenome-Assembled Genome'
  AND g.checkm_completeness >= 50
  AND g.checkm_contamination <= 10

-- MAGs: genome_completion as fallback when taxon_gtdbtk_lineage has no entry
WHERE t.analysis_project_type = 'Metagenome-Assembled Genome'
  AND t.genome_completion >= 80
```

**MIMAG quality thresholds** (applied to CheckM2 fields in `taxon_gtdbtk_lineage`):

| Tier | Completeness | Contamination |
|------|-------------|---------------|
| High quality | ≥90% | ≤5% |
| Medium quality | ≥50% | ≤10% |
| Low quality | <50% | >10% |

For isolates, `completeness_percentage` / `contamination_percentage` from `gold.analysis_project` are often NULL — they are frequently not filled in for traditional isolates.

---

## Linking IMG taxon to GOLD analysis_project

The GOLD `analysis_project` table holds additional quality fields (`completeness_percentage`, `contamination_percentage`, `scaffold_count`) and the `analysis_project_type`. Link via:

```sql
LEFT JOIN "gold-db-2 postgresql".gold.analysis_project ap
  ON t.analysis_project_id = ap.gold_id
```

`taxon.analysis_project_id` stores the GOLD Ga* identifier (e.g. `Ga0123456`), which matches `analysis_project.gold_id`.

**Caution**: for many older isolate genomes, GOLD completeness/contamination fields are NULL. The join is still useful for `analysis_project_type` confirmation.

---

## Linking GTDB to IMG taxon

Use `img_core_v400.taxon_gtdbtk_lineage` — it joins directly on `taxon_oid` with no fan-out:

```sql
LEFT JOIN "img-db-2 postgresql".img_core_v400.taxon_gtdbtk_lineage g
  ON t.taxon_oid = g.taxon_oid
```

Use `LEFT JOIN` (not `INNER JOIN`) when your query covers multiple domains or data types. Taxons without a GTDB entry are almost entirely data types GTDB doesn't apply to: metagenomes/metatranscriptomes, Viruses, Plasmids, and Eukaryota. For queries already filtered to `domain IN ('Bacteria', 'Archaea')` and individual-genome project types, coverage is effectively complete (99.8% / 99.4%).

**If you need GTDB data for genomes outside IMG** (all NCBI public genomes, not just JGI-annotated ones), fall back to the GOLD table:

```sql
FROM "gold-db-2 postgresql".gold.gtdb g
-- link to IMG via:
LEFT JOIN "gold-db-2 postgresql".gold.analysis_project ap
  ON g.ncbi_bioproject = ap.ncbi_bioproject_accession
```

**Caution with the GOLD route**: this join can produce multiple rows per GTDB entry (fan-out) if multiple analysis projects share the same BioProject accession. Always check row counts before and after the join, or use `COUNT(DISTINCT g.gtdb_id)` rather than `COUNT(*)` when aggregating.

---

## Standard Genome Metadata Query Template

```sql
SELECT
  t.taxon_oid,
  t.taxon_display_name,
  t.genus,
  t.species,
  t.analysis_project_type,
  t.high_quality_flag,
  t.genome_completion,
  ts.total_bases / 1000000.0  AS genome_size_mb,
  ts.gc_percent,
  ts.n_scaffolds,
  g.gtdbtk_genus,
  g.gtdbtk_species,
  g.checkm_completeness,
  g.checkm_contamination
FROM "img-db-2 postgresql".img_core_v400.taxon t
JOIN "img-db-2 postgresql".img_core_v400.taxon_stats ts
  ON t.taxon_oid = ts.taxon_oid
LEFT JOIN "img-db-2 postgresql".img_core_v400.taxon_gtdbtk_lineage g
  ON t.taxon_oid = g.taxon_oid
WHERE t.genus = 'MyGenus'          -- NCBI taxonomy filter
  AND t.is_public = 'Yes'
  AND t.obsolete_flag = 'No'
  AND ts.total_bases > 100000      -- exclude plasmids / tiny records
ORDER BY t.analysis_project_type, t.taxon_display_name
```

For aggregated statistics by type and quality:
```sql
SELECT
  analysis_project_type,
  high_quality_flag,
  COUNT(*)                              AS n,
  ROUND(MIN(ts.total_bases)/1e6, 2)    AS min_size_mb,
  ROUND(MAX(ts.total_bases)/1e6, 2)    AS max_size_mb,
  ROUND(AVG(ts.total_bases)/1e6, 2)    AS mean_size_mb,
  ROUND(MIN(ts.gc_percent), 1)         AS min_gc,
  ROUND(MAX(ts.gc_percent), 1)         AS max_gc,
  ROUND(AVG(ts.gc_percent), 1)         AS mean_gc
FROM "img-db-2 postgresql".img_core_v400.taxon t
JOIN "img-db-2 postgresql".img_core_v400.taxon_stats ts
  ON t.taxon_oid = ts.taxon_oid
WHERE t.genus = 'MyGenus'
  AND t.is_public = 'Yes'
  AND t.obsolete_flag = 'No'
  AND ts.total_bases > 100000
GROUP BY analysis_project_type, high_quality_flag
ORDER BY analysis_project_type, high_quality_flag
```

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Querying only NCBI genus | Always also check GTDB — genera are frequently split or renamed |
| Looking for GTDB data in GOLD for IMG genomes | Use `img_core_v400.taxon_gtdbtk_lineage` — joins directly on `taxon_oid`, no fan-out; pre-split rank columns and CheckM2 quality scores |
| GTDB join fan-out (GOLD route) | If you must use `gold.gtdb`, join via `ncbi_bioproject` can return multiple rows per genome; use `DISTINCT` or aggregate on `gtdb_id` |
| Assuming GOLD completeness/contamination is populated | For traditional isolates these fields are often NULL; use `high_quality_flag` instead |
| Including plasmid sequences in size statistics | Filter `total_bases > 100000` |
| Not filtering `obsolete_flag` | Always add `obsolete_flag = 'No'` to exclude superseded entries |
| Using `high_quality_flag` to rank MAG quality | For MAGs the flag is 'No' in 99.9% of cases — it carries no quality information. Use `checkm_completeness` / `checkm_contamination` from `taxon_gtdbtk_lineage` instead. |
| Ignoring `high_quality_flag` for isolates | For isolates the flag IS a meaningful QC gate (1.9% fail it, independent of `seq_status`). Always filter isolates with `high_quality_flag = 'Yes'` unless you specifically want low-quality entries. |
| Assuming all taxons have GTDB classification | GTDB only covers Bacteria and Archaea. Coverage for those domains is essentially complete (99.8% / 99.4%). Taxons without GTDB are metagenomes, Viruses, Plasmids, and Eukaryota — data types GTDB doesn't apply to. Use `LEFT JOIN` when queries span multiple domains. |
| GTDB genome count >> IMG count (when using gold.gtdb) | Expected — `gold.gtdb` aggregates all NCBI public genomes; `taxon_gtdbtk_lineage` covers only genomes processed through the JGI IMG pipeline |

---

## Related Documentation

- [IMG_data_types.md](IMG_data_types.md) — Full breakdown of analysis project types (isolates, MAGs, SAGs, metagenomes)
- [IMG-tables-reference.md](IMG-tables-reference.md) — Complete IMG table catalog including `taxon_stats` and all annotation tables
- [data-catalog.md](data-catalog.md) — All databases and key tables (GOLD, IMG, Portal)
