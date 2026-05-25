#!/bin/bash
which python
conda config --set show_channel_urls false
conda config --add channels conda-forge
conda config --add channels bioconda
conda install -y bwa
bwa index ./data/mm39.fa
bwa mem ./data/mm39.fa ./output/003/trimmed_SRR620205.fastq.gz > ./output/003/aligned_SRR620205.sam
bwa mem ./data/mm39.fa ./output/003/trimmed_SRR620208.fastq.gz > ./output/003/aligned_SRR620208.sam
