# Metagenome Comparability Guide

## Critical Overview

Metagenomes from different sources, sequencing strategies, and protocols **may not be directly comparable** in the same analysis. This guide helps you identify metagenome characteristics that affect comparability and build homogeneous datasets for robust comparative analysis.

### Key Comparability Factors:
1. **Sequencing Type** - DNA vs RNA-based (metatranscriptomes)
2. **RNA Protocol** - RNA handling method (polyA selection, ribo-depletion, total RNA)
3. **Enrichment Method** - Sample preparation (standard, sorted cells, enriched, SIP-labeled)
4. **Complexity Level** - Community structure (simple vs complex)

---

## 1. DNA vs RNA: Metagenomes vs Metatranscriptomes

### Metagenome (DNA-based)
- Captures **genomic potential** of microbial communities
- Represents entire organisms present, regardless of activity
- **Can compare**: All DNA metagenomes with each other (subject to other criteria)

**GOLD sequencing_strategy:** `Metagenome`

### Metatranscriptome (RNA-based)
- Captures **active gene expression** in the community
- Only represents genes actively transcribed at sampling time
- **Cannot compare directly with**: DNA metagenomes (different biology)
- **Can compare**: Metatranscriptomes with each other (with protocol caveats)

**GOLD sequencing_strategy:** `Metatranscriptome`, `Metatranscriptome - Co-Culture`

### Query Pattern: Filter by Sequencing Type

```sql
-- Get all DNA metagenomes
SELECT taxon_oid, taxon_display_name, analysis_project_type
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE analysis_project_type IN (
    'Metagenome Analysis',
    'Metagenome-Assembled Genome',
    'Metagenome - Single Particle Sort',
    'Metagenome - Cell Enrichment',
    'Metagenome - Low Complexity',
    'Metagenome - SIP'
  )
  AND is_public = 'Yes'
LIMIT 100

-- Get all RNA metagenomes (metatranscriptomes)
SELECT taxon_oid, taxon_display_name
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE analysis_project_type = 'Metatranscriptome Analysis'
  AND is_public = 'Yes'
LIMIT 100
```

### Linking to GOLD for Metadata

```sql
-- Get GOLD project metadata for a metagenome
SELECT
  p.project_id,
  p.project_name,
  p.sequencing_strategy,
  p.sequencing_strategy_full,
  p.library_method
FROM "gold-db-2 postgresql".gold.project p
WHERE p.sequencing_strategy_full LIKE '%Metagenome%'
  AND p.is_public = 'Yes'
LIMIT 20
```

---

## 2. RNA Protocols: Critical for Metatranscriptome Comparability

### RNA Handling Methods (by prevalence)

| Protocol | Count | Description | Comparability | Best For |
|----------|-------|-------------|----------------|----------|
| **rRNA Depletion** | ~6,000 | Removes ribosomal RNA; captures all transcripts | Comparable with other rRNA depletion | Bacteria, all organisms |
| **polyA Selection** | ~2,600 | Selects mRNA (polyadenylated); removes rRNA | **NOT comparable** with ribo-depletion | Eukaryotes only |
| **Total RNA** | 651 | Unbiased; keeps rRNA and mRNA | Comparable with other total RNA | Unbiased profiling |
| **Mixed/Other** | Various | May use multiple protocols | **Use with caution** | Custom studies |

### Why RNA Protocols Matter

```
rRNA Depletion captures:
  ✓ Bacterial transcripts (all bacteria lack polyA)
  ✓ rRNA (abundant in cells)
  ✓ Eukaryotic mRNA
  ✓ ncRNAs

polyA Selection captures:
  ✓ Eukaryotic mRNA only (has polyA tail)
  ✗ Cannot detect bacterial genes
  ✗ Misses eukaryotic ncRNAs

Total RNA captures:
  ✓ All RNA molecules
  ✗ Dominated by rRNA (>90% in some samples)
```

### GOLD Library Method Field

Common metatranscriptome library protocols:

