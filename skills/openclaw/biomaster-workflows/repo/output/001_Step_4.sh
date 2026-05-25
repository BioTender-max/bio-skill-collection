#!/bin/bash
which python
conda config --set show_channel_urls false
conda config --add channels conda-forge
conda config --add channels bioconda
mkdir -p ./output/001
conda install -y gatk
gatk AddOrReplaceReadGroups -I ./output/001/sorted_aligned_reads.bam -O ./output/001/sorted_aligned_reads_rg.bam -RGID 1 -RGLB lib1 -RGPL illumina -RGPU unit1 -RGSM sample1
gatk MarkDuplicates -I ./output/001/sorted_aligned_reads_rg.bam -O ./output/001/dedup_sorted_aligned_reads.bam -M ./output/001/marked_dup_metrics.txt
gatk BuildBamIndex -I ./output/001/dedup_sorted_aligned_reads.bam
