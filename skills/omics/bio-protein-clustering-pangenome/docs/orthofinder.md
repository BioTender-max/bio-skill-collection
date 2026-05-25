# OrthoFinder Usage Guide

## Official Documentation
- GitHub: https://github.com/davidemms/OrthoFinder
- Manual: https://github.com/davidemms/OrthoFinder/blob/master/OrthoFinder-manual.pdf
- Tutorials: https://davidemms.github.io/orthofinder_tutorials/
- Paper: https://genomebiology.biomedcentral.com/articles/10.1186/s13059-019-1832-y

## Installation

### Conda (Recommended)
```bash
conda install -c bioconda orthofinder
```

### Docker
```bash
docker pull davidemms/orthofinder
docker run -it --rm davidemms/orthofinder orthofinder -h
```

### Manual Installation
```bash
# Download latest release
wget https://github.com/davidemms/OrthoFinder/releases/latest/download/OrthoFinder.tar.gz
tar xzf OrthoFinder.tar.gz

# Test installation
python OrthoFinder/orthofinder.py -h
```

### Dependencies
- Python 3.x
- BLAST+ or Diamond (for sequence search)
- MCL (for clustering)
- FastME (optional, for tree inference)
- MAFFT (optional, for MSA)

## Key Command-Line Flags

### Basic Usage
```bash
orthofinder -f DIRECTORY [OPTIONS]
```

### Input/Output Options
- `-f DIRECTORY` - Directory containing protein FASTA files (one per species)
- `-b RESULTS_DIR` - Use previous BLAST results from specified directory
- `-o OUTPUT_DIR` - Output directory name (default: auto-generated timestamp)

### Search Method
- `-S PROGRAM` - Sequence search program
  - `blast` - NCBI BLAST+ (default, slower, more sensitive)
  - `diamond` - Diamond (faster, recommended for >20 species)
  - `diamond_ultra_sens` - Diamond ultra-sensitive mode
  - `blast_gz` - BLAST with compressed database
  - `mmseqs` - MMseqs2 (fastest for very large datasets)

### Threading and Performance
- `-t THREADS` - Number of parallel threads for BLAST/Diamond
- `-a THREADS` - Number of parallel threads for MSA and tree inference
- `-T AUTO|BLAST|MSA` - Control which steps use parallelization

### Analysis Modes
- `-M msa` - Infer orthogroup and species trees from multiple sequence alignments
- `-M dendroblast` - Infer species tree from BLAST bit scores (fastest)
- `-og` - Stop after inferring orthogroups (skip gene trees)
- `-os` - Stop after writing orthogroup sequences
- `-oa` - Stop after performing MSAs

### Species Tree Options
- `-s TREE_FILE` - Provide custom species tree (Newick format)
- `-S` - Skip orthogroup inference, use previous results

### Incremental Analysis
- `--core RESULTS_DIR` - Designate core analysis for incremental workflow
- `--assign NEW_SPECIES_DIR` - Assign new species to existing orthogroups

### Advanced Options
- `-op` - Only prepare for running in parallel (pre-process step)
- `-n NAME` - Custom analysis name
- `-x SPECIESINFO` - Species tree inference information file
- `-p PICKLEFILES` - Use pickled intermediate files

## Common Usage Examples

### Basic Ortholog Analysis
```bash
# Simple analysis with default settings
orthofinder -f protein_fastas/

# Output: Results_MMM_DD/
#   - Orthogroups/
#   - Phylogenetic_Hierarchical_Orthogroups/
#   - Species_Tree/
#   - Gene_Trees/
```

### Fast Analysis with Diamond
```bash
# Recommended for datasets with >20 species
orthofinder -f protein_fastas/ -S diamond -t 16

# Ultra-sensitive mode (slower but more accurate)
orthofinder -f protein_fastas/ -S diamond_ultra_sens -t 16
```

