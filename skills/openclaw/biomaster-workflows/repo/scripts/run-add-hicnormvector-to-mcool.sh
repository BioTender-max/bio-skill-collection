#!/bin/bash

input_hic=$1
input_mcool=$2
outdir=$3

output_mcool=$outdir/output.mcool
cp $input_mcool $output_mcool 

cd $outdir

scriptdir=/usr/local/bin/
hic2cool extract-norms -e $input_hic $output_mcool

