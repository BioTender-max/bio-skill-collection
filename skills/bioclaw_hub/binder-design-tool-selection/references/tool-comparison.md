# Binder Design Tool Comparison

## Overview

| Tool | Method | Output | Requires Seq Design |
|------|--------|--------|---------------------|
| RFdiffusion | Diffusion | Backbone | Yes (ProteinMPNN) |
| BindCraft | Hallucination | Full design | No |
| BoltzGen | Diffusion | All-atom | No |
| ColabDesign | AF2 optimization | Full design | No |

## Detailed comparison

### RFdiffusion

**Strengths:**
- Fastest backbone generation
- High structural diversity
- Well-validated hotspot specification
- Flexible length ranges

**Weaknesses:**
- Requires separate sequence design
- No side-chain information
- May need multiple iterations

**Best for:**
- Initial exploration
- High-throughput campaigns
- Novel scaffold discovery

**Typical workflow:**
```
RFdiffusion (500 backbones)
    --> ProteinMPNN (8 seq/backbone = 4000 sequences)
    --> AF2 validation
    --> Filter
```

### BindCraft

**Strengths:**
- End-to-end design (backbone + sequence)
- High experimental success rate
- Built-in AF2 validation loop
- Multiple protocols available

**Weaknesses:**
- Slower than RFdiffusion
- Less structural diversity
- More compute-intensive

**Best for:**
- Production campaigns
- High-confidence hits needed
- When AF2 validation is critical

**Typical workflow:**
```
BindCraft (100 designs)
    --> AF2 validation (built-in)
    --> Filter
    --> Optional: refinement
```

### BoltzGen

**Strengths:**
- All-atom diffusion
- Side-chain aware from start
- Based on Boltz-1 architecture
- Joint structure-sequence

**Weaknesses:**
- Newer, less validated
- Computationally expensive
- Requires YAML configuration

**Best for:**
- Precision design
- When side-chain geometry matters
- Small molecule binding sites

**Typical workflow:**
```
BoltzGen (50-100 designs)
    --> AF2/Boltz validation
    --> Filter
```

### ColabDesign (AFDesign)

**Strengths:**
- Direct AF2 gradient optimization
- Can refine existing designs
- Multiple protocols (fixbb, hallucination, binder)
- Interpretable loss functions

**Weaknesses:**
- Computationally expensive
- Can get stuck in local minima
- Requires careful hyperparameter tuning

**Best for:**
- Refinement of existing designs
- When AF2 metrics are priority
- Hallucinating from scratch with AF2

**Typical workflow:**
```
AFDesign binder protocol
    --> Multiple design stages
    --> Built-in metrics
    --> Optional: ProteinMPNN diversification
```

## Decision matrix

| Criterion | RFdiffusion | BindCraft | BoltzGen | ColabDesign |
|-----------|-------------|-----------|----------|-------------|
| Speed | Fast | Medium | Slow | Slow |
| Diversity | High | Medium | Medium | Low |
| Success rate | Medium | High | Medium | Medium |
| Compute cost | Low | High | High | High |
| Ease of use | Medium | Easy | Medium | Medium |
| All-atom | No | Yes | Yes | Yes |

## Resource requirements

| Tool | GPU | VRAM | Time (100 designs) |
|------|-----|------|-------------------|
| RFdiffusion | A10G | 24GB | 30 min |
| BindCraft | L40S | 48GB | 4-8 hours |
| BoltzGen | A100 | 40GB | 2-4 hours |
| ColabDesign | A100 | 40GB | 4-8 hours |

## Combining tools

### RFdiffusion + ProteinMPNN + AF2
Standard pipeline, good balance of diversity and validation.

### RFdiffusion + ColabDesign
Use RFdiffusion for backbone, then refine with AFDesign.

### BindCraft + ProteinMPNN
Diversify BindCraft backbones with additional ProteinMPNN sequences.

### BoltzGen + AF2
Validate BoltzGen designs with AF2-Multimer for cross-validation.

## Publication references

- RFdiffusion: Watson et al., Nature 2023
- BindCraft: Pacesa et al., bioRxiv 2024
- BoltzGen: Stark et al., bioRxiv 2025
- ColabDesign: https://github.com/sokrypton/ColabDesign
