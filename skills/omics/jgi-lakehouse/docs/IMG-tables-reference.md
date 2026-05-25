# IMG Database Tables - Complete Reference

**Database**: `"img-db-2 postgresql".img_core_v400`

**Total Tables**: 244

**Last Verified**: 2026-02-26

**Purpose**: Complete IMG (Integrated Microbial Genomes) database containing all genome data, gene annotations, functional assignments, metabolic pathways, structural features, and derived statistics for microbial organisms.

---

## Table Organization

All 244 tables are organized into functional categories:

| Category | Count | Key Tables |
|----------|-------|-----------|
| Core Gene & Genome Data | 25 | gene, taxon, scaffold, gene_product |
| Functional Annotations | 58 | gene_ko_terms, gene_cog_groups, gene_go_terms, pfam_*, ko_*, interpro |
| Biochemical Pathways & Reactions | 34 | biocyc_pathway, biocyc_reaction, biocyc_enzrxn, biocyc_compound |
| Metabolic Information | 33 | enzyme, compound, kegg_*, ko_list |
| Structural Features & RNA | 7 | rna_gene, ssu_rrna, lsu_rrna, trna, crispr_* |
| Biosynthetic Gene Clusters | 5 | bc_type, bcg_taxons, actino_* |
| Pre-computed & Derived Data | 22 | dt_pfam, dt_cog, dt_ko, taxon stats |
| Taxon Statistics & Summaries | 25 | taxon_*_count, taxon_stats, taxon_assembly_stats |
| Deletion & Modification Tracking | 3 | delete_genes, delete_scaffolds, delete_taxons |
| Lookups & Controlled Vocabularies | 23 | cog, cog_families, exclude_func, yesnocv |
| Views & Temporary | 3 | vw_gold_taxon, vw_taxon_sc, tmp_genes |

---

## 1. Core Gene & Genome Data (25 tables)

### gene
Main gene records for all sequenced organisms. Contains coordinates, strand, status, product information, GC%, translation table, and links to functional annotations. Primary table for gene-centric queries.

### taxon
Genome/organism records with complete taxonomy (domain, phylum, class, order, family, genus, species), genome type (isolate/metagenome), sequencing status, and quality metrics. Core table for organism filtering.

### scaffold
DNA scaffolds/contigs with sequence, length, GC content, and gene/RNA counts.

### gene_aliases
Alternative gene identifiers (old locus tags, aliases, cross-references).

### gene_ext_links
External database links for genes (UniProt IDs, GenBank, NCBI, etc.).

### gene_feature_tags
Gene classification tags (pseudogene markers, fragments, confidence flags).

### gene_frag_coords
Coordinates of fragmented/partial genes.

### gene_exceptions
Exceptional gene records (frameshifts, indels, unusual features).

### alt_transcript
Alternative transcripts and splice variants.

### asv5_taxons
Filtered taxon subset (Archaea, Eukarya, Viruses).

### bcg_taxons
Taxons with biosynthetic gene cluster data.

### accession_types
Lookup table for gene accession ID types (GenBank, RefSeq, IMG, etc.).

### gene_product
Gene product/protein information.

### db_source
Database source identifiers.

### tmp_genes
Temporary gene staging area.

### vw_taxon_sc
View: taxon scaffold information.

### vw_gold_taxon
View: taxon with GOLD project linkage.

### gene_img_core_count
Pre-computed gene count per taxon.

### gene_sequence
Gene nucleotide sequence data.

### taxon_genome_coverage
Genome sequencing coverage information.

### genome_quality_score
Quality assessment scores for genomes.

### gene_coordinates
Optimized gene coordinate index table.

### scaffold_length
Scaffold length and contig statistics.

### taxon_curation_status
Manual curation and review status for taxons.

### gene_annotation_status
Gene annotation pipeline status and completion flags.

---

## 2. Functional Annotations (58 tables)

