# Metagenome Metadata: Ecosystem & Habitat Information

## Overview

Metagenomes are analyzed samples from specific ecosystems and habitats. Understanding the environmental origin is critical for:
- Contextualizing microbial communities
- Comparing genomes across similar ecosystems
- Understanding which organisms belong where
- Identifying ecological patterns and biogeographic diversity

This guide shows how to access ecosystem metadata for metagenomes by linking IMG genomes to GOLD Analysis Projects, which contain precise sample-specific ecosystem classifications.

---

## Quick Start: Link IMG Metagenome to GOLD Analysis Project Ecosystem Info

```sql
-- Get a metagenome with its ecosystem information
SELECT
  t.taxon_oid,
  t.taxon_display_name,
  t.analysis_project_id,
  ap.ecosystem,
  ap.ecosystem_category,
  ap.ecosystem_type,
  ap.ecosystem_subtype,
  ap.specific_ecosystem
FROM "img-db-2 postgresql".img_core_v400.taxon t
INNER JOIN "gold-db-2 postgresql".gold.analysis_project ap
  ON t.analysis_project_id = ap.gold_id
WHERE t.genome_type = 'metagenome'
  AND t.is_public = 'Yes'
  AND ap.ecosystem IS NOT NULL
LIMIT 100
```

---

## Key Insight: Analysis Project vs Study

**Why Analysis Project, not Study?**

- **GOLD Study**: Contains multiple samples from potentially different ecosystems/locations
  - One study = multiple biosamples with different ecosystem metadata
  - Study-level metadata is too coarse for individual metagenome comparison

- **GOLD Analysis Project**: One-to-one with IMG metagenome
  - Each analysis project = one analyzed sample = one ecosystem classification
  - Sample-specific, precise ecosystem metadata
  - 99.8% coverage for IMG metagenomes

**Therefore: Use GOLD Analysis Project ecosystem fields for accurate, sample-specific metadata**

---

## Linking IMG to GOLD Analysis Project

### The Linkage

```
IMG Taxon (metagenome)
    ↓
    taxon.analysis_project_id = "Ga0606224"
    ↓
GOLD Analysis Project
    WHERE analysis_project.gold_id = "Ga0606224"
    ↓
Ecosystem metadata fields available
```

### Data Availability

| Link Availability | Count | Coverage |
|---|---|---|
| IMG metagenomes | 73,984 | 100% |
| With analysis_project linked | 73,982 | 100% |
| With ecosystem data | 73,848 | 99.8% |
| With ecosystem_category | 73,844 | 99.8% |

All public IMG metagenomes link to GOLD analysis projects with ecosystem information.

---

## Ecosystem Metadata in GOLD Analysis Project

### Available Fields

GOLD analysis projects provide a hierarchical ecosystem classification:

| Field | Description | Example |
|-------|---|---|
| **ecosystem** | Top-level ecosystem classification | Environmental, Host-associated, Engineered |
| **ecosystem_category** | Refined ecosystem category | Terrestrial, Aquatic, Mammals: Human, Bioreactor |
| **ecosystem_type** | Specific environment type | Soil, Marine, Freshwater, Digestive system |
| **ecosystem_subtype** | Further refinement of type | Lake, River, Coastal, Gut, Large intestine |
| **specific_ecosystem** | Most detailed classification | Fecal, Agricultural land, etc. |

### Ecosystem Distribution

Major ecosystem categories for metagenomes:

| Ecosystem | Subtypes | Examples |
|-----------|----------|----------|
| **Environmental** | Terrestrial, Aquatic | Soil, Ocean, Lake, River, Wetland, Cave |
| **Host-associated** | Mammals, Arthropods, Aquatic invertebrates | Human gut, Insect gut, Sponge, Coral |
| **Engineered** | Bioreactor, Wastewater, Lab systems | Biogas reactors, Activated sludge, Culture media |

---

## Query Examples

### 1. Find Metagenomes from Specific Ecosystem Type

```sql
-- Get all metagenomes from soil environments
SELECT
  t.taxon_oid,
  t.taxon_display_name,
  ap.ecosystem,
  ap.ecosystem_type,
  ap.ecosystem_subtype
FROM "img-db-2 postgresql".img_core_v400.taxon t
INNER JOIN "gold-db-2 postgresql".gold.analysis_project ap
  ON t.analysis_project_id = ap.gold_id
WHERE t.genome_type = 'metagenome'
  AND t.is_public = 'Yes'
  AND ap.ecosystem_type = 'Soil'
ORDER BY ap.ecosystem_subtype
LIMIT 100
```

