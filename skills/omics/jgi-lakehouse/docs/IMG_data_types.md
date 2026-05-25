# IMG Genome & Metagenome Data Types

Note: numbers are as of February 13, 2026, but will change in the future with new data addition

## Overview

The IMG (Integrated Microbial Genomes) database contains **286,759 genomic sequences** organized into two major categories:
- **196,379 isolate genomes** from cultured organisms or single-cell amplified genomes (SAGs)
- **90,380 metagenomes** from environmental samples

This guide helps you identify which IMG data types match your research needs and how to query them efficiently.

---

## Quick Reference: Data Types by Analysis Project Type

### **Individual Genomes from Cultures or Single Cells**

| Type | Count | Description | Best For |
|------|-------|-------------|----------|
| **Genome Analysis (Isolate)** | 150,515 | Traditional single-organism genomes from pure cultures | Comparative genomics, metabolic pathway analysis |
| **Single Cell Analysis (screened)** | 3,281 | SAGs with contaminant sequences removed by database comparison | Single-cell studies, rare organisms |
| **Single Cell Analysis (unscreened)** | 11,427 | SAGs without contaminant screening | Where you handle QC yourself |
| **Combined Assembly Single Cell (screened)** | 22 | Co-assembled SAGs with QC |  |
| **Combined Assembly Single Cell (unscreened)** | 14 | Co-assembled SAGs without QC |  |

### **Individual Genomes Reconstructed from Environmental Data**

These types represent individual genome reconstructions binned from metagenome assemblies, stored with a specific bacterial/archaeal `domain` (not `*Microbiome`).

| Type | Count | Description | Best For |
|------|-------|-------------|----------|
| **Metagenome-Assembled Genome (MAG)** | 26,260 | Genomes reconstructed by binning a metagenome assembly | Uncultured organisms, ecosystem diversity |
| **Metagenome-Extracted Genome** | 12 | Individual genomes manually extracted from metagenome datasets |  |

### **Community Metagenomes** (whole-community assemblies, `domain = '*Microbiome'`)

These types represent assemblies of reads from an environmental community rather than a single organism. They are stored with `domain = '*Microbiome'` in the taxon table and GTDB-Tk classification does not apply to them.

| Type | Count | Description | Best For |
|------|-------|-------------|----------|
| **Metagenome Analysis** | 49,939 | Standard shotgun environmental metagenomes | Community composition, functional potential |
| **Metatranscriptome Analysis** | 12,758 | Community mRNA sequenced as cDNA | Active metabolism, expressed gene profiling |
| **Metagenome - Single Particle Sort (SPS)** | 13,098 | Assembly from a single particle (cell or aggregate) isolated by flow cytometry; particle may contain multiple cells of mixed phylogenetic background | Cell-sorted community fractions |
| **Metagenome - Cell Enrichment** | 4,850 | Draft metagenome assembly from a cell enrichment (>1 cell); DNA typically amplified by WGA | Target-specific enriched communities |
| **Metagenome - Low Complexity** | 7,221 | Metagenomes from simple, well-defined communities | Biofilms, co-cultures, bioreactors |
| **Metagenome - SIP** (Stable Isotope Probing) | 1,374 | Metagenomes from isotope-labeled DNA fractions | Metabolically active community members |
| **Combined Assembly** | 1,057 | Co-assembly from reads across multiple metagenome samples | Cross-sample comparison, recovering low-abundance genes |
| **Combined Assembly SIP Metagenome** | 209 | Co-assembled SIP metagenomes | Isotope-labeled ecosystem studies |
| **Metagenome - Co-Culture** | 31 | Defined mixed-culture metagenomes | Synthetic communities, interaction studies |

---

## Filtering by Genome Type

IMG uses two genome type categories that cross-cut the analysis project types:

```sql
SELECT genome_type, COUNT(*) cnt
FROM "img-db-2 postgresql".img_core_v400.taxon
GROUP BY genome_type
```

### **Genome Type = 'isolate'** (196,379 records)
- Individual genome assemblies (one organism per record)
- Includes: traditional isolates, MAGs, SAGs (screened and unscreened)
- Best for: single-organism analyses, comparative genomics

### **Genome Type = 'metagenome'** (90,380 records)
- Whole-community assemblies (mixed-organism reads assembled together)
- Includes: Metagenome Analysis, Metatranscriptome Analysis, Single Particle Sort, Cell Enrichment, Low Complexity, SIP, Combined Assembly, Co-Culture
- Best for: community-level analyses, functional potential of ecosystems
- Note: `domain = '*Microbiome'` for all records in this group; GTDB-Tk does not apply

---

## Common Query Patterns

### 1. Find Traditional Isolate Genomes

```sql
SELECT taxon_oid, taxon_display_name, domain, phylum, genus, species
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE analysis_project_type = 'Genome Analysis (Isolate)'
  AND is_public = 'Yes'
LIMIT 100
```

