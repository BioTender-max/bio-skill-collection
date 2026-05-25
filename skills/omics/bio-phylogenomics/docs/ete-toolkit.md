# ETE Toolkit Usage Guide

## Official Documentation
- Main Documentation: https://etetoolkit.github.io/ete/
- Tutorial: https://etetoolkit.github.io/ete/tutorial/tutorial_trees.html
- API Reference: https://etetoolkit.github.io/ete/reference/reference_tree.html
- GitHub Repository: https://github.com/etetoolkit/ete

## Installation

### Quick Installation
```bash
pip install ete4
```

### Conda Installation
```bash
conda install conda-forge::ete4
```

### Development Installation
```bash
git clone https://github.com/etetoolkit/ete.git
cd ete
pip install -e .
```

### With Visualization Support (PyQt)
```bash
pip install -e ".[treeview,test,doc]"
```

### Dependencies
Core: Cython, Bottle, Cheroot, Brotli, NumPy, SciPy
Optional: PyQt (for GUI treeview)

## Input/Output Formats

### Supported Formats
- **Newick**: Standard phylogenetic tree format
- **Nexus**: Alternative tree format
- **NHX** (Extended Newick): Newick with custom annotations

### Reading Trees
```python
from ete4 import Tree

# From string
t = Tree('(A:1,(B:1,(E:1,D:1):0.5):0.5);')

# From file
t = Tree(open('tree.nw'))

# With format specification (0-10)
t = Tree('tree.nw', parser=1)  # Internal nodes as names
```

### Writing Trees
```python
# To string
newick_str = t.write()

# To file
t.write(outfile='output.nw')

# With format
t.write(parser=1)  # Include internal node names

# With custom properties (NHX)
t.write(props=['support', 'custom_feature'])
```

## Key Python API Methods

### Tree Structure and Attributes

#### Core Node Attributes
```python
node.name           # Node identifier
node.dist           # Branch length to parent
node.support        # Bootstrap/support value
node.up             # Parent node reference
node.children       # List of child nodes
```

#### Node Properties
```python
node.is_leaf        # Boolean: terminal node?
node.is_root        # Boolean: root node?
len(node)           # Number of descendant leaves
```

### Tree Traversal

#### Basic Iteration
```python
# Iterate over all leaves
for leaf in t:
    print(leaf.name)

# Iterate over all nodes
for node in t.traverse():
    print(node.name)
```

#### Traversal Strategies
```python
# Levelorder (breadth-first, default)
for node in t.traverse('levelorder'):
    process(node)

# Preorder (root, left, right)
for node in t.traverse('preorder'):
    process(node)

# Postorder (left, right, root)
for node in t.traverse('postorder'):
    process(node)
```

#### Access Methods
```python
# Get all leaves
leaves = list(t.leaves())

# Get all descendants
descendants = list(t.descendants())

# Get ancestors
ancestors = list(node.ancestors())

# Get sisters (siblings)
sisters = node.get_sisters()

# Get children
children = node.get_children()
```

### Searching and Filtering

#### Basic Search
```python
# Find first node by name
node = t['A']

# Find all nodes with specific attribute
nodes = list(t.search_nodes(dist=0.5))
nodes = list(t.search_nodes(name='A'))
```

#### Advanced Search
```python
# Custom criteria
matches = [n for n in t.traverse() if n.dist > 0.3 and n.is_leaf]

# Using function
def my_filter(node):
    return len(node) > 5 and node.support > 0.9

filtered = [n for n in t.traverse() if my_filter(n)]
```

#### Finding Common Ancestors
```python
# Get most recent common ancestor
ancestor = t.common_ancestor(['A', 'B', 'C'])

# Check if exists
if ancestor:
    print(f"MRCA at node: {ancestor.name}")
```

### Tree Manipulation

#### Building Trees Programmatically
```python
# Create empty tree
t = Tree()

# Add children
child1 = t.add_child(name='A', dist=1.0)
child2 = t.add_child(name='B', dist=1.5)

# Add grandchildren
grandchild = child1.add_child(name='C', dist=0.5)

# Add sister
sister = grandchild.add_sister(name='D', dist=0.5)

# Populate with random topology
t.populate(10)  # 10 leaves with random structure
```

