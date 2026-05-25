# Tool Documentation

Last updated: 2026-02-01

## Overview

This directory contains practical usage guides for gene calling tools used in the bio-gene-calling skill.

## Tools

### Prokaryotic and viral gene calling

- **[pyrodigal.md](pyrodigal.md)** - Python bindings around Prodigal (v3.7.0+) for bacteria and archaea
  - Fast prokaryotic gene prediction
  - Metagenomic and single-genome modes
  - Thread-safe parallel processing
  - Source: https://github.com/althonos/pyrodigal

- **[pyrodigal-gv.md](pyrodigal-gv.md)** - SIMD-accelerated Python bindings around prodigal-gv for viruses, including giant viruses
  - Replaces the standalone `prodigal-gv` C binary
  - Same model set, much faster, actively maintained
  - Source: https://github.com/althonos/pyrodigal-gv

### Eukaryotic gene calling

- **[braker.md](braker.md)** - BRAKER3 (*Genome Research* 2024) — fully automated eukaryotic annotation pipeline
  - Combines GeneMark-ETP and AUGUSTUS internally (AUGUSTUS is not run as a standalone tool)
  - RNA-seq and protein evidence integration
  - Automated training
  - Source: https://github.com/Gaius-Augustus/BRAKER

### RNA gene detection

- **[trnascan-se.md](trnascan-se.md)** - tRNA detection (v2.0.12+)
  - Covariance model-based; isotype-specific models
  - Bacterial, archaeal, eukaryotic modes
  - Uses Infernal v1.1.5
  - Source: https://github.com/UCSC-LoweLab/tRNAscan-SE

- **[infernal.md](infernal.md)** - rRNA and other ncRNA detection via `cmsearch` against Rfam covariance models
  - Replaces barrnap as the default rRNA caller in this workflow
  - Domain-appropriate Rfam models (SSU, LSU, 5S, 5.8S; mitochondrial 12S/16S where applicable) — see SKILL.md for the model list
  - Source: http://eddylab.org/infernal/

## Quick reference

| Tool | Organism type | Mode | Typical use case |
|------|---------------|------|------------------|
| pyrodigal | Bacteria, archaea | Meta / single | Fast prokaryotic gene calling |
| pyrodigal-gv | Viruses (including giants) | Meta | Viral genomes |
| BRAKER3 | Eukaryotes | Evidence-based | High-quality eukaryotic annotation |
| tRNAscan-SE | All domains | Domain-specific | tRNA detection |
| Infernal `cmsearch` | All domains | Rfam covariance models | rRNA (SSU/LSU/5S/5.8S) and other ncRNA |

> **Retired from this workflow:** AUGUSTUS as a standalone tool (now invoked only through BRAKER3); standalone `prodigal-gv` (use pyrodigal-gv); `barrnap` (replaced by Infernal `cmsearch` against domain-specific Rfam models).

## Documentation Format

Each tool guide includes:
- Official documentation URLs
- Installation commands
- Key command-line flags
- Common usage examples for gene calling
- Input/output format specifications
- Performance optimization tips

## Usage Notes

- All tools are installed via pixi (see pixi.toml in skill root)
- Examples assume tools are in PATH
- Adjust thread counts based on available resources
- Check tool-specific QC recommendations
