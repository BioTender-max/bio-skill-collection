# Structural QC

**Purpose**: Assess fold confidence and structural consistency

Structural QC validates that the designed sequence folds to the intended structure with high confidence.

---

## Metric-level QC (calculated values)

### Fold confidence metrics

| Metric | Source | Standard | Stringent | Interpretation |
|--------|--------|----------|-----------|----------------|
| pLDDT | AF2/ESMFold/Chai/Boltz | > 0.85 | > 0.90 | Per-residue confidence |
| pTM | AF2/Chai/Boltz | > 0.70 | > 0.80 | Global fold quality |
| pLDDT_binder | AF2 (binder alone) | > 0.85 | > 0.90 | Binder folds independently |

### Self-consistency metrics

| Metric | Standard | Stringent | Interpretation |
|--------|----------|-----------|----------------|
| scRMSD | < 2.0 A | < 1.5 A | Designed vs predicted backbone |
| Binder RMSD | < 2.5 A | < 2.0 A | Binder alone vs in complex |

---

## pLDDT Interpretation

Per-residue confidence score (0-100 scale, often normalized to 0-1):

| Range | Interpretation | Action |
|-------|----------------|--------|
| > 90 | Very high confidence | Excellent - proceed |
| 70-90 | Confident | Good - proceed |
| 50-70 | Low confidence | Potentially disordered - review |
| < 50 | Very low confidence | Likely disordered - redesign |

### pLDDT distribution analysis

```python
import numpy as np

def analyze_plddt(plddt_array):
    """Analyze pLDDT distribution for a design."""
    mean_plddt = np.mean(plddt_array)
    min_plddt = np.min(plddt_array)
    low_conf_fraction = np.mean(plddt_array < 70)

    print(f"Mean pLDDT: {mean_plddt:.2f}")
    print(f"Min pLDDT: {min_plddt:.2f}")
    print(f"Low confidence regions: {low_conf_fraction:.1%}")

    # Warnings
    if mean_plddt < 0.85:
        print("WARNING: Low average confidence")
    if min_plddt < 0.50:
        print("WARNING: Contains very low confidence regions")
    if low_conf_fraction > 0.20:
        print("WARNING: >20% low confidence residues")

    return {
        'mean': mean_plddt,
        'min': min_plddt,
        'low_conf_fraction': low_conf_fraction
    }
```

---

## pTM Interpretation

Global fold quality score (0-1):

| Range | Interpretation |
|-------|----------------|
| > 0.8 | Very high confidence in overall fold |
| 0.7-0.8 | Good confidence |
| 0.5-0.7 | Moderate confidence |
| < 0.5 | Low confidence - topology may be wrong |

**Note**: pTM is more meaningful than mean pLDDT for assessing global fold correctness.

---

## Self-consistency RMSD (scRMSD)

Measures whether the designed sequence specifies the intended structure:

1. Design backbone with RFdiffusion/BindCraft
2. Design sequence with ProteinMPNN
3. Predict structure with AF2/ESMFold
4. Calculate RMSD between designed and predicted backbone

| scRMSD | Interpretation | Action |
|--------|----------------|--------|
| < 1.0 A | Excellent agreement | Proceed |
| 1.0-1.5 A | Good agreement | Proceed |
| 1.5-2.0 A | Marginal | Review carefully |
| > 2.0 A | Poor agreement | Redesign sequence |

### Computing scRMSD

```python
from Bio.PDB import PDBParser, Superimposer
import numpy as np

def calculate_scrmsd(designed_pdb, predicted_pdb, chain='A'):
    """Calculate self-consistency RMSD between designed and predicted structures."""
    parser = PDBParser(QUIET=True)

    designed = parser.get_structure('designed', designed_pdb)
    predicted = parser.get_structure('predicted', predicted_pdb)

    # Extract CA atoms
    designed_cas = [atom for atom in designed[0][chain].get_atoms() if atom.name == 'CA']
    predicted_cas = [atom for atom in predicted[0][chain].get_atoms() if atom.name == 'CA']

    # Ensure same length
    min_len = min(len(designed_cas), len(predicted_cas))
    designed_cas = designed_cas[:min_len]
    predicted_cas = predicted_cas[:min_len]

    # Superimpose
    sup = Superimposer()
    sup.set_atoms(designed_cas, predicted_cas)

    rmsd = sup.rms
    print(f"scRMSD: {rmsd:.2f} A")

    if rmsd > 2.0:
        print("WARNING: High scRMSD - sequence may not specify intended structure")

    return rmsd
```

