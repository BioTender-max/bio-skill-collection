#!/bin/bash
input_pairs=$1
chromsize=$2
sample_name=$3
enzyme=$4 # either 4 or 6
outdir=$5
max_distance=$6

scriptdir=/usr/local/bin/pairsqc/
python3 $scriptdir/pairsqc.py -p $input_pairs -c $chromsize -tP -s $sample_name -O $sample_name -M $max_distance
Rscript $scriptdir/plot.r $enzyme $sample_name\_report
zip -r $sample_name\_report.zip $sample_name\_report
if [[ $outdir != "." ]]; then
  mkdir -p $outdir
  mv $sample_name\_report.zip $outdir
fi
