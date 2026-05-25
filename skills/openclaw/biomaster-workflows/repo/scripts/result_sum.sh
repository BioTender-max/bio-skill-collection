dir1=$1
dir2=$2
alignment_stats=$3
gene_abundance=$4
basecall=$5
report_dir=$6
mkdir -p $report_dir
cp -r $dir1 $dir2 $alignment_stats $gene_abundance $basecall $report_dir