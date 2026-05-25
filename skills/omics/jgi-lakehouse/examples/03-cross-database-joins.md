# Cross-Database Joins & Common Pitfalls

Patterns for joining GOLD, IMG, and SRA tables - with documented pitfalls from real queries.

## Use Case
Link sequencing projects to gene annotations, SRA experiments, or ecosystem metadata across databases.

## Key Pitfalls (from benchmark testing)

| What You Might Try | Actual Column/Table |
|-------------------|---------------------|
| `project.ecosystem` | `study.ecosystem` (join via `master_study_id`) |
| `rnaseq_experiment.experiment_id` | `exp_oid` |
| `rnaseq_experiment.experiment_name` | `exp_name` |
| `sra_experiment_v2.platform` | `library_instrument` |
| `project.study_id` | `master_study_id` |

---

## Pattern 1: Project → Study (Ecosystem)

**Problem:** Ecosystem classification is NOT in project table.

**Solution:** Join to study via `master_study_id`:

```sql
SELECT
    p.gold_id,
    p.project_name,
    s.ecosystem,
    s.ecosystem_category,
    s.ecosystem_type,
    s.ecosystem_subtype
FROM "gold-db-2 postgresql".gold.project p
JOIN "gold-db-2 postgresql".gold.study s ON p.master_study_id = s.study_id
WHERE s.ecosystem IS NOT NULL
  AND p.is_public = 'Yes'
LIMIT 50
```

### Count Projects by Ecosystem
```sql
SELECT
    s.ecosystem,
    s.ecosystem_type,
    COUNT(DISTINCT p.gold_id) as project_count
FROM "gold-db-2 postgresql".gold.project p
JOIN "gold-db-2 postgresql".gold.study s ON p.master_study_id = s.study_id
WHERE p.is_public = 'Yes'
  AND s.ecosystem IS NOT NULL
GROUP BY s.ecosystem, s.ecosystem_type
ORDER BY project_count DESC
LIMIT 20
```

---

## Pattern 2: Project → SRA Experiments

**Problem:** Column is `library_instrument`, NOT `platform`.

```sql
SELECT
    p.gold_id,
    p.project_name,
    s.sra_experiment_id,
    s.library_instrument,
    s.library_strategy,
    s.library_source
FROM "gold-db-2 postgresql".gold.project p
JOIN "gold-db-2 postgresql".gold.sra_experiment_v2 s ON p.project_id = s.project_id
WHERE p.is_public = 'Yes'
LIMIT 50
```

### Filter by Sequencing Technology
```sql
WHERE s.library_instrument LIKE '%Illumina%'
-- or
WHERE s.library_strategy = 'WGS'
```

---

## Pattern 3: IMG Taxon → GOLD Analysis Project

Link IMG genomes to their GOLD analysis projects:

```sql
SELECT
    t.taxon_oid,
    t.organism_name,
    t.analysis_project_id,
    t.gold_id
FROM "gold-db-2 postgresql".gold.img_taxon t
WHERE t.analysis_project_id IS NOT NULL
LIMIT 50
```

### Full Chain: IMG → GOLD Project → Study
```sql
SELECT
    i.taxon_oid,
    i.organism_name,
    p.project_name,
    s.ecosystem,
    s.ecosystem_type
FROM "gold-db-2 postgresql".gold.img_taxon i
JOIN "gold-db-2 postgresql".gold.project p ON i.analysis_project_id = p.gold_id
JOIN "gold-db-2 postgresql".gold.study s ON p.master_study_id = s.study_id
WHERE s.ecosystem IS NOT NULL
LIMIT 50
```

---

## Pattern 4: RNAseq Experiments

**Problem:** Columns are `exp_oid` and `exp_name`, NOT `experiment_id`/`experiment_name`.

```sql
SELECT
    exp_oid,
    exp_name,
    description,
    taxon
FROM "img-db-2 postgresql".img_rnaseq.rnaseq_experiment
LIMIT 50
```

### Link RNAseq to Taxon
```sql
SELECT
    r.exp_oid,
    r.exp_name,
    t.taxon_display_name
FROM "img-db-2 postgresql".img_rnaseq.rnaseq_experiment r
JOIN "img-db-2 postgresql".img_core_v400.taxon t ON r.taxon = t.taxon_oid
LIMIT 50
```

---

## Pattern 5: Biosynthetic Gene Clusters

```sql
-- Get cluster types
SELECT bcg_type, description
FROM "img-db-2 postgresql".abc.bcg_type
LIMIT 100

-- Note: Also available at "img-db-1 mysql".abc.bcg_type
```

---

## Common Filter Patterns

### Public Data Only
```sql
WHERE p.is_public = 'Yes'
-- or for IMG
WHERE t.is_public = 'Yes'
```

### By Domain
```sql
WHERE t.domain = 'Bacteria'
WHERE t.domain = 'Archaea'
WHERE t.domain = 'Eukaryota'
```

### By Sequencing Status
```sql
WHERE p.seq_status = 'Complete'
WHERE p.seq_status = 'Permanent Draft'
```

---

## Schema Quick Reference

| Source | Schema | Key Tables |
|--------|--------|------------|
| GOLD | `"gold-db-2 postgresql".gold` | project, study, organism_v2, biosample, ncbi_assembly |
| IMG Core | `"img-db-2 postgresql".img_core_v400` | taxon, gene |
| IMG RNAseq | `"img-db-2 postgresql".img_rnaseq` | rnaseq_experiment |
| IMG ABC | `"img-db-2 postgresql".abc` | bcg_type |
| IMG Gold Link | `"gold-db-2 postgresql".gold` | img_taxon |