```
Illumina Low Input RNASeq w/rRNA Depletion, Plates       2,744
Illumina Low Input RNASeq w/rRNA Depletion, Tubes        2,611
Illumina RNASeq w/PolyA Selection, Plates                1,927
Illumina Low Input RNASeq w/PolyA Selection, Plates      1,600
Illumina Ultra-Low Input RNASeq w/rRNA Depletion        1,375
Illumina Ultra-Low Input RNASeq w/out PolyA Selection,
  w/out rRNA Depletion (Total RNA)                        651
```

### Query Pattern: Get Metatranscriptome Protocol Details

```sql
-- Get GOLD projects with metatranscriptome protocols
SELECT
  p.project_id,
  p.project_name,
  p.library_method,
  COUNT(DISTINCT p.project_id) as project_count
FROM "gold-db-2 postgresql".gold.project p
WHERE p.sequencing_strategy_full = 'Metatranscriptome'
  AND p.is_public = 'Yes'
GROUP BY p.project_id, p.project_name, p.library_method
ORDER BY project_count DESC
LIMIT 50
```

### Warning: Protocol-Based Filtering for Metatranscriptomes

```sql
-- Get ONLY rRNA-depleted metatranscriptomes (comparable)
SELECT p.project_id, p.project_name, p.library_method
FROM "gold-db-2 postgresql".gold.project p
WHERE p.sequencing_strategy_full = 'Metatranscriptome'
  AND p.library_method LIKE '%rRNA Depletion%'
  AND p.is_public = 'Yes'
LIMIT 50

-- Get ONLY polyA-selected metatranscriptomes (comparable)
SELECT p.project_id, p.project_name, p.library_method
FROM "gold-db-2 postgresql".gold.project p
WHERE p.sequencing_strategy_full = 'Metatranscriptome'
  AND p.library_method LIKE '%PolyA%'
  AND p.is_public = 'Yes'
LIMIT 50

-- WARNING: Do not mix rRNA depletion + polyA selection
-- Different gene sets will be captured!
```

---

## 3. Enrichment & Sampling Methods: Metagenome Types

### Overview of Metagenome Analysis Project Types

| Type | Count | Sampling Method | Comparability | Community Type |
|------|-------|-----------------|---|---|
| **Metagenome (standard)** | 49,939 | Whole community, no selection | ✓ High | Complex |
| **Viral Metagenome** | 1,266+ | Size-fractionated viruses (<0.2 μm) | ✗ Limited | Viral |
| **Metagenome - Single Particle Sort (SPS)** | 13,098 | Flow-sorted cells | ✗ Limited | Simplified |
| **Metagenome - Low Complexity** | 7,221 | Simple, defined communities | ✗ Limited | Simple |
| **Metagenome - Cell Enrichment** | 4,850 | Targeted enrichment | ✗ Limited | Simplified |
| **Metagenome - SIP** | 1,374 | Isotope-labeled organisms | ✗ Limited | Functional |
| **Metagenome - Co-Culture** | 31 | Defined mixed cultures | ✗ Limited | Minimal |

### Standard Metagenomes (Best for Comparative Studies)

**Description:** Whole environmental samples with no enrichment or sorting
- Direct reflection of community composition
- Unbiased sampling

**GOLD sequencing_strategy_full:** `Metagenome`
**IMG analysis_project_type:** `Metagenome Analysis`

**✓ Comparable with:** Other standard metagenomes (same environment or similar habitats)

```sql
-- Get standard metagenomes for comparative analysis
SELECT taxon_oid, taxon_display_name, analysis_project_type
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE analysis_project_type = 'Metagenome Analysis'
  AND is_public = 'Yes'
LIMIT 100
```

### Viral Metagenomes (Viromes)

**Description:** Size-fractionated metagenomic samples enriching for viruses
- Samples typically filtered through 0.2 or 0.22 micron filters (viral size fraction)
- Captures viral particles and small nucleic acids
- Represents viral community structure and genetic diversity
- Often complementary to microbial metagenomes from same environment

**Key Terms:** Viral metagenome, virome, metavirome, viral community

**IMG Identifiers:**
- `analysis_product_name` contains: "Metagenome Viral Standard Draft" (~792), "Viral Enrichment" (~100), "Single Viral Sort, Unscreened" (~374)
- Search `taxon_display_name` for keywords: "viral", "virome", "phage"