### MSA-Based Tree Inference
```bash
# Infer gene trees from multiple sequence alignments
orthofinder -f protein_fastas/ -M msa -t 32

# Produces highest quality phylogenetic trees
# Slower but recommended for phylogenomic analysis
```

### Incremental Analysis (Core + Assign)
```bash
# Step 1: Analyze core set of representative species
orthofinder -f CoreSpecies/ -n Core -t 16

# Step 2: Assign additional species to existing orthogroups
orthofinder --core Results_Core/ --assign AdditionalSpecies/ -t 16

# Efficient for large datasets (100+ species)
# Core set: 8-64 representative species
```

### Resume Previous Analysis
```bash
# Use previous BLAST results to save time
orthofinder -b PreviousResults/WorkingDirectory/ -t 16

# Useful when analysis was interrupted or parameters changed
```

### Custom Species Tree
```bash
# Provide pre-computed species tree
orthofinder -f protein_fastas/ -s my_species_tree.nwk -t 16

# Skips species tree inference, uses provided tree
```

### Stop After Orthogroups
```bash
# Get orthogroups only, skip gene trees (fast)
orthofinder -f protein_fastas/ -og -t 32

# Useful for quick pangenome analysis
```

### Large-Scale Analysis
```bash
# MMseqs2 backend for 100+ species
orthofinder -f protein_fastas/ -S mmseqs -t 64 -a 32

# Example: 1000 genomes analyzed efficiently
```

## Input/Output Formats

### Input Requirements

**Directory Structure:**
```
protein_fastas/
├── species1.faa
├── species2.faa
├── species3.faa
└── species4.faa
```

**FASTA File Requirements:**
- **Extensions**: `.fa`, `.faa`, `.fasta`, `.fas`, `.pep`
- **Content**: Protein sequences (amino acids)
- **Headers**: Unique IDs within each file
- **One file per species/genome**

**Example FASTA:**
```
>gene001
MTHKQVLVGADGVGKSAL...
>gene002
MRVLVVGAGGVGKSALT...
```

### Output Directory Structure

```
Results_MMM_DD/
├── Orthogroups/
│   ├── Orthogroups.tsv              # Primary orthogroup table
│   ├── Orthogroups.txt              # One orthogroup per line
│   ├── Orthogroups_UnassignedGenes.tsv
│   └── Orthogroups_SingleCopyOrthologues.txt
│
├── Phylogenetic_Hierarchical_Orthogroups/
│   ├── N0.tsv                        # Hierarchical orthogroups (root)
│   ├── N1.tsv, N2.tsv, ...          # Internal nodes
│   └── HOG_Sequences/
│
├── Orthologues/
│   ├── Orthologues_species1/        # Pairwise ortholog files
│   │   ├── species1__v__species2.tsv
│   │   └── species1__v__species3.tsv
│   └── ...
│
├── Gene_Trees/
│   └── OG000001_tree.txt             # Newick format gene trees
│
├── Species_Tree/
│   ├── SpeciesTree_rooted.txt        # Primary species tree
│   ├── SpeciesTree_rooted_node_labels.txt
│   └── SpeciesTree_Gene_Duplications_0.5_Support.txt
│
├── Comparative_Genomics_Statistics/
│   ├── OrthologuesStats_*.tsv        # Ortholog counts
│   ├── Duplications_per_Orthogroup.tsv
│   └── Statistics_Overall.tsv
│
└── WorkingDirectory/                 # Intermediate files
    ├── BlastDBSpecies0.fa
    ├── Blast0_1.txt
    └── SequenceIDs.txt
```

### Key Output Files

#### Orthogroups.tsv
Tab-separated orthogroup assignments:

| Orthogroup | species1.faa | species2.faa | species3.faa |
|------------|--------------|--------------|--------------|
| OG0000001 | gene001 | gene101, gene102 | gene201 |
| OG0000002 | gene002, gene003 | | gene202 |

- Empty cells = No gene from that species
- Comma-separated = Multiple genes (paralogs)

