# ColabFold

Fast and accessible protein structure prediction using AlphaFold2 and RoseTTAFold with optimized MSA generation.

## Official Documentation

- GitHub: https://github.com/sokrypton/ColabFold
- Paper: https://www.nature.com/articles/s41592-022-01488-1
- Google Colab: https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/AlphaFold2.ipynb

## Installation

### LocalColabFold (Recommended for Local Use)
LocalColabFold installer for Windows 10+, macOS, and Linux:
```bash
# See: https://github.com/YoshitakaMo/localcolabfold
# Follow OS-specific installation instructions
```

### Docker
See ColabFold wiki for Docker deployment instructions.

### Manual Installation
```bash
pip install colabfold
```

## Key Commands

### Basic Structure Prediction
```bash
colabfold_batch input_sequences.fasta output_directory
```
Automatically queries public MSA server and performs prediction.

### Two-Step MSA Generation
Separate MSA computation from prediction for better GPU resource management:

```bash
# Step 1: Generate MSAs only
colabfold_batch input_sequences.fasta output_dir --msa-only

# Step 2: Run predictions using generated MSAs
colabfold_batch input_sequences.fasta output_dir
```

### Local Database Search
For large-scale predictions (requires ~940GB storage):

```bash
# Setup databases (one-time)
MMSEQS_NO_INDEX=1 ./setup_databases.sh /path/to/db_folder

# Search and predict
colabfold_search --mmseqs /path/to/bin/mmseqs sequences.fasta \
  /path/to/db_folder msas

colabfold_batch msas predictions
```

## Command-Line Flags

### MSA Generation

| Flag | Description | Example |
|------|-------------|---------|
| `--msa-only` | Generate MSAs without structure prediction | `colabfold_batch seqs.fa out --msa-only` |
| `--gpu 1` | Enable GPU-accelerated MSA search | `colabfold_search --gpu 1` |
| `--db-load-mode` | Database loading strategy (0/1/2) | `--db-load-mode 1` |

### Prediction Parameters

| Flag | Description | Example |
|------|-------------|---------|
| `--num-models` | Number of models to use | `--num-models 5` (default) |
| `--num-recycle` | Number of recycling iterations | `--num-recycle 3` |
| `--use-gpu-relax` | GPU-accelerated AMBER relaxation | `--use-gpu-relax` |
| `--templates` | Enable template search | `--templates` |
| `--amber` | Run AMBER relaxation | `--amber` |

### Output Control

| Flag | Description | Example |
|------|-------------|---------|
| `--af3-json` | Export MSAs in AlphaFold3 JSON format | `--af3-json` |
| `--save-all` | Save all intermediate outputs | `--save-all` |
| `--save-recycles` | Save all recycling iterations | `--save-recycles` |

### GPU Selection
```bash
CUDA_VISIBLE_DEVICES=0,1 colabfold_batch input.fasta output/
```

## Input Formats

### Standard FASTA
```
>protein1
MKTAYIAKQRQISFVKSHFSRQ...
>protein2
GSSGSSGAVVTGVTAVAVAQKT...
```

### AlphaFold3-Compatible Format
For complexes with non-protein molecules:
```
>Complex1|Prot1:Prot2:Ligand
PROTEINSEQ:PROTEINSEQ:ccd|ATP|2
```

Supported molecule types:
- `dna` - DNA sequences
- `rna` - RNA sequences
- `ccd` - Chemical Component Dictionary ID
- `smiles` - SMILES notation for small molecules

## Output Files

For each prediction:
- `.pdb` - Structure coordinates
- `.json` - Detailed prediction metrics (pLDDT, PAE, etc.)
- `.png` - Structure visualization with confidence coloring
- `_relaxed.pdb` - AMBER-relaxed structure (if `--amber` used)

**Note**: pLDDT confidence scores populate B-factor column in PDB files.

## Common Usage Examples

### Single sequence prediction
```bash
colabfold_batch protein.fasta results/
```

### Batch prediction with local databases
```bash
colabfold_search sequences.fasta /db/colabfold msas/
colabfold_batch msas/ predictions/
```

### Protein complex prediction
```bash
# Input FASTA with chains separated by ':'
>complex
CHAINASEQ:CHAINBSEQ
```

### High-quality prediction with relaxation
```bash
colabfold_batch input.fasta output/ --amber --num-recycle 5
```

### MSA-only for later use
```bash
colabfold_batch sequences.fasta msas/ --msa-only
colabfold_batch msas/ structures/ --num-models 3
```

### GPU-accelerated with templates
```bash
colabfold_batch input.fasta output/ --templates --use-gpu-relax
```

## Hardware Requirements

### Memory Guidelines
- **Tesla T4 GPU (~16GB VRAM)**: Max ~2000 residues
- Actual limits depend on sequence length and model complexity
- Check GPU type: `nvidia-smi`

### Storage Requirements
- Local databases: ~940GB
- Predictions: ~5-50MB per structure (varies with output flags)

## Performance Tips

### For Small-Scale Work
- Use public MSA server with `colabfold_batch` directly
- Quick testing and validation workflows

### For Large-Scale Batch Processing
- Download local databases for offline operation
- Use `colabfold_search` + `colabfold_batch` for efficiency
- Avoid repeated MSA generation for same sequences

### GPU Optimization
- Use `--use-gpu-relax` for faster AMBER relaxation
- Set `CUDA_VISIBLE_DEVICES` to control GPU allocation
- Run multiple predictions in parallel on different GPUs

### MSA Server Usage
- Serial single-IP access required for public server
- Rate limiting applies to prevent overuse
- Consider local databases for high-throughput work

## Typical Workflow

1. Prepare FASTA input (proteins, complexes, or multi-chain systems)
2. Generate MSAs (via server or local databases)
3. Run structure prediction with desired models
4. Optional: AMBER relaxation for refinement
5. Analyze confidence scores (pLDDT, PAE) in JSON output
6. Visualize structures using provided PNG or external tools

## Limitations

- Public MSA server has rate limits and requires serial access
- Google Colab free tier has runtime limits
- Memory constraints limit maximum sequence length
- Complex predictions may require multiple GPU hours
