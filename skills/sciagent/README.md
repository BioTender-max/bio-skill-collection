# 🔭 SciAgent Skills

[![Skills](https://img.shields.io/badge/Skills-151-00d4aa?style=flat-square&logo=databricks&logoColor=white)](https://github.com/jaechang-hits/SciAgent-Skills)
[![Source](https://img.shields.io/badge/Source-jaechang-hits%2FSciAgent-Skills-0079d3?style=flat-square&logo=github&logoColor=white)](https://github.com/jaechang-hits/SciAgent-Skills)

> 面向科研 Agent 的技能集 · Skills for scientific research agents
> `Biostatistics · Database access · Clinical decision support`

---

## Skills List

| 文件夹 · Folder | 技能名称 · Skill | 描述 · Description |
|-----------------|-----------------|-------------------|
| `adaptyv-bio` | **"adaptyv-bio"** | API + Python SDK for ordering cell-free protein expression and binding assays. Submit sequences for expression (10–100 µg), measure binding affinit... |
| `alphafold-database-access` | **alphafold-database-access** |  |
| `anndata-data-structure` | **anndata-data-structure** | Annotated matrices for single-cell genomics. Stores X with obs/var metadata, layers, embeddings (obsm/varm), graphs (obsp/varp), uns. Use for .h5ad... |
| `arboreto-grn-inference` | **"arboreto-grn-inference"** | GRN inference from expression via GRNBoost2 (gradient boosting) or GENIE3 (Random Forest). Load matrix, filter by TFs, infer TF-target-importance l... |
| `archs4-database` | **"archs4-database"** | Query ARCHS4 REST API for uniformly processed RNA-seq expression, tissue patterns, co-expression across 1M+ human/mouse samples. Retrieve z-scores,... |
| `astropy-astronomy` | **astropy-astronomy** | Core Python library for astronomy/astrophysics: units with dimensional analysis, celestial coordinate transforms (ICRS/Galactic/AltAz/FK5), FITS I/... |
| `autodock-vina-docking` | **"autodock-vina-docking"** | Molecular docking with AutoDock Vina (Python API). Receptor/ligand prep (Meeko + RDKit), grid box, docking, pose and binding energy analysis, and b... |
| `bakta-genome-annotation` | **"bakta-genome-annotation"** | Annotate bacterial and archaeal genomes and plasmids with Bakta's Prodigal/HMM/diamond pipeline. Identifies CDS, ncRNA, tRNA, rRNA, tmRNA, sORFs, C... |
| `bcftools-variant-manipulation` | **"bcftools-variant-manipulation"** | CLI for VCF/BCF: filter, merge, annotate, query, normalize, compute stats. Core post-variant-calling: quality filtering, multi-sample merging, rsID... |
| `bedtools-genomic-intervals` | **"bedtools-genomic-intervals"** | Genomic interval ops on BED/BAM/GFF/VCF. Find overlaps, merge intervals, compute coverage, extract FASTA, find nearest features. Core for ChIP-seq ... |
| `biopython-molecular-biology` | **"biopython-molecular-biology"** | Molecular biology toolkit: sequence manipulation, FASTA/GenBank/PDB I/O, NCBI Entrez, BLAST automation, pairwise/MSA alignment, Bio.PDB, phylogenet... |
| `biopython-sequence-analysis` | **"biopython-sequence-analysis"** | Biopython sequence analysis: parse FASTA/FASTQ/GenBank/GFF (SeqIO), NCBI Entrez (esearch/efetch/elink), remote/local BLAST, pairwise/MSA alignment ... |
| `biorxiv-database` | **"biorxiv-database"** | Query bioRxiv/medRxiv preprints via REST API. Search by DOI, category, or date range; retrieve metadata (title, abstract, authors, category, DOI, v... |
| `bioservices-multi-database` | **bioservices-multi-database** |  |
| `brenda-database` | **"brenda-database"** | BRENDA Enzyme DB SOAP/REST queries: kinetic parameters (Km, Vmax, kcat, Ki), EC classes, substrate specificity, inhibitors, cofactors, organism dat... |
| `busco-status-interpretation` | **busco-status-interpretation** | Guide to interpreting BUSCO completeness statuses: why Duplicated BUSCOs count as complete, parsing output files, computing/comparing completeness ... |
| `bwa-mem2-dna-aligner` | **"bwa-mem2-dna-aligner"** | Fast short-read DNA aligner for WGS/WES/ChIP-seq. 2× faster BWA-MEM successor; outputs SAM/BAM with read group headers for GATK. Primary plus suppl... |
| `cancer-research-figure-guide` | **cancer-research-figure-guide** | Cancer Research (AACR) figures: resolution (300-1200 DPI), formats (EPS/TIFF/AI), hierarchical panel labels (Ai, Aii, Bi), figure/table limits, leg... |
| `cbioportal-database` | **"cbioportal-database"** | Cancer genomics (TCGA et al.) via cBioPortal REST API. Retrieve somatic mutations, CNAs, expression, clinical data (survival/stage/treatment) acros... |
| `cell-figure-guide` | **cell-figure-guide** | Cell (Cell Press) figure preparation: resolution (300-1000 DPI), formats (TIFF/PDF), RGB color, Avenir/Arial fonts, uppercase panel labels, strict ... |
| `cellchat-cell-communication` | **"cellchat-cell-communication"** | Infer and visualize intercellular communication from scRNA-seq with CellChat (R). Build CellChat from Seurat/counts → subset CellChatDB ligand-rece... |
| `cellpose-cell-segmentation` | **"cellpose-cell-segmentation"** | DL cell/nucleus segmentation for fluorescence and brightfield microscopy. Pre-trained models (cyto3, nuclei, tissuenet) and a generalist flow-based... |
| `celltypist-cell-annotation` | **"celltypist-cell-annotation"** | Automated scRNA-seq cell type annotation via pre-trained logistic regression. 45+ models: immune, gut, lung, brain, fetal, cancer microenvironments... |
| `chembl-database-bioactivity` | **chembl-database-bioactivity** | Query ChEMBL (2M+ compounds, 19M+ bioactivity measurements, 13K+ targets) via the public REST/JSON API with plain `requests` — no SDK install requi... |
| `clinical-decision-support-documents` | **clinical-decision-support-documents** | Guidelines for clinical decision support (CDS) documents: biomarker-stratified cohort analyses and GRADE-graded treatment reports. Covers structure... |
| `clinicaltrials-database-search` | **clinicaltrials-database-search** | Query ClinicalTrials.gov API v2 for trial data. Search by condition, drug/intervention, location, sponsor, or phase; fetch details by NCT ID; filte... |
| `clinpgx-database` | **"clinpgx-database"** | Query the ClinPGx (formerly PharmGKB) REST API plus the CPIC PostgREST companion API for pharmacogenomic clinical annotations, CPIC/DPWG dosing gui... |
| `clinvar-database` | **"clinvar-database"** | Query NCBI ClinVar via E-utilities for variant clinical significance, pathogenicity, disease associations. Search by gene/rsID/condition/review sta... |
| `cnvkit-copy-number` | **"cnvkit-copy-number"** | Detect somatic CNVs from WES/WGS/targeted BAMs (CNVkit v0.9.x). Bin coverage in target/antitarget regions, normalize vs reference, segment with CBS... |
| `cobrapy-metabolic-modeling` | **cobrapy-metabolic-modeling** | Constraint-based (COBRA) analysis of genome-scale metabolic models: FBA, FVA, knockouts, flux sampling, production envelopes, gapfilling, media opt... |
| `cosmic-database` | **"cosmic-database"** | Query COSMIC for cancer somatic mutations, gene census, mutational signatures, drug resistance variants. REST API v3.1 supports gene/sample/variant... |
| `dailymed-database` | **"dailymed-database"** | Query FDA drug labels (DailyMed) via REST API. Search structured product labels (SPLs) by name, NDC, set ID, or RxCUI; get indications, dosage, war... |
| `datamol-cheminformatics` | **datamol-cheminformatics** | - |
| `dbsnp-database` | **"dbsnp-database"** | Query NCBI dbSNP for SNP records by rsID, gene, or region via E-utilities and Variation Services REST API. Retrieve alleles, MAF, variant class (SN... |
| `ddinter-database` | **"ddinter-database"** | Query DDInter drug-drug interactions via REST API (1.7M+ interactions, 2,400+ drugs). Search by drug name/ID for severity (major/moderate/minor), m... |
| `deeptools-ngs-analysis` | **deeptools-ngs-analysis** | NGS CLI for ChIP/RNA/ATAC-seq. BAM→bigWig with RPGC/CPM/RPKM, sample correlation/PCA, heatmaps/profiles around features, fingerprints. For alignmen... |
| `degenerate-input-filtering` | **degenerate-input-filtering** | Filter degenerate, uninformative inputs before statistical tests: single-sequence alignments, empty files, constant features, zero-variance inputs,... |
| `depmap-crispr-essentiality` | **depmap-crispr-essentiality** | DepMap CRISPR gene effect (Chronos) analysis: sign convention for essentiality, per-gene NaN-safe Spearman correlation, data loading/alignment. For... |
| `deseq2-differential-expression` | **"deseq2-differential-expression"** | Bulk RNA-seq DE with R/Bioconductor DESeq2. Negative binomial GLM, empirical Bayes shrinkage, Wald/LRT tests, multi-factor designs, Salmon tximeta ... |
| `drugbank-database-access` | **"drugbank-database-access"** | Parse local DrugBank XML for drug info, interactions, targets, and properties. Search by ID/name/CAS, extract DDIs with severity, map targets/enzym... |
| `emdb-database` | **"emdb-database"** | Look up EMDB cryo-EM density maps and fitted atomic models via the entry REST API + EBI Search WS. Fetch entry metadata (resolution, method, organi... |
| `ena-database` | **ena-database** | ENA REST API for sequences, reads, assemblies, and annotations. Portal API search, Browser API retrieval (XML/FASTA/EMBL), file reports for FASTQ/B... |
| `encode-database` | **"encode-database"** | ENCODE Portal REST API for regulatory genomics: TF ChIP-seq, ATAC-seq/DNase-seq peaks, histone marks, and RNA-seq across 1000+ cell types. Search e... |
| `ensembl-database` | **"ensembl-database"** | Ensembl REST API for gene/transcript/variant annotations in 300+ species. Gene info by symbol/ID, sequence, cross-refs (HGNC, RefSeq, UniProt), reg... |
| `esm-protein-language-model` | **esm-protein-language-model** | Protein language models (ESM3, ESM C) for sequence generation, structure prediction, inverse folding, and embeddings. Design novel proteins, extrac... |
| `fastp-fastq-preprocessing` | **"fastp-fastq-preprocessing"** | All-in-one FASTQ QC and adapter trimming. Auto-detects Illumina adapters, filters low-quality reads, corrects paired-end overlaps, emits HTML+JSON ... |
| `fda-database` | **"fda-database"** | Query openFDA REST API for adverse events (FAERS), labeling, product info, recalls, enforcement. Search by drug name, ingredient, MedDRA, or NDC. 1... |
| `featurecounts-rna-counting` | **"featurecounts-rna-counting"** | Counts RNA-seq reads overlapping GTF gene features. Takes sorted STAR BAMs plus GTF; outputs a per-gene tab-delimited matrix across samples. Handle... |
| `flowio-flow-cytometry` | **flowio-flow-cytometry** | Parse/write FCS (Flow Cytometry) files v2.0-3.1. Events as NumPy, channel metadata, multi-dataset files, CSV/FCS export. Use FlowKit for gating/com... |
| `gatk-variant-calling` | **"gatk-variant-calling"** | GATK Best Practices for germline SNP/indel calling from WGS/WES BAMs. Per-sample HaplotypeCaller GVCFs, GenomicsDBImport, GenotypeGVCFs joint calli... |
| `gene-database` | **"gene-database"** | NCBI Gene via E-utilities: curated records across 1M+ taxa. Official symbols, aliases, RefSeq IDs, summaries, coordinates, GO, interactions. Use fo... |
| `general-figure-guide` | **general-figure-guide** | Universal QA checklist for generated scientific plots: overlapping labels, clipped text, missing axes/legends, overcrowded data, and cross-journal ... |
| `geo-database` | **"geo-database"** | NCBI GEO access via GEOparse and E-utilities. Search by keyword/organism/platform, download GSE series matrices, parse GPL annotations, extract GSM... |
| `geopandas-geospatial` | **geopandas-geospatial** | - |
| `gget-genomic-databases` | **gget-genomic-databases** | Unified CLI/Python interface to 20+ genomic databases. Gene lookups (Ensembl search/info/seq), BLAST/BLAT, AlphaFold, Enrichr enrichment, OpenTarge... |
| `gnomad-database` | **"gnomad-database"** | gnomAD v4 population variant frequencies via GraphQL API. Allele counts and frequencies stratified by ancestry (AFR, AMR, EAS, NFE, SAS, FIN, ASJ, ... |
| `gseapy-gene-enrichment` | **"gseapy-gene-enrichment"** | GSEA and over-representation analysis (ORA) for RNA-seq and proteomics. Wraps Enrichr for ORA against MSigDB, KEGG, GO, and 200+ databases; runs pr... |
| `gtopdb-database` | **"gtopdb-database"** | Query IUPHAR/BPS Guide to Pharmacology (GtoPdb) for receptor-ligand interactions, target/ligand metadata, families, and approved drugs. Affinities ... |
| `gwas-database` | **gwas-database** | NHGRI-EBI GWAS Catalog REST API for SNP-trait associations from published GWAS. Query studies, associations, variants, traits, genes, summary stats... |
| `harmony-batch-correction` | **"harmony-batch-correction"** | Harmony batch correction for scRNA-seq and other omics. Removes batch effects from PCA embeddings while preserving biology. Run after PCA, before U... |
| `histolab-wsi-processing` | **"histolab-wsi-processing"** | WSI processing for digital pathology. Tissue detection, tile extraction (random, grid, score-based), filter pipelines for H&E/IHC. For dataset prep... |
| `hmdb-database` | **"hmdb-database"** | Parse HMDB (Human Metabolome Database) local XML for metabolite info, chemical properties, biological context, disease links, spectra, and cross-DB... |
| `homer-motif-analysis` | **"homer-motif-analysis"** | De novo and known TF motif enrichment in ChIP-seq/ATAC-seq peaks via HOMER. findMotifsGenome.pl finds over-represented patterns vs background; anno... |
| `hypogenic-hypothesis-generation` | **"hypogenic-hypothesis-generation"** | LLM-driven hypothesis generation/testing on tabular data. Three methods: HypoGeniC (data-driven), HypoRefine (literature+data), Union. Iterative re... |
| `interpro-database` | **"interpro-database"** | Query InterPro REST API for protein domain architecture, family classification, and member-DB integration. Search entries, retrieve a protein's dom... |
| `jaspar-database` | **"jaspar-database"** | JASPAR 2024 TF binding profiles via REST API and pyJASPAR. Retrieve PFMs/PWMs by TF name, JASPAR ID, species, or structural class. Scan DNA for TFB... |
| `kegg-database` | **kegg-database** | KEGG REST API (academic only). Pathways, genes, compounds, enzymes, diseases, drugs via 7 ops (info/list/find/get/conv/link/ddi). ID conversion (NC... |
| `kegg-pathway-analysis` | **kegg-pathway-analysis** | Guide to KEGG pathway enrichment for DEG results. Covers ORA vs GSEA, mandatory directionality splitting, KEGG organism codes, API failure handling... |
| `lamindb-data-management` | **lamindb-data-management** | Open-source FAIR biology data framework. Version artifacts (AnnData, DataFrame, Zarr), track lineage, validate via ontologies (Bionty), query datas... |
| `latex-research-posters` | **latex-research-posters** | Research posters in LaTeX using beamerposter, tikzposter, or baposter. Layout, typography, color schemes, figure integration, accessibility, and QA... |
| `libsbml-network-modeling` | **"libsbml-network-modeling"** | Build, read, validate, modify SBML biological network models via the libSBML Python API. SBML Levels 1–3, reactions/kinetic laws, species, rules, F... |
| `macs3-peak-calling` | **"macs3-peak-calling"** | Poisson-model peak caller for ChIP-seq/ATAC-seq BAMs. MACS3 callpeak finds enriched regions (TF sites or histone marks) vs input/IgG; outputs BED n... |
| `matchms-spectral-matching` | **matchms-spectral-matching** | MS spectral matching and metabolite ID with matchms. Import spectra (mzML, MGF, MSP, JSON), filter/normalize peaks, score similarity (cosine, modif... |
| `matplotlib-scientific-plotting` | **"matplotlib-scientific-plotting"** | Low-level Python plotting for scientific figures: publication-quality line, scatter, bar, heatmap, contour, 3D; multi-panel layouts; fine control o... |
| `maxquant-proteomics` | **"maxquant-proteomics"** | MaxQuant + Perseus proteomics pipeline: run MaxQuant for LFQ and SILAC; parse proteinGroups.txt in Python; filter contaminants/decoys; log2 + media... |
| `mdanalysis-trajectory` | **"mdanalysis-trajectory"** | Analyze MD trajectories from GROMACS, AMBER, NAMD, CHARMM, LAMMPS. Reads topology/trajectory into Universe objects; supports RMSD, RMSF, radius of ... |
| `metabolomics-workbench-database` | **"metabolomics-workbench-database"** | Query Metabolomics Workbench REST API (4,200+ NIH studies) for metabolite ID, study discovery, RefMet standardization, m/z precursor searches, and ... |
| `mofaplus-multi-omics` | **"mofaplus-multi-omics"** | Multi-Omics Factor Analysis v2 (MOFA+) with mofapy2. Jointly decompose omics layers (scRNA, ATAC, proteomics, methylation) into latent factors capt... |
| `molfeat-molecular-featurization` | **molfeat-molecular-featurization** | Molecular featurization hub (100+ featurizers) for ML. SMILES to fingerprints (ECFP, MACCS, MAP4), descriptors (RDKit 2D, Mordred), pretrained embe... |
| `monarch-database` | **"monarch-database"** | Monarch Initiative knowledge graph REST API for disease-gene-phenotype associations and cross-species orthology. MONDO disease-to-gene/phenotype, H... |
| `mouse-phenome-database` | **"mouse-phenome-database"** | Retrieve mouse phenotype data from the Jackson Laboratory Mouse Phenome Database (MPD) via its REST API. Browse 520+ projects, look up per-project ... |
| `multiqc-qc-reports` | **"multiqc-qc-reports"** | Aggregates QC from 150+ bioinformatics tools into one interactive HTML report. Scans FastQC, samtools, STAR, HISAT2, Trim Galore, featureCounts, Ka... |
| `muon-multiomics-singlecell` | **"muon-multiomics-singlecell"** | Multi-modal single-cell analysis with muon/MuData. Joint RNA+ATAC (10x Multiome), CITE-seq (RNA+protein), other multi-omics. MuData holds per-modal... |
| `nan-safe-correlation` | **nan-safe-correlation** | Per-feature NaN-safe Spearman/Pearson correlation across many features (genes, proteins, variants) with missing values. Covers why bulk matrix shor... |
| `napari-image-viewer` | **"napari-image-viewer"** | Interactive viewer for microscopy. Displays 2D/3D/4D arrays as Image, Labels, Points, Shapes, Tracks layers; supports annotation, plugin analysis, ... |
| `networkx-graph-analysis` | **"networkx-graph-analysis"** | Graph and network analysis toolkit. Four graph types (directed, undirected, multi-edge), centrality, shortest paths, community detection, generator... |
| `nextflow-workflow-engine` | **"nextflow-workflow-engine"** | Dataflow workflow engine for scalable bioinformatics pipelines. Defines processes (containerized tasks) connected by channels; runs local, HPC (SLU... |
| `nnunet-segmentation` | **"nnunet-segmentation"** | Medical image segmentation with nnU-Net's self-configuring framework — auto-selects architecture, preprocessing, training for any modality. CT, MRI... |
| `omics-analysis-guide` | **omics-analysis-guide** | Three-tiered approach to omics data analysis (transcriptomics, proteomics) covering validated pipelines, standard workflows, and custom methods |
| `openalex-database` | **"openalex-database"** | Query OpenAlex REST API for 250M+ scholarly works, authors, institutions, journals, concepts. Search by keyword, author, DOI, ORCID, or ID; filter ... |
| `opencv-bioimage-analysis` | **"opencv-bioimage-analysis"** | Computer vision for bio-image preprocessing, feature detection, real-time microscopy. Color conversion, morphology, contour/blob detection, templat... |
| `opentargets-database` | **"opentargets-database"** | Query Open Targets GraphQL API for target-disease associations, evidence, drug links, safety. Search targets by gene, diseases by EFO ID; scores fr... |
| `pdb-database` | **"pdb-database"** | Query RCSB PDB (200K+ structures) via the public REST + GraphQL APIs with plain `requests` (no SDK). Search by text, attribute, sequence, or 3D str... |
| `peer-review-methodology` | **peer-review-methodology** | Structured peer review of manuscripts and grants. 7-stage evaluation: initial assessment, section review, statistical rigor, reproducibility, figur... |
| `plannotate-plasmid-annotation` | **"plannotate-plasmid-annotation"** | Auto-annotate plasmids with features (promoters, terminators, resistance, origins, tags, fluorescent proteins) via BLAST against curated DBs (Addge... |
| `plink2-gwas-analysis` | **"plink2-gwas-analysis"** | GWAS and population genetics tool. Processes PLINK (.bed/.bim/.fam), VCF, and BGEN; runs QC (MAF, HWE, missingness), IBD estimation, PCA, and linea... |
| `plotly-interactive-plots` | **"plotly-interactive-plots"** | Interactive scientific visualization with Plotly. Two APIs: plotly.express (px) for one-liner DataFrame plots, plotly.graph_objects (go) for trace-... |
| `plotly-interactive-visualization` | **plotly-interactive-visualization** | Interactive visualization with Plotly. 40+ chart types (scatter, line, heatmap, 3D, geographic) with hover, zoom, pan. Two APIs: Plotly Express (Da... |
| `popv-cell-annotation` | **"popv-cell-annotation"** | Consensus cell type annotation: runs 10+ algorithms (KNN-Harmony/BBKNN/Scanorama/scVI, CellTypist, ONCLASS, Random Forest, SCANVI, SVM, XGBoost) on... |
| `pride-database` | **"pride-database"** | Search the PRIDE Archive v3 REST API for proteomics datasets: discover projects by keyword + faceted filters (organism, instrument, disease, softwa... |
| `prokka-genome-annotation` | **"prokka-genome-annotation"** | Annotate prokaryotic genomes (bacteria, archaea, viruses) via Prokka's BLAST/HMM pipeline. Identifies CDS, rRNA, tRNA, tmRNA, signal peptides again... |
| `protocolsio-integration` | **"protocolsio-integration"** | protocols.io REST API: search and fetch wet-lab, bioinformatics, and clinical protocols by keyword, DOI, or category, with steps, reagents, materia... |
| `pubchem-compound-search` | **"pubchem-compound-search"** | Query PubChem (110M+ compounds) directly via the PUG-REST/JSON API with plain `requests` — no SDK install required. Search by name/CID/SMILES/InChI... |
| `pubmed-database` | **pubmed-database** | - |
| `pydeseq2-differential-expression` | **"pydeseq2-differential-expression"** | Bulk RNA-seq DE with PyDESeq2: load counts, normalize, fit negative binomial models, Wald test (BH-FDR), LFC shrinkage, volcano/MA plots. Use for t... |
| `pydicom-medical-imaging` | **"pydicom-medical-imaging"** | Pure Python DICOM for medical imaging (CT, MRI, X-ray, ultrasound). Read/write DICOM, pixels as NumPy, edit tags, windowing (VOI LUT), PHI anonymiz... |
| `pyimagej-fiji-bridge` | **"pyimagej-fiji-bridge"** | Python bridge to ImageJ2/Fiji for macros, plugins (Bio-Formats, TrackMate, Analyze Particles), NumPy↔ImagePlus/ImgLib2 exchange, and ImageJ Ops. Au... |
| `pymc-bayesian-modeling` | **"pymc-bayesian-modeling"** | Bayesian modeling with PyMC 5: priors, likelihood, NUTS/ADVI sampling, diagnostics (R-hat, ESS), LOO/WAIC comparison, prediction. Hierarchical, log... |
| `pymoo` | **"pymoo"** | Python framework for single- and multi-objective optimization with evolutionary algorithms. Define vectorized objectives and constraints; solve wit... |
| `pyopenms-mass-spectrometry` | **pyopenms-mass-spectrometry** | MS data processing with PyOpenMS for LC-MS/MS proteomics and metabolomics — mzML/mzXML I/O, signal processing (smoothing, peak picking, centroiding... |
| `pysam-genomic-files` | **pysam-genomic-files** | Read/write SAM/BAM/CRAM, VCF/BCF, FASTA/FASTQ. Region queries, pileup, variant filtering, read groups. Python htslib wrapper exposing samtools/bcft... |
| `pytdc-therapeutics-data-commons` | **pytdc-therapeutics-data-commons** |  |
| `quickgo-database` | **"quickgo-database"** | Query EBI QuickGO REST API for GO terms and protein annotations. Fetch term metadata by ID, search by keyword, walk ancestor/descendant hierarchies... |
| `rdkit-cheminformatics` | **"rdkit-cheminformatics"** | Cheminformatics toolkit for molecular analysis and virtual screening: SMILES/SDF parsing, descriptors (MW, LogP, TPSA), fingerprints (Morgan/ECFP, ... |
| `reactome-database` | **reactome-database** | Query Reactome pathways via REST: pathway queries, entity lookup, keyword search, gene list enrichment, hierarchy, cross-refs. Content + Analysis s... |
| `regulomedb-database` | **"regulomedb-database"** | Query RegulomeDB v2 GET REST API to score variants for regulatory function and retrieve overlapping evidence (TF binding, histone marks, DNase peak... |
| `remap-database` | **"remap-database"** | Query ReMap 2022 TF ChIP-seq peak database via REST API and BED downloads. Retrieve TF peaks overlapping a region (chr:start-end), peaks near a gen... |
| `roary-pangenome` | **"roary-pangenome"** | Compute the bacterial pan-genome from Prokka/Bakta GFF3 annotations with Roary's CD-HIT + BLAST + MCL clustering pipeline. Builds gene presence/abs... |
| `salmon-rna-quantification` | **"salmon-rna-quantification"** | Ultra-fast RNA-seq transcript/gene quantification via quasi-mapping (no BAM). Builds a k-mer index from transcriptome FASTA, quantifies in minutes.... |
| `samtools-bam-processing` | **"samtools-bam-processing"** | CLI toolkit for SAM/BAM/CRAM: sort, index, convert, filter, QC alignments. Core commands: view, sort, index, flagstat, stats, depth, markdup, merge... |
| `sar-analysis` | **sar-analysis** | Structure-activity relationship (SAR) analysis guide for drug discovery including molecular descriptor analysis, scaffold analysis, and activity cl... |
| `scanpy-scrna-seq` | **"scanpy-scrna-seq"** | scRNA-seq with Scanpy: QC, normalization, HVG selection, PCA, neighborhood graph, UMAP/t-SNE, Leiden clustering, markers, cell annotation, trajecto... |
| `scientific-critical-thinking` | **"scientific-critical-thinking"** | Evaluating scientific evidence and claims. Covers study design hierarchy (RCT to expert opinion), effect sizes (OR, RR, NNT, Cohen's d), confoundin... |
| `scientific-literature-search` | **scientific-literature-search** | Systematic strategies for searching scientific literature across PubMed, arXiv, Google Scholar, and AI-assisted tools. Covers PICO framework for cl... |
| `scikit-image-processing` | **"scikit-image-processing"** | Python image processing for microscopy and bioimage analysis. Read/write images, filter (Gaussian, median, LoG), segment (thresholding, watershed, ... |
| `scikit-learn-machine-learning` | **"scikit-learn-machine-learning"** | Classical ML in Python: classification, regression, clustering, dim reduction, evaluation, tuning, preprocessing pipelines. Linear models, tree ens... |
| `scikit-survival-analysis` | **scikit-survival-analysis** | Time-to-event modeling with scikit-survival: Cox PH (elastic net), Random Survival Forests, Boosting, SVMs for censored data. C-index, Brier, time-... |
| `scvi-tools-single-cell` | **"scvi-tools-single-cell"** | Deep generative models for single-cell omics: probabilistic batch correction (scVI), semi-supervised annotation (scANVI), CITE-seq RNA+protein (tot... |
| `sgrna-design-guide` | **sgrna-design-guide** | Three-tiered sgRNA design guide using validated Addgene sequences, CRISPick pre-computed datasets, or de novo design rules for CRISPR experiments |
| `shap-model-explainability` | **shap-model-explainability** | - |
| `simpleitk-image-registration` | **"simpleitk-image-registration"** | Register, segment, filter, resample 3D medical images (MRI, CT, microscopy) via SimpleITK Python; DICOM, NIfTI, multi-modal. Rigid/affine/deformabl... |
| `simpy-discrete-event-simulation` | **simpy-discrete-event-simulation** | Process-based discrete-event simulation. Model queues, shared resources, timed events: manufacturing, service ops, network traffic, logistics. Proc... |
| `single-cell-annotation` | **single-cell-annotation** | Best practices for single-cell RNA-seq cell type annotation including marker-based, reference-based, and automated classification approaches. |
| `single-cell-annotation-guide` | **"single-cell-annotation-guide"** | Decision framework for manual marker-based, automated (CellTypist), and reference-based (popV) cell type annotation in scRNA-seq. Three-tier strate... |
| `snpeff-variant-annotation` | **"snpeff-variant-annotation"** | Annotate and filter VCF variants with SnpEff and SnpSift. SnpEff predicts functional effects (HIGH/MODERATE/LOW/MODIFIER), genes, transcripts, AA c... |
| `spikeinterface-electrophysiology` | **"spikeinterface-electrophysiology"** | Unified Python framework for extracellular electrophysiology. Load 20+ formats (SpikeGLX, OpenEphys, NWB, Intan, Maxwell, Blackrock), preprocess, r... |
| `star-rna-seq-aligner` | **"star-rna-seq-aligner"** | Splice-aware RNA-seq aligner producing sorted BAM and splice junction tables. Builds genome index, runs two-pass alignment for better junctions. Ou... |
| `statistical-analysis` | **statistical-analysis** | - |
| `statistical-significance-annotation` | **"statistical-significance-annotation"** | Guide for annotating statistical significance (p-value asterisks) on comparison plots. Covers standard notation (ns, *, **, ***, ****), matplotlib ... |
| `statsmodels-statistical-modeling` | **"statsmodels-statistical-modeling"** | Python statistical modeling: regression (OLS, WLS, GLM), discrete (Logit, Poisson, NegBin), time series (ARIMA, SARIMAX, VAR), with rigorous infere... |
| `string-database-ppi` | **string-database-ppi** | Query STRING REST API for PPIs (59M proteins, 20B interactions, 5000+ species). Retrieve networks, run GO/KEGG enrichment, find partners, test PPI ... |
| `torch-geometric-graph-neural-networks` | **torch-geometric-graph-neural-networks** | PyTorch Geometric (PyG) for graph neural networks: node/graph classification, link prediction with GCN, GAT, GraphSAGE, GIN. Message passing, mini-... |
| `trackpy-particle-tracking` | **"trackpy-particle-tracking"** | Python library for single-particle tracking (SPT) in video microscopy via the Crocker-Grier algorithm. Locate particles (fluorescent spots, colloid... |
| `transformers-bio-nlp` | **"transformers-bio-nlp"** | HuggingFace Transformers with biomedical LMs (BioBERT, PubMedBERT, BioGPT, BioMedLM) for scientific NLP: NER (genes, diseases, chemicals), relation... |
| `ucsc-genome-browser` | **"ucsc-genome-browser"** | Query UCSC Genome Browser REST API for DNA sequences, tracks, gene models, and conservation across 100+ assemblies. Retrieve sequence by region, li... |
| `unichem-database` | **"unichem-database"** | Cross-reference compound IDs across 20+ databases (ChEMBL, DrugBank, PubChem, ChEBI, PDB, SureChEMBL, HMDB, DrugCentral, BindingDB) via UniChem RES... |
| `uniprot-protein-database` | **uniprot-protein-database** | Query UniProt REST API: search by gene/protein name, fetch FASTA, map IDs (Ensembl, PDB, RefSeq), access Swiss-Prot annotations. Use bioservices fo... |
| `uspto-database` | **"uspto-database"** | Access USPTO patent data via PatentsView REST API and Google Patents Public Data (BigQuery). Search by inventor, assignee, CPC, or keywords; downlo... |
| `vcf-variant-filtering` | **vcf-variant-filtering** | Guide to quality filtering raw VCF files before computing summary stats (Ts/Tv ratio, variant counts, AF distributions). Covers detecting raw VCFs ... |
| `viennarna-structure-prediction` | **"viennarna-structure-prediction"** | Predict RNA secondary structure, MFE folding, base-pair probabilities, RNA-RNA interactions via ViennaRNA Python bindings. Pipeline: sequence → MFE... |
| `zinc-database` | **"zinc-database"** | Query ZINC15/ZINC22 virtual compound libraries (1.4B compounds, 750M purchasable). Search lead/fragment/drug-like compounds by MW, logP, reactivity... |

---
*151 skills · Source: [jaechang-hits/SciAgent-Skills](https://github.com/jaechang-hits/SciAgent-Skills)*