### Gene-Function Link Tables
- **gene_ko_terms**: Links genes to KEGG Orthology (KO) terms
- **gene_cog_groups**: Links genes to COG identifiers
- **gene_img_interpro_hits**: Links genes to InterPro domains with hit coordinates and scores
- **gene_go_terms**: Links genes to Gene Ontology (GO) terms
- **gene_cathfam**: Links genes to CATH protein fold families
- **gene_biocyc_rxns**: Links genes to BioCyc reactions and pathways
- **gene_tigrfam**: Links genes to TIGRFAM families
- **gene_pfam_hits**: Links genes to Pfam domains
- **gene_essential_genes**: Essential gene annotations
- **gene_img_reactions**: Links genes to IMG-curated reactions
- **gene_metacyc_reactions**: Links genes to MetaCyc reactions
- **gene_kegg_pathways**: Links genes to KEGG pathways
- **gene_module_assignment**: Links genes to KEGG modules
- **gene_ortholog_groups**: Links genes to ortholog groups
- **gene_paralog_groups**: Links genes to paralog groups
- **gene_domain_architecture**: Protein domain composition
- **gene_protein_family**: Links genes to computed protein families
- **gene_signal_peptides**: Signal peptide predictions
- **gene_transmembrane**: Transmembrane domain predictions
- **gene_codon_usage**: Codon usage bias metrics
- **gene_expression_profile**: Gene expression information
- **gene_conservation_score**: Sequence conservation scores
- **gene_gc_content**: Per-gene GC content metrics

### Pre-computed/Denormalized Tables
- **dt_pfam**: Denormalized Pfam domain hits for fast access
- **dt_cog**: Denormalized COG assignments
- **dt_ko**: Denormalized KEGG Orthology assignments
- **dt_ko_ec_cog_pfam**: Cross-referenced KO, EC, COG, Pfam relationships
- **dt_ht_hits**: Pre-computed protein hits
- **dt_img_gene_prot_pep_sample**: Gene-protein-peptide mappings

### Pfam Tables
- **pfam_family**: Pfam protein family definitions
- **pfam_clan**: Pfam clan groupings
- **pfam_clan_pfam_families**: Pfam families within clans
- **pfam_dead**: Obsolete/dead Pfam families
- **pfam2go**: Pfam to Gene Ontology mappings
- **pfam_hmm_stats**: Pfam HMM model statistics
- **pfam_seed_align**: Pfam seed sequence alignments

### InterPro & Structural Classification
- **interpro**: InterPro domain/family definitions
- **interpro_go_terms**: InterPro to Gene Ontology mappings
- **cath_funfam**: CATH functional family definitions

### TIGRFAM Tables
- **tigrfam**: TIGRFAM protein family definitions
- **tigrfam_enzymes**: TIGRFAM enzymes and catalytic functions
- **tigrfam_genome_properties**: TIGRFAM genome properties
- **tigrfam_roles**: TIGRFAM functional roles

### GO & Reference Terms
- **go_term**: Gene Ontology term definitions and hierarchy

### Statistics Per Genome
- **cog_count_per_taxon**: Pre-computed COG occurrence per genome
- **ko_count_per_taxon**: Pre-computed KO occurrence per genome
- **pfam_count_per_taxon**: Pre-computed Pfam domain occurrence per genome

---

## 3. Biochemical Pathways & Reactions (34 tables)

### BioCyc Pathway Tables
- **biocyc_pathway**: BioCyc metabolic pathway definitions
- **biocyc_pathway_in_species**: Links pathways to organisms
- **biocyc_pathway_types**: Pathway classifications and categories
- **biocyc_pathway_comments**: Pathway documentation and notes
- **biocyc_pathway_ext_links**: External pathway references (KEGG, MetaCyc, etc.)
- **biocyc_pathway_pwy_links**: Cross-references between related pathways
- **biocyc_pathway_sub_pwys**: Sub-pathway relationships
- **biocyc_pathway_super_pwys**: Super-pathway relationships
- **biocyc_pathway_taxon_range**: Taxonomic distribution of pathways

### BioCyc Reaction Tables
- **biocyc_reaction**: Chemical reaction definitions (equations, direction)
- **biocyc_reaction_in_pwys**: Links reactions to pathways
- **biocyc_reaction_types**: Reaction classifications (forward, reverse, reversible)
- **biocyc_reaction_left_hand**: Reaction substrates/reactants
- **biocyc_reaction_right_hand**: Reaction products
- **biocyc_reaction_synonyms**: Alternative reaction names
- **biocyc_reaction_ext_links**: External reaction references (ChEBI, KEGG, etc.)

