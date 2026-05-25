#!/bin/bash
shopt -s extglob
ncores=1
chunksize=10000000
juicer_res=0  # if 1, use juicer resolutions
custom_res=''  # custom resolutions, separated by commas
balance=1
outprefix=out

printHelpAndExit() {
    echo "Usage: ${0##*/} [-p ncores] [-c chunksize] [-j] [-o out_prefix] -i input_cool"
    echo "-i input_cool : input file in .cool format"
    echo "-o out_prefix : default out"
    echo "-p ncores : default 1"
    echo "-c chunksize : default 10000000"
    echo "-j : use Juicer resolutions (default HiGlass resolutions)"
    echo "-u : custom resolutions (separated by commas)"
    echo "-B : no balance"
    exit "$1"
}

while getopts "i:o:p:c:ju:B" opt; do
    case $opt in
        i) input=$OPTARG;;
        o) outprefix=$OPTARG;;
        p) ncores=$OPTARG;;
        c) chunksize=$OPTARG;;
        j) juicer_res=1;;
        u) custom_res=$OPTARG;;
        B) balance=0;;
        h) printHelpAndExit 0;;
        [?]) printHelpAndExit 1;;
        esac
done


if [[ $juicer_res == "1" && ! -z $custom_res ]]; then
    echo "Do you want juicer resolutions (-j) or custom resolutions (-u)? Make up your mind! :)"
    exit 1
fi

if [[ $juicer_res == "1" ]]; then
    RES_ARG="-r 5000,10000,25000,50000,100000,250000,500000,1000000,2500000"
fi

if [[ ! -z $custom_res ]]; then
    RES_ARG="-r $custom_res"
fi

if [[ $balance == "1" ]]; then
    cooler zoomify --balance --balance-args '--convergence-policy store_nan' -n $ncores -o $outprefix.multires.cool -c $chunksize $RES_ARG $input
else
    cooler zoomify -n $ncores -o $outprefix.multires.cool -c $chunksize $RES_ARG $input
fi


