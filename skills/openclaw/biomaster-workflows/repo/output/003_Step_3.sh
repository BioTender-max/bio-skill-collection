#!/bin/bash
which python
conda config --set show_channel_urls false
conda config --add channels conda-forge
conda config --add channels bioconda
conda install -y samtools picard openjdk=17
samtools sort -o ./output/003/aligned_sorted_SRR620205.bam ./output/003/aligned_SRR620205.sam
samtools index ./output/003/aligned_sorted_SRR620205.bam
picard MarkDuplicates INPUT=./output/003/aligned_sorted_SRR620205.bam OUTPUT=./output/003/aligned_dedup_SRR620205.bam METRICS_FILE=./output/003/dedup_metrics_SRR620205.txt REMOVE_DUPLICATES=true VALIDATION_STRINGENCY=SILENT
samtools index ./output/003/aligned_dedup_SRR620205.bam
samtools sort -o ./output/003/aligned_sorted_SRR620208.bam ./output/003/aligned_SRR620208.sam
samtools index ./output/003/aligned_sorted_SRR620208.bam
picard MarkDuplicates INPUT=./output/003/aligned_sorted_SRR620208.bam OUTPUT=./output/003/aligned_dedup_SRR620208.bam METRICS_FILE=./output/003/dedup_metrics_SRR620208.txt REMOVE_DUPLICATES=true VALIDATION_STRINGENCY=SILENT
samtools index ./output/003/aligned_dedup_SRR620208.bam