**Characteristics:**
- Often paired with microbial metagenomes from same sample
- Different assembly and recovery challenges than microbial genomes (smaller, more diverse)
- May include bacteriophages, archaeal viruses, and eukaryotic viruses

**✓ Can compare with:**
- Other viral metagenomes from similar environments
- Viral metagenomes using same size-fractionation method (<0.2 μm)
- **Microbial metagenomes from same sample** (when goal is to evaluate whether different viruses are recovered using viral size-fraction approach vs standard metagenome)

**✗ NOT comparable with:**
- Filtered metagenomes (where viruses were removed by filtration)

**⚠ Important Distinction:** Viral and microbial metagenomes from the **same sample** represent complementary but distinct communities. They capture different organisms (size-selected viruses vs. bacteria/archaea) and can be compared to answer biological questions like "what viruses are co-occurring with microbial community X" or "does viral size-fractionation recover different viral diversity than standard metagenome sequencing". However, do not combine them in abundance/diversity analyses without careful normalization and clear documentation of their complementary nature.

```sql
-- Get all viral metagenomes
SELECT taxon_oid, taxon_display_name, analysis_product_name
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE (analysis_product_name LIKE '%Viral%'
   OR LOWER(taxon_display_name) LIKE '%viral%'
   OR LOWER(taxon_display_name) LIKE '%virome%')
  AND is_public = 'Yes'
LIMIT 100

-- Get only viral standard draft metagenomes
SELECT taxon_oid, taxon_display_name
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE analysis_product_name = 'Metagenome Viral Standard Draft'
  AND is_public = 'Yes'
LIMIT 100

-- Get viral enrichment samples
SELECT taxon_oid, taxon_display_name
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE analysis_product_name = 'Viral Enrichment'
  AND is_public = 'Yes'
LIMIT 100
```

### Single Particle Sort (SPS) - RIBOSOMAL SORTED

**Description:** Cells sorted by flow cytometry before sequencing
- Captures single ribosomal particles or cells
- Reduces community complexity artificially
- Biased toward sorted population

**GOLD sequencing_strategy_full:** `Metagenome - Single Particle Sort`
**IMG analysis_project_type:** `Metagenome - Single Particle Sort`

**✗ NOT comparable with:** Standard metagenomes or other enrichment types

**⚠ Warning:** Community composition will be skewed toward sorted population; abundances not representative of original community

```sql
-- Get SPS metagenomes (use with caution in comparative analysis)
SELECT taxon_oid, taxon_display_name
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE analysis_project_type = 'Metagenome - Single Particle Sort'
  AND is_public = 'Yes'
LIMIT 100
```

### Low Complexity Metagenomes

**Description:** Simple, well-defined microbial communities
- Examples: biofilms, pure co-cultures, bioreactors, lab-controlled enrichments
- Often representing specific ecological niches or functionally enriched communities
- Better assembled due to lower diversity

**GOLD sequencing_strategy_full:** `Metagenome - Low Complexity`
**IMG analysis_project_type:** `Metagenome - Low Complexity`

**✗ NOT comparable with:** Complex environmental metagenomes

**✓ Can compare with:** Other low-complexity metagenomes from similar systems

```sql
-- Get low-complexity metagenomes
SELECT taxon_oid, taxon_display_name
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE analysis_project_type = 'Metagenome - Low Complexity'
  AND is_public = 'Yes'
LIMIT 100
```

### Cell Enrichment Metagenomes

**Description:** Communities enriched for specific populations through culturing or immunomagnetic capture
- Captures specific microbial groups
- Biased toward enriched population
- Often used for mining specific metabolisms

**GOLD sequencing_strategy_full:** `Metagenome - Cell Enrichment`
**IMG analysis_project_type:** `Metagenome - Cell Enrichment`

**✗ NOT comparable with:** Unenriched environmental metagenomes

**✓ Can compare with:** Other enrichments targeting same population/metabolism

```sql
-- Get cell-enriched metagenomes
SELECT taxon_oid, taxon_display_name
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE analysis_project_type = 'Metagenome - Cell Enrichment'
  AND is_public = 'Yes'
LIMIT 100
```

