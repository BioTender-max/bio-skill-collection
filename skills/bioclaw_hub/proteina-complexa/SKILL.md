---
name: proteina-complexa
description: >
  Proteina-Complexa flow-based protein backbone generation with fold-conditioned sampling guidance.
  Use this skill when: (1) Generating de novo protein backbones with hierarchical fold conditioning,
  (2) Exploring long-chain backbone generation beyond standard diffusion baselines,
  (3) Using NVIDIA Proteina-style flow matching workflows for controllable backbone design,
  (4) Comparing flow-based backbone generation against RFdiffusion or BoltzGen,
  (5) Prototyping fold-guided backbone campaigns before sequence design.

  This skill is based on the public NVIDIA Digital Bio Proteina project and uses
  "Proteina-Complexa" as the BioClaw-facing skill label.
  For sequence design after backbone generation, use proteinmpnn or solublempnn.
  For QC thresholds, use protein-design-qc.
license: MIT
category: design-tools
tags: [structure-design, backbone-generation, flow-matching, fold-conditioning]
---

# Proteina-Complexa Backbone Generation

**Plain-language role**: Use this skill when you want a flow-based backbone generator with fold-class conditioning, especially for exploratory de novo design.

## Source Notes

- Public upstream reference: `NVIDIA-Digital-Bio/proteina`
- Publicly described as a large-scale flow-based protein backbone generator with hierarchical fold class conditioning
- Upstream setup and weights may change over time, so verify the current README and license before running
- Check the upstream NVIDIA license before commercial use or redistribution of model artifacts

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.10+ | 3.11 |
| CUDA | 12.0+ | 12.1+ |
| GPU VRAM | 24GB | 40GB+ |
| Environment manager | conda | mamba or micromamba |

## How to Run

### Option 1: Upstream Proteina environment
```bash
git clone https://github.com/NVIDIA-Digital-Bio/proteina.git
cd proteina
mamba env create -f environment.yaml
conda activate proteina_env
pip install -e .
```

Create a `.env` file in the repository root:
```bash
echo "DATA_PATH=/path/to/proteina-data" > .env
```

### Additional files

The upstream project documents extra data and weight bundles that must live under `DATA_PATH`.
At minimum, verify:

- metric feature files
- model weights
- CATH label mapping files
- dataset index files if you plan to train or evaluate

## Recommended Use Pattern

### 1. Start from backbone generation

Use Proteina-Complexa when the main task is generating diverse backbones, not sequence optimization.

### 2. Prefer fold-conditioned exploration

The upstream model is especially useful when you want:

- hierarchical fold control
- long-chain generation
- comparison against diffusion-based backbone generators

### 3. Hand off to sequence design

After generating promising backbones:

- use `proteinmpnn` for general inverse folding
- use `solublempnn` when expression robustness matters more

### 4. Validate and filter

After sequence design:

- use `chai1-structure-prediction`, `boltz-structure-prediction`, or `alphafold2-multimer`
- use `protein-design-qc` for filtering and ranking

## Typical Workflow

```text
Target goal
  -> Proteina-Complexa backbone generation
  -> ProteinMPNN / SolubleMPNN sequence design
  -> Chai / Boltz / AlphaFold validation
  -> Protein Design QC
```

## When to Prefer This Over Other Tools

| Need | Prefer |
|------|--------|
| Maximum backbone diversity with established community recipes | `rfdiffusion` |
| All-atom generation with side-chain awareness | `boltzgen` |
| Flow-based backbone generation with fold conditioning | `proteina-complexa` |
| End-to-end integrated binder pipeline | `bindcraft` |

## Key Ideas to Preserve

- Keep fold-conditioning choices explicit
- Record which checkpoint and config produced each backbone batch
- Separate backbone-generation artifacts from downstream sequence-design artifacts
- Treat generated backbones as candidates that still require validation and QC

## Common Mistakes

- Treating Proteina-Complexa as a sequence-design tool
- Skipping required upstream weight and data bundles
- Comparing outputs against RFdiffusion or BoltzGen without matching length and conditioning settings
- Moving generated backbones directly to experiments without refolding validation

## Troubleshooting

| Error | Likely cause | Fix |
|-------|--------------|-----|
| Missing `DATA_PATH` files | Required upstream bundles not downloaded | Re-check upstream setup and place files under the documented directory tree |
| CUDA OOM | Backbone length or batch too large | Reduce batch size or use a larger GPU |
| Config mismatch | Wrong checkpoint/config pair | Keep checkpoint, config, and conditioning mode aligned |
| Weak downstream foldability | Backbone exploration too unconstrained | Tighten fold conditioning and validate more aggressively |

## Inputs

- A backbone-generation objective such as fold-conditioned sampling, long-chain exploration, or de novo backbone discovery.
- A configured Proteina-style environment with checkpoints, configs, and required data bundles available under the configured data path.
- Optional fold-class or topology guidance for controlled generation.

## Outputs

- Generated protein backbone candidates suitable for downstream inverse folding.
- Run metadata describing checkpoint choice, conditioning mode, and generation settings.
- Backbone batches ready for sequence design with `proteinmpnn` or `solublempnn`.

## Next Step

Send promising backbones to `proteinmpnn` or `solublempnn`, then validate them structurally and filter with `protein-design-qc`.
