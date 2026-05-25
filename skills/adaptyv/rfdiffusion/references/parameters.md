# RFdiffusion Complete Parameter Reference

## Inference parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `inference.input_pdb` | path | required | Input PDB file |
| `inference.output_prefix` | string | "output" | Output file prefix |
| `inference.num_designs` | int | 10 | Number of designs to generate |
| `inference.symmetry` | string | None | Symmetry type (C2, C3, etc.) |
| `inference.ckpt_override_path` | path | None | Custom model checkpoint |

## Contigmap parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `contigmap.contigs` | list | required | Chain/length specification |
| `contigmap.inpaint_seq` | list | None | Positions to inpaint sequence |
| `contigmap.inpaint_str` | list | None | Positions to inpaint structure |
| `contigmap.provide_seq` | list | None | Positions with known sequence |

### Contigmap syntax examples

```bash
# De novo monomer, 80-120 residues
contigmap.contigs=[80-120]

# Binder design: fixed target (A1-150) + new binder (70-100 AA)
contigmap.contigs=[A1-150/0 70-100]

# Motif scaffolding: N-term + motif + C-term
contigmap.contigs=[20-40/0 A10-30/0 20-40]

# Multi-domain: two fixed domains with linker
contigmap.contigs=[A1-100/0 10-30 B1-100/0]
```

## Diffuser parameters

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `diffuser.T` | int | 50 | 20-200 | Diffusion timesteps |
| `diffuser.partial_T` | int | None | 1-T | Start from partial diffusion |

## Denoiser parameters

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `denoiser.noise_scale_ca` | float | 1.0 | 0.0-2.0 | CA position noise |
| `denoiser.noise_scale_frame` | float | 1.0 | 0.0-2.0 | Frame orientation noise |

### Noise scale guide

| noise_scale | Effect |
|-------------|--------|
| 1.0 | Full diversity (default) |
| 0.8 | Moderate conservation |
| 0.5 | Conservative, more regular SS |
| 0.3 | Very conservative |

## PPI (Protein-Protein Interface) parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ppi.hotspot_res` | list | None | Target residues to contact |

### Hotspot specification

```bash
# Single chain hotspots
ppi.hotspot_res=[A45,A67,A89]

# Multi-chain hotspots
ppi.hotspot_res=[A45,A67,B23,B45]
```

## Potentials parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `potentials.guide_scale` | float | 1.0 | Guidance strength |
| `potentials.guide_decay` | string | "constant" | Decay schedule |
| `potentials.olig_intra_all` | float | None | Intra-chain potential |
| `potentials.olig_inter_all` | float | None | Inter-chain potential |

## Model checkpoints

| Checkpoint | Size | Use Case |
|------------|------|----------|
| `Complex_base_ckpt.pt` | 500MB | Binder/complex design |
| `Base_ckpt.pt` | 500MB | De novo monomers |
| `ActiveSite_ckpt.pt` | 500MB | Active site scaffolding |
| `InpaintSeq_ckpt.pt` | 500MB | Sequence inpainting |

## Performance tuning

### Memory optimization

```bash
# Reduce memory usage
inference.num_designs=10  # Process in batches
diffuser.T=35             # Fewer timesteps
```

### Speed optimization

```bash
# Faster generation
diffuser.T=25             # Minimum reasonable
denoiser.noise_scale_ca=0.8  # Converges faster
```

## Common parameter combinations

### High-quality binders
```bash
inference.num_designs=500
diffuser.T=50
denoiser.noise_scale_ca=1.0
ppi.hotspot_res=[A45,A67,A89]
```

### Fast exploration
```bash
inference.num_designs=100
diffuser.T=25
denoiser.noise_scale_ca=0.8
```

### Conservative scaffolding
```bash
inference.num_designs=200
diffuser.T=50
denoiser.noise_scale_ca=0.5
denoiser.noise_scale_frame=0.5
```