### SIP (Stable Isotope Probing) Metagenomes

**Description:** Metagenomes from organisms that incorporated specific isotope labels
- Identifies organisms actively utilizing labeled substrate
- Functional approach: captures only active populations
- Often paired with parent samples

**GOLD sequencing_strategy_full:** `Metagenome - SIP`, `Metagenome - SIP Parent`
**IMG analysis_project_type:** `Metagenome - SIP`

**✗ NOT comparable with:** Non-labeled metagenomes

**✓ Can compare with:** Other SIP metagenomes using same substrate/label

**Note:** Look for related parent and labeled datasets

```sql
-- Get SIP metagenomes with parents
SELECT
  t.taxon_oid,
  t.taxon_display_name,
  t.analysis_project_type,
  t.study_gold_id
FROM "img-db-2 postgresql".img_core_v400.taxon t
WHERE t.analysis_project_type LIKE '%SIP%'
  AND t.is_public = 'Yes'
ORDER BY t.study_gold_id
LIMIT 100

-- Find parent/labeled pairs (same study)
SELECT
  study_gold_id,
  analysis_project_type,
  COUNT(*) cnt
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE analysis_project_type LIKE '%SIP%'
GROUP BY study_gold_id, analysis_project_type
```

---

## 4. Decision Tree for Comparative Analysis

### Question 1: DNA vs RNA?

```
Do you want to study:
├─ Active gene expression (RNA)?
│  └─ Use Metatranscriptomes (Metatranscriptome Analysis)
│     └─ Filter by library_method (polyA, ribo-depletion, or total RNA)
│
└─ Genomic potential (DNA)?
   └─ Use DNA Metagenomes
      └─ Question 2...
```

### Question 2: Enrichment/Bias Acceptable?

```
Do you want:
├─ Unbiased, whole community?
│  └─ Use Standard Metagenomes ONLY
│
└─ Specific populations only?
   ├─ Sorted particles?  → Single Particle Sort
   ├─ Enriched culture?  → Cell Enrichment
   ├─ Isotope tracking?  → SIP
   └─ Simple community?  → Low Complexity
      └─ Question 3...
```

### Question 3: Can You Filter to Homogeneous Set?

```
For non-standard metagenomes:
├─ Can you group by enrichment type?
│  └─ Compare only SPS with SPS
│  └─ Compare only enrichments with enrichments
│
└─ All mixed?
   └─ ⚠ NOT RECOMMENDED for comparative analysis
   └─ Document differences as confounding variable
```

---

## 5. Practical Query Examples for Comparable Datasets

### Example 1: Build a Homogeneous DNA Metagenome Dataset

```sql
-- Standard metagenomes only (unbiased, comparable)
SELECT
  taxon_oid,
  taxon_display_name,
  analysis_project_type,
  study_gold_id
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE analysis_project_type = 'Metagenome Analysis'
  AND is_public = 'Yes'
ORDER BY study_gold_id
LIMIT 100
```

### Example 2: Build a Metatranscriptome Dataset (rRNA-Depleted Only)

```sql
-- Step 1: Identify rRNA-depleted metatranscriptome GOLD projects
WITH rna_depleted_projects AS (
  SELECT DISTINCT project_id
  FROM "gold-db-2 postgresql".gold.project
  WHERE sequencing_strategy_full = 'Metatranscriptome'
    AND library_method LIKE '%rRNA Depletion%'
    AND is_public = 'Yes'
)
-- Step 2: Get IMG genomes from those projects
SELECT
  taxon_oid,
  taxon_display_name,
  analysis_project_type,
  sequencing_gold_id
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE analysis_project_type = 'Metatranscriptome Analysis'
  AND is_public = 'Yes'
LIMIT 100
```

### Example 3: Get LOW Complexity Metagenomes Only

```sql
-- Low complexity communities (e.g., biofilms, bioreactors)
SELECT
  taxon_oid,
  taxon_display_name,
  analysis_project_type
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE analysis_project_type = 'Metagenome - Low Complexity'
  AND is_public = 'Yes'
LIMIT 100
```

