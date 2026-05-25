# IMG and GOLD Terms Glossary

Reference for terminology used across the IMG and GOLD databases.
Source: https://sites.google.com/lbl.gov/imghelp/home/img-and-gold-terms

---

## Database Structure and Identifiers

### Projects and Studies

**Study** (`gold.study`, `gold_id` prefix `Gs*`)
An overarching project name encompassing a list of sequencing projects (isolates, metagenomes, SAGs, etc.) that are part of the original research proposal (e.g. HMP study, GEBA study).

**Sequencing Project** (`gold.project`, `gold_id` prefix `Gp*`)
The individual organism or sample targeted for sequencing. A single sequencing project may use more than one sequencing reaction or technology. Types include isolate genomes, metagenomes, transcriptomes, metatranscriptomes, 16S surveys, etc. Multiple sequencing projects may be performed from a single Biosample.

**Biosample** (`gold.biosample`, `gold_id` prefix `Gb*`)
The original isolation place of the physical sample from which DNA was isolated. Usually describes the environment from which the sample was taken. For isolate genomes where the environment is unknown, the organism name may be used. Multiple sequencing projects can be derived from a single Biosample.

**Analysis Project (AP)** (`gold.analysis_project`, `gold_id` prefix `Ga*`)
The informatics processing of a Sequencing Project in IMG and GOLD. Describes how assembly and annotation were performed. Each IMG submission corresponds to one Analysis Project. The IMG taxon table links to it via `analysis_project_id = gold_id`.

**Organism** (`gold.organism_v2`, `gold_id` prefix `Go*`)
An individual living entity (plant, fungus, microbe, etc.).

**Specimen**
The sequencing material source — either an Organism or a Biome (environmental sample).

### Key Identifiers

| Identifier | Description |
|------------|-------------|
| `taxon_oid` | Primary IMG taxon identifier. Every genome/metagenome in IMG has one. |
| GOLD Analysis Project ID (`Ga*`) | Links to `gold.analysis_project`; stored as `taxon.analysis_project_id` in IMG. |
| GOLD Sequencing Project ID (`Gp*`) | Unique ID for every sequencing project in GOLD. |
| IMG Submission ID | Unique ID assigned when a dataset is submitted to the IMG annotation pipeline. |
| JGI Project ID / ITS SP ID | Internal JGI production pipeline IDs, available only for JGI-sequenced projects. |
| ITS Proposal ID | Unique ID assigned to all proposals approved for sequencing at JGI. |
| GPTS Proposal ID | Legacy JGI proposal ID for older projects. |
| HMP ID | Unique ID for datasets from the Human Microbiome Project DACC catalogue. |

---

## Analysis Project Types

`analysis_project_type` (in `img_core_v400.taxon` and `gold.analysis_project`) describes the annotation process applied and is determined by the sequencing project type. Key values:

| `analysis_project_type` | Description |
|------------------------|-------------|
| `Genome Analysis (Isolate)` | Standard isolate genome annotation |
| `Metagenome Analysis` | Shotgun metagenome (community) assembly and annotation |
| `Metagenome-Assembled Genome` | MAG: genome reconstructed by binning a metagenome |
| `Metagenome - Cell Enrichment` | Draft assembly from a cell enrichment (>1 cell), typically with WGA |
| `Metagenome - Combined Assembly` | Co-assembly from reads across multiple metagenome samples |
| `Metagenome - Single Particle Sort` | Draft genome/metagenome from a single particle isolated by flow cytometry |
| `Metagenome - Low Complexity` | Metagenome from a low-complexity community |
| `Metagenome - SIP` | Stable Isotope Probing metagenome |
| `Metatranscriptome Analysis` | mRNA community sequencing (cDNA-based) |
| `Single Cell Analysis (screened)` | SAG with contaminant screening applied |
| `Single Cell Analysis (unscreened)` | SAG without contaminant screening |

---

## Sequencing Status

`seq_status` applies to isolate genomes. For all other types (metagenomes, SAGs, MAGs) the status is always `Permanent Draft`.
For isolates, this can be specified by the data submitter, otherwise it default to `Permanent Draft`. Because most users do not 
specify this metadata, this `seq_status` is not very informative nowadays.

