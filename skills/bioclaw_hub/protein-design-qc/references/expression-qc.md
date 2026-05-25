# Expression QC

**Purpose**: Assess manufacturability, solubility, and expression likelihood

Expression QC catches sequence liabilities that can cause:
- Poor expression in E. coli/mammalian cells
- Aggregation and insolubility
- Chemical instability during production/storage
- Proteolytic degradation

---

## Metric-level QC (calculated values)

### Biophysical properties

| Metric | Threshold | Risk if Failed | Source |
|--------|-----------|----------------|--------|
| Instability Index (DIWV) | < 40 | Unstable protein | BioPython |
| GRAVY | < 0.4 | Aggregation-prone | BioPython |
| Isoelectric Point (pI) | != 6.5-7.5 | Low solubility at neutral pH | BioPython |
| ESM2 PLL (normalized) | > 0.0 | Implausible sequence | ESM2 |
| Surface hydrophobicity | < 0.37 | Aggregation risk | PyRosetta |

### Computing biophysical properties

```python
from Bio.SeqUtils.ProtParam import ProteinAnalysis

seq = "MKTAYIAKQRQISFVK..."
analysis = ProteinAnalysis(seq)

# Stability
instability = analysis.instability_index()
print(f"Instability Index: {instability:.1f}")
if instability > 40:
    print("  WARNING: Protein may be unstable")

# Hydrophobicity
gravy = analysis.gravy()
print(f"GRAVY: {gravy:.2f}")
if gravy > 0.4:
    print("  WARNING: High aggregation risk")

# Solubility risk
pi = analysis.isoelectric_point()
print(f"pI: {pi:.1f}")
if 6.5 <= pi <= 7.5:
    print("  WARNING: pI near neutral - low solubility")

# Molecular weight
mw = analysis.molecular_weight()
print(f"MW: {mw:.0f} Da")
```

---

## Design-level QC (pattern detection)

### Expression system liabilities

| Check | Pattern | Severity | Risk |
|-------|---------|----------|------|
| **Cysteine count** | Odd number | High (20) | Unpaired disulfides, aggregation |
| **Polybasic clusters** | K/R >= 3 consecutive | Medium (8) | Proteolysis, nucleic acid binding |
| **Polyacidic clusters** | D/E >= 4 consecutive | Low (5) | Expression issues |
| **N-terminal Q** | Starts with Q | Medium (5) | Pyroglutamate formation |
| **N-terminal E** | Starts with E | Low (3) | Slower pyroglutamate |
| **N-terminal N** | Starts with N | Medium (5) | Deamidation hotspot |
| **C-terminal K/R** | Ends with K or R | Low (3) | Trypsin-like clipping |
| **Met retention** | N-term not followed by small AA | Low (2) | Met may not be cleaved |

### Structural liabilities

| Check | Pattern | Severity | Risk |
|-------|---------|----------|------|
| **Homopolymer runs** | >= 4 identical AA | Low (3) | Low complexity, disordered |
| **High A/G/S content** | > 50% | Low (5) | Disordered regions |
| **Hydrophobic runs** | >= 6 consecutive hydrophobic | High (8) | Aggregation |
| **TM-like segments** | > 70% hydrophobic in 19-AA window | Very High (25) | Insolubility |
| **Aromatic clusters** | >= 3 consecutive F/W/Y | Medium (5) | Pi-stacking aggregation |

### Chemical stability

| Check | Pattern | Severity | Risk |
|-------|---------|----------|------|
| **Deamidation** | NG, NS, NT, NN, NH, NA, NQ | High (6-8) | Asparagine hydrolysis |
| **Isomerization** | DG, DS, DT, DD, DH, DN | Medium (5-6) | Aspartate rearrangement |
| **Fragmentation** | DP, TS, NP | Medium (5) | Cleavage sites |
| **Oxidation** | M >= 3 or W >= 2 | Medium (5) | Oxidative damage |
| **N-glycosylation** | N-X-S/T (X != P) | Low (3) | Glycan attachment (if mammalian) |

---

## Pattern detection code

