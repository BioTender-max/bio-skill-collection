#!/bin/bash
shopt -s extglob
input_pairs=''
restriction_file=''  # Juicer format
output_prefix=out

printHelpAndExit() {
    echo "Usage: ${0##*/} [-o out_prefix] -i input_pairs -r restriction_site_file"
    echo "-i input_pairs : input file in pairs.gz format"
    echo "-r restriction_site_file : restriction site file"
    echo "-o out_prefix : default out"
    exit "$1"
}

while getopts "i:r:o:h" opt; do
    case $opt in
        i) input_pairs=$OPTARG;;
        r) restriction_file=$OPTARG;;
        o) output_prefix=$OPTARG;;
        h) printHelpAndExit 0;;
        [?]) printHelpAndExit 1;;
        esac
done


if [ ! -z $restriction_file ]; then
    scriptdir=/usr/local/bin
    # use fragment_4dnpairs.pl in pairix/util instead of juicer/CPU/common
    gunzip -c $input_pairs | $scriptdir/pairix/util/fragment_4dnpairs.pl -a - $output_prefix.ff.pairs $restriction_file
    bgzip -f $output_prefix.ff.pairs
    pairix -f $output_prefix.ff.pairs.gz
else
    cp $input_pairs $output_prefix.ff.pairs.gz
    if [ -e "$input_pairs.px2" ]; then
        cp $input_pairs.px2 $output_prefix.ff.pairs.gz.px2
    else
        pairix -f $output_prefix.ff.pairs.gz
    fi
fi
