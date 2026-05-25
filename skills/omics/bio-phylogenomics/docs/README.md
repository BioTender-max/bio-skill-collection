# Bio-Phylogenomics Tool Documentation

Documentation for phylogenetic tree inference and post-processing tools.

**Last Updated**: 2026-02-01

## Documentation Files

### Tree inference tools

- **[iqtree.md](iqtree.md)** - IQ-TREE v3.1.2+ usage guide
  - Maximum likelihood tree inference with comprehensive model selection
  - MAST and GTRpmix models (new in v3)
  - Default choice for final/publication-quality trees up to ~2,000 taxa
  - UFBoot, SH-aLRT, and standard bootstrap support

- **[veryfasttree.md](veryfasttree.md)** - VeryFastTree v4.0+ usage guide
  - Default choice for exploratory trees and when leaf count exceeds ~2,000
  - Parallelization and SIMD optimizations
  - "Disk computing" mode scales to >1M taxa
  - Drop-in replacement for FastTree-2 (FastTree itself is no longer recommended)

### Tree post-processing

- **[ete-toolkit.md](ete-toolkit.md)** - ETE v4 (`ete4`) usage guide
  - Python API for tree manipulation and analysis
  - Tree statistics, rooting, pruning, filtering
  - Distance calculations and topology comparison
  - Annotation and visualization capabilities
  - `ete4` replaces `ete3`; use `from ete4 import Tree`

## Tool selection guide

### When to use each tree inference tool

| Leaf count | Recommended tool | Notes |
|-----------|------------------|-------|
| Any size, exploratory | VeryFastTree v4 | Default for placement, screening, benchmark iterations, and other time-bounded work. Use local support values with `-boot 1000` when support is needed. |
| Up to ~2,000, final | IQ-TREE v3 standard | Full model selection (`-m MFP`), UFBoot/SH-aLRT. Publication-quality. |
| Up to ~2,000, exploratory fallback | `iqtree3 -fast` | Use only when VeryFastTree is unavailable or IQ-TREE-compatible exploratory output is explicitly required. |
| ~2,000 to ~100,000 | VeryFastTree v4 | Default beyond the IQ-TREE 3 sweet spot. |
| >100,000 | VeryFastTree v4 with `--disk-computing` | Scales to >1M taxa. |

### When to Use ETE Toolkit

Use ETE Toolkit for **all** tree post-processing tasks:
- Calculate tree statistics (branch lengths, support values, topology metrics)
- Root trees (midpoint or outgroup rooting)
- Prune or filter trees (by taxa, support values, or custom criteria)
- Collapse poorly supported nodes
- Add taxonomic or trait annotations
- Compare tree topologies (Robinson-Foulds distance)
- Extract subtrees or clades
- Generate publication-quality visualizations

## Typical Phylogenomic Workflows

### Small Dataset (Publication Quality)
```bash
# 1. Tree inference with IQ-TREE
iqtree -s alignment.phy -m MFP -bb 1000 -alrt 1000 -nt AUTO

# 2. Post-process with ETE
python << EOF
from ete4 import Tree
t = Tree('alignment.treefile')
midpoint = t.get_midpoint_outgroup()
t.set_outgroup(midpoint)
t.write(outfile='alignment.rooted.nw')
EOF
```

### Exploratory Dataset
```bash
# 1. Fast exploratory tree with VeryFastTree
VeryFastTree -boot 1000 -threads 32 < large.faa > large.nw

# 2. Filter and analyze
python << EOF
from ete4 import Tree
t = Tree('large.nw')
for node in t.traverse():
    if not node.is_leaf and node.support < 70:
        node.delete()
t.write(outfile='large.filtered.nw')
EOF
```

### Massive Dataset (>100K sequences)
```bash
# 1. Ultra-fast inference with VeryFastTree
VeryFastTree -threads 32 < massive.faa > massive.nw

# 2. Root and summarize
python << EOF
from ete4 import Tree
import numpy as np

t = Tree('massive.nw')
midpoint = t.get_midpoint_outgroup()
t.set_outgroup(midpoint)

# Calculate statistics
supports = [n.support for n in t.traverse() if not n.is_leaf]
print(f"Mean support: {np.mean(supports):.2f}")
print(f"Median support: {np.median(supports):.2f}")

t.write(outfile='massive.rooted.nw')
EOF
```

