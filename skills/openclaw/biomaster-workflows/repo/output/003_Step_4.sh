#!/bin/bash
which python
conda config --set show_channel_urls false
conda config --add channels conda-forge
conda config --add channels bioconda
conda install -y macs3
macs3 callpeak -t ./output/003/aligned_dedup_SRR620205.bam -c ./output/003/aligned_dedup_SRR620208.bam -f BAM -g mm -n cbx7_peaks --outdir ./output/003
