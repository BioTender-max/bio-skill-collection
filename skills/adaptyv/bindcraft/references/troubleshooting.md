# BindCraft Troubleshooting

## Common issues and solutions

### Low success rate

**Symptoms**: Few or no designs pass filtering

**Solutions**:
1. Increase `num_of_final_designs` (try 200-500)
2. Try relaxed filters for difficult targets
3. Verify hotspot residues are accessible
4. Check target PDB quality (no missing residues)

### Out of memory (OOM) errors

**Symptoms**: CUDA out of memory

**Solutions**:
1. Reduce `binder_length` range
2. Use L40S instead of A10G GPU
3. Reduce batch size
4. Trim target to binding region only

### Poor interface quality

**Symptoms**: Low ipTM scores consistently

**Solutions**:
1. Verify hotspot residues are surface-exposed
2. Check residue numbering matches PDB
3. Try different hotspot combinations
4. Increase `num_recycles` for AF2 validation

### Aggregation-prone designs

**Symptoms**: High surface hydrophobicity

**Solutions**:
1. Tighten `surface_hydrophobicity` threshold to 0.35
2. Check for hydrophobic patches on binder
3. Consider SolubleMPNN for sequence redesign

### Slow generation

**Symptoms**: Very long runtime

**Solutions**:
1. Reduce target PDB size (trim to binding region)
2. Use fewer `num_of_final_designs`
3. Reduce `num_recycles`
4. Use A100 GPU for faster inference

## Validation issues

### Designs pass in-silico but fail experimentally

**Possible Causes**:
1. Computational metrics don't predict affinity
2. Expression or solubility issues
3. Target flexibility not captured

**Solutions**:
1. Use sequence-level QC (instability index, GRAVY)
2. Validate with multiple structure predictors
3. Test diverse sequence clusters experimentally

### Inconsistent results between runs

**Solutions**:
1. Set explicit random seed
2. Use deterministic mode
3. Average metrics across multiple runs

## Error messages

### "Target chain not found"
- Verify chain ID in PDB matches configuration
- Check PDB has correct chain labels

### "Invalid hotspot residue"
- Residue number may not exist in PDB
- Residue may be missing atoms

### "AF2 prediction failed"
- Sequence may be too long
- GPU memory insufficient
- Try reducing complexity

## Performance tips

1. **Trim targets**: Only include binding region + 10A buffer
2. **Parallelize**: Run multiple campaigns simultaneously
3. **Early filtering**: Use quick metrics first, expensive ones later
4. **Cluster outputs**: Select diverse representatives for testing
