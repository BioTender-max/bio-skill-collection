#!/bin/sh

input_bam=$1
prefix=$2

samtools sort -o $prefix.sorted.bam -T $prefix.tmp.bam $input_bam
samtools index $prefix.sorted.bam

