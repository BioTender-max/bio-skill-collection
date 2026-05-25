# IQ-TREE Usage Guide

## Official Documentation
- Main: https://iqtree.github.io/doc/
- Command Reference: https://iqtree.github.io/doc/Command-Reference
- Quickstart: https://iqtree.github.io/doc/Quickstart
- Tutorial: https://iqtree.github.io/doc/Tutorial

## Installation

### Package Managers
```bash
# Conda
conda install -c bioconda iqtree

# macOS Homebrew
brew install brewsci/bio/iqtree3
```

### Manual Installation
Download from http://www.iqtree.org/ and extract archive. Copy files from `bin/` to system path:
```bash
# Linux/macOS
cp bin/iqtree /usr/local/bin/
```

## Input/Output Formats

### Supported Input
- PHYLIP format (default)
- FASTA format
- NEXUS format (for partitioned alignments)

### Key Output Files
- `.treefile` - Maximum likelihood tree in Newick format
- `.iqtree` - Analysis report with model selection, tree statistics
- `.log` - Run log with detailed progress
- `.ckp.gz` - Checkpoint file for resuming interrupted runs
- `.state` - Ancestral state reconstruction (with `-asr`)

## Key Command-Line Flags

### Essential Options
```bash
-s <alignment>          # Input alignment file (required)
-st <AA|DNA|CODON>      # Sequence type (auto-detected if not specified)
-pre <prefix>           # Output file prefix
-nt AUTO                # Auto-detect CPU cores
-mem <GB>               # Maximum RAM allocation (e.g., 8G)
```

### Model Selection
```bash
-m TEST                 # Standard model selection
-m MFP                  # Extended model selection with FreeRate models
-m <MODEL>              # Use specific model (e.g., GTR+I+G, LG+G4)
-mset <models>          # Restrict to specific models (e.g., WAG,LG,JTT)
-msub <type>            # AA model subset (nuclear|mitochondrial|chloroplast|viral)
-mfreq <freq_type>      # Frequency parameters
-mrate <rate_type>      # Rate heterogeneity parameters
```

### Model Syntax
General format: `-m MODEL+FreqType+RateType`

**DNA Models**: GTR, HKY, K2P, TN, TNe, K2P, F81, JC

**Protein Models**: LG, WAG, JTT, Dayhoff, DCMut, CpREV, mtREV, mtART, MtZoa, VT, Blosum62, FLU, rtREV, PMB

**Rate Heterogeneity**:
- `+I` - Invariable sites
- `+G4` - Gamma with 4 categories (default)
- `+G8` - Gamma with 8 categories
- `+R4` - FreeRate with 4 categories
- `+I+G` - Combined invariable + Gamma

### Bootstrap and Branch Support
```bash
-bb <replicates>        # Ultrafast bootstrap (recommended: ≥1000)
-bcor <threshold>       # Convergence threshold for UFBoot (default: 0.99)
-b <replicates>         # Standard nonparametric bootstrap
-alrt <replicates>      # SH-like approximate likelihood ratio test
-abayes                 # Approximate Bayes test
-lbp <replicates>       # Local bootstrap probability
```

### Tree Search Optimization
```bash
-fast                   # Fast tree search mode
-nstop <iterations>     # Stop after N unsuccessful iterations (default: 100)
-pers <strength>        # Perturbation strength 0-1 (default: 0.5)
-g <constraint_tree>    # Topological constraint tree
-redo                   # Ignore checkpoint and redo analysis
-safe                   # Numerical stability for large datasets (>2000 seqs)
```

### Partitioned Analysis
```bash
-p <partition_file>     # Partition file in NEXUS format
-sp <partition_file>    # Edge-unlinked partition model
-spp <partition_file>   # Edge-proportional partition model
-m MFP+MERGE            # Test merging partitions
```

### Advanced Features
```bash
--pathogen              # Use CMAPLE for low-divergence sequences
-asr                    # Ancestral state reconstruction
-z <tree_file>          # Tree topology tests (KH, SH, AU, ELW)
-zb <replicates>        # Bootstrap replicates for topology tests
```