### Cysteine analysis

```python
def check_cysteines(seq):
    """Check for unpaired disulfide risk."""
    cys_count = seq.count('C')
    if cys_count % 2 != 0:
        return {
            'severity': 20,
            'risk': 'high',
            'message': f'Odd cysteine count ({cys_count}) - unpaired disulfide risk',
            'suggestion': 'Add or remove cysteine to make count even'
        }
    return None
```

### Polybasic cluster detection

```python
import re

def find_polybasic_clusters(seq):
    """Find K/R runs that may cause proteolysis."""
    liabilities = []

    # Consecutive K/R
    for match in re.finditer(r'[KR]{3,}', seq):
        liabilities.append({
            'position': match.start(),
            'pattern': match.group(),
            'severity': 8 + len(match.group()),
            'risk': 'medium',
            'message': f'Polybasic cluster at {match.start()}: {match.group()}'
        })

    return liabilities
```

### Deamidation site detection

```python
def find_deamidation_sites(seq):
    """Find asparagine deamidation hotspots."""
    motifs = {
        'NG': 8, 'NS': 7, 'NT': 6, 'NN': 6,
        'NH': 5, 'NA': 4, 'NQ': 4
    }

    liabilities = []
    for motif, severity in motifs.items():
        start = 0
        while True:
            pos = seq.find(motif, start)
            if pos == -1:
                break
            liabilities.append({
                'position': pos,
                'pattern': motif,
                'severity': severity,
                'risk': 'high' if severity >= 7 else 'medium',
                'message': f'Deamidation site {motif} at position {pos}',
                'suggestion': f'Consider N->{{"Q","D"}} or G->{{"A","S"}} substitution'
            })
            start = pos + 1

    return liabilities
```

### Hydrophobic run detection

```python
HYDROPHOBIC = set('VILMFYW')

def find_hydrophobic_runs(seq, min_length=6):
    """Find aggregation-prone hydrophobic stretches."""
    liabilities = []
    run_start = None
    run_length = 0

    for i, aa in enumerate(seq):
        if aa in HYDROPHOBIC:
            if run_start is None:
                run_start = i
            run_length += 1
        else:
            if run_length >= min_length:
                liabilities.append({
                    'position': run_start,
                    'end_position': i - 1,
                    'severity': 8 + run_length,
                    'risk': 'high',
                    'message': f'Hydrophobic run ({run_length} AA) at {run_start}-{i-1}'
                })
            run_start = None
            run_length = 0

    return liabilities
```

---

## Severity scoring system

Total severity score determines action:

| Level | Score | Action |
|-------|-------|--------|
| LOW | 0-15 | Proceed with design |
| MODERATE | 16-35 | Review flagged issues |
| HIGH | 36-60 | Redesign recommended |
| CRITICAL | 61+ | Redesign required |

```python
def calculate_severity(liabilities):
    """Calculate total severity from all liabilities."""
    total = sum(l.get('severity', 0) for l in liabilities)
    total = min(total, 100)  # Cap at 100

    if total <= 15:
        level = 'LOW'
    elif total <= 35:
        level = 'MODERATE'
    elif total <= 60:
        level = 'HIGH'
    else:
        level = 'CRITICAL'

    return {'total': total, 'level': level}
```

---

## Remediation strategies

### High instability index

- Use SolubleMPNN instead of ProteinMPNN
- Add stabilizing mutations (proline in turns, charged residues on surface)
- Consider different backbone topology

### High GRAVY (aggregation risk)

- Redesign surface-exposed residues to be more polar
- Add charged residues (K, R, E, D) on surface
- Avoid large hydrophobic patches

### Deamidation sites (NG, NS)

- Substitute N with Q or D
- Substitute G with A or S
- Accept if site is buried (slower deamidation)

### Polybasic clusters

- Break up K/R runs with small residues (G, A, S)
- Check if cluster is functional (may be intentional)

### Odd cysteines

- Add/remove cysteine to make count even
- Ensure proper disulfide pairing
- Consider C->S mutation if cysteine not critical
