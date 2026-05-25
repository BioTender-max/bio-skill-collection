# Tool Documentation

Comprehensive usage guides for metagenomic binning and quality control tools.

Last updated: 2026-05-15

## Overview

This directory contains practical documentation for the tools used in the bio-binning-qc skill:
- **Binning tools**: Reconstruct genomes from metagenomic assemblies
- **QC tools**: Assess genome quality (completeness, contamination, chimerism)
- **Coverage tools**: Compute depth and abundance from read alignments

## Documentation Files

### Coverage Computation
- [coverm.md](coverm.md) - CoverM v0.7.0: Read alignment statistics and coverage computation

### Binning tools (in recommended order)
- [quickbin.md](quickbin.md) - **QuickBin (BBTools) v39.84 via `bryce911/bbtools`)**: high-fidelity neural-network binner; default for both short-read and long-read assemblies
- [semibin2.md](semibin2.md) - **SemiBin2 v2.2.1+**: deep-learning binner with pre-trained models; use as the GPU alternative to QuickBin on CUDA-equipped nodes
- [metabat2.md](metabat2.md) - MetaBAT2 v2.15+: legacy coverage-based binner; keep as fallback only for reproducing prior pipelines

### Quality-control tools

#### Domain-specific QC
- [checkm2.md](checkm2.md) - **CheckM2 v1.1.0+**: completeness/contamination for bacteria and archaea. v1.1.0 is a breaking upgrade — new DIAMOND v3 database from Zenodo (DOI 10.5281/zenodo.14897628) and new dependency tree; refresh the install and DB before use.
- [eukcc.md](eukcc.md) - EukCC v2.1.3+: quality assessment for eukaryotic MAGs

#### Contamination detection
- [gunc.md](gunc.md) - GUNC v1.0.6+: chimerism and contamination detection across all domains

## Quick Reference

### Installation Commands

```bash
# Install all tools via conda/mamba
mamba create -n binning-qc python=3.10
mamba install -c bioconda -c conda-forge \
  coverm metabat2 semibin checkm2 gunc

# QuickBin is provided by Bryce Foster's official BBTools container
docker pull bryce911/bbtools:39.84

# Download databases
checkm2 database --download
gunc download_db -db progenomes -o gunc_db/
wget http://ftp.ebi.ac.uk/pub/databases/metagenomics/eukcc/eukcc2_db_ver_1.2.tar.gz
tar -xzvf eukcc2_db_ver_1.2.tar.gz
export EUKCC2_DB=$(realpath eukcc2_db_ver_1.2)
```

### Typical Workflow

```bash
# 1. Compute coverage from BAM files
coverm contig --bam-files *.bam -m mean variance -o depth.txt

# 2. Bin (QuickBin by default; SemiBin2 only when a CUDA GPU is available)
mkdir -p quickbin
docker run --rm -u "$(id -u):$(id -g)" \
  -v "$PWD":/work -w /work \
  bryce911/bbtools:39.84 \
  quickbin.sh in=contigs.fasta out=quickbin/bin%.fa *.bam xstrict
# GPU alternative:
# SemiBin2 single_easy_bin -i contigs.fasta -b reads.bam --environment human_gut -o semibin/ -p 16
# Legacy only, to reproduce prior pipelines:
# metabat2 -i contigs.fasta -a depth.txt -o metabat/bin -t 16

# 3. Classify bins by domain (bacteria/archaea vs eukaryotes)
# Use appropriate classifier tool

# 4. Run domain-specific QC
checkm2 predict --input prokaryotic_bins/ --output-directory qc_prok/ -t 16
eukcc folder eukaryotic_bins/ --db $EUKCC2_DB --threads 16

# 5. Detect contamination/chimerism
gunc run --input_dir prokaryotic_bins/ --db_file gunc_db/gunc_db_progenomes2.1.dmnd -o gunc_qc/ -t 16

# 6. Filter high-quality bins
# Criteria: ≥90% complete, ≤5% contamination, pass GUNC
```

### Quality Thresholds (MIMAG Standards)

| Quality | Completeness | Contamination | Additional |
|---------|--------------|---------------|------------|
| High | ≥90% | ≤5% | rRNA genes, ≥18 tRNAs |
| Medium | ≥50% | ≤10% | - |
| Low | <50% | <10% | - |

### Tool selection guide

**Choose binning tool based on:**
- **QuickBin (default)**: high precision, low contamination; performs well on both short-read and long-read assemblies; CheckM2-agnostic.
- **SemiBin2 (GPU alternative)**: deep-learning binner with pre-trained models; preferred over QuickBin only when a CUDA GPU is available and SemiBin2's pre-trained environment models fit the dataset.
- **MetaBAT2 (legacy fallback)**: only when reproducing prior pipelines; otherwise prefer QuickBin.

**Choose QC tool based on domain:**
- **Bacteria/Archaea**: CheckM2 (completeness/contamination) + GUNC (chimerism)
- **Eukaryotes**: EukCC (completeness/contamination)

**Run multiple binners:** Ensemble approaches (e.g., DAS Tool, MetaWRAP) often improve results.

## Key Concepts

