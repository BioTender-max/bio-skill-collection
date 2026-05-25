# Boltz

Biomolecular interaction model for structure prediction and binding affinity estimation.

## Official Documentation

- GitHub: https://github.com/jwohlwend/boltz
- Paper: https://www.biorxiv.org/content/10.1101/2024.11.19.624167v1
- Website: https://boltz.ai

## Installation

### PyPI (Recommended)
```bash
# With CUDA support
pip install boltz[cuda] -U

# CPU only or non-CUDA GPU
pip install boltz -U
```

### From GitHub
```bash
git clone https://github.com/jwohlwend/boltz.git
cd boltz

# With CUDA support
pip install -e .[cuda]

# Without CUDA
pip install -e .
```

**Important**: Install in a fresh Python environment to avoid dependency conflicts.

## Key Commands

### Basic Prediction
```bash
boltz predict input_path --use_msa_server
```

### Help and Options
```bash
boltz predict --help
```

## Command-Line Flags

### Input/Output

| Flag | Description | Example |
|------|-------------|---------|
| `input_path` | Single YAML file or directory of YAML files | `boltz predict structures.yaml` |
| `--output` | Output directory path | `--output results/` |
| `--use_msa_server` | Use MSA generation server | `--use_msa_server` |

### MSA Server Authentication
Credentials can be provided through configuration when using protected MSA servers.

### Batch Processing
```bash
# Directory of YAML files
boltz predict input_configs/ --use_msa_server
```

## Input Format

YAML files describing biomolecular systems and prediction tasks.

Example structure (refer to official documentation for detailed specifications):
```yaml
# Protein-ligand complex prediction with affinity
sequences:
  - id: protein1
    type: protein
    sequence: MKTAYIAKQRQISFVKSHFSRQ...
  - id: ligand1
    type: small_molecule
    smiles: CC(C)CC1=CC=C(C=C1)C(C)C(=O)O

prediction:
  affinity: true
```

See project prediction instructions for complete YAML schema.

## Output Format

### Structure Files
- Standard biomolecular structure formats
- Confidence scores and quality metrics

### Affinity Predictions

| Output Field | Range | Description | Use Case |
|--------------|-------|-------------|----------|
| `affinity_probability_binary` | 0-1 | Probability ligand is a binder | Hit-discovery screening |
| `affinity_pred_value` | log₁₀(IC₅₀) μM | Binding affinity prediction | Lead optimization |

## Common Usage Examples

### Protein Structure Prediction
```bash
boltz predict protein.yaml --use_msa_server
```

### Protein-Ligand Complex with Affinity
```bash
# YAML specifies protein, ligand, and affinity=true
boltz predict complex_with_affinity.yaml --use_msa_server
```

### Batch Prediction
```bash
# Process all YAML files in directory
boltz predict input_configs/ --use_msa_server --output predictions/
```

### Without MSA Server
```bash
# For pre-generated MSAs or single-sequence prediction
boltz predict input.yaml
```

## Typical Use Cases

### 1. Biomolecular Structure Prediction
Predict 3D structures of:
- Proteins
- Nucleic acids (DNA/RNA)
- Protein complexes
- Protein-nucleic acid complexes

### 2. Binding Affinity Screening
**Hit Discovery Phase**:
- Screen large compound libraries
- Use `affinity_probability_binary` to identify potential binders
- Filter candidates with probability > threshold (e.g., 0.7)

**Lead Optimization Phase**:
- Rank candidate compounds
- Use `affinity_pred_value` for quantitative comparison
- Prioritize compounds with favorable IC₅₀ predictions

### 3. Drug Discovery Workflows
- Virtual screening of ligand libraries
- Structure-based optimization
- Affinity-guided compound refinement
- Hit-to-lead progression

### 4. Protein-Protein Interaction Prediction
- Predict complex structures
- Estimate binding interfaces
- Guide experimental validation

## Performance Tips

- Use fresh Python environment to avoid dependency conflicts
- MSA server access speeds up prediction for novel sequences
- Batch processing multiple YAML files in single command for efficiency
- GPU acceleration recommended for large-scale predictions

## Workflow Integration

### Typical Drug Discovery Pipeline
1. **Target Selection**: Define protein target and binding site
2. **Ligand Preparation**: Compile library of candidate molecules (SMILES)
3. **Structure Prediction**: Generate protein-ligand complexes
4. **Affinity Screening**: Filter by `affinity_probability_binary`
5. **Lead Ranking**: Sort top hits by `affinity_pred_value`
6. **Experimental Validation**: Test prioritized compounds

### Protein Complex Analysis
1. Prepare YAML with all complex components
2. Run prediction with MSA server for sequence coverage
3. Analyze predicted structure and confidence scores
4. Validate interface predictions experimentally

## Requirements

- Python environment (fresh installation recommended)
- CUDA support for GPU acceleration (optional)
- MSA server access for improved predictions (optional)
- YAML input files following Boltz specification

## Limitations

- Requires YAML configuration (learning curve for input format)
- MSA server dependency for optimal performance
- Affinity predictions are estimates (experimental validation recommended)
- Computational requirements scale with system complexity