#### Removing Nodes
```python
# Detach entire subtree (removed but intact)
removed_subtree = node.detach()

# Delete node, reconnect children to parent
node.delete()
```

#### Pruning
```python
# Keep only specified leaves
t.prune(['A', 'B', 'C', 'D'])

# Preserve branch lengths
t.prune(['A', 'B', 'C'], preserve_branch_length=True)
```

#### Copying Trees
```python
# Fast copy (topology + basic attributes)
t2 = t.copy('newick')

# With extended features
t2 = t.copy('newick-extended')

# Full clone with Python objects
t2 = t.copy('cpickle')

# Deep copy (slowest, most complete)
t2 = t.copy('deepcopy')
```

### Node Annotation

#### Adding Custom Properties
```python
# Single property
node.add_prop('species', 'E. coli')

# Multiple properties
node.add_props(confidence=0.95, method='ML')

# Delete property
node.del_prop('old_feature')
```

#### Accessing Properties
```python
# Direct access
print(node.name, node.dist, node.support)

# Dictionary access
print(node.props['species'])
print(node.props.get('optional_feature', 'default'))
```

#### Writing with Custom Properties
```python
# Include specific properties in NHX format
t.write(props=['species', 'confidence'])

# Include all properties
t.write(props=None)
```

### Tree Rooting

#### Set Outgroup
```python
# Root by outgroup node
outgroup = t['outgroup_species']
t.set_outgroup(outgroup)

# Root by common ancestor
mrca = t.common_ancestor(['A', 'B'])
t.set_outgroup(mrca)
```

#### Midpoint Rooting
```python
# Find midpoint
midpoint = t.get_midpoint_outgroup()

# Root at midpoint
t.set_outgroup(midpoint)
```

#### Unroot Tree
```python
t.unroot()
```

### Distance Calculations

#### Between Nodes
```python
# Branch length distance
dist = t.get_distance('A', 'B')

# Topological distance (number of nodes)
dist = t.get_distance('A', 'B', topological=True)
```

#### Farthest Points
```python
# Farthest node
farthest_node, distance = node.get_farthest_node()

# Farthest leaf
farthest_leaf, distance = node.get_farthest_leaf()

# Topological distance
farthest_leaf, distance = node.get_farthest_leaf(topological=True)
```

### Tree Statistics

#### Basic Statistics
```python
# Number of leaves
n_leaves = len(t)

# Number of all nodes
n_nodes = len(list(t.traverse()))

# Tree depth
max_depth = max(len(list(leaf.ancestors())) for leaf in t)

# Average branch length
branches = [n.dist for n in t.traverse() if not n.is_root]
avg_branch = sum(branches) / len(branches)
```

#### Caching for Performance
```python
# Cache leaf information for fast repeated access
node2leaves = t.get_cached_content()

for node in t.traverse():
    n_tips = len(node2leaves[node])
    print(f"{node.name} has {n_tips} descendant leaves")

# Cache specific property
node2names = t.get_cached_content('name')
```

### Monophyly Testing

#### Check Monophyly
```python
# Test if taxa form monophyletic group
is_mono, category, outliers = t.check_monophyly(
    values=['A', 'B', 'C'],
    prop='name'
)

print(f"Monophyletic: {is_mono}")
print(f"Type: {category}")  # monophyletic, paraphyletic, or polyphyletic
print(f"Outliers: {outliers}")
```

#### Get Monophyletic Clades
```python
# Get all nodes with specific property values
for node in t.get_monophyletic(prop='species', values=['E. coli', 'S. enterica']):
    print(f"Monophyletic clade rooted at: {node.name}")
```

### Tree Comparison

#### Robinson-Foulds Distance
```python
t1 = Tree('(((a,b),c),((e,f),g));')
t2 = Tree('(((a,c),b),((e,f),g));')

# Calculate RF distance
rf, rf_max, common, parts_t1, parts_t2, _, _ = t1.robinson_foulds(t2)

print(f'RF distance: {rf} / {rf_max}')
print(f'Normalized RF: {rf/rf_max}')
print(f'Common nodes: {common}')
print(f'Unique to t1: {parts_t1 - parts_t2}')
```