| Status | Meaning |
|--------|---------|
| `Finished` | <1 error per 100,000 bp; each replicon assembled into a single contiguous sequence; all misassemblies resolved; repetitive sequences correctly ordered. |
| `Permanent Draft` | Incomplete assembly; no further sequencing improvements planned. |
| `Draft` | Incomplete assembly; further sequencing or gap closure may still be planned. |

---

## Genome Quality

### `high_quality_flag` (IMG internal QC)

IMG assigns `high_quality_flag = 'Yes'` to a genome only when **all** of the following are met:
- The genome is **not** a MAG or an unscreened SAG
- GOLD phylogeny is neither `UNCLASSIFIED`, `UNCLASSIFIED-ARCHAEAL`, nor `UNCLASSIFIED-BACTERIAL`
- Coding density is between **70% and 100%**
- Genes per million bases is between **700 and 1,400**
- Sequences per million bases is **≤ 300**

IMG recommends also considering scaffold count, CheckM2 completeness, and contamination as additional quality metrics.

Practical coverage across data types (public, non-obsolete taxons):
- **Isolates**: 98.1% flagged `Yes` — a meaningful QC gate
- **MAGs**: 99.9% flagged `No` — not informative; use CheckM2 instead
- **Metagenomes / metatranscriptomes**: mostly `NULL` — not applicable

### Completeness and Contamination (CheckM2)

CheckM2 completeness and contamination scores are computed for isolate genomes, MAGs, and metagenome bins. In the Lakehouse these are available in `img_core_v400.taxon_gtdbtk_lineage` as `checkm_completeness` and `checkm_contamination`.

MIMAG quality tiers based on CheckM2:

| Tier | Completeness | Contamination |
|------|-------------|---------------|
| High quality | ≥90% | ≤5% |
| Medium quality | ≥50% | ≤10% |
| Low quality | <50% | >10% |

### GOLD Sequencing Quality

Community-defined categories reflecting genome sequence quality (based on Chain et al.). Stored in `gold.analysis_project` as `completeness_percentage` / `contamination_percentage`. These are frequently `NULL` for traditional isolate genomes (assumed complete).

---

## Sequence Assembly Concepts

**Contig**
A consensus sequence of a continuous DNA fragment from overlapping reads. Bases, order, and length are known with high confidence. No gaps.

**Scaffold**
A portion of the genome reconstructed from partial sequencing (e.g. paired-end reads, Hi-C, optical mapping). Composed of contigs joined by gaps (represented as Ns). Length is less certain than a contig.

**Scaffold Lineage**
IMG-computed taxonomic affiliation of a scaffold based on the last common ancestor of LAST hits (against the IMG-NR isolate database) for genes on the scaffold, where ≥50% of genes have hits.

**Scaffold Read Depth** (= scaffold/contig average coverage)
Average number of reads aligned to each base of the contig. Computed by aligning reads with tools like bbmap or Bowtie.

**Scaffold Set**
A user-created group of scaffolds from any project, saved to the IMG workspace.

**Genome Fragments**
DNA sequences from plasmids, cosmids, fosmids, or other vectors, typically from efforts to sequence biosynthetic gene clusters. Imported from NCBI.

---

## MAGs, SAGs, and Metagenome Bins

**MAG** (Metagenome-Assembled Genome)
A genome reconstructed through assembly and binning from a metagenome. Stored with `analysis_project_type = 'Metagenome-Assembled Genome'`.

**Binning**
The process of grouping reads or contigs and assigning them to operational taxonomic units (OTUs). IMG's binning process produces Metagenome Bins.

**Metagenome Bin**
A scaffold set grouped by IMG's metagenome binning process. A more general term than MAG; all MAGs are bins, but not all bins meet MAG quality thresholds.

**SAG** (Single Amplified Genome)
A genome obtained via Whole Genome Amplification (WGA) on a single cell. Stored with `analysis_project_type = 'Single Cell Analysis (screened)'` or `'(unscreened)'`.
- **Screened**: contaminant sequences were identified and removed by comparison to a reference database.
- **Unscreened**: no contaminant screening was performed.

