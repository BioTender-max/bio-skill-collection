# ProteinMPNN Temperature Guide

## Understanding temperature

Temperature controls the diversity of generated sequences. Lower temperatures produce more conservative, higher-recovery sequences. Higher temperatures produce more diverse but potentially less stable sequences.

## Temperature effects

| Temperature | Diversity | Recovery | Use Case |
|-------------|-----------|----------|----------|
| 0.0001 | Minimal | ~95% | Near-native recovery |
| 0.1 | Low | ~85-90% | Production designs |
| 0.2 | Moderate | ~75-85% | Default, balanced |
| 0.3 | High | ~65-75% | Exploration |
| 0.5 | Very high | ~50-65% | Maximum diversity |
| 1.0 | Extreme | ~30-50% | Random-like |

## Recommendations by application

### Binder design
```bash
--sampling_temp "0.1"   # Low diversity, high confidence
```
- Focus on high-quality sequences
- 8-16 sequences per backbone
- Filter by ESM2 PLL and pLDDT

### Enzyme redesign
```bash
--sampling_temp "0.2"   # Moderate diversity
```
- Need to sample functional variants
- 32-64 sequences
- Screen for activity

### Diversity library
```bash
--sampling_temp "0.3"   # Higher diversity
```
- Maximize sequence space
- 64-128 sequences
- For directed evolution

### Structure recovery testing
```bash
--sampling_temp "0.0001"  # Near-deterministic
```
- Validate backbone quality
- Check if backbone can specify sequence

## Temperature scaling

### Per-position temperature
Not directly supported, but can achieve similar effect:
1. Run with high temperature
2. Fix certain positions
3. Run again with low temperature

### Multi-temperature sampling
```bash
# Generate diverse library
for temp in 0.1 0.2 0.3; do
  python protein_mpnn_run.py \
    --sampling_temp "$temp" \
    --out_folder "output_temp_$temp" \
    --num_seq_per_target 16
done
```

## Quality metrics at different temperatures

### Low temperature (0.1)
- Higher pLDDT predictions
- Better ESM2 PLL scores
- Less structural diversity
- More predictable behavior

### High temperature (0.3+)
- More sequence diversity
- Some low-quality sequences
- Requires more aggressive filtering
- May discover novel solutions

## Temperature vs. number of sequences

| Goal | Temperature | Num Sequences |
|------|-------------|---------------|
| Best single design | 0.1 | 8-16, pick best |
| Robust hit | 0.1 | 32-64, filter |
| Diversity panel | 0.2 | 64-128 |
| Evolution seed | 0.3 | 128-256 |

## Common mistakes

### Wrong: Float instead of string
```bash
--sampling_temp 0.1   # May cause issues
```

### Correct: String
```bash
--sampling_temp "0.1"  # Correct
```

### Wrong: Too high temperature
```bash
--sampling_temp "0.8"  # Produces many poor sequences
```

### Better: Moderate with filtering
```bash
--sampling_temp "0.2" --num_seq_per_target 64
# Then filter for best
```

## Integration with QC

After sequence generation, filter by:
1. ESM2 pseudo-log-likelihood (normalized > 0.0)
2. AlphaFold2 pLDDT (> 0.85)
3. Self-consistency RMSD (< 2.0 A)

See protein-qc skill for detailed thresholds.
