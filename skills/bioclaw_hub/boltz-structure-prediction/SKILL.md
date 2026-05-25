---
name: boltz-structure-prediction
description: >
  Boltz-1 / Boltz-2 structure prediction for proteins, complexes, and ligand-aware validation.
  Use this skill when: (1) Predicting protein complex structures,
  (2) Validating designed binders,
  (3) Need open-source alternative to AF2,
  (4) Predicting protein-ligand complexes,
  (5) Using local GPU resources.

  For QC thresholds, use protein-design-qc.
  For AlphaFold2 prediction, use alphafold2-multimer.
  For Chai prediction, use chai1-structure-prediction.
license: MIT
category: design-tools
tags: [structure-prediction, validation, open-source]
biomodals_script: modal_boltz.py
---

# Boltz-1 / Boltz-2 Structure Prediction

**Plain-language role**: Use Boltz when you want an open-source structure predictor for protein or protein-ligand validation.

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.10+ | 3.11 |
| CUDA | 12.0+ | 12.1+ |
| GPU VRAM | 24GB | 48GB (L40S) |
| RAM | 32GB | 64GB |

## How to run

> **First time?** See [Installation Guide](../../docs/installation.md) to set up Modal and biomodals.

### Option 1: Modal
```bash
cd biomodals
modal run modal_boltz.py \
  --input-faa complex.fasta \
  --out-dir predictions/
```

**GPU**: L40S (48GB) | **Timeout**: 1800s default

### Option 2: Local installation
```bash
pip install boltz-structure-prediction

boltz-structure-prediction predict \
  --fasta complex.fasta \
  --output predictions/
```

## Key parameters

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `--recycling_steps` | 3 | 1-10 | Recycling iterations |
| `--sampling_steps` | 200 | 50-500 | Diffusion steps |
| `--use_msa_server` | true | bool | Use MSA server |

## FASTA Format

```
>protein_A
MKTAYIAKQRQISFVK...
>protein_B
MVLSPADKTNVKAAWG...
```

## Output format

```
predictions/
├── model_0.cif       # Best model (CIF format)
├── confidence.json   # pLDDT, pTM, ipTM
└── pae.npy          # PAE matrix
```

**Note**: Boltz outputs CIF format. Convert to PDB if needed:
```python
from Bio.PDB import MMCIFParser, PDBIO
parser = MMCIFParser()
structure = parser.get_structure("model", "model_0.cif")
io = PDBIO()
io.set_structure(structure)
io.save("model_0.pdb")
```

## Comparison

| Feature | Boltz-1 | Boltz-2 | AF2-Multimer |
|---------|---------|---------|--------------|
| MSA-free mode | Yes | Yes | No |
| Diffusion | Yes | Yes | No |
| Speed | Fast | Faster | Slower |
| Open source | Yes | Yes | Yes |

## Sample output

### Successful run
```
$ boltz-structure-prediction predict --fasta complex.fasta --output predictions/
[INFO] Loading Boltz-1 weights...
[INFO] Predicting structure...
[INFO] Saved model to predictions/model_0.cif

predictions/confidence.json:
{
  "ptm": 0.78,
  "iptm": 0.65,
  "plddt": 0.81
}
```

**What good output looks like:**
- pTM: > 0.7 (confident global structure)
- ipTM: > 0.5 (confident interface)
- pLDDT: > 0.7 (confident per-residue)
- CIF file: ~100-500 KB for typical complex

## Decision tree

```
Should I use Boltz?
│
├─ What are you predicting?
│  ├─ Protein-protein complex → Boltz ✓ or Chai or ColabFold
│  ├─ Protein + ligand → Boltz ✓ or Chai
│  └─ Single protein → Use ESMFold (faster)
│
├─ Need MSA?
│  ├─ No / want speed → Boltz ✓
│  └─ Yes / maximum accuracy → ColabFold
│
└─ Why Boltz over Chai?
   ├─ Open weights preference → Boltz ✓
   ├─ Boltz-2 speed → Boltz ✓
   └─ DNA/RNA support → Consider Chai
```

## Typical performance

| Campaign Size | Time (L40S) | Cost (Modal) | Notes |
|---------------|-------------|--------------|-------|
| 100 complexes | 30-45 min | ~$8 | Standard validation |
| 500 complexes | 2-3h | ~$35 | Large campaign |
| 1000 complexes | 4-6h | ~$70 | Comprehensive |

**Per-complex**: ~15-30s for typical binder-target complex.

---

## Verify

```bash
find predictions -name "*.cif" | wc -l  # Should match input count
```

---

## Troubleshooting

**Low confidence**: Increase recycling_steps
**OOM errors**: Use MSA-free mode or A100-80GB
**Slow prediction**: Reduce sampling_steps

### Error interpretation

| Error | Cause | Fix |
|-------|-------|-----|
| `RuntimeError: CUDA out of memory` | Complex too large | Use `--use_msa_server false` or larger GPU |
| `KeyError: 'iptm'` | Single chain only | Ensure FASTA has 2+ chains |
| `FileNotFoundError: weights` | Missing model | Run `boltz-structure-prediction download` first |
| `ValueError: invalid residue` | Non-standard AA | Check for modified residues in sequence |

### Boltz-1 vs Boltz-2

| Aspect | Boltz-1 | Boltz-2 |
|--------|---------|---------|
| Speed | Fast | ~2x faster |
| Accuracy | Good | Improved |
| Ligands | Basic | Better support |
| Release | 2024 | Late 2024 |

---

**Next**: `protein-design-qc` for filtering and ranking.

## Inputs

- Protein or complex sequences, optionally with ligands or cofactors depending on the prediction task.
- A chosen Boltz model version, runtime settings, and output directory.
- GPU-enabled environment or Modal configuration for prediction runs.

## Outputs

- Predicted structures and confidence artifacts for each sampled model.
- Confidence metrics suitable for downstream QC, including interface-aware scores on complexes.
- A ranked set of validation structures for design triage.

## Next Step

Filter the resulting predictions with `protein-design-qc` and compare top candidates against `chai1-structure-prediction` or `alphafold2-multimer` when needed.