#### General Comparison
```python
result = t1.compare(t2, prop='name')

print(f"Normalized RF: {result['norm_rf']}")
print(f"Effective tree size: {result['effective_tree_size']}")
print(f"Common leaves: {result['common_leaves']}")
```

### Resolving Polytomies

#### Convert Multifurcations to Binary
```python
# Resolve single node
polytomy_node = t.common_ancestor(['a', 'b', 'c'])
polytomy_node.resolve_polytomy(descendants=False)

# Resolve entire tree
t.resolve_polytomy(descendants=True)
```

## Command-Line Tools

### Interactive Tree Explorer
```bash
# Launch web-based tree explorer
ete4 explore -t tree.nw

# Python API version
python -c "from ete4 import Tree; Tree('tree.nw').explore()"
```

## Common Usage Patterns

### Load, Root, and Prune
```python
from ete4 import Tree

# Load tree
t = Tree('input.nw')

# Root at midpoint
midpoint = t.get_midpoint_outgroup()
t.set_outgroup(midpoint)

# Prune to taxa of interest
taxa_to_keep = ['species1', 'species2', 'species3']
t.prune(taxa_to_keep, preserve_branch_length=True)

# Save
t.write(outfile='rooted_pruned.nw')
```

### Filter by Bootstrap Support
```python
from ete4 import Tree

t = Tree('tree.nw')

# Remove poorly supported branches
threshold = 70.0

for node in t.traverse():
    if not node.is_leaf and not node.is_root:
        if node.support < threshold:
            node.delete()

t.write(outfile='filtered.nw')
```

### Annotate with Taxonomy
```python
from ete4 import Tree

t = Tree('tree.nw')

# Add taxonomic information
taxonomy = {
    'seq1': 'Bacteria;Proteobacteria;Gammaproteobacteria',
    'seq2': 'Bacteria;Firmicutes;Bacilli',
    # ... more mappings
}

for leaf in t:
    if leaf.name in taxonomy:
        leaf.add_prop('taxonomy', taxonomy[leaf.name])
        leaf.add_prop('phylum', taxonomy[leaf.name].split(';')[1])

# Save with annotations
t.write(props=['taxonomy', 'phylum'], outfile='annotated.nw')
```

### Calculate Tree Statistics
```python
from ete4 import Tree
import numpy as np

t = Tree('tree.nw')

# Collect statistics
branch_lengths = [n.dist for n in t.traverse() if not n.is_root]
support_values = [n.support for n in t.traverse() if not n.is_leaf and not n.is_root]

print(f"Total branches: {len(branch_lengths)}")
print(f"Mean branch length: {np.mean(branch_lengths):.4f}")
print(f"Median branch length: {np.median(branch_lengths):.4f}")
print(f"Total tree length: {sum(branch_lengths):.4f}")
print(f"Mean support: {np.mean(support_values):.2f}")
print(f"Branches >90% support: {sum(s > 90 for s in support_values)}")
```

### Compare Multiple Trees
```python
from ete4 import Tree

# Load trees
trees = [Tree(f'tree{i}.nw') for i in range(1, 6)]

# Calculate pairwise RF distances
for i, t1 in enumerate(trees):
    for j, t2 in enumerate(trees[i+1:], start=i+1):
        rf, rf_max, _, _, _, _, _ = t1.robinson_foulds(t2)
        norm_rf = rf / rf_max if rf_max > 0 else 0
        print(f"Tree{i+1} vs Tree{j+1}: RF={rf}, normalized={norm_rf:.3f}")
```

### Extract Subtrees
```python
from ete4 import Tree

t = Tree('large_tree.nw')

# Find clade of interest
clade_ancestor = t.common_ancestor(['species1', 'species2', 'species3'])

# Copy subtree
subtree = clade_ancestor.copy()

# Save
subtree.write(outfile='subtree.nw')
```

### Traverse from Leaf to Root
```python
from ete4 import Tree

t = Tree('tree.nw')

# Start at specific leaf
leaf = t['species1']

# Walk up to root
node = leaf
path = []
while node:
    path.append(node.name)
    node = node.up

print("Path from leaf to root:", ' -> '.join(path))
```