## Common Usage Examples

### Basic Tree Inference with Auto Model Selection
```bash
iqtree -s alignment.phy -nt AUTO
```

### Specific Model with Ultrafast Bootstrap
```bash
iqtree -s alignment.phy -m GTR+I+G -bb 1000 -nt AUTO
```

### Model Selection with Multiple Support Tests
```bash
iqtree -s alignment.phy -m MFP -bb 1000 -alrt 1000 -nt AUTO
```

### Partitioned Analysis
```bash
iqtree -s alignment.phy -p partitions.nex -m MFP+MERGE -bb 1000 -nt AUTO
```

### Fast Mode for Large Datasets
```bash
iqtree -s large_alignment.phy -m GTR+G -fast -nt AUTO
```

### Protein Alignment with AA Model Selection
```bash
iqtree -s proteins.faa -st AA -m MFP -bb 1000 -nt AUTO
```

### Resume Interrupted Run
```bash
iqtree -s alignment.phy -redo
```

### Ancestral State Reconstruction
```bash
iqtree -s alignment.phy -m GTR+G -asr -nt AUTO
```

## Performance Tips

### Dataset Size Guidelines
- **<1K sequences**: Use standard mode with comprehensive model testing
- **1K-10K sequences**: Consider `-fast` for exploratory analysis
- **10K-100K sequences**: Use `-fast` mode or consider VeryFastTree
- **>100K sequences**: Switch to VeryFastTree

### Memory Optimization
- Use `-mem` flag to limit RAM usage
- Enable `-safe` for datasets >2000 sequences (adds numerical stability)
- Checkpoint files (`.ckp.gz`) enable resuming interrupted runs

### CPU Optimization
- `-nt AUTO` automatically detects available cores
- Specify exact core count with `-nt <number>`
- Parallelization efficiency decreases beyond 8-16 cores for most datasets

### Model Selection Speed
- `-m TEST` is faster than `-m MFP`
- Use `-mset` to restrict model testing to relevant subset
- For large datasets, consider fixing model based on pilot analysis

### Convergence
- Default `-nstop 100` works for most datasets
- Increase for difficult datasets: `-nstop 200` or `-nstop 500`
- Use `-pers 0.2` for more thorough search (lower perturbation)

## Typical Phylogenomic Workflows

### Exploratory Analysis
```bash
# Quick tree with reasonable accuracy
iqtree -s alignment.phy -m GTR+G -fast -bb 1000 -nt AUTO
```

### Publication-Quality Single Gene Tree
```bash
# Comprehensive model selection with multiple support measures
iqtree -s gene.phy -m MFP -bb 1000 -alrt 1000 -nt AUTO
```

### Multi-Gene Concatenated Analysis
```bash
# Partitioned analysis with model testing per partition
iqtree -s concat.phy -p partitions.nex -m MFP+MERGE -bb 1000 -nt AUTO
```

### Bootstrap Convergence Check
```bash
# Use correlation coefficient to assess convergence
iqtree -s alignment.phy -m GTR+G -bb 1000 -bcor 0.99 -nt AUTO
```

## Quality Control Checks

### Model Selection
Check `.iqtree` file for:
- BIC/AIC scores of selected model
- Alternative models within 2 AIC units (essentially equivalent)

### Bootstrap Support
- UFBoot: Values ≥95% indicate strong support
- SH-aLRT: Values ≥80% indicate strong support
- Both tests agreeing provides strongest confidence

### Tree Statistics
Check `.iqtree` file for:
- Log-likelihood value
- Tree length (sum of branch lengths)
- Proportion of invariable sites
- Gamma shape parameter

### Alignment Quality Indicators
- High proportion of invariable sites (>50%) may indicate poor alignment
- Very long tree length may indicate saturation or alignment errors
- Extremely short branches may indicate insufficient signal