### 2. Find Metagenome-Assembled Genomes (MAGs)

```sql
SELECT taxon_oid, taxon_display_name, domain, phylum, genus
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE analysis_project_type = 'Metagenome-Assembled Genome'
  AND is_public = 'Yes'
LIMIT 100
```

### 3. Find All Metagenomes (Environmental Samples)

```sql
SELECT taxon_oid, taxon_display_name, analysis_project_type
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE genome_type = 'metagenome'
  AND is_public = 'Yes'
LIMIT 100
```

### 4. Find Single-Cell Amplified Genomes (SAGs)

```sql
SELECT taxon_oid, taxon_display_name, analysis_project_type
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE analysis_project_type IN (
    'Single Cell Analysis (screened)',
    'Single Cell Analysis (unscreened)'
  )
  AND is_public = 'Yes'
LIMIT 100
```

### 5. Find RNA-Based Community Studies

```sql
SELECT taxon_oid, taxon_display_name
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE analysis_project_type = 'Metatranscriptome Analysis'
  AND is_public = 'Yes'
LIMIT 100
```

### 6. Find Specific Enrichment Studies

```sql
SELECT taxon_oid, taxon_display_name, analysis_project_type
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE analysis_project_type = 'Metagenome - Cell Enrichment'
  AND is_public = 'Yes'
LIMIT 100
```

### 7. Find Specific Isotope-Labeled Studies (SIP)

```sql
SELECT taxon_oid, taxon_display_name, analysis_project_type
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE analysis_project_type IN (
    'Metagenome - SIP',
    'Combined Assembly SIP Metagenome'
  )
  AND is_public = 'Yes'
LIMIT 100
```

### 8. Count Genomes by All Analysis Types

```sql
SELECT analysis_project_type, COUNT(*) cnt
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE is_public = 'Yes'
GROUP BY analysis_project_type
ORDER BY cnt DESC
```

### 9. Find good-quality isolate genomes of a specific phylum

For isolates, use `high_quality_flag` (IMG internal QC). `completeness_percentage`/`contamination_percentage`
from GOLD are often NULL for traditional isolates.

```sql
SELECT t.taxon_oid, t.taxon_display_name, t.genus, t.species,
       ts.total_bases / 1e6 AS genome_size_mb, ts.n_scaffolds
FROM "img-db-2 postgresql".img_core_v400.taxon t
JOIN "img-db-2 postgresql".img_core_v400.taxon_stats ts
  ON t.taxon_oid = ts.taxon_oid
WHERE t.phylum = 'Proteobacteria'
  AND t.analysis_project_type = 'Genome Analysis (Isolate)'
  AND t.high_quality_flag = 'Yes'
  AND t.is_public = 'Yes'
  AND t.obsolete_flag = 'No'
LIMIT 100
```

### 10. Find High-Quality Metagenome-Assembled Genomes

Use CheckM2 scores from `taxon_gtdbtk_lineage` (preferred) or `genome_completion` from the taxon table as a fallback.

```sql
-- Preferred: CheckM2-based quality (MIMAG high-quality tier: ≥90% complete, ≤5% contaminated)
SELECT t.taxon_oid, t.taxon_display_name, t.domain, t.phylum,
       g.gtdbtk_genus, g.checkm_completeness, g.checkm_contamination
FROM "img-db-2 postgresql".img_core_v400.taxon t
JOIN "img-db-2 postgresql".img_core_v400.taxon_gtdbtk_lineage g
  ON t.taxon_oid = g.taxon_oid
WHERE t.analysis_project_type = 'Metagenome-Assembled Genome'
  AND g.checkm_completeness >= 90
  AND g.checkm_contamination <= 5
  AND t.is_public = 'Yes'
  AND t.obsolete_flag = 'No'
LIMIT 100

-- Fallback: genome_completion field (may be NULL for many MAGs)
SELECT taxon_oid, taxon_display_name, genome_completion
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE analysis_project_type = 'Metagenome-Assembled Genome'
  AND genome_completion >= 80
  AND is_public = 'Yes'
  AND obsolete_flag = 'No'
LIMIT 100
```

---

## Data Type Selection Guide

### **Choose "Genome Analysis (Isolate)" if you:**
- Want well-curated, single-organism genomes
- Need taxonomically reliable data
- Are doing comparative genomics
- Require highest annotation quality
- **Row count: 150,515** (most abundant type)

### **Choose MAGs (Metagenome-Assembled Genome) if you:**
- Study uncultured organisms
- Want microbial diversity from environmental samples
- Accept reconstructed genomes from metagenomics
- Need organisms not available in pure culture
- **Row count: 26,260**

### **Choose Metatranscriptomes if you:**
- Study active gene expression
- Differentiate between potential and actual metabolism
- Work with RNA-based community profiling
- Analyze functional activity in environments
- **Row count: 12,758**

