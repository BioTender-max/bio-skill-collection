# Literature Deep Research - Complete Tool Reference

**All tool names for literature search + annotation databases used in enhanced research strategy.**

---

## Literature Search Tools (18)

### Biomedical & Life Sciences
```python
'PubMed_search_articles'          # 35M+ papers - primary biomedical
'PMC_search_papers'               # Full-text biomedical archive (NIH)
'EuropePMC_search_articles'       # 42M+ European biomedical (use source='PPR' for preprints)
'BioRxiv_get_preprint'            # Get bioRxiv preprint by DOI (not search)
'MedRxiv_get_preprint'            # Get medRxiv preprint by DOI (not search)
```

### Computer Science
```python
'DBLP_search_publications'        # 6M+ CS publications
'ArXiv_search_papers'             # Physics/CS/math preprints
'SemanticScholar_search_papers'   # 200M+ AI-ranked papers
```

### General Academic
```python
'openalex_literature_search'      # 250M+ works across fields
'Crossref_search_works'           # 140M+ DOI registry
'Fatcat_search_scholar'           # Internet Archive
'DOAJ_search_articles'            # Open access journals
```

### Regional/Specialized
```python
'OpenAIRE_search_publications'    # EU-funded research
'HAL_search_archive'              # French national archive
'OSF_search_preprints'            # Social science preprints
'Zenodo_search_records'           # Datasets, software, publications
```

---

## Citation & Metadata Tools (7)

### PubMed Citation Tools
```python
'PubMed_get_article'              # Complete metadata for PMID
'PubMed_get_cited_by'             # Forward citations (papers citing this)
'PubMed_get_related'              # Computationally related papers
'PubMed_get_links'                # External links (full-text)
```

### Europe PMC Citation Tools (Fallbacks)
```python
'EuropePMC_get_citations'         # Forward citations (fallback for PubMed)
'EuropePMC_get_references'        # Backward citations (reference list)
```

### Open Access
```python
'Unpaywall_check_oa_status'       # OA status by DOI (requires email)
```

---

## Protein/Gene Annotation Tools (NEW in v5.0)

### UniProt Tools
```python
'UniProt_search'                  # Search UniProt by query
'UniProt_get_entry_by_accession'  # Full protein entry
'UniProt_id_mapping'              # Map between ID types
'UniProt_get_function_by_accession'  # Function description
'UniProt_get_sequence_by_accession'  # Protein sequence
'UniProt_get_recommended_name_by_accession'  # Official name
'UniProt_get_alternative_names_by_accession'  # Aliases
'UniProt_get_subcellular_location_by_accession'  # Localization
'UniProt_get_ptm_processing_by_accession'  # PTMs, active sites
'UniProt_get_disease_variants_by_accession'  # Disease variants
```

### Domain/Structure Tools
```python
'InterPro_get_protein_domains'    # Domain architecture
'alphafold_get_prediction'        # AlphaFold structure
'get_protein_metadata_by_pdb_id'  # PDB structure metadata
'proteins_api_get_protein'        # Alternative protein data
```

### Gene Annotation
```python
'MyGene_get_gene_annotation'      # NCBI gene info, aliases
'ensembl_lookup_gene'             # Ensembl gene details
'ensembl_get_xrefs'               # Cross-references
```

---

## Expression Tools (NEW in v5.0)

### GTEx (Tissue Expression)
```python
'GTEx_get_gene_expression'        # Expression data
'GTEx_get_median_gene_expression' # Median TPM by tissue
```

### Human Protein Atlas
```python
'HPA_get_comprehensive_gene_details_by_ensembl_id'  # Full HPA data
'HPA_get_rna_expression_by_source'  # RNA expression
'HPA_get_subcellular_location'    # Subcellular localization
'HPA_get_protein_interactions_by_gene'  # Interactions
'HPA_get_cancer_prognostics_by_gene'  # Cancer prognosis
```

### Single-Cell (if available)
```python
'CELLxGENE_get_expression_data'   # Single-cell expression
```

---

## Pathway & Function Tools (NEW in v5.0)

