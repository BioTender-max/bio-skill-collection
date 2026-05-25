# VeryFastTree Usage Guide

## Official Documentation
- GitHub Repository: https://github.com/citiususc/veryfasttree
- Based on FastTree-2 algorithm with parallelization and vectorization optimizations

## Installation

### Package Managers
```bash
# Bioconda
conda install veryfasttree

# Homebrew (macOS)
brew install veryfasttree

# MacPorts
port install veryfasttree

# Python bindings
pip install veryfasttree
```

### From Source
Requires CMake 3.5+, C++11 compiler (GCC 5+), and optionally CUDA Toolkit for GPU support.

```bash
git clone https://github.com/citiususc/veryfasttree.git
cd veryfasttree
cmake .
make
make install  # Optional
```

### Build Options
```bash
cmake -DEXT=AVX2 .           # Specify vector extension
cmake -DCUDA_ENABLED=ON .    # Enable experimental GPU support
```

## Input/Output Formats

### Supported Input
- FASTA
- FASTQ
- PHYLIP (interleaved)
- NEXUS
- Compressed formats (zlib, libBZ2)

### Output
- Newick format phylogenetic trees
- Branch lengths and support values included

## Key Command-Line Flags

VeryFastTree maintains exact CLI compatibility with FastTree-2, allowing drop-in replacement.

### Essential Options
```bash
-nt                          # Nucleotide sequences (default: protein)
-n <number>                  # Number of sequences
-threads <n>                 # Number of threads (default: OMP_NUM_THREADS)
-threads-level <0-4>         # Parallelization degree (default: 3)
-threads-mode <0-1>          # 0=non-deterministic, 1=deterministic (default)
```

### Vector Extensions
```bash
-ext <type>                  # Vector instruction set
                             # AUTO (default): AVX2 if available, else SSE3
                             # SSE3, AVX, AVX2, AVX512
                             # CUDA (experimental GPU)
                             # NONE (native with loop unrolling)
```

### Arithmetic Precision
```bash
-double-precision            # Use 64-bit floats (default: 32-bit)
```

### Fast Exponential Approximations
```bash
-fastexp <0-3>               # Exponential function implementation
                             # 0: Standard library (default)
                             # 1-3: Fast approximations (decreasing precision)
```

### Memory Optimization
```bash
-disk-computing              # Use disk when RAM insufficient
-disk-computing-path <path>  # Specify storage location
-disk-dynamic-computing      # Further memory reduction with performance cost
```

### Tree Search Parameters
```bash
-fastest                     # Speed-up heuristics (less thorough)
-gtr                         # Generalized time-reversible model (DNA)
-lg                          # Le-Gascuel model (protein, default)
-wag                         # Whelan-And-Goldman model (protein)
-cat <n>                     # CAT approximation with n rate categories (default: 20)
-gamma                       # Use Gamma instead of CAT approximation
```

### Bootstrap Support
```bash
-boot <replicates>           # Calculate local bootstrap support
                             # Recommended: 1000 replicates
```

### Advanced Threading
```bash
-threads-ptw <n>             # Partitioning Tendency Window (default: 50)
-threads-verbose             # Display thread assignments and speedup estimates
```

## Common Usage Examples

### Basic Nucleotide Tree (DNA/RNA)
```bash
VeryFastTree -nt < alignment.fna > tree.nw
```

### Protein Tree with Default Settings
```bash
VeryFastTree < alignment.faa > tree.nw
```

### Multi-threaded Analysis
```bash
VeryFastTree -threads 16 < alignment.faa > tree.nw
```

### High-Precision Analysis
```bash
VeryFastTree -double-precision -threads 16 < alignment.faa > tree.nw
```

### GTR Model for Nucleotides
```bash
VeryFastTree -nt -gtr < alignment.fna > tree.nw
```

### Fastest Mode for Very Large Datasets
```bash
VeryFastTree -fastest -threads 32 < alignment.faa > tree.nw
```

### Memory-Constrained Environment
```bash
VeryFastTree -disk-computing -disk-computing-path /scratch/tmp < alignment.faa > tree.nw
```

### Maximum Parallelization
```bash
VeryFastTree -threads 64 -threads-level 4 < alignment.faa > tree.nw
```

### Specific Vector Extension
```bash
VeryFastTree -ext AVX512 -threads 32 < alignment.faa > tree.nw
```

### Bootstrap Support Values
```bash
VeryFastTree -boot 1000 -threads 16 < alignment.faa > tree.nw
```

## Performance Tips

### Dataset Size Guidelines
- **Exploratory or time-bounded analyses at any size**: VeryFastTree is the default first-pass tree builder; reserve IQ-TREE for final publication-quality inference or explicit project requirements.
- **10K-100K sequences**: VeryFastTree preferred over IQ-TREE -fast
- **>100K sequences**: VeryFastTree is the practical choice
- **>1M sequences**: Demonstrated capability (36 hours on 1M taxa)

### Speed vs Accuracy Tradeoffs