### Coverage/Depth
- **Mean coverage**: Average read depth across contig
- **Variance**: Variation in coverage (helps separate bins)
- **Multi-sample**: Differential abundance patterns improve binning

### Completeness
- Percentage of expected marker genes present
- Estimated via single-copy orthologous genes
- Higher = more complete genome

### Contamination
- Percentage of marker genes duplicated or from different lineages
- Indicates mixed genomes or chimeric assemblies
- Lower = purer bin

### Chimerism
- Contigs from unrelated organisms assembled into single bin
- Detected by lineage heterogeneity (GUNC)
- Complementary to marker-based contamination detection

## Common Workflows

### Single-Sample Binning
```bash
coverm contig --bam-files sample.bam -m mean variance -o depth.txt
mkdir -p bins
docker run --rm -u "$(id -u):$(id -g)" \
  -v "$PWD":/work -w /work \
  bryce911/bbtools:39.84 \
  quickbin.sh in=contigs.fasta out=bins/bin%.fa sample.bam strict
checkm2 predict --input bins/ --output-directory qc/ -t 16
```

### Multi-Sample Binning (Recommended)
```bash
coverm contig --bam-files sample*.bam -m mean variance -o depth.txt
mkdir -p bins
docker run --rm -u "$(id -u):$(id -g)" \
  -v "$PWD":/work -w /work \
  bryce911/bbtools:39.84 \
  quickbin.sh in=contigs.fasta out=bins/bin%.fa sample*.bam xstrict
checkm2 predict --input bins/ --output-directory qc/ -t 16
gunc run --input_dir bins/ --db_file gunc_db/gunc_db_progenomes2.1.dmnd -o gunc_qc/ -t 16
```

### Ensemble Binning with QC
```bash
# Run multiple binners
metabat2 -i contigs.fasta -a depth.txt -o metabat/bin -t 16
SemiBin2 single_easy_bin -i contigs.fasta -b reads.bam --environment soil -o semibin/ -p 16
mkdir -p quickbin
docker run --rm -u "$(id -u):$(id -g)" \
  -v "$PWD":/work -w /work \
  bryce911/bbtools:39.84 \
  quickbin.sh in=contigs.fasta out=quickbin/bin%.fa *.bam

# Combine with DAS Tool or similar
# Then QC
checkm2 predict --input final_bins/ --output-directory qc/ -t 16
gunc run --input_dir final_bins/ --db_file gunc_db/gunc_db_progenomes2.1.dmnd -o gunc_qc/ -t 16
```

## Troubleshooting

### Low Completeness
- Increase sequencing depth
- Try different binners or ensemble approach
- Decrease minimum contig length (if appropriate)
- Check if organism is from novel lineage

### High Contamination
- Use stricter binning parameters
- Try QuickBin with `xstrict` mode
- Manually refine bins using detailed QC output
- Check for chimeric contigs (GUNC detailed output)

### Few Bins
- Ensure adequate coverage variation (multi-sample)
- Check assembly quality
- Try relaxed binning parameters
- Consider community complexity

### No Bins
- Verify coverage file format
- Check contig length distribution
- Ensure BAM files are sorted and indexed
- Review alignment quality

## Performance Optimization

### Threading
- Most tools scale well: use 8-32 threads
- Balance between tools: limit concurrent jobs

### Memory
- CheckM2: 8-16 GB (use `--lowmem` if needed)
- GUNC: 8-16 GB (ProGenomes), 16-32 GB (GTDB)
- Binning tools: Generally modest (4-16 GB)

### Storage
- Place databases on fast SSD
- Use temporary directories on fast storage
- Clean intermediate files after successful runs

## References

### Official Documentation
- CoverM: https://github.com/wwood/CoverM
- MetaBAT2: https://bitbucket.org/berkeleylab/metabat
- SemiBin2: https://github.com/BigDataBiology/SemiBin
- QuickBin: https://bbmap.org/tools/quickbin
- CheckM2: https://github.com/chklovski/CheckM2
- EukCC: https://github.com/EBI-Metagenomics/EukCC
- GUNC: https://github.com/grp-bork/gunc

### Key Publications
- MetaBAT2: Kang et al. (2019) *PeerJ* https://doi.org/10.7717/peerj.7359
- SemiBin2: Pan et al. (2022) *Nat Commun* https://doi.org/10.1038/s41467-022-29843-y
- QuickBin: Bushnell (2026) *bioRxiv* https://doi.org/10.64898/2026.01.08.698506
- CheckM2: Chklovski et al. (2023) *Nat Methods* https://doi.org/10.1038/s41592-023-01940-w
- EukCC: Saary et al. (2020) *Genome Biol* https://doi.org/10.1186/s13059-020-02155-4
- GUNC: Orakov et al. (2021) *Genome Biol* https://doi.org/10.1186/s13059-021-02393-0

### Standards
- MIMAG: Bowers et al. (2017) *Nat Biotechnol* https://doi.org/10.1038/nbt.3893

## Contributing

To update documentation:
1. Verify tool versions and commands
2. Test examples on real datasets
3. Include practical tips from experience
4. Keep concise and actionable
5. Update this README with changes
