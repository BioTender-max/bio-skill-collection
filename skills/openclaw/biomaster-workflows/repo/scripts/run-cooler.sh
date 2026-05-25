#!/bin/sh
pairs_file=$1  # bgzipped, with .px2 index
chrsize_file=$2
bin_size=$3
ncores=$4 # (default 8)
out_prefix=$5
max_split=$6 # (default 2)

cp $chrsize_file ./tmpchrsize

# make bin file (skipped)
# cooler makebins -o ./tmpchrsize:$bin_size ./tmpchrsize $bin_size

# the cload command requires the chrom size file to exist besides the chrom size bin file.
cooler cload pairix -p $ncores -s $max_split ./tmpchrsize:$bin_size $pairs_file $out_prefix.cool