### Example 4: Build SIP Dataset with Parent Controls

```sql
-- Find SIP studies with both parent and labeled
SELECT
  study_gold_id,
  COUNT(CASE WHEN analysis_project_type LIKE '%SIP Parent%' THEN 1 END) as parent_count,
  COUNT(CASE WHEN analysis_project_type = 'Metagenome - SIP' THEN 1 END) as labeled_count
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE analysis_project_type LIKE '%SIP%'
  AND is_public = 'Yes'
GROUP BY study_gold_id
HAVING COUNT(*) >= 2  -- Has both parent and labeled
ORDER BY study_gold_id
LIMIT 50
```

---

## 6. Comparability Matrix

### Can These Be Mixed in One Analysis?

|  | Standard DNA | Viral | Metatranscriptome | SPS | Enriched | Low-Complexity | SIP |
|---|---|---|---|---|---|---|---|
| **Standard DNA** | ✓ Yes | ⚠ Limited* | ✗ No | ⚠ Limited | ⚠ Limited | ⚠ Limited | ✗ No |
| **Viral** | ⚠ Limited* | ✓ Yes | ✗ No | ✗ No | ✗ No | ✗ No | ✗ No |
| **Metatranscriptome** | ✗ No | ✗ No | ✓ Yes* | ✗ No | ✗ No | ✗ No | ✗ No |
| **SPS** | ⚠ Limited | ✗ No | ✗ No | ✓ Yes | ⚠ Limited | ⚠ Limited | ✗ No |
| **Enriched** | ⚠ Limited | ✗ No | ✗ No | ⚠ Limited | ✓ Yes | ⚠ Limited | ✗ No |
| **Low-Complexity** | ⚠ Limited | ✗ No | ✗ No | ⚠ Limited | ⚠ Limited | ✓ Yes | ✗ No |
| **SIP** | ✗ No | ✗ No | ✗ No | ✗ No | ✗ No | ✗ No | ✓ Yes |

**Legend:**
- ✓ Yes = Directly comparable
- ⚠ Limited = Can mix **only with careful documentation** of differences as confounding variables
- ✗ No = **Do not mix** in same analysis

**Key Notes:**
- **\* Viral vs Standard DNA:** Can be compared when from **same sample** to evaluate recovery of different viruses via complementary approaches (size-fractionation vs standard metagenome). Do not mix in abundance/diversity analysis without normalization and careful documentation.
- **\* Metatranscriptomes:** Only comparable if same RNA protocol (rRNA depletion with rRNA depletion, polyA with polyA, etc.)

---

## 7. Metagenome Quality & Complexity Criteria

### Critical Data-Driven Metrics for Comparative Analysis

Before comparing metagenomes, you should assess these four key quality and complexity criteria:

#### 1. **Type of Sequencing: Long-Read vs Short-Read**

**Why it matters:** Assembly quality, contig length, and recovery of complete genomes differ dramatically between platforms.

**GOLD Field:** `library_method`

**Platform Types:**

| Category | Platforms | Count | Characteristics | Pros | Cons |
|----------|-----------|-------|---|---|---|
| **Short-read** | Illumina (various fragments) | ~184,888 | 75-300 bp reads | High accuracy, low cost, fast | Short contigs, gaps in assembly |
| **Long-read** | PacBio, Nanopore | ~1,915 | 10-50 kb+ reads | Long contigs, fewer gaps, haplotype resolution | Higher error rates (older platforms), costlier |

**Query to identify platform:**

```sql
-- Get sequencing platform info
SELECT
  p.project_id,
  p.project_name,
  p.library_method,
  CASE WHEN p.library_method LIKE '%Illumina%' THEN 'SHORT-READ'
       WHEN p.library_method LIKE '%PacBio%' THEN 'LONG-READ'
       WHEN p.library_method LIKE '%Nanopore%' THEN 'LONG-READ'
       WHEN p.library_method LIKE '%10x%' THEN 'LONG-READ'
       ELSE 'OTHER' END AS platform_type
FROM "gold-db-2 postgresql".gold.project p
WHERE p.is_public = 'Yes'
LIMIT 100
```