### **Choose Metagenomes if you:**
- Study whole microbial community composition
- Analyze metabolic potential of ecosystems
- Look for rare organisms or functions
- Want unbiased environmental sampling
- **Row count: 49,939** (largest metagenome category)

### **Choose Single-Cell SAGs if you:**
- Study rare or unculturable microorganisms at the individual cell level
- Examine individual cell genomes
- **Prefer screened SAGs** (`Single Cell Analysis (screened)`) for analysis — unscreened SAGs may contain contaminant sequences
- **Row count: 14,708** (screened 3,281 + unscreened 11,427)

### **Choose community metagenome subtypes (Cell Enrichment, SPS, SIP, Low Complexity) if you:**
- Study enriched or sorted microbial fractions at the **community** level (these are metagenome assemblies, not individual genomes)
- Track isotope incorporation in active community members (SIP)
- Study flow-cytometry-sorted particles (SPS may contain multiple cells of mixed background)
- Analyze low-complexity biofilm or co-culture communities
- **Row count: ~26,500** (SPS 13,098 + Cell Enrichment 4,850 + Low Complexity 7,221 + SIP 1,374)

---

## Data Type Statistics (as of Feb 2026)

```
Total genomes in IMG: 286,759

By Genome Type:
  • Isolate genomes:     196,379 (68.5%)
  • Metagenomes:          90,380 (31.5%)

Top 5 Analysis Project Types:
  1. Genome Analysis (Isolate)        150,515 (52.5%)
  2. Metagenome Analysis               49,939 (17.4%)
  3. Metagenome-Assembled Genome       26,260 (9.2%)
  4. Metagenome - Single Particle Sort 13,098 (4.6%)
  5. Metatranscriptome Analysis        12,758 (4.4%)
```

---

## Accessing Genome Files

Once you've identified the genomes you want, use the `taxon_oid` field to download files from the JGI filesystem:

```bash
# Genome packages are located at:
/clusterfs/jgi/img_merfs-ro/img_web/img_web_data/download/{taxon_oid}.tar.gz

# Example: Download and extract MAG
cp /clusterfs/jgi/img_merfs-ro/img_web/img_web_data/download/2601500125.tar.gz .
tar -xzf 2601500125.tar.gz

# Extracted files include:
#   - {taxon_oid}.fna          (genome assembly)
#   - {taxon_oid}.genes.faa    (protein sequences)
#   - {taxon_oid}.genes.fna    (gene sequences)
#   - {taxon_oid}.gff          (annotations)
#   - {taxon_oid}.cog.tab.txt  (COG annotations)
#   - {taxon_oid}.pfam.tab.txt (Pfam annotations)
#   - {taxon_oid}.ko.tab.txt   (KEGG KO annotations)
```

See the [examples](../examples/) folder for automated download scripts.

---

## Important Notes

1. **Not all genomes are public**: Always filter with `is_public = 'Yes'` and `obsolete_flag = 'No'`
2. **`seq_status` is not informative**: For metagenomes, SAGs, and MAGs it is always `Permanent Draft`. For isolates it can be `Finished`, `Permanent Draft`, or `Draft`, but most submitters do not specify it, so it defaults to `Permanent Draft` regardless of actual assembly quality. Do not use it as a quality proxy.
3. **`high_quality_flag` is only meaningful for isolates**: IMG assigns it based on coding density (70–100%), genes per Mb (700–1400), sequences per Mb (≤300), and GOLD phylogeny not being UNCLASSIFIED. For MAGs it is almost always `'No'` (99.9%) and carries no quality signal — use CheckM2 from `taxon_gtdbtk_lineage` instead.
4. **MAG quality**: Use `taxon_gtdbtk_lineage.checkm_completeness` / `checkm_contamination` (CheckM2). Fall back to `genome_completion` in the taxon table when GTDB-Tk has no entry.
5. **Community metagenome quality**: `high_quality_flag`, `genome_completion`, and GTDB-Tk classification all do not apply to community metagenomes (`domain = '*Microbiome'`).
6. **Gene content**: Use the `gene` table for annotations within individual genomes.
7. **Cross-references**: Link to GOLD projects via `analysis_project_id` (= GOLD `Ga*` ID) or `sequencing_gold_id` / `study_gold_id`.

---

## Related Documentation

- [img_and_gold_terms.md](img_and_gold_terms.md) - Full IMG/GOLD glossary (definitions for all terms, project types, quality flags, IDs)
- [explore_IMG_genomes.md](explore_IMG_genomes.md) - Genome metadata query guide (taxonomy, quality, size, GTDB)
- [data-catalog.md](data-catalog.md) - Full table inventory
- [sql-quick-reference.md](sql-quick-reference.md) - SQL syntax guide
- [examples/](../examples/) - Download and analysis scripts