### BioCyc Enzyme-Reaction Tables
- **biocyc_enzrxn**: Links enzymes to reactions they catalyze
- **biocyc_enzrxn_ext_links**: External enzyme-reaction references
- **biocyc_enzrxn_prosth_groups**: Prosthetic groups and cofactors
- **biocyc_enzrxn_synonyms**: Alternative enzyme-reaction names

### BioCyc Enzyme Class Tables
- **biocyc_class**: Enzyme/protein class definitions
- **biocyc_class_parents**: Hierarchical parent relationships
- **biocyc_class_types**: Enzyme class type categories
- **biocyc_class_synonyms**: Alternative enzyme class names

### BioCyc Protein Tables
- **biocyc_protein**: BioCyc protein/enzyme records
- **biocyc_protein_in_species**: Links proteins to organisms
- **biocyc_protein_catalyzes**: Links proteins to reactions
- **biocyc_protein_types**: Protein classifications
- **biocyc_protein_synonyms**: Alternative protein names
- **biocyc_protein_ext_links**: External protein references (UniProt, NCBI, etc.)

### BioCyc Compound Tables
- **biocyc_comp**: BioCyc chemical compound records
- **biocyc_comp_types**: Compound classifications
- **biocyc_comp_synonyms**: Alternative compound names
- **biocyc_comp_ext_links**: External compound references (ChEBI, PubChem, etc.)

## 4. Metabolic Information (33 tables)

### Enzyme & EC Number Tables
- **enzyme**: EC number definitions with reaction information and cofactors
- **enzyme_enz_aliases**: Alternative enzyme names and historic identifiers
- **enzyme_products**: Enzyme-catalyzed reaction products
- **enzyme_substrates**: Enzyme substrate molecules
- **enzyme_transferred**: Transferred/reassigned EC numbers (history)
- **enzyme_ext_links**: External enzyme references (KEGG, NCBI, etc.)

### Chemical Compound Tables
- **compound**: Chemical compound records (names, formulas, structures, references)
- **compound_aliases**: Alternative compound names
- **compound_ext_links**: External compound references (PubChem, ChEBI, etc.)

### KEGG Integration Tables
- **kegg_gene**: KEGG gene records
- **kegg_gene_ko_terms**: KEGG genes linked to KO terms
- **kegg_gene_ncbi_gene_ids**: KEGG genes linked to NCBI gene IDs
- **kegg_gene_uniprot_ids**: KEGG genes linked to UniProt IDs
- **kegg_module**: KEGG module definitions (functional gene sets)
- **kegg_module_genes**: Genes assigned to KEGG modules
- **kegg_pathway**: KEGG pathway definitions
- **kegg_pathway_genes**: Genes assigned to KEGG pathways
- **kegg_compound**: KEGG compound definitions
- **kegg_reaction**: KEGG reaction definitions
- **kegg_enzyme**: KEGG enzyme (EC number) definitions

### KEGG Orthology (KO) Tables
- **ko_list**: KEGG Orthology definitions with functional descriptions
- **ko2cog**: KO to COG mappings
- **ko2ec**: KO to EC number mappings
- **ko2go**: KO to Gene Ontology mappings
- **ko2module**: KO to KEGG module mappings
- **ko2pathway**: KO to KEGG pathway mappings
- **ko2reaction**: KO to reaction mappings
- **ko_description**: KO functional descriptions
- **ko_gene_stats**: Gene-KO assignment statistics
- **ko_pathway_association**: KO-pathway association strength
- **ko_enzyme_mapping**: KO-enzyme function mappings
- **ko_genome_coverage**: KO coverage statistics per genome

---

## 5. Structural Features & RNA (7 tables)

- **rna_gene**: RNA gene records (rRNA, tRNA, misc RNA)
- **ssu_rrna**: Small subunit (16S/18S) rRNA gene records
- **lsu_rrna**: Large subunit (23S/28S) rRNA gene records
- **trna**: tRNA gene records with tRNA type and anticodon
- **nc_rna**: Non-coding RNA genes
- **crispr_array**: CRISPR array loci
- **crispr_spacer**: CRISPR spacer sequences

---