#### N0.tsv (Hierarchical Orthogroups)
Root-level orthogroups representing deepest evolutionary splits:

| HOG | OG | Gene Tree Parent Clade | species1 | species2 | species3 |
|-----|----|-----------------------|----------|----------|----------|
| N0.HOG0000001 | OG0000001 | N1 | gene001 | gene101 | gene201 |

### Parsing OrthoFinder Output

```python
import pandas as pd

# Read primary orthogroups
orthogroups = pd.read_csv('Results_MMM_DD/Orthogroups/Orthogroups.tsv',
                          sep='\t', index_col=0)

# Extract genome columns
genome_cols = orthogroups.columns

# Create presence/absence matrix
def is_present(cell):
    return 0 if pd.isna(cell) or cell == '' else 1

presence = orthogroups.apply(lambda col: col.apply(is_present))

# Identify single-copy orthologs
def is_single_copy(cell):
    if pd.isna(cell) or cell == '':
        return False
    return ',' not in str(cell)

single_copy_mask = orthogroups.apply(
    lambda row: all(is_single_copy(val) and not pd.isna(val)
                    for val in row),
    axis=1
)

single_copy_orthogroups = orthogroups[single_copy_mask]

print(f"Total orthogroups: {len(orthogroups)}")
print(f"Single-copy core orthogroups: {len(single_copy_orthogroups)}")

# Calculate core/accessory genome
n_genomes = len(genome_cols)
presence_freq = presence.sum(axis=1) / n_genomes

core = orthogroups[presence_freq >= 0.99]
accessory = orthogroups[(presence_freq >= 0.15) & (presence_freq < 0.99)]
cloud = orthogroups[presence_freq < 0.15]

print(f"Core: {len(core)}, Accessory: {len(accessory)}, Cloud: {len(cloud)}")
```

## Performance Tips

### Speed vs Accuracy Trade-offs

**Fast (Large datasets, >100 species):**
```bash
orthofinder -f fastas/ -S mmseqs -og -t 64
# Skip gene trees, use MMseqs2
```

**Balanced (Typical use, 20-100 species):**
```bash
orthofinder -f fastas/ -S diamond -t 32 -a 16
# Diamond search, full analysis
```

**Accurate (Phylogenomic analysis, <50 species):**
```bash
orthofinder -f fastas/ -M msa -S blast -t 16 -a 8
# MSA-based trees, BLAST search
```

### Memory Management

**Low Memory Mode:**
```bash
# Reduce parallelization
orthofinder -f fastas/ -t 4 -a 2

# Use Diamond instead of BLAST
orthofinder -f fastas/ -S diamond -t 8
```

**High Memory System:**
```bash
# Maximize parallelization
orthofinder -f fastas/ -t 64 -a 32

# Use BLAST for maximum sensitivity
orthofinder -f fastas/ -S blast -t 64
```

### Incremental Analysis for Large Datasets

**Strategy: Core (8-64 species) + Assign (remaining)**

```bash
# Select 30 representative species as core
orthofinder -f CoreSet_30species/ -n CoreAnalysis -t 32 -a 16

# Assign remaining 500 species to core orthogroups
orthofinder --core Results_CoreAnalysis/ \
            --assign Remaining_500species/ \
            -t 64
```

**Benefits:**
- Dramatically faster for >100 species
- Maintains phylogenetic accuracy
- Scalable to thousands of genomes

### Reusing Previous Results

```bash
# Initial analysis
orthofinder -f fastas/ -n InitialRun -t 16

# Resume or modify analysis
orthofinder -b Results_InitialRun/WorkingDirectory/ -M msa -t 16
# Reuses BLAST results, changes to MSA mode
```

## Parameter Recommendations

### Bacterial Pangenomics (Same Species)
```bash
orthofinder -f bacterial_genomes/ \
    -S diamond \
    -og \
    -t 32 \
    -n bacteria_pangenome

# Fast, orthogroups only
# Sufficient for presence/absence analysis
```

