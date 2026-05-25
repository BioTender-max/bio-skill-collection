#!/bin/bash
which python
conda config --set show_channel_urls false
conda config --add channels conda-forge
conda config --add channels bioconda
mkdir -p ./output/001
conda install -y samtools
samtools view -S -b ./output/001/aligned_reads.sam > ./output/001/aligned_reads.bam