**Implication for Comparative Analysis:**
- ⚠️ **Do not mix short-read and long-read metagenomes without careful normalization**
- Contiguity, N50, and genome recovery will be fundamentally different
- Document platform differences when comparing

#### 2. **Total Number of Reads Sequenced**

**Why it matters:** Higher read count = deeper coverage = better assembly quality and rare organism detection.

**GOLD Field:** `read_count` (note: sparse data - only ~0.6% of projects have this)

**Data Availability:**
- Only 3,752 out of 609,696 GOLD projects have read_count data
- When available, format varies (e.g., "125bp", numeric)

**Query to get read metrics when available:**

```sql
-- Get projects with read count information
SELECT
  p.project_id,
  p.project_name,
  p.read_count,
  p.read_size,
  p.library_method
FROM "gold-db-2 postgresql".gold.project p
WHERE p.read_count IS NOT NULL
  AND p.is_public = 'Yes'
LIMIT 50
```

**Recommended Filtering:**
- **High coverage:** >100 million reads (better for rare organisms)
- **Standard coverage:** 10-100 million reads
- **Low coverage:** <10 million reads (increased assembly gaps, missing rare taxa)

**Implication for Comparative Analysis:**
- ✓ Combine metagenomes with similar read depths
- ⚠️ Use coverage normalization if mixing high/low coverage samples
- Document read count disparities in methods

#### 3. **Read Mapping to Assembly: Coverage Information**

**Why it matters:** Percentage of reads mapped indicates assembly completeness and potential biases.

**IMG Fields:**
- `has_coverage` (Yes/No) - indicates if coverage data was calculated
- `has_per_sample_coverage` (Yes/No) - rarely populated (only 1/73,984 metagenomes)

**Coverage Data Availability in IMG Metagenomes:**
- With coverage data: 44,576 metagenomes (60.3%)
- Without coverage data: 29,408 metagenomes (39.7%)

**Query to identify metagenomes with coverage information:**

```sql
-- Get metagenomes with coverage metrics
SELECT
  t.taxon_oid,
  t.taxon_display_name,
  t.has_coverage,
  t.has_per_sample_coverage,
  t.analysis_project_type
FROM "img-db-2 postgresql".img_core_v400.taxon t
WHERE t.genome_type = 'metagenome'
  AND t.is_public = 'Yes'
  AND t.has_coverage = 'Yes'
LIMIT 100
```

**Interpreting Coverage Flags:**
- **has_coverage = 'Yes':** Coverage information was calculated during assembly
- **has_per_sample_coverage = 'Yes':** Per-sample mapping info available (very rare)
- **Absence = 'No':** Coverage data not available

**Implication for Comparative Analysis:**
- ✓ Prioritize metagenomes with `has_coverage = 'Yes'` for consistency
- ⚠️ If mixing coverage/no-coverage data, only perform analyses based on gene, contig, or genome counts, but be clear that these do not reflect relative abundance in the original sample. Never mix counts from coverage and raw counts.
- Note that some metagenomes lack coverage due to assembly method or older processing, or because they were submitted as assemblies only (i.e. no coverage information) by external users

#### 4. **Estimated Number of Genomes Recovered**

**Why it matters:** Estimated genome count indicates community complexity and stability of abundance estimates. More genomes = higher complexity and potentially more assembly artifacts; fewer genomes = simpler, more reliable assemblies.

**IMG Field:** `est_num_of_genomes` in **`taxon_assembly_stats`** table
- **Calculated from:** Single-copy marker genes (SCGs) / single-copy proteins
- **Data type:** Float (integer value, can be NULL or 0 when not calculable)

**Data Availability for Metagenomes:**
- With data: 73,176 / 73,984 metagenomes (98.9%)
- With positive value (>0): 39,368 metagenomes (53.2%)

**Distribution of Estimated Genome Counts:**
| Genome Count | Frequency | Description |
|---|---|---|
| 0 (not calculable) | 33,808 (46.2%) | Could not estimate or no organisms detected |
| 0-5 | 6,463 (8.8%) | Simple, well-defined communities |
| 5-20 | 6,198 (8.5%) | Low-moderate complexity |
| 20-100 | 13,218 (18.1%) | Moderate-to-high complexity |
| >100 | 14,409 (19.7%) | Complex environmental samples |

