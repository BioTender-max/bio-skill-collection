# Whole Exome Sequencing Report: Sample1
> **Project** X202SC26016276-Z01-F001 | **Platform** Illumina NovaSeq PE150 | **Capture** Xplus WES (60.5 Mb) | **Reference** GRCh38/hg38

---

## 1. Exome Summary

| Metric | Count |
|--------|-------|
| Total SNP variants | 25,432 |
| Missense | 11,234 |
| Synonymous | 12,100 |
| Stopgain | 85 |
| Frameshift | 42 |
| Splicing | 120 |
| Loss-of-function (stopgain + frameshift) | 127 |
| Rare coding (gnomAD < 1%) | 3,210 |
| Rare + computationally damaging | 245 |
| ClinVar Pathogenic / Likely Pathogenic | 8 |

The homozygosity to heterozygosity ratio is **2.35**, which is above the expected ~1.5 for outbred populations.

## 2. Clinically Significant Variants

Sample1 carries 8 variant(s) classified as Pathogenic or Likely Pathogenic in ClinVar:

| Gene | Variant | Zygosity | Classification | Consequence | Associated Condition |
|------|---------|----------|----------------|-------------|---------------------|
| BRCA2 | c.5946delT | Het | Pathogenic | frameshift deletion | Hereditary breast/ovarian cancer |
| MUTYH | c.536A>G | Het | Pathogenic | missense SNV | MUTYH-associated polyposis |
| GJB2 | c.35delG | Hom | Pathogenic | frameshift deletion | Deafness, autosomal recessive 1A |
| SERPINA1 | c.1096G>A | Het | Pathogenic | missense SNV | Alpha-1-antitrypsin deficiency |
| HFE | c.845G>A | Het | Pathogenic | missense SNV | Hereditary hemochromatosis |
| DPYD | c.1905+1G>A | Het | Pathogenic/LP | splicing | Dihydropyrimidine dehydrogenase deficiency |
| MEFV | c.2080A>G | Het | Likely Pathogenic | missense SNV | Familial Mediterranean fever |
| GAA | c.525delT | Het | Pathogenic | frameshift deletion | Pompe disease |

An additional 12 variant(s) have conflicting or uncertain classifications.

The most clinically relevant are listed below (coding variants in disease-associated genes):

ACMG SF v3.2 actionable genes: 156 coding variants identified across 73 medically actionable genes, of which 2 have ClinVar P/LP classification.

Cancer predisposition panel: 3 with P/LP classification across 95 cancer predisposition genes.

## 3. Pharmacogenomics

The following pharmacogenomic markers were identified from CPIC-defined star-allele positions. Variants are reported where the genotype differs from the reference allele.

| Gene | Variant | Allele | Zygosity | Clinical Effect | Affected Medications |
|------|---------|--------|----------|-----------------|---------------------|
| CYP2D6 | rs3892097 | *4 | Het | Slow metaboliser | codeine, tramadol, tamoxifen |
| NAT2 | rs1801280 | *5 | Hom | Slow acetylator | isoniazid, hydralazine |
| CYP2C19 | rs4244285 | *2 | Het | Slow metaboliser | clopidogrel, omeprazole |
| SLCO1B1 | rs4149056 | *5 | Het | Decreased transport | simvastatin, atorvastatin |
| VKORC1 | rs9923231 | - | Het | Low-dose warfarin | warfarin |
| CYP1A2 | rs762551 | *1F | Hom | Ultra-rapid (inducible) | caffeine, clozapine |

## 4. Fitness and Nutrition Traits

Genotypes at positions associated with fitness and nutrition traits (Corpas et al. 2021, Tables 3-5). Only markers captured by the WES panel and with non-reference genotypes are shown.

Evidence grades: A = strong replication, B = moderate, C = preliminary.

### Fitness

| Gene | Variant | Trait | Interpretation | Ev. |
|------|---------|-------|----------------|-----|
| ACTN3 | rs1815739 | Muscle fibre type (power vs endurance) | XX - endurance phenotype | A |

### Nutrition

| Gene | Variant | Trait | Interpretation | Ev. |
|------|---------|-------|----------------|-----|
| MTHFR | rs1801133 | Folate metabolism (C677T) | CT - 35% reduced | A |
| GC | rs2282679 | Vitamin D binding protein | Lower vitamin D | A |
| FADS1 | rs174547 | Omega-3 conversion | Poor converter | B |
| TCF7L2 | rs7903146 | Type 2 diabetes risk | Moderate | A |
| ADH1B | rs1229984 | Alcohol metabolism speed | Ultra-rapid | A |
| TAS2R38 | rs713598 | Bitter taste perception | Medium taster | B |

## 5. Prioritised Rare Damaging Variants

245 variants pass all filters: coding, rare (gnomAD AF < 0.01), and computationally predicted damaging (CADD > 20 or REVEL > 0.5). Top 15 ranked by pathogenicity prediction score:

| Gene | Variant | Consequence | Zygosity | REVEL | CADD | gnomAD AF | OMIM Disease |
|------|---------|-------------|----------|-------|------|-----------|-------------|
| ABCA4 | c.5882G>A | missense SNV | Het | 0.92 | 33.0 | 0.0012 | Stargardt disease |
| GJB2 | c.35delG | frameshift deletion | Hom | - | 35.0 | 0.0089 | Deafness, autosomal recessive 1A |
| USH2A | c.2299delG | frameshift deletion | Het | - | 34.0 | 0.0034 | Usher syndrome type 2A |
| CFTR | c.1521_1523delCTT | frameshift deletion | Het | - | 32.0 | 0.0078 | Cystic fibrosis |
| ATP7B | c.3207C>A | missense SNV | Het | 0.88 | 29.5 | 0.0015 | Wilson disease |

## 6. Disease and Pathway Context

Across the full variant set: 1,245 variants map to OMIM disease entries, 456 overlap GWAS Catalog associations, and 89 have COSMIC somatic mutation records.

KEGG pathways enriched in rare coding variants:
- hsa04010: MAPK signalling pathway (12 variants)
- hsa04151: PI3K-Akt signalling pathway (9 variants)
- hsa04110: Cell cycle (7 variants)
- hsa04310: Wnt signalling pathway (5 variants)

## 7. Methods

Whole exome sequencing was performed on an Illumina NovaSeq 6000 platform using 150 bp paired-end reads with the Xplus capture kit (60.5 Mb target region). Reads were aligned to the GRCh38/hg38 reference genome using BWA-MEM. Variant calling was performed with GATK HaplotypeCaller v4.3.0 following GATK Best Practices. Functional annotation was performed with ANNOVAR, incorporating ClinVar (2024), gnomAD v3.1.2 (9 population groups), COSMIC, OMIM, SIFT, PolyPhen-2, CADD, REVEL, and 15 additional databases. Pharmacogenomic analysis used CPIC star-allele definitions with evidence enrichment from the ClinPGx API (PharmGKB). Fitness and nutrition trait interpretation followed the evidence framework of Corpas et al. (2021) Frontiers in Genetics 12:535123. Variant prioritisation applied sequential filters: coding consequence, population frequency (gnomAD AF < 0.01), computational pathogenicity (CADD > 20 or REVEL > 0.5).

*Report prepared by ClawBio WES Analysis Pipeline on 2026-04-05*

> **Disclaimer**: This report is generated for research and educational purposes only. It is not a clinical diagnostic report and should not be used for making medical decisions without consulting a qualified healthcare professional.