### Fungal/Eukaryotic Comparative Genomics
```bash
orthofinder -f eukaryote_proteomes/ \
    -S diamond_ultra_sens \
    -M msa \
    -t 16 \
    -a 8 \
    -n eukaryote_phylogenomics

# High sensitivity, MSA-based trees
# Better for divergent species
```

### Large-Scale Metagenomic Bins
```bash
# Core-assign workflow for 500+ MAGs
orthofinder -f CoreMAGs_50/ -n CoreMAGs -S mmseqs -t 64

orthofinder --core Results_CoreMAGs/ \
    --assign RemainingMAGs_450/ \
    -t 64

# Scalable approach for metagenomics
```

### Phylogenomic Analysis (Species Tree)
```bash
orthofinder -f proteomes/ \
    -S diamond \
    -M msa \
    -t 32 \
    -a 16 \
    -n phylogenomics

# Extract single-copy orthologs from:
# Results_phylogenomics/Orthogroups/Orthogroups_SingleCopyOrthologues.txt
```

## Troubleshooting

### No Orthogroups Found
- **Cause**: Input files not recognized
- **Solution**:
  - Check FASTA file extensions (.faa, .fa, .fasta)
  - Verify protein sequences (not nucleotides)
  - Ensure files are in input directory

### Very Few Single-Copy Orthologs (<50)
- **Cause**: Divergent species, annotation quality issues
- **Solution**:
  - Use `-S diamond_ultra_sens` for better sensitivity
  - Check if species are too distantly related
  - Verify annotation completeness (BUSCO scores)

### Out of Memory
- **Cause**: Too many parallel processes
- **Solution**:
  - Reduce `-t` and `-a` thread counts
  - Use incremental analysis (core + assign)
  - Use Diamond instead of BLAST (`-S diamond`)

### Analysis Interrupted
- **Solution**: Resume using previous results
```bash
orthofinder -b Results_MMM_DD/WorkingDirectory/ -t 16
```

### Slow Performance
- **For >100 species**: Use incremental analysis or MMseqs2
- **For gene trees**: Use `-og` to skip tree inference
- **For species tree**: Use `-M dendroblast` (faster than MSA)

## Key Features

### OrthoFinder Advantages
- **Phylogenetic orthology inference**: Most accurate method
- **Gene tree reconciliation**: Identifies duplication events
- **Hierarchical orthogroups**: Evolutionary relationships
- **Species tree inference**: Multiple methods (STAG, STRIDE, MSA)
- **Comprehensive output**: Orthologs, paralogs, gene trees, statistics
- **Incremental analysis**: Scalable to thousands of genomes

### Unique Capabilities
- Rooted gene trees with duplication events
- Pairwise ortholog predictions for all species pairs
- Gene duplication statistics per orthogroup
- Orthogroup overlap matrices
- Comparative genomics statistics

## Benchmarks
- **Small datasets (<20 species)**: ~1-4 hours on desktop
- **Medium datasets (50-100 species)**: ~8-24 hours with 32 cores
- **Large datasets (>500 species)**: Use core+assign workflow
- **Example**: 80 vertebrate proteomes (1.7M sequences) in ~20 hours

## Recommended Workflows

### Quick Pangenome Analysis
```bash
orthofinder -f genomes/ -S diamond -og -t 32
# Extract Orthogroups.tsv for downstream analysis
```

### Comprehensive Phylogenomics
```bash
orthofinder -f proteomes/ -M msa -t 32 -a 16
# Use single-copy orthologs for species tree
# Extract Gene_Trees/ for gene family evolution
```

### Scalable Metagenomics
```bash
# Core analysis (50 high-quality MAGs)
orthofinder -f CoreMAGs/ -n Core -S mmseqs -t 64

# Assign remaining MAGs
orthofinder --core Results_Core/ --assign AllMAGs/ -t 64
```
