#!/bin/bash
input_hic=$1
output_prefix=$2
min_res=$3   # e.g. 5000
maxmem=$4   # e.g. 64g

cp $input_hic $output_prefix.hic

# normalization
java -Xmx$maxmem -Xms$maxmem -jar /usr/local/bin/juicer_tools.jar addNorm -w $min_res -d -F $output_prefix.hic


