# Chai-1 API Reference

## Python API

### Basic usage

```python
from chai_lab.chai1 import run_inference

# Simple prediction
run_inference(
    fasta_file="complex.fasta",
    output_dir="predictions/",
    num_trunk_recycles=3
)
```

### Full parameter reference

```python
run_inference(
    # Required
    fasta_file: str,           # Path to FASTA file
    output_dir: str,           # Output directory

    # Recycling
    num_trunk_recycles: int = 3,      # Structure recycles (1-10)
    num_diffn_timesteps: int = 200,   # Diffusion steps (50-500)

    # Sampling
    seed: int = 0,                    # Random seed
    num_diffn_samples: int = 5,       # Number of samples per model

    # Constraints (optional)
    constraint_file: str = None,      # Restraints file path

    # Resources
    device: str = "cuda",             # Device (cuda/cpu)
)
```

## CLI usage

```bash
# Basic prediction
chai-lab predict \
    --fasta complex.fasta \
    --output predictions/

# With options
chai-lab predict \
    --fasta complex.fasta \
    --output predictions/ \
    --num-trunk-recycles 5 \
    --num-diffn-timesteps 300 \
    --seed 42
```

## FASTA format specifications

### Protein-protein complex
```
>protein_A
MKTAYIAKQRQISFVKSHFSRQLE...
>protein_B
MVLSPADKTNVKAAWGKVGAHAGE...
```

### Protein-ligand complex
```
>protein
MKTAYIAKQRQISFVKSHFSRQLE...
>ligand|smiles
CCO
```

### Protein-DNA complex
```
>protein
MKTAYIAKQRQISFVKSHFSRQLE...
>dna
ATCGATCGATCG
```

### Protein-RNA complex
```
>protein
MKTAYIAKQRQISFVKSHFSRQLE...
>rna
AUCGAUCGAUCG
```

### Modified residues
```
>protein
MKTAYIAKQRQISFVK[SEP]SHFSRQLE...
```

## Output format

```
predictions/
├── pred.model_idx_0.cif    # Best prediction (CIF)
├── pred.model_idx_1.cif    # Second prediction
├── pred.model_idx_2.cif    # Third prediction
├── scores.json             # Confidence metrics
├── pae.npy                 # PAE matrix (NxN)
└── plddt.npy               # pLDDT per residue
```

### scores.json format
```json
{
    "ptm": 0.85,
    "iptm": 0.72,
    "ranking_score": 0.78
}
```

## Restraints file format

```yaml
# restraints.yaml
distance_restraints:
  - chain_a: "A"
    residue_a: 45
    atom_a: "CA"
    chain_b: "B"
    residue_b: 12
    atom_b: "CA"
    distance: 8.0
    tolerance: 2.0
```

## API response objects

### PredictionResult
```python
result = PredictionResult(
    structure: Structure,      # BioPython Structure
    plddt: np.ndarray,        # Shape: (n_residues,)
    pae: np.ndarray,          # Shape: (n_residues, n_residues)
    ptm: float,               # Global TM-score
    iptm: float,              # Interface TM-score
)
```

## Error handling

```python
from chai_lab.chai1 import run_inference, ChaiError

try:
    result = run_inference(
        fasta_file="complex.fasta",
        output_dir="predictions/"
    )
except ChaiError as e:
    print(f"Prediction failed: {e}")
```

## Memory requirements

| Complex Size | Recommended GPU |
|--------------|-----------------|
| < 500 residues | A10G (24GB) |
| 500-1000 residues | A100 (40GB) |
| > 1000 residues | A100-80GB |

## Batch processing

```python
from pathlib import Path

fastas = Path("sequences/").glob("*.fasta")
for fasta in fastas:
    run_inference(
        fasta_file=str(fasta),
        output_dir=f"predictions/{fasta.stem}/"
    )
```
