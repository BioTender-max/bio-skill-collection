# BoltzGen YAML Design Specification

BoltzGen uses an entity-based YAML format to specify what to design and what the target is.

**Important notes:**
- Residue indices use `label_seq_id` (1-indexed), not `auth_seq_id`
- File paths are relative to the YAML file location
- Run `boltzgen check config.yaml` to verify before running
- View in Molstar to confirm binding site is correctly specified

## Entity Types

### Designed Protein
```yaml
entities:
  - protein:
      id: B                    # Chain ID for designed protein
      sequence: 80..140        # Variable length (80-140 residues)
```

**Sequence specification:**
- `80..140` - random length between 80 and 140 residues
- `80` - exactly 80 designed residues
- `AAAVVV20PPP` - specific residues with 20 designed in middle
- `3..5C6C3` - designed residues with specific cysteines

### Target from File
```yaml
entities:
  - file:
      path: target.cif        # CIF or PDB file (relative to YAML)
      include:                 # Which chains/residues to include
        - chain:
            id: A
            res_index: 2..50,55..  # Optional: specific residues
      binding_types:           # Where design should bind
        - chain:
            id: A
            binding: 45,67,89  # Binding site residues
      structure_groups: "all"  # Optional: structure specification
```

### Non-Designed Protein
```yaml
entities:
  - protein:
      id: X
      sequence: AAVTTTTPPP    # Fixed sequence (not designed)
```

### Constraints (Bonds)
```yaml
constraints:
  - bond:
      atom1: [S, 11, SG]      # [chain_id, res_index, atom_name]
      atom2: [S, 18, SG]      # Disulfide bond
```

## Protocol-Specific Examples

### Protein Binder Design (`protein-anything`)
```yaml
entities:
  # Designed binder (80-140 residues)
  - protein:
      id: B
      sequence: 80..140

  # Target protein
  - file:
      path: target.cif
      include:
        - chain:
            id: A
      binding_types:
        - chain:
            id: A
            binding: 45,67,89
```

### Peptide Design (`peptide-anything`)
```yaml
entities:
  # Designed peptide (12-20 residues)
  - protein:
      id: G
      sequence: 12..20

  - file:
      path: target.cif
      include:
        - chain:
            id: A
      binding_types:
        - chain:
            id: A
            binding: 343,344,251
      structure_groups: "all"
```

### Cyclic Peptide with Disulfide
```yaml
entities:
  - protein:
      id: S
      sequence: 10..14C6C3    # Designed with cysteines

  - file:
      path: target.cif
      include:
        - chain:
            id: A

constraints:
  - bond:
      atom1: [S, 11, SG]
      atom2: [S, 18, SG]
```

### WHL Stapled Peptide
```yaml
entities:
  - protein:
      id: R
      sequence: 3..5C6C3

  - ligand:
      id: Q
      ccd: WHL

  - file:
      path: target.cif
      include:
        - chain:
            id: A

constraints:
  - bond:
      atom1: [R, 4, SG]
      atom2: [Q, 1, CK]
  - bond:
      atom1: [R, 11, SG]
      atom2: [Q, 1, CH]
```

### Small Molecule Binding (`protein-small_molecule`)
```yaml
entities:
  - protein:
      id: A
      sequence: 100..150

  - ligand:
      smiles: "CCO"           # Ethanol
      # or ccd: ATP           # From CCD database
```

### Nanobody Design (`nanobody-anything`)
```yaml
entities:
  - protein:
      id: H
      sequence: EVQLVESGG...  # Framework with designed CDRs
      # Use specific residue notation for CDR design

  - file:
      path: antigen.cif
      include:
        - chain:
            id: A
```

## Advanced Options

### Partial Target Flexibility
```yaml
entities:
  - file:
      path: target.cif
      include:
        - chain:
            id: A
      structure_groups:
        - group:
            visibility: 1     # Fixed structure
            id: A
            res_index: 10..50
        - group:
            visibility: 0     # Flexible (not structurally specified)
            id: A
            res_index: 51..60
```

### Redesign Existing Residues
```yaml
entities:
  - file:
      path: complex.cif
      include:
        - chain:
            id: A
      design:                  # Residues to redesign
        - chain:
            id: A
            res_index: 14..19
```

### Secondary Structure Constraints
```yaml
entities:
  - file:
      path: target.cif
      design:
        - chain:
            id: A
            res_index: 14..19
      secondary_structure:
        - chain:
            id: A
            helix: 15..17
            sheet: 19
            loop: 14
```

### Not-Binding Regions
```yaml
entities:
  - file:
      path: target.cif
      include:
        - chain:
            id: A
        - chain:
            id: B
      binding_types:
        - chain:
            id: A
            binding: 45,67,89
        - chain:
            id: B
            not_binding: "all"  # Design should NOT bind here
```

## Running with Modal

```bash
# Basic run
modal run modal_boltzgen.py \
  --input-yaml binder.yaml \
  --protocol protein-anything \
  --num-designs 50

# With custom GPU
GPU=L40S modal run modal_boltzgen.py \
  --input-yaml binder.yaml \
  --protocol protein-anything \
  --num-designs 100

# Run specific pipeline steps only
modal run modal_boltzgen.py \
  --input-yaml binder.yaml \
  --protocol protein-anything \
  --num-designs 50 \
  --steps "design inverse_folding"
```

## CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `--input-yaml` | required | Path to YAML design specification |
| `--protocol` | `protein-anything` | Design protocol |
| `--num-designs` | 10 | Number of designs |
| `--steps` | all | Pipeline steps (design, inverse_folding, folding, analysis, filtering) |
| `--out-dir` | `./out/boltzgen` | Output directory |
| `--run-name` | timestamp | Run name for output subdirectory |

## Verifying Your Config

Always verify your config before running a large campaign:

```bash
boltzgen check config.yaml
```

Then visualize the output CIF in Molstar (https://molstar.org/viewer/) to confirm:
- Binding site residues are highlighted correctly
- Target structure loads properly
- Chain IDs match your specification
