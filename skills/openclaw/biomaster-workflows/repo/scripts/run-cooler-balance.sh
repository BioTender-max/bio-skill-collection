#!/bin/sh
cool_file=$1  # bgzipped, with .px2 index
max_iter=$2
out_prefix=$3
chunksize=$4 # default: 10000000

# matrix balancing
cp $cool_file $out_prefix.cool
cooler balance --max-iters $max_iter --chunksize $chunksize $out_prefix.cool