### Gene Ontology
```python
'GO_get_annotations_for_gene'     # GO terms (BP, MF, CC)
'GO_get_term_details'             # GO term details
```

### Pathways
```python
'Reactome_map_uniprot_to_pathways'  # Reactome pathways
'kegg_get_gene_info'              # KEGG gene/pathways
'WikiPathways_search'             # WikiPathways
```

### Open Targets
```python
'OpenTargets_get_target_gene_ontology_by_ensemblID'  # GO via OT
'OpenTargets_get_target_tractability_by_ensemblID'   # Druggability
'OpenTargets_get_associated_drugs_by_target_ensemblID'  # Known drugs
'OpenTargets_get_target_safety_profile_by_ensemblID'   # Safety
'OpenTargets_get_diseases_phenotypes_by_target_ensembl'  # Disease links
'OpenTargets_get_publications_by_target_ensemblID'   # Publications
```

---

## Interaction Tools

```python
'STRING_get_protein_interactions'  # STRING PPI network
'intact_get_interactions'         # IntAct experimental PPIs
'intact_get_complex_details'      # Complex membership
'OpenTargets_get_target_interactions_by_ensemblID'  # OT interactions
```

---

## Variant & Disease Tools

### gnomAD
```python
'gnomad_get_gene'                 # Population variants
'gnomad_get_gene_constraints'     # Constraint scores (pLI, LOEUF)
```

### ClinVar
```python
'clinvar_search_variants'         # Clinical variants
'clinvar_get_variant_by_id'       # Variant details
```

### Disease
```python
'OpenTargets_get_diseases_phenotypes_by_target_ensembl'  # Disease associations
'DGIdb_get_drug_gene_interactions'  # Drug-gene
'DGIdb_get_gene_druggability'     # Druggability categories
```

---

## Tool Categories by Use Case

### Target Disambiguation (Phase 1)
```python
# Resolve IDs
'UniProt_search'
'UniProt_id_mapping'
'ensembl_lookup_gene'

# Get baseline profile
'InterPro_get_protein_domains'
'HPA_get_subcellular_location'
'GTEx_get_median_gene_expression'
'GO_get_annotations_for_gene'
'Reactome_map_uniprot_to_pathways'
```

### High-Precision Literature Seeds
```python
'PubMed_search_articles'          # "[GENE]"[Title] queries
'EuropePMC_search_articles'       # Alternative
```

### Citation Network Expansion
```python
'PubMed_get_cited_by'             # Forward citations (primary)
'EuropePMC_get_citations'         # Forward (fallback)
'PubMed_get_related'              # Related papers
'EuropePMC_get_references'        # Backward citations
```

### Broad Search
```python
'openalex_literature_search'      # Comprehensive
'Crossref_search_works'           # DOI-based
'SemanticScholar_search_papers'   # AI-ranked
```

### OA Status Check
```python
'Unpaywall_check_oa_status'       # If email provided
# Otherwise use OA fields from:
# - EuropePMC (isOpenAccess)
# - OpenAlex (is_oa)
# - PMC papers (all OA)
```

---

## Fallback Chains

| Primary Tool | Fallback 1 | Fallback 2 |
|--------------|------------|------------|
| `PubMed_get_cited_by` | `EuropePMC_get_citations` | OpenAlex citations |
| `PubMed_get_related` | `SemanticScholar_search_papers` | Keyword search |
| `GTEx_get_median_gene_expression` | `HPA_get_rna_expression_by_source` | Mark unavailable |
| `InterPro_get_protein_domains` | UniProt features | Mark unavailable |
| `Unpaywall_check_oa_status` | EuropePMC OA flag | OpenAlex is_oa |

---

## Parameter Quick Reference

### Literature Search
```python
# PubMed
{'query': '"GENE"[Title]', 'limit': 100}

# OpenAlex
{'search_keywords': 'term', 'max_results': 100, 'year_from': 2020}

# With collision filter
{'query': '"TRAG" AND immune NOT plasmid NOT conjugation', 'limit': 50}
```

