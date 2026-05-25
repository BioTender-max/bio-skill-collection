# BindCraft Design Protocols

## Protocol overview

BindCraft provides predefined filter configurations for different use cases.

## Available protocols

### Default protocol (recommended)
Most stringent filtering, highest experimental success rate.

```python
filters = {
    "plddt": 0.8,
    "ptm": 0.45,
    "i_ptm": 0.5,
    "pae": 0.4,
    "i_pae": 0.4,
    "shape_complementarity": 0.5,
    "interface_dSASA": 1,
    "interface_hbonds": 2,
    "interface_nres": 6,
    "unsatisfied_hbonds": 6,
    "surface_hydrophobicity": 0.37
}
```

### Relaxed protocol
More permissive thresholds for challenging targets.

```python
filters = {
    "plddt": 0.7,
    "ptm": 0.4,
    "i_ptm": 0.4,
    "pae": 0.5,
    "i_pae": 0.5,
    "shape_complementarity": 0.4,
    "interface_dSASA": 0.5,
    "interface_hbonds": 1,
    "interface_nres": 4,
    "unsatisfied_hbonds": 8,
    "surface_hydrophobicity": 0.45
}
```

### Peptide protocol
Optimized for peptide binders (< 30 residues).

```python
filters = {
    "plddt": 0.75,
    "ptm": 0.4,
    "i_ptm": 0.45,
    "interface_nres": 3,
    "interface_hbonds": 1
}
```

### Peptide relaxed protocol
More permissive peptide-specific filters.

## Protocol selection guide

| Target Type | Recommended Protocol |
|-------------|---------------------|
| Standard binder | Default |
| Difficult target | Relaxed |
| Short peptide (8-20 AA) | Peptide |
| Long peptide (20-30 AA) | Peptide Relaxed |
| Benchmarking | None (no filtering) |

## Custom protocol configuration

```python
from bindcraft import BindCraft

bc = BindCraft(
    target_pdb="target.pdb",
    filters={
        "plddt": 0.85,       # Stricter confidence
        "i_ptm": 0.55,       # Higher interface quality
        "surface_hydrophobicity": 0.35  # Lower aggregation risk
    }
)
```

## Metric thresholds reference

| Metric | Default | Relaxed | Unit |
|--------|---------|---------|------|
| pLDDT | 0.8 | 0.7 | 0-1 |
| pTM | 0.45 | 0.4 | 0-1 |
| ipTM | 0.5 | 0.4 | 0-1 |
| PAE | 0.4 | 0.5 | normalized |
| iPAE | 0.4 | 0.5 | normalized |
| Shape Comp | 0.5 | 0.4 | 0-1 |
| dSASA | 1 | 0.5 | normalized |
| H-bonds | 2 | 1 | count |
| Interface res | 6 | 4 | count |

## Important notes

1. **Do not relax filters** unless absolutely necessary
2. Default filters have highest experimental success rate
3. Relaxed filters increase false positives
4. Generate at least 100 designs for statistical reliability
