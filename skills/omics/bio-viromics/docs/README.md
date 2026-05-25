# Tool Documentation

Last updated: 2026-02-01

## Overview

This directory contains practical usage guides for the core tools in the bio-viromics skill. Each guide includes installation instructions, command-line options, usage examples, and integration tips for the viromics workflow.

## Available Tools

### [geNomad](genomad-usage.md)
Version: 1.11.2

Identifies virus and plasmid genomes from nucleotide sequences with state-of-the-art classification performance. Provides taxonomic assignment using ICTV taxonomy and functional annotation.

- **Official docs**: https://portal.nersc.gov/genomad/
- **GitHub**: https://github.com/apcamargo/genomad
- **Use case**: Initial viral detection from assemblies

### [CheckV](checkv-usage.md)
Version: 1.0.3

Automated quality assessment tool for viral genomes. Identifies closed genomes, estimates completeness, and removes host contamination from proviruses.

- **Official docs**: https://bitbucket.org/berkeleylab/checkv
- **PyPI**: https://pypi.org/project/checkv/
- **Use case**: Quality control and completeness estimation

### [vConTACT3](vcontact3-usage.md)
Version: 3.0.1

Viral genome clustering and taxonomic assignment using gene-sharing networks. Improved speed and scalability over previous versions.

- **Official docs**: https://vcontact3.readthedocs.io/
- **Bitbucket**: https://bitbucket.org/MAVERICLab/vcontact3
- **Use case**: Hierarchical classification and genome clustering

### [GVClass](gvclass-usage.md)
Version: 1.2.0 (internal build tag)

Specialized tool for giant virus (Nucleocytoviricota) identification and taxonomy. Uses phylogenetic analysis with >90% genus-level accuracy.

- **Official docs**: https://github.com/NeLLi-team/gvclass
- **Publication**: npj Viruses (2024), DOI: 10.1038/s44298-024-00069-7
- **Use case**: Focused NCLDV detection and classification

## Typical Workflow Integration

0. **Domain Triage** (QuickClade via `/tracking-taxonomy-updates`)
   - Input: Assembled contigs, genomes, MAGs, or bin directories
   - Output: Per-contig domain routing table; viral/virus-like rows proceed here

1. **Viral Detection** (geNomad)
   - Input: Assembled contigs
   - Output: Candidate viral sequences

2. **Quality Control** (CheckV)
   - Input: Viral sequences from geNomad
   - Output: Quality-filtered genomes with completeness estimates

3. **Clustering & Taxonomy** (vConTACT3)
   - Input: High/medium quality genomes from CheckV
   - Output: Genome clusters and taxonomic assignments

4. **Giant Virus Analysis** (GVClass - optional)
   - Input: Contigs or assembled genomes
   - Output: NCLDV-specific taxonomy and quality metrics

## Quick Reference

| Tool | Primary Function | Key Output | Typical Runtime |
|------|------------------|------------|-----------------|
| geNomad | Viral detection | viral_contigs.fasta | Minutes-hours |
| CheckV | Quality assessment | quality_summary.tsv | Minutes |
| vConTACT3 | Clustering/taxonomy | genome_clusters.tsv | Hours |
| GVClass | NCLDV classification | gvclass_summary.tsv | Minutes-hours |

## Installation Overview

All tools can be installed via conda/mamba:

```bash
# geNomad
pixi global install -c conda-forge -c bioconda genomad

# CheckV
conda install -c conda-forge -c bioconda checkv

# vConTACT3
mamba create -n vcontact3 python=3.10
mamba activate vcontact3
mamba install -c bioconda vcontact3

# GVClass
wget https://raw.githubusercontent.com/NeLLi-team/gvclass/main/gvclass-a
chmod +x gvclass-a
```

## Additional Resources

- Paper summaries with use cases: `../summaries/`
- Skill specification: `../SKILL.md`
