#!/bin/bash

inputfile=$1
nthread=$2
outdir=$3

mkdir -p $outdir

if [[ $inputfile =~ \.gz$ ]]
then
  cp $inputfile $outdir/data.fastq.gz
  fastqc -t $nthread $outdir/data.fastq.gz
else
  cp $inputfile $outdir/data.fastq
  fastqc -t $nthread $outdir/data.fastq
fi


