# Protein Design QC Checklist

## Pre-design QC

### Target preparation
- [ ] PDB downloaded from RCSB or AlphaFold DB
- [ ] Correct chain selected
- [ ] Waters and ligands removed (unless needed)
- [ ] Missing residues identified
- [ ] Hotspot residues verified (surface accessible)
- [ ] Target trimmed to binding region + 10A buffer

### Hotspot selection
- [ ] 3-6 residues selected
- [ ] Residues are surface-exposed (SASA > 20 A^2)
- [ ] Mix of charged/aromatic preferred (K, R, E, D, W, Y, F)
- [ ] Residue numbering matches PDB

## Post-backbone QC (RFdiffusion)

### Visual inspection
- [ ] Secondary structure present (helices/sheets)
- [ ] No severe clashes with target
- [ ] Backbone connects hotspots appropriately
- [ ] Reasonable topology (compact, no extended loops)

### Diversity check
- [ ] Generate 100-500 backbones
- [ ] Visual inspection of 10+ diverse samples
- [ ] Cluster if needed (RMSD-based)

## Post-sequence QC (ProteinMPNN)

### Structure metrics
| Metric | Threshold | Action if Fail |
|--------|-----------|----------------|
| pLDDT | > 0.85 | Increase num_designs |
| pTM | > 0.70 | Check backbone quality |
| scRMSD | < 2.0 A | Sequence may not match backbone |

### Interface metrics
| Metric | Threshold | Action if Fail |
|--------|-----------|----------------|
| ipTM | > 0.50 | Check hotspots, try different backbone |
| iPAE | < 10 | Interface not confident |
| SC | > 0.50 | Poor shape match |

### Sequence metrics
| Metric | Threshold | Action if Fail |
|--------|-----------|----------------|
| ESM2 PLL | > 0.0 (normalized) | Sequence implausible |
| Instability Index | < 40 | Unstable protein |
| GRAVY | < 0.4 | Too hydrophobic |
| Deamidation sites | minimize | Check NG, NS motifs |

## Final selection QC

### Composite score
```python
score = (
    0.30 * pLDDT +
    0.20 * ipTM +
    0.20 * (1 - PAE/20) +
    0.15 * SC +
    0.15 * ESM2_PLL
)
```

### Diversity
- [ ] Cluster sequences (70% identity)
- [ ] Select representatives from each cluster
- [ ] Ensure diverse backbones represented

### Manufacturability
- [ ] No poly-K/R runs (> 3 consecutive)
- [ ] Even number of cysteines
- [ ] Reasonable length (< 150 AA for E. coli)
- [ ] No N-terminal Q (pyroglutamate risk)

## Experimental validation plan

### Tier 1: Expression Screen (10-50 designs)
- Express in E. coli or CFPS
- Check solubility (SDS-PAGE)
- Target: > 50% soluble expression

### Tier 2: Binding Screen (5-20 designs)
- SPR or BLI binding
- Target: detectable binding

### Tier 3: Affinity Measurement (1-5 designs)
- Full kinetic characterization
- Target: KD < 100 nM

## Common failure modes

| Failure | Checkpoint | Solution |
|---------|------------|----------|
| Low expression | Instability Index > 40 | Use SolubleMPNN |
| Aggregation | GRAVY > 0.4 | Lower surface hydrophobicity |
| No binding | ipTM < 0.5 | Better hotspots, more designs |
| Weak binding | All metrics pass | More diverse sequences |

## Metric limitations

**IMPORTANT**: In-silico metrics are filters, not affinity predictors.
- Individual metrics have weak predictive power (AUC ~0.65)
- Composite scores improve but don't predict affinity
- Always validate experimentally
