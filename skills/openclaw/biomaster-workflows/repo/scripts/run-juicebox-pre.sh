#!/bin/bash
shopt -s extglob
mapqfilter=0
min_res=5000
maxmem=64g
higlass=0  # if 1, higlass-compatible aggregation
custom_res=''  # custom resolutions, separated by commas
normonly=0  # if 1, normalization only
balance=1  # if 0, no normalization
output_prefix=out

printHelpAndExit() {
    echo "Usage: ${0##*/} [-q mapqfilter] [-m maxmem] [-r min_res] [-g] [-o out_prefix] -i input_pairs -c chromsize_file"
    echo "-i input_pairs : input file in pairs.gz format"
    echo "-c chromsize_file : chromsizes file"
    echo "-o out_prefix : default out"
    echo "-q mapqfilter : default 0"
    echo "-m maxmem : default 64g"
    echo "-r min_res : default 5000"
    echo "-g : use HiGlass resolutions (default juicer resolutions)"
    echo "-u : custom resolutions (separated by comman)"
    echo "-n : normalization only"
    echo "-B : no balancing/normalization"
    exit "$1"
}

while getopts "i:c:q:r:m:go:nu:B" opt; do
    case $opt in
        i) input_pairs=$OPTARG;;
        c) chromsizefile=$OPTARG;;
        q) mapqfilter=$OPTARG;;
        r) min_res=$OPTARG;;
        m) maxmem=$OPTARG;;
        g) higlass=1 ;;
        u) custom_res=$OPTARG;;
        n) normonly=1 ;;
        B) balance=0 ;;
        o) output_prefix=$OPTARG;;
        h) printHelpAndExit 0;;
        [?]) printHelpAndExit 1;;
        esac
done



# error when both higlass and custom_res are set
if [[ $higlass == '1' && ! -z $custom_res ]]
then
    echo "Do you want higlass resolution (-g) or custom-resolution (-u)? Make up your mind! :)"
    exit 1
fi


# error when custom resolution clashes with min_res
if [[ ! -z $custom_res ]]
then
    lowest_custom_res=${custom_res//,*/} 
    if [[ $lowest_custom_res != $min_res ]]
    then
        echo "Lowest custom res (-u) does not match min_res (-r)."
        exit 1
    fi
fi


# error when default juicer resolution clashes with min_res
if [[ $higlass == '0' && -z $custom_res ]]
then
    if [[ $min_res != '5000' ]]
    then
        echo "min_res (-r) should be 5000 for default juicer resolutions."
        exit 1
    fi
fi


# aggregation
if [[ $normonly == '0' ]]
then

    # creating a hic file
    if [[ $higlass == '1' ]]
    then
        reslist=$(python3 -c "from cooler.contrib import higlass; higlass.print_zoom_resolutions('$chromsizefile', $min_res)")
        java -Xmx$maxmem -Xms$maxmem -jar /usr/local/bin/juicer_tools.jar pre -n $input_pairs $output_prefix.hic $chromsizefile -r $reslist -q $mapqfilter
    elif [[ ! -z $custom_res ]]
    then
        java -Xmx$maxmem -Xms$maxmem -jar /usr/local/bin/juicer_tools.jar pre -n $input_pairs $output_prefix.hic $chromsizefile -r $custom_res -q $mapqfilter
    else
        java -Xmx$maxmem -Xms$maxmem -jar /usr/local/bin/juicer_tools.jar pre -n $input_pairs $output_prefix.hic $chromsizefile -q $mapqfilter
    fi
fi


# normalization
if [[ $balance == '1' ]]
then
  java -Xmx$maxmem -Xms$maxmem -jar /usr/local/bin/juicer_tools.jar addNorm -w $min_res -d -F $output_prefix.hic
fi

