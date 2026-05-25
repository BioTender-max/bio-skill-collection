#!/bin/bash
which python
conda config --set show_channel_urls false
conda config --add channels conda-forge
conda config --add channels bioconda
conda install -y fastqc trimmomatic
mkdir -p ./output/003
fastqc ./data/SRR620205.fastq.gz
fastqc ./data/SRR620208.fastq.gz
trimmomatic SE -phred33 ./data/SRR620205.fastq.gz ./output/003/trimmed_SRR620205.fastq.gz ILLUMINACLIP:./data/TruSeq3-SE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36
trimmomatic SE -phred33 ./data/SRR620208.fastq.gz ./output/003/trimmed_SRR620208.fastq.gz ILLUMINACLIP:./data/TruSeq3-SE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36
