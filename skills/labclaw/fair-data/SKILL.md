# FAIR Data Principles — Findable, Accessible, Interoperable, Reusable

## Overview
Guidelines for making scientific data FAIR: Findable, Accessible, Interoperable, and Reusable.

## Findable
- Assign globally unique persistent identifiers (DOIs) to datasets
- Rich metadata describing the dataset (title, authors, description, keywords, dates)
- Metadata registered in searchable resources (DataCite, re3data, FAIRsharing)
- Data indexed in domain-specific repositories

## Accessible
- Data retrievable by identifier using standardized protocol (HTTP, FTP)
- Metadata accessible even if data is restricted
- Authentication/authorization where necessary, clearly documented
- Long-term preservation plan (minimum 10 years for funded research)

## Interoperable
- Use formal, shared vocabularies (ontologies: GO, ChEBI, EFO, MeSH)
- Standard file formats (CSV, JSON, HDF5, NetCDF — not proprietary)
- Include references to related datasets and publications
- Machine-readable metadata (JSON-LD, Dublin Core, schema.org)

## Reusable
- Clear data usage license (CC-BY, CC0 recommended for scientific data)
- Detailed provenance (how data was collected, processed, quality controlled)
- Meet community standards (MIAME for microarrays, MINSEQE for sequencing)
- Version control for datasets that evolve

## Recommended Repositories
| Domain | Repository |
|--------|-----------|
| General | Zenodo, Figshare, Dryad |
| Genomics | GEO, SRA, ENA |
| Proteomics | PRIDE, MassIVE |
| Structures | PDB, EMDB |
| Clinical | ClinicalTrials.gov, YODA |
| Chemistry | ChEMBL, PubChem |
| Materials | NOMAD, Materials Cloud |