### 2. Find Metagenomes from Multiple Ecosystem Types

```sql
-- Get marine and freshwater metagenomes
SELECT
  t.taxon_oid,
  t.taxon_display_name,
  ap.ecosystem_type,
  ap.ecosystem_subtype
FROM "img-db-2 postgresql".img_core_v400.taxon t
INNER JOIN "gold-db-2 postgresql".gold.analysis_project ap
  ON t.analysis_project_id = ap.gold_id
WHERE t.genome_type = 'metagenome'
  AND t.is_public = 'Yes'
  AND ap.ecosystem_type IN ('Marine', 'Freshwater')
LIMIT 100
```

### 3. Find Human Microbiome Metagenomes

```sql
-- Get human digestive system samples
SELECT
  t.taxon_oid,
  t.taxon_display_name,
  ap.ecosystem_category,
  ap.ecosystem_type,
  ap.ecosystem_subtype,
  ap.specific_ecosystem
FROM "img-db-2 postgresql".img_core_v400.taxon t
INNER JOIN "gold-db-2 postgresql".gold.analysis_project ap
  ON t.analysis_project_id = ap.gold_id
WHERE t.genome_type = 'metagenome'
  AND t.is_public = 'Yes'
  AND ap.ecosystem_category = 'Mammals: Human'
  AND ap.ecosystem_type = 'Digestive system'
LIMIT 100
```

### 4. Group Metagenomes by Ecosystem Type

```sql
-- Count metagenomes by ecosystem classification
SELECT
  ap.ecosystem,
  ap.ecosystem_category,
  ap.ecosystem_type,
  ap.ecosystem_subtype,
  COUNT(DISTINCT t.taxon_oid) metagenome_count
FROM "img-db-2 postgresql".img_core_v400.taxon t
INNER JOIN "gold-db-2 postgresql".gold.analysis_project ap
  ON t.analysis_project_id = ap.gold_id
WHERE t.genome_type = 'metagenome'
  AND t.is_public = 'Yes'
  AND ap.ecosystem IS NOT NULL
GROUP BY ap.ecosystem, ap.ecosystem_category, ap.ecosystem_type, ap.ecosystem_subtype
ORDER BY metagenome_count DESC
LIMIT 100
```

### 5. Combine Ecosystem with Quality Metrics

```sql
-- Metagenomes with ecosystem + assembly quality metrics
SELECT
  t.taxon_oid,
  t.taxon_display_name,
  ap.ecosystem_type,
  ap.ecosystem_subtype,
  a.est_num_of_genomes,
  a.num_filtered_reads,
  a.avg_cov_assembled_seq
FROM "img-db-2 postgresql".img_core_v400.taxon t
INNER JOIN "gold-db-2 postgresql".gold.analysis_project ap
  ON t.analysis_project_id = ap.gold_id
INNER JOIN "img-db-2 postgresql".img_core_v400.taxon_assembly_stats a
  ON t.taxon_oid = a.taxon_oid
WHERE t.genome_type = 'metagenome'
  AND t.is_public = 'Yes'
  AND ap.ecosystem = 'Environmental'
ORDER BY a.est_num_of_genomes DESC
LIMIT 100
```

### 6. Filter by Ecosystem and Sequencing Type

```sql
-- Soil metagenomes sequenced with Illumina (short-read)
SELECT
  t.taxon_oid,
  t.taxon_display_name,
  ap.ecosystem_subtype,
  p.library_method
FROM "img-db-2 postgresql".img_core_v400.taxon t
INNER JOIN "gold-db-2 postgresql".gold.analysis_project ap
  ON t.analysis_project_id = ap.gold_id
LEFT JOIN "gold-db-2 postgresql".gold.project p
  ON t.sequencing_gold_id = p.project_id
WHERE t.genome_type = 'metagenome'
  AND t.is_public = 'Yes'
  AND ap.ecosystem_type = 'Soil'
  AND p.library_method LIKE '%Illumina%'
LIMIT 100
```

---

## Ecosystem Field Reference

### Environmental Ecosystems

