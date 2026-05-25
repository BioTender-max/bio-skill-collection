#!/bin/bash
which python
conda config --set show_channel_urls false
conda config --add channels conda-forge
conda config --add channels bioconda
mkdir -p ./output/001
conda install -y bwa
bwa index ./data/minigenome.fa
bwa mem ./data/minigenome.fa ./data/rnaseq_1.fastq.gz ./data/rnaseq_2.fastq.gz > ./output/001/aligned_reads.sam
