#!/bin/sh
outdir=$1
outprefix=$2
enzyme=$3
shift;  # array of report zip files
scriptdir=/usr/local/bin/pairsqc/

outreportdir=$outprefix\_report
mkdir -p $outreportdir

for file in $@
do
  unzip $file
done

for reportdir in `ls -1d *_report`
do
  cp -r reportdir/* $outreportdir/
done
rm -rf $outreportdir/plots/

Rscript $scriptdir/plot.r $enzyme $outreportdir
zip $outreportdir.zip $outreportdir
mv $outreportdir.zip $outdir

