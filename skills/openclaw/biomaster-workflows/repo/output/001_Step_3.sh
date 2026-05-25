#!/bin/bash
which python
conda config --set show_channel_urls false
conda config --add channels conda-forge
conda config --add channels bioconda
mkdir -p ./output/001
conda install -y samtools
mkdir -p ./output/001
samtools sort -o ./output/001/sorted_aligned_reads.bam ./output/001/aligned_reads.bam
