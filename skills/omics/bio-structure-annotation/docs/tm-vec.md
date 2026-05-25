# TM-Vec

Fast protein structure embedding and similarity search using transformer-based vector representations.

## Official Documentation

- GitHub: https://github.com/tymor22/tm-vec
- Paper: https://www.biorxiv.org/content/10.1101/2022.07.25.501437v1
- DeepBLAST wiki: https://github.com/valentynbez/tmvec (database building & search examples)

## Installation

### CPU Installation
```bash
conda create -n tmvec faiss-cpu python=3.9 -c pytorch
conda activate tmvec
pip install tm-vec
```

### GPU Installation
```bash
conda create -n tmvec faiss-gpu python=3.9 -c pytorch
conda activate tmvec
pip install tm-vec
```

If installation fails, resolve dependencies:
```bash
conda install mkl=2021 mkl_fft
```

### Download Model Weights
Required for embedding generation:
```bash
mkdir Rostlab && cd Rostlab
wget https://zenodo.org/record/4644188/files/prot_t5_xl_uniref50.zip
unzip prot_t5_xl_uniref50.zip
cd ..
```

## Available Models

| Model | Max Length | Training Set | Use Case |
|-------|-----------|--------------|----------|
| `tmvec_swiss_model` | 300 residues | SWISS-PROT | Base model for short sequences |
| `tmvec_swiss_model_large` | 1000 residues | SWISS-PROT | Long sequences, Swiss-Prot searches |
| `tm_vec_cath_model` | 300 residues | CATH S40 | Base model for domain searches |
| `tm_vec_cath_model_large` | 1000 residues | CATH S100 | Long domains, CATH searches |

Models available at: https://figshare.com/s/e414d6a52fd471d86d69

## Pre-built Databases

Download from Zenodo: https://zenodo.org/records/11199459

- **CATH domains database** - Use with `tm_vec_cath_model_large`
- **SWISS-PROT sequences** - Use with `tmvec_swiss_model_large`

Embeddings stored as numpy arrays (.npy format):
```python
import numpy as np
embeddings = np.load('database.npy', allow_pickle=True)
```

## Common Usage

### Embedding Sequences
Use Google Colab notebook or scripts in the repository's `scripts/` folder.

### Building Custom Databases
See DeepBLAST wiki for detailed instructions on:
- Embedding your sequences with TM-vec models
- Creating searchable databases with FAISS
- Index optimization for large databases

### Searching Against Databases
See DeepBLAST wiki for search protocol and examples.

## Input/Output Formats

- **Input**: Protein sequences in FASTA format
- **Output**:
  - Vector embeddings (numpy arrays)
  - Similarity scores for homology detection
  - Position-indexed metadata linking embeddings to sequences

## Performance Tips

- Use GPU for embedding generation on large datasets
- GPU users may need to reinstall PyTorch separately for optimal compatibility
- Choose model size based on maximum sequence length in dataset
- Pre-embed large databases for repeated searches

## Typical Workflow

1. Download appropriate pre-trained model
2. Generate embeddings for query sequences
3. Search against pre-built databases (CATH or Swiss-Prot) OR
4. Build custom database from target sequences
5. Perform fast vector similarity search using FAISS
6. Filter hits by similarity threshold