## Official Documentation Sources

### IQ-TREE
- Main: https://iqtree.github.io/doc/
- Command Reference: https://iqtree.github.io/doc/Command-Reference
- Quickstart: https://iqtree.github.io/doc/Quickstart
- Tutorial: https://iqtree.github.io/doc/Tutorial

### VeryFastTree
- GitHub: https://github.com/citiususc/veryfasttree
- Based on FastTree-2 algorithm

### ETE Toolkit
- Main: https://etetoolkit.github.io/ete/
- Tutorial: https://etetoolkit.github.io/ete/tutorial/tutorial_trees.html
- API Reference: https://etetoolkit.github.io/ete/reference/reference_tree.html
- GitHub: https://github.com/etetoolkit/ete

## Quick Reference

### IQ-TREE Essential Commands
```bash
iqtree -s alignment.phy                       # Auto model selection
iqtree -s alignment.phy -m GTR+I+G            # Specific model
iqtree -s alignment.phy -m MFP -bb 1000       # Model selection + UFBoot
iqtree -s alignment.phy -fast -nt AUTO        # Exploratory fallback when VeryFastTree cannot be used
```

### VeryFastTree Essential Commands
```bash
VeryFastTree -nt < dna.fna > tree.nw          # DNA/RNA sequences
VeryFastTree < proteins.faa > tree.nw         # Protein sequences
VeryFastTree -boot 1000 < proteins.faa > tree.nw # Exploratory tree with local support
VeryFastTree -threads 32 < input.faa > tree.nw # Multi-threaded
VeryFastTree -fastest -threads 64 < huge.faa > tree.nw # Maximum speed
```

### ETE Toolkit Essential Python
```python
from ete4 import Tree

# Load and basic info
t = Tree('tree.nw')
print(f"Leaves: {len(t)}")

# Root at midpoint
midpoint = t.get_midpoint_outgroup()
t.set_outgroup(midpoint)

# Filter by support
for node in t.traverse():
    if not node.is_leaf and node.support < 70:
        node.delete()

# Save
t.write(outfile='output.nw')
```

## Installation Summary

### IQ-TREE
```bash
conda install -c bioconda iqtree
# or
brew install brewsci/bio/iqtree3
```

### VeryFastTree
```bash
conda install veryfasttree
# or
brew install veryfasttree
```

### ETE Toolkit
```bash
pip install ete4
# or
conda install conda-forge::ete4
```

## Performance Comparison

| Tool | 10K seqs | 100K seqs | 1M seqs | Accuracy |
|------|----------|-----------|---------|----------|
| IQ-TREE standard | ~30 min | ~10 hours | Impractical | Highest |
| IQ-TREE -fast | ~10 min | ~3 hours | Impractical | High |
| VeryFastTree | ~5 min | ~30 min | ~36 hours | High |

**Notes**:
- Times are approximate and vary with alignment length, model, and hardware
- For exploratory work, choose VeryFastTree first; `IQ-TREE -fast` is a fallback when VeryFastTree is unavailable or IQ-TREE-compatible output is required.
- IQ-TREE provides best model selection and publication-quality trees
- VeryFastTree maintains identical topology to FastTree-2 with 3x+ speedup
- All tools produce maximum likelihood trees with support values

## Key Differences

### IQ-TREE vs VeryFastTree

| Feature | IQ-TREE | VeryFastTree |
|---------|---------|--------------|
| Model selection | Comprehensive (100+ models) | Fixed (GTR, LG, WAG) |
| Bootstrap | UFBoot, standard, SH-aLRT | Local bootstrap |
| Speed (100K seqs) | Hours | Minutes |
| Max practical size | ~100K sequences | >1M sequences |
| Best for | Final/publication trees | Exploratory, large-scale, time-bounded work |

### When to Use ETE Over Command-Line Tools

- **Automated processing**: Python scripts for batch tree processing
- **Custom statistics**: Calculate metrics not provided by inference tools
- **Complex filtering**: Filter by multiple criteria or custom logic
- **Annotation**: Add metadata from external sources
- **Topology comparison**: Compare multiple trees systematically
- **Integration**: Part of larger bioinformatics pipeline
- **Visualization**: Programmatic figure generation for publications

## Additional Resources

- Project paper summaries: `../summaries/`
- Main skill documentation: `../SKILL.md`