**Query to get estimated genome counts:**

```sql
-- Get metagenomes with estimated genome counts
SELECT
  t.taxon_oid,
  t.taxon_display_name,
  t.analysis_project_type,
  a.est_num_of_genomes,
  a.num_mapped_reads,
  a.num_filtered_reads,
  a.avg_cov_assembled_seq,
  a.est_avg_genome_size
FROM "img-db-2 postgresql".img_core_v400.taxon t
INNER JOIN "img-db-2 postgresql".img_core_v400.taxon_assembly_stats a
  ON t.taxon_oid = a.taxon_oid
WHERE t.genome_type = 'metagenome'
  AND t.is_public = 'Yes'
  AND a.est_num_of_genomes IS NOT NULL
ORDER BY a.est_num_of_genomes DESC
LIMIT 100
```

**Interpreting the Values:**
- **est_num_of_genomes = 0:** Cannot estimate (insufficient SCGs, low coverage, or no organisms)
- **est_num_of_genomes = 1-5:** Simple, pure or nearly-pure cultures; single-strain or bioreactor samples
- **est_num_of_genomes = 5-100:** Moderate complexity; defined enrichment cultures or low-diversity environments
- **est_num_of_genomes > 100:** High complexity; diverse environmental samples with many co-occurring organisms

**Implication for Comparative Analysis:**
- ✓ **Filter by estimated genome count** to ensure dataset homogeneity
- Group metagenomes: simple (<10) vs moderate (10-100) vs complex (>100)
- Simple metagenomes: cleaner assemblies, less fragmented, more reliable MAG recovery
- Complex metagenomes: more genomes present, potential for assembly artifacts, higher fragmentation
- ⚠️ Be cautious mixing simple with complex metagenomes: organism abundances will differ dramatically

---

## 8. Data Quality & Filtering Recommendations

### Recommended Filters for All Datasets

```sql
-- Good starting point for any comparative analysis
SELECT
  t.taxon_oid,
  t.taxon_display_name,
  t.analysis_project_type,
  t.has_coverage,
  p.library_method,
  p.read_count
FROM "img-db-2 postgresql".img_core_v400.taxon t
LEFT JOIN "gold-db-2 postgresql".gold.project p
  ON t.sequencing_gold_id = p.project_id
WHERE t.is_public = 'Yes'
  AND t.genome_type = 'metagenome'
  -- Add your analysis_project_type filter here
LIMIT 100
```

### Quality Filtering Best Practices

1. **Sequencing Platform Consistency (CRITICAL)**
   - Filter by `library_method` in GOLD to ensure all Illumina OR all PacBio/Nanopore
   - Short-read (Illumina): 184,888 projects
   - Long-read (PacBio/Nanopore): 1,915 projects
   - Document platform differences if mixing unavoidable

2. **Read Depth & Coverage**
   - **Best:** Use metagenomes with `has_coverage = 'Yes'` (60.3% of metagenomes)
   - **If read_count available:** Filter for similar sequencing depth
   - **Higher reads:** >100M reads preferred for detecting rare organisms
   - **Data availability:** Only 0.6% of GOLD projects have explicit read_count

3. **Assembly Quality & Complexity (CRITICAL)**
   - **Filter by `est_num_of_genomes`** from `taxon_assembly_stats` table (98.9% coverage)
   - Group metagenomes by estimated genome count:
     - **Simple** (0-5 genomes): clean assemblies, rare organisms
     - **Moderate** (5-100 genomes): defined enrichments or low-diversity habitats
     - **Complex** (>100 genomes): diverse environments, more artifacts
   - ⚠️ Do NOT mix simple and complex metagenomes in same analysis, or raise a warning if you do