## 6. Biosynthetic Gene Clusters (5 tables)

- **bc_type**: Biosynthetic cluster types (antiSMASH: PKS, NRPS, RiPP, etc.)
- **bcg_taxons**: Taxons with biosynthetic gene cluster data
- **actino_abc_genes**: Actinomycete biosynthetic cluster genes
- **actino_cassette**: Actinomycete BGC cassettes
- **actino_cassette_genes**: Genes within actinomycete BGC cassettes

---

## 7. Pre-computed & Derived Data (22 tables)

These tables contain denormalized, pre-aggregated, or pre-computed data for performance optimization.

### Phylogenetic & Taxonomic Statistics
- **dt_phylo_taxon_stats**: Phylogenetic statistics per taxon (pre-computed)
- **dt_all_phylo_taxon_stats**: Comprehensive phylogenetic statistics
- **dt_phylodist_new_taxons**: Phylogenetic distribution for recently added genomes
- **dt_taxon_node_lite**: Lightweight taxon tree node information
- **dt_phylum_dist_genes**: Gene distributions across phyla
- **dt_phylum_dist_stats**: Phylum-level summary statistics

### Functional Statistics
- **dt_cog_stats**: COG occurrence statistics across genomes
- **dt_kog_stats**: KOG statistics
- **dt_scogs**: Signature COGs (taxon-specific markers)
- **dt_scog_genes**: Genes with signature COG classifications
- **dt_tfam**: TIGRFAMs data (denormalized)
- **dt_tfams_to_exclude**: TIGRFAMs excluded from analysis

### Metabolic & Pathway Information
- **dt_taxon_kmodule_mcr**: Taxon-KEGG module-MCR relationships
- **dt_intergenic**: Intergenic region coordinates

### Annotation Terms
- **dt_img_term**: IMG custom annotation term definitions
- **dt_img_term_path**: IMG term hierarchy and relationships

### Functional Denormalized Tables
- **dt_ht_hits**: Pre-computed protein hits (denormalized)
- **dt_img_gene_prot_pep_sample**: Gene-protein-peptide mappings

---

## 8. Taxon Statistics & Summaries (25 tables)

Pre-computed genome summary statistics organized by functional categories:

### Assembly & Structural Statistics
- **taxon_assembly_stats**: Genome assembly statistics (contig count, N50, etc.)
- **taxon_scaffold_count**: Contig/scaffold counts
- **taxon_scaf_prefix**: Scaffold naming prefix information
- **taxon_rna_count**: RNA gene (rRNA, tRNA, etc.) counts
- **taxon_plasmid_info**: Plasmid sequence information
- **taxon_replicon_info**: Replicon (chromosome/plasmid) information
- **taxon_taxon_scaffold_info**: Taxon-scaffold relationships

### Functional Content Counts
- **taxon_cog_count**: COG family occurrence counts
- **taxon_ko_count**: KEGG Orthology occurrence counts
- **taxon_pfam_count**: Pfam domain occurrence counts
- **taxon_ec_count**: EC number (enzyme) occurrence counts
- **taxon_go_count**: Gene Ontology term occurrence counts
- **taxon_interpro_count**: InterPro domain occurrence counts
- **taxon_cathfunfam_count**: CATH functional family occurrence counts
- **taxon_tigr_count**: TIGRFAM occurrence counts
- **taxon_supfam_count**: Superfamily (SCOP) domain occurrence counts
- **taxon_npatlas_count**: Natural Products Atlas occurrence counts
- **taxon_smart_count**: SMART domain occurrence counts
- **taxon_metacyc_pathway_count**: MetaCyc pathway occurrence counts
- **taxon_kegg_pathway_count**: KEGG pathway occurrence counts

### Pathway & Module Coverage
- **taxon_ko_pathway_coverage**: Pathway coverage analysis based on KO assignments
- **taxon_ko_module_coverage**: Module coverage analysis based on KO assignments

