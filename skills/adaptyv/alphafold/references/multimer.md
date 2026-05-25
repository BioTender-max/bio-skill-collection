# AlphaFold-Multimer Guide

## Overview

AlphaFold-Multimer predicts structures of protein complexes. Essential for validating binder designs against targets.

## FASTA Format

### Heteromer (Different Chains)
```
>chain_A
MKTAYIAKQRQISFVKSHFSRQLE...
>chain_B
MVLSPADKTNVKAAWGKVGAHAGE...
```

### Homomer (Identical Chains)
```
>monomer
MKTAYIAKQRQISFVKSHFSRQLE...
```
Use `--num_multimer_predictions_per_model=N` for N copies.

### Stoichiometry
For A2B complex (2 copies of A, 1 copy of B):
```
>chain_A
SEQUENCE_A
>chain_A
SEQUENCE_A
>chain_B
SEQUENCE_B
```

## Key parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--model_preset` | multimer | Required for complexes |
| `--num_multimer_predictions_per_model` | 5 | Predictions per model |
| `--num_recycle` | 3 | Recycling iterations |

## ipTM interpretation

ipTM (interface predicted TM-score) measures interface confidence:

| ipTM | Interpretation |
|------|----------------|
| < 0.3 | No interaction predicted |
| 0.3-0.5 | Weak/uncertain interaction |
| 0.5-0.7 | Moderate confidence |
| > 0.7 | High confidence interaction |

## PAE analysis for interfaces

### Reading PAE plots
- X-axis: Aligned residue position
- Y-axis: Scored residue position
- Color: Expected position error (A)

### Interface PAE
Extract interface PAE by selecting cross-chain blocks:
```python
# For chains A (0:100) and B (100:200)
interface_pae = pae[0:100, 100:200]  # A->B
mean_interface_pae = interface_pae.mean()
# Good: < 10 A
```

## Complex types

### Binder-Target
- Most common validation scenario
- Target typically has known structure
- ipTM assesses binding confidence

### Multivalent complexes
- Multiple binders on one target
- Check each interface independently
- Watch for inter-binder clashes

### Symmetric oligomers
- Use identical sequences
- Check for correct symmetry
- Verify interfaces match design

## Ranking models

AF2-Multimer returns multiple models. Ranking criteria:
1. **ipTM * 0.8 + pTM * 0.2** (default)
2. Select model with highest composite score
3. Also check PAE for interface confidence

## Common issues

### No predicted interaction
- ipTM < 0.3 suggests no binding
- May indicate:
  - Poor binder design
  - Wrong chain order
  - Incompatible sequences

### Incorrect stoichiometry
- Chains may form unexpected assemblies
- Check contact maps
- Verify interface positions

### MSA contamination
- If target is in training set, mask templates
- Use `--max_template_date` before target deposition

## Batch processing

For many sequences:
```bash
# Prepare FASTA files
for seq in sequences/*.fasta; do
  python run_alphafold.py \
    --fasta_paths="$seq" \
    --output_dir="output/$(basename $seq .fasta)" \
    --model_preset=multimer
done
```

## Integration with design pipeline

1. Generate binder backbones (RFdiffusion)
2. Design sequences (ProteinMPNN)
3. Predict complex (AF2-Multimer)
4. Filter: ipTM > 0.5, PAE_interface < 10
5. Calculate self-consistency RMSD
6. Select top designs for experimental testing

## Output parsing script

```python
import json
import glob

results = []
for pkl_path in glob.glob('output/*/ranking_debug.json'):
    with open(pkl_path) as f:
        ranking = json.load(f)

    design_name = pkl_path.split('/')[1]
    iptm = ranking['iptm']
    ptm = ranking['ptm']

    results.append({
        'name': design_name,
        'iptm': iptm,
        'ptm': ptm,
        'score': 0.8 * iptm + 0.2 * ptm
    })

# Sort by score
results.sort(key=lambda x: x['score'], reverse=True)
```
