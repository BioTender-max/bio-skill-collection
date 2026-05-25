# Pyrodigal

Python binding to Prodigal for fast prokaryotic gene finding.

## Official Documentation
- GitHub: https://github.com/althonos/pyrodigal
- Documentation: https://pyrodigal.readthedocs.io/

## Installation

```bash
# PyPI (recommended)
pip install pyrodigal

# Conda/Bioconda
conda install -c bioconda pyrodigal
```

Requires Python 3.7+. Pre-built wheels available for Linux, macOS, and Windows (x86-64 and Aarch64).

## Key Features

- Pure Python API (no CLI)
- Thread-safe for parallel processing
- SIMD-accelerated (up to 50% faster than original Prodigal)
- No intermediate files
- In-memory processing

## Common Usage Examples

### Metagenomic Mode (Pre-trained)

```python
import pyrodigal

# Initialize gene finder with metagenomic model
gene_finder = pyrodigal.GeneFinder(meta=True)

# Find genes
genes = gene_finder.find_genes(sequence_bytes)

# Extract protein sequences
for gene in genes:
    print(f">{gene.name}")
    print(gene.translate())
```

### Single Mode (Train on Genome)

```python
gene_finder = pyrodigal.GeneFinder()

# Train on genome sequence
gene_finder.train(training_sequence)

# Predict genes
genes = gene_finder.find_genes(sequence_bytes)
```

### Parallel Processing

```python
import multiprocessing.pool

gene_finder = pyrodigal.GeneFinder()
gene_finder.train(training_seq)

# Thread-safe parallel prediction
with multiprocessing.pool.ThreadPool() as pool:
    results = pool.map(gene_finder.find_genes, sequences)
```

## Input/Output Formats

**Input:**
- Raw bytes or strings (DNA sequences)
- No FASTA formatting required

**Output:**
- Gene objects with `.translate()` method
- Protein sequences via translation
- Training data can be serialized and reused

## Key Parameters

- `meta=True` - Use metagenomic mode (pre-trained)
- `closed=True` - Ignore genes running off sequence edges
- `mask=True` - Prevent predictions across unknown nucleotides
- `translation_table` - Set genetic code (default: 11)

## Performance Tips

- Use metagenomic mode for mixed communities
- Train once, reuse for similar genomes
- Leverage ThreadPool for parallel processing
- SIMD instructions provide 30-50% speedup
- In-memory operation eliminates I/O overhead
- Pre-allocates node arrays based on GC%
