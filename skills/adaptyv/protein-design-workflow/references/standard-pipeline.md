# Standard Binder Design Pipeline

## Pipeline overview

```
Target Prep → Backbone Generation → Sequence Design → Validation → Filtering
    |              |                     |               |            |
  (pdb)      (rfdiffusion)         (proteinmpnn)    (alphafold)  (protein-qc)
```

## Phase 1: Target preparation

### Step 1.1: Obtain structure
```bash
# From PDB
curl -o target.pdb "https://files.rcsb.org/download/XXXX.pdb"

# Or use AlphaFold DB for modeled structures
curl -o target.pdb "https://alphafold.ebi.ac.uk/files/AF-PXXXXX-F1-model_v4.pdb"
```

### Step 1.2: Clean structure
```python
from Bio.PDB import PDBParser, PDBIO, Select

# Extract target chain
class ChainSelect(Select):
    def accept_chain(self, chain):
        return chain.id == 'A'

parser = PDBParser()
structure = parser.get_structure('target', 'target.pdb')
io = PDBIO()
io.set_structure(structure)
io.save('target_chain_A.pdb', ChainSelect())
```

### Step 1.3: Identify hotspots
- Select 3-6 surface-exposed residues
- Prefer charged/aromatic (K, R, E, D, W, Y, F)
- Check SASA > 20 A^2
- Record residue numbers (verify against PDB)

**Output**: `target_prepared.pdb`, hotspot list (e.g., "A45,A67,A89")

---

## Phase 2: Backbone generation

### Option A: RFdiffusion (Diverse Exploration)
```bash
modal run modal_rfdiffusion.py \
    --pdb target_prepared.pdb \
    --contigs "A1-150/0 70-100" \
    --hotspot "A45,A67,A89" \
    --num-designs 500
```

**Output**: 500 backbone PDBs

### Option B: BindCraft (End-to-End)
```bash
modal run modal_bindcraft.py \
    --target-pdb target_prepared.pdb \
    --hotspots "A45,A67,A89" \
    --num-designs 100
```

**Output**: 100 designed binders with sequences

---

## Phase 3: Sequence design

### For RFdiffusion Backbones
```bash
# Batch process all backbones
for backbone in backbones/*.pdb; do
    modal run modal_proteinmpnn.py \
        --pdb-path "$backbone" \
        --num-seq-per-target 8 \
        --sampling-temp 0.1
done
```

**Output**: 8 sequences per backbone (4000 total from 500 backbones)

---

## Phase 4: Structure prediction

### Prepare complexes
```python
# Combine binder sequence with target sequence
def make_complex_fasta(binder_seq, target_seq, output_path):
    with open(output_path, 'w') as f:
        f.write(f">binder\n{binder_seq}\n>target\n{target_seq}\n")
```

### Run validation
```bash
modal run modal_colabfold.py \
    --input-faa all_complexes.fasta \
    --out-dir predictions/
```

**Output**: pLDDT, ipTM, PAE for each design

---

## Phase 5: Filtering

### Stage 1: Structure Confidence
```python
designs = designs[designs['pLDDT'] > 0.85]
```

### Stage 2: Self-Consistency
```python
designs = designs[designs['scRMSD'] < 2.0]
```

### Stage 3: Interface Quality
```python
designs = designs[
    (designs['ipTM'] > 0.50) &
    (designs['PAE_interface'] < 10)
]
```

### Stage 4: Sequence Quality
```python
designs = designs[designs['esm2_pll_normalized'] > 0.0]
```

### Stage 5: Composite Ranking
```python
designs['score'] = (
    0.30 * designs['pLDDT'] +
    0.20 * designs['ipTM'] +
    0.20 * (1 - designs['PAE_interface'] / 20) +
    0.15 * designs['shape_complementarity'] +
    0.15 * designs['esm2_pll_normalized']
)
top_designs = designs.nlargest(100, 'score')
```

**Output**: 50-200 filtered candidates

---

## Resource estimates

| Phase | GPU | Time (500 designs) |
|-------|-----|-------------------|
| RFdiffusion | A10G | 2-3 hours |
| ProteinMPNN | T4 | 1-2 hours |
| ColabFold | A100 | 12-24 hours |
| Filtering | CPU | 30 min |

**Total**: 16-30 hours for 500 backbone campaign

---

## Troubleshooting

| Issue | Phase | Solution |
|-------|-------|----------|
| No good backbones | 2 | Check hotspots, increase designs |
| Low ipTM | 4 | Try different hotspots |
| All filtered out | 5 | Relax thresholds, generate more |
| High scRMSD | 4 | Backbone may be unusual |

---

## Quality checkpoints

### After backbone generation
- [ ] Visual inspection of 10+ samples
- [ ] Secondary structure present
- [ ] No clashes with target

### After sequence design
- [ ] ESM2 PLL > 0.0 for most sequences
- [ ] Reasonable sequence diversity

### After validation
- [ ] pLDDT > 0.85
- [ ] ipTM > 0.50
- [ ] scRMSD < 2.0

### Final selection
- [ ] Diverse sequences (cluster if needed)
- [ ] Manufacturable (no problematic motifs)
- [ ] Ready for experimental testing