4. **Note on Metagenome-Specific Fields:**
   - **Do NOT use `seq_status` for metagenomes** - This field is meaningful for individual isolate genomes, not metagenomes
   - **Do NOT use `has_per_sample_coverage` for metagenomes** - This flag is rarely populated (only 1/73,984 metagenomes) and not meaningful
   - **Do NOT use `genome_completion` for metagenomes** - This field is only meaningful for MAGs (individual assembled genomes from metagenomes), not for the metagenome assembly itself
   - **Instead use `est_num_of_genomes`** from `taxon_assembly_stats` to assess metagenome quality and complexity

5. **Co-assembly Artifacts:**
   - Be aware of `combined_sample_flag` for co-assembled genomes
   - Single-sample assemblies more reliable for individual comparisons

---

## 9. Common Pitfalls to Avoid

| Pitfall | Impact | Solution |
|---------|--------|----------|
| Mixing DNA + RNA | Completely incomparable gene sets | Filter to one or the other |
| Mixing viral + microbial metagenomes (different samples) | Different size fractions, non-overlapping taxa | Keep separate; use complementary if from same sample |
| Mixing rRNA depletion + polyA selection | Missing genes, biased abundance | Keep RNA protocols separate |
| Comparing enriched with unenriched | Biased community composition | Document or separate datasets |
| Ignoring enrichment method | Unknown confounding bias | Always check `analysis_project_type` |
| Using low-complexity with complex environments | Over-estimates rare organisms | Keep community types separate |
| **Mixing short-read & long-read metagenomes** | **Assembly quality, contiguity fundamentally different** | **Filter by `library_method`, use same platform type** |
| Ignoring read depth disparities | High-coverage bias masks low-coverage organisms | Normalize reads or filter for similar `read_count` |
| **Using `seq_status` for metagenomes** | **Misleading filtering - not meaningful for metagenomes** | **Do not use this field for metagenomes; use `est_num_of_genomes` instead** |
| **Using `genome_completion` for metagenomes** | **Misleading filtering - not meaningful for metagenomes** | **Do not use this field for metagenomes; use `est_num_of_genomes` instead** |
| Assuming all metagenomes are equally complex | Variable genome recovery affects abundance estimates | Group by expected complexity level using `est_num_of_genomes` |

---

## 10. Recommended Approach for New Comparative Analysis

### Step 1: Define Your Biology Question
- Studying activity or potential?
- Specific populations or whole community?
- Controlled or natural environments?

### Step 2: Choose Data Type
- Use decision tree (Section 4)
- Document inclusion/exclusion criteria

### Step 3: Assess Quality Criteria
- Check sequencing platform type (`library_method`)
- Verify read depth/coverage data availability
- Estimate genome recovery (associated MAGs)
- See Section 7 for detailed quality metrics

### Step 4: Query & Filter
- Use example queries from Section 5
- Apply quality filters from Section 8
- Verify homogeneity of dataset

### Step 5: Document Limitations
- Record which metagenomes are included
- Note platform, enrichment, and protocol differences
- Flag any data quality issues
- Justify any compromises (e.g., mixed platforms)

### Step 6: Validate Assumptions
- Check that data types are as expected
- Verify study metadata in GOLD
- Spot-check read counts and coverage flags
- Confirm MAG recovery for metagenome pairs

---

## 11. Getting Help: Linking IMG to GOLD

When you find a metagenome in IMG, link back to GOLD for detailed metadata:

```sql
-- From IMG metagenome, find GOLD project
SELECT
  t.taxon_oid,
  t.sequencing_gold_id,  -- Link to GOLD
  t.study_gold_id,        -- Link to GOLD study
  t.analysis_project_type
FROM "img-db-2 postgresql".img_core_v400.taxon t
WHERE t.taxon_oid = 2601500125  -- Replace with your taxon_oid
  AND t.is_public = 'Yes'

-- Then look up GOLD project for full details
SELECT *
FROM "gold-db-2 postgresql".gold.project
WHERE project_id = 'Gp0123456'  -- Replace with project_id from above
```

---

## Related Documentation

- [IMG_data_types.md](IMG_data_types.md) - Overview of all IMG genome types
- [data-catalog.md](data-catalog.md) - Complete GOLD and IMG table schemas
- [sql-quick-reference.md](sql-quick-reference.md) - SQL syntax for Dremio
- [authentication.md](authentication.md) - Token setup