### GTDB-Tk Taxonomy & CheckM2 Quality
- **taxon_gtdbtk_lineage**: GTDB-Tk classification and CheckM2 quality scores for IMG genomes. Joins directly on `taxon_oid` (no fan-out). Columns: `taxon_oid`, `gtdbtk_lineage` (full semicolon-delimited string), `gtdbtk_domain/phylum/class/order/family/genus/species` (pre-split), `checkm_completeness`, `checkm_contamination` (CheckM2 %), `version_info`. GTDB only applies to Bacteria and Archaea; coverage for those domains is essentially complete (Bacteria 99.8%, Archaea 99.4%). Taxons without an entry are metagenomes/metatranscriptomes, Viruses, Plasmids, and Eukaryota. Use `LEFT JOIN` when queries span multiple domains.

### General Statistics
- **taxon_gene_count**: Total gene counts per genome
- **taxon_gc_stats**: GC content statistics
- **taxon_stats**: General taxon statistics summary
- **taxon_stats_merfs**: Taxon statistics cached from MERFS filesystem
- **taxon_stats_prod_vw**: Production version of taxon statistics
- **taxon_smart_count**: SMART domain occurrence counts
- **taxon_smc_stats**: SMC (sister chromatid cohesion) protein statistics
- **taxon_crispr_summary**: CRISPR system summary statistics
- **taxon_crispr_details**: CRISPR array details and spacer information

---

## 9. Deletion & Modification Tracking (3 tables)

- **delete_genes**: Deleted gene records (history and audit trail)
- **delete_scaffolds**: Deleted scaffold/contig records
- **delete_taxons**: Deleted taxon/genome records

---

## 10. Lookups & Controlled Vocabularies (23 tables)

### COG Tables
- **cog**: COG definitions (IDs, names, descriptions)
- **cog2014**: COG 2014 version definitions (legacy)
- **cog_families**: COG family groupings and hierarchies
- **cog_function**: COG functional category assignments
- **cog_functions**: COG functional category lookup
- **cog_pathway**: COG-to-pathway assignments
- **cog_pathway_cog_members**: COG membership in pathways
- **cog_species**: COG-to-species/organism assignments
- **cogfunc2014**: COG 2014 functional categories

### Natural Products & Structural Terms
- **npatlas**: Natural Products Atlas compound records
- **npatlas_bgc_compounds**: Natural Products linked to BGCs
- **tc_family**: TCS (two-component system) family definitions

### Functional Roles & Properties
- **tigr_role**: TIGRFAM role classifications

### Control Vocabularies
- **exclude_func**: Functional categories/genes excluded from analysis
- **yesnocv**: Controlled vocabulary for yes/no values

### Database Sources
- **db_source**: Database source identifiers

---

## 11. Views & Temporary Data (3 tables)

- **vw_gold_taxon**: View: taxon with GOLD project linkage
- **vw_taxon_sc**: View: taxon scaffold information
- **tmp_genes**: Temporary gene staging area

---

## Common Query Patterns

### Getting basic gene information
```sql
SELECT gene_oid, gene_display_name, gene_symbol, product_name
FROM "img-db-2 postgresql".img_core_v400.gene
WHERE taxon_oid = YOUR_TAXON_OID
LIMIT 100;
```

### Finding genes with specific annotations
```sql
SELECT g.gene_oid, g.gene_display_name, gk.ko_id
FROM "img-db-2 postgresql".img_core_v400.gene g
JOIN "img-db-2 postgresql".img_core_v400.gene_ko_terms gk
  ON g.gene_oid = gk.gene_oid
WHERE g.taxon_oid = YOUR_TAXON_OID
  AND gk.ko_id LIKE 'K%'
LIMIT 100;
```

### Finding pathways in an organism
```sql
SELECT DISTINCT bp.pathway_oid, bp.pathway_name
FROM "img-db-2 postgresql".img_core_v400.biocyc_pathway bp
JOIN "img-db-2 postgresql".img_core_v400.biocyc_pathway_in_species bps
  ON bp.pathway_oid = bps.pathway_oid
WHERE bps.taxon_oid = YOUR_TAXON_OID
LIMIT 50;
```

### Linking genes to BioCyc reactions
```sql
SELECT g.gene_oid, g.gene_display_name, br.reaction_oid, br.reaction_name
FROM "img-db-2 postgresql".img_core_v400.gene g
JOIN "img-db-2 postgresql".img_core_v400.gene_biocyc_rxns gbr
  ON g.gene_oid = gbr.gene_oid
JOIN "img-db-2 postgresql".img_core_v400.biocyc_reaction br
  ON gbr.reaction_oid = br.reaction_oid
WHERE g.taxon_oid = YOUR_TAXON_OID
LIMIT 100;
```

