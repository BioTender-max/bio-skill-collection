# Hotspot Selection Guide for RFdiffusion

## What are hotspots?

Hotspots are target residues that the designed binder should contact. Good hotspot selection significantly improves binder success rates.

## Selection criteria

### 1. Surface accessibility
- Choose residues with >30% solvent accessible surface area (SASA)
- Avoid buried residues that cannot be contacted
- Use PyMOL: `get_area selection, dot_solvent=1`

### 2. Conservation (if applicable)
- Conserved residues often indicate functional importance
- Use ConSurf or similar for conservation analysis
- Targeting conserved epitopes reduces escape mutations

### 3. Secondary structure context
- Loop regions: More flexible, easier to contact
- Helix/sheet edges: Good anchor points
- Avoid middle of helices (steric constraints)

### 4. Chemical properties
- Charged residues (K, R, E, D): Strong interactions
- Aromatic residues (W, Y, F): Pi-stacking potential
- Polar residues (N, Q, S, T): Hydrogen bonding

## Number of hotspots

| Count | Effect |
|-------|--------|
| 1-2 | Very loose constraint, high diversity |
| 3-5 | Recommended balance |
| 6-8 | Tight constraint, focused interface |
| >8 | May over-constrain design |

## Hotspot spacing

- Minimum 3-4 residues apart in sequence
- Spatial clustering: hotspots within 10-15A of each other
- Avoid hotspots on opposite sides of target

## Example selection process

### Step 1: Identify surface residues
```python
# PyMOL
select surface_res, byres (all within 5 of solvent)
```

### Step 2: Check conservation
```bash
# Use ConSurf webserver or local analysis
# Select residues with conservation score >= 7
```

### Step 3: Filter by chemistry
```python
# Prefer charged/aromatic
select good_hotspots, surface_res and resn ARG+LYS+GLU+ASP+TRP+TYR+PHE
```

### Step 4: Validate spatial arrangement
- Hotspots should form a contiguous patch
- 200-400 A^2 total hotspot area is typical

## Common patterns

### Receptor binding sites
- Active site residues
- Ligand-coordinating residues
- Known functional epitopes

### Enzyme targets
- Catalytic residues
- Substrate binding pocket edges
- Allosteric sites

### Cytokine/Growth Factors
- Receptor-interacting surface
- Dimerization interface residues

## Troubleshooting

### Binder not contacting hotspots
1. Verify residue numbering matches PDB
2. Check PDB chain labels
3. Increase num_designs to 500+
4. Reduce number of hotspots

### Poor interface quality
1. Add more hotspots (up to 6)
2. Choose better-exposed residues
3. Check for clashes in target structure

## Hotspot format

```bash
# Format: [ChainResnum,ChainResnum,...]
ppi.hotspot_res=[A45,A67,A89]

# Multi-chain
ppi.hotspot_res=[A45,A67,B23]

# No spaces allowed
# Correct: [A45,A67,A89]
# Wrong:   [A45, A67, A89]
```
