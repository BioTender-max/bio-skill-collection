# Binding QC

**Purpose**: Assess interface quality and binding geometry

## Critical caveat

**From BindCraft documentation**: "NONE of the current computational metrics are predictive of affinity in any way."

These metrics filter structurally viable binders, not high-affinity ones. A design passing all thresholds has higher probability of success, but success is not guaranteed.

---

## Metric-level QC (calculated values)

### Deep learning metrics (AF2/Chai/Boltz)

| Metric | Standard | Stringent | Interpretation |
|--------|----------|-----------|----------------|
| ipTM | > 0.50 | > 0.60 | Interface predicted TM-score (0-1) |
| PAE_interaction | < 12 A | < 10 A | Cross-chain alignment error |
| pLDDT_interface | > 0.80 | > 0.85 | Interface residue confidence |

**ipTM Interpretation:**
- > 0.8: Very high confidence interface
- 0.6-0.8: Good confidence
- 0.5-0.6: Marginal
- < 0.5: Poor interface

**PAE Interpretation:**
- < 5 A: Very high confidence
- 5-10 A: Good confidence
- 10-15 A: Moderate
- > 15 A: Low confidence

### PyRosetta physics metrics

| Metric | Standard | Stringent | Description |
|--------|----------|-----------|-------------|
| Shape Complementarity (SC) | > 0.50 | > 0.60 | Surface packing quality (0-1) |
| interface_dG | < -10 kcal/mol | < -15 | Binding energy (favorable) |
| dSASA | > 800 A^2 | > 1000 | Buried surface area |
| interface_hbonds | > 2 | > 4 | Hydrogen bonds at interface |
| interface_nres | > 6 | > 10 | Interface residue count |
| unsaturated_hbonds | < 6 | < 4 | Buried polar without H-bonds |
| PackStat | > 0.65 | > 0.70 | Interface packing quality (0-1) |

### Computing PyRosetta metrics

```python
from pyrosetta import init, pose_from_pdb
from pyrosetta.rosetta.protocols.analysis import InterfaceAnalyzerMover

init()
pose = pose_from_pdb("complex.pdb")
analyzer = InterfaceAnalyzerMover("A_B")  # Interface between chains A and B
analyzer.apply(pose)

print(f"dG: {analyzer.get_interface_dG():.2f} kcal/mol")
print(f"dSASA: {analyzer.get_interface_delta_sasa():.0f} A^2")
print(f"SC: {analyzer.get_interface_sc():.2f}")
print(f"H-bonds: {analyzer.get_interface_hbonds()}")
print(f"Interface residues: {analyzer.get_interface_nres()}")
print(f"Unsaturated H-bonds: {analyzer.get_interface_unsat_hbonds()}")
print(f"PackStat: {analyzer.get_packstat():.2f}")
```

---

## Design-level QC (pattern detection)

| Check | What it finds | Risk | Recommendation |
|-------|---------------|------|----------------|
| Hotspot coverage | Interface covers target hotspots | Low contact = weak binding | Verify >= 50% hotspot contact |
| Interface composition | Charged/polar vs hydrophobic | Imbalance | Mix ~50% polar at interface |
| Interface hydrophobic patches | Exposed hydrophobic areas | Aggregation | Check surface hydrophobicity < 0.37 |

### Hotspot coverage check

```python
def check_hotspot_coverage(design_contacts, hotspot_residues):
    """
    Verify designed interface contacts target hotspots.

    Args:
        design_contacts: Set of target residues contacted by binder
        hotspot_residues: Set of target hotspot residues

    Returns:
        float: Fraction of hotspots contacted
    """
    contacted = len(design_contacts & hotspot_residues)
    total = len(hotspot_residues)
    coverage = contacted / total if total > 0 else 0

    if coverage < 0.5:
        print(f"WARNING: Only {coverage:.0%} hotspot coverage")

    return coverage
```

---

## Filtering strategy for binding

### Sequential filter order

1. **ipTM > 0.50** - Primary binding confidence
2. **PAE_interaction < 10** - Interface alignment
3. **SC > 0.50** - Geometric fit (if available)
4. **interface_dG < -10** - Physics-based energy (if available)

### BindCraft Filter Levels

| Level | ipTM | PAE | SC | Use Case |
|-------|------|-----|-----|----------|
| Default | > 0.5 | < 10 | > 0.5 | Standard binder design |
| Relaxed | > 0.4 | < 12 | > 0.45 | Need more designs |
| Peptide | > 0.35 | < 15 | > 0.4 | Designs < 30 AA |

**Peptide binders**: Expect ~5-10x lower success rate with relaxed thresholds.

---

## Common issues

### Low ipTM

**Causes:**
- Poor hotspot selection
- Insufficient interface contacts
- Binder not folding correctly

**Solutions:**
- Review hotspot residues (surface-exposed, conserved)
- Increase binder length
- Try different backbone topologies
- Generate more designs

### High PAE despite good ipTM

**Causes:**
- Flexible regions at interface
- Multiple binding modes
- Poor sequence-structure match

**Solutions:**
- Check scRMSD (should be < 2.0)
- Examine PAE matrix for specific problem regions
- Try designs with more rigid interfaces

### Poor shape complementarity

**Causes:**
- Large cavities at interface
- Poor surface matching

**Solutions:**
- Try different backbone conformations
- Increase sampling (more designs)
- Consider flexible backbone design