---

## Binder RMSD (Alone vs Complex)

For binder designs, check if the binder maintains its fold:

1. Predict binder alone (without target)
2. Predict binder in complex with target
3. Calculate RMSD between the two conformations

| Binder RMSD | Interpretation |
|-------------|----------------|
| < 1.5 A | Binder maintains fold - stable |
| 1.5-2.5 A | Some conformational change - acceptable |
| 2.5-4.0 A | Significant change - may be flexible |
| > 4.0 A | Large change - unstable or induced fit |

**Note**: High binder RMSD isn't always bad - some binders use induced fit. But it increases risk of expression issues.

---

## Design-level checks

### Secondary structure content

| Check | What it finds | Risk |
|-------|---------------|------|
| % Helix | Alpha-helix content | Low helix in helix-designed proteins |
| % Sheet | Beta-sheet content | Low sheet in sheet-designed proteins |
| % Coil | Loop/disordered content | High coil may indicate poor folding |

```python
from Bio.PDB.DSSP import DSSP
from Bio.PDB import PDBParser

def analyze_secondary_structure(pdb_file, chain='A'):
    """Analyze secondary structure content."""
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure('protein', pdb_file)
    model = structure[0]

    dssp = DSSP(model, pdb_file, dssp='mkdssp')

    ss_counts = {'H': 0, 'E': 0, 'C': 0}  # Helix, Sheet, Coil

    for key in dssp:
        ss = dssp[key][2]
        if ss in ['H', 'G', 'I']:  # Alpha, 3-10, Pi helix
            ss_counts['H'] += 1
        elif ss in ['E', 'B']:  # Extended, Bridge
            ss_counts['E'] += 1
        else:
            ss_counts['C'] += 1

    total = sum(ss_counts.values())

    print(f"Helix: {ss_counts['H']/total:.1%}")
    print(f"Sheet: {ss_counts['E']/total:.1%}")
    print(f"Coil:  {ss_counts['C']/total:.1%}")

    return {k: v/total for k, v in ss_counts.items()}
```

---

## Filtering strategy for structure

### Sequential filter order

1. **pLDDT > 0.85** - Filter poorly folded designs
2. **pTM > 0.70** - Filter incorrect topologies
3. **scRMSD < 2.0** - Filter sequence-structure mismatches
4. **Binder RMSD < 2.5** - Filter unstable binders (optional)

### Per-design-stage thresholds

| Stage | pLDDT | pTM | scRMSD | Notes |
|-------|-------|-----|--------|-------|
| After backbone | - | - | - | Visual check only |
| After sequence | - | - | - | ESM2 PLL > 0 |
| After AF2 (monomer) | > 0.85 | > 0.70 | < 2.0 | Binder alone |
| After AF2 (complex) | > 0.85 | > 0.70 | < 2.0 | With target |

---

## Common issues

### Low pLDDT

**Causes:**
- Intrinsically disordered regions
- Poor sequence for the backbone
- Unusual backbone conformation

**Solutions:**
- Redesign with ProteinMPNN (more sequences)
- Try SolubleMPNN for stability
- Simplify backbone topology
- Increase secondary structure content

### Low pTM

**Causes:**
- Incorrect global topology
- Multiple competing folds
- Very flexible structure

**Solutions:**
- Generate more backbones
- Use different checkpoint/model
- Try shorter/simpler designs

### High scRMSD

**Causes:**
- Sequence doesn't specify intended fold
- ProteinMPNN temperature too high
- Unusual backbone geometry

**Solutions:**
- Lower ProteinMPNN temperature (0.1)
- Increase num_seq_per_target
- Check backbone quality
- Try fixed-backbone sequence design