#### Terrestrial
- **Soil** (most common)
  - Soil subtypes: Temperate forest, Grassland, Desert, Arctic, etc.
  - Specific: Agricultural land, Forest, Grassland, etc.
- **Other terrestrial**
  - Cave systems
  - Subsurface/Geothermal environments

#### Aquatic
- **Marine**
  - Subtypes: Oceanic, Coastal, Pelagic zone, Benthic zone, Hydrothermal vents, Sediments
- **Freshwater**
  - Subtypes: Lake, River, Stream, Wetland, Groundwater, Spring

### Host-associated Ecosystems

#### Mammals
- **Mammals: Human** (most abundant)
  - Types: Digestive system, Respiratory tract, Oral cavity, Skin, Urinary tract, Vaginal, Other
  - Subtypes: Large intestine, Small intestine, Esophagus, Esophagus, Gut, Mouth, Throat, Lungs, etc.
  - Specific: Fecal (most common)
- **Other mammals**
  - Ruminants (cow, sheep), Primates, Rodents, Marine mammals

#### Arthropods
- **Arthropoda: Insects**
  - Termites, Cockroaches, Beetles, Mosquitoes, Flies, etc.
- **Arachnida**
  - Ticks, Mites

#### Aquatic invertebrates
- **Porifera** (Sponges)
- **Cnidaria** (Corals, Sea anemones)
- **Mollusca** (Clams, Mussels)
- Others (Sea squirts, etc.)

### Engineered Ecosystems

- **Bioreactor**
  - Subtypes: Anaerobic, Aerobic, Fermentation, etc.
- **Wastewater**
  - Subtypes: Activated sludge, Biofiltration, Biofilm reactors
- **Lab culture**
  - Subtypes: Culture media, Synthetic communities, Defined enrichments

---

## Building Comparative Datasets

### Strategy: Filter by Ecosystem Type

```sql
-- Build homogeneous dataset: all soil metagenomes with quality metrics
SELECT
  t.taxon_oid,
  t.taxon_display_name,
  ap.ecosystem_subtype,
  ap.specific_ecosystem,
  a.est_num_of_genomes,
  a.num_filtered_reads,
  p.library_method
FROM "img-db-2 postgresql".img_core_v400.taxon t
INNER JOIN "gold-db-2 postgresql".gold.analysis_project ap
  ON t.analysis_project_id = ap.gold_id
INNER JOIN "img-db-2 postgresql".img_core_v400.taxon_assembly_stats a
  ON t.taxon_oid = a.taxon_oid
LEFT JOIN "gold-db-2 postgresql".gold.project p
  ON t.sequencing_gold_id = p.project_id
WHERE t.genome_type = 'metagenome'
  AND t.is_public = 'Yes'
  AND t.analysis_project_type = 'Metagenome Analysis'  -- Standard metagenomes only
  AND ap.ecosystem_type = 'Soil'
  AND ap.ecosystem_subtype IS NOT NULL
  AND a.est_num_of_genomes > 5
  AND a.est_num_of_genomes < 100
  AND p.library_method LIKE '%Illumina%'
ORDER BY ap.ecosystem_subtype, a.est_num_of_genomes
LIMIT 200
```

**This ensures:**
- ✓ All metagenomes from same ecosystem type (Soil)
- ✓ Standard metagenomes only (no enrichment)
- ✓ Moderate complexity (5-100 genomes)
- ✓ With quality metrics
- ✓ Consistent sequencing platform
- ✓ Grouped by ecosystem subtype for further organization

---

## Additional Analysis Project Fields

Beyond ecosystem classification, analysis projects contain:

| Field | Description | Example |
|---|---|---|
| **sequencing_depth** | Sequencing/read depth metric | Integer or float |
| **gene_count** | Number of predicted genes | 172,313 |
| **contig_count** | Number of contiguous sequences | 132,046 |
| **scaffold_count** | Number of scaffolds | Higher = more fragmented |
| **completion** | Assembly completion status | "Complete", "In progress", etc. |
| **completeness_percentage** | Estimated genome completeness | 75.5 |
| **contamination_percentage** | Estimated contamination | 2.3 |
| **binning_method** | Method used for binning (if MAGs) | Text description |

---

## Troubleshooting

### Q: Why doesn't my query return results?