**GVMAG** (Giant Virus Metagenome-Assembled Genome)
Genome bins identified as giant viruses (similar in size/complexity to small bacteria). Presented in the IMG/VR database.

---

## Viral and Plasmid Sequences

**UViG** (Uncultivated Virus Genome)
Virus genomes predicted computationally from sequences; viral origin not experimentally verified.

**vOTU** (viral Operational Taxonomic Unit)
Groups of UViGs clustered at ≥95% ANI over ≥85% alignment fraction.

**Predicted Viruses**
Sequences predicted to be viral by geNomad (https://portal.nersc.gov/genomad/). Presented in IMG/VR.

**Predicted Plasmids**
Sequences predicted to represent plasmids by geNomad. Presented in IMG/PR.

**PTU** (Plasmid Taxonomic Unit)
Groups of plasmid sequences sharing a common genomic backbone with elevated ANI.

---

## Taxonomy

### NCBI Taxonomy
Standard lineage assigned to isolate genomes: `domain`, `phylum`, `ir_class`, `ir_order`, `family`, `genus`, `species` fields in `img_core_v400.taxon`.

### GTDB-Tk Lineage
Genome-based taxonomic classification of bacterial and archaeal genomes using the GTDB-Tk toolkit (Parks et al.) compared against a comprehensive reference database. In IMG:
- Applied to isolate genomes (in addition to NCBI taxonomy), MAGs, and metagenome bins
- Available in `img_core_v400.taxon_gtdbtk_lineage` — joins directly on `taxon_oid`
- Pre-split rank columns: `gtdbtk_domain`, `gtdbtk_phylum`, `gtdbtk_class`, `gtdbtk_order`, `gtdbtk_family`, `gtdbtk_genus`, `gtdbtk_species`
- Only covers Bacteria and Archaea; coverage for those domains in IMG is essentially complete (Bacteria 99.8%, Archaea 99.4%)

### Ecosystem Classification (GOLD)
A five-level hierarchical classification of the environment from which a sample or organism was collected. Stored in `gold.biosample`, `gold.study`, and `gold.project`.

```
Ecosystem → Ecosystem Category → Ecosystem Type → Ecosystem Subtype → Specific Ecosystem
Example:
Environmental → Aquatic → Marine → Oceanic → Aphotic zone
```

### ANI (Average Nucleotide Identity)
A measure of nucleotide-level genomic similarity between the coding regions of two genomes. Used for species-level clustering.

**ANI Cluster**: a set of genomes grouped above an ANI threshold, with a unique ANI Cluster ID.
- **Clique**: all genomes in the cluster are connected to each other above the threshold.
- **Clique group**: some genomes within the cluster fall below the threshold.

### OTU / Ecotype
- **OTU** (Operational Taxonomic Unit): a group of similar sequences used as a proxy for "species" in diversity analyses.
- **Ecotype**: a population of a species distinct through environmental selection, comparable to a subspecies but not yet formally classified as one.

---

## Functional Annotation Terms

**Abundance Profile**
Count of the number of genes (or gene copies) across protein family collections (COG, Pfam, etc.) for a selected set of datasets.

**Function Profile**
An IMG matrix visualization tool showing the abundance of protein families of interest across a set of (meta)genomes or scaffolds. Rows = genomes/scaffolds, columns = protein families, cells = counts.

**Biosynthetic Cluster**
A computationally predicted biosynthetic gene cluster (BGC) for secondary metabolite production. Predictions use antiSMASH v5.0.

**Cassette** (Chromosomal / Gene Cassette)
Co-located genes in a chromosome: a series of CDS with intergenic distance ≤300 nucleotides. Computed for isolate genomes only.

**Homolog** (IMG usage)
A similar sequence found by BLAST or pairwise alignment. Does not imply shared ancestry in IMG's usage.

**Ortholog** (IMG usage)
Identified by reciprocal best BLAST hit; may be used to infer identical or equivalent function when comparing two isolate genomes.

**Paralog** (IMG usage)
Identified by BLAST hits within the same genome.

**Fused Protein** (Gene Fusion)
A protein with ≥2 domains encoded by genes that have been joined and are transcribed/translated as a single unit.

**Locus Type**
IMG's subset of INSDC feature keys: `CDS` (protein-coding sequence), `rRNA`, `tRNA`, `miscRNA`.

---

## Metagenome-Specific Metrics

**Estimated Gene Copies**
Average coverage (read depth) of a gene in a metagenome. Used to compute gene abundances accounting for population abundance variation. Approximated by the average contig coverage.

**Estimated Number of Genomes**
Estimated total number of genomes in an assembled metagenome, calculated from single-copy marker gene counts (approach similar to Anvi'o). Considers only bacteria and archaea — viruses and eukaryotes are excluded.

**Estimated Average Genome Size**
Total contig size divided by the estimated number of genomes (see above). Can be unusually high if the assembly contains significant non-bacterial/archaeal sequences (e.g. viruses, eukaryotes); IMG displays a warning in this case.

**Biome**
The environmental sample selected for sequencing.

**Marker Gene**
A gene or signature DNA region with a known genomic location, used to identify individuals or species.

---

## Other Terms

**Metadata**
Supplementary data linked to DNA sequences (organism or environmental sample descriptions). Adapted from GOLD in IMG.

**Metagenomics**
The study of genetic material via shotgun DNA sequencing from environmental samples (also: environmental genomics, ecogenomics, community genomics).

**Metatranscriptomics**
The study of expressed mRNAs isolated from an environmental sample, converted to cDNA for sequencing.

**Culture Type**
How an organism was obtained: `isolate` or `co-culture`.

**Organism Type**
Origin of the organism: Natural, Genetically modified, Hybrid, or Synthesized.

**Phenotype**
The set of observable characteristics of an individual resulting from genotype–environment interaction (morphology, biochemistry, physiology, behavior).

**Obsolete Genome**
A genome removed from IMG due to a sequence error or replacement by a newer version. May still be downloadable from the JGI Genome Portal. Always filter with `obsolete_flag = 'No'` in queries.

**Submission Type**
Indicates whether a dataset is `primary` (included in the IMG reference dataset) or `reanalysis` (excluded from the reference dataset).

**Type Strain**
An alphanumeric string designating the type strain status of an isolate — the strain used when the species was first described, typically deposited in culture collections (DSMZ, ATCC, etc.).

**IMG Release / Pipeline Version**
Version number of the annotation pipeline used when a dataset was processed. Pipeline details (tool versions, databases used) are in the "Annotation Method" field starting from pipeline v5.1.x. For isolate genomes, older functional annotations are "backfilled" when newer database versions are applied.

**IMG Terms / Pathways / Parts / Network**
IMG-specific functional curation efforts (curated pathways, parts lists, networks).

**JGI Genome Portal**
Centralized JGI resource for data download (https://genome.jgi.doe.gov).

**HPC** (High-Performance Computing)
Computer clusters used for parallel analysis or large job splitting. IMG uses HPC for back-end "Request for computation" tasks.

**WGS** (Whole Genome Sequencing)
Complete DNA sequencing of an organism's genome (also: full-genome sequencing, complete genome sequencing).

**FASTA**
Text-based file format for nucleotide or amino acid sequences. Each record starts with `>` followed by an identifier/description, then the sequence string.

**Workspace**
Available in IMG/MER and IMG/ABC portals. Users save genome, gene, function, or scaffold carts for later use, share datasets privately, and access extended functionality (large BLAST jobs, statistical analysis of genome sets).

**ProPortal**
An IMG DataMart for Prochlorococcus (and related species) datasets. ProPortal Clade is a taxonomy assignment for Cyanobacterial lineages only.

---

## Related Documentation

- [data-catalog.md](data-catalog.md) — All databases and key tables (GOLD, IMG, Portal)
- [IMG-tables-reference.md](IMG-tables-reference.md) — Complete IMG table catalog
- [IMG_data_types.md](IMG_data_types.md) — Breakdown of analysis project types with query patterns
- [explore_IMG_genomes.md](explore_IMG_genomes.md) — Genome metadata query guide (taxonomy, quality, size)