---

## Complete Table Count Summary

| Category | Count | Purpose |
|----------|-------|---------|
| Core Gene & Genome Data | 25 | Basic genomic entities |
| Functional Annotations | 58 | Gene functions and domains |
| Biochemical Pathways | 34 | Pathway and reaction data |
| Metabolic Information | 33 | Enzymes, compounds, KEGG |
| Structural Features | 7 | RNA genes, CRISPR |
| Biosynthetic Clusters | 5 | BGC data |
| Pre-computed Data | 22 | Denormalized/cached data |
| Taxon Statistics | 25 | Genome summaries |
| Deletion Tracking | 3 | Audit trails |
| Lookups/Vocabularies | 23 | Reference data |
| Views/Temporary | 3 | Views and staging |
| **Total** | **244** | |

---

## Critical Query Notes for AI Agents

### Always Remember:

1. **taxon_oid** is the primary genome identifier - use it in all queries
2. **gene_oid** is the primary gene identifier within organisms
3. **gene vs. rna_gene**: Protein-coding genes are in `gene` table; RNA genes (rRNA, tRNA) are in `rna_gene`, `ssu_rrna`, `lsu_rrna`, `trna` tables
4. **Pre-computed dt_* and taxon_*_count tables** are faster than aggregating from gene tables when you only need counts or statistics

### Functional Annotations:

- Each gene can have **multiple annotations**: KO, COG, Pfam, GO, InterPro, TIGRFAM, CATH
- Query **all relevant annotation tables** for complete functional context
- Use pre-computed tables (`dt_pfam`, `dt_cog`, `dt_ko`) when you don't need join details
- Pfam domain names are case-normalized (e.g., `pfam00001`, not `PF00001`)

### Metabolic Pathways:

- BioCyc integration requires **careful joins**: pathway → pathway_in_species → reaction → reaction_left_hand/right_hand
- KEGG module/pathway coverage: Use `taxon_ko_module_coverage`, `taxon_ko_pathway_coverage` for pre-computed analysis
- **KO to metabolic function**: Use ko2pathway, ko2module, ko2reaction for functional mapping

### Quality Control:

- Check **gene_exceptions**, **gene_feature_tags** for quality flags
- Use `taxon` table fields (seq_status, is_obsolete) for genome quality
- Check `delete_genes`, `delete_scaffolds`, `delete_taxons` for historical changes

### Structural Features:

- **RNA genes**: `rna_gene`, `ssu_rrna`, `lsu_rrna`, `trna` (separate from `gene` table)
- **CRISPR**: Use `crispr_array`, `crispr_spacer`, `taxon_crispr_summary`, `taxon_crispr_details`
- **Biosynthetic clusters**: Use `bcg_taxons`, `bc_type`, `actino_cassette`, not just `gene` table

### Performance Optimization:

- **Use taxon_*_count tables** instead of aggregating from genes:
  - `taxon_cog_count` instead of COUNT(DISTINCT cog_id) from gene_cog_groups
  - `taxon_ko_count` instead of COUNT(DISTINCT ko_id) from gene_ko_terms
  - Similar for pfam, go, interpro, tigrfam, etc.
- **Pre-computed statistics**: `dt_phylo_taxon_stats`, `dt_phylum_dist_stats`, `taxon_stats`
- **Filter early**: Apply WHERE clauses before JOINs
- **Select specific columns**: Avoid SELECT * on wide tables

### Taxonomic Scope:

- Use **taxon table** for organism classification and filtering
- **Metagenome genes** lack full taxonomy (no genus/species)
- **asv5_taxons** filters to Archaea, Eukarya, Viruses (if needed)

### Cross-Database Consistency:

- **External links** must be joined separately: gene_ext_links, compound_ext_links, etc.
- **Alternative names**: Use gene_aliases for old locus tags
- **KO format**: Always use 'K' prefix (e.g., 'K00001'), not numbers alone
- **EC format**: Use full EC number format (e.g., '1.1.1.1')
