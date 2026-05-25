fq=$1 
fast5dir=$2
sortedBam=$3
ref=$4
npsummary=$5
numcore=$6
np_out=$7
#需根据实际nanopolish路径调整
../nanopolish/nanopolish index -d $fast5dir $fq
export HDF5_PLUGIN_PATH=/home/sirui/anaconda3/envs/x/envs/ai/hdf5/lib/plugin
../nanopolish/nanopolish eventalign --reads $fq --bam $sortedBam --genome $ref --summary $npsummary --print-read-names --threads $numcore --scale-events > $np_out