#!/bin/bash
which python
conda config --set show_channel_urls false
conda config --add channels conda-forge
conda config --add channels bioconda
mkdir -p ./output/001
conda install -y samtools
samtools faidx ./data/minigenome.fa
gatk CreateSequenceDictionary -R ./data/minigenome.fa
conda install -y gatk
gatk Mutect2 -R ./data/minigenome.fa -I ./output/001/dedup_sorted_aligned_reads.bam -O ./output/001/somatic_variants.vcf