## Performance Tips

### Use Generators for Large Trees
```python
# Generators are memory-efficient
for node in t.traverse():  # Generator
    if node.support > 90:
        process(node)

# Lists load everything into memory
nodes = list(t.traverse())  # List
```

### Cache Frequently Accessed Information
```python
# Cache once, use many times
node2leaves = t.get_cached_content()

# Fast repeated access
for node in t.traverse():
    n_descendants = len(node2leaves[node])
```

### Efficient Node Lookup
```python
# Build name lookup dictionary for repeated searches
name_to_node = {n.name: n for n in t.traverse()}

# Fast O(1) lookup
node = name_to_node.get('species1')
```

### Choose Appropriate Copy Method
```python
# Fast: topology + basic attributes
t2 = t.copy('newick')

# Medium: includes custom properties as strings
t2 = t.copy('newick-extended')

# Slow: full Python object clone
t2 = t.copy('cpickle')

# Slowest: handles complex objects
t2 = t.copy('deepcopy')
```

## Integration with Phylogenomic Workflows

### Post-Process IQ-TREE Output
```python
from ete4 import Tree

# Load IQ-TREE result
t = Tree('alignment.treefile')

# Root at midpoint
midpoint = t.get_midpoint_outgroup()
t.set_outgroup(midpoint)

# Filter by UFBoot support
for node in list(t.traverse()):
    if not node.is_leaf and not node.is_root:
        if node.support < 95:
            print(f"Low support node: {node.name} ({node.support})")

# Save rooted tree
t.write(outfile='alignment.rooted.nw')
```

### Post-Process VeryFastTree Output
```python
from ete4 import Tree

# Load VeryFastTree result
t = Tree('tree.nw')

# VeryFastTree uses local support values
# Filter branches
min_support = 0.7  # Local support threshold

for node in list(t.traverse()):
    if not node.is_leaf and not node.is_root:
        if node.support < min_support:
            node.delete()

# Save cleaned tree
t.write(outfile='filtered_tree.nw')
```

### Visualize Tree with Custom Layout
```python
from ete4 import Tree

# Load tree
t = Tree('tree.nw')

# Launch interactive explorer
# Supports zooming, searching, filtering
t.explore()
```

## Typical Phylogenomic Analysis Pipeline

```python
from ete4 import Tree
import numpy as np

# 1. Load tree
t = Tree('iqtree_output.treefile')

# 2. Basic statistics
print(f"Number of leaves: {len(t)}")
print(f"Number of internal nodes: {len([n for n in t.traverse() if not n.is_leaf])}")

# 3. Support value summary
supports = [n.support for n in t.traverse() if not n.is_leaf and not n.is_root]
print(f"Mean support: {np.mean(supports):.2f}")
print(f"Median support: {np.median(supports):.2f}")
print(f"Support >95%: {sum(s > 95 for s in supports)}/{len(supports)}")

# 4. Root tree
midpoint = t.get_midpoint_outgroup()
t.set_outgroup(midpoint)

# 5. Remove low support branches
threshold = 70
for node in list(t.traverse()):
    if not node.is_leaf and not node.is_root:
        if node.support < threshold:
            node.delete()

# 6. Add annotations
for leaf in t:
    # Add custom metadata
    leaf.add_prop('analyzed', True)

# 7. Save processed tree
t.write(outfile='final_tree.nw')
t.write(props=['analyzed'], outfile='final_tree_annotated.nhx')

# 8. Generate report
with open('tree_report.txt', 'w') as f:
    f.write(f"Final tree statistics:\n")
    f.write(f"Leaves: {len(t)}\n")
    f.write(f"Nodes: {len(list(t.traverse()))}\n")
    f.write(f"Mean support: {np.mean(supports):.2f}\n")
```

## Citation

When using ETE Toolkit, cite:

Jaime Huerta-Cepas, François Serra and Peer Bork (2016). ETE 3: Reconstruction, analysis and visualization of phylogenomic data. *Molecular Biology and Evolution*, 33(6):1635-1638. doi: 10.1093/molbev/msw046