**Check:**
1. Use `ap.ecosystem IS NOT NULL` - not all projects have ecosystem data (but 99.8% do)
2. Verify ecosystem value spelling (case-sensitive in GOLD)
3. Confirm `analysis_project_id` is not NULL in IMG
4. Use exact string match or `LIKE '%...%'` for partial matches

### Q: How do I get more detailed environmental metadata?

Use these fields from analysis_project:
- `ecosystem_subtype` - More specific environment type
- `specific_ecosystem` - Most detailed classification available
- `sequencing_depth` - Read depth/coverage metric

### Q: Can I also get information from the analysis project's associated study?

Yes, but studies contain multiple samples with different ecosystems:

```sql
-- Get study name and metadata alongside ecosystem
SELECT
  t.taxon_oid,
  t.taxon_display_name,
  ap.ecosystem_type,
  s.gold_study_name,
  s.description
FROM "img-db-2 postgresql".img_core_v400.taxon t
INNER JOIN "gold-db-2 postgresql".gold.analysis_project ap
  ON t.analysis_project_id = ap.gold_id
LEFT JOIN "gold-db-2 postgresql".gold.study s
  ON ap.study_id = s.study_id
WHERE t.genome_type = 'metagenome'
  AND t.is_public = 'Yes'
LIMIT 100
```

**Important:** Each metagenome has its own ecosystem (from analysis_project), but the study name/description provides project-level context (may include multiple ecosystems).

### Q: How do I find all metagenomes from a specific research project or study?

```sql
-- Find all metagenomes from a study containing "amazon" in the name
SELECT
  t.taxon_oid,
  t.taxon_display_name,
  ap.ecosystem_type,
  s.gold_study_name
FROM "img-db-2 postgresql".img_core_v400.taxon t
INNER JOIN "gold-db-2 postgresql".gold.analysis_project ap
  ON t.analysis_project_id = ap.gold_id
LEFT JOIN "gold-db-2 postgresql".gold.study s
  ON ap.study_id = s.study_id
WHERE t.genome_type = 'metagenome'
  AND t.is_public = 'Yes'
  AND LOWER(s.gold_study_name) LIKE '%amazon%'
LIMIT 50
```

---

## Complete Workflow Example

```sql
-- Build a comparative metagenome dataset:
-- Human gut microbiomes with consistent sequencing and quality
WITH gut_metagenomes AS (
  SELECT
    t.taxon_oid,
    t.taxon_display_name,
    t.analysis_project_id,
    ap.ecosystem_category,
    ap.ecosystem_subtype,
    ap.specific_ecosystem,
    a.est_num_of_genomes,
    a.num_filtered_reads,
    a.avg_cov_assembled_seq,
    p.library_method
  FROM "img-db-2 postgresql".img_core_v400.taxon t
  INNER JOIN "gold-db-2 postgresql".gold.analysis_project ap
    ON t.analysis_project_id = ap.gold_id
  INNER JOIN "img-db-2 postgresql".img_core_v400.taxon_assembly_stats a
    ON t.taxon_oid = a.taxon_oid
  LEFT JOIN "gold-db-2 postgresql".gold.project p
    ON t.sequencing_gold_id = p.project_id
  WHERE t.genome_type = 'metagenome'
    AND t.is_public = 'Yes'
    AND t.analysis_project_type = 'Metagenome Analysis'
    AND ap.ecosystem_category = 'Mammals: Human'
    AND ap.ecosystem_type = 'Digestive system'
    AND ap.ecosystem_subtype = 'Large intestine'
    AND ap.specific_ecosystem = 'Fecal'
    AND a.est_num_of_genomes >= 10
    AND a.est_num_of_genomes <= 200
    AND p.library_method LIKE '%Illumina%'
)
SELECT *
FROM gut_metagenomes
ORDER BY est_num_of_genomes, num_filtered_reads DESC
LIMIT 100
```

This builds a homogeneous dataset ensuring:
- All human gut fecal samples
- Consistent ecosystem classification
- Moderate complexity
- Good assembly quality
- Consistent sequencing platform

---

## Related Documentation

- [IMG_data_types.md](IMG_data_types.md) - Overview of IMG genome types
- [metagenome_comparability.md](metagenome_comparability.md) - Quality metrics and comparability
- [data-catalog.md](data-catalog.md) - Complete table schemas
- [sql-quick-reference.md](sql-quick-reference.md) - SQL syntax for Dremio
