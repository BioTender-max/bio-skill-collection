# Complete Binder Design Walkthrough

End-to-end tutorial: Design a binder for IL-6 (PDB: 1ALU, chain A).

## Step 1: Prepare target

```bash
# Download PDB
curl -o 1alu.pdb "https://files.rcsb.org/download/1ALU.pdb"

# Extract chain A (target)
grep "^ATOM" 1alu.pdb | grep " A " > target_chainA.pdb
```

## Step 2: Identify hotspots

Criteria for good hotspots:
- Surface-exposed (accessible)
- Conserved across species
- Aromatic (Phe, Tyr, Trp) or charged (Arg, Lys, Glu)

For 1ALU chain A, good hotspots: **A42, A58, A62** (receptor binding interface)

## Step 3: Generate backbones

```bash
# Using Modal
modal run modal_rfdiffusion.py \
  --pdb target_chainA.pdb \
  --contigs "A1-185/0 70-90" \
  --hotspot "A42,A58,A62" \
  --num-designs 100

# Or locally
python run_inference.py \
  inference.input_pdb=target_chainA.pdb \
  contigmap.contigs=[A1-185/0 70-90] \
  ppi.hotspot_res=[A42,A58,A62] \
  inference.num_designs=100
```

**Expected output**: 100 PDB files in `output/`, ~25-35 min on A10G

## Step 4: Quick quality check

```bash
# Verify file count
ls output/*.pdb | wc -l  # Should be 100

# Check a design has secondary structure
pymol output/output_0.pdb
# Should see helices/sheets, not random coil
```

## Step 5: Design sequences (ProteinMPNN)

```bash
# Design sequences for each backbone
for pdb in output/output_*.pdb; do
  python ProteinMPNN/protein_mpnn_run.py \
    --pdb_path "$pdb" \
    --out_folder sequences/ \
    --num_seq_per_target 8 \
    --sampling_temp "0.1"
done
```

**Expected output**: 800 sequences (100 backbones × 8 sequences each)

## Step 6: Validate with structure prediction

```bash
# Combine sequences
cat sequences/seqs/*.fa > all_designs.fasta

# Predict structures with Chai/ColabFold
colabfold_batch all_designs.fasta predictions/ \
  --num-recycles 3 \
  --model-type alphafold2_multimer_v3
```

## Step 7: Filter results

Good binder criteria:
- **ipTM > 0.5** (interface confidence)
- **pLDDT > 0.7** (structural confidence)
- **No clashes** (visual inspection)

```python
import json
import glob

passing = []
for scores_file in glob.glob("predictions/*/scores*.json"):
    with open(scores_file) as f:
        scores = json.load(f)
    if scores.get("iptm", 0) > 0.5 and scores.get("ptm", 0) > 0.7:
        passing.append(scores_file)

print(f"Passing designs: {len(passing)}/800")  # Expect ~80-120 (10-15%)
```

## Expected results

| Stage | Input | Output | Pass Rate |
|-------|-------|--------|-----------|
| Backbone generation | 1 target | 100 backbones | 100% |
| Sequence design | 100 backbones | 800 sequences | 100% |
| Structure validation | 800 sequences | ~80-120 pass | 10-15% |

## Next steps

1. **Experimental testing**: Order top 10-20 designs
2. **Optimization**: Use passing designs as starting points
3. **Alternative approaches**: Try BindCraft for higher success rate

## Troubleshooting

| Problem | Solution |
|---------|----------|
| All random coil | Reduce noise_scale to 0.5-0.8 |
| No designs pass validation | Try different hotspots |
| Low diversity | Increase temperature to 0.2 |