| Mode | Speed | Accuracy | Use Case |
|------|-------|----------|----------|
| Default | Fast | High | Balanced phylogenomics |
| `-fastest` | Fastest | Reduced | Exploratory, ultra-large datasets |
| `-double-precision` | Slower | Highest | Publication-quality |
| `-gamma` | Slower | Higher | Better model fit than CAT |

### Threading Optimization
- **Threads-level 3** (default): Optimal for most datasets
- **Threads-level 4**: Maximum parallelization for very large datasets
- **Threads-mode 1** (default): Deterministic results (reproducible)
- **Threads-mode 0**: Faster but non-deterministic

### Vector Extension Selection
- **AUTO** (default): Safe choice, automatically selects best available
- **AVX2**: Good balance for modern CPUs (2013+)
- **AVX512**: Best for recent server CPUs (2017+)
- **SSE3**: Compatibility mode for older systems

### Memory Management
VeryFastTree typically requires less memory than IQ-TREE:
- Default mode: Efficient memory usage
- Memory issues: Enable `-disk-computing`
- Extreme constraints: Add `-disk-dynamic-computing`
- Specify temp path: `-disk-computing-path /path/to/fast/disk`

### Fast Exponential Approximations
- **-fastexp 0** (default): Standard library, most accurate
- **-fastexp 1**: Fast approximation, minimal accuracy loss
- **-fastexp 2**: Faster, slight accuracy reduction
- **-fastexp 3**: Fastest, noticeable accuracy reduction

**Recommendation**: Use default unless speed is critical; test `-fastexp 1` on subset first.

## Comparison with FastTree-2

| Feature | VeryFastTree | FastTree-2 |
|---------|--------------|------------|
| Speed | 3x+ faster | Baseline |
| Tree topology | Identical | N/A |
| Determinism | Yes | No (parallel mode) |
| Vectorization | AVX/AVX512 | Limited |
| GPU support | Experimental | None |
| Memory efficiency | Enhanced | Standard |
| Max tested dataset | 1M sequences | ~100K |

## Typical Phylogenomic Workflows

### Standard Large Dataset Analysis
```bash
# 10K-100K sequences, balanced speed/accuracy
VeryFastTree -threads 32 -threads-level 3 < alignment.faa > tree.nw
```

### Ultra-Large Dataset (>100K sequences)
```bash
# Maximum speed with reasonable accuracy
VeryFastTree -fastest -threads 64 -threads-level 4 < massive.faa > tree.nw
```

### Publication-Quality Large Tree
```bash
# Higher precision, Gamma model, bootstrap
VeryFastTree -double-precision -gamma -boot 1000 -threads 32 < alignment.faa > tree.nw
```

### Memory-Limited Server
```bash
# Use disk for overflow, specify fast scratch space
VeryFastTree -disk-computing -disk-computing-path /scratch/phylo \
  -threads 16 < alignment.faa > tree.nw
```

### Nucleotide Metagenome Tree
```bash
# GTR model for DNA, multi-threaded
VeryFastTree -nt -gtr -threads 32 < 16S_alignment.fna > 16S_tree.nw
```

### Exploratory Analysis of Massive Dataset
```bash
# Fastest possible, then refine subsets with IQ-TREE
VeryFastTree -fastest -fastexp 1 -threads 64 < huge.faa > rough_tree.nw
```

## Quality Control Checks

### Tree Validity
- Ensure all input sequences appear in output tree
- Check for suspiciously long branches (potential alignment errors)
- Verify tree is binary (fully resolved)

### Performance Monitoring
- Use `-threads-verbose` to check parallelization efficiency
- Expected speedup: 50-80% of thread count for large datasets
- Sublinear scaling normal beyond 32-64 threads

### Model Fit
- CAT approximation (default) suitable for most large-scale analyses
- Consider `-gamma` for better model fit if time permits
- GTR generally preferred over simpler models for nucleotides

### Bootstrap Values
- Values >70% suggest reasonable support
- Values >90% indicate strong support
- Lower support expected for rapid diversifications

## Integration with Downstream Tools

### ETE Toolkit
```python
from ete4 import Tree
t = Tree('tree.nw')
# Perform post-processing, annotation, visualization
```

### Rooting and Refinement
```bash
# Generate tree with VeryFastTree
VeryFastTree -threads 32 < alignment.faa > tree.nw

# Root and analyze with ETE
ete4 explore -t tree.nw
```

## Performance Benchmarks

Based on published results (VeryFastTree v4.0):

| Dataset Size | VeryFastTree | FastTree-2 | IQ-TREE |
|-------------|--------------|------------|---------|
| 10K sequences | ~5 min | ~15 min | ~30 min |
| 100K sequences | ~30 min | ~2 hours | ~10 hours |
| 1M sequences | ~36 hours | ~5+ days | Impractical |

**Notes**: Times approximate, vary with alignment length, model, hardware.

## Citation

When using VeryFastTree, cite:
- Piñeiro & Pichel (2024) - VeryFastTree 4.0 and 1M taxa analysis (GigaScience)
- Piñeiro et al. (2020) - Original VeryFastTree parallelization (Bioinformatics)
- Price et al. (2010) - Original FastTree-2 algorithm (PLoS ONE)