### Citation Tools
```python
{'pmid': '12345678', 'limit': 100}  # PubMed citations
{'article_id': 'MED:12345678', 'source': 'MED'}  # EuropePMC
```

### Annotation Tools
```python
# UniProt
{'accession': 'P38606'}
{'ids': ['P38606'], 'from_db': 'UniProtKB_AC-ID', 'to_db': 'Ensembl'}

# GTEx
{'gencode_id': 'ENSG00000114573', 'tissue': 'all'}

# InterPro
{'uniprot_accession': 'P38606'}
```

---

## Complete Alphabetical Tool List

### Literature (18)
1. `ArXiv_search_papers`
2. `BioRxiv_get_preprint` (DOI retrieval)
3. `Crossref_search_works`
4. `DBLP_search_publications`
5. `DOAJ_search_articles`
6. `EuropePMC_search_articles`
7. `Fatcat_search_scholar`
8. `HAL_search_archive`
9. `MedRxiv_get_preprint` (DOI retrieval)
10. `OpenAIRE_search_publications`
11. `OSF_search_preprints`
12. `PMC_search_papers`
13. `PubMed_search_articles`
14. `SemanticScholar_search_papers`
15. `Zenodo_search_records`
16. `openalex_literature_search`
17. `openalex_search_works`
18. `PubTator_search_entities`

### Citation (7)
19. `EuropePMC_get_citations`
20. `EuropePMC_get_references`
21. `PubMed_get_article`
22. `PubMed_get_cited_by`
23. `PubMed_get_links`
24. `PubMed_get_related`
25. `Unpaywall_check_oa_status`

### Protein/Gene (15)
26. `InterPro_get_protein_domains`
27. `MyGene_get_gene_annotation`
28. `UniProt_get_alternative_names_by_accession`
29. `UniProt_get_disease_variants_by_accession`
30. `UniProt_get_entry_by_accession`
31. `UniProt_get_function_by_accession`
32. `UniProt_get_ptm_processing_by_accession`
33. `UniProt_get_recommended_name_by_accession`
34. `UniProt_get_sequence_by_accession`
35. `UniProt_get_subcellular_location_by_accession`
36. `UniProt_id_mapping`
37. `UniProt_search`
38. `alphafold_get_prediction`
39. `ensembl_lookup_gene`
40. `proteins_api_get_protein`

### Expression (6)
41. `CELLxGENE_get_expression_data`
42. `GTEx_get_gene_expression`
43. `GTEx_get_median_gene_expression`
44. `HPA_get_comprehensive_gene_details_by_ensembl_id`
45. `HPA_get_rna_expression_by_source`
46. `HPA_get_subcellular_location`

### Pathway/Function (8)
47. `GO_get_annotations_for_gene`
48. `Reactome_map_uniprot_to_pathways`
49. `WikiPathways_search`
50. `kegg_get_gene_info`
51. `OpenTargets_get_target_gene_ontology_by_ensemblID`
52. `OpenTargets_get_target_tractability_by_ensemblID`
53. `OpenTargets_get_associated_drugs_by_target_ensemblID`
54. `OpenTargets_get_publications_by_target_ensemblID`

### Interaction (4)
55. `STRING_get_protein_interactions`
56. `intact_get_interactions`
57. `intact_get_complex_details`
58. `OpenTargets_get_target_interactions_by_ensemblID`

### Variant/Disease (8)
59. `clinvar_search_variants`
60. `gnomad_get_gene`
61. `gnomad_get_gene_constraints`
62. `OpenTargets_get_diseases_phenotypes_by_target_ensembl`
63. `OpenTargets_get_target_safety_profile_by_ensemblID`
64. `DGIdb_get_drug_gene_interactions`
65. `DGIdb_get_gene_druggability`
66. `HPA_get_cancer_prognostics_by_gene`

---

**Total Tools**: 66
- Literature: 18
- Citation: 7
- Protein/Gene Annotation: 15
- Expression: 6
- Pathway/Function: 8
- Interaction: 4
- Variant/Disease: 8

*Last Updated: 2026-02-04 (v5.0 - Added annotation tools)*
